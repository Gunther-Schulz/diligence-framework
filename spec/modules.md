# Diligence Framework — Modules

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
loop control: the operator selects an option — continue the loop, or
proceed to the next phase. The operator's input on a design decision
is free-form override against the recorded tracker (`core.md` §1) —
never an answer to a posed choice. The AI may suggest *example*
wording the operator could use — lowering friction without
restricting the reply. Posing a binary or n-ary choice ("A or B?") is
the line: it constrains the operator's input to selected options and
is not permitted.

The menu **persists**. It is the last element of every response until
the operator selects continue or proceed. The operator may interject
free-form instead of selecting — a question, a comment, an override;
the AI answers the question or applies the override, and then
re-presents the menu. The operator never loses the advance choice.

**Closed-artifact form.** The closed artifact is structured for the
dual-purpose principle (`core.md` §3.1) — both the operator's
decision and the AI's own discipline. The form follows from that
purpose:

1. **State leads.** Open with what the operator needs to decide on:
   counts (findings, decisions, by status), whether the last cycle's
   standardized pass was clean, and the named blockers preventing
   [READY] (drawn from [PENDING] decisions and weak-basis entries in
   the ledger). Decision-relevant content first; detail follows.
2. **Scannable inventories.** Findings and decisions are bulleted
   lists, one entry per line, with status tag and identifier at the
   start of each line — not paragraph-prose summaries.
3. **Pointer, not duplicate.** Where retained artifacts (the tracker
   file, the standardized-pass per-cycle artifact) hold detail, the
   closed artifact references them — it does not paragraph-summarize.
   Detail lives once, in its persisted home.
4. **Recommendation separate from menu.** The AI's next-step proposal
   (thorough-fix-shaped per `core.md` §1; not pre-clipped on cost)
   and its rationale (including any "not recommended because…" calls)
   live in their own section. The menu carries only the loop-control
   options (continue / proceed), plain, at the very end — no inline
   annotations. **For each open [CONDITIONAL] decision, the
   recommendation surfaces the AI's committed default crisply** — what
   the AI recommends, what value or shape selecting proceed will commit
   to. This is what makes proceed-select an informed accept: the
   operator sees what they accept when they accept; the [CONDITIONAL]
   then records [AUTO-ACCEPTED] (`core.md` §5.2). The operator's
   alternative is free-form override against the tracker at any moment,
   in either mode (`core.md` §1).
5. **Commands and code set apart.** Search commands, file paths,
   tracker citations are presented as code, not buried in prose.

The result is a two-tier read: a skim gets state + recommendation +
blockers in seconds; a deep read goes into the persisted artifacts.

### 1.2 auto-battle

Auto-battle is **interactive minus the operator**. Every protocol
behavior — cycle loop, lens application, basis-rule discipline,
tracker shape, dispatch self-check (`core.md` §4.2), verify
isolation (`core.md` §4.3), [CONDITIONAL] handling — is identical to
interactive mode. The single difference is the operator slot at
decision moments: in interactive, an operator selects continue or
proceed at the closed-artifact presentation; in auto-battle, no
operator is present, so the AI's committed recommendation is taken
as default automatically.

The loop self-advances without per-cycle operator input. Cycles run
until the working context judges the design complete (`core.md` §4.1,
[READY]). At [READY], where interactive presents the closed artifact
and waits for the operator's proceed-selection, auto-battle skips
the presentation and proceeds directly — the same default-take of
the AI's recommendation, just without the operator-present-to-attest.

A [CONDITIONAL] decision still resting on its assumption when the
design reaches [READY] is recorded [AUTO-ACCEPTED] (`core.md` §5.2)
in both modes. Interactive: the operator's proceed-selection without
override on the open [CONDITIONAL] is the trigger (the closed-
artifact form per §1.1 rule #4 surfaces the AI's recommendation, so
proceed-select is an informed accept). Auto-battle: mode-absence-of-
operator is the trigger. The tag records the same thing in either
case — the recommendation stands; the assumption was not verified.
Every [AUTO-ACCEPTED] decision is, by its tag, surfaced in the
tracker for the operator's review of the completed run.

Auto-battle's remaining halt conditions — when a phase genuinely
cannot complete, such as a verify loop that will not converge — are
a separate effort, not yet undertaken.

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
ledger, not its design narrative.
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

The tracker is **append-only**. A new entry, and every later change
to an entry — a new status, a corrected summary — is a new ledger
line appended to the tracker; existing lines are never edited. Each
line carries its entry's identifier, and an entry's current state is
its latest line: where current state is needed — at [READY], a
resume, the closed artifact — it is the tracker reduced to the latest
line per entry. The append-only history is the run's audit trail;
because no line is ever rewritten, no past entry can be silently
altered.

Not every change is substantive. A **basis-only refinement** on an
entry at its terminal status — [VERIFIED], or [AUTO-ACCEPTED] for a
design decision in auto-battle — where the status and summary are
unchanged and only the basis strengthens (further evidence grounds
what previously rested on a weaker basis) — is appended as a
**sub-annotation** under the entry, not as a new peer-level ledger
line. The sub-annotation carries the strengthened basis on one
line; the peer-level entry is unchanged. Reduce-to-latest: an
entry's current state is its latest peer-level line together with
any sub-annotations attached. The append-only property holds — no
past line is rewritten, the sub-annotation is itself a new appended
line — and the audit trail is preserved without the duplicate-line
tax of re-emitting a peer line for an evidence-only update.

### 3.2 The standardized-pass findings artifact

Each cycle's standardized inspection pass emits a findings artifact
(`core.md` §4.1): one line for each lens whose scope the cycle touched
— a finding, or a cited-clean reason. A lens out of scope that cycle
is not lined; the standardized set is accounted for whole once, at
[READY] (`core.md` §4.1).

### 3.3 The impl plan

implement-phase's planning artifact (`core.md` §4.2): a list of
**dispatch units** in dependency order, with a parallel-eligibility
marker on each. A dispatch unit is a group of design decisions
implemented together as one piece of work; the unit's entry cites
the [VERIFIED] decisions it implements (by their tracker
identifiers).

Parallel-eligibility is a load-bearing claim per `core.md` §3.2: the
unit's file and contract scopes are listed, and the disjointness
from sibling units' scopes is established by the re-runnable search
behind the claim — the executable query, not the asserted
disjointness or a recalled enumeration. A unit whose disjointness is
not search-established is sequential by default. The basis-rule
discipline that governs decision bases (`core.md` §3.2) applies here
in the same form: a recalled disjointness is not a basis; the search
is.

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

## 4. Post-run review

An optional final step after verify reports [PASSED]: surface what
the protocol missed or got wrong in this run, to inform the next
iteration. This is the framework's empirical-validation procedure —
the input that drives the next amendment cycle
(`development-process.md`).

### 4.1 When and how

After verify reports [PASSED] the run is complete. The operator
**may** request a post-run review. The AI does not prompt for it;
the operator decides when a run warrants the analysis.

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
  specific lens, the basis rule, the [READY] judgement) should have
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
  evidence-bearing rule, violated anyway → the irreducible residual
  the verify, operator, and loopback backstops carry.

### 4.6 What this is not

A general code review. A confidence check. A graded report. The
review's only job is to surface what the *protocol* missed or got
wrong, in a form the operator can act on.
