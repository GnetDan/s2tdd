---
name: s2tdd-foundation-review
description: "Read-only, measured review of the whole codebase against its invariants and its own evidence (logs, databases, test counts, git history). Produces ranked drift findings with file:line and a stop rule each, the measurements with the commands used, a patterns-to-repeat/not-to-repeat list for the agent guidance file, and a hardening-spec input block (baselines per proposed success criterion, inherited violations per constitution principle). Never modifies source, tests, or specs."
argument-hint: "Optional focus area (a subsystem, a symptom, a date range of evidence) or an output path"
---

## User Input

The input is the text the user typed after the command. You **MUST** consider it before
proceeding (if not empty). It may name a focus area (a subsystem, a symptom, a date range of
evidence) or an output path.

<!-- s2tdd:shared worktrees -->
**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
<!-- /s2tdd:shared -->

## Goal

A hardening feature is only as good as the evidence it starts from. This command makes the
evidence-first review repeatable: measure before judging, rank drift by what it costs, give
every finding a stop rule (the grep or test that proves it fixed), and hand
`/s2tdd-specify` a block it can turn into success criteria with real baselines.
It is read-only on the project: it reads everything and writes almost nothing.

Writes:

- `docs/reviews/<YYYY-MM-DD>-foundation-review.md` — the report (path overridable by argument)
- the "patterns to repeat" / "patterns not to repeat" sections of the project's agent guidance
  file (e.g. `CLAUDE.md`), and only after the user confirms the proposed diff

Never:

- modify anything under the source tree, the tests or `specs/`
- run destructive or state-changing commands; measurements are read-only queries
- invent a number: every measurement names the command or query that produced it, or is
  recorded as "not measurable yet — needs <instrumentation>"

## Phase 1 — Measure

Collect evidence from real artifacts before reading code for style. Run the read-only
commands that apply to the project and record each with its output:

- **Invariant checks** from the agent guidance file (the greps and structural tests it declares
  checkable) — run each; a non-empty result is a finding
- **Test inventory**: collected test count (the runner's collect-only count, e.g.
  `pytest --collect-only -q`), per-suite counts, tests that skip or are expected to fail, suite
  duration from the last run if recorded
- **Acceptance coverage**: scenario IDs in open specs vs acceptance tests present; scenarios
  with neither a test nor a recorded checkpoint
- **Runtime evidence** when the project has it: inference-server or application logs (e.g.
  truncation, retry, timeout counts over a date range), database queries over recorded runs
  (event counts by type, fallback notices, retries per request), trace or accounting stores
- **Change evidence**: `git log --oneline --since=<range>` for churn per module; files edited
  in most commits; spec artifacts whose tasks were ticked without a named test
- **Drift between artifacts and code**: contract documents vs the signatures actually in
  code; documented env vars vs the tests/config that define them; counts restated in docs

Record the **baseline table** (`Measurement | Value | Command/query | Date`) — it becomes the
success-criteria baselines in Phase 4.

## Phase 2 — Findings

Read the code that the measurements point at (not the whole tree for its own sake). Produce
ranked findings, each with:

- **Where**: `path:line` (every finding; no finding without a location)
- **What**: the drift in one sentence, with the measurement that exposes it
- **Cost**: what it breaks or makes expensive today (a failure mode, a number)
- **Stop rule**: the grep, query, or test that proves it fixed, runnable now (it will be red)
- **Principle**: the constitution principle or guidance invariant it strains, if any

**Test upkeep.** List duplicate tests (two tests asserting the same behavior) and obsolete tests
(tests of behavior no longer in the code or its specs) as findings, each with its `path:line`
and a stop rule. This command reports them only: no test is removed or skipped by it; pruning
follows `specs/WORKFLOW.md#test-upkeep`.

Rank by cost, then by blast radius. Cap at the findings that a single hardening feature can
absorb; list the remainder in an overflow table with one line each.

## Phase 3 — Patterns

From the findings and from what is working, write two short lists for the agent guidance file:

- **Patterns to repeat** — committed patterns that are deliberate and worked (with the file
  that exemplifies each), so later sessions copy them rather than improvise
- **Patterns not to repeat** — known debt with its root cause and the fix direction, so later
  sessions do not copy it as precedent; each entry names the finding it comes from

Present the diff to the user; write it only on confirmation. The review report carries the
lists regardless.

## Phase 4 — Hardening-spec input

Write a block formatted for `/s2tdd-specify`:

- **Proposed success criteria** with baselines: `SC-?: <measurable outcome> (baseline:
  <value from Phase 1>, measured by <command>)`
- **Inherited violations** per constitution principle: `<principle> — <path:line> — <which
  story would resolve it>`
- **Candidate user stories**, outcome-framed (what the user experiences), not mechanisms
- **Checkpoints**: which criteria need a scripted run against live services, which few need a human
  (a verdict, a UX or design call, or a critical control gate), and why
- **Out of scope**: drift deliberately left for a later feature, with the evidence it waits for

## Report layout (`docs/reviews/<date>-foundation-review.md`)

1. Scope and evidence window (what was measured, over which dates, from which artifacts)
2. Baseline table
3. Findings (ranked) and overflow
4. Patterns to repeat / not to repeat
5. Hardening-spec input block
6. Commands run (verbatim, in order) — so the next review can re-measure

## Validation Gates (before reporting)

- Every finding has `path:line`, a measurement, and a runnable stop rule
- Every baseline names its command or query, or is marked not measurable yet
- No file under the source tree, tests or `specs/` changed (`git status` shows only the
  report and, if confirmed, the guidance file)

## Completion Report

- Report path; findings count (ranked + overflow); baselines collected vs not measurable
- Guidance-file sections updated (or "proposed, not applied")

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->
