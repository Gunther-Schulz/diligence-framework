# Diligence Framework — Validation Watch

Companion to the Diligence-framework spec; not part of it. The spec
states fixed decisions. Some were made best-effort, under genuine
uncertainty. This doc records those — the decision, why it was
uncertain, and the production signal that would prompt revisiting it.
The spec stays pure prescription; the uncertainty is tracked here.

Production signals come from any instance's real runs — Clippy's, or
a future sibling's.

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

**Status: FIX-SHIPPED (2026-05-25, commit pending).** The recurrence
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
