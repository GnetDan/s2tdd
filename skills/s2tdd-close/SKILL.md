---
name: s2tdd-close
description: "Close a feature: gate on delivered tasks, a green test suite and a converge at or after the last wave, write close-out.md (delivered, not delivered, deviations from intent, acceptance tests vs scenarios, checkpoints, where to look now), audit living references into the directory, and stamp spec.md Closed. Run after /s2tdd-converge reports converged and /s2tdd-pr-review has reviewed the PR (or you choose to skip it), before merge. Specs are intent records; the tests a feature leaves behind are its documentation."
argument-hint: "Optional feature (002-user-login, or 002) to close instead of the active one"
---

## User Input

The input is the text the user typed after the command. You **MUST** consider it before
proceeding (if not empty). If it names a feature directory (`001-user-login`, or just `001`),
close that feature instead of the active one.

## Goal

A feature directory is the record of what we intended and what we decided while building it,
and it is authoritative only while the feature is open. This command ends that phase: it
records what was actually delivered and where the implementation deviated from the spec, audits
the living files that still point into the directory, and stamps the spec `Closed`. From then on
the directory is history — read to retrace decisions, never edited, never consulted for current
behavior (that is the code, its tests, `CLAUDE.md`, `README.md`, `docs/`). Write the boundary
down once, well, so later sessions can ignore the directory with confidence and still find
their way back when they need the *why*.

Writes:

- `FEATURE_DIR/close-out.md` — new
- `FEATURE_DIR/spec.md` — **one line**: the `**Status**:` stamp
- `FEATURE_DIR/tasks.md` — tick marks only, on tasks the user confirms delivered with named
  evidence (Phase A)
- outside the feature directory: only what the user picks in Phase C

Never:

- edit any other feature directory whose spec is `Closed`
- reword spec.md, plan.md, research.md, contracts, or task text — the close-out records
  deviations beside the intent; it does not edit the intent
- move files by default — moving is an explicit per-item choice in Phase C
- commit project files — report the suggested commit message; the user commits (the last
  step saves only the specs repository)

## Prerequisites

<!-- s2tdd:shared worktrees -->
**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
<!-- /s2tdd:shared -->

<!-- s2tdd:shared feature-resolution -->
**Which feature.** Work out the feature this command is for, in this order; the first match
wins:

1. **Named.** The text the user typed after the command names a feature, as `NNN` or
   `NNN-name`, and `specs/` has that directory.
2. **Branch.** `git branch --show-current` prints a name, and `specs/<branch>/` exists.
3. **Branch number.** The branch name, after any `prefix/` such as `claude/`, starts with a
   number `NNN`, and exactly one directory `specs/NNN-*` has it.
4. **Ask.** Otherwise, list the open features (the directories in `specs/` whose spec's
   `**Status**:` does not begin with `Closed`) and ask which one.

If two directories share the number, ask; never pick one. Never write a pointer file: work the
answer out again on every run.
<!-- /s2tdd:shared -->

Then FEATURE_DIR is `specs/` plus the feature the block above resolves, in the specs directory
the first block names. The argument, when given, is the *Named* step. No argument and the block
would ask, or no match: STOP and list what exists. Run no script and write no pointer file.

1. If spec.md's `**Status**:` value already begins with `Closed`, STOP: "already closed on
   <date>; see close-out.md".
2. If tasks.md is missing, the only valid close is an abandonment: confirm with the user, write
   a two-line close-out (not started; why), stamp spec.md
   `**Status**: Closed — <DATE> — <SHA> — not started (see [close-out.md](close-out.md))`, and
   skip Phases A–C.
3. Record `SHA` = `git rev-parse --short HEAD` and `DATE` (today, ISO). If application code is
   uncommitted, say so and ask whether to continue — the close-out describes the code at SHA.
   When the only uncommitted files are exactly the docs wave's files `run-ledger.md` names,
   step 3 leaves them to A0 and asks nothing: A0 stops on them.
4. Read spec.md, plan.md, tasks.md, and every other file in FEATURE_DIR (research, data-model,
   contracts/, quickstart, orchestration, validation, checklists). This command needs everything
   once so that nobody needs it again.

