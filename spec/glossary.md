# Diligence Framework — Glossary

Locked definitions. Each term has exactly one definition; every spec
section uses terms as defined here. Where a term names a closed set,
the members are enumerated. Extended as `core.md` and `modules.md`
surface new terms.

**Operational vs analytic terms.** Operational terms appear in the
protocol text the AI acts on — e.g. [READY], the tracker, the named
standardized lenses. Analytic terms are for reasoning about the
framework in this spec and never appear in a generated protocol —
e.g. "ad-hoc". The spec generates the protocol from the operational
terms; analytic terms are scaffolding.

---

## Mechanism and inspection

**Mechanism** — a named, defined element of the protocol that the AI
applies during a phase. The framework's one reusable mechanism is
inspection.

**Inspection** — looking through a lens at the work produced so far.
Produces a finding when the lens catches something, nothing when it
does not.

**Lens** — a single defined inspection criterion: one specific
question asked of the work already produced. All looking is lensed;
inspection differs only by where the lens comes from. Two sources:

1. **Ad-hoc** — derived from the task at hand, situationally. Covers
   the task-obvious; bounded by what the AI thinks to look for.
2. **Standardized** — pre-written in the protocol, capturing recurring
   blind spots. Applied, not derived — the looking the AI would not
   think to do on its own. The standardized lens set's shape is
   specified in `modules.md`; the set itself is supplied by the
   domain instance.

## Basis and evidence

**Basis** — the evidence a claim or design decision rests on: a
search result, a located read of the source — the artifact itself.
The basis rule is specified in `core.md` §3.2.

**Assumption** — a basis that resolves to recall ("assumed,"
"inferred") or to deferral ("will verify in cycle N," "TBD")
rather than evidence. An assumption does not ground a decision;
how it holds a run short of [READY] is specified in `core.md`.

**Load-bearing** — descriptive of a claim or premise that a design
decision, a recommendation, or [READY] rests on. Only load-bearing
claims carry the basis apparatus (`core.md` §3.2).

**Completeness claim** — a claim about a complete set: a scope, an
element's dependents, an input's value-classes, a flaw class's
instances. Its basis is a mechanical search (`core.md` §3.2).

**Silent substitution** — missing or malformed evidence defaulted to
a plausible proxy that propagates as if it were the basis: a
recalled count where a search is needed, a free-text claim of having
looked, a sampled subset where the whole set is the unit. The
canonical AI failure shape the basis rule (`core.md` §3.2) rejects.
The discipline is to surface the gap, not substitute.

## Phases and structure

**Run** — a single execution of the framework on a task: the three
phases conducted from request to a verified outcome.

**Work product** — what a run produces; what implement carries the
locked design out into (also: "the work"). An instance binds it to
its domain — code, for Clippy.

**Phase** — a top-level stage of the protocol. The framework has
three, run in sequence:

1. **investigate-design** — investigation and design, run as a loop
   of cycles, producing a locked design and the [READY] state. One
   phase despite the compound name.
2. **implement** — carrying out the locked design, producing the
   work.
3. **verify** — checking the produced work against the locked design
   and the standardized lenses.

**Investigation** — a single run of the investigate-design phase, from
the first cycle to [READY].

**Cycle** — one iteration of the investigate-design loop.

**Convergence cycle** — a full cycle (investigation pass +
standardized inspection pass) run after the working context judges
the §4.1.1 supporting facts met and the §4.1.2 fresh-session test
PASSED. [READY] requires the convergence cycle to produce zero
D-track deltas (`core.md` §4.1.4). The investigation pass must
enumerate new surfaces investigated this cycle, cited as file:line
or grep queries not present in any prior cycle's investigation-
pass artifact this run; a convergence cycle that only re-attests
prior findings is malformed.

**Cycle-another (recommendation)** — the AI's recommendation to
run another investigate-design cycle rather than transition to
implement (`core.md` §4.1.3). Triggered when the fresh-session
implementability test fails, a lens in scope was not applied in
the cycle that touched its scope, or the convergence cycle
surfaces D-track deltas. Justified by enumeration of observations,
not by cost comparison.

**Loopback** — a phase returning the run to an earlier phase
rather than proceeding (`core.md` §6 Loopbacks). Three trigger
points: implement → investigate-design on major new scope (§4.2);
verify [ISSUES FOUND] → investigate-design (§4.3); an
[INVALIDATED] finding or design decision reopens design work
(§5). Each carries a defined return-shape; the orchestrator
honors the return rather than proceeding.

