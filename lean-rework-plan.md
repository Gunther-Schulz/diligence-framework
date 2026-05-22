# Lean rework — the plan

Status: planned, not implemented. Direction agreed 2026-05-22; the
detailed design and the spec surgery are a fresh, focused pass
working from this note + the current `spec/`.

## Why — the diagnosis

The framework's mechanisms split in two. One kind keeps the AI's
judgment **in motion** — lenses (questions that make it look), the
cycle loop (look again), forcing functions (compel a step or a
stop). These are external scaffolding; they channel judgment and
do not depend on the AI's verdict being right. They work.

The other kind **caches** judgment into a verdict the run reads
instead of re-judging — a `[VERIFIED]` tag, the `[READY]` gate that
fires on the tags, and (added in 0.7.0) the implementation
decomposition and the isolated `[READY]` evaluation. A cached
judgment goes stale as the loop keeps moving the design; the run
trusts the stale verdict anyway. F21 — a cross-decision
contradiction that passed three isolated `[READY]` evaluations as
`[READY CONFIRMED]` — is a stale verdict. The 0.7.0 additions were
verdict-machinery; a real run (the multi-strategy Unit-3 run) tested
them and they overshot: heavy cost, and they still missed F21.

The treadmill to stop: "a failure surfaces -> add another
mechanism." Completeness cannot be reached by mechanism; every
mechanism has a blind spot.

## The change

Stop producing verdicts the run trusts. Keep what channels
judgment; cut what replaces it.

1. **The `[READY]` gate stops certifying itself.** Today a tag-check
   the run passes on its own. It becomes a forcing function — a hard
   stop that surfaces the whole design for the operator's judgment.
2. **"Complete enough to implement?" stops being a verdict.** Drop
   the mandatory decomposition artifact and the isolated
   `[READY]`-evaluation subagent. Completeness becomes a recurring
   cycle-level question — see open question 1.
3. **The tracker becomes a notebook** — a record that supports the
   judge, not a state machine whose tags a gate fires on.
4. **Cut:** the isolated `[READY]` evaluation; the mandatory
   implementation-decomposition artifact (`core.md` §5.2,
   `modules.md` §3.3).
5. **Keep:** lenses, the cycle loop, forcing functions, the
   implement loopback, evidence-grounded verify. Keep §3.1's
   evidence-bearing reframe — a status tag is a weak artifact,
   nothing is un-fakeable — it is the diagnosis's own basis.

## Open design questions — resolve in the fresh pass

1. **Completeness as a question.** The standardized lens set is
   instance-supplied; completeness is framework-universal — so it is
   not a domain lens. Is it a framework-mandated cycle check, a
   property of the loop, or something else? Work it out.
2. **The `[READY]` forcing function.** What exactly does it surface,
   in what form? Does the closed artifact become the surfacing?
3. **The status-state machine.** With tags no longer gated-on, what
   survives? Does `[VERIFIED]` remain as a record-only tag? Does the
   demote transition (added 0.7.0) stay or go?
4. **`core.md` / `modules.md` restructure** — §4.1, §5, §6,
   `modules.md` §3: the exact edits and how the sections re-cohere.
5. **Re-render scope** — `foundations.md`, `tracker.md`,
   `investigate-design.md`, `SKILL.md`.

## Expectations

- Leaner and faster — fewer mechanisms, far less bookkeeping, fewer
  subagent runs.
- The operator stays the judge at `[READY]`.
- Trade-off: some design defects reach implement rather than being
  stopped at the gate; the implement-loopback and verify catch them
  there — later, but more cheaply than an ever-growing gate.
- NOT promised: completeness. A miss is not answered by adding a
  mechanism — that reflex is what overshot.
- Auto-battle: unchanged as a trade-off; post-change its `[READY]`
  judgment is skipped, so its design defects surface at
  implement/verify.

## The 0.7.0 driver is still a target

0.7.0 was driven by a real problem — the AI over-marks a design
decision "done" when it is not. That problem is not dropped; it is
re-homed from verdict-machinery to the cycle-level completeness
question (open question 1). The other 0.7.0 gaps (pass-artifact
persistence, basis-content validation, the un-verify path) were
largely artifacts of the verdict-gate — cutting the gate dissolves
them. Honest limit: a cycle-level question is answered by the AI and
can be under-answered; it makes over-marking more likely caught, not
guaranteed — the backstop is the `[READY]` surfacing, the
implement-loopback, and verify.