## Phase A — Gate (is it done?)

**A0. Docs wave (gate — check first, before A4, so a STOP here writes nothing).**
When `run-ledger.md` records a docs wave built and uncommitted (`Docs wave <n> built,
uncommitted: <files>`) and its files are still uncommitted, STOP with no writes: "Review and
commit the docs wave first: <files>."

**A1. Tasks.** List every unchecked task (`- [ ] T…`). Ask the user in one batch, not one
prompt per task: *delivered* (name the test or checkpoint result that proves it; tick it in tasks.md) or
*dropped* (recorded under Not delivered with a one-line why). A task whose description cites a
test file that exists and passes may be treated as delivered without asking. No silent ticks
otherwise. Apply the ticks only after the whole batch is decided; if the user declines to
decide, STOP with no writes.

**A2. Suite.** Run the project's full test command (its `Full suite:` line in the agent
guidance file, otherwise from its agent guidance file or README), including the acceptance
suite. Before running it, reuse a green full run: when the newest verification-log line that
ends `· green at <sha>` has `<sha>` equal to `git rev-parse --short HEAD` and
`git status --porcelain` prints nothing, run nothing, and the close-out header says
`Suite: reused green run at <sha> (<the verification-log line's date> verify-done)`. Green is
the gate. Red: STOP unless the user explicitly accepts
it — then record the failing tests and the user's note in the close-out header. A pass against
test doubles is never a checkpoint result.

**A3. Checkpoints.** From validation.md (or the living checkpoint log it moved to) collect each validation
scenario's outcome, date, and commit. Missing outcomes are recorded as *not run* — not a gate
(unless the constitution makes it one), but never omitted from the record.

**A4. Convergence and PR review (gate — check before A1, so a STOP here writes nothing).**
Read `## Verification log` in validation.md.

