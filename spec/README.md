# Diligence Framework — Specification README

This directory is the Diligence-framework specification: the
domain-agnostic method an instance is generated from. This file
specifies the spec itself — its architecture, file layout, and
conventions.

---

## Architecture — three levels

Every piece of spec content belongs to exactly one of three
conceptual levels, decided by this test:

- **skill-craft** — how to build and maintain *any* skill: universal
  guidance (plumbing, protocol-writing technique, enforcement
  primitives, evolution, reflexivity) and per-skill-type guidance
  (how to build a workflow skill, a judgment skill, and so on). All
  generic skill-design. Lives in the `skill-craft` plugin, external
  to this spec.
- **Diligence framework** — the *specifics of one structured
  methodology*: the named phases (investigate-design / implement /
  verify), the two-pass cycle, inspection, the standardized lens
  set, the two-track tracker and status-state machine, [READY], the
  two modes, the orchestrator. The domain-agnostic, sharpened
  abstraction of proven structured-work mechanics. **This spec is
  this level.**
- **instance** — a domain binding: the standardized lens set for the
  domain, and the domain wording. Clippy is the coding instance; a
  marketing-clippy would be a sibling.

The line between the first two: skill-craft says how to build *a*
workflow skill (define phases, gate transitions, use menus); the
Diligence framework *is* one — its specific phases, cycle, and
mechanisms named. Generic skill-design is skill-craft; a named
methodology's specifics are the Diligence framework. The two are
siblings, not nested — skill-craft is meta (how to build any skill),
the Diligence framework is object-level (a methodology for doing
work); the framework is built *using* skill-craft, not part of it.

The line between the framework and an instance: the framework's
method is fixed; the instance supplies only the domain's standardized
lens set and the domain wording. See `../instantiation-guide.md`.

An instance is a **rendered artifact** — its protocol files are
generated from this spec and stay generated from it. The spec is the
standing source of truth: a change to the methodology is made here
and re-rendered into the instance, never hand-edited into the
instance directly. Hand-editing drifts the instance from the spec and
forfeits re-derivability. The re-render procedure is
`../development-process.md`.

## Files

- `glossary.md` — locked term definitions. Definitions only.
- `core.md` — model, the mechanisms, the grounding discipline, phase
  specs, status-state machine.
- `modules.md` — modes, the standardized lens set (its shape; the set
  itself is instance-supplied), artifact and tracker formats.
- `validation-watch.md` — companion, not part of the spec. Records
  fixed decisions made under uncertainty and the production signal to
  watch.
- `README.md` — this file.

`../instantiation-guide.md` is a separate companion: how to derive a
new Diligence-based plugin for a domain.

## Entry conventions

- **Operational vs analytic terms.** Operational terms appear in the
  generated protocol text; the AI acts on them. Analytic terms are
  for reasoning about the framework in this spec and never appear in
  a generated protocol. The spec generates the protocol from the
  operational terms.
- **Glossary is definitions-only.** A glossary entry states what a
  term means. It never specifies shape, structure, behavior, or
  state-models — those live in `core.md`.
- **Closed sets are enumerated.** Where a term names a closed set,
  its members are listed as an explicit enumeration.

## The fixed-decision rule

The spec states fixed decisions. It does not hedge, mark items "to be
decided," or carry tradeoffs.

A decision made best-effort under genuine uncertainty is still stated
as fixed. The uncertainty is recorded separately in
`validation-watch.md` — the decision, why it was uncertain, and the
production signal that would prompt revisiting it. The spec is
best-effort on current information and revised through production
learning, but that provisional nature is understood, never written
into the spec.

## Prescription discipline

The spec prescribes where prescription serves the framework's purpose
(see `core.md` Purpose) — where it secures grounded claims or a
coherent, complete picture. Everywhere else it leaves the AI to work
ad-hoc.

Over-prescription is not the safe default: it bloats the protocol,
raises cognitive load, and crowds out attention — a failure mode of
its own. Under-prescription lets the AI's default shortcuts return.
For every rule, mechanism, and format: prescribe only what furthers
the purpose, and prescribe it minimally. What, where, and how much to
prescribe is decided against that rubric — never by defaulting to
more.

Prescription has two independent axes: how *much* — the
minimal-quantity rule above — and how *strongly enforced*. They do not
trade off. A minimal prescription can be fully structural: a two-line
blocking gate is minimal *and* enforced. A rule load-bearing for the
purpose — one whose violation breaks grounded claims or the coherent
picture — is given structural enforcement (an evidence-bearing
artifact, a gate, a forced step) regardless of how minimal it is. "Minimal" never
licenses "soft": a load-bearing rule left as unenforced prose is
under-prescribed, not minimally prescribed.

## Extending the framework

The framework grows by adding concepts — a mechanism, a status, a
mode, a lens-set property. It does not grow freely: a new concept
earns its place, or it does not enter.

A proposed concept runs three filters:

1. **Level.** The three-level test above — is the concept skill-craft
   (how to build any skill), the Diligence framework (a specific of
   this methodology), or instance (a domain binding)? Only a
   framework-level concept enters this spec; the others belong
   elsewhere.
2. **Placement.** Within the framework: part of the stable spine — a
   mechanism foundation, a phase, a status, orchestrator behaviour →
   `core.md`; or a revisable module — a mode, the lens-set shape, an
   artifact format → `modules.md`. A genuinely new category that fits
   neither may warrant its own file; the bar is that it fits neither.
3. **Warrant.** The prescription discipline above — the concept earns
   its place only if it serves the Purpose (`core.md`), and is then
   prescribed minimally and at the right enforcement strength.

The framework is deliberately resistant to extension. The question is
never "is there room for this" but "does it further the Purpose, and
what is the least of it that does." A concept that cannot answer that
does not belong in the spec.
