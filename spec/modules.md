# Anneal Framework — Modules

The framework's revisable modules — modes, the standardized lens set,
artifact formats. Built on `core.md` and `glossary.md`; terms are
used as defined there.

---

## 1. Modes

A run is driven in one of two modes. A run is interactive by
default; it is in auto-battle only when auto-battle is explicitly
requested at invocation. The orchestrator detects the mode at run
start (`core.md` §6).

### 1.1 interactive

The operator advances the run. After each investigate-design cycle,
and at each phase boundary, the AI presents a **closed artifact** —
the tracker (its findings and recorded design decisions), a
recommendation, and the menu — and nothing else. Design decisions are
recorded in the tracker; they are never posed to the operator as
questions or choices (`core.md` §1, §5.2). The **menu** carries only
loop control: the operator selects an option — `another cycle` (run
the loop again) or `next phase` (transition). The operator's input
on a design decision
is free-form override against the recorded tracker (`core.md` §1) —
never an answer to a posed choice. The AI may suggest *example*
wording the operator could use — lowering friction without
restricting the reply. Posing a binary or n-ary choice ("A or B?") is
the line: it constrains the operator's input to selected options and
is not permitted.

The menu **persists**. It is the last element of every response until
the operator selects `another cycle` or `next phase`. The operator
may interject
free-form instead of selecting — a question, a comment, an override;
the AI answers the question or applies the override, and then
re-presents the menu. The operator never loses the advance choice.

**Closed-artifact form.** The closed artifact contains these named
sections in this order. Each section is required; missing or
out-of-order sections make the artifact malformed:

1. **State summary** — what the operator decides on first:
   counts (findings + decisions by status), the last cycle's
   standardized-pass status (clean or line items), the
   fresh-session implementability result line (PASSED / FAILED
   per `core.md` §4.1), **the convergence-cycle status** when at
   [READY] (the convergence cycle's investigation-pass artifact
   citation + falsification-pass artifact citation + zero-D-delta
   confirmation per `core.md` §4.1.4),
   named blockers preventing [READY] (open [PENDING] decisions
   and weak-basis ledger entries), **impl plan preview at
   [READY]** — header line with unit count + run-level
   sequential-vs-parallel summary + the disjointness basis
   citation; followed by one line per dispatch unit naming
   dependencies (after which units, or "first" if none) and
   parallelism (parallel with which units, or "sequential"),
   per `core.md` §4.2. Decision-relevant content first; detail
   follows.
2. **Inventories** — findings and decisions as scannable
   one-per-line ledger entries with status tag and identifier at
   start; not paragraph-prose summaries.
3. **Persisted artifacts** — citations to where detail lives
   (tracker file path, standardized-pass artifact path). The
   closed artifact references; it does not paragraph-summarize.
4. **Recommendation** — the AI's next-step proposal,
   thorough-fix-shaped per `core.md` §1; rationale and any "not
   recommended because…" callouts in this section. **For each
   open [CONDITIONAL] decision, the AI's committed default
   surfaces crisply** — what the operator accepts by selecting
   `next phase`; the [CONDITIONAL] then records [AUTO-ACCEPTED]
   (`core.md` §5.2). Operator's free-form override against the
   tracker is available in either mode (`core.md` §1).
5. **Menu** — `(a)nother cycle` / `(n)ext phase` only; accept
   `a` or `n` as menu selection; plain otherwise; no inline
   annotations except a single `← recommended` tag on the
   option matching section 4's recommendation. The tag is
   mandatory: every menu has exactly one tagged option.

**Presentation.** Search commands, file paths, tracker citations
are presented as code, not buried in prose.

The closed artifact surfaces the design for the operator's
menu/free-form decision moment (interactive mode); in auto-battle
no closed artifact is presented — the [AUTO-ACCEPTED] decisions +
fresh-session result line + tracker entries persist for the
operator's review if and when invoked.

### 1.2 auto-battle

Auto-battle is **interactive minus the operator**. Every protocol
behavior — cycle loop, lens application, basis-rule discipline,
tracker shape, dispatch self-check (`core.md` §4.2), verify
isolation (`core.md` §4.3), [CONDITIONAL] handling — is identical to
interactive mode. The single difference is the operator slot at
decision moments: in interactive, an operator selects `another cycle`
or `next phase` at the closed-artifact presentation; in auto-battle, no
operator is present, so the AI's committed recommendation is taken
as default automatically.

The loop self-advances without per-cycle operator input. Cycles run
until the working context judges the design complete (`core.md` §4.1,
[READY]). At [READY], where interactive presents the closed artifact
and waits for the operator's next-phase selection, auto-battle skips
the presentation and proceeds directly — the same default-take of
the AI's recommendation, just without the operator-present-to-attest.

