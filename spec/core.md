# Diligence Framework — Core

The stable spine of the spec: the model, the mechanisms, the
grounding discipline, the phase specs, the status-state machine, and
the orchestrator. Built on `glossary.md`; terms are used as defined
there.

---

## Purpose

The framework exists to secure two things in the AI's work — the
rubric every prescription is judged against:

1. **Grounded claims.** No assertion without its basis. Every
   load-bearing claim is backed by evidence or explicitly marked as
   inferred.
2. **A coherent, complete picture.** Every concern is held,
   visible, and carries a state. A superseded aspect is reconciled
   or invalidated, never silently dropped.

Human inspectability is a constraint, not a primary value:
artifacts must stay cognitively palatable rather than bloating
into detail too large to hold.

---

## 1. Model

A run proceeds through three phases in sequence:

1. **investigate-design** — a loop of cycles that builds
   understanding of the task and the problem space and produces a
   locked design. Ends at [READY], when the operator, presented the
   design, decides to proceed.
2. **implement** — carries out the locked design, producing the work.
3. **verify** — checks the produced work against the locked design
   and the standardized lenses.

The tracker carries state across the phases: investigate-design
produces it, implement works from it, and verify records its results
into it.

An orchestrator conducts the run — running the phases, holding their
transitions, and honoring any loopback a phase raises (§6).

A run is driven in one of two modes:

- **interactive** — the operator advances the loop and selects at
  menus.
- **auto-battle** — the loop self-advances without per-cycle operator
  input.

The AI self-resolves every design decision and records it as a
tracked design decision (§5.2) with its basis (§3.2) — visible,
never silent. **Committed recommendations default to the
thorough-fix shape — the option that addresses the situation at
its actual scope, not pre-clipped on perceived cost. Cost is the
operator's judgment.** "Defer X, because Y" is itself a recorded
decision, not an absence. A decision resting on an assumption —
including one only the operator could confirm — carries that
assumption as its basis and is recorded [CONDITIONAL] (§5.2). The
operator retains free-form override at any point.

The operator's request sets the task; it may also propose a solution.
Such a proposal is a strong input, not a locked design: that it is
the right solution is a design premise — grounded on evidence like
any other (§3.2), not assumed because the operator proposed it. The
AI investigates the proposal as it would any design question —
confirming, sharpening, or replacing it on evidence.

---

## 2. Inspection

The framework's one reusable mechanism is **inspection**: it looks
through a lens at the work so far and yields a finding when the lens
catches something. The lens is ad-hoc — the AI's own task-derived
line of inquiry — or standardized: pre-written, the standardized set
specified by the domain instance.

A standardized lens is specified by the lens-entry shape
(`modules.md`): its name, the question it asks, and its scope, which
carries the trigger that brings it into a cycle.

The run's phase transitions — investigate-design's end at [READY],
the loopbacks — are not mechanisms of this kind. They are not a
mechanical check on accumulated state; they are governed by the phase
specs (§4) and the orchestrator (§6), where what each transition
requires is specified directly.

---

## 3. The grounding discipline

### 3.1 The evidence-bearing-artifact rule

Every load-bearing artifact the protocol requires — a mechanism's
output, a recorded design decision — must be **evidence-bearing**:
producing it requires doing the work it represents, so a
non-adherent AI cannot produce it by pattern alone. A bare claim —
"checked all consumers" — is satisfiable whether or not the work
happened; a located enumeration — "consumers: [file:line, …]" — is
not.

Evidence-bearing is a gradient, not an absolute — no artifact an AI
produces is un-fakeable, since it can fabricate one. An artifact's
strength is how far faking it requires active fabrication rather than
mere omission, and how cheaply a checker catches the fake. A
**strong** artifact points at external, re-checkable truth — a search
result, a located read, an executed verification's output: faking it
means fabricating something a checker re-runs and catches. A **weak**
artifact is a claim about the run's own state — a status tag, a
self-assessment that work is complete: there is no external truth to
check it against.

- An inspection's finding, or its cited reason that a lens is clean,
  must cite evidence that required looking.
