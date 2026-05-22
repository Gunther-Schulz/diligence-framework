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
operator's judgement, and the other transitions are specified
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