A [CONDITIONAL] decision still resting on its assumption when the
design reaches [READY] is recorded [AUTO-ACCEPTED] in both modes
(triggers + semantics per `core.md` §5.2 #5). Every [AUTO-ACCEPTED]
decision is, by its tag, surfaced in the tracker for the operator's
review of the completed run.

Verify [ISSUES FOUND] in auto-battle triggers automatic loopback to
investigate-design (`core.md` §4.3, §6). A finding that closes
[VERIFIED — deferred] (`core.md` §5.1) does not trigger loopback —
the disposition cites the existing [AUTO-ACCEPTED] decision and the
run completes; the AI's prior judgment to defer is preserved for
the operator's post-run review. Other halt conditions — phases that
genuinely cannot complete on causes other than [ISSUES FOUND] —
remain a separate effort, not yet undertaken.

## 2. The standardized lens set

The standardized lenses are the pre-written inspection criteria the
standardized inspection pass applies (`core.md` §4.1). The set is
closed: a lens is in the set or it is not, and "did the pass apply
all of them" is answerable.

### 2.1 Lens-entry shape

Each standardized lens is specified by:

| Slot | Meaning |
|---|---|
| Name | the lens's identifier |
| Question | the single question the lens asks of the work |
| Scope | what the lens applies to, and the trigger that brings it into a cycle's standardized pass |

### 2.2 The set

The set itself — the specific lenses — is the domain instance's
content: the recurring blind-spots of the domain, each filling the
§2.1 shape. The instance specifies it; the framework
requires the set be closed — a lens is in it or not. Completeness
for the domain is the aim, not a checkable property: it is approached
as real use surfaces missing lenses (see `../instantiation-guide.md`).
Clippy's coding lens set is an example instance.

## 3. Artifact formats

### 3.1 The tracker

The tracker holds two tracks (`core.md` §5): findings and design
decisions. Each entry is a **fixed-shape ledger line** — a status
tag, a summary, and an evidence-or-basis field — and carries nothing
else:

- **Finding** — a status tag, a summary of what was found, and its
  verification evidence.
- **Design decision** — a status tag, a summary of the committed
  position, and its basis (`core.md` §3.2).

The evidence and basis fields hold a `core.md` §3.2 artifact — a
located read, or the re-runnable search behind a completeness claim
(the executable query, not the count it returned) — not prose
describing one; a free-text account of having looked is not a basis
(`core.md` §3.2), and neither is a bare count with no query behind it
— in a tracker entry, each is a malformed field. The summary is one
sentence by default; multi-sentence is permitted where each
additional sentence carries a cited rationale or premise (the
basis-rule discipline applies within the summary, not only at the
basis field). An entry has no narrative field: floating uncited
reasoning does not belong in the tracker — the tracker is the run's
ledger, not its design narrative. **Derivation walk-throughs** —
multi-step prose tracing *how* a conclusion follows from citations
("X at line A calls Y, which acquires Z at line B, therefore…") —
are working context, not basis: record the conclusion, omit the
steps.
The standardized-pass findings artifact (§3.2) is a separate
per-cycle artifact, not part of the tracker.

A design decision may carry, as an optional sub-line under its peer
entry, a structured **considered** field — one line per alternative
in the shape `considered: <alternative> (rejected: <reason>)`. The
rejection reason carries a cited basis (`core.md` §3.2) where
applicable; loose narrative does not belong here. The field is
optional — fabricating alternatives degrades the ledger. Use it
where alternatives were genuinely weighed and naming them informs a
later reader (the operator at [READY] or post-hoc debugging).

The tracker is **append-only** at the **ledger** layer. A new entry,
and every later change to an entry — a new status, a corrected
summary — is a new ledger line appended to the tracker; existing
ledger lines are never edited. Instance renders carry a header above
the ledger with the run identifier, status (an instance-defined
closed enum), current phase (an instance-defined closed enum),
mode, and a one-line task summary. The header is mutable
run-state distinct from the append-only ledger; updating header
fields is not an edit to ledger lines. Instances enumerate their
Status and Phase values in their tracker reference doc. Two
malformed annotation shapes: within-field qualifier on a bare
enum value (e.g. "PASSED (1st pass)" — the common-word-qualifier
symptom, `skill-craft/references/anti-patterns.md`); and
cross-field conflation (e.g. "verify [PASSED]" — embedding the
Status value inside the Phase field, or vice versa). Each ledger
line carries its entry's identifier, and an entry's current state is
its latest line: where current state is needed — at [READY], a
resume, verify (`core.md` §4.3), the closed artifact — it is the
tracker reduced to the latest line per entry. The append-only
history is the run's audit trail; because no ledger line is ever
rewritten, no past entry can be silently altered.

A **basis-only refinement** on a terminal-status entry
([VERIFIED], or [AUTO-ACCEPTED] for an auto-battle design
decision) — same status and summary, strengthened basis — is
appended as a **sub-annotation** under the entry, not a new
peer-level line. Reduce-to-latest reads each entry's latest
peer-level line plus its sub-annotations. The append-only
property holds — sub-annotations are themselves appended, no
past line is rewritten — without the duplicate-line tax of
re-emitting peer-level lines for evidence-only updates.

**Sub-annotations are scoped to basis-only refinement of the
parent entry's own claim** (same status, same summary,
strengthened basis). Cross-unit observations, recurrence-
confirmations (e.g. "the pattern observed in F-N also appears
in Unit X's data"), and any findings that surface a new claim —
even one related to or confirming a prior entry — appear as
peer-level F-entries with their own basis, not as sub-annotations
under the related entry. The discriminator: does the new evidence
strengthen the parent's own claim verbatim, or does it constitute
its own observation? Verbatim-strengthening → sub-annotation;
new observation → peer-level entry.

### 3.2 The standardized-pass findings artifact

Each cycle's standardized inspection pass emits a findings artifact
(`core.md` §4.1): one line for each lens whose scope the cycle touched
— a finding, or a cited-clean reason. **Each line cites this-cycle
basis: a this-cycle tracker entry (F# from this cycle's investigation
pass, or D# from this cycle's design work) or a surface (file:line,
grep query) introduced in this cycle. A line whose only basis is
prior-cycle entries is malformed — its lens was not touched this
cycle.** A lens out of scope that cycle is not
lined; the standardized set is accounted for whole once, at [READY]
(`core.md` §4.1).

### 3.3 The impl plan

implement-phase's planning artifact (`core.md` §4.2): a list of
**dispatch units** in dependency order, with a parallel-eligibility
marker on each. A dispatch unit is a group of design decisions
implemented together as one piece of work; the unit's entry cites
the [VERIFIED] decisions it implements (by their tracker
identifiers).

Parallel-eligibility is a load-bearing claim per `core.md` §3.2: the
unit's element and contract scopes are listed, and the disjointness
from any in-flight unit's scope is established by the re-runnable
search behind the claim — the executable query, not the asserted
disjointness or a recalled enumeration. The scope listing is the
per-unit artifact the orchestrator uses at runtime (`core.md` §4.2
Dispatch) to check disjointness against the in-flight set before each
dispatch. A unit whose disjointness is not search-established is
sequential by default. The basis-rule discipline that governs
decision bases (`core.md` §3.2) applies here in the same form: a
recalled disjointness is not a basis; the search is.

The plan is persisted alongside the tracker — a phase-start artifact,
kept for the run's history and for resume. Like the standardized-pass
artifact (§3.2), it is a per-phase artifact persisted alongside the
tracker, not filed into it.

The plan is immutable across the impl phase: completion lives on
the tracker via each dispatch unit's commit reference (`core.md`
§4.2), not in the plan itself. Only a loopback to investigate-design
(`core.md` §4.2, §6) invalidates the plan, in which case a new plan
is produced after the next [READY], reflecting any changes to the
locked design.

