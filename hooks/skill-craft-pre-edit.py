#!/usr/bin/env python3
"""
PreToolUse hook — gates Edit/Write/NotebookEdit on rule-corpus files
behind a transcript-verified skill-craft invocation (Path A).

Trigger: Edit, Write, NotebookEdit tool calls on rule-corpus files:
  - Plugin render paths (plugin/skills/<skill>/{SKILL,PROCEDURE}.md,
    references/*.md, phases/*.md)
  - Framework-spec paths (spec/*.md, development-process.md,
    post-run-review.md, instantiation-guide.md, foundation.md)

Action:
  - Scans the session transcript (transcript_path from hook input)
    for any prior Skill tool_use invoking skill-craft.
  - If found → allow (exit 0). For plugin renders (excluding
    skill-craft canonical), additionally inject spec-origin reminder
    via additionalContext.
  - If not found → block (exit 2 with permissionDecision: deny).
    Forces AI to invoke skill-craft via Skill tool before proceeding.

Per anneal-framework development-process.md practice 5: skill-craft
invocation gates Edits to rule-corpus files. Session-level
enforcement at the system layer; per-cycle re-invocation remains an
AI-discipline goal (not mechanically detectable from transcript).

Housekeeping carve-out: files outside the rule-corpus patterns
(README.md, .gitignore, plugin.json version bumps) pass without
gating.
"""

import json
import re
import sys

# Plugin render paths (instance plugin files — rendered from spec).
PLUGIN_RENDER_PATTERNS = [
    re.compile(r"/plugin/skills/[^/]+/(SKILL|PROCEDURE)\.md$"),
    re.compile(r"/plugin/skills/[^/]+/references/[^/]+\.md$"),
    re.compile(r"/plugin/skills/[^/]+/phases/[^/]+\.md$"),
]

# Framework-spec / dev-process paths (source files — canonical content).
SPEC_SOURCE_PATTERNS = [
    re.compile(r"/spec/.+\.md$"),
    re.compile(r"/development-process\.md$"),
    re.compile(r"/post-run-review\.md$"),
    re.compile(r"/instantiation-guide\.md$"),
    re.compile(r"/foundation\.md$"),
]

# Skill-craft canonical exemption — skill-craft is a meta-plugin where
# canonical files ARE the source (no upstream render). Spec-origin
# discipline doesn't apply.
SKILL_CRAFT_CANONICAL = re.compile(r"/skill-craft/plugin/skills/skill-craft/")

# Skill-craft invocation pattern — matches any Skill tool_use whose
# `skill` input includes "skill-craft" (covers "skill-craft:skill-craft",
# "plugin:skill-craft:skill-craft", and similar fully-qualified forms).
SKILL_CRAFT_INVOCATION = re.compile(r"skill-craft")

DENY_REASON = """skill-craft invocation required before Edit/Write to
rule-corpus files. No prior Skill tool_use with skill-craft was found
in this session's transcript.

To proceed:
  1. Invoke skill-craft via the Skill tool:
     Skill(skill="skill-craft:skill-craft")
  2. Retry this Edit/Write — the hook will scan the transcript again
     and allow.

Per anneal-framework development-process.md practice 5
(skill-craft invocation gates Edits to rule-corpus files;
system-side enforcement at the transcript-scan layer)."""

SPEC_ORIGIN_REMINDER = """Spec-origin trace required for this plugin
render edit (per anneal-framework development-process.md practice 5
"Spec-origin grounding for plugin edits" + contract 2). Surface which
spec clause this edit originates from:
  → framework spec section (anneal-framework/spec/*.md), OR
  → instance spec slot (e.g., coding-clippy/spec/*.md), OR
  → `cosmetic-no-spec-origin` exemption with sources considered.

The citation IS the artifact; a plugin edit without a cited spec
origin is drift (Edit-without-spec-origin anti-pattern,
skill-craft references/anti-patterns.md)."""


def has_skill_craft_invocation(transcript_path: str) -> bool:
    """Scan the JSONL transcript for any Skill tool_use invoking
    skill-craft. Returns True if found, False otherwise."""
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = event.get("message")
                if not isinstance(msg, dict):
                    continue
                if msg.get("role") != "assistant":
                    continue
                content = msg.get("content", [])
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") != "tool_use":
                        continue
                    if block.get("name") != "Skill":
                        continue
                    tool_input = block.get("input", {})
                    if not isinstance(tool_input, dict):
                        continue
                    skill = tool_input.get("skill", "")
                    if SKILL_CRAFT_INVOCATION.search(str(skill)):
                        return True
    except (OSError, IOError):
        # Transcript unreadable — fail-open: return True to allow the
        # Edit. The True here is NOT "invocation found"; it's
        # "couldn't verify, so don't block." Caller treats True as the
        # allow-condition (whether by verified invocation or by
        # unverifiability). Defensive: should not happen in normal
        # operation.
        return True
    return False


def deny(reason: str) -> None:
    """Emit deny payload and exit with code 2 (hard block)."""
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
        },
        "systemMessage": f"Blocked: {reason}",
    }
    sys.stderr.write(json.dumps(payload))
    sys.exit(2)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Invalid hook input — don't block, just exit.
        return 0

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    transcript_path = payload.get("transcript_path", "")

    if not file_path:
        return 0

    is_plugin_render = any(p.search(file_path) for p in PLUGIN_RENDER_PATTERNS)
    is_spec_source = any(p.search(file_path) for p in SPEC_SOURCE_PATTERNS)
    is_sc_canonical = bool(SKILL_CRAFT_CANONICAL.search(file_path))

    if not (is_plugin_render or is_spec_source):
        # Not a rule-corpus file — out of scope, allow.
        return 0

    # Rule-corpus file — gate on transcript-verified skill-craft invocation.
    if not transcript_path:
        # No transcript path provided — fail-open (don't block).
        # Defensive: should not happen in normal operation.
        return 0

    if not has_skill_craft_invocation(transcript_path):
        deny(DENY_REASON)
        # Unreachable; deny() exits.

    # Skill-craft was invoked. Allow, with informational spec-origin
    # reminder for plugin renders (except skill-craft canonical, which
    # IS source not render).
    if is_plugin_render and not is_sc_canonical:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": SPEC_ORIGIN_REMINDER,
            }
        }
        print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
