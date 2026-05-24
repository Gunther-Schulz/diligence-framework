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

A deviation found by running the instance is triaged. A *render gap*
— the instance file does not faithfully carry the spec → fix the
render. A *spec gap* — the render is faithful, the AI followed it,
and it still broke → a finding for the framework or the instance
spec. A *conformant success* — followed and worked → a positive
signal, logged to `spec/validation-watch.md`. The subtle case is a
faithful render the AI did *not* follow: do not call it a render gap
by reflex. First test the rule for underspecification — if it was
loose enough to admit the violating reading, it fails the framework's
evidence-bearing standard (`spec/core.md` §3.1, that violating a
load-bearing rule produces no artifact) and is a *spec gap*: sharpen
the rule. Only a faithful render of an already-unambiguous,
evidence-bearing rule, violated anyway, is a true *adherence gap* —
not a render fix but the irreducible residual the verify, operator,
and loopback backstops carry.

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
future need.

**Foundation work** (framework spec, skill-craft, instance
foundations, load-bearing discipline) is judged at full discipline
— proportionality governs the details of an edit, not whether to
do foundational work at all. Under-building the foundation trades
a small near-term saving for a recurring downstream tax. When the
same discipline could fire at either stage, design-time placement
wins.

### 8. Structural-form gate for fixes

A failure surfacing invites a fix. The gate on the fix is its
**structural form**, not its occurrence count. Per skill-craft's
"Judgment calls as design risk", every rule the AI must follow
has one of three forms: **mechanical criteria** (computed from
observable evidence), **structural enforcement** (artifact-shape
forcing function), or **safety net** (accept the AI will sometimes
fail; catch downstream). A fix in pure prose form is malformed —
it adds an unenforced suggestion. Both new mechanisms and fixes
to existing rules are gated by this classification: if classifiable
as one of the three, it earns its place at n=1; if not, keep
iterating on form, or accept the failure shape isn't tractable
for codification (operator catch remains).

**Validation-watch is not a deferral journal.** `spec/validation-
watch.md` records observations about framework design choices
made under *genuine uncertainty* — choices the framework
couldn't classify cleanly at decision time. Writing a V-N entry
whose Production-Signal section reads "if recurrent X, then
change Y" — where Y is a classifiable fix (mechanical criteria /
structural enforcement / safety net) earning its place at n=1 —
is cost-gating dressed as epistemic humility. The fix earns its
place now; the V-N entry, if written, records the observation
that produced the fix, not the deferral of the fix. Distinguish:
genuine uncertainty about a design choice's correctness =
validation-watch material; classifiable fix whose form is
already in hand = practice-8 n=1 commit material.

**Entry hygiene.** Validation-watch entries are scoped to their
own titled question. An observation that doesn't bear on that
question is either its own V-N entry (if it's genuine uncertainty
about a separate design choice) or doesn't belong in
validation-watch at all (if it's classifiable per the three forms,
or operator-side tracking, or a gap in some other doc). A
footnote-style observation tagging along inside an unrelated V-N
is a **stowaway** — same root failure as the deferral journal
(validation-watch used as a catch-all), different mechanism. The
entry's scope is its title; observations outside that scope earn
their own entry or live elsewhere.

### 9. Design, then decide, then implement

Surface a design and its **genuine choices** and trade-offs before
building. Genuine includes three things: (a) the **thorough-fix
option** (per `core.md` §1) — name it, lead with it, weigh
cheaper alternatives against it (not cheap-only menus); (b) for
any new rule, its **mitigation classification** per practice 8
(mechanical criteria / structural enforcement / safety net per
skill-craft's "Judgment calls as design risk"); (c) for any new
terminology proposed, **terminology quality** per skill-craft's
"Naked judgment in rule statements" anti-pattern — no term whose
meaning rests on AI judgment rather than observable property;
framework vocabulary collisions are flagged and replaced.

The AI takes operator wording as intent, not literal text;
improves where the intent supports a better expression. A design
surface omitting any of the three is malformed. Incremental steps
within an authorized workstream do not need ceremonial
confirmation, but crossing into implementation after a design
surface does. Only then implement — at the source level,
re-rendered, verified.

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
   - a changed skill file against skill-craft's full review
     (Layer 1 plugin structure + Layer 2 protocol conventions +
     Layer 4 evolution disciplines + all anti-patterns);
   - a changed framework-spec section (`spec/*.md`,
     `development-process.md`) against skill-craft's self-review
     mandate, with Check #1's canonical-rules iteration restricted
     to Layer 2 + Layer 4 + anti-patterns (Layer 1 skill-structure
     checks excluded). After commit:
     ```
     - [ ] Subagent dispatched with: commit SHA, changed-file list,
           instruction to load SKILL.md + PROCEDURE.md +
           references/anti-patterns.md from
           `skill-craft/plugin/skills/skill-craft/`?
       - NO → CANNOT proceed.
       - YES → Evidence: [loaded-references manifest from subagent]
     ```
     Recovery: blocking → revert; notable → operator amend
     decision (next-commit fix or accept-with-rationale); nit →
     surface for optional address.
   - the whole document a substantive edit touched, for coherence
     (practice 6).
6. **Release the instance** — version-bump the plugin, commit,
   reinstall.
7. **Persist outcomes** — real-run findings and deferred ideas in the
   instance's status log; process changes back into this document.