**Dispatch-brief schema.** Each dispatch carries a brief to its
subagent that follows a closed-section form: (a) **load
instructions** — the orchestrator's skill files to read; (b)
**tracker reference** — at implement dispatch, full tracker or
the cited reduction (`core.md` §4.2); at verify dispatch
(`core.md` §4.3) and convergence-falsification dispatch
(`core.md` §4.1.4), the §3.1 reduced-to-latest projection —
the orchestrator produces the projection before brief
construction; the raw tracker remains accessible to the
subagent for ledger-history inspection; (c) **unit scope** —
at implement dispatch, the [VERIFIED] decisions this unit
implements (by tracker identifier) plus the unit's element
and contract scopes; at convergence-falsification dispatch,
the [VERIFIED] D-entry set at the convergence cycle's start
(by tracker identifier); (d) **return-state expectations** —
at implement dispatch, the fixed-shape ledger lines for new
findings (§3.1), the unit's commit reference, and any
loopback signal; at convergence-falsification dispatch, the
§3.4 per-decision artifact — one line per [VERIFIED] entry,
coverage-checked by the orchestrator on return (`core.md`
§4.1.4). Sections (a) AND (d) are uniform across dispatches
within a run and live in the instance's phase files as a
reusable template the subagent loads on dispatch; only
sections (b) and (c) carry per-dispatch parameters written
into each brief. The brief MUST NOT restate (a) or (d)
content — those live in the template only; the brief
references them by section letter.

### 3.4 The falsification-pass artifact

