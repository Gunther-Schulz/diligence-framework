# Anneal Framework

> Convert AI confidence into AI evidence.

A domain-agnostic methodology for taking an AI through an open-ended
task to a verified outcome. Bound to a domain in an **instance** like
[Clippy](https://github.com/Gunther-Schulz/coding-clippy) (building
software) or [DANEEL](https://github.com/Gunther-Schulz/daneel)
(debugging it).

If you use Clippy or DANEEL, this is what's under them. If you want
to build a new instance for your domain, start with
[`instantiation-guide.md`](./instantiation-guide.md).

## What it holds

Two invariants every instance inherits:

1. **Grounded claims.** Every load-bearing claim carries a *basis* —
   a search result, or a `file:line` citation with an observable fact
   about what's there — or is marked as an assumption. AI confidence
   is not evidence.
2. **A coherent picture.** Every concern carries a status in the
   tracker. Nothing is silently dropped; the view does not narrow or
   circle. The design is held whole, not in working memory.

## How a cycle works

Each cycle has two passes — **investigation** (the AI looks at
relevant surfaces with task-derived lenses) and **standardized
inspection** (the pre-written lens set applied to what the cycle's
work touched). Design work — committing positions on what to build
— interleaves within the cycle, not as a separate pass. Findings
land in the **F-track**; design decisions in the **D-track**. The
cycle ends when both tracks settle and the standardized pass is
clean; otherwise the AI recommends another cycle, justified by
what's still open. Cost is the operator's judgment, not the AI's.

## A tracker excerpt

What the framework actually produces — every line evidence-grounded:

```
F12 [VERIFIED] handleSubmit lacks input validation
  Basis: form.tsx:42 (read) —
    `const handleSubmit = (e) => { e.preventDefault(); onSubmit(data) }`

D5 [VERIFIED] Add validation to handleSubmit before onSubmit
  Basis: F12 + signup.tsx:67-82 (read) showing the project's
         established validation pattern
```

A claim without a basis is held as an assumption until grounded —
it does not advance the run.

## Architecture

```
       Anneal framework (spec/)
                  ↓
            renders to
                  ↓
      ┌───────────┴───────────┐
      ↓                       ↓
 ┌────────┐              ┌────────┐
 │ Clippy │              │ DANEEL │
 │ build  │              │ debug  │
 └────────┘              └────────┘
            ↓        ↓
         coding (domain)
```

Both instances inherit the framework's structural discipline (basis
rule, status-state machine, phase pipeline). They differ in domain
binding and lens set.

## Available instances

| Instance | Domain | Repo |
|---|---|---|
| **Clippy** | Building software | [coding-clippy](https://github.com/Gunther-Schulz/coding-clippy) |
| **DANEEL** | Debugging wrong behavior | [daneel](https://github.com/Gunther-Schulz/daneel) |

## This repo

- [`foundation.md`](./foundation.md) — the three architectural
  contracts (framework arbitrariness / render completeness /
  instance domain-binding scope). Upstream anchor that
  development-process.md and instantiation-guide.md both
  operate within.
- [`spec/`](./spec/) — the framework specification. The
  domain-agnostic source of truth instances are rendered from.
- [`instantiation-guide.md`](./instantiation-guide.md) — how to
  derive a new Anneal-based plugin for your domain.
- [`instance-template/`](./instance-template/) — starter scaffold
  for a new instance. One placeholder file per slot the framework
  recognises; copy as the seed for a new instance repo and fill /
  delete per the instantiation guide.
- [`development-process.md`](./development-process.md) — how this
  repo and its instances evolve. Codifies the architectural
  foundation (framework / render / instance contracts), the
  development practices, and the release loop with its
  step-5 discharge artifact.
- [`post-run-review.md`](./post-run-review.md) — the framework's
  empirical-validation procedure (the Q-set for analyzing a real
  run against the spec; rendered into each instance's
  `references/post-run-review.md`).
- [`hooks/`](./hooks/) — hooks that enforce the development
  process. The `commit-msg` git hook validates the step-5
  discharge artifact for rule-corpus commits (rejects commits
  missing required check labels or carrying fold-into
  rationalizations). The `skill-craft-pre-edit.py` PreToolUse hook
  (configured in user settings) fires on Edit/Write/NotebookEdit
  to skill-craft, framework spec, or instance skill files —
  scans the session transcript and BLOCKS the Edit if no Skill
  tool_use invoking skill-craft is found; allows once invoked.
  Plugin renders additionally receive a spec-origin reminder.

## License

MIT
