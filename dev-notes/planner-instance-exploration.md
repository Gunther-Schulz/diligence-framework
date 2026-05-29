# Planner-instance exploration — design notes

**Status:** design locked, pre-build (gray-zone fork **(a)** operator-confirmed
2026-05-29). Planner spec not yet written — by design, pass-1 isolated subagent
writes it. Not yet a rule-corpus edit cycle for the planner.
**Working name:** "planner" (provisional — undersells it; see Naming).
**Captured:** 2026-05-29, from an exploratory session. Records decisions
and framework findings so they survive context loss; not itself spec.

---

## Resume point (last session 2026-05-29)

**Where we are:** design phase done; gray-zone fork **(a) locked**. No planner
spec content written yet — correct: pass-1 is an isolated subagent's job, not
the main agent's (writing it here would contaminate the first-ever forward
derivation test). `development-process.md` read in full 2026-05-29 (per-cycle).

**Next action — start here:**
1. Read `instantiation-guide.md` in full (the derive-a-new-instance procedure;
   not yet read this effort — required before pass-1).
2. Run the locked boundary through `decision-design-sharpening` (pre-commit).
3. Build the pass-1 brief — **domain identity IN; every conclusion in this doc
   OUT** (they are the hypotheses the derivation tests) — and dispatch an
   **isolated subagent** for the diagnostic derivation; collect its gap report.
4. Gap report → interface fix (release loop) → clean re-derive.

**Side-quest CLOSED (not a planner dependency):** clippy lens-set
language-neutralization shipped — **clippy v0.9.89** (commits `56d8983` +
`566a663`, pushed; installed pin bumped 0.9.88→0.9.89). Operator `/reload-plugins`
was the only pending handoff. Parked follow-ups, each its own cycle: (1) broader
clippy lens-set coherence-audit (uneven granularity, boundary-lens overlap, the
2 left observations); (2) candidate framework principle — "a lens set sits at
its instance's declared scope; sub-domain specifics → supplement."

## What this is