**Major new scope** — an implementation-phase finding classified
as returning the run rather than proceeding within the current
unit's locked design. Closed four-clause definition (`core.md`
§4.2): (1) touches an element or contract not in the unit's
listed scope; (2) changes a locked contract's members; (3)
introduces a new design decision; (4) crosses a sibling unit's
scope. Otherwise a local clarification (recorded; unit proceeds).

**Self-check (at dispatch boundary)** — a check the dispatched
impl-phase subagent (and the working context, for a single-unit
plan) applies to its own diff before returning state, using the
instance's standardized lenses most relevant to write-time issues
(`core.md` §4.2). Compounds with the design-time forcing function
(§3.2); catches references and behaviors introduced post-design.
A self-check finding of major-new-scope shape triggers loopback.

**Pass** — one of the two activities within a cycle. Every cycle has
exactly two, in order:

1. **Investigation pass** — the AI investigates the relevant surfaces
   with task-derived lenses. The default activity. (Analytic
   character: ad-hoc inspection.)
2. **Standardized inspection pass** — the AI applies the standardized
   lenses whose scope the cycle's work touched to what the
   investigation pass produced.

**Orchestrator** — the coordinating layer of a run: it detects the
mode, conducts the phase pipeline through its transitions, and
manages the run lifecycle. Specified in `core.md` §6.

**Working context** — the AI's context that conducts
investigate-design and implement. Distinct from verify's isolated
context (`core.md` §4.3) — verify is established by the orchestrator
in a context separate from the one that produced the work. The
working context judges design completeness at [READY] (`core.md`
§4.1).

**Operator** — the human directing the run. In interactive mode,
advances the loop via the menu (`modules.md` §1.1), resolves
[CONDITIONAL] decisions via free-form override against the tracker,
and decides at [READY]. In auto-battle mode, absent during the run;
reviews the completed run's tracker (including [AUTO-ACCEPTED]
tags). The framework's role-separation principle is *AI surfaces
best, operator judges cost* (`core.md` §1).

## State

**Tracker** — the structured state record of an investigation: its
findings, design decisions, and their status.
The primary state of the investigate-design phase.

**F-track / D-track** — shorthand for the tracker's two tracks
(`core.md` §5): the **F-track** is the finding track (observations
from inspection); the **D-track** is the design-decision track
(committed positions on what to build). The instance specifies
whether the D-track holds only design decisions (Clippy) or also
other forms of committed positions (e.g., hypothesis verdicts in
Daneel). Used where deltas between cycles are compared per-track —
e.g., the convergence cycle test (`core.md` §4.1.4) gates [READY]
on zero D-track delta.

**Finding** — a discrete observation recorded in the tracker, carrying
a status tag.

**Status tag** — a bracketed marker on a finding or a design
decision recording its state. The full set:
**[PENDING]** (recorded, not yet at terminal — both tracks),
**[PARTIALLY VERIFIED]** (finding mid-verification),
**[VERIFIED]** (verified terminal — both tracks),
**[INVALIDATED]** (verified terminal contradicted by later
evidence — both tracks),
**[OUTLINED]** (decision: committed direction, detail not yet
investigated),
**[CONDITIONAL]** (decision: rests on unverified assumption),
**[AUTO-ACCEPTED]** (decision: AI's committed recommendation taken
as default at [READY] when operator did not override — both modes).
Transitions and per-tag rules specified in `core.md` §5.

**[READY] / [NOT READY]** — the terminal state of the
investigate-design phase: [READY] is the design judged complete and
presented for the decision to proceed; [NOT READY] precedes it. How
[READY] is determined is specified in `core.md`.

**[PASSED] / [ISSUES FOUND]** — verify's terminal result: [PASSED]
when every check is accounted for and no finding is short of
[VERIFIED], [ISSUES FOUND] otherwise. Specified in `core.md` §4.3.

**Design decision** — a committed resolution: the AI's resolved
choice about what to build, including a choice to defer or exclude.
Its shape, states, and rules are specified in `core.md` §5.2.

**Scope** — the set of elements a run's work will modify; the
foundational design decision, established by search. Specified in
`core.md` §4.1.

