# Anneal Framework — Validation Watch

Companion to the Anneal-framework spec; not part of it. The spec
states fixed decisions. Some were made best-effort, under genuine
uncertainty. This doc records those — the decision, why it was
uncertain, and the production signal that would prompt revisiting it.
The spec stays pure prescription; the uncertainty is tracked here.

Production signals come from any instance's real runs — Clippy's, or
a future sibling's.

**n=1 convention.** Closing criteria are n=1 — one observed instance
is sufficient evidence to transition. The post-run review's
self-review surfaces n=1 evidence per run. Multi-run thresholds
("3+ consecutive runs", "n≥2 distinct shapes", "5+ runs show
absence of recurrence", etc.) are cost-gating dressed as epistemic
humility (per `development-process.md` practice 8) — they defer
classifiable fixes that the lifecycle is designed to process on
first observation. RESOLUTION requires one load-bearing instance;
INVALIDATION requires one recurrence under the fixed spec; entries
are not held open waiting for repetitions.

## Entry lifecycle

Each V-N entry carries a **Status** with one of four values:

- **WATCHING** — uncertainty exists; no structural fix shipped yet.
  Production signal is being watched. If the signal observes per
  `development-process.md` practice 8 (classifiable structural
  fix), ship the fix at n=1 and transition to FIX-SHIPPED.

- **FIX-SHIPPED** — structural fix in spec, dated + commit-cited.
  Still watching, but now for **load-bearing instances** of the
  mitigation: a post-run review identifies a finding the
  mitigation actively caught that would have escaped under the
  pre-mitigation protocol. One observed instance is sufficient
  evidence the mitigation works.

- **RESOLVED** — at least one load-bearing instance observed via
  post-run review. Closing requires **positive evidence** (active
  catch counter-factually shown to require the mitigation), not
  mere absence-of-recurrence — absence is indistinguishable from
  "failure shape didn't surface this run." Once RESOLVED, the
  entry is dormant unless later recurrence reopens it as
  INVALIDATED.

- **INVALIDATED** — production signal recurred under the
  fix-shipped spec. The mitigation didn't hold. Requires new
  analysis; the entry doesn't move forward without a fresh
  structural fix proposal.

**Transitions:**
- WATCHING → FIX-SHIPPED at fix-ship commit
- FIX-SHIPPED → RESOLVED on first observed load-bearing instance
- FIX-SHIPPED → INVALIDATED on first recurrence under new spec
- RESOLVED → INVALIDATED on later recurrence

**Post-run review (Q7) reads status and responds per state.**
FIX-SHIPPED entries are walked for `mitigation load-bearing` /
`mitigation not exercised` / `mitigation evaded` classification.
RESOLVED entries are skipped. WATCHING entries follow the original
production-signal walk.

A V-N's structural design — Decision, Why uncertain, Production
signal to watch, Resolution (when FIX-SHIPPED or beyond) — remains
unchanged. Status is a single line at the top of the entry.

---

## V-1. Standardized lens timing — per-cycle incremental

**Status: WATCHING.**

**Decision (`core.md`).** Standardized lenses are applied every
cycle, incrementally: each cycle's standardized inspection pass
applies the lenses whose scope that cycle's work touched.

**Why uncertain.** Chosen on the fail-safe principle — when
uncertain, check more and check earlier — not on evidence. The one
grounding incident applied the standardized lenses only as a late
correction pass, which was a low-adherence artifact, not a design
choice. There is no comparison between per-cycle and end-only
application; the quantitative value of per-cycle over end-only is
unverified.

**Production signal to watch.** Whether per-cycle standardized passes
mostly come back clean. If they routinely find nothing and findings
cluster only near [READY], end-only sweeping may suffice and
per-cycle is overhead. If per-cycle passes catch things early —
before the design locks them in — per-cycle is confirmed.

---

## V-2. One mechanism — inspection; transitions are operator-judged

**Status: WATCHING.**

**Decision (`glossary.md`, `core.md`).** The framework has one
reusable mechanism: inspection (with an ad-hoc or standardized lens
source). Phase transitions — chiefly [READY] — are not a self-passed
gate on accumulated state; [READY] surfaces the design for the
operator's judgment, and the other transitions are specified
directly by the phase specs and the orchestrator.

**Why uncertain.** This is the lean rework. An earlier model
classified mechanisms as inspection *or* gate and had the run
self-pass a [READY] gate on its tracker tags. A diagnosed failure —
a cross-decision contradiction that passed three [READY] evaluations
(F21) — showed the gate cached a verdict that went stale as the loop
moved the design. The rework cut the gate machinery on that
diagnosis; it is a design call from one failure, not a measured one.

**Production signal to watch.** Whether design defects the old
[READY] gate aimed to catch now reach implement and verify, and
whether catching them there is acceptably cheap — or whether they
slip past verify too. Also whether any mechanism appears in real runs
that is not inspection, which would reopen the need for a mechanism
taxonomy.

**First signal (2026-05-22).** The Unit-3 run (under 0.7.0) is the
first real-run evidence. It surfaced F17/F18/F19 — design decisions
marked [READY] on recalled counts where the basis rule (`core.md`
§3.2) requires a search — and F21, a cross-decision contradiction.
The 0.7.0 isolated [READY] evaluation caught some recall-proxy
errors, missed F21 (it checked decisions singly, never pairwise), and
once false-confirmed a [READY] that implement-start then
contradicted; the operator caught ~2 of ~5 defects by plain review.
Reading: F17–F19 are a basis-rule *adherence* failure — the rule
existed and was correctly rendered; the AI ran the protocol and did
not follow it. The rework removed the isolated evaluation, so
post-0.8.0 that recall-proxy class has no catcher before the
operator's review — the named, accepted residual. It is not a
missing mechanism; adding one was the 0.7.0 reflex this rework
reversed.

---

## V-3. The tracker does not mark a finding's inspection source

**Status: WATCHING.**

**Decision (`modules.md` §3.1).** A tracker finding is a status tag,
a one-sentence summary, and its evidence — it does not record whether
it came from an ad-hoc inspection or a standardized lens. Findings
from both sit undifferentiated in the one finding track. Standardized
coverage is identifiable separately — the per-cycle standardized-pass
artifact (§3.2) accounts for every lens — but not from a finding's
own form.

**Why uncertain.** An ad-hoc inspection that comes back clean
produces a coverage-shaped result ("X checked, clean"); recorded as a
[VERIFIED] finding it is indistinguishable from a standardized lens's
cited-clean line, and can read as protocol coverage when it is a
one-run addition — building a false model of what the protocol
systematically checks. Observed once: a Clippy run recorded an ad-hoc
pairwise cross-decision coherence check in finding form, which read
as protocol-prescribed. A per-finding lens-source marker was judged
not worth it — the investigation pass is mostly ad-hoc, so the marker
would be near-universal noise. Left as-is on one low-severity
occurrence.

**Production signal to watch.** Whether an ad-hoc clean-check, read
as protocol coverage, misleads a real [READY] ratification, or the
pattern recurs across runs. If so, the fix is not a per-finding
field: anchor the [READY] coverage statement to the standardized lens
set, and have an ad-hoc check's clean result labelled as ad-hoc (or
kept out of finding form).

