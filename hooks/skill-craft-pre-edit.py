#!/usr/bin/env python3
"""
PreToolUse hook — gates Edit/Write/NotebookEdit on rule-corpus files
behind a per-turn transcript-verified skill-craft invocation.

Trigger: Edit, Write, NotebookEdit tool calls on rule-corpus files:
  - Plugin render paths (plugin/skills/<skill>/{SKILL,PROCEDURE}.md,
    references/*.md, phases/*.md)
  - Framework-spec paths (spec/*.md, development-process.md,
    post-run-review.md, instantiation-guide.md, foundation.md)

Action:
  - Scans the JSONL transcript from the last operator prompt (a
    user message with text content, NOT a tool_result message)
    forward, looking for a Skill tool_use invoking skill-craft.
  - If found in the current turn → allow (exit 0). For plugin
    renders (excluding skill-craft canonical), additionally inject
    spec-origin reminder via additionalContext.
  - If not found in the current turn → block (exit 2 with
    permissionDecision: deny). Forces AI to invoke skill-craft via
    Skill tool in this turn before proceeding.

Per anneal-framework development-process.md practice 5: skill-craft
invocation gates Edits to rule-corpus files. Per-turn enforcement
aligns the gate with operator-request boundaries — a new operator
message starts a new turn requiring fresh invocation. Mid-turn
cycle boundaries remain an AI-discipline goal (multiple scopes of
change within one operator response are not mechanically separated).

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

DENY_REASON = """skill-craft invocation required in the current turn
before Edit/Write to rule-corpus files. No Skill tool_use with
skill-craft was found in the transcript since the last operator
message.

To proceed:
  1. Invoke skill-craft via the Skill tool:
     Skill(skill="skill-craft:skill-craft")
  2. Retry this Edit/Write — the hook will scan again and allow.

Per anneal-framework development-process.md practice 5
(skill-craft invocation gates Edits to rule-corpus files;
per-turn enforcement at the transcript-scan layer). Invocations
in prior turns do NOT discharge the current turn's gate; each
operator message starts a fresh enforcement window."""

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


def has_skill_craft_invocation_this_turn(transcript_path: str) -> bool:
    """Scan the JSONL transcript: find the last operator-prompt
    user message (a user-role event with isMeta unset, origin
    unset, and text/string content), then check if any subsequent
    assistant Skill skill-craft tool_use exists.

    Returns True if skill-craft was invoked since the last
    operator prompt, False otherwise.

    Fail-open policy: returns True ("allow the Edit") on any of
    the following failure modes — the True here is NOT
    "invocation found"; it's "couldn't verify, so don't block."
    Caller treats True as the allow-condition.

      1. Transcript file unreadable (OSError/IOError).
      2. No operator-prompt boundary found in events (empty
         events list, malformed JSONL with all lines unparseable,
         or all user events filtered as non-prompts — should not
         happen in normal operation)."""
    try:
        events = []
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except (OSError, IOError):
        # Transcript unreadable — fail-open. Defensive: should not
        # happen in normal operation.
        return True

    # Find index of last operator-prompt user message. Discriminators
    # observed in Claude Code transcripts:
    #   - isMeta=True user-role events carry Skill outputs and system
    #     notifications as text content under role=user. Skip them.
    #   - Non-empty `origin` field marks non-prompt user events
    #     (e.g., {'kind': 'task-notification'} from subagent
    #     completions). Real operator prompts have no `origin`.
    #     Skip them.
    #   - Tool-result user events have content as a list with
    #     tool_result blocks (no text block). Skip them via the
    #     content-shape check below.
    #   - Operator prompts: role=user, isMeta is None/absent, origin
    #     is None/absent, content is a string (or list with at least
    #     one text block).
    last_prompt_idx = -1
    for i, event in enumerate(events):
        msg = event.get("message")
        if not isinstance(msg, dict):
            continue
        if msg.get("role") != "user":
            continue
        if event.get("isMeta") is True:
            continue
        if event.get("origin"):
            continue
        content = msg.get("content")
        if isinstance(content, str):
            last_prompt_idx = i
            continue
        if not isinstance(content, list):
            continue
        if any(
            isinstance(b, dict) and b.get("type") == "text"
            for b in content
        ):
            last_prompt_idx = i

    if last_prompt_idx == -1:
        # No user prompt found yet — degenerate case (very early in
        # session, before any prompt). Fail-open.
        return True

    # Scan events after the last operator prompt for any Skill
    # tool_use invoking skill-craft.
    for event in events[last_prompt_idx + 1:]:
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

    # Rule-corpus file — gate on per-turn-verified skill-craft invocation.
    if not transcript_path:
        # No transcript path provided — fail-open (don't block).
        # Defensive: should not happen in normal operation.
        return 0

    if not has_skill_craft_invocation_this_turn(transcript_path):
        deny(DENY_REASON)
        # Unreachable; deny() exits.

    # Skill-craft was invoked in the current turn. Allow, with
    # informational spec-origin reminder for plugin renders (except
    # skill-craft canonical, which IS source not render).
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
