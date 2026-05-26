# Diligence Framework

## Iterate on understanding, not output.

A structured method for taking a complex, open-ended task to a
verified outcome — converting AI confidence into AI evidence.

The framework self-discovers the issues and gaps in the work —
including ones neither the operator nor the AI named up front — and
auto-resolves them, looping until none material remain. Throughout,
the AI synthesizes its inputs — the original task, the investigation
findings, the standardized lens results — into an evolving design the
loop drives to a verified-ready state. "Done" is derived from
evidence, not asserted.

The framework is domain-agnostic, and *instantiated* for a domain:
Clippy is the Diligence framework bound to software engineering; a
sibling instance could bind it to another domain.

## How a cycle works

Each cycle has two passes — investigation (the AI looks at
relevant surfaces with task-derived lenses) and standardized
inspection (the pre-written lens set applied to what the cycle's
work touched). Design work — committing positions on what to
build — interleaves within the cycle, not as a separate pass.
Findings land in the F-track; design decisions in the D-track.
The cycle ends when both tracks settle and the standardized
pass is clean; otherwise the AI recommends another cycle,
justified by what's still open (findings, pending decisions,
lens-applications still required). Cost is the operator's
judgment, not the AI's.

## This repo

- `spec/` — the Diligence-framework specification: the domain-agnostic
  method, the source of truth an instance is generated from.
- `instantiation-guide.md` — how to derive a new Diligence-based
  plugin for a domain.

Extracted from the Clippy spec effort, 2026-05 (in progress — see the
`coding-clippy` repo's `docs/spec/STATUS.md`).