A prospective new Anneal instance, **upstream of clippy**, whose domain is
authoring a **feature spec that clippy can run against**. Trigger: in the
`beat-the-books` project, clippy correctly **halted** on Unit 9 (the
strategy-board UI) because the architecture doc (`MULTI_STRATEGY_ARCHITECTURE.md`,
ad-hoc, uncodified) *defers* the board design (§6/§8 "out of scope / separate
effort") while the execution order routes to it — so clippy had no defined
targets to ground scope against. That seam — defining *what a feature is*,
before clippy designs *how to build it* — is the proposed instance's domain.

Recurrence confirmed by operator: the board recurs, and the pattern (fuzzy
goal → clippy-runnable spec) recurs across features and future projects.

## Decisions

- **Build a new instance** (not hand-author one doc; not extend clippy).
  Additive check passes: the anneal discipline catches what a PRD template
  can't — proven by the Unit 9 doc shipping a self-contradiction
  (exec-order says do Unit 9; §6/§8 say it's out of scope). Coverage +
  coherence verification doesn't let that out the door.

- **Domain boundary — the WHAT/HOW line:**
  - Planner owns: **WHAT** the feature does, **WHY**, what it **depends on**
    (conceptually), its **UX shape**, its **scope boundary**.
  - Clippy owns: **HOW** (impl design, integration against real interfaces,
    build, executable verify).
  - Handoff = clippy's entry condition: *can clippy reach `[VERIFIED]` scope
    and start impl-design from this spec?* If yes, planner did enough; if it
    specified impl, it overstepped. (One criterion doing triple duty:
    verification bar, handoff definition, boundary test.)

- **OUT of the planner domain:**
  - **Impl details** — what makes it a distinct instance vs. clippy-in-a-hat.
  - **Interface-grounding** ("cite the real `replay.py:42` interface") — that's
    clippy's, AND it would break greenfield (no interfaces to cite when nothing
    is built). Replaced by **dependency completeness**: every capability the
    feature leans on is named with provenance (in-scope / other-unit / existing
    / external) — codebase reads are an *optional* basis, never required.

- **Verification semantics:** coverage + coherence + dependency-completeness,
  re-run by an isolated context (§4.3 isolation still applies). NOT code
  execution. Foundation #3 expects each instance to define "executable
  verification" in its domain; planner defines it here.

- **Run feel:** `[CONDITIONAL]`-heavy. Most product positions rest on operator
  intent, not searchable evidence — the operator *is* the source of product
  truth. Framework already carries this: `[CONDITIONAL]` → operator confirms
  (`[VERIFIED]`) or `[AUTO-ACCEPTED]` at `[READY]` (§5.2). Different feel from
  clippy, same machinery.

- **Gray-zone fork (architecture decisions) — LOCKED (a), operator-confirmed
  2026-05-29:** planner owns
  **scope-determining** architecture, defers **impl-internal** to clippy. Falls
  out of the handoff criterion, not gut:
  - "Standalone SPA vs embedded in existing app" → changes *which files/symbols*
    clippy's scope covers; clippy can't reach `[VERIFIED]` scope without it →
    **planner** (leaving it to clippy = Unit 9 in miniature).
  - "Redux vs context / framework / data-layer shape" → doesn't change the
    scope-set; clippy resolves in impl-design → **clippy**.
  - **Residual still open:** decisions that are *both* scope-determining AND
    technically-contingent ("reuse existing auth service vs stand up a new
    one") force a planner↔clippy round-trip. Where exactly the cut lands here is
    to be resolved by the derivation + `decision-design-sharpening`, not guessed.

- **Naming:** "planner" misleads (sounds like task scheduling). It authors a
  *feature spec*. Name after the domain locks — name follows domain, not vice
  versa.

## Parked (explicitly, not dropped)

- **Orchestration** — whether the instance also *executes* (drives clippy), or
  clippy *pulls* the planner's doc, or a 3rd orchestrator coordinates. A
  *composition* boundary, downstream of the domain lock. Revisit after domain
  is fixed.

## Framework findings surfaced by this exploration

These are about the framework/triad, independent of whether the planner ships.

1. **Greenfield tolerance is already in the framework; the brownfield bias is
   one clippy binding.**
   - Framework is greenfield-tolerant *as written*: the basis rule (§3.2)
     treats absent evidence as a first-class **assumption** (not error); scope
     search (§4.1) legitimately returns empty sets (§5.1 admits an empty search
     result as a valid basis). Neither breaks in an empty repo — they return
     less and lean on `[CONDITIONAL]`/`[AUTO-ACCEPTED]` early; self-heals as the
     project grows.
   - The brownfield assumption is concentrated in **clippy's `verify.md:50`**
     binding ("run the project's test suite, build, and linters"). Making clippy
     explicitly greenfield-capable is therefore **instance-level**, not
     framework-level — and the framework *must not* change for it (a greenfield
     *mode* at framework level would leak a corpus-state distinction into the
     domain-agnostic methodology — foundation #1 violation).
   - **CAVEAT:** only `verify.md:50` confirmed by read. A clean clippy
     greenfield-hardening needs a sweep of its other bindings
     (`lenses.md`, `investigate-design.md`) for the same assumption. Not done.
   - Note: the planner does **not** fix clippy's greenfield grounding — clippy
     grounds against *code*, and an empty repo has none regardless of spec
     quality. Planner reduces clippy's *design-assumption* load, not its
     *codebase-grounding* gap. Orthogonal.

2. **The planner would be the first forward derivation, ever.**
   - clippy is the *origin* (anneal was extracted from it); daneel
     *co-evolved*. So the instantiation path (framework spec + guide + template
     → instance) has **never been walked forward**. Zero prior validation.
   - Therefore the build **is** the render-completeness / instantiation-guide
     validation experiment. The guide's gaps are an *expected output*, not a
     risk. Conditions for it to be a valid test:
     1. **Brief discipline** — give the subagent ONLY published specs + guide +
        template; withhold every conclusion in these notes, and see if the guide
        leads it there itself. Handing it our answers masks the gaps.
     2. **Gap-reporting, not gap-smoothing** — require the subagent to flag every
        instance-binding decision the guide did *not* determine ("I invented X;
        the guide is silent"). Those flags are the findings; they feed
        development-process triage (render / spec / adherence gap).
   - **Arbitrariness caveat:** the planner's domain (producing a structured
     design artifact) is *close to anneal's own nature*, so it's an unambiguous
     test of the **forward path** but a **soft** test of foundation #1
     (arbitrariness). Don't read a clean derivation as proof the guide is truly
     domain-agnostic — a domain unlike "author a structured artifact" (physical,
     real-time, adversarial) would stress that harder.

3. **The existing instance specs are muddied — fingerprints of co-evolution.**
   - clippy's `spec/` = **3 files** (bindings, lens-set, README) vs. the
     template's **7** (bindings, extensions, lens-set, lens-supplement,
     persistence, presentation, README).
   - `bindings.md` = **slot-collapse**: the template says it's *just the
     term→value table* ("rationale belongs in commentary, not in the table"),
     but clippy's absorbed persistence + operator-editable + extensions +
     dispatch-models + a full git-worktree isolation mechanism (197 lines; a
     declarative table next to literal git command strings).
   - `lens-set.md` = **accretion** (milder): all lenses, but uneven granularity
     (Quality-category is 6-in-1; others standalone) and **language over-fit**.
     Grep (2026-05-29) confirms: **`pytest` is NOT encoded** — the
     executable-verification binding is correctly agnostic (`bindings.md:33`,
     `verify.md:50` = "test suite, build, linters"). But three CORE lenses carry
     Python/mypy/Pydantic specifics — `Consumer-enumeration` (`mock.patch`,
     `monkeypatch`, `importlib`), `Silent-substitution-at-boundary` ("→ Python",
     `dict.get`), `Defensive-paranoia-vs-type-guarantee` (`hasattr`/`isinstance`,
     Pydantic, mypy) — at `spec/lens-set.md:131-132,176,184` (+ mirrored render
     `plugin/skills/clippy/references/lenses.md`). This is a **known** over-fit:
     an archived cross-review (`docs/archived/dev/FINAL_CROSS_REVIEW.md`) already
     dispositioned Python-specificity as minor/illustrative/low-priority-keep;
     operator now reopens it ("clippy must be language-agnostic").
   - **Fix-shape (separate clippy cycle, NOT the planner):** restate the three
     core lenses **language-neutrally** + push Python specifics into the
     **existing supplement mechanism** (`clippy.config/lenses.md`, additive-only)
     — Pareto: core more agnostic (matches clippy's stated all-software scope),
     coverage preserved. Candidate framework-level principle lurking (a lens set
     sits at its instance's declared scope; sub-domain specifics → supplement) —
     triage at fix time. Nit: `venv` as bootstrap example (`bindings.md:193`,
     `implement.md:118`) is illustrative/out-of-scope, minor.
   - **Implication:** derive the planner **clean from the template**, never by
     copying clippy → planner becomes the **first clean reference instance**.
   - **Triage fork (open):** is the template *over-split* (clippy's 3-file
     consolidation is the ergonomic right call → fix template) or did clippy
     *drift* (7 clean slots right → re-split clippy)? Lean drift (a pure table
     and git mechanics genuinely don't belong together), but the derivation
     answers it: if the subagent produces 7 files and 3 feel like ceremony,
     that's evidence for over-split.

4. **Instance specs should couple to the framework's *contract*, not its
   *implementation*.**
   - Necessary: reference framework **terms** (what's being bound) — this is
     also foundation #2 traceability.
   - Brittle/removable: reference framework **section numbers** (`core.md
     §3.2`, `§4.1.4`) and re-explain internal mechanisms. clippy does this
     heavily (its co-evolution fingerprint again).
   - **Clean rule:** instance specs cite framework **glossary terms** (locked,
     stable vocabulary), never section numbers. The **glossary is the
     instance-facing interface** — it owns the mapping to internal sections, so
     instances decouple from layout churn *and* keep traceability (the term is
     the trace). Resolves decoupling vs. foundation #2 without choosing.
   - **The template itself leaks:** `instance-template/spec/persistence.md`
     cites `core.md §6`, `modules.md §3.1/§3.2/§3.3` in the *slot description*.
     So "write the instance spec in isolation" is **not achievable with the
     current template** — a template/guide defect, not just clippy's.
   - **Second derivation-measurable:** can an isolated subagent write the
     instance *spec* from glossary + guide + template alone? Each forced dive
     into `core.md` = an interface leak to fix.
   - **CAVEAT:** the glossary isn't a *complete* instance-facing contract today
     (the bindings table binds terms — e.g. "executable verification" — that
     aren't necessarily full glossary entries). Making it complete is real work;
     scoping it is part of what the derivation exposes.

## Sequencing — does anneal need fixing first?

The findings sort into three layers, and only one is an anneal-level issue:

- **The method** (core spec): exercised and sound via clippy; not in question.
  Greenfield analysis *confirmed* it.
- **Clippy-instance issues** (`verify.md:50` brownfield binding; spec
  muddiness): instance-level, clippy's own schedule, **not blockers**.
- **The instantiation apparatus** (template + guide + glossary-as-interface):
  the real soft spot (Finding 4) — under-developed *because never exercised
  forward*. The one genuine anneal-level issue.

**Decision: do NOT fix the interface first.** Fixing it before a derivation
exercises it is guessing-without-evidence — the act-on-confidence failure anneal
exists to prevent; there's no completion criterion for the interface without an
instance binding against it. The derivation is the **instrument that scopes the
fix**. Order:

1. **Derive the planner as a diagnostic run** (isolated subagent, instrumented
   for gap-reporting per Finding 2). Primary deliverable = the leak report;
   expect a somewhat-leaky planner.
2. **Gap report → scopes the interface fix** (template/glossary), done through
   the proper rule-corpus cycle.
3. **Re-derive clean** against the fixed interface → reference-quality planner.

Two passes, cheap (diagnostic is a subagent run, not a hand-build). NOT a
halt-and-rework-anneal — scope-creeping into a full framework audit before the
gap report is the same confidence-not-evidence mistake in the other direction.

## Who writes the specs (per pass)

Settled by isolation, not by writing skill. **The writer-choice is the
output-choice:** a naive subagent yields planner **+ gap report**; the main
agent (contaminated by this session) yields planner **only**, silently filling
every interface gap from our conclusions — which also **reproduces clippy's
original sin** (knowledgeable insider bakes in undocumented assumptions).
Anneal's own §4.3 verify-isolation prescribes it: deriving the instance spec
*is* a verify of the instantiation apparatus, so the actor who designed all
session cannot write it.

- **Pass 1 (diagnostic derivation):** isolated **subagent**. Main agent is
  disqualified from writing — role is **brief + audit the gap report**.
  - **Brief is the control surface.** IN: domain *identity* ("instance that
    authors feature-specs upstream of a code-builder") + published spec + guide
    + template. OUT: every worked-out conclusion in this doc (boundary,
    verification semantics, gray-zone, greenfield reasoning) — those are the
    hypotheses under test. Leaking them into the brief kills the test.
- **Pass 2 (interface fix):** **main agent + operator**, in the rule-corpus
  process — contamination is an asset here; human in the loop.
- **Pass 3 (clean re-derivation):** **subagent** again — re-deriving against the
  fixed interface is what proves the fix.

Optional: a small **panel** of independent derivations sharpens the signal
(leaks all hit = robust gaps vs. one subagent's quirk). Later call.

## Before building (process gate)

Building trips the rule-corpus cycle: read `development-process.md` **in full**,
invoke **skill-craft** before edits, work from **`instantiation-guide.md`**. The
boundary should also pass through **`decision-design-sharpening`** before it
touches an instance spec. This is an **instance derivation, not a framework-spec
change** — contained scope (instance bindings + a new lens set + the render);
the framework spec stays untouched (findings 1, 4 above notwithstanding — those
are *separate* potential framework/template improvements, triaged on their own).
