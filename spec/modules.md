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
   and its rationale (including any "not recommended because…" calls)
   live in their own section. The menu carries only the loop-control
   options (continue / proceed), plain, at the very end — no inline
   annotations.
5. **Commands and code set apart.** Search commands, file paths,
   tracker citations are presented as code, not buried in prose.

The result is a two-tier read: a skim gets state + recommendation +
blockers in seconds; a deep read goes into the persisted artifacts.

### 1.2 auto-battle

The loop self-advances without per-cycle operator input. Cycles run
until the working context judges the design complete (`core.md` §4.1,
[READY]). In interactive mode the operator is then presented the
design and decides to proceed; auto-battle has no operator, so that
judgement is itself the transition to implement — the operator's
decision at [READY] is skipped.

A design decision recorded [CONDITIONAL] would, in interactive mode,
hold the run until the operator resolves it (`core.md` §1, §5.2).
Auto-battle has no operator to resolve it. Instead, when such a
decision still rests on its assumption as the design reaches [READY],
auto-battle **accepts the AI's committed recommendation** — every
design decision carries one (`core.md` §1) — and the decision is
tagged **[AUTO-ACCEPTED]** (`core.md` §5.2): the recommendation
stands, the assumption it rested on was not verified, and the tag
records exactly that. The run proceeds. Every [AUTO-ACCEPTED]
decision is, by its tag, surfaced in the tracker for the operator's
review of the completed run — it is auto-battle accepting a call the
operator would otherwise have made, recorded as such, never silently.

Auto-battle's remaining halt conditions — when a phase genuinely
cannot complete, such as a verify loop that will not converge — are a
separate effort, not yet undertaken.

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
