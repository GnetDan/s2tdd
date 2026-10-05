---
name: s2tdd-converge
description: "Assess the current codebase against the feature's spec, plan, tasks and acceptance tests, then append any remaining unbuilt work as new tasks to tasks.md so implement can complete it. Refuses closed features; recorded, cited deviations are superseded, not gaps (s2tdd)."
argument-hint: "Optional feature (002-user-login, or 002)"
---
<!-- Adapted from github/spec-kit (MIT). -->

## User Input

The input is the text the user typed after the command. It may name a feature directory
(`002-user-login`, or just `002`); converge that one instead of the active one. Empty means the
active feature.

## Goal

Close the gap between what a feature's specification, plan, and tasks call for and what the
codebase currently implements. Read `spec.md`, `plan.md`, and `tasks.md` as the **sole
source of intent** (with the constitution as governing constraints), assess the current
state of the code, determine which requirements, acceptance criteria, plan decisions, and
existing tasks are unmet, incomplete, or only partially satisfied, and **append each piece
of remaining work as a new, traceable task** at the bottom of `tasks.md` so it can be
hardened and implemented. This command MUST run only after `/s2tdd-implement`
has completed every task in the current `tasks.md` (Step 1 checks).

This is **not** a diff tool and does **not** track changes. It assesses the present state
of the code relative to the feature's artifacts — no branch comparison, no history. Its only
git use is reading HEAD's short SHA for the log line.

## Operating Constraints

**APPEND-ONLY, NEVER REWRITE**: The command writes exactly two things: a new
`## Phase N: Convergence` section appended to `tasks.md` (only when there are gaps), and one
line appended to `## Verification log` in `FEATURE_DIR/validation.md` (always). It MUST NOT:

- modify `spec.md` or `plan.md` in any way;
- rewrite, renumber, reorder, or delete any existing task (including tasks from a prior
  Convergence phase);
- modify, create, or delete any application code — completing the appended tasks is the
  job of `/s2tdd-implement`.

When the codebase already satisfies everything, the command MUST leave `tasks.md`
**byte-for-byte unchanged** (no empty Convergence header) and report a clean result; its only
write is then the `converged` log line.

**Constitution Authority**: The project constitution (`specs/constitution.md`) is
**non-negotiable**. Code that violates a MUST principle is the highest-severity finding and
produces a corresponding remediation task. If the constitution is an unfilled template,
skip constitution checks gracefully rather than failing.

## Execution Steps

### 1. Initialize Convergence Context

Find the feature and its directory.

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

<!-- s2tdd:shared worktrees -->
**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
<!-- /s2tdd:shared -->

Call that directory `FEATURE_DIR`. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md
- CONSTITUTION = `specs/constitution.md` (if present)

If `spec.md`, `plan.md`, or `tasks.md` is missing, STOP with a clear, actionable message naming the
prerequisite command to run (`/s2tdd-specify` for a missing spec, `/s2tdd-plan` for a missing plan,
`/s2tdd-harden` for missing tasks). Do not produce partial output.

**Closed-feature guard**: read the `**Status**:` line of SPEC. If its value begins with
`Closed`, STOP without loading anything else and without touching tasks.md: "This feature is
closed (see close-out.md); its spec is a historical intent record and is neither assessed nor
edited. Further work belongs in a new feature: `/s2tdd-specify`."

