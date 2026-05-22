# Deriving a Diligence-based plugin

The Diligence framework is domain-agnostic. A working tool is an
*instance* of it — the framework bound to a domain. Clippy is the
instance for software engineering; a marketing-strategy tool would be
a sibling. This guide is how to derive a new instance.

## The process — spec-first

1. **Write the instance spec.** Bind the framework to the domain
   (§§1–4 below). The instance spec is small: it references the
   framework spec (`spec/`) for the method, and supplies only the
   domain bindings and the domain's standardized lens set.
2. **Generate the plugin** from the spec, per skill-craft.
3. **Validate** — the generative and empirical tests (§5).

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
  skill, not a Diligence instance.
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
- the two-pass cycle, and inspection / gate — the two functions
- the basis rule and the un-fakeable-artifact rule
- the tracker and the status-state machine
- [READY] and the gates
- the two modes (interactive, auto-battle)
- the orchestrator
- the two values (the Purpose) — the rubric every prescription is
  judged against

**You supply** — and only this:

- the domain **bindings** (§3)
- the domain's standardized **lens set** (§4)

## 3. Binding the framework to the domain

The framework spec is written in domain-general terms. Bind each to
the domain by answering:

- **The work product** — what does implement produce? (Code; a
  campaign; a document.)
- **The problem space** — what does investigate-design investigate?
  (A codebase; a market; a corpus.)
- **Scope** — what is "the set of elements the work will modify," and
  what search establishes it? Scope is a completeness claim and needs
  a mechanical basis (`spec/core.md` §2.4) — name the domain's
  search. If the domain has no mechanical search for scope, that is a
  strain (§1).
- **Verification** — what is "the domain's executable verification"
  that verify runs and shows? (Tests, build, linters; a metrics
  check; a structured review.)

Record the bindings as a table. Clippy's `core.md` is the worked
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

## 5. Generate and validate

With the instance spec written, generate the plugin:

- Generate the plugin files from the spec, per skill-craft — skill
  architecture, file layout, enforcement primitives, progressive
  disclosure. The spec is the source of truth; skill-craft is how it
  becomes a skill.
- Render faithfully. Each framework rule or mechanism becomes
  operational plugin text — and the rendering is lossy by default:
  paraphrase silently drops clauses, and a structurally-enforced
  mechanism flattens into a soft principle. Apply skill-craft's
  rendering-fidelity rule — every load-bearing clause of the source
  survives, and a structural mechanism renders *as* a structural
  mechanism (a forced step, a gate), never as prose. Verify by a
  clause-level diff against the source, not by re-reading the rendered
  text — the renderer is blind to its own flattening.

The instance also needs its `CLAUDE.md`. It auto-loads for any
session working on the instance repo, so it must carry the rule that
the skill content is rendered, not authored — or a session will
hand-edit a skill file unaware, and the instance drifts from the
spec. Seed the `CLAUDE.md` with this section, binding `<Instance>` to
the instance's name and `<skill-dir>` to its skill directory:

```
## The skill content is rendered, not authored

<Instance> is an *instance* of the Diligence framework. The skill
files — `<skill-dir>/SKILL.md`, `phases/`, and `references/` — are
**rendered** from the framework spec (the `diligence-framework`
repo, `spec/`). They are not authored here, and are never where a
behavior change originates.

A change to how <Instance> behaves goes to the framework spec first:
committed there, then re-rendered into these files and verified in a
separate context — the procedure is `development-process.md` in the
`diligence-framework` repo. Hand-editing a skill file as if it were
source breaks re-derivability: the spec and the instance drift, and
the change cannot be reproduced for another instance.

This rule covers the skill *content*. The plugin's packaging — this
file, the READMEs, `plugin.json`, and the like — is repo-local,
maintained in the instance repo directly.
```

Extend the `CLAUDE.md` below this section with the instance's own
plugin-housekeeping — description sync, version discipline, component
inventory — and any instance-specific rules.

Then validate:

- **Generative test** — not merely "could a skeleton be built," but:
  does each rendered rule carry every load-bearing clause of its
  source, and is every structural mechanism still structural? Verified
  against the spec, clause by clause. A faithful render means the spec
  is complete and the rendering held; a dropped clause or a flattened
  mechanism is the finding.
- **Empirical test** — run the instance on a real task and review the
  run against the spec. Triage each run-vs-spec deviation: an
  *adherence gap* (the spec is right, the plugin did not follow it →
  fix the plugin), a *spec gap* (the plugin followed the spec and it
  still broke → a new finding for the framework or the instance
  spec), or a *conformant success* (followed and worked → a positive
  signal for `spec/validation-watch.md`).

---

*Status: written from the Clippy spec effort and its first plugin
rewrite — which exercised the spec→plugin path and exposed the
rendering-fidelity gap §5 now addresses.*