---

## V-4. Standardized pass — in-scope per cycle, whole set at [READY]

**Status: WATCHING.**

**Decision (`core.md` §4.1, `modules.md` §3.2).** Each cycle's
standardized inspection pass emits a line only for the lenses in
scope that cycle; an out-of-scope lens is not lined. The set is
accounted for whole once, at [READY] — every lens applied in the
cycle(s) where its scope was touched, or cited out of scope for the
run. Per-cycle application of in-scope lenses is unchanged.

**Why uncertain.** Earlier the pass accounted for every lens every
cycle, in-scope and out. The every-cycle out-of-scope accounting was
identified as grind, and the fixed ten-row grid as competing with
ad-hoc investigation for attention; the change drops the per-cycle
whole-set attestation and moves omission-visibility to [READY]-time.
It rests on a single run's evidence (Unit-3/Unit-4 — ad-hoc
investigation found the load-bearing defects, and most per-cycle lens
lines recorded what was already in scope). The lower-risk variant was
chosen: per-cycle application of in-scope lenses stays a forcing
function, and the soft-priming variant — priming only, no per-cycle
attestation — was not adopted. One run is still thin evidence for a
cycle-structure change.

**Production signal to watch.** Whether a concern a lens would catch,
that per-cycle attestation surfaced earlier, now slips — caught later
at the [READY] whole-set accounting (acceptable, still before
implement) or past it entirely (not acceptable). And whether the
[READY] accounting reliably catches a lens silently dropped from a
cycle's scope. If lens-catchable concerns routinely reach implement,
the per-cycle whole-set attestation earned its cost and should
return.

---

## V-5. [READY] self-assessment vs external check

**Status: FIX-SHIPPED (2026-05-25, commit e18bca1).** The recurrence
the production-signal watched for was observed in the unit-14 run
(beat-the-books project): cycle 3 declared [READY], operator chose
Continue, cycle 4 surfaced material design corrections (F31-F36 +
D9/D10 amendments). The diagnosis (AI in the working context
answered the fresh-session test from the same recall pool that
wrote the design) confirmed self-assessment alone is insufficient.

**Resolution.** Two layered mitigations now in spec:

1. **§4.1.2 sharpened — per-implementer-step external evidence.**
   The fresh-session-implementability test artifact requires
   file:line citations from re-reading source per implementer
   step, not paraphrases of the tracker. Structural enforcement at
   the AI's self-test moment — forces re-reading (or fabrication,
   which is harder) to satisfy the PASSED artifact.

2. **§4.1.4 added — convergence cycle.** [READY] requires one more
   cycle after the AI's self-test passes, producing zero D-track
   deltas. A full cycle (investigation + standardized inspection
   passes) with enumerated new surfaces, not lens-clean re-attest.
   Catches what the self-test misses by switching the working
   context from self-assessment mode to fresh investigation mode.

**Alternative considered: V-5's original prescribed candidate —
operator-invoked subagent-at-[READY] external check.** Not chosen
because (a) the unit-14 failure shape was recall, not frame, and
the convergence cycle directly addresses recall via fresh
investigation; (b) the convergence cycle reuses existing cycle
machinery rather than adding a new mechanism; (c) operator's
empirical workflow already includes an extra cycle on every run —
the convergence cycle codifies this. The external subagent remains
the defined escalation candidate if **frame-lock failures** emerge
(cycles produce material findings but all reinforce a wrong frame
— a different failure shape that fresh investigation alone might
not catch). Frame-lock has not been observed yet; per practice 8,
the external subagent earns its place at n=1 if observed.