- Converge: take the latest `converge · at <sha> · converged` line. Find the latest wave commit
  (`git log -1 --format=%h --grep='^feat(<NNN>): wave'`, NNN from FEATURE_DIR's name). Missing
  line, or a wave commit that is not an ancestor of (or equal to) the converge SHA
  (`git merge-base --is-ancestor <wave sha> <converge sha>` fails) → STOP: "Run
  `/s2tdd-converge` first: no converged result at or after the last wave commit."
- PR review: if no `pr-review` line exists, ask the user whether to close without a PR review
  (`/s2tdd-pr-review`). No → STOP. Yes → record `PR review: skipped by user` in
  the close-out header.

## Phase B — Deviation record

A deviation is where the code deliberately does something other than what spec, plan, or
contracts said. Sources, in order:

- tasks.md: the Notes section and every `## Phase N: Convergence` section
- validation.md findings and the fixes that cite them
- run-ledger.md's *Amendments*, *Test-owner fixes*, *Ownership exceptions*, *Expected red*,
  *Blocked and skipped* and *Open review notes*, and the `Decision:` lines in the
  `s<k>-wave-reports.md` files
- research.md entries dated after spec.md's `Created` date; contract change notes; plan.md
  Complexity Tracking
- `git log --oneline <first feature commit>..SHA` for decisions committed but never written
  down (cite the commit)

One row per deviation: *spec said* / *code does* / *why* / *recorded in* (file + heading, or
commit). A deviation with no findable reason is recorded as "why: not recorded" — never invented.

**Acceptance tests vs scenarios.** For every scenario ID in spec.md, read the acceptance test
named in the story's `**Scenarios**:` line (tasks.md) and compare its description with the
spec's scenario text. A test whose Given/When/Then differs from the spec is a deviation row
whose *recorded in* must be the orchestrator `Decision:` and test-owner commit that changed it;
if none exists, record "why: not recorded — test diverged without a decision". A scenario
mapped to a CHECKPOINT is reported with its recorded outcome (or *not run*).

**Test upkeep.** List duplicate tests (two tests asserting the same behavior) and obsolete tests
(tests of behavior the feature removed or replaced) as findings in the close-out, each with its
path. This command reports them only: no test is removed or skipped by it; pruning follows
`specs/WORKFLOW.md#test-upkeep`.

## Phase C — Reference audit (no moves by default)

Grep `CLAUDE.md`, `README.md`, `docs/`, `src/`, `tests/`, and every *open* feature directory for
`specs/<NNN>-`, the directory name, and relative links into it. Classify each hit:

- **rationale link** — cites a decision or research entry (keep; links into history are fine)
- **current-shape link** — cites a contract, schema, or runbook as the current truth
- **append target** — a log other work keeps writing to (checkpoint log, evidence tables)
- **living term** — a spec.md `Key Entities` / `Terminology` bullet that clarify marked
  `*(living)*`: a name the code, UI or users keep using after the spec freezes

For every current-shape link, append target and living term ask the user, in one batch, which
of these to do (for a living term, "repoint" means adding it to the `docs/` page or module
docstring that documents the code using it):

1. **leave** — accept the citation as historical
2. **repoint** — cite the module, test, or `docs/` page that is now the truth
3. **start a fresh `docs/` page** — new file for what must keep growing or stay true; the frozen
   original stays where it is
4. **move** — `git mv <from> docs/<same basename>`, a one-line dated stub at the old path
   (`Graduated to docs/<name> at close-out (<DATE>, <SHA>).`), references updated everywhere
   except inside `Closed` feature directories. Explicit opt-in only — never the default.

Apply only what the user picked. Declined items are listed as "kept (frozen)".

## Phase D — Write and stamp

1. Write `FEATURE_DIR/close-out.md` from the template below. Facts only — no re-narration of
   the spec, no aspirations; aim for under ~80 lines.
2. Replace spec.md's `**Status**:` line with
   `**Status**: Closed — <DATE> — <SHA> — historical intent record; see [close-out.md](close-out.md). For current behavior read the code and tests.`
   This is the only edit to spec.md and the last edit to the directory.

### close-out.md template

```markdown
# Close-out: [FEATURE NAME]

**Closed**: [DATE] at `[SHA]` (HEAD when `/s2tdd-close` ran) | **Spec**: [spec.md](spec.md) |
**Tasks**: [delivered]/[total] delivered | **Suite**: [green | reused green run at <sha> (<date> verify-done) | red — accepted: <note>] |
**PR review**: [#<PR> at `<sha>` | skipped by user]

## Delivered

| Story / requirement | Tasks | Verified by |
|---|---|---|
| US1 … | T010–T018 | `tests/acceptance/test_checkout.py`; V1 pass 2026-08-20 |

(`unverified` is an allowed value — never invent a proof.)

## Not delivered

| Item | Tasks | Why (one line) |
|---|---|---|

## Deviations from intent

| Spec said | Code does | Why | Recorded in |
|---|---|---|---|

## Checkpoint status

| Scenario | Outcome | Date / commit |
|---|---|---|

## Where to look now

- Behavior documentation: [the acceptance tests this feature left behind — file::test per scenario]
- Behavior: [modules]
- Other tests: [contract / integration / unit suites]
- Living docs: [docs/…, agent guidance sections]
- Rationale (historical, this directory): [research.md entries]

## Still referenced from living files

| Path | Classification | Decision |
|---|---|---|

Kept (frozen): [everything else in this directory]
```

## Validation Gates (before reporting)

- spec.md differs from its pre-close content by exactly one line
- every task in tasks.md is `[X]` or appears under Not delivered
- every scenario ID in spec.md appears in a `**Scenarios**:` line mapped to an existing
  acceptance test or a recorded checkpoint; the acceptance hygiene guard (no skipped or
  expected-to-fail acceptance tests; descriptions in scenario form) is green
- every path under "Where to look now" exists
- every moved file (if any): old path is a one-line stub, new path exists, no reference to the
  old path remains outside `Closed` feature directories
- `git status` shows changes only in FEATURE_DIR plus the files the user picked in Phase C;
  nothing in any other `Closed` feature directory changed

## Completion Report

- the stamp line; counts: delivered / not delivered / deviations / checkpoints run vs not run
- reference audit: kept / repointed / new pages / moved (file list)
- suggested commit: `docs: close feature NNN — <name>` with the file list
- later features cite this one with a `**Supersedes**:` line, never by editing it

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->
