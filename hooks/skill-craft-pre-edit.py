#!/usr/bin/env python3
"""
PreToolUse hook — reminds AI to invoke skill-craft when editing skill
canonical files.

Trigger: Edit, Write, NotebookEdit tool calls.
Condition: target file_path matches skill canonical patterns
  (plugin/skills/<skill>/{SKILL,PROCEDURE}.md, references/*.md,
  phases/*.md) OR framework-spec paths (spec/*.md,
  development-process.md).
Action: inject reminder via Claude Code hook protocol
  (additionalContext) — does NOT block the edit.

The reminder fires the per-edit-cycle discipline (per
anneal-framework/development-process.md practice 5) without
requiring the AI to recall from memory or CLAUDE.md.

Bypass: none needed — hook only adds context, never blocks.
"""

import json
import re
import sys

# Skill canonical paths + framework-spec paths.
# Matched against absolute paths in tool_input.file_path.
SKILL_PATH_PATTERNS = [
    # Skill canonical files (any plugin's skill directory)
    re.compile(r"/plugin/skills/[^/]+/(SKILL|PROCEDURE)\.md$"),
    re.compile(r"/plugin/skills/[^/]+/references/[^/]+\.md$"),
    re.compile(r"/plugin/skills/[^/]+/phases/[^/]+\.md$"),
    # Framework-spec paths
    re.compile(r"/spec/.+\.md$"),
    re.compile(r"/development-process\.md$"),
]

REMINDER_TEMPLATE = """Skill canonical-file edit detected: {file_path}

This file is in skill-craft scope — per anneal-framework
development-process.md practice 5, skill-craft must be invoked
via the Skill tool BEFORE the edit for this scope (per
edit cycle, not per session).

If skill-craft has NOT been invoked this session for the current
edit scope:
  → Invoke now: Skill(skill="skill-craft:skill-craft", args="...")
  → The invocation auto-loads anti-patterns.md, which supplies
    Form-choice, Edit-as-Pareto, Naked-judgment, Skip-rationalization,
    Soft-load-pointers, Additive-reflex — the disciplines you must
    apply at DRAFTING time, not only at validation.

If skill-craft IS already invoked for this scope:
  → Proceed with the edit. The disciplines should be active in context.
  → Apply Amendment discipline (path 1: revise > 2: merge >
    3: extend > 4: add new sub-section) before any addition.
  → Edit-as-Pareto: name what reduces or consolidates; pure addition
    without coverage gain is the bloat path.

If this edit is repo-housekeeping (README, .gitignore, CI config,
plugin.json version-only bump) rather than rule-corpus content:
  → Skill-craft does not apply. Proceed.
"""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Invalid hook input — don't block, just exit.
        return 0

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        return 0

    is_skill_file = any(p.search(file_path) for p in SKILL_PATH_PATTERNS)

    if not is_skill_file:
        return 0

    reminder = REMINDER_TEMPLATE.format(file_path=file_path)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": reminder,
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
