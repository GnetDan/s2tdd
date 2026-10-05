---
name: s2tdd-next
description: "Save, then say where things stand and what to run next: commits and pushes the active feature's (or epic's) files in the specs repository, reads its files and git, recaps in a few lines, and prints the next step as a ready-to-paste prompt that carries whatever the next session needs. Every s2tdd step ends by running it; run it yourself any time, e.g. after a break. Read-only on the project; never force-pushes; never runs the suite."
argument-hint: "Optional feature (002-user-login, or 002) or epic slug"
---

## User Input

The input is the text the user typed after the command. It may name a feature directory
(`002-user-login`, or just `002`) or an epic slug; save and report on that instead of the active
one. When this runs as another command's last step, the command that just finished is earlier
in this session's transcript: use what it reported.

## Goal

One answer to "what now?", from the repository, not from memory. Every fact comes from a file
read or a command run now; a remembered fact the repo contradicts is reported as stale.

Saving comes first: spec changes are saved as soon as a step makes them, so the user never has
to commit or push them by hand and the next session (or another machine, or a cloud session)
sees them. That save only ever commits and pushes in the specs repository. Beyond it, this
command writes nothing: it is read-only on the project (it never stages, commits or edits
anything there) and never runs the test suite.

## Steps

### 1. Locate

<!-- s2tdd:shared worktrees -->
**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
<!-- /s2tdd:shared -->

In the `git -C specs …` commands below, `specs` is that directory: `./specs`, or the main
worktree's `specs/` when `./specs` does not exist here. Paths given to `git -C specs` are
relative to the specs repository: `<feature>/`, `epics/<slug>/`, `README.md`, `WORKFLOW.md`,
`constitution.md` (never `specs/<feature>/`, which would name `specs/specs/<feature>/` and match
nothing).

