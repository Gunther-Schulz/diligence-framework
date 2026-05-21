# Diligence Framework — Core

The stable spine of the spec: the model, mechanism foundations, phase
specs, and the status-state machine. Built on `glossary.md`; terms
are used as defined there.

---

## Purpose

The framework exists to secure two things in the AI's work. They are
the rubric every prescription in this spec is judged against — a
prescription that serves neither does not belong.

1. **Grounded claims.** No assertion without its basis. The AI cannot
   silently pass an assumption or a guess as fact; every load-bearing
   claim is backed by evidence or explicitly marked as inferred. This
   is what
   "converts AI confidence into AI evidence" means.
2. **A coherent, complete picture.** Every concern is held, visible,
   and carries a state. A superseded aspect is reconciled or
   invalidated, never silently dropped; the view does not narrow and
   does not circle.

These are two axes of one failure — hollow work (a claim with nothing
under it) and lost work (the picture going partial or narrow). Every
part of this spec — inspection, the tracker, the status-state
machine, the cycle loop, the gates — exists to secure one or both.

Human inspectability of the work is a further value, but a
lower-priority one: it does not change outcome quality. It does
impose a constraint — the artifacts must stay cognitively palatable,
to a human and to the AI alike, rather than bloating into detail too
large to hold.

---

## 1. Model

The Diligence framework is a protocol — a structured method the AI
follows to take a complex, open-ended task from request to a verified
outcome.

A run proceeds through three phases in sequence:

1. **investigate-design** — a loop of cycles that builds
   understanding of the task and the problem space and produces a
   locked design. Ends when the [READY] gate permits.
2. **implement** — carries out the locked design, producing the work.
3. **verify** — checks the produced work against the locked design
   and the standardized lenses.

The tracker carries state across the phases: investigate-design
produces it, implement works from it, and verify records its results
into it.

An orchestrator conducts the run — running the phases, holding their
transitions, and honoring any loopback a phase raises (§5).

A run is driven in one of two modes:

- **interactive** — the operator advances the loop and selects at
  menus.
- **auto-battle** — the loop self-advances under structural control,
  without per-cycle operator input.

The AI self-resolves every design decision it faces during a run; it
does not pose decisions to the operator as choices to make. It
commits to a recommendation and records the decision as a tracked
design decision (§4.2), with its basis (§2.4) — visible, never
silent. This holds for a decision to defer or not act: "defer X,
because Y" is a recorded decision, not an absence. A decision resting
on an assumption — including one only the operator could confirm —
carries that assumption as its basis; per §2.4 it holds the run short
of [READY] until the assumption is grounded or the operator resolves
it. The operator, seeing the recorded decisions, retains free-form
override at any point, in either mode.

---

## 2. Mechanism foundations

### 2.1 The two functions

Every mechanism has exactly one function.

- **Inspection** produces. It looks through a lens at the work so
  far and yields a finding when the lens catches something. Its lens
  is ad-hoc (task-derived) or standardized (pre-written; the
  standardized set is specified by the domain instance).
- **Gate** permits or blocks. It checks accumulated state at a
  transition point and either permits the transition or blocks it. It
  does not look and yields no findings.

### 2.2 Specifying a mechanism

A mechanism is specified in the form that fits its function (§2.1) —
there is no single shared template.

- An **inspection** — a lens — is specified by the lens-entry shape
  (`modules.md`): its name, the question it asks, and its scope,
  which carries the trigger that brings it into a cycle.
- A **gate** is specified directly — the condition it checks and the
  transition it guards (the [READY] gate: §3.1, §4.3).

### 2.3 The un-fakeable-artifact rule

Every load-bearing artifact the protocol requires — a mechanism's
output, and a recorded design decision — must be an artifact that
cannot be produced without doing the work it represents.

- A gate's check must require such an artifact. A form check — "N
  items are present," "a sample exists," "the section is filled in" —
  is satisfiable whether or not the work happened, so the gate passes
  without firing.
- An inspection's finding, or its cited reason that a lens is clean,
  must cite evidence that required looking.
- A design decision's artifact is its committed resolution and basis
  (§4.2). An open question, or a choice posed to the operator, is the
  absence of a resolution — not the artifact — so the design-decision
  track cannot hold one.

An artifact a non-adherent AI can produce by pattern alone enforces
nothing.

