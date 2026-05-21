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

## Mechanism and function

**Mechanism** — a named, defined element of the protocol that the AI
applies during a phase. Every mechanism has exactly one function.

**Function** — what a mechanism does when it runs. Exactly one of
two:

1. **Inspection** — looking through a lens at the work produced so
   far. Produces a finding when the lens catches something, nothing
   when it does not. Generative.
2. **Gate** — permit or block on accumulated state. Does not look;
   produces no findings. Gated.

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
The basis rule is specified in `core.md` §2.4.

**Assumption** — a basis that resolves to recall — "assumed,"
"inferred" — rather than evidence. An assumption does not ground a
decision; how it holds a run short of [READY] is specified in
`core.md`.

**Load-bearing** — descriptive of a claim or premise that a design
decision, a recommendation, or [READY] rests on. Only load-bearing
claims carry the basis apparatus (`core.md` §2.4).

**Completeness claim** — a claim about a complete set: a scope, an
element's dependents, an input's value-classes, a flaw class's
instances. Its basis is a mechanical search (`core.md` §2.4).

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
   and the quality standards.

**Investigation** — a single run of the investigate-design phase, from
the first cycle to [READY].

**Cycle** — one iteration of the investigate-design loop.

**Pass** — one of the two activities within a cycle. Every cycle has
exactly two, in order:

1. **Investigation pass** — the AI investigates the relevant surfaces
   with task-derived lenses. The default activity. (Analytic
   character: ad-hoc inspection.)
2. **Standardized inspection pass** — the AI applies the standardized
   lens set to what the investigation pass produced.

**Orchestrator** — the coordinating layer of a run: it detects the
mode, conducts the phase pipeline through its transitions, and
manages the run lifecycle. Specified in `core.md` §5.

## State

**Tracker** — the structured state record of an investigation: its
findings, design decisions, and their status.
The primary state of the investigate-design phase.

**Finding** — a discrete observation recorded in the tracker, carrying
a status tag.

**Status tag** — a bracketed marker on a finding or a design
decision recording its state. The full set and the
transitions between them are the status-state machine, specified in
`core.md`.

**[READY] / [NOT READY]** — the terminal state of the
investigate-design phase: [READY] permits transition to implement,
[NOT READY] precedes it. How [READY] is determined is specified in
`core.md`.

**Design decision** — a recorded choice about what to build. Its
shape — basis, levels — is specified in `core.md`.

**Scope** — the set of elements a run's work will modify; the
foundational design decision, established by search. Specified in
`core.md` §3.1.

## Modes

**Mode** — how a run drives the phases. The framework has two:

1. **Interactive** — operator-driven: the operator advances the loop
   and chooses at menus.
2. **Auto-battle** — autonomous-execution: the loop self-advances
   under structural control, without per-cycle operator input.

**Menu** — interactive mode's advance point: the AI presents the
tracker and a recommendation, and the operator selects an option —
continue, or proceed to the next phase — or free-form overrides.
Specified in `modules.md` §1.1.