When the input names no feature or epic and the command that just finished (earlier in this
session's transcript) reported the feature or epic it worked on, use that one and skip the
resolution blocks below; when it was `/s2tdd-epic`, that is the epic, in epic mode. Otherwise
resolve as follows.

When the step that just finished was `/s2tdd-epic`, or the input names an epic slug, work in
**epic mode** (step 4b) and find the epic:

<!-- s2tdd:shared epic-resolution -->
**Which epic.** Work out the epic, in this order; the first match wins:

1. **Named.** The text the user typed after the command names a slug, and
   `specs/epics/<slug>/` exists.
2. **Single open epic.** Exactly one epic in `specs/epics/` has a `map.md` whose `**Status**:`
   does not begin with `Closed`.
3. **Ask.** Otherwise, list the open epics and ask which one.
<!-- /s2tdd:shared -->

Otherwise work in feature mode and find the feature:

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

The directory to save and report on is the feature's `specs/<feature>/`, or in epic mode
`specs/epics/<slug>/`; under `git -C specs` it is `<feature>/` or `epics/<slug>/`, written
`<directory>` below.

### 2. Save

1. **Is `specs/` its own repository?** `git -C specs rev-parse --show-toplevel` must be the
   `specs/` directory itself. If it is the project root (specs are tracked by the project
   repository) or `specs/` isn't a git repository, commit nothing: say so in one line and go on
   to step 3. Never commit in the project repository; its commits are the implementer's waves.
2. **Commit.** `git -C specs status --short -- <directory> constitution.md`. Nothing changed: say
   "specs: nothing to save" and go to the push. Otherwise stage only that directory
   (`git -C specs add -- <directory>`), plus `specs/README.md` or `specs/WORKFLOW.md` when it is
   untracked (first-run setup copies them in; `git -C specs add -- README.md WORKFLOW.md` for
   the untracked ones), plus `specs/constitution.md` when it is new or changed
   (`/s2tdd-constitution` writes it outside any feature directory;
   `git -C specs add -- constitution.md`), and commit with a
   message naming the feature and what changed, e.g. `006: tasks`, `006: hardened`,
   `006: verify-done waves 3–4`, `epic auth: ticket 4 resolved`. Never stage anything else:
   other sessions may be editing other features or tickets.
3. **Push.** When the branch has an upstream and is ahead of it, `git -C specs push`. Never
   force, rebase or pull. If the push is rejected (another machine pushed first), say so in one
   line, as a fact. If the branch has no upstream, the push is skipped: say so in one line, with
   why (no upstream). Either way, carry on: the recap and the next step still print.

### 3. Gather (in parallel; name each command)

- `git branch --show-current`, `git status --short`,
  `git log -15 --date=relative --format="%h %ad %s"`, `git stash list`, `git worktree list`
- The feature directory: which of `spec.md`, `plan.md`, `tasks.md`, `orchestration.md`,
  `handoff.md`, `validation.md`, `close-out.md` exist; the spec's `**Status**:` line; whether
  spec.md has a `## Clarifications` section with a `### Session` heading.
- `tasks.md`: ticked vs unticked counts; unticked tasks no packet in `orchestration.md` covers
  (typically a `## Phase N: Convergence` section); the next 2–3 unticked task IDs.
- `validation.md`: the `## Verification log` lines (verify-done, converge, pr-review), and any
  `PENDING SCRIPTED RUN` / `PENDING HUMAN RUN` blocks.
- `run-ledger.md`, when it exists: the lease, *Blocked and skipped*, *Open review notes*, a
  docs wave left uncommitted, rejected pushes, and the *Handoff* section's newest prompt.
- `s<k>-wave-reports.md` files: which waves they cover.
- Wave commits: `git log --format="%h %s" --grep="^feat(<NNN>): wave"`, newest first.
- Open PR for this branch, when `gh` is available: `gh pr list --head <branch> --state all
  --json number,state,url`.
- Other live sessions for this repo, if the harness can list them.
- The suite record: the newest `validation.md` verification-log line that holds ` · suite `
  (verify-done and converge append it). When it says `over`, the line's date and command and its
  `<M>m<SS>s` and `<N>m` feed **Watch out**'s suite item.
- Merged feature branches: the default branch (`git symbolic-ref --short
  refs/remotes/origin/HEAD` without its `origin/`, else `main`, else `master`), then
  `git branch --merged <default>` for local branches and `git branch -r --merged <default>`
  for remote ones still present. Keep only the branches whose name leads with a feature number
  (`004-csv-export`, or `claude/004-csv-export`), never the default branch or the current one.
  Specs live in their own repository, so a feature branch has no project commits until
  implement, and `git branch --merged` lists such a branch too: from git alone, a branch with no
  commits of its own (`git rev-list --count <default>..<b>` is 0) looks the same as a merged
  one. So keep a branch only when its feature's spec in `specs/` is `Closed`, or
  `gh pr list --head <b> --state merged` finds its PR; when neither can be read, leave it off.
- A project copy of the skills: when `.claude/skills/s2tdd-*/` exists here, whether the plugin is
  also installed. Run `claude plugin list --json` and look for an entry whose `id` starts with
  `s2tdd@` and whose `enabled` is true, at any scope. When `claude` is not on the path, read
  `~/.claude/plugins/installed_plugins.json` for an `s2tdd@` key and `enabledPlugins` in
  `~/.claude/settings.json`. When neither can be read, you cannot tell. Without such a folder,
  run none of this.
- What step 2's save left: spec changes still uncommitted or unpushed in the specs repository
  (`git -C specs status -sb`), when `specs/` is its own repository. Any left go under
  **Watch out**, as facts; the save already ran, so offer no fix for them.

### 4a. Decide the next step (feature mode; first match wins)

| State | Next | Session |
|---|---|---|
| No `spec.md` | `/s2tdd-specify` | — |
| Status `Closed`, PR open | Commit and push the close-out (`close-out.md` and the `Closed` stamp: in the specs repository, or on this branch when `specs/` is tracked here), then merge the PR (give its URL) | — |
| Status `Closed` | `/s2tdd-specify` for the next feature | fresh |
| No `plan.md`, no clarify session in spec.md | `/s2tdd-clarify` | same |
| No `plan.md` | `/s2tdd-plan` | same |
| No `tasks.md`, `orchestration.md` or `handoff.md` | `/s2tdd-harden` (it writes `tasks.md` first when it is missing) | same, or fresh if this context is heavy |
| Unticked tasks no packet covers | `/s2tdd-harden` (it hardens only the new tasks) | fresh, strong model |
| The ledger's newest Lease line is a session's (not `handed off`, not `released`) | Nothing to start: that session is still the orchestrator (name it). Let it finish; if it is gone, append `released by user <date>` under Lease in run-ledger.md, then run the implement step | — |
| The ledger records a docs wave built and left uncommitted | Review the docs diff, then commit it and tick its tasks | — |
| Wave commits newer than the last `verify-done` log line | `/s2tdd-verify-done` on those waves | fresh |
| Unticked tasks | `/s2tdd-implement` (next slice) | fresh |
| No `converge` log line after the newest wave commit | `/s2tdd-converge` | fresh |
| Converged, no PR for this branch | Commit the feature directory if `specs/` is tracked in this repository, then push and open the PR: `git push -u origin <branch>`, then `gh pr create --fill` (or the hosting UI); then `/s2tdd-pr-review <n>` | — |
| PR open, no `pr-review` line after the newest wave commit | `/s2tdd-pr-review <n>` | fresh, strong model |
| Newest `pr-review` line is a `report` run with fixable findings | `/s2tdd-pr-review <n> --fix`, or fix by hand | fresh |
| Reviewed | `/s2tdd-close` | fresh |

**Pending checkpoints** are unticked tasks whose description begins `CHECKPOINT` after any
`[P]` and `[USn]` markers: checkpoints that run only at close, or whose Done-when accepts a
PENDING block. Every row above that counts unticked tasks ignores them, so a feature whose
only unticked tasks are pending checkpoints goes on to converge, the PR and close, which
decides them. List them under **Watch out**.

The implement step is always `/s2tdd-implement`, which runs `handoff.md` in the new session
itself. Never offer the handoff prompt instead; name `/s2tdd-implement --print` only as the
option for running the slice in another harness, model or window.

A wave commit after the newest `converge` line sends the chain back through
`/s2tdd-verify-done` and `/s2tdd-converge`. Fix commits from `/s2tdd-pr-review --fix` don't:
they are test-first and suite-checked inside the review. A failed verification unticks the
tasks it failed, so the *Unticked tasks* row picks them up. `PENDING HUMAN RUN` blocks never
hold up the chain: list them under **Watch out**, and close records any still not run. Without
`gh`, say you can't see PRs and ask the user for the PR number instead of guessing. A review
run in a cloud session leaves its log line only in that session's report: before recommending a
review again, ask whether one already ran there.

When the transcript shows the step that just finished stopped early (refused, blocked, the user
said stop), the next step is to resolve that, named in one line, not the next row of the table.

### 4b. Decide the next step (epic mode)

Read `specs/epics/<slug>/map.md` and its tickets:

- Status `Closed`: the epic is done; the next step is the feature specs it names (above).
- Frontier tickets left: `/s2tdd-epic <slug> <ticket>` for the first unclaimed one, fresh
  session, strong model. Name any other unclaimed ones that can run in parallel sessions.
- Frontier and fog empty, no seeds: `/s2tdd-epic <slug>` to write the seeds.
- Seeds written: `/s2tdd-specify` with the first seed whose spec doesn't exist yet, fresh
  session, strong model.
- Every seeded spec exists, Status still `Open`: `/s2tdd-epic <slug>` to close the epic.

### 5. Write the prompt

The prompt is what the user pastes to start the next step. It is the command line plus, only
when there is something, a short **Context** block: what the next session needs and cannot
rediscover from the files. Draw it from this session's transcript and the gathered facts:

- before plan: questions clarify deferred, or that the user said "enough" with branches open
- before implement: the `RESUME AT` line; corrective items from a failed verification;
  blockers or open questions a packet reported
- before verify-done: the wave-reports file to read, as the argument `reports:
  <feature directory>/s<k>-wave-reports.md; commits <first>..<last>` (a path, never the
  reports pasted: long arguments get cut); when no such file covers the waves, the wave reports
  from this session verbatim, else the wave commits to check
- after an unattended run (`/s2tdd-implement --nobrakes`): when it started the next session
  itself, say so under **Where things stand** and print no prompt; when it printed a handoff
  prompt, that prompt is the next step, unchanged
- after a failed verification: the tasks it unticked and why, one line each
- before converge, pr-review or close: deviations decided in conversation but not yet written
  down, and anything the user asked to have checked
- anything the user said that changes the next step and isn't recorded in a file

Never paste file contents, restate the spec, or add advice. Housekeeping never goes in the
prompt: uncommitted or unpushed files, branch state. Those are reported under **Watch out**, as
facts. No context, no block: the bare command is the prompt.

Pass arguments only in the form the target command documents. The feature is found from the
branch, so don't add the feature name: `/s2tdd-harden`, for example, reads its argument as a
phase name. Implement takes a scope (`wave 5`, `T031-T034`); pr-review takes the PR number.

## Output (short; this order)

When the command that just finished has not printed its own report yet, print that report
first and this output after it, so the prompt is the last thing on screen.

1. **Saved**: step 2's one line, e.g. `specs: committed and pushed 73fdb34 (006: tasks)`,
   `specs: nothing to save`, `specs: committed 73fdb34; push skipped, the branch has no
   upstream`, or `specs: committed 73fdb34; push rejected, the remote has newer commits`.
2. **Where things stand**: one or two lines: branch and last commit (how long ago); feature,
   stage and `done/total` tasks; uncommitted files and what they look like (waves commit
   themselves when green, so dirty files owned by unticked tasks mean a wave didn't finish).
3. **Watch out**, only when something applies: stashes, extra worktrees, other live sessions,
   open `Decision:` lines, a remembered fact the repo contradicts, spec changes the save left
   uncommitted or unpushed, and from run-ledger.md: blocked packets, open review notes,
   rejected pushes.

   Two more items, each only when it applies:

   - **Suite over budget.** When the newest suite record says `over`:
     `Suite over budget: <M>m<SS>s against <N>m (<date>, <command>).` A fact; nothing refuses
     because of it, and with no stated budget the record never says `over`.
   - **Merged feature branches.** Each branch the gather found, one line per branch, with
     `git branch -d <b>` for a local one and `git push origin --delete <b>` for a remote one
     (`<b>` without its `origin/`). This command deletes nothing: the lines are for the user to
     run. Add one line recommending the repository's automatic deletion of head branches (the
     hosting setting that removes a branch when its pull request merges), so the list stays
     empty.
   - **Copy beside the plugin.** Only when `.claude/skills/s2tdd-*/` exists. When the gather found
     the plugin installed and enabled, the item lists the copy and says its commands are the ones
     that run: Claude Code loads the plugin's as `/s2tdd:s2tdd-<name>`, so every bare
     `/s2tdd-<name>` the chain prints runs the copy. An installed but disabled plugin raises
     nothing. When the gather could not tell, the item says it could not tell whether the plugin
     is installed and still lists the copy, as a fact.

<!-- s2tdd:migration -->
   **Spec-kit leftovers.** First-run setup and the move to the plugin leave files of the old
   packaging behind; they are leftovers, reported here as facts. Check, read-only, which of these
   exist in the project: `.specify/`, `.claude/skills/speckit-*/` and `docs/sdd-workflow.md` (the
   old project page, which first-run setup leaves in place when it writes `specs/WORKFLOW.md`).
   Under Watch out, name each one found, one line each. With none found, say nothing. This
   command deletes and edits none of them.
<!-- /s2tdd:migration -->

4. **Next**: the command and one line of why, then where it runs: *this session* or *fresh
   session*, and the model when it changes. Strong model (high effort) for epic, specify,
   clarify, plan, harden and pr-review; a cost-efficient model is enough for implement,
   verify-done and converge.
5. The prompt, in one fenced `text` block, so it can be copied whole:

   ````text
   /s2tdd-implement

   Context:
   - RESUME AT: wave 5 (baseline 3f2fdaa)
   - Wave 4's verification failed T031: the retry test passes against the stub only. Fix first.
   ````

End on exactly one line, after the prompt block: "Run it now?" when the next step is in *this
session* (run it on a yes), otherwise "Nothing else to do in this session: paste the prompt into
a fresh session." Leave no other open question, offer or loose end anywhere in the output (to
commit, push, fix or explain something): the user's harness suggests replies from what is on
screen, and a loose end becomes the suggested next message instead of the prompt. Facts that
need the user go under **Watch out**, stated as facts.