This rule reaches the protocol's behavioral rules, not its mechanisms
alone: a rule whose adherence cannot be read off an artifact is not
enforced. A load-bearing rule is specified so that following it
produces an artifact and not following it produces none.

### 2.4 The basis rule

Every load-bearing claim and every design premise carries a named
basis — the evidence it rests on. The basis is the artifact itself
(§2.3): a search result, a located read of the source. A free-text
claim of having looked is not a basis.

A basis that resolves to recall — "assumed," "inferred," "it is
obviously so" — is not a basis but an assumption. An assumption does
not ground a decision; the work is held short of [READY] until the
assumption is converted to evidence.

The rule does not ask the AI to recognise its own blind spots. The
mechanical tell of a blind spot is the basis the AI cannot produce —
a missing or recall-only basis is the flag, whether or not the claim
ever felt uncertain.

The rule has two edges:

- **Basis-naming.** Every load-bearing claim and design premise names
  its basis or stands as an assumption. This reaches design premises
  — such as the premise that an element is the work's alone to change
  — not findings alone.
- **True-unit basis.** A basis must cover the claim's true unit, not
  a coarser proxy of it. A claim about a *complete set* — a scope, an
  element's dependents, an input's value-classes, a flaw class's
  instances — has the whole set as its unit; its basis is an
  exhaustive search, not a declared scope or one instance. The
search's own reach is not exempt: a scope narrowed by where the
members are assumed to live is a declared scope in a search's
clothing — and a member co-located with the change is the one a
search of "everywhere else" is built to miss. A claim
  about a *construct* — a unit of the work product that must be taken
  whole — has the whole construct as its unit; its basis is a read to
  the construct's visible close, not a window that catches part of
  it. "I sampled," "I read the artifact," "I declared the scope" are
  proxies: each passes while the true unit goes unexamined.

A secondary source — a sub-agent report, a prior session's notes, an
audit summary — is not itself a basis. A direct citation it carries
(the located artifact with its verbatim content) relays the artifact
and can stand as a basis; its interpretation, synthesis, or
recommendation cannot, and is re-grounded against the actual artifact
before anything rests on it.

Only load-bearing claims and premises carry the basis apparatus; a
claim of bounded, contained cost does not.

---

## 3. Phase specs

### 3.1 investigate-design

investigate-design runs as a loop of cycles and produces a locked
design recorded in the tracker. It ends at [READY].

**A cycle** has two passes, in order:

1. **Investigation pass.** The AI investigates the relevant surfaces
   — ad-hoc inspection, by its own task-derived method, not a
   prescribed one. The standardized lens set is known going in and
   informs what the AI attends to (not how it investigates).
   Findings are recorded in the tracker.
2. **Standardized inspection pass.** Apply each standardized lens
   whose scope this cycle's investigation touched — incremental, over
   what this cycle produced. The pass emits a findings artifact that
   accounts for **every** lens in the set: for a lens in scope, a
   finding or a one-line cited reason it is clean; for a lens out of
   scope, a one-line cited reason it does not apply this cycle. A
   lens is never silently absent. (The standardized lens set is
   specified by the domain instance.)

The standardized inspection pass runs every cycle.

**Design.** Across the cycle the AI forms and updates design decisions
(§4.2) from the cycle's findings — the design-formation the phase is
named for, §1's synthesis into the evolving design. The locked design
is the body of those decisions; it locks as they reach [VERIFIED].

**Scope.** The scope — the set of elements the work will modify — is
the foundational design decision; every other decision is designed
within it. By §2.4 it is a completeness claim: its basis is an
exhaustive search of every intended target's dependents across the
problem space, not the AI's model of it. It is established first and
reaches [VERIFIED] only when search-established. When a later cycle
grows the set of intended targets, the scope decision re-opens and is
re-searched. Because [READY] requires every design decision
[VERIFIED] — or, in auto-battle, [AUTO-ACCEPTED] (§4.3) — an
unestablished scope, at neither, holds the phase.

**[READY]** has two parts. From the cycle history, investigate-design
reaches [READY] only when both hold:

- every cycle has completed its standardized inspection pass, and
- the last cycle's standardized inspection pass produced no material
  finding — none that changes the design.

The tracker-state conditions — every design decision [VERIFIED] (or
[AUTO-ACCEPTED] in auto-battle), no finding left open — complete the
gate and are specified in §4.3. [READY] permits the transition to implement; until the full
gate is met, the phase is [NOT READY] and the loop continues.

