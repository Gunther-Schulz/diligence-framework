# Post-run review

Companion to `dev-notes/validation-watch.md`; not part of the spec. The
framework's empirical-validation procedure: when a session has run
the instance on a real task, review the run against the spec. The
review's deviations are triaged (`development-process.md` practice
1) — render gap, spec gap, or adherence gap — and feed the
post-analysis loop. This file specifies how the review is conducted.

## When to run

**Post-run review is a debugging tool, not a routine check.**
Normal interactive runs and auto-battle runs do not invoke it.
The operator invokes it only when investigating a specific
issue, auditing a release's behavior, or empirically validating
spec changes. The Q-set therefore does not need to fire on every
run — it fires on suspicion. Mechanisms that need to fire on
every run (e.g., catching ad-hoc impl decisions via the verify-
phase design-completeness audit, `core.md` §4.3) belong in-phase,
not here.

**At any point during or after a run, at the operator's
discretion** — at completion (verify [PASSED]), mid-run after a
[READY] presentation, after a verify result, after a cycle that
surfaced unexpected findings, or after an interruption. The
post-run review is an analysis tool for the *protocol's
execution*, not a phase-gated artifact — invocable at any state
the operator wants to inspect.

Especially valuable after a release that changed instance
behavior (the run is the change's empirical test) and after
runs where the operator overrode a phase transition (e.g.,
selected `another cycle` at [READY]) — the override itself is data.

Q's that depend on a phase not yet reached (e.g., Q6 verify-
phase audit before verify has fired) classify as **not yet
applicable to this run state** rather than skipped silently. The
operator decides when a run (in progress or complete) warrants
the analysis; the instance does not prompt for one.

## The output

The review's output is **delivered to the operator in the session**
— not persisted to a file in the project. Persisting prior-run
analysis to the project directory would pollute future runs (a
later run reading prior-run conclusions is biased by them) and
clutter the project tree. The operator carries forward what
matters by their own means: a chat paste into the next session, an
external note, an issue, a memory entry. The discipline lives in
(a) the artifact-forcing questions asked here and (b) the
operator's retention of the answers.

## Standing questions

Questions **surface observable artifacts** (counts,
classifications, quotes, walks, named symptoms); they do **not**
prescribe actions on those artifacts. Action emerges from
operator+AI judgment in the session, applying the framework's
existing disciplines (`development-process.md` practice 1 triage,
practice 8 structural-form enumeration). A Q that prescribes
"ship X" / "observe Y" over-reaches the review's purpose — the
session decides.

Phrase each question **artifact-forcing** — "quote it verbatim,"
"give the count," "classify into one of N," "diff against the
retained tracker of run X." Generic "did it help" yields
sycophantic mush; a forced artifact yields data that can be wrong
and checked.

### Q1. Design defects — misses (the keystone)

> List every design defect the run produced. Classify each as an
> **escape** (implement or verify recorded it past `[READY]`) or an
> **operator catch** (the operator caught it at the `[READY]`
> presentation, before the run proceeded). For each: name which
> investigate-design check (a specific lens, the basis rule, the
> `[READY]` judgement) should have caught it and why it didn't; or
> state "no existing check covers this class."

This measures the design phase's true failure rate. Zero defects
means the design phase is working autonomously; an operator catch
means the design phase missed but the `[READY]` presentation caught
(protocol-as-designed); an escape means both missed (caught only by
implement-loopback or verify — the most expensive catch). Each
non-zero count names a concrete blind spot, triaged per
`development-process.md` practice 1.
### Q3. Grind — cost

> Where did this run's effort go: token-heavy or time-heavy regions,
> repeated work, fixed-shape attestation? Identify any work the
> protocol forced but the run didn't need — quote the specific
> procedure parts that felt unnecessary. Specific examples, not
> impressions.

Cost matters. A protocol that catches everything but costs many
times what it should is broken in its own way. Grind reductions
(v0.7.0→v0.8.0, v0.8.3, the basis-only sub-annotation) all started
from this kind of observation. Artifact-forcing: name the procedure
parts, quote the tracker lines or pass artifacts, don't
generalize.

### Q4. Ad-hoc additions — gaps

> Did you add any ad-hoc check, step, or instruction not in the
> protocol this run? For each: quote the ad-hoc work verbatim, name
> the gap it was covering, and say whether the gap is particular to
> this task or generalizable across runs.

Ad-hoc additions are how protocol gaps surface — the AI noticed
something the protocol didn't cover and patched it. F18 (Unit-4's
ad-hoc pairwise cross-decision coherence check) was this pattern;
investigating it surfaced the §5.2 detection gap and produced
v0.8.2. This is the most directly-actionable signal for protocol
completeness.