- A design decision's artifact is its committed resolution and its
  basis (§3.2). An open question, or a choice posed to the operator,
  is the absence of a resolution — so the design-decision track cannot
  hold one.

A weak artifact is not self-enforcing — the protocol cannot rest on
the artifact alone. It is enforced by a **separate checker**: a
context that did not produce the artifact re-derives it, or the
operator inspects it. The artifact still earns its place — it makes
faking require fabrication, and gives the checker something concrete
to check — but the guarantee comes from the checker, not the
artifact.

This rule reaches the protocol's behavioral rules, not its
mechanisms alone: a rule whose adherence cannot be read off an
artifact is not enforced. A load-bearing rule is specified so
that following it produces an artifact and not following it
produces none.

### 3.2 The basis rule

Every load-bearing claim and every design premise carries a named
basis — the evidence it rests on. The basis is the artifact itself
(§3.1): a search result, a located read of the source. A free-text
claim of having looked is not a basis.

A basis that resolves to recall — "assumed," "inferred,"
"obviously so" — or to deferral — "will verify in cycle N,"
"impl-phase will produce," "TBD" — is not a basis but an
assumption. An assumption does not ground a decision; the work
is held short of [READY] until the assumption is converted to
evidence. The mechanical tell of a blind spot is the basis the
AI cannot produce.

The rule rejects **silent substitution**: missing or malformed
evidence defaulted to a plausible proxy that propagates as if it
were the basis. Surface the gap, do not substitute.

#### 3.2.1 The two edges

- **Basis-naming.** Every load-bearing claim and every design
  premise names its basis or stands as an assumption. This
  reaches design premises, not findings alone, AND it reaches
  **claims embedded within larger statements** — implicit
  premises in target-naming decisions, cited rules or prior
  decisions, completeness counts asserted as facts. Each
  embedded claim carries the basis-rule requirement *separately*
  from the surrounding statement: the surrounding claim's basis
  does not cover the embedded one. The basis is a re-runnable
  artifact at decision-lock time (§3.2), not recall. An embedded
  claim with no separate basis is an assumption and cannot reach
  [VERIFIED].