**Closing criterion (FIX-SHIPPED → RESOLVED).** A post-run review
identifies a run where the convergence cycle was load-bearing — it
surfaced a D-track delta that would have escaped under the
pre-fix self-test-only protocol. One observed instance is
sufficient.

**Original observation preserved below for audit trail.**

---

**Decision (`core.md` §4.1, v0.8.7 + v0.8.9).** The [READY] judgment
is sharpened — a presence-based fresh-session-implementability test
plus the named silent-substitution failure shape — but it remains
self-assessment. The producing AI judges whether a fresh session
could implement from the tracker alone. No external check (no
subagent) at [READY]; the operator's review at the closed-artifact
presentation is the only external catcher.

**Why uncertain.** The v0.8.0 lean rework removed the 0.7.0 isolated
[READY] evaluation (a per-cycle automatic subagent that
false-confirmed once and missed cross-decision contradictions). The
replacement is operator-review-at-presentation plus, in v0.8.7/0.8.9,
sharper self-assessment criteria. Whether the named self-assessment
reduces false-[READY]s enough — or whether an external check is
needed — is empirical. Cycle 3 of the Unit-5 run was a false-[READY]
the sharpening targets; the next runs under v0.8.9 are the first
real test. Adding a subagent-at-[READY] check before that evidence
would be the over-mechanization reflex this session repeatedly
reversed.

**Production signal to watch.** Whether false-[READY]s recur under
v0.8.9 — cycles declaring [READY] that subsequent cycles still
surface material design gaps for. If they recur, the candidate fix
is an *operator-invoked* subagent-at-[READY] external check —
structurally different from the 0.7.0 isolated eval: operator-invoked
(not automatic), whole-design (not per-decision), "what would
surface during implementation" simulation (not cached verdict),
output to the operator (not cached in the tracker). If false-[READY]s
do not recur, the named self-assessment is sufficient and no new
mechanism is warranted.

---

## V-6. Implementation decomposition + impl-phase subagent topology

**Status: WATCHING.**

**Decision (`core.md` §4.2, §6; `modules.md` §3.3).** The impl phase
opens with an impl plan: dispatch units derived from the locked
design, dependency-ordered, parallel-eligibility marked with a
search-established disjointness basis. Dispatch to subagents is the
default when the plan has two or more units; a single-unit plan is
implemented in the working context. The orchestrator owns the tracker
append; subagents return state. A subagent surfacing major new scope
triggers a loopback to investigate-design, with other in-flight
parallel subagents halted. Per-unit commits are the checkpoint
discipline that makes resume-from-tracker reliable.

**Why uncertain.** Design completed on n=1 evidence (Unit 5, mid-impl
session-budget exhaustion, 2026-05-23). Ship-fast applied: a
reversible spec change with a real post-analysis hook (this entry),
preferred over withholding for more runs of the unsupported old
protocol. Several calls rest on analogy to verify rather than direct
evidence — that the impl-subagent brief shape mirroring verify will
be artifact-sufficient, that the loopback-from-impl-subagent pattern
works the same as verify's [ISSUES FOUND] return, that one-writer
tracker append remains workable when parallel subagents return state
in short intervals. The ≥2-unit dispatch threshold is a judgment call
balancing verify-isolation symmetry against mechanism-creep on
trivial impls.

**Production signal to watch.** (1) Whether impl-plan production at
implement-start works smoothly — is the dispatch-unit grouping
intuitive from the locked design, is parallel-eligibility usefully
identifiable, does the artifact feel useful or ceremonial. Difficulty
here is also a downstream signal on [READY] quality (V-5): a tracker
[READY]'d but not yielding a well-formed impl plan suggests the
design was incomplete. (2) Whether parallel dispatch actually
parallelizes cleanly in practice (Unit 6 candidate, may not exercise
it to full extent) — tracker write integration, return-state
handling, no race-on-merge surprises. (3) Whether the
loopback-across-boundary protocol fires correctly — subagent halts at
the right moments (not too liberal, not too conservative);
orchestrator's halt-other-subagents works without lost work. (4)
Whether per-unit commits become natural cadence or chafe (too coarse
/ too fine). (5) Whether verify's task remains tractable when reading
code from multiple impl subagents.

**First signal (2026-05-23).** A real instance run hit mid-impl
session-budget exhaustion with ad-hoc per-slice commit + resume
recommendation. Decomposition was clean; resume-from-tracker observed
working in practice. Instance-specific detail (findings, slice
numbers, commit references) lives in the instance's run tracker
(`.clippy/runs/`), not here. Lessons abstracted into the protocol
changes named in subsequent V-N entries.

---

## V-7. Design-decision premise basis — paths, filenames, completeness counts

**Status: FIX-SHIPPED (2026-05-24, commit c5e7ad9).** Downgraded
from RESOLVED 2026-05-25 per the new lifecycle: a fix shipped to
spec is FIX-SHIPPED, not RESOLVED, until a post-run review
identifies a load-bearing instance of the mitigation. The
structural fix is in spec; positive evidence of the fix actively
catching a finding that would have escaped pre-fix has not yet
been recorded.

**Closing criterion (FIX-SHIPPED → RESOLVED).** A post-run review
identifies a run where the §3.2 embedded-claims sharpening or the
Target-locality lens was load-bearing — caught a path / filename /
count claim that the pre-fix protocol would have allowed to slip
into [READY].

**Original observation preserved below for audit trail.**

---

