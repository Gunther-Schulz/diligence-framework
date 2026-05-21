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
  verify), the two-pass cycle, inspection/gate, the standardized lens
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

## Files

- `glossary.md` — locked term definitions. Definitions only.
- `core.md` — model, mechanism foundations, phase specs,
  status-state machine.
- `modules.md` — modes, the standardized lens set (its shape; the set
  itself is instance-supplied), artifact and tracker formats.
- `validation-watch.md` — companion, not part of the spec. Records
  fixed decisions made under uncertainty and the production signal to
  watch.
- `README.md` — this file.

`../instantiation-guide.md` is a separate companion: how to derive a
new Diligence-based plugin for a domain.

## Entry conventions

- **Template / binding / instance.** For each kind of thing
  (mechanism, phase, mode): skill-craft defines the *template* — the
  slots an entry fills; the Diligence framework *binds* the template
  to its vocabulary; an instance holds the named domain-specific
  content (the lens set).
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