- **True-unit basis.** A basis must cover the claim's true unit,
  not a coarser proxy. A claim about a *complete set* (a scope,
  an element's dependents, an input's value-classes, a flaw
  class's instances) has the whole set as its unit; its basis is
  an exhaustive search recorded as the **re-runnable search
  itself** — the executable query, not the count it returned. A
  search narrowed by where the members are assumed to live is a
  declared scope wearing a search's clothing — including a search
  of "everywhere else" that excludes the change site, where
  co-located members hide. A claim about a
  *construct* (a unit of the work product that must be taken
  whole) has the whole construct as its unit; its basis is a
  read to the construct's visible close.

#### 3.2.2 Replacement, removal, or amendment as completeness claim

A design decision involving **replacement, removal, or amendment
of an existing artifact** carries an implicit completeness claim:
that all references to (and load-bearing behaviors of) the
affected artifact have been accounted for. The basis must
include the re-runnable search enumerating references AND — for
replacements introducing a successor — an explicit enumeration
of behaviors preserved or dropped. Without both where applicable,
the decision is missing its true-unit basis and cannot reach
[VERIFIED]. This is the forcing function for Coupled-change
adherence.

#### 3.2.3 Secondary sources

A secondary source — a sub-agent report, a prior session's notes, an
audit summary — is not itself a basis. A direct citation it carries
(the located artifact with its verbatim content) relays the artifact
and can stand as a basis; its interpretation, synthesis, or
recommendation cannot, and is re-grounded against the actual artifact
before anything rests on it.

#### 3.2.4 Scope: load-bearing only

Only load-bearing claims and premises carry the basis apparatus; a
claim of bounded, contained cost does not.

---

## 4. Phase specs

### 4.1 investigate-design

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
   what this cycle produced. The pass emits a line for each in-scope
   lens: a finding, or a one-line cited reason it is clean. A lens out
   of scope this cycle is not lined — the set is not re-attested every
   cycle; it is accounted for whole once, at [READY]. (The
   standardized lens set is specified by the domain instance.)

The standardized inspection pass runs every cycle.

**Design.** Across the cycle the AI forms and updates design decisions
(§5.2) from the cycle's findings — the design-formation the phase is
named for, §1's synthesis into the evolving design. The locked design
is the body of those decisions; it locks as they reach [VERIFIED].

**Scope.** The scope — the set of elements the work will modify — is
the foundational design decision; every other decision is designed
within it. By §3.2 it is a completeness claim: its basis is an
exhaustive search of every intended target's dependents across the
problem space, not the AI's model of it. It is established first and
reaches [VERIFIED] only when search-established. When a later cycle
grows the set of intended targets, the scope decision re-opens and is
re-searched. Because [READY] requires every design decision
[VERIFIED] or [AUTO-ACCEPTED] (§5.3) — applies in both modes — an
unestablished scope, at neither, holds the phase.

#### 4.1.1 [READY] — judgment criteria

**[READY]** is reached when the working context judges the design
complete — every concern resolved, every design decision at its
terminal, and the last cycle's standardized inspection pass producing
no load-bearing finding. The supporting facts are recorded across the run:
the standardized lens set is accounted for whole — every lens applied
in the cycle(s) where its scope was touched, or carrying a cited
reason it was out of scope for the run, no lens silently absent; the
last cycle's pass left no load-bearing finding; every design decision is
[VERIFIED] or [AUTO-ACCEPTED] (§5.3) — both modes; **and every
[VERIFIED] design decision's embedded target-naming and count
premises carry a re-runnable basis** (per §3.2 basis-naming for
design-decision premises); no finding is left open. These are the
status the tracker carries (§5.3) — a notebook of where each
concern stands — not a mechanical check the run self-passes.

The supporting facts above check that everything *recorded* is
at terminal. The judgment must also test whether the recording is
*complete*. The strongest single test is **fresh-session
implementability**: would a session with only the tracker (no
chat context, no current-session memory) implement the design
without surfacing a new design decision? If not, another cycle is
warranted regardless of recorded statuses.

#### 4.1.2 [READY] — artifact-produced result line

**[READY]'s judgment is artifact-produced.** The fresh-session
implementability test produces a named result line in the closed
artifact at [READY] presentation: PASSED (with a one-line cited
reason) or FAILED (with the specific gap identified). Without
this artifact line, the closed-artifact form (`modules.md` §1.1)
is malformed; the [READY] declaration is unenforced. In
auto-battle the result line is recorded in the tracker for
post-run review.

#### 4.1.3 [READY] — cycle-another recommendation

The AI recommends cycle-another whenever the fresh-session
implementability test fails, or a lens in scope was not applied
in the cycle that touched its scope. Cost-asymmetry does not
enter the recommendation; per §1, the operator judges cost.
**The recommendation's justification enumerates observations** —
open findings, [PENDING] decisions, lens-applications still
required, fresh-session-implementability gaps — not costs
(effort, budget, time, "cheaper than"). A justification framed
in cost comparison is malformed.

At [READY] the AI does not certify itself ready: it presents the
design — the tracker, the recorded design decisions, and a
recommendation — for the operator's judgment. The cycle-history
facts (the standardized lens set accounted for whole; the last
cycle's pass clean) are part of what is presented and weighed,
not a self-passed gate. The operator's decision to proceed is
the transition to implement; until the operator proceeds, the
phase continues and the loop may run further cycles.

### 4.2 implement

implement carries out the locked design recorded in the tracker,
producing the work.

The locked design is the authority. The existing work product and
surrounding conventions are context, not authority — where they
diverge from the locked design, the design governs. The work is derived from the
design first; existing patterns are evaluated for fit afterward.

Discovery in implement is minimal. A new finding during
implementation is **major new scope** (and triggers loopback) if
any of:

1. Touches an element or contract not in the unit's listed scope
2. Changes a locked contract's members (the instance defines what counts)
3. Introduces a new design decision (per §5.2)
4. Crosses a sibling unit's scope (breaks the disjointness basis)

Otherwise it is a **local clarification** — recorded in the
tracker; the unit proceeds. No work is lost when loopback fires.

**The impl plan.** implement opens with an impl plan: the locked
design's decisions grouped into **dispatch units**, dependency-
ordered, with a parallel-eligibility marker on each — a planning
artifact, not a new tracker construct. Parallel-eligibility is a
load-bearing claim per §3.2: a unit's element and contract scopes are
listed and the disjointness from sibling units' scopes established
by the re-runnable search behind the claim, not by recall. A unit
whose disjointness is not search-established is sequential. The
plan is persisted alongside the tracker (`modules.md` §3.3).

**Dispatch.** When the impl plan has two or more units, each unit's
work is dispatched to a subagent isolated from the run's working
context; a single-unit plan is implemented in the working context.
The subagent is briefed artifact-driven, mirroring verify (§4.3):
it loads the orchestrator's skill files and receives the tracker
plus the locked contracts the unit honors. The default is the
full tracker; reduction to the unit's in-scope decisions is
permitted only when the orchestrator cites a concrete cause
(e.g., tracker size exceeds the subagent's context budget),
recorded as the basis (§3.2) for the reduction. It implements the in-scope
decisions; it does not design — major new scope halts it (below).
Parallel-eligible units may be dispatched concurrently; the
disjointness basis makes that safe.

**Self-check at dispatch boundary.** Before returning state, the
dispatched subagent (and the working context, for a single-unit
plan) applies the standardized lenses most relevant to write-time
issues — the instance specifies which ones (`modules.md` §2.2) —
to its diff against the unit's in-scope locked design decisions. Findings are entered as
fixed-shape ledger lines (`modules.md` §3.1) and returned with
state; the orchestrator appends per Tracker writes below. The
self-check compounds with the design-time forcing function for
delete/replace/amend decisions (§3.2): the basis enumerates
references as of [READY]; the self-check catches references and
behaviors introduced post-design (new docstrings, new branches, new
failure modes the unit's diff introduces). The check is
unconditional — applied at every dispatch boundary, and by the
working context for a single-unit plan. A self-check finding
of major-new-scope shape triggers the loopback below; an in-scope
concern is appended for verify's later sweep but does not halt the
unit.

**Tracker writes.** The orchestrator (§6) owns the tracker append.
A dispatched subagent does not write directly; on completion or
halt it returns state — findings, the unit's commit reference, a
loopback signal where applicable — and the orchestrator appends in
deterministic order. The append-only model (`modules.md` §3.1) is
preserved without concurrency machinery.

**Loopback across the subagent boundary.** A subagent finding
major new scope halts and returns a loopback-required result with
four fields:

- **trigger** — the artifact, code site, or signal the subagent
  encountered
- **scope** — what's outside the locked design (specific element,
  contract, or behavior)
- **basis** — the re-runnable search or read that surfaced it
  (per §3.2)
- **affected_decisions** — locked design decisions invalidated or
  extended (cited by §5.2 identifier)

On receiving it, the orchestrator halts other in-flight parallel
subagents (their work may rest on the disjoint-scope claim the
new finding contradicts), preserves committed work and tracker
state, and returns the run to investigate-design with the
four-field result feeding the new cycle. The pattern mirrors
verify's [ISSUES FOUND] return (§4.3, §6).

**Checkpoint.** A dispatch unit's work product is committed on
completion (instance-specific persistence artifact) and the
orchestrator appends the commit reference to the tracker. The
commit plus tracker line is the unit's persistence artifact: a run
interrupted mid-implement resumes from the tracker — the
last-completed unit, the next per the impl plan (§6, Run
lifecycle). Without per-unit commits, resume must re-derive from
work-product state — a silent-substitution shape this rule closes.

implement reports completion when every unit in the impl plan is
completed. The implement→verify transition is not gated: verify
(§4.3) is itself the check on implement, so an incomplete
implementation surfaces as verify findings rather than passing
silently.

### 4.3 verify

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
judgment the run makes per task. verify's recorded result names the
context it was conducted in, so a [PASSED] carries whether the check
was independent. If an isolated context genuinely cannot be
established, verify is still conducted, without isolation, and its
result records that — an un-isolated verify is never silently taken
as though it were independent.

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
Any non-failure output the executable verification surfaces is
also a finding unless the project has explicitly de-prioritized
that output class. **De-prioritization** requires an artifact:
a project config naming the class, or a tracker entry recording
the class + reason. De-prioritization without an artifact is
the silent-substitution shape (§3.2) the rule rejects. Every
divergence or issue is recorded as a **finding**, entering the
finding track (§5.1) at [PENDING].

verify's terminal result is **[PASSED]** — every check accounted for
and no finding short of [VERIFIED] — or **[ISSUES FOUND]**. The
result is recorded as an evidence-bearing artifact (§3.1): the result
line is paired with a **finding-status ledger** enumerating every
recorded finding's current status. A [PASSED] alongside any finding
short of [VERIFIED] is a malformed artifact.

[ISSUES FOUND] returns the run to investigate-design (§6 loopback).
The fix runs through the full procedure: investigate-design →
implement → verify. There is no in-place shortcut at verify-terminal
— no fix-in-implement bypass and no accept-as-followup at the
verify boundary in either mode. The re-run is either a **fresh
verify pass** (full re-attest) when the fix changes load-bearing
behavior, or a **delta verify** (confirm finding closed + minimal
regression) when the fix is **behavior-preserving** (instance-
defined). Classification recorded in tracker; un-classified defaults
to fresh.

---

## 5. The status-state machine

A status tag records the state of a finding or a design decision.
There are two tracks. ([PASSED] and [ISSUES FOUND] — verify's phase
result — are not a track; they are specified in §4.3.)

Three tags appear in both tracks, track-scoped and with one
consistent sense: **[PENDING]** (recorded, not yet at a terminal),
**[VERIFIED]** (a verified terminal), **[INVALIDATED]** (a verified
terminal contradicted by later evidence). The reuse is deliberate —
one vocabulary across both tracks.

### 5.1 Finding states

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
verification is corrected — appended as a new line at its current
status (`modules.md` §3.1); verification continues.

A [VERIFIED] finding can then be invalidated:

4. **[INVALIDATED]** — a [VERIFIED] finding contradicted by later
   evidence. An [INVALIDATED] finding reopens — it reverts to
   [PENDING] for re-verification — and holds the phase (§5.3) until
   it does. Only a [VERIFIED] finding becomes [INVALIDATED]; one
   contradicted before [VERIFIED] is simply corrected.

### 5.2 Design-decision states

A design decision is the AI's resolved choice about what to build — a
**committed position**, including a choice to defer or exclude. It is
never an open question or a choice posed to the operator: per §3.1 a
question is the absence of a resolution and yields no valid artifact,
so the design-decision track holds none. It carries that resolution,
a **basis** (§3.2) — the evidence the choice rests on, or, where it
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
5. **[AUTO-ACCEPTED]** — a [CONDITIONAL] decision the AI's committed
   recommendation was taken as default when the operator did not
   override: in interactive mode, by the operator selecting proceed at
   the closed-artifact presentation without overriding any open
   [CONDITIONAL] (`modules.md` §1.1); in auto-battle mode, by the
   absence of an operator (`modules.md` §1.2). The recommendation
   stands; the assumption it rested on was not verified —
   [AUTO-ACCEPTED] records exactly that, and does not claim the
   verification that [VERIFIED] does. Both modes reach this state; the
   difference is who-or-what occupies the decision-moment.
6. **[INVALIDATED]** — a [VERIFIED] or [AUTO-ACCEPTED] decision
   contradicted by later evidence.

**Transitions between concrete states.** A [PENDING] decision
found to rest on an unverified assumption becomes [CONDITIONAL];
a [CONDITIONAL] decision becomes [VERIFIED] when its assumption
is verified, and reverts to [PENDING] if the assumption is
disproved. A [CONDITIONAL] decision still resting on its
assumption at [READY] becomes [AUTO-ACCEPTED] (triggers per #5).
An [INVALIDATED] decision reverts to [PENDING], and any decision
that depended on it reverts with it; the phase holds (§5.3)
until re-formed. **Contradiction includes amendment of recorded
resolution** (target naming, scope, completeness counts, basis
source); any such change to a [VERIFIED]/[AUTO-ACCEPTED] decision
flips through [INVALIDATED]→[PENDING] (forces cycle-another
§4.1.3). Silent in-place edit (same status, changed resolution)
is a malformed artifact. Basis-only refinement (`modules.md` §3.1
sub-annotation, resolution unchanged) is not amendment.

A design decision's basis can be broken by another decision,
not only by external evidence. When a decision is locked or its
meaning changes, examine it against the run's other recorded
decisions — does it break what any of their bases rest on. A
broken-basis decision is reopened per the rule above
([INVALIDATED] or revised). The examination is incremental, not
pairwise: the newly locked/changed decision against existing
ones. This holds whether or not the affected decision's work
product exists yet — the contradiction is between decisions,
not in the work product.

### 5.3 Relationship to [READY]

[READY] (§4.1) is the point at which the working context judges the
design complete. The tracker state it weighs in that judgment: no
finding is [INVALIDATED], no load-bearing finding is left below
[VERIFIED], and every design decision is [VERIFIED] or
[AUTO-ACCEPTED] (§5.2 — triggers per §5.2 #5). An [INVALIDATED]
finding, a load-bearing finding short of [VERIFIED], or a design
decision short of that bar is an unresolved concern — the design is
not complete, and the loop continues.

These are the status the tracker carries — a notebook of where each
concern stands — that the AI reads when it judges the design complete
and presents it (§4.1). They are not gate-conditions a separate
evaluation re-derives.

---

## 6. Orchestrator

The orchestrator conducts a run through the phase pipeline. The
phases (§4) and the status-state machine (§5) define the work and its
transitions; the orchestrator runs the phases in order, holds the
transitions, and manages the run's lifecycle.

**Run start.** The orchestrator detects the run's mode (§1) and
enters investigate-design. Mode detection and the per-mode conduct of
the run are specified in `modules.md` §1.

**Sequencing and transitions.** The orchestrator advances
investigate-design → implement → verify, entering a phase only when
its predecessor has reported completion. The investigate-design →
implement transition is [READY] (§4.1, §5.3): implement is not entered
until the operator, presented the design, decides to proceed. The
orchestrator establishes verify in a context isolated from the one
that ran the work, each time verify is conducted — on first reaching
it, and on each re-run after [ISSUES FOUND] (§4.3).

**Dispatch in implement.** The orchestrator carries out the impl-phase
dispatch protocol specified in §4.2: dispatching units to subagents
when the impl plan has two or more units, owning the tracker append,
honoring the loopback shape across the subagent boundary. The
mechanics live in §4.2.

**Loopbacks.** A phase may return the run to an earlier phase; the
orchestrator honors the return rather than proceeding. The specific
returns are specified at their source: implement → investigate-design
on major new scope (§4.2, including the dispatched-subagent boundary
case); [INVALIDATED] finding or design decision reopens design work
(§5); verify ending [ISSUES FOUND] returns the run to
investigate-design — the single locus for fix resolution; the fix
runs through the full procedure before verify re-runs (§4.3).

**Run lifecycle.** A run starts at investigate-design and ends when
verify reports [PASSED]. A run's state — the tracker (§5) and the
phase it is in — persists across interruptions; a run interrupted
mid-flight resumes from that state rather than restarting.

**Halt and surface.** When the orchestrator cannot advance — a phase
cannot complete — it halts the run and surfaces the reason; it does
not advance past the incomplete phase. A decision that needs the operator is
not such a case: in interactive mode it is held as [CONDITIONAL]
until the operator resolves it; in auto-battle it becomes
[AUTO-ACCEPTED] and the run proceeds (§5.2, `modules.md` §1.2).
Auto-battle's remaining halt conditions are part of that mode's
design (`modules.md` §1.2).
