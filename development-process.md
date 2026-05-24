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

A failure surfacing invites a fix. The gate on the fix is its
**structural form**, not its occurrence count. Per skill-craft's
"Judgment calls as design risk" (`PROCEDURE.md`), every rule the AI
must follow has one of three forms: **mechanical criteria** (computed
from observable evidence), **structural enforcement** (artifact-shape
forcing function), or **safety net** (accept the AI will sometimes
fail; catch downstream). A proposed fix in pure prose form — an "AI
must X" rule with none of the three backing it — is malformed; it
adds an unenforced suggestion (skill-craft anti-pattern: "Naked
judgment call"; "Procedure drift through incremental patches" /
adversarial tone). Both adding a new mechanism and fixing an existing
instruction are gated by this: can the fix be classified as one of
the three forms? If yes, it earns its place at n=1 — wait-for-
recurrence is the wrong gate (the recurrence isn't what makes the
fix valid; the structural form is). If no, the fix isn't ready —
keep iterating on form, or accept the failure shape isn't tractable
for codification at all (operator catch remains the catch).

The cost calculus differs for **foundation work** — work on the
framework spec, skill-craft, an instance's foundations, or
load-bearing discipline (`CLAUDE.md`, `JOURNAL.md` observations
driving amendments), as distinct from production work (running the
framework on a real task). Investment in the foundation amortizes
across every future run that uses it; under-building to save session
length or upfront design effort trades a small near-term saving for
a recurring downstream tax. Proportionality still governs the
*details* of an edit (what words, what sequencing); it does not gate
whether to do foundational work at all. The framework's
cost-asymmetry argument (`core.md` §4.1) — that an extra
investigate-design cycle costs one cycle while an
implement→investigate loopback is materially larger — applies to the
meta-level work as well: foundation work that strengthens
design-time discipline (sharpening basis-rule artifacts, lens
articulation, forcing functions on locked decisions) pays the
asymmetry down for every future run. When the same discipline could
fire at either stage, design-time placement wins.

### 8. Design, then decide, then implement

Surface a design and its **genuine choices** and trade-offs before
building. Genuine includes three things: (a) the **thorough-fix
option** — the AI's default disposition is to prefer the thorough
fix and lead with it, weighing cheaper alternatives honestly
against it (not to construct cheap-only menus); (b) for any new rule
the AI must follow, the rule's **mitigation classification** per
practice 7's structural-quality gate (mechanical criteria /
structural enforcement / safety net per skill-craft's "Judgment
calls as design risk"); and (c) for any new terminology proposed
(operator's first draft or AI's own), **terminology quality** per
skill-craft's "Moralistic, vague, or AI-judgment-coded terminology"
anti-pattern — the principle being *no term whose meaning rests on
the AI's own judgment rather than an observable property*; framework
vocabulary collisions are flagged and replaced. The AI
takes operator wording as intent, not literal text; improves where
the intent supports a better expression. A design surface that omits
any of the three is malformed; operator review should send it back.
Cheap variants are sometimes right (small stakes, throwaway scope)
but rarely on foundation work (practice 7) — the production-run
amortization changes the math. The operator decides; the operator's
go before implementation is part of the discipline, even when
established tenets already authorize the workstream — incremental
steps within an authorized workstream do not need ceremonial
confirmation, but crossing into implementation after a design
surface does. Only then implement — at the source level,
re-rendered, verified. Do not accrete a design through
implementation, and do not implement past the point the operator
has agreed.

The thorough-fix rule has a recurring violation shape: defaulting
to cheap variants or deferral, recovering only on operator pushback.
Catching requires explicit construction — name the thorough-fix
option first; weigh cheaper alternatives against it, not the other
way around. Smell tests: heaviest option offered still light;
deferring real design work to "another session" on cost grounds;
option set is all variants of one shape; crossing from
design-surface into implementation without the operator's explicit
go.

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
     `development-process.md`) against skill-craft's Layer 2
     principles + Layer 4 disciplines + all anti-patterns. Layer 1
     skill-structure checks (frontmatter, file layout, SKILL.md
     trigger format) do NOT apply to specs because specs are not
     skills — but every other skill-craft rule does. This is
     skill-craft's self-review mandate adopted for the framework:
     after committing any framework canonical file, dispatch a
     fresh-context subagent to apply the mandate's 5 checks
     (`skill-craft/plugin/skills/skill-craft/PROCEDURE.md`,
     "Self-review mandate"), restricting Check #1's "canonical
     rules" iteration to Layer 2 + Layer 4 + anti-patterns.
   - the whole document a substantive edit touched, for coherence
     (practice 6).
6. **Release the instance** — version-bump the plugin, commit,
   reinstall.
7. **Persist outcomes** — real-run findings and deferred ideas in the
   instance's status log; process changes back into this document.