The convergence cycle's falsification pass (`core.md` §4.1.4)
emits a per-decision artifact: one line per [VERIFIED] D-entry
at the start of the convergence cycle, in the shape
`{decision-ID, falsification-candidate, result, holds-or-falsified}`.
Produced by the fresh-context falsification subagent dispatched
per `core.md` §4.1.4; the orchestrator coverage-checks the
returned artifact (line count against [VERIFIED] entry count)
on return.

- **decision-ID** — the D# being attempted.
- **falsification-candidate** — an executable query (grep,
  search) or located read (file:line) whose positive result
  would invalidate the entry's basis. Form follows §3.2 — the
  candidate is a search-established artifact, not a recalled
  hypothesis. A candidate whose negative result would not
  invalidate the basis is malformed: the candidate must be
  capable of returning falsifying evidence if the basis is
  wrong.
- **result** — the actual output of running the candidate:
  cited matches (file:line) for a search, content for a read.
- **holds-or-falsified** — binary, computed from the result:
  `holds` if no falsifying evidence returned; `falsified`
  otherwise. `falsified` flips the entry through
  [INVALIDATED]→[PENDING] (per `core.md` §5.2).

A [VERIFIED] entry without a falsification-pass line at the
convergence cycle is a malformed artifact — the [READY]
declaration requires the pass complete across all [VERIFIED]
entries (`core.md` §4.1.4).

The artifact is per-cycle, fired only at the convergence cycle
(not at every cycle's standardized pass). Persisted alongside
the cycle's standardized-pass findings (§3.2); instances supply
the file location per their run-artifact persistence mechanism.

## 4. Post-run review

An optional analysis step: surface what the protocol missed or got
wrong in this run, to inform the next iteration. This is the
framework's empirical-validation procedure — the input that drives
the next amendment cycle (`development-process.md`).

This section specifies the minimum shape (when, output discipline,
question dimensions). The full procedure — the standing questions
themselves and their state-aware Q7 walk — lives in framework-root
`post-run-review.md` and is rendered to instance `references/
post-run-review.md`. The spec carries the minimum; the procedure
carries the operative detail.

### 4.1 When and how

**At any point during or after a run, at the operator's
discretion** — at completion (verify [PASSED]), mid-run after a
[READY] presentation, after a verify result, after a cycle that
surfaced unexpected findings, or after an interruption. The
post-run review is an analysis tool for the *protocol's
execution*, not a phase-gated artifact. The operator **may**
request a review; the AI does not prompt for one.

### 4.2 Output, no persistence

Conduct the review in the session — output to the operator. Do
**not** persist the review or its findings to a file in the
project. Persisting prior-run analysis would pollute future runs
(a later run reading prior-run conclusions is biased by them) and
clutter the project tree. The operator carries forward what matters
by their own means.

### 4.3 Standing questions

Four questions, each phrased **artifact-forcing** (specific quotes,
counts, classifications — not impressions):

- **Misses.** List every design defect the run produced. Classify
  each as an *escape* (implement or verify recorded it past [READY])
  or an *operator catch* (caught at [READY] presentation, before
  proceeding). For each: name which investigate-design check (a
  specific lens, the basis rule, the [READY] judgment) should have
  caught it and why it didn't; or state "no existing check covers
  this class."
- **Cost.** Where did this run's effort go: token-heavy or
  time-heavy regions, repeated work, fixed-shape attestation? Name
  any work the protocol forced but the run didn't need — quote the
  procedure parts.
- **Gaps.** Did the AI add any ad-hoc check, step, or instruction
  not in the protocol this run? For each: quote the ad-hoc work
  verbatim, name the gap it was covering, and say whether the gap
  is particular to this task or generalizable across runs.
- **Attribution.** Tag every finding by what surfaced it — a
  standardized lens / ad-hoc investigation / the basis rule forcing
  a search / a cycle re-examination / verify. Counts.

### 4.4 Artifact-forcing throughout

A generic "did the protocol help" yields sycophantic mush. A forced
artifact yields data that can be wrong and checked. Use:
"quote it verbatim", "give the count", "classify into one of N",
"diff against retained run X."

### 4.5 What outcomes mean

The review surfaces; the operator decides what to do. The
framework's triage applies (`development-process.md` practice 1):

- A **render gap** — the instance file does not faithfully carry
  the spec → re-render.
- A **spec gap** — the render is faithful and was followed, and it
  still broke → a finding for the framework spec.
- An **adherence gap** — a faithful render of an unambiguous,
  evidence-bearing rule, violated anyway → failure indicator
  requiring practice 1's three-form structural-enforcement
  enumeration; residual accepted only after enumeration shows all
  three forms fail with cited per-form failure reasons.

### 4.6 What this is not

A general code review. A confidence check. A graded report. The
review's only job is to surface what the *protocol* missed or got
wrong, in a form the operator can act on.