This entry's "if recurrent X, then sharpen the rule" framing was
itself the cost-gating-as-epistemic-humility shape that
`development-process.md` practice 8 ("Validation-watch is not a
deferral journal") now rejects. The proposed sharpening
classified as a **structural enforcement** fix (§3.2 sub-clause
that an embedded design-decision premise carries the basis-rule
requirement separately from the surrounding statement), so it
earned its place at n=1 rather than waiting for recurrence.

**Resolution.** Commit c5e7ad9 sharpened §3.2 with the embedded-
claims principle: "claims embedded within larger statements —
implicit premises in target-naming decisions, cited rules or
prior decisions, completeness counts asserted as facts. Each
embedded claim carries the basis-rule requirement *separately*
from the surrounding statement." Plus the Target-locality lens
(Clippy v0.9.9, DANEEL v0.2.1) is the standardized-inspection
catcher. The class now has a write-time catcher (§3.2 sharpening),
a gate-time catcher (§4.1 [READY] judgment), and a
standardized-inspection-time catcher (Target-locality lens).

**Original observation preserved below for audit trail.**

---

**Decision (`core.md` §3.2).** The basis rule requires every
load-bearing claim and every design premise to carry a named basis.
Applied uniformly: findings cite evidence, design decisions cite
basis. The rule's text did not separately enumerate paths,
filenames, or completeness counts embedded within design
decisions — these were covered by "every design premise" generally
*at the time of this entry's writing* (pre-c5e7ad9).

**Why uncertain (at time of writing).** A real-run incident
(coding-clippy unit-10 file-split refactor, 2026-05-24) surfaced
a class of [READY] escape where the rule was loaded but unevenly
applied: design-decision premises that name a path/filename
("move X to **new file** `overtime_settlement_persistence.py`")
have an implicit completeness claim — "no existing nearby module
is suitable" — that got less rigorous basis-rule application
than explicit findings did. Cycle 2 declared [READY] with this
claim ungrounded; cycle 3 surfaced the existing
`services/autobet/overtime_settlement.py` module that would have
been the natural home, requiring D3 to be re-formed. Same shape
on cross-reference completeness: cycle 2 listed 3 sites, cycle 3
found 7.

The fresh-session implementability test (`core.md` §4.1) PASSED
at cycle 2 — a fresh session reading the tracker would have
implemented the design *as specified*, never surfacing a new
design decision. The test catches **clear-but-incomplete**
designs; it did not catch **clear-but-wrong-target** designs
where the implementation lands cleanly but in the wrong
location. (Now caught by the §3.2 embedded-claims sharpening +
Target-locality lens.)

---

## V-8. Dispatch self-check at the impl-phase subagent boundary

**Status: WATCHING.**

**Decision (`core.md` §4.2 "Self-check at dispatch boundary").**
Each dispatched subagent applies the instance's standardized lenses
against its own diff before returning state. The check compounds with
the design-time forcing function (§3.2) as the implement-time catcher
for references introduced post-design and behaviors slipping the
locked enumeration.

**Why uncertain.** Lever B selected from the impl-phase
lens-application discussion (alongside lever A: catch at orchestrator
post-merge; lever C: defer to verify). Rests on judgment that
per-unit self-check produces a useful signal that compounds with
design-time and verify-time checks rather than duplicating them.
Originally appended as a stowaway addendum inside V-6
(decomposition + topology) — split out at audit time per practice 8
entry hygiene.

**Production signal to watch.** (a) whether the self-check catches
what would otherwise have reached verify in subsequent runs;
(b) per-dispatch overhead remaining acceptable; (c) subagent findings
well-shaped as ledger lines (no free-text drift); (d) loopback-vs-
in-scope-concern classification working — subagents correctly
distinguishing major-new-scope findings that halt the unit from
in-scope concerns that proceed.

---

## V-9. Verify-terminal loopback destination and auto-battle convergence

**Status: WATCHING.**

**Decision (`core.md` §4.3, §6; `modules.md` §1.2).** Verify [ISSUES
FOUND] returns the run to investigate-design — the single locus for
fix resolution. The fix runs through the full procedure
(investigate-design → implement → verify); no in-place shortcut at
verify-terminal in either mode. In auto-battle, loopback is
automatic, with a convergence exception: a verify finding whose
evidence field explicitly cross-references an existing
[AUTO-ACCEPTED] design decision by tracker ID does not trigger
loopback; the run completes with the finding noted as a re-surfacing
alongside the original [AUTO-ACCEPTED] tag, for the operator's
post-run review.

**Why uncertain.** Two judgment calls. (1) Always-loopback to
investigate-design as the single re-entry point — no fix-in-implement
shortcut, no operator-accept-as-followup option at verify-terminal in
interactive — was chosen to unify with implement-loopback (§4.2)
and [INVALIDATED] reopening (§5), and to deny the silent-
accept-by-close pathway observed at n=1 (unit-12 F43/F47, closed as
"scope-proportional gaps" without explicit operator decision — a
deferral-shape resolution the basis rule §3.2 rejects). The cost is
overhead on verify findings that could in principle be addressed in
implement directly; the rationale is that "trivially fixable" is
itself a judgment that belongs in design, not at verify-terminal.
(2) The [AUTO-ACCEPTED]-re-surfacing exception prevents auto-battle
non-convergence on findings the AI already chose to defer at
investigate-design. Originally a naked judgment ("the same gap, now
observed in the work"); sharpened post-n=1 to a mechanical criterion
— the finding's evidence field must cross-reference the
[AUTO-ACCEPTED] decision by tracker ID for the exception to apply.
The remaining uncertainty: whether the verify subagent reliably
*recognizes* when to construct the cross-reference, since a missed
recognition produces a false-new-gap finding which triggers loopback
(conservative; over-loops rather than under-converges).

**Production signal to watch.** (a) Whether always-loopback in
interactive feels right vs heavy for trivial verify findings; whether
operators routinely use free-form override to scope-out a finding
rather than re-investigate. (b) Whether the verify subagent reliably
recognizes when an [AUTO-ACCEPTED] cross-reference applies — under-
recognition produces false-new-gap findings which over-loop
(conservative). Over-recognition is structurally prevented by the
cross-reference-by-tracker-ID criterion (no cross-reference → no
exception). (c) Whether auto-battle converges under the rule in
practice — no observed infinite verify-loopback loops. (d) Whether
the close-with-re-surfacing-notation creates useful post-run review
material or noise.

---

## V-10. D-track delta as convergence criterion

**Status: WATCHING.**

**Decision (`core.md` §4.1.4).** The convergence cycle test for
[READY] uses **D-track delta = 0** as the mechanical convergence
criterion: a cycle producing no new design decisions and no
amendments to existing ones is "converged." F-track entries
(findings) alone don't count as material — only D-track entries
do, since design decisions are the load-bearing artifact that
implement reads.

**Why uncertain.** D-track delta is a *proxy* for "material" —
operator-named at the design moment. The proxy is mechanical and
artifact-observable (delta the two cycles' D-track), which is the
class-1 mitigation skill-craft prefers. But the question whether
D-delta correctly captures *materiality* — every material change
in the design appears as a D-track entry — is empirical.

Possible misses:
- Findings whose implication for the design is real but doesn't
  trigger a D-track update (the AI judges the finding doesn't
  invalidate any decision but later implementation reveals it
  did).
- Amendments expressed as evidence-only sub-annotations
  (`modules.md` §3.1 basis-only refinement) — these are
  intentionally not new peer-level ledger lines; the convergence
  test would read this as "no D-track delta" even though the
  basis strengthening might be material.

**Production signal to watch.** Post-implement reviews where new
design decisions surface in implement OR verify that should have
been caught in investigate-design, **and** the convergence-test
cycle(s) for that run produced zero D-track deltas. That'd be
evidence the D-delta proxy is missing real materiality. If
observed: the convergence criterion needs broadening — possibly
to include basis-only sub-annotations on already-[VERIFIED]
decisions, or to add an F-track materiality classifier.

Absence-of-recurrence does not close this; only positive
load-bearing evidence per the lifecycle (or refutation evidence
that proxy misses) updates state.

---

## V-11. §4.1.2 per-step external evidence — independence from §4.1.4 convergence cycle

**Status: WATCHING.**

**Decision (`core.md` §4.1.2, §4.1.4).** V-5's false-[READY] failure
shape was closed in commit e18bca1 with two layered mitigations:
§4.1.2 requires per-implementer-step external evidence (file:line /
grep) in the [READY] artifact, and §4.1.4 requires a convergence
cycle producing zero D-track deltas. §4.1.4 fires after §4.1.2
produces PASSED.

**Why uncertain.** Both shipped in the same commit and have not been
separately validated. The unit-14 continuation (the first run under
the new protocol) showed §4.1.4 paying for itself — cycles 5–7
surfaced material findings (production performance bug, cycle-1
basis-rule violation in F31/F32, pattern catches) before convergence
at cycle 8. But every catch was an investigation-pass finding, not
an implementer-walkthrough artifact. §4.1.2 fires at [READY] *after*
§4.1.4 — by which point the investigation has already surfaced the
gaps.

The failure shape §4.1.2 specifically targets — *design decisions
that look complete but don't cash out to clear implementer steps*
(translation gap) — is distinct from §4.1.4's target shape
(incomplete investigation, missed surfaces). Plausible: a decision
whose surfaces are settled but whose per-step implementer
walkthrough exposes a gap not visible as a new investigation
surface. Not yet observed in the field.

In unit-14, §4.1.2 was delivered in *cheap variant* — paraphrased
prior tracker citations rather than re-read source — which is
recall-pool-equivalent and doesn't independently validate against
§4.1.4. The §4.1.2 sharpening (commit [pending]) closes the cheap
loophole by inheriting §3.2's basis form (citation + observable
fact for a read; executable query with output for a search — see
V-13 below for the verbatim-content drop) — cheap can no longer
satisfy structurally. Independence vs §4.1.4 becomes
testable with strict-by-construction data on next runs.

**Production signal to watch.** A run where §4.1.2's per-step
external-evidence artifact catches a citation failure (file:line
mismatch, decision-to-step translation gap) that §4.1.4's
convergence cycle did not catch. If observed: §4.1.2 is
independently load-bearing.

The contrary signal: one run where §4.1.4's convergence cycle
produces non-zero D-track deltas (catches) and §4.1.2 runs clean
on the resulting tracker. In that case, §4.1.2 is redundancy
candidate; the spec-change shape is designed at observation time
per practice 8.

**Closing criterion (WATCHING → RESOLVED).** A post-run review
identifies a run where §4.1.2 surfaced a translation-gap catch
§4.1.4's convergence cycle did not. One observed instance is
sufficient.

Alternative closure (WATCHING → INVALIDATED): one run where
§4.1.4's convergence cycle produced non-zero D-track deltas and
§4.1.2 ran clean on the resulting tracker.

---

## V-12. Basis-rule artifact form for file:line citations

**Status: FIX-SHIPPED (2026-05-26, commit [pending]).** §3.2 lead
sharpened to require the artifact form for any basis: a search
result with its executable query, OR a located read with the
verbatim content. Paraphrase, summary, or free-text claim of
having looked is explicitly not a basis. Converts §3.2 from
naked-judgment-shaped (the AI judges whether its cited basis is
sufficient) to artifact-bearing-shaped (the basis record includes
the un-fakeable content). Extends V-7's prior basis-rule sharpening
(`spec/core.md` §3.2.1 embedded-claims rule, commit c5e7ad9) along
a different axis — V-7 widened *which claims* carry the rule; V-12
sharpens *what counts as the artifact*.

**Closing criterion (FIX-SHIPPED → RESOLVED).** A post-run review
identifies a run where the artifact-form requirement was
load-bearing — caught a paraphrase-shape finding at finding-record
time that would have forced cascade convergence cycles to correct
under the pre-fix protocol. One observed instance is sufficient.

**Original observation preserved below for audit trail.**

---

The unit-14 run (beat-the-books continuation) had F31/F32 in cycle
1 citing paraphrased line ranges (`bets.py:359-425` was
approximated from recall rather than re-read). The wrong class was
implicit in the cited range; cycles 5 and 6 ran on the inaccurate
tracker; cycle 7 caught the discrepancy. The producing AI's
diagnosis: *"a tighter first cycle (actually read every cited
file:line, don't recall) would have cut probably 2 of the 8
cycles."*

§3.2 named the re-runnable basis requirement; compliance was
naked-judgment — the AI judged whether its cited basis satisfied
"located read of source" without producing the un-fakeable
artifact. The sharpening converts naked-judgment to artifact-
bearing: basis records include either the verbatim content at the
citation OR the executable search query and its output. Paraphrase
is no longer satisfiable as basis.

---

## V-13. Minimal verbatim content scope — sufficient or polluting?

**Status: FIX-SHIPPED (2026-05-27, commit [pending]).** Basis form
revised — verbatim content dropped entirely. Basis is now (a) a
re-runnable executable query OR (b) a file:line range citation
paired with one observable fact (count, identifier, type,
structural shape). Un-fakeability shifts to verifier-side: verify
(`core.md` §4.3) and convergence cycles (`core.md` §4.1.4) re-open
citations to check both location AND observable fact. The
"minimal" naked qualifier — flagged as Naked-judgment per
skill-craft `anti-patterns.md` — is gone; the operational form
(citation + one fact) replaces it. Trackers no longer contain
code-shaped content as basis.

**Production signal that triggered the fix.** Unit-11
dynamic-bet-sizing tracker (beat-the-books, 2026-05-26):
8.6% of tracker lines exceed 500 chars; basis records quote 5-15+
lines of Python/SQL per claim; tracker bulk dominated by code-
quote rather than analysis. Pollution flag tripped clearly.

**Closing criterion (FIX-SHIPPED → RESOLVED).** A post-run review
identifies a run where the new basis form was load-bearing —
either grounded a claim cleanly without producing code-quote
pollution, OR verify/convergence caught a fabricated citation
under the new form. One observed instance is sufficient.

**Original observation preserved below for audit trail.**

---

**Decision (`core.md` §3.2).** The basis form for a located read
was *"minimal verbatim content from the cited range that grounds
the claim"* — the load-bearing excerpt, not the entire range.
Adopted to avoid tracker pollution from full-range citations
(e.g., 59-line class bodies pasted as basis records).

**Why uncertain.** The "minimal" qualifier introduces bounded
judgment: the AI selects which lines from the cited range
ground the claim. The selection is artifact-checkable (does
the cited verbatim match source at the cited location, and
does it ground the stated claim?), but the selection moment
is naked-judgment. Three possible failure shapes:

- *Under-grounding*: AI cites too little; the excerpt doesn't
  actually contain enough text to verify the claim. Operator
  catch or downstream verify catch.
- *Pollution*: AI cites too much; basis bloats with surrounding
  context that doesn't ground the specific claim. Tracker
  becomes dominated by code bulk rather than analysis.
- *Right-sized*: AI cites the load-bearing excerpt at the
  intended scope. The target case.

**Production signal to watch.** Tracker review after runs:
- Pollution flag: any single point claim's basis exceeds ~5
  lines of verbatim, OR the tracker becomes dominated by
  code-quote bulk
- Under-grounding flag: any finding whose basis doesn't contain
  enough verbatim text to verify the stated claim

**Closing criterion (WATCHING → RESOLVED).** Three consecutive
runs produce tracker-clean, sufficiently-grounded basis records
with no under-grounding catches and no pollution flags. The
minimal-text qualifier is empirically sufficient.

**Alternative closure (WATCHING → SHARPENED).** A run shows
either consistent under-grounding (operator catches insufficient
basis repeatedly) or consistent pollution (tracker becomes
unwieldy with verbatim bulk). Sharpen §3.2 — either toward
fuller citation (accept pollution as the price of safety) or
toward a more mechanical scope criterion (e.g., "cite N lines
max around the load-bearing point").

---

## V-14. Emergent tracker-header fields — codify or leave instance-free?

**Status: WATCHING.**

**Decision (`modules.md` §3.1).** The 2026-05-26 light tracker
formalization requires `Status` and `Phase` as instance-defined
closed enums (plus run identifier, mode, task summary as the
core header fields). It does **not** formalize emergent fields
observed in practice — specifically `Protocol` (Clippy version
stamp, observed in Unit 16's tracker) and `Cycles complete`
(count + per-cycle summary, also Unit 16). The framework's
header schema currently names only the core required fields;
emergent fields are instance-free.

**Why uncertain.** These fields appeared organically in the
most recent run and look useful but are n=1 at this shape.
The formalization-vs-instance-freedom trade-off is unsettled:

- *Codify (broader header schema):* cross-instance consistency,
  audit-trail predictability, easier retroactive audits.
- *Leave instance-free:* preserves evolution; instances carry
  different metadata as their domains demand.

The codify-path risks freezing emergent shape from n=1; the
instance-free path risks drift that future retroactive audits
will struggle with.

**Production signal to watch.** Tracker review across future
runs:

- Whether `Protocol` and `Cycles complete` recur in subsequent
  Clippy runs
- Whether daneel or campaign-craft trackers develop their own
  emergent-field set (different from Clippy's)
- Whether new emergent fields appear that warrant inclusion
- Whether the absence of formalization causes AI confusion or
  drift about what to put in the header

**Closing criterion (WATCHING → RESOLVED via codify).** One run
where the emergent fields appear with content that semantically
matches the prior emergence (Protocol version stamp; Cycles
complete count) — codify at instance-level
(`references/tracker.md` extension) or framework-level
(`modules.md` §3.1 extension) per scope. One cross-instance
recurrence is equivalent positive evidence.

**Alternative closure (WATCHING → INVALIDATED).** One run shows
the emergent field set drifted (different fields, different
semantics) from the prior emergence — accept instance freedom as
design intent; document as observation, no codification.

---

## V-15. Standardized-pass lens noise on methodology-design tasks — collapse or accept?

**Status: WATCHING.**

**Decision (`core.md` §4.1.1 + `modules.md` §3.2).** Each cycle's
standardized inspection pass emits a line per lens whose scope
the cycle touched — a finding, cited-clean reason, or
out-of-scope reason. The lens set is accounted for whole once,
at [READY]. The current spec does not differentiate cycle
categories; every cycle's pass emits the per-lens enumeration.

**Why uncertain.** Unit 16 (a methodology-design task that
produced no code) generated 3 cycles × 12 lenses = 36 lens-lines,
of which ~24 were "cited-clean (re-attest)" or "out of scope
this cycle." For tasks that don't touch code (audit-only,
methodology-design, framework-design), most lenses are
perpetually out-of-scope or trivially clean; the protocol forces
rote per-lens lining anyway. Cost is small per-line but
cumulative across cycles.

Possible spec sharpening (deferred pending recurrence):

- *Form 1 — cycle-category enum*: classify cycles as
  `code-change | refactor-only | methodology-design | audit-only`,
  with per-category default lens-scope. Out-of-scope lenses
  batch-collapse to a single line per cycle.
- *Form 2 — batch out-of-scope*: keep per-lens lining but allow
  a "batch out-of-scope: [list] — cited reason: [reason]" line
  covering multiple lenses. AI still enumerates which, just
  doesn't write a per-lens line.

At n=1 (Unit 16) the categories are not stable; shipping Form 1
risks premature codification. Form 2 is incremental but adds
protocol surface without strong evidence the savings justify.
Defer; watch.

**Production signal to watch.** Future runs where ≥50% of
lens-lines collapse to "cited-clean re-attest" or "out-of-scope"
across 3+ cycles. If recurrent across 3+ runs with consistent
shape (same categorical pattern), Form 1 earns its place. If
the lens-noise pattern is one-off (only methodology-design
runs), Form 2 may be sufficient.

**Closing criterion (WATCHING → RESOLVED via sharpening).** One
run shows ≥50% cited-clean-re-attest or out-of-scope lens-lines
in a recognizable categorical pattern (code-change /
refactor-only / methodology-design / audit-only). Ship Form 1 or
Form 2 per the observed shape.

**Alternative closure (WATCHING → INVALIDATED).** One run shows
the lens-noise pattern was one-off (specific to its categorical
context) and does not generalize. Accept current per-lens lining
as design intent.

---

## V-16. Design-validity/coherence at [READY] — gap?

**Status: WATCHING.**

**Decision (no dedicated mechanism shipped).** The framework
does not ship a dedicated design-validity/coherence audit at
[READY]. Existing partial coverage:

- Per-decision basis rule (`core.md` §3.2) — each decision
  evidence-grounded
- Convergence cycle (`core.md` §4.1.4) — zero D-track deltas
  required for [READY]
- Standardized lens set (`modules.md` §2) — per-decision checks
- Fresh-session implementability test (`core.md` §4.1.2) —
  whole-design re-derivability indirectly tests coherence
- Verify's planned-vs-actual (`core.md` §4.3) — diff-vs-design
  + design-completeness audit (catches material ad-hoc decisions
  in impl-phase)
- Q4 ad-hoc additions in post-run review (debug-only) —
  historical catch of cross-decision detection gaps (Unit-4
  F18 → v0.8.2 §5.2 sharpening)

**Why uncertain.** Generic design-validity/coherence is
naked-judgment-shaped: no observable artifact-form forces
"these decisions hang together" or "this design actually solves
the request." Specific coherence shapes (e.g., pairwise
cross-decision detection per Unit-4) ARE structural-enforcement-
shaped and have been addressed per-incident. Open question: is
there a CLASS of coherence/validity failure beyond what
per-decision + fresh-session + verify + Q4 mechanisms catch?

**Production signal to watch.** Any [READY] design later found
internally incoherent (contradictions between decisions) or
invalid (the locked design wouldn't actually solve the
operator's request) — surfacing via verify [ISSUES FOUND],
implement-loopback, post-run review Q-set, or operator's
free-form override at presentation. The shape of the
incoherence is the analytical handle; per Unit-4 §5.2 evidence,
specific shapes get specific structural fixes, not a generic
coherence audit. **One observed shape** earns its specific
structural fix at n=1; a second distinct shape (different cause,
different fix) under the new spec would suggest a class-level
mechanism is warranted instead of per-shape sharpening.

Per `development-process.md` practice 8, this V-N is legitimate
(Y not classifiable upfront — fix form depends on the specific
shape that surfaces), not deferral-journal.

---

## V-17. HOLLOW artifacts at design — basis-rule + executable-verify residual

**Status: WATCHING.**

**Decision (no dedicated mechanism shipped).** The framework
does not ship a dedicated catcher for "design decision names an
artifact as a binding/wiring target, the artifact exists at the
named location, but the artifact is a stub or wired-but-data-
disconnected." Existing partial coverage:

- Basis rule's embedded-claim edge (`core.md` §3.2) — catches
  HOLLOW when the design decision makes any claim about the
  artifact's current behavior (the observable fact at the cited
  range — e.g., terminal statement, return type — exposes
  stub-shape)
- Basis rule's true-unit basis (`core.md` §3.2) — a claim about
  a construct's behavior requires a citation to the construct's
  visible close paired with an observable fact about it
- Executable-verification artifact (`core.md` §4.3) — a stub or
  wired-but-disconnected artifact fails the project's test/build
  suite when the implementation exercises the wiring chain

**Why uncertain.** The residual class: design decisions that
NAME an artifact as a binding/wiring/target without making any
embedded claim about its substance (e.g., "add toggle bound to
`userSettings.darkMode`" without claiming anything about
darkMode's current downstream wiring). Basis rule doesn't fire
on substance; executable-verify catches it at impl, but by then
a full cycle's design has locked targeting a hollow artifact —
a wasted cycle. Whether this class produces observable Clippy
incidents (vs. being caught upstream by basis rule's claim-about-
behavior edge, or downstream cheaply by executable-verify) is
empirical. The GSD framework's verifier (gsd-verifier.md) ships
this as a four-level artifact taxonomy (exists/substantive/wired/
data-flows); whether it earns its place in Clippy's lens set is
unverified at n=0.

**Production signal to watch.** Any Clippy [ISSUES FOUND] traceable
to a HOLLOW artifact whose design decision named it as a target
WITHOUT making behavioral claims about it — where executable-verify
caught at impl-time what a design-time lens would have caught at
[READY]. **n>=1** of this specific shape (basis rule didn't fire,
executable-verify did, full cycle's worth of design landed on a
hollow target) earns a structural fix. The fix form depends on
the shape: a Substantive-artifact lens, a basis-rule sub-edge
(target-naming carries an implicit substance claim), or a pre-
verify check are the candidates.

Per `development-process.md` practice 8, this V-N is legitimate
(Y not classifiable upfront — fix form depends on the specific
shape that surfaces), not deferral-journal. The proposing context
was a cross-framework comparison with GSD's verifier, not an
observed Clippy incident.

---

## V-18. 5-part design-decision body shape — trivial decisions over-structured?

**Status: WATCHING.**

**Decision (`core.md` §5.2, commit e12eec5).** Design decision
body specifies (a) target, (b) shape, (c) acceptance criteria,
(d) side effects/failure modes, (e) basis. Adopted to prevent
code-block pollution in design decisions (Unit-11 tracker showed
D2/D8/D11 with full Python/SQL bodies).

**Why uncertain.** The 5-part structure is sized for complex
decisions (Unit-11 D2 four-reducer signature; D5 calibration repo
contract; D8 validator spec). For trivial decisions — deferrals
("defer X to Unit Y because Z"), single-line acknowledgments,
version-pin assertions — the 5 named slots read heavy; risk of
checklist-driven slot-filling rather than thinking-driven
body-shaping.

Two mitigation paths considered but rejected:

- Trivial-decisions exception ("5 slots when non-trivial; basis
  alone for trivial") → introduces Naked-judgment qualifier
  ("trivial") — the anti-pattern this corpus has been sharpening
  against
- "Content not format" clarification → defensible but
  Additive-reflex default ("do nothing on ambiguous rule-need")
  and the rule's "specifies" wording is already loose

Cross-session reasoning (2026-05-27): "the 5-part shape is more
often a help than a hindrance, so the net is positive even with
the over-structuring tax."

**Production signal to watch.** Future tracker runs — do trivial
decisions naturally compress to one sentence (all 5 slots present
implicitly), or do they get boilerplate-filled (5 sequential
paragraphs even when content is trivial)?

- Compression flag: one run shows trivial decisions in
  one-sentence form with all 5 slots present implicitly → R2
  working as designed → RESOLVED.
- Boilerplate flag: one run shows trivial decisions with 5
  sequential mostly-empty paragraphs → R2 needs sharpening →
  candidate fix is the "content not format" clarification, OR a
  trivial-decision exception with mechanical criterion (not
  naked-judgment "trivial").

Per `development-process.md` practice 8, this V-N is legitimate
(Y not classifiable upfront — fix form depends on whether
boilerplate or compression dominates), not deferral-journal.