### 3.2 implement

implement carries out the locked design recorded in the tracker,
producing the work.

The locked design is the authority. The existing work product and
surrounding conventions are context, not authority — where they
diverge from the locked design, the design governs. The work is derived from the
design first; existing patterns are evaluated for fit afterward.

Discovery in implement is minimal — a small local clarification, not
new design. Major new scope surfacing during implementation holds the
phase and returns the run to investigate-design; no work is lost.

implement reports completion when the locked design is carried out.
The implement→verify transition is not gated: verify (§3.3) is itself
the check on implement, so an incomplete implementation surfaces as
verify findings rather than passing silently.

### 3.3 verify

verify checks the completed work against the locked design and the
standardized lenses.

verify is conducted in a context **isolated** from the run's working
context — the context that conducted investigate-design and
implement. An actor checking its own work carries its own anchoring
and blind spots into the check; isolation is what makes verify an
independent check and not the actor re-reading itself. verify is
artifact-driven — the three checks below work from the tracker, the
standardized lens set, and the work product, and need nothing from
the run's conversation — so the isolated context is fully equipped.
The isolation is unconditional: that verify runs isolated is not a
judgement the run makes per task.

- **Planned vs actual** — every locked design decision is checked
  against what the work actually does.
- **Standardized lenses** — the standardized lens set is applied to
  the produced work.
- **Executing the verification** — the domain's executable
  verification is run and its output shown. verify does not pass on
  static inspection alone.

verify accounts for every check. Each planned-vs-actual check, and
every standardized lens — applied where it is in scope, or given a
cited reason it is not — either holds, recorded as a cited-clean
line, or yields a divergence from the locked design or a lens issue;
a failed run of the executable verification is likewise an issue.
Every divergence or issue is recorded as a **finding**, entering the
finding track (§4.1) at [PENDING].

verify's terminal result is **[PASSED]** — every check accounted for
and no finding short of [VERIFIED] — or **[ISSUES FOUND]**.
[ISSUES FOUND] returns the run to resolve those findings; verify then
re-runs (§5).

---

## 4. The status-state machine

A status tag records the state of a finding or a design decision.
There are two tracks. ([PASSED] and [ISSUES FOUND] — verify's phase
result — are not a track; they are specified in §3.3.)

Three tags appear in both tracks, track-scoped and with one
consistent sense: **[PENDING]** (recorded, not yet at a terminal),
**[VERIFIED]** (a verified terminal), **[INVALIDATED]** (a verified
terminal contradicted by later evidence). The reuse is deliberate —
one vocabulary across both tracks.

### 4.1 Finding states

A finding — an observation recorded by inspection — moves through:

1. **[PENDING]** — recorded; not yet verified.
2. **[PARTIALLY VERIFIED]** — verification begun but incomplete. A
   finding fully verified in one step moves [PENDING] → [VERIFIED]
   directly; [PARTIALLY VERIFIED] holds a finding whose verification
   spans steps or cycles.
3. **[VERIFIED]** — verification complete: the finding's content is
   established on evidence — whether that content is a live concern
   (it informs the design) or a non-issue (investigated, it does
   not). Which it is lives in the finding's summary, not a separate
   state.

A finding whose stated content is found inaccurate during
verification is corrected in place; verification continues, with no
status change.

A [VERIFIED] finding can then be invalidated:

4. **[INVALIDATED]** — a [VERIFIED] finding contradicted by later
   evidence. An [INVALIDATED] finding reopens — it reverts to
   [PENDING] for re-verification — and holds the phase (§4.3) until
   it does. Only a [VERIFIED] finding becomes [INVALIDATED]; one
   contradicted before [VERIFIED] is simply corrected.

### 4.2 Design-decision states

A design decision is the AI's resolved choice about what to build — a
**committed position**, including a choice to defer or exclude. It is
never an open question or a choice posed to the operator: per §2.3 a
question is the absence of a resolution and yields no valid artifact,
so the design-decision track holds none. It carries that resolution,
a **basis** (§2.4) — the evidence the choice rests on, or, where it
rests on an assumption, that assumption named — and a status. A
decision the operator could resolve is recorded [CONDITIONAL] — the
AI's committed recommendation carrying the operator-resolvable
assumption — never a posed choice; the operator overrides it from the
tracker (§1). The basis is mandatory; a decision whose basis is an
assumption cannot reach [VERIFIED]. It moves through:

1. **[OUTLINED]** — a committed direction; concrete detail not yet
   investigated.
2. **[PENDING]** — a concrete decision whose detail still needs
   investigation.
3. **[CONDITIONAL]** — a concrete decision resting on an unverified
   assumption; the assumption is recorded with it.
4. **[VERIFIED]** — a concrete decision, complete and locked, its
   basis evidence, detailed enough that implementing it introduces no
   new design decision.
5. **[AUTO-ACCEPTED]** — a [CONDITIONAL] decision that auto-battle
   accepted on the AI's committed recommendation, the run proceeding
   without the operator who would otherwise resolve it (`modules.md`
   §1.2). The recommendation stands; the assumption it rested on was
   not verified — [AUTO-ACCEPTED] records exactly that, and does not
   claim the verification that [VERIFIED] does. Reached only in
   auto-battle.
6. **[INVALIDATED]** — a [VERIFIED] or [AUTO-ACCEPTED] decision
   contradicted by later evidence.

An [OUTLINED] decision becomes concrete as either [PENDING] or
[CONDITIONAL]. [PENDING] and [CONDITIONAL] are the
concrete-intermediate states, and a decision moves between them as
investigation proceeds — a [PENDING] decision found to rest on an
unverified assumption becomes [CONDITIONAL]; a [CONDITIONAL] decision
becomes [VERIFIED] when its assumption is verified, and reverts to
[PENDING] to be re-formed if the assumption is disproved. In
auto-battle, a [CONDITIONAL] decision still resting on its assumption
at the [READY] gate — with no operator available to resolve it —
becomes [AUTO-ACCEPTED] rather than holding the run (`modules.md`
§1.2). An [INVALIDATED] decision reopens — it reverts to [PENDING],
and any decision that depended on it reverts with it — and holds the
phase (§4.3) until re-formed. Only a [VERIFIED] or [AUTO-ACCEPTED]
decision becomes [INVALIDATED]; one contradicted before reaching
either is simply revised.

### 4.3 Relationship to [READY]

Beyond the cycle-history condition in §3.1, the [READY] gate
requires: no finding is [INVALIDATED], no load-bearing finding is
left below [VERIFIED], and every design decision is [VERIFIED] — or,
in auto-battle, [VERIFIED] or [AUTO-ACCEPTED] (§4.2). An [INVALIDATED]
finding, a load-bearing finding short of [VERIFIED], or a design
decision short of that bar holds the phase at [NOT READY].

---

## 5. Orchestrator

The orchestrator conducts a run through the phase pipeline. The
phases (§3) and the status-state machine (§4) define the work and its
gates; the orchestrator runs the phases in order, holds the
transitions, and manages the run's lifecycle.

**Run start.** The orchestrator detects the run's mode (§1) and
enters investigate-design. Mode detection and the per-mode conduct of
the run are specified in `modules.md` §1.

**Sequencing and transitions.** The orchestrator advances
investigate-design → implement → verify, entering a phase only when
its predecessor has reported completion. The investigate-design →
implement transition is held by the [READY] gate (§3.1, §4.3):
implement is not entered until [READY]. Each time verify is conducted
— on first reaching it, and on each re-run after [ISSUES FOUND] — the
orchestrator establishes it in a context isolated from the one that
conducted investigate-design and implement (§3.3).

**Loopbacks.** A phase may return the run to an earlier phase; the
orchestrator honors the return rather than proceeding. implement
returns to investigate-design when major new scope surfaces (§3.2);
an [INVALIDATED] finding or design decision reopens design work (§4);
verify ending [ISSUES FOUND] returns the run to resolve those
findings, then re-runs.

**Run lifecycle.** A run starts at investigate-design and ends when
verify reports [PASSED]. A run's state — the tracker (§4) and the
phase it is in — persists across interruptions; a run interrupted
mid-flight resumes from that state rather than restarting.

**Halt and surface.** When the orchestrator cannot advance — a phase
cannot complete — it halts the run and surfaces the reason; it never
advances on an unresolved gate. A decision that needs the operator is
not such a case: in interactive mode it is held as [CONDITIONAL]
until the operator resolves it; in auto-battle it becomes
[AUTO-ACCEPTED] and the run proceeds (§4.2, `modules.md` §1.2).
Auto-battle's remaining halt conditions are part of that mode's
design (`modules.md` §1.2).