**Dispatch unit** — a group of design decisions implemented together
as one piece of impl-phase work. Derived from the locked design at
implement-phase start. Specified in `core.md` §4.2.

**Impl plan** — implement-phase's planning artifact: a list of
dispatch units in dependency order, each carrying a
parallel-eligibility marker. Produced at implement-phase start;
persisted alongside the tracker. Specified in `core.md` §4.2 and
`modules.md` §3.3.

**Production signal** — a real-run observation that confirms or
refutes a watch entry's hypothesis about an uncertain design
choice (`validation-watch.md` preamble). Validation-watch entries
record uncertain decisions and what signal would prompt revisiting
them; production signals come from any instance's real runs.

**Watch-entry lifecycle states** — the four states a
`validation-watch.md` entry carries on its Status line
(`validation-watch.md` preamble Entry lifecycle): **WATCHING**
(uncertainty exists, no fix yet; signal being watched);
**FIX-SHIPPED** (structural fix in spec; watching for a
load-bearing instance of the mitigation); **RESOLVED**
(load-bearing instance observed via post-run review — positive
evidence the mitigation works); **INVALIDATED** (production
signal recurred under the fix-shipped spec; mitigation didn't
hold; requires new analysis). Distinct from the [INVALIDATED]
status tag above — the status tag is a finding/decision state in
the tracker; the lifecycle state is a watch-entry state in
validation-watch.md.

**Load-bearing instance** — a finding the watch entry's
mitigation actively caught that would have escaped under the
pre-mitigation protocol (`validation-watch.md` preamble Entry
lifecycle). The positive-evidence criterion for FIX-SHIPPED →
RESOLVED transitions — distinct from absence-of-recurrence
(which is indistinguishable from "failure shape didn't surface
this run").

**Recall pool** — the working context's accumulated set of
already-recorded findings and design decisions when answering a
self-test (`core.md` §4.1.4 + V-5). The failure shape that allows
false-[READY]s: the AI answers the fresh-session implementability
test from recall of what the tracker contains rather than from
re-reading external evidence. The convergence cycle (§4.1.4)
breaks the recall pool by switching modes to fresh investigation;
§4.1.2's per-step external evidence requirement forces re-reading
at the self-test moment.

**False-[READY]** — a [READY] declaration that subsequent work
surfaces material design gaps for (`validation-watch.md` V-5).
Caught by operator at the closed-artifact review (Continue
override), by the convergence cycle (§4.1.4), or — when both
miss — by implement-loopback or verify [ISSUES FOUND].

**Convergence exception (auto-battle verify [ISSUES FOUND])** —
the rule that prevents auto-battle from infinite-looping on a
finding the AI already chose to defer at investigate-design time
(`modules.md` §1.2; V-9). A verify finding whose evidence field
cross-references an existing [AUTO-ACCEPTED] decision by tracker
identifier does not trigger loopback; the run completes with the
re-surfacing notation. Without the explicit cross-reference, the
finding triggers loopback as a new gap.

## Modes

**Mode** — how a run drives the phases. The framework has two:

1. **Interactive** — operator-driven: the operator advances the loop
   and chooses at menus.
2. **Auto-battle** — autonomous-execution: the loop self-advances
   without per-cycle operator input.

**Menu** — interactive mode's advance point: the AI presents the
tracker and a recommendation, and the operator selects an option —
continue, or proceed to the next phase — or free-form overrides.
Specified in `modules.md` §1.1.

## Triage and review classifications

**Render gap / spec gap / adherence gap** — the closed triage
classification of post-run review findings
(`development-process.md` practice 1; used in `modules.md` §4 and
`post-run-review.md` Where outcomes land). A **render gap** is
the instance file not faithfully carrying the spec → re-render.
A **spec gap** is the render faithful, the AI followed it, and
it still broke → sharpen the spec. An **adherence gap** is a
faithful render of an unambiguous evidence-bearing rule violated
anyway — the irreducible residual the verify, operator, and
loopback backstops carry.

**Escape / operator catch** — the closed pair classifying Q1
design-defect findings in post-run review (`post-run-review.md`
Q1). An **escape** is a defect recorded past [READY] by
implement-phase loopback or verify [ISSUES FOUND] (both
investigate-design checks and the [READY] presentation missed).
An **operator catch** is a defect caught at the [READY]
presentation, before the run proceeded (investigate-design
missed but the [READY] presentation worked as designed).
