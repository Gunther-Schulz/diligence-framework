# Diligence Framework — Validation Watch

Companion to the Diligence-framework spec; not part of it. The spec
states fixed decisions. Some were made best-effort, under genuine
uncertainty. This doc records those — the decision, why it was
uncertain, and the production signal that would prompt revisiting it.
The spec stays pure prescription; the uncertainty is tracked here.

Production signals come from any instance's real runs — Clippy's, or
a future sibling's.

---

## V-1. Standardized lens timing — per-cycle incremental

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

**Status: RESOLVED (2026-05-24, commit c5e7ad9).**

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

**Decision (`core.md` §4.3, §6; `modules.md` §1.2).** Verify [ISSUES
FOUND] returns the run to investigate-design — the single locus for
fix resolution. The fix runs through the full procedure
(investigate-design → implement → verify); no in-place shortcut at
verify-terminal in either mode. In auto-battle, loopback is
automatic, with a convergence exception: a verify finding that
re-surfaces an existing [AUTO-ACCEPTED] design decision in the
tracker does not trigger loopback; the run completes with the
finding noted as a re-surfacing alongside the original
[AUTO-ACCEPTED] tag, for the operator's post-run review.

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
investigate-design. It rests on the assumption that "this verify
finding re-surfaces an existing [AUTO-ACCEPTED] decision" is a
determinable identity — the AI in the isolated verify context must
recognize the match against the tracker without false positives.

**Production signal to watch.** (a) Whether always-loopback in
interactive feels right vs heavy for trivial verify findings; whether
operators routinely use free-form override to scope-out a finding
rather than re-investigate. (b) Whether the [AUTO-ACCEPTED]-re-
surfacing exception correctly skips prior judgments without letting
through *new* gaps that should have re-triggered investigate-design
(false-match risk). (c) Whether auto-battle converges under the rule
in practice — no observed infinite verify-loopback loops. (d)
Whether the close-with-re-surfacing-notation creates useful post-run
review material or noise.
