# Development process

This document is the development process for evolving the
**diligence-framework**, **skill-craft**, and the framework's
**instances** (such as `coding-clippy`). It covers development work
*on* these repos — distinct from `instantiation-guide.md`, which
covers deriving a new instance from the framework.

A fresh session does not hold this process by default. Read and
adopt it before doing development work here.

## The three levels

Three repositories, three levels of abstraction:

- **skill-craft** — how to build and review any Claude Code skill:
  structural-enforcement mechanisms (forcing functions, blocking
  gates, observable checkpoints, menus), protocol conventions, skill
  architecture. Domain-agnostic and skill-agnostic.
- **diligence-framework** — the one domain-general methodology: the
  investigate-design / implement / verify phases, the tracker, the
  status-state machine, the basis rule, the
  evidence-bearing-artifact rule. Built *using* skill-craft's mechanisms.
- **An instance** — the framework bound to a domain and rendered into
  a working plugin. `coding-clippy` is the instance for software
  engineering. An instance is *rendered* — paraphrased, with domain
  bindings — from the framework spec.

A change belongs at the highest level at which it is true. Work flows
down: skill-craft informs the framework; the framework is rendered
into instances.

## The practices

### 1. Fix at the source

A problem that surfaces in an instance is rarely the instance's to
fix. Diagnose which level it belongs to — a skill-design weakness
(skill-craft), a methodology gap (framework), or a genuine domain
binding (instance) — and fix it *there*, then re-render downward.
Patching the instance directly hides the real gap; the same fault
recurs in the next render, or the next instance.

A deviation found by running the instance is triaged to its level: an
*adherence gap* — the instance did not follow the spec → fix the
instance's render; a *spec gap* — it followed the spec and still
broke → a finding for the framework or the instance spec; a
*conformant success* — it followed and worked → a positive signal,
logged to `spec/validation-watch.md`.

### 2. Rendering is lossy — renderer ≠ verifier

An instance is rendered from the framework spec by paraphrase.
Paraphrase silently flattens structural rules into soft prose ("must"
becomes "should") and drops clauses. The renderer cannot see its own
flattening — it reads its output as faithful. So every render is
verified by a **separate context** — a fresh subagent, or a different
party — by clause-level diff against the source. The context that
produced a render never verifies it. What "faithful" requires — the
rendering-fidelity rule itself — is skill-craft's (`Rendering from a
source`).

### 3. Subagents for context-heavy work

Transcript analysis, large audits, multi-file renders, and
verification all consume context. Delegate them to a subagent with a
self-contained brief and an explicit concise-report requirement; the
main session stays lean. A sub-agent's **facts** — cited file:line —
can be relied on; its **recommendations and interpretation** are
re-checked against the framework before being acted on, because a
sub-agent's framing reflects its brief, not the full context.

### 4. A contract change audits every dependent

When a rule, a shape, or a status changes, that is a contract
change. Grep for *every* spot that encodes the old contract — across
all three repos — including the changed file itself: an intra-file or
intra-repo dependent is the easiest to miss. A found instance is the
*start* of the audit, not the end; the question is always "what is
the class, and where else does it live."

### 5. Ground before asserting or editing

Re-read the exact current text of a passage before editing it —
stale assumptions about wording cause failed edits. Check
`git status` and `git log` before claiming the state of a repo.
Never assert current state from memory or from a document written
earlier; verify against the live source.

### 6. Integrate, don't insert

An edit integrates a change into a document that must stay coherent
as a whole — it is not the insertion of correct content at a
plausible spot. Hold the whole document's structure in view before
editing; after, it is no muddier than before — right placement,
weight proportional to the change's importance, no prose accreted
where a list belongs. Where accretion has already happened,
re-deriving the structure is part of the edit. The local check — "is
the new content correct" — always passes while the whole degrades;
the check that matters is whether the document, as a whole, still
coheres. A substantive edit's coherence is verified in a separate
context (practice 2's isolation, applied to structure).

### 7. Honest trade-offs, and proportionality

Every design proposal names its real cost, not only its benefit.
Push back on an idea — including the operator's — when the reasoning
warrants it. Do not over-build: no machinery for a hypothetical
future need. Promote a pattern to a higher level (instance →
framework, or framework → skill-craft) only when a *second* user
appears — the rule of three. Until then it lives where it is used.

### 8. Design, then decide, then implement

Surface a design and its genuine choices and trade-offs before
building. The operator decides. Only then implement — at the source
level, re-rendered, verified. Do not accrete a design through
implementation, and do not implement past the point the operator has
agreed.

## The release loop

A change runs the same loop:

1. **Diagnose the level** — skill-craft, framework, or instance
   (practice 1).
2. **Fix at the source** — edit the spec at the level the change
   belongs to.
3. **Commit the source repo** — a clear message stating what changed
   and why.
4. **Re-render** the affected instance files from the corrected spec
   — faithfully, clause by clause.
5. **Verify** — each check below, in a separate context where it
   requires one:
   - the render against its source (practice 2);
   - every dependent of a contract change (practice 4);
   - a changed skill file against skill-craft's full review;
   - a changed framework-spec section against skill-craft's
     protocol-quality lens (a spec is not a skill — its
     skill-structure checks do not apply);
   - the whole document a substantive edit touched, for coherence
     (practice 6).
6. **Release the instance** — version-bump the plugin, commit,
   reinstall.
7. **Persist outcomes** — real-run findings and deferred ideas in the
   instance's status log; process changes back into this document.