### Q5. Tracker integrity

> For this run's tracker: was append-only honored at the ledger
> layer (no edits to existing ledger lines — quote any apparent
> edit); were cycle numbers continuous across the run including
> any loopback re-entries (list the sequence); were finding and
> decision identifiers unique with no collisions (list any
> duplicates); did header updates stay within the header
> carve-out (mutable run-state — status, phase, terminal — not
> edits to ledger lines)?

Q5 checks the tracker rules' actual adherence. The tracker is
the run's audit trail (`spec/modules.md` §3.1); silent violations
corrupt the record. Each clause is artifact-forceable (quotes,
lists, counts). A violation triages as adherence-class unless
the spec's wording allowed the violating reading — then it is a
spec gap.

### Q6. Verify-phase audit

> For this run's verify: was the recorded context "isolated"
> (quote the result line's context tag); were all three checks
> accounted for — planned-vs-actual (decision-matching AND
> design-completeness audit per `spec/core.md` §4.3),
> standardized lenses,
> executable verification — with no check silently absent (cite
> each); on [ISSUES FOUND], did the loopback route to
> investigate-design (quote the next-cycle entry); if in
> auto-battle and the convergence exception fired, did the
> finding's evidence field cite the [AUTO-ACCEPTED] decision by
> tracker identifier?

Q6 checks verify-phase discipline (`spec/core.md` §4.3). Verify
is the framework's primary catcher; its discipline failing means
the catcher itself is failing. Mechanical checks; adherence vs
spec triage applies.

### Q7. Validation-watch cross-check

> For each V-N in `dev-notes/validation-watch.md`, read the entry's
> Status line and respond per state:
>
> - **WATCHING**: walk the production signal against this run's
>   tracker. Classify as **confirms** (cite the evidence),
>   **refutes** (cite the evidence), or **no relevant evidence in
>   this run**.
> - **FIX-SHIPPED**: walk for **load-bearing instances** of the
>   mitigation. Classify as **mitigation load-bearing** (cite the
>   finding the mitigation caught + counter-factual: would this
>   have escaped the pre-mitigation protocol?), **mitigation not
>   exercised this run** (failure shape didn't surface), or
>   **mitigation evaded** (a finding escaped that the mitigation
>   should have caught — INVALIDATED trigger).
> - **RESOLVED**: skip — already validated; only re-walk if a
>   later recurrence surfaces in Q1-Q4 findings.
> - **INVALIDATED**: skip — already known to need new analysis.

Q7 actively closes the watch loop. The "outcomes land" routing
below picks up signals passively — it captures only Q1-Q4
findings that happen to bear on a V-N. Q7 forces the per-entry
walk so signals accumulate systematically rather than waiting
for fortuitous correlations. "No relevant evidence" across many
WATCHING entries is itself useful signal — a watch entry nobody
exercises warrants its own scrutiny. A **mitigation load-bearing**
finding on a FIX-SHIPPED entry is the positive evidence needed to
promote it to RESOLVED. The operator decides which V-Ns to
transition from the walk's findings.

### Q2. Value attribution

> Tag every finding F1..Fn by what surfaced it — a standardized
> lens / ad-hoc investigation / the basis rule forcing a search / a
> cycle re-examination / verify. Give the counts.

Descriptive data on which mechanisms produced findings this run.
Useful context — **not** a verdict on whether a standardized lens
"earns its rent." A lens's job is the rare-but-critical catch — a
lens clean nine runs out of ten that catches a disaster on the
tenth has terrible yield and pays enormous rent. Judge a lens by
its **misses** (Q1 — what its absence let escape), not its
hit-rate (Q2).

### Other artifact-forcing prompts as needed

- "Quote it verbatim" — a specific spec or render line, a tracker
  line, a finding.
- "Diff against retained run X" — for measuring the effect of a
  recent change (e.g. the first run under v0.X.Y diffs against the
  last under v0.X.Y-1).
- "Classify into one of these N options" — for forced choices
  instead of waffle.

## Where outcomes land

- **A render / spec / adherence gap** — per
  `development-process.md` practice 1; the triage routes each.
- **A signal informing a `validation-watch.md` entry** — append to
  or amend the relevant V-N (the watchlist).
- **An instance-level F-finding** — if the instance has an
  F-finding record (e.g. coding-clippy's `docs/spec/STATUS.md`),
  record there.

## What it is not

A general code review. A confidence check ("did Clippy help"). A
graded report. The post-run review's only job is to surface what
the *protocol* missed or got wrong, in a form the next iteration
can read and act on.