**Implementation-complete guard**: list the unticked tasks (`- [ ] T…`) in TASKS, including
any in an earlier Convergence phase. Set aside as **pending checkpoints** each one whose
description begins `CHECKPOINT` after any `[P]` and `[USn]` markers (e.g. `- [ ] T091 [US3]
CHECKPOINT V2 scripted, final run before close`): checkpoints that run only at close, or whose
Done-when accepts a PENDING block, are decided by `/s2tdd-close`, which needs a `converged`
line first. Also set aside the docs wave's unticked tasks when `run-ledger.md` exists and
`handoff.md` names a docs wave (`DOCS WAVE (W<n>)`), whether the ledger records it built or not;
list them in the summary as docs wave (pending). Set the docs wave aside only in a nobrakes run:
`run-ledger.md` records one (a Runs line naming `nobrakes`) or a `Docs wave <n> built,
uncommitted` line; otherwise the docs wave's tasks count as unticked like any other. If any
other unticked task remains, STOP without writing anything: "<n> task(s) in
tasks.md are unticked; finish implementing (and verify) them before converging." (`<n>` counts
only those.) When those unticked tasks are exactly the newest Convergence phase's and the
newest verification-log line is a converge line at this HEAD reporting them appended, add:
"Converge at <sha> appended T<a>–T<b>; harden them (`/s2tdd-harden`) and implement them."
Otherwise go on, and list the pending checkpoints in the summary.

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Functional Requirements (FR-###)
- Success Criteria (SC-###) — include only items requiring buildable work; exclude
  post-launch outcome metrics and business KPIs
- User Stories and their Acceptance Scenarios
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices and technical decisions
- Data Model references
- Phases and named touch-points (files/components the plan says will be created or edited)
- Technical constraints

**From tasks.md:**

- Task IDs (to compute the next ID and next phase number)
- Descriptions, phase grouping, and referenced file paths
- Every `**Scenarios**:` line (scenario ID → acceptance test `path::name` or CHECKPOINT)

**From the acceptance tests** (the executable form of the spec's scenarios):

- Run the project's acceptance suite (the directory named by the plan's *Acceptance tests*
  field, e.g. `tests/acceptance/`; the test command comes from the agent guidance file's
  `Full suite:` line, otherwise from the project's README/CLAUDE.md). Record each red test of this feature with its scenario ID. Do not run checkpoints
  (scripted or human) — read their recorded outcome instead. Measure the wall time around
  that one run; make no second run for it.
- Before running it, reuse a green full run: when the newest verification-log line that ends
  `· green at <sha>` has `<sha>` equal to `git rev-parse --short HEAD` and
  `git status --porcelain` prints nothing, run nothing; this round's verification-log line ends
  `· suite reused (green at <sha>)` in place of the suite suffix, and the budget comparison uses
  that line's wall time.

**Suite-time budget** (from the project's agent guidance file):

- Read the budget from `CLAUDE.md`, else `AGENTS.md`: a line containing
  `Suite-time budget: <N> minutes` (case-insensitive; `<N>` an integer). No such line means no
  budget.
- Compare the wall time of the run above with it. The result becomes the suffix of the
  verification-log line (Step 8), and, when the wall time exceeds the budget, the test-upkeep
  task of Step 7. Neither changes any other finding.

**From the feature's deviation record** (decisions made after the spec was written):

- tasks.md: the Notes section and every `## Phase N: Convergence` section
- orchestration.md `Decision:` lines (a reclassified red test cites the spec scenario it now
  follows and the test-owner commit that rewrote the test)
- validation.md (or the living checkpoint log) findings and the fixes that cite them (if present)
- research.md entries dated after spec.md's `Created` date; contract change notes;
  close-out.md if present

**From run-ledger.md** (if present): every line under Open review notes, and every Carried
constraint marked carry to converge. Each one still open becomes a finding and a task like any
other gap; each one resolved is cited (the commit, test or decision that resolved it) in the
summary, with no task.

**From constitution (if not an unfilled template):**

- Principle names and MUST/SHOULD normative statements

### 3. Build the Intent Inventory

Create an internal model (do not echo raw artifacts):

- **Requirements inventory**: one stable key per FR-### / SC-### / user-story acceptance
  scenario, plus the plan decisions and constitution principles that
  impose buildable obligations. A user-story scenario is cited in the spec's ID form,
  `US<n>-AC<m>` (e.g. `US1-AC2`), in the intent inventory, in task source-refs and in the
  report.
- **Code-scope map**: from the file paths named in `plan.md` and `tasks.md`, plus a keyword
  search for the concepts each requirement describes, derive the set of source files and
  components in scope for assessment. Bound the assessment to these — do **not** infer
  scope beyond what the artifacts define.

### 4. Assess the Codebase and Classify Findings

For each item in the intent inventory, inspect the current code in scope and produce a
`Finding` only where there is a gap. Classify every finding by **gap type**:

- **`missing`**: the required work is absent from the code entirely.
- **`partial`**: the work exists but does not yet fully satisfy the requirement /
  acceptance criterion / plan decision.
- **`contradicts`**: the code does something that conflicts with stated intent or a
  constitution MUST principle, and no recorded decision explains it. A test that was changed
  in the same commit as the code that failed it is `contradicts`, never `superseded` — the
  implementer does not get to rewrite the documentation it broke.
- **`superseded`**: the code differs from the spec, plan, or a contract **and a recorded
  decision explains why** — cite it: the orchestrator `Decision:` naming the spec scenario it
  follows (`Supersedes …`) and the test-owner commit that rewrote the scenario test. A
  deliberate, recorded deviation is not a gap: summary row only, no task. Check for this before
  classifying anything `contradicts` or `unrequested`; no citation means not superseded.
- **`unrequested`**: the code contains work not called for by the spec, plan, or tasks.
  Informational — summary row only, no task — unless it violates a constitution MUST, in which
  case it is `contradicts`.

A red acceptance test of this feature is `missing` (the scenario has no implementation) or
`partial` (it has one that does not satisfy the scenario), keyed by its scenario ID. A scenario
with neither a test nor a checkpoint in any `**Scenarios**:` line is a `missing` finding on the
test side ("acceptance test absent"), source-ref the scenario ID.

Each `Finding` records: a stable id, the `source-ref` it traces to, the `gap-type`, a
severity, and a short human-readable description with the evidence (the file/area observed).

**Edge cases:**

- **Little or no code yet**: treat the entire specified scope as `missing` remaining work
  rather than failing.
- **Nothing remains**: produce zero findings and follow the converged branch in Step 7.

### 5. Assign Severity

- **CRITICAL**: violates a constitution MUST principle, or a `missing`/`contradicts` gap
  that blocks baseline functionality of a P1 user story.
- **HIGH**: a `missing` or `partial` gap on a core functional requirement or acceptance
  criterion.
- **MEDIUM**: a `partial` gap on a secondary requirement.
- **LOW**: minor partial gaps or polish.
- **INFO**: `superseded` and `unrequested` findings — never actionable.

### 6. Present the In-Session Findings Summary

Before appending anything, output a compact, severity-graded summary (no file writes yet):

## Convergence Findings

| ID | Gap Type | Severity | Source | Evidence | Remaining Work |
|----|----------|----------|--------|----------|----------------|
| F1 | missing  | HIGH     | FR-008 | Example: no append-only guard detected in path/to/module.py when writing tasks.md | Add append-only enforcement |

**Summary metrics:**

- Requirements / acceptance criteria checked
- Plan decisions checked
- Constitution principles checked (or "skipped — template")
- Acceptance tests run: green / red (by scenario ID); scenarios without a test or checkpoint
- Pending checkpoints: the unticked `CHECKPOINT` tasks the guard set aside, by task ID (left
  for `/s2tdd-close`), or "none"
- Run-ledger notes: each open one by its finding ID; each resolved one cited with the commit,
  test or decision that resolved it, with no task; or "none"
- Findings by gap type (missing / partial / contradicts / superseded / unrequested)
- Findings by severity

### 7. Append Convergence Tasks (or report converged)

**If there are one or more actionable findings** (`missing`, `partial`, `contradicts`; `tasks_appended` outcome):

Append to the **end** of `tasks.md`, per the append contract:

1. Scan all existing task IDs; let `M` be the maximum. Determine the next phase number `N`
   (highest existing phase + 1).
2. Write a single new section header `## Phase N: Convergence`.
3. Emit one checklist item per actionable finding, ordered CRITICAL/HIGH first, assigning
   zero-padded IDs `T{M+1:03d}, T{M+2:03d}, …`:

   ```markdown
   - [ ] T042 <imperative description> per <source-ref> (<gap-type>)
   ```

   `<source-ref>` traces the task to its origin: e.g. `FR-003`, `SC-002`,
   `US1-AC2`, `plan: storage decision`, `Constitution II`.

   `<gap-type>` is one of `missing`, `partial`, `contradicts`. A finding on a red or absent
   acceptance test yields a *test* task (test owner) before its implementation task.

   Constitution-violation tasks MUST be emitted first and described as
   `CRITICAL`.
4. Never reuse or renumber existing IDs. If a prior Convergence phase exists, add a new,
   separately-numbered one below it — do not touch the old one.
5. The appended tasks are unhardened (no packets, no test-first split); harden's append mode
   prepares them before implement.
6. **When the suite is over budget**, append one more task, after the others. Converge never refuses
   for the budget:

   ```markdown
   - [ ] T<n> Test upkeep: bring the suite under its <N>-minute budget (last run <M>m<SS>s); see specs/WORKFLOW.md#test-upkeep
   ```

   With no actionable findings but an over-budget suite, this one task is appended under its
   own `## Phase N: Convergence` header, and the outcome is `tasks_appended`.

   A reused run appends no test-upkeep task: its wall time is the full suite's, not this
   converge's acceptance run, so the task comes only from a run this converge timed and
   whether reuse fired never changes the task list.

**If there are no actionable findings** (`converged` outcome):

- Do **not** modify `tasks.md` at all — no empty phase header.
- Report: **"✅ Converged — the implementation satisfies the spec, plan, and tasks (acceptance suite green), or deviates only where a decision is recorded."**
- Include the summary counts of what was checked.

### 8. Record the Outcome in the Verification Log

In both outcomes, append one line under `## Verification log` at the end of
`FEATURE_DIR/validation.md` (`SHA` = `git rev-parse --short HEAD`, `DATE` = today, ISO). If the
heading is missing, add it at the end of the file; if validation.md does not exist, create it
containing only that heading.

- `converged`: `- <DATE> · converge · at <SHA> · converged`
- `tasks_appended`: `- <DATE> · converge · at <SHA> · <k> tasks appended (T<first>–T<last>)`

Then append the suite's wall time as a suffix of that line: ` · suite <M>m<SS>s (budget <N>m)`,
` · suite <M>m<SS>s (budget <N>m, over)` when the wall time exceeds the budget, or
` · suite <M>m<SS>s (no budget)` when the guidance file states none. When the suite was
reused, the suffix is ` · suite reused (green at <sha>)` instead. When the guidance file
states a budget, the reused suffix carries the comparison inside its parentheses:
` · suite reused (green at <sha>; <M>m<SS>s, budget <N>m)`, or
` · suite reused (green at <sha>; <M>m<SS>s, budget <N>m, over)` when that time exceeds it.

### 9. Report the Outcome

- On `tasks_appended`: state how many tasks were appended under which phase; note that a
  follow-up converge run will find fewer or no remaining items. List each appended task with
  the spec IDs it cites, one line each: `T<n>: <IDs>` (`US<n>-AC<m>`, `EC-<nnn>`, `FR-<nnn>`,
  `SC-<nnn>`, space-separated, or `none`), and `T<n>: upkeep` for the test-upkeep task. A task
  an earlier round wrote with `US<n>/AC<m>` is reported as `US<n>-AC<m>`, never as `none`.
- On `converged`: no further implement pass is needed for this feature's specified scope.

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->
