# Deriving a Anneal-based plugin

The Anneal framework is domain-agnostic. A working tool is an
*instance* of it — the framework bound to a domain. Clippy is the
instance for software engineering; a marketing-strategy tool would be
a sibling. This guide is how to derive a new instance.

This guide operates within the architectural foundation
(`foundation.md`): the three contracts (framework arbitrariness /
render completeness / instance domain-binding scope) hold across
every instance, and the slots below (§2-4) are the operative form
of contract 3's "instance domain-binding scope".

## The process — spec-first

**Start by copying** `anneal-framework/instance-template/` into
your new instance repo as the seed. The template scaffolds a
placeholder file for every slot the framework recognises —
required slots ready to fill, optional slots marked "delete if
not used." This makes the framework's closed slot set visible as
files at bootstrap time rather than as prose you have to
remember. Then proceed:

1. **Write the instance spec.** Bind the framework to the domain
   (§§1–4 below). The instance spec is small: it references the
   framework spec (`spec/`) for the method, and supplies only the
   domain bindings and the domain's standardized lens set.
2. **Generate the plugin** from the spec, per skill-craft.
3. **Verify and validate** the instance by the development process (§6).

Spec-first is not optional. Writing and settling the spec before
building the plugin surfaces gaps — mis-bindings, missing lenses,
unverifiable outcomes — that building-first bakes in. The instance
spec follows the framework spec's conventions: the fixed-decision
rule, the prescription discipline, the three-level test
(`spec/README.md`).

---

## 1. Domain-fit check

Before binding anything, confirm the domain fits the framework's
shape. The framework is for complex, open-ended work that proceeds
investigate-design → implement → verify to a *verifiable* outcome.
Check three things:

- **Open-ended.** The work needs investigation and design, not just
  execution of a known procedure. A fixed procedure is a workflow
  skill, not a Anneal instance.
- **Verifiable outcome.** "Done" can be checked against evidence, not
  asserted — verify needs something to run or check.
- **Recurring blind-spots.** The domain has a body of mistakes an
  expert learns to watch for. That body becomes the standardized lens
  set; without it the standardized inspection pass is empty.

Name where the domain strains. A domain with no executable
verification (verify can only inspect statically) still fits, but
verify is weaker — record that as a known strain. A domain where
"scope" has no mechanical search needs care at §3. A domain with none
of the three shapes is the wrong fit — the framework is not the tool.

## 2. What you inherit, what you supply

The framework's method is fixed. An instance that redefines it is a
fork, not an instance.

**Inherited, fixed** — do not redesign:

- the three phases (investigate-design, implement, verify) and their
  specs
- the two-pass cycle and inspection
- the basis rule and the evidence-bearing-artifact rule
- the tracker's form and the status-state machine
- [READY]
- the two modes (interactive, auto-battle)
- the orchestrator
- the two values (the Purpose) — the rubric every prescription is
  judged against

**You supply** — and only this:

- the domain **bindings** (§3)
- the domain's standardized **lens set** (§4)
- the **run-artifact persistence mechanism** — the framework fixes the
  forms of the run's persisted artifacts and requires them to persist:
  the tracker (an append-only ledger, persisted across interruptions —
  `spec/core.md` §6, `spec/modules.md` §3.1), each cycle's
  standardized-pass findings artifact (`spec/modules.md` §3.2), and
  each design decision's implementation decomposition
  (`spec/modules.md` §3.3); the instance supplies the concrete
  mechanism — where these artifacts live, how an in-progress run is
  found and resumed. Clippy's `bindings.md` is the worked example.

"Only this" bounds the *method* — an instance binds the framework to
a domain, it does not extend or revise the method. It does not bound
*presentation* — the instance's decorative layer: icons, a persona or
name, visual flourish. Presentation is only this orthogonal layer;
the *wording* of an instruction is not presentation but rendered
function, derived from the spec.

The framework prescribes no presentation: it mandates no look, and
instances may differ freely. An instance that wants to steer its look
records the intent in its own spec — an optional presentation section
in `bindings.md`, the render's instance-side input. The section is
optional and most instances leave it empty: the framework defines the
slot, it never dictates its content.

The framework also recognises **lifecycle extensions** — instance-
declared behaviors that fire at framework-defined points in the cycle
(e.g., on verify-PASSED, on instance-complete) and are bounded by a
framework-defined capability boundary. Lifecycle extensions do not
extend the method — they ride alongside it, as bookends layered on
framework-defined events. The set of points is closed (an instance
hooks existing points; it does not invent them) and every extension
ships disabled by default (the instance supplies the enable
mechanism the operator toggles). §5 specifies the points, the
boundary, the declaration shape, and the enable mechanism.

