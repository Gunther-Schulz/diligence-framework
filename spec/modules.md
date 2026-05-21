# Diligence Framework — Modules

The framework's revisable modules — modes, the standardized lens set,
artifact formats. Built on `core.md` and `glossary.md`; terms are
used as defined there.

---

## 1. Modes

A run is driven in one of two modes. A run is interactive by
default; it is in auto-battle only when auto-battle is explicitly
requested at invocation. The orchestrator detects the mode at run
start (`core.md` §5).

### 1.1 interactive

The operator advances the run. After each investigate-design cycle,
and at each phase boundary, the AI presents the tracker — its
findings and recorded design decisions — and a recommendation; the
operator reviews and selects whether to continue or to proceed. The
advance point is a menu.

### 1.2 auto-battle

The loop self-advances without per-cycle operator input. Advancement
is governed by structural control — the cycle structure and the
[READY] gate — not by AI judgement of when to stop.

This is auto-battle's foundation only. Its full design — halt
conditions, and the handling of a decision that needs the operator
with none available — is a separate effort, not yet undertaken.

## 2. The standardized lens set

The standardized lenses are the pre-written inspection criteria the
standardized inspection pass applies (`core.md` §3.1). The set is
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
§2.1 shape. The instance specifies it; the framework requires only
that the set is closed and complete for the domain. Clippy's coding
lens set is an example instance.

## 3. Artifact formats

### 3.1 The tracker

The tracker holds three tracks (`core.md` §4): findings, design
decisions, implementation steps. Each entry carries its status tag
and the content its track requires:

- **Finding** — a summary and verification evidence.
- **Design decision** — a category, a summary, and a basis
  (`core.md` §2.4).
- **Implementation step** — the concrete design detail required to
  mark it [RESOLVED]: enough that implementing it introduces no new
  design decision.

### 3.2 The standardized-pass findings artifact

Each cycle's standardized inspection pass emits a findings artifact
(`core.md` §3.1): one line for every lens in the set — a finding or a
cited-clean reason for a lens in scope, a cited reason for one out of
scope.