Together these are the instance spec's **slots** — its
render-consumed kinds of content, each with a framework-defined
meaning: the three required above (the lens-set slot optionally
extends with a supplement mechanism, §4 "Optional:
project-supplemental lenses"), and the two optional sections
(presentation and lifecycle extensions, §5). The set is **closed**.
An instance never adds a slot silently — an unrecognised section is
undefined input to the render. A genuinely new slot is proposed to
the framework and recognised in this guide, or it does not exist. An
instance's freedom is in how it fills the slots, and in free-form
rationale the render does not consume — not in inventing
render-consumed structure the framework does not know.

## 3. Binding the framework to the domain

The framework spec is written in domain-general terms. Bind each to
the domain by answering:

- **The work product** — what does implement produce? (Code; a
  campaign; a document.)
- **The problem space** — what does investigate-design investigate?
  (A codebase; a market; a corpus.)
- **Scope** — what is "the set of elements the work will modify," and
  what search establishes it? Scope is a completeness claim and needs
  a mechanical basis (`spec/core.md` §3.2) — name the domain's
  search. If the domain has no mechanical search for scope, that is a
  strain (§1).
- **Verification** — what is "the domain's executable verification"
  that verify runs and shows? (Tests, build, linters; a metrics
  check; a structured review.)

Record the bindings as a table. Clippy's `bindings.md` is the worked
example.

## 4. Deriving the standardized lens set

The hardest base. The lens set is the domain's recurring blind-spots
— the looking an expert does that a novice would not think to. It is
the instance's core content; the rest of the instance spec is thin
by comparison.

The difficulty: a new domain has **no incident history**. Clippy's
lens set distils years of accumulated coding mistakes. A fresh domain
has none — so the set cannot be mined from incidents the way Clippy's
was.

Bootstrap it as **Path 2** (skill-craft's term): blank-slate
hypotheses. State the domain's plausible blind-spots as hypothesized
lenses, grounded in domain expertise and intuition. Mark the set
Path 2 / validate-by-use. As real runs surface real incidents, each
incident confirms a lens or adds one — promoting the set toward
**Path 1**, incident-grounded.

Each lens fills the lens-entry shape — Name, Question, Scope
(`spec/modules.md` §2.1). Keep the set closed — a lens is in it or
not — so the standardized inspection pass can account for every lens,
every cycle. Completeness for the domain is the aim the Path 2
process above approaches, not a property declared up front.

Clippy's set is not a template, but it can be read for *shapes* that
recur across domains — does a change force a coupled change
elsewhere; are all downstream consumers enumerated; are failure paths
specified; are all value-classes covered. Use these as prompts; the
domain decides its own set.

### Optional: project-supplemental lenses

An instance may extend its lens-set slot with a **supplement
mechanism** — a way for projects using the instance to add their
own lenses (**lens supplements**) on top of the instance's closed
core set. Supplements are optional: an instance may declare the
mechanism; a project using that instance may or may not supply
lens supplements.

Supplemental lenses follow the same shape and discipline as core
lenses — Name, Question, Scope (per `spec/modules.md` §2.1) — and
are iterated by the standardized inspection pass the same way. The
runtime lens set is core ∪ supplement, closed at the project's
runtime: the standardized pass accounts for every lens whose scope
is touched, whichever subset it belongs to.

Constraints on the supplement mechanism:

1. **Same lens shape.** Every supplemental lens fills the
   Name/Question/Scope entry shape; loose-prose "lenses" are
   malformed.
2. **Closed at project level.** The project's supplemental set is
   enumerable from the supplement file or location; the
   standardized pass accounts for every supplemental lens whose
   scope is touched.
3. **Operator-supplied.** The operator writes the lenses; they
   are not invented at runtime.
4. **Additive-only.** Supplemental lenses do not disable, narrow,
   or override the instance's core lenses. If a core lens
   consistently mismatches a project's needs, the fix is at the
   instance-spec level (sharpen the core lens), not at the project
   level (silence it).
5. **Skill-craft form discipline.** Supplemental lenses are
   reviewed against the same form-quality rules as core lenses
   — the full canonical sweep per skill-craft's `PROCEDURE.md`
   + `references/anti-patterns.md`.

The instance spec declares the mechanism — where the supplement
file lives, how the orchestrator loads it at standardized-pass
dispatch. The supplement file is an operator-editable artifact
subject to the filesystem layout rule in §5 (operator-editable
distinct from runtime state, instance-unique namespace).

## 5. Lifecycle extensions (optional)

An instance may declare behaviors that fire at framework-defined
points in the cycle — for example, opening a pull request when verify
reaches [PASSED], or refusing to start a run on a dirty tree. These
are **lifecycle extensions**: bookends layered on the framework's
cycle, not modifications to it.

The framework defines a **closed set** of lifecycle extension points.
Each point has framework-defined firing semantics, exposed read-only
context, and permitted effect scope. An instance hooks one or more
points by declaring extensions in its spec — as an `## Extensions`
section in `bindings.md`, or as a separate `spec/extensions.md` when
the section grows. The set is closed: an instance never hooks an
unrecognised point and never invents one. A genuinely new point is
proposed to the framework and recognised here, or it does not exist.

### Extension points

| Point | Fires when | Exposes (read-only) | Permitted effects |
|---|---|---|---|
| `on-instance-start` | Run begins, pre-investigate | Task summary, mode | External side effects; **may return a precondition-failure** (a halt signal with a stated reason) **that blocks the run** (only point allowed to gate) |
| `on-cycle-end` | A cycle's two tracks settle and its standardized pass is clean | The cycle's F/D entries with statuses, the cycle's standardized-pass artifact | External side effects; writes to non-spec paths |
| `on-verify-PASSED` | Verify reaches [PASSED] | Full tracker snapshot, work-product paths, basis citations | External side effects; writes to non-spec paths |
| `on-instance-complete` | Run reaches its closed state | Full tracker, all artifacts | External side effects; archival; writes to non-spec paths |

### Capability boundary

A lifecycle extension cannot:

1. **Modify tracker state.** No status changes; no F/D additions.
   The tracker is the spine — extensions cannot bypass it.
2. **Influence phase gates mid-flow.** Only `on-instance-start` may
   gate. The framework's phase mechanics ([READY], verify-PASSED)
   are framework-determined; extensions are bookends, not gates.
3. **Read context outside its point's exposed snapshot.** An
   extension at `on-cycle-end` does not peek at other cycles or
   at run-internal mechanics not in the exposed context.
4. **Write to framework spec, instance spec, or rendered skill
   files.** Extensions cannot smuggle in content with no spec
   origin (`foundation.md` contract 2).
5. **Fire other extension points, or recurse into the cycle.**
   Linear orchestration only; no reentrancy.
6. **Run during a phase.** Only at the named extension points —
   between-phases or at-event.
7. **Block subsequent extensions** at the same point, unless
   framework-marked blocking. Failure of one is logged and
   continues.

**Binding-refinement vs lifecycle extension.** Some domain concerns
look like extensions but are not. The test is slot-membership:

- A behavior that refines a domain-general term in §3's bindings
  table (verification, scope, work product, etc.) is a **binding
  refinement** — extend that row in §3, not §5. Examples: adding
  a new check tool to verification; adding a new search class to
  scope.
- A behavior that fires at one of the extension points named in
  the table above is a **lifecycle extension** — declare it in
  the instance spec's `## Extensions` section.
- A behavior that fits neither requires a framework-spec change
  (a new extension point, or a new binding category) per the
  closed-slot rule above.

### Disabled by default

Every declared extension ships in the rendered plugin but is
**disabled** until the operator enables it. The framework does not
prescribe the enable mechanism — the instance supplies it (parallel
to how the instance supplies the run-artifact persistence mechanism,
§2). The AI reads the enable state before firing any extension;
missing or ambiguous state is read as disabled (fail-safe).

The instance-supplied enable mechanism, declared in the same section
as the extension declarations, must be:

- **Operator-controllable** — togglable without spec or code edits.
- **Version-controllable** — the operator can choose whether the
  enable state travels with the project (committed) or is per-clone
  (gitignored).
- **Fail-safe** — missing, malformed, or ambiguous state reads as
  disabled. The AI never fires an extension whose enable state is
  unreadable.

A worked example for software-engineering instances: a file at
`<instance-config-dir>/extensions.enabled` listing enabled extension
names, one per line — the operator edits the file to toggle. Other
instances may use config lines, environment variables, or per-run
tracker-header entries; the framework is mechanism-agnostic.

### Filesystem layout for operator-editable artifacts

When an instance places operator-editable artifacts on disk — the
enable mechanism above; the lens-supplement file in §4; any future
operator-editable instance-side artifact — three framework rules
apply:

1. **Distinct location from runtime state.** Operator-editable
   artifacts and runtime-state artifacts (the run-artifacts an
   instance writes per §2's persistence mechanism) live at
   observably distinct filesystem paths — observable under git
   as: operator-editable paths are tracked (`git ls-files`);
   runtime-state paths are gitignored (`git check-ignore`).
   Mixing them blurs the commit boundary and the edit-permission
   contract: operators forget which files they own, instances
   overwrite operator-edited files, and gitignore rules fragment.
2. **Namespace uniqueness.** Each instance's filesystem footprint
   uses a namespace unique to that instance, preventing collisions
   when multiple anneal-derived instances coexist in one project.
3. **Convention** (recommended, not mandated):
   `<plugin-skill-name>.config/` (committed, operator-editable) +
   `.<plugin-skill-name>/runs/` (gitignored, instance-managed). The
   visible-vs-hidden filesystem distinction maps to
   commit-vs-gitignore; the namespace inherits uniqueness from the
   plugin manifest's skill-name uniqueness.

**Project init.** When an instance runs in a project for the
first time, it bootstraps placeholder files for **every
operator-editable slot kind the framework recognises**
(enumerated at the top of this subsection), regardless of
whether the instance has declared specific items in those slots.
The placeholder is what makes the capability visible: an
operator landing in a fresh project sees the slot kinds
available without needing to read spec-prose to discover them. Placeholders are committed (tracked under git);
the runtime-state directory is added to `.gitignore` by the
instance on the same first-run.

**Placeholder content style.** Each placeholder carries: a
header comment naming the slot kind and pointing at its spec
section; empty sections matching the slot's declaration shape;
optionally a commented-out small example showing what filling-in
looks like. The file documents
the capability — its presence is the un-fakeable signal that
the slot is available in this instance; its content shows the
operator what content goes here. An instance that later adds a
declared item (a specific extension; a specific supplemental
lens) replaces the placeholder content rather than creating a
new file. (Distinct from the developer-time template-copy at
the top of "The process — spec-first", which scaffolds the
instance repo itself.)

### Declaration shape

An extension declaration carries: the point it hooks, the action it
performs, the side-effect target, and its failure handling. Multiple
extensions at the same point run in declared order.

```
## Extensions

Enable mechanism: <instance-supplied — names the artifact's location
and format and how absence is interpreted>

### on-verify-PASSED · auto-create-pr
Action: invoke `gh pr create --title <T> --body <B>`
  T derived from: the cycle's task summary
  B derived from: tracker reduced to verified F/D entries
Side-effect target: GitHub remote
Failure handling: log + continue
```

The declaration is the audit surface: a capability-violating action
string is observable in the instance spec at review time, not
deferred to runtime. The catch is the spec-origin audit
(`foundation.md` contract 2 + `development-process.md` practice 4).

## 6. Generate the instance

With the spec settled — bindings, lens set, run-artifact persistence,
optionally presentation and lifecycle extensions — the domain-specific
work is done. From here the instance is built and
evolved by the **development process** (`development-process.md`) —
render, verify in a separate context, validate, and change. The first
build is that process run once over the whole instance; every later
change runs it over the affected parts. This guide does not restate
it.

Render the plugin files from the instance spec and the framework spec
— faithfully, per skill-craft's rendering-fidelity rule (`Rendering
from a source`). The same rule governs every later re-render.

The instance also needs its `CLAUDE.md`. It auto-loads for any
session working on the instance repo, so it must carry the rule that
the skill content is rendered, not authored — or a session will
hand-edit a skill file unaware, and the instance drifts from the
spec. Seed the `CLAUDE.md` with this section, binding `<Instance>` to
the instance's name and `<skill-dir>` to its skill directory:

```
## The skill content is rendered, not authored

<Instance> is an *instance* of the Anneal framework. The skill
files — `<skill-dir>/SKILL.md`, `phases/`, and `references/` — are
**rendered** from the framework spec (the `anneal-framework`
repo, `spec/`) and from this instance's `spec/` folder. They are
not authored here, and are never where a behavior change
originates.

A change to how <Instance> behaves goes to the framework spec or
the instance spec first: committed there, then re-rendered into
these files and verified in a separate context — the procedure is
`development-process.md` in the `anneal-framework` repo. Hand-
editing a skill file as if it were source breaks re-derivability:
the spec and the instance drift, and the change cannot be
reproduced for another instance.

This rule covers the skill *content*. The plugin's packaging — this
file, the READMEs, `plugin.json`, and the like — is repo-local,
maintained in the instance repo directly.
```

Extend the `CLAUDE.md` below this section with the instance's own
plugin-housekeeping — description sync, version discipline, component
inventory — and any instance-specific rules.

Then verify and validate the instance by the development process —
the render checked in a separate context, the first empirical run
triaged as `development-process.md` describes. From there the
instance is evolved like any other.

---

*Status: written from the Clippy spec effort and its first plugin
rewrite — which exercised the spec→plugin path and exposed the
rendering-fidelity gap now closed by skill-craft's
rendering-fidelity rule.*
