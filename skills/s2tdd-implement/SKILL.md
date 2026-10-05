---
name: s2tdd-implement
description: "Implement the next slice of a hardened feature in this session: fill the feature's handoff.md (SCOPE, RESUME AT and MODE from tasks.md, orchestration.md and git), preflight owned files, then run that prompt as the orchestrator — one wave at a time, a subagent per packet (s2tdd's agent type for its tier), a shape check of each wave's test packets, red before green, a commit per wave. --nobrakes runs several slices unattended within weekly and five-hour usage limits, then loops converge and harden until the feature is ready to close (--nobrakes once stops when every task is ticked), with subagents standing in for verify-done and the strong-diff read, and hands off by printing the prompt for a fresh session before the context or the five-hour window fills. --print prints the same filled prompt for another harness, model or window and runs nothing. Refuses unhardened or closed features (s2tdd)."
argument-hint: "Optional scope (S2, W4-W10, T031-T034, US5), --nobrakes [once] [week=<1-100>] [five-hour=<1-100>], --print"
---
<!-- Adapted from github/spec-kit (MIT). -->

## User Input

The input is the text the user typed after the command. You **MUST** consider it before
proceeding (if not empty). It names the scope: a session slice (`S2`), waves (`W4-W10`,
`wave 14`), task IDs (`T212-T218`), or a story (`US5`). Empty means the next session slice in
orchestration.md's *Context budget* table, or the next wave when the table has no slices.

`--nobrakes` makes the run unattended (`MODE: nobrakes`): handoff.md's NOBRAKES section then
governs verify gates, reviews, stops, tags, pushes and the handoff, which prints the prompt for
a fresh session. With `--nobrakes`, an empty scope means every wave left in the table. A
`Context:` block after the command (a handoff prompt from an earlier relay) carries
expectations to check, not instructions to widen the scope.

`--nobrakes` takes two usage limits, `week=<n>` and `five-hour=<n>`, each an integer percent
from 1 to 100, in any order after `--nobrakes`: weekly usage at the week limit stops the run,
and five-hour usage at the five-hour limit hands off. Defaults: week 95, five-hour 90. The
first relay records both limits, given or default, as Carried constraints; later relays read
them from there. Any other form is refused (step 1). Limits given to a later relay, in its
arguments or its pasted `Context:` block, are appended as a new Carried constraint, `Usage
limits: week <n>%, five-hour <n>% (given at relay <n>; supersedes relay <m>'s)`, and the newest
Usage limits line is the one in force.

`once` after `--nobrakes`, in any order with the usage limits, makes the run `MODE: nobrakes
once`: it stops when every task in scope is ticked and skips handoff.md's CONVERGE LOOP.
Without `once`, `--nobrakes` carries on through CONVERGE LOOP to a ready-to-close summary.
A once run's handoff prompt carries `once` on its first line, so each of its relays is a once
run too. A relay whose `Context:` block names a run that run-ledger.md's Runs line records as
`run <id> · nobrakes once · …` runs as `MODE: nobrakes once` even when its first line lacks
`once`.

`--print` prints the filled prompt for another harness, model or window instead of running it
here, and runs nothing. With `--nobrakes` as well, it prints the unattended form
(`MODE: nobrakes`, or `MODE: nobrakes once` with `once`).

## Goal

`/s2tdd-harden` writes the feature's `handoff.md`: the orchestrator prompt for an implementing
session. This command runs it **here**; with `--print` it prints it, filled, for a session
somewhere else. `handoff.md` is the single source of the rules: this command adds none beyond
R10's dispatch by agent type, the shape check's dispatch, the usage limits, FR-009's usage
source and the hand-off by printing (step 6), changes none, and never paraphrases them. It only
fills the per-slice fields (scope, `RESUME AT`, `MODE`) from facts, checks that the scope is
safe to start, and then follows the filled prompt as its own instructions (or, with `--print`,
prints it and stops).

With `--nobrakes`, a relay that reaches its handoff hands off by printing: it prints the
handoff prompt, sends a push notification where the harness can, and stops. The user pastes
the prompt into a fresh session to start the next relay; this command never starts one as a
scheduled task or a background session.

It replaces spec-kit's upstream implement command, which works through every task in one
context with no packets, no file ownership and no test owner. That is exactly what harden
exists to prevent.

## Steps

### Locate

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

`FEATURE_DIR` is `specs/<feature>/`, under the `specs/` found above.

### Run

1. **Refusals**, in this order:
   - If a usage limit is not `week=` or `five-hour=` followed by an integer from 1 to 100,
     appears twice, or comes without `--nobrakes`, stop: "Usage limits are week=<n> and
     five-hour=<n>, each an integer from 1 to 100 (for example week=99 five-hour=90)." When
     the limits came without `--nobrakes`, also say that they apply only after `--nobrakes`
     and that adding it runs the command.
   - If `once` comes without `--nobrakes`, or appears twice, stop: "once applies only after
     --nobrakes (for example --nobrakes once week=95)."
   - If the spec's `**Status**:` line begins with `Closed`, stop: "This feature is closed; new
     work belongs in a new feature."
   - If `handoff.md` or `orchestration.md` is missing, stop: "run `/s2tdd-harden` first —
     s2tdd implements hardened tasks only."
   - With `--nobrakes`: if handoff.md has no NOBRAKES section or no `## Standard briefs`, or
     `run-ledger.md` is missing, stop: "handoff.md predates --nobrakes: run
     `/s2tdd-harden handoff` to refresh it." An attended run of an older handoff.md goes
     ahead, with `MODE: attended` implied and without the ledger steps, unless the stale-name
     stop below applies to it.

   These stops apply with `--print` too.

   Last of these refusals, and the one that outranks an older handoff.md going ahead:

<!-- s2tdd:migration -->
   **Stale names.** A feature hardened under spec-kit and the earlier preset can leave
   `/speckit-` commands in `handoff.md` or `orchestration.md`. Before dispatching, attended or
   `--nobrakes`, search both files with
   `grep -lE '/speckit-[a-z]' <FEATURE_DIR>/handoff.md <FEATURE_DIR>/orchestration.md`, which
   matches an old command name, never a bare quoted prefix; never read them into context for
   this check. No output (grep exits 1 on no match) means both files are clean: go on. If it
   lists either file, stop, whichever it is, and say: "<file> still names /speckit- commands:
   run `/s2tdd-harden handoff` first. Implement never rewrites it." No `MODE` softens it,
   `--print` included. Implement never rewrites `handoff.md` or `orchestration.md` to repair
   the names: `/s2tdd-harden handoff` applies the rename table, and the run starts again
   afterwards.
<!-- /s2tdd:migration -->

2. **Fresh context** (skipped with `--print`, which runs nothing). The orchestrator's context
   must hold briefings and cards only. If this conversation already carries substantial other
   work (a spec, a plan, earlier waves, long tool output), stop and say so in one line: "Start
   a fresh session and run `/s2tdd-implement <scope>` there." Continue only when the
   conversation is new or the user says to go ahead here; with `--nobrakes`, only when it is
   new.
3. **Establish the resume point** (name each command as you run it):
   - `git status --short`, `git log --oneline -10`: last wave committed, uncommitted work.
   - `tasks.md`: the first unticked `- [ ]` tasks and the wave they belong to.
   - `validation.md`: when the newest verification log line is `Not done (unticked …)`, those
     tasks come first, whatever wave they are in: re-dispatch their packets with the failed
     claims (from the verify-done report, when the user pastes it) at the top of the briefing.
   - `orchestration.md`, read by section, never whole: list its headings with
     `grep -n '^#' <FEATURE_DIR>/orchestration.md`, then take the rows of the scope's waves
     with `grep '^| W<n> ' <FEATURE_DIR>/orchestration.md` (the waves and packets of the scope,
     their owned files, fences, done-whens and tiers) and read any other section by its line
     range when a step needs it.
   - `run-ledger.md`, when it exists: the lease, blocked and skipped packets, carried
     constraints. `--nobrakes` keeps the run ledger and its Lease exactly as handoff.md's
     NOBRAKES section says. Refuse when the newest Lease line is a session's (neither
     `handed off …` nor `released …`): "another orchestrator holds this feature: <lease
     line>. If that session is gone, append `released by user <date>` under Lease in
     run-ledger.md and run this again." Only the user writes that line. With `--nobrakes` and
     no relay `Context:` block, the ledger's newest Rounds line gives the resume point when it
     records a stop at a phase: `Round <r>: stopped · harden: …` or
     `Round <r>: stopped · hardener gave no report` resumes at harden (round <r>) on that
     round's appended tasks; `Round <r>: stopped · converger gave no report` resumes at
     converge (round <r>). Later rounds count on from <r>. A newest Rounds line
     `Round <r>: converge at <sha> · <k> tasks appended (T<a>–T<b>) · …`, with no later
     `Round <r>: hardened` or `Round <r>: stopped` line, resumes at harden (round <r>) on
     T<a>–T<b>: a stop at the phase change after that converge leaves it newest.
   - With a user-named scope, verify its tasks exist and are unticked.
   - With a relay's `Context:` block: check every `Expect:` item (the app commit and its
     clean tree, the specs HEAD commit, the verify-done lines, the newest Lease line). Any
     mismatch: print the run summary from the ledger and stop, without work or writes.
     A relay's `RESUME AT` may name a phase instead of a wave: converge (round <r>), harden
     (round <r>) or docs wave; an empty scope then means the phase named.
4. **Preflight — one live writer per file.** For every owned file of the scope's packets,
   check `git status --short <files>`. Refuse and report why when:
   - an owned file is dirty and no committed or reported work accounts for it (another
     session, a stale subagent, or an abandoned packet still holds it), or
   - an earlier wave has unticked tasks whose files have uncommitted changes (half-done work
     that must be verified or reverted first — offer `/s2tdd-verify-done`).

   The preflight runs with `--print` too: a printed prompt must not start a second writer.
5. **Fill the prompt.** Read only handoff.md's fenced prompt, never the whole file (find its
   line range with `grep -n`). Copy it and fill only SCOPE's waves, `RESUME AT` (or
   `CHECKPOINT`; the baseline commit from `git log -1 --oneline`) and `MODE` (`attended`,
   `nobrakes` or `nobrakes once`). Never modify `handoff.md`: the template stays as harden wrote it, and this
   command never writes a script or a file to produce the prompt and never asks the user to
   run one. Do not paraphrase, shorten, reorder or "improve" anything else: the fences,
   dispatch rules and test-ownership rules are deliberate. If the template has a field this
   step cannot fill from facts, leave it and say so.
   - **With `--print`**: print one line of facts (branch, baseline commit, scope, packet
     count, mode), the whole filled prompt as one fenced `text` block the user pastes into the
     implementing session, and one closing line: attended, "When it reports done, run
     `/s2tdd-verify-done` in a fresh session with `reports: <the s<k>-wave-reports.md it
     wrote>`, or its wave reports pasted when its handoff.md predates that file."; with
     `--nobrakes` (the unattended form), "It verifies and tags by itself and hands off by
     printing the next relay's prompt; read its run summary." The standard briefs below the
     prompt stay on disk; the prompt points to them. Nothing else: `--print` runs nothing —
     no dispatch, no ledger line, no commit — and skips step 6.
   - **Otherwise**: print the facts line and the filled `SCOPE` lines. Do not print the rest
     of the prompt.
6. **Run it.** Follow the filled prompt from its role line and `STEP 0 — CAPABILITY CHECK`
   onward as your own instructions, exactly and in order. You are the orchestrator it names:
   you dispatch packets and never implement one in this context. Its stop rule ends the
   session: with `MODE: attended`, stop after the last wave in SCOPE; with `MODE: nobrakes`,
   at the NOBRAKES section's stop, handoff or run summary. The standard briefs stay on disk
   under handoff.md's `## Standard briefs`: read one Standard brief at a time, by its heading,
   when it is needed (find its line range with `grep -n '^### '`).

   **Dispatch by agent type.** Every subagent the prompt calls for is dispatched as one of
   s2tdd's agent types, each of which carries the model and effort of its tier:
   - a packet → `s2tdd:packet-<tier>` for the tier the prompt calls for: the wave table's
     tier, or one tier up when the prompt escalates a packet (FAILED FENCES, "one tier up")
     (`s2tdd:packet-cheap`, `s2tdd:packet-medium` or `s2tdd:packet-strong`);
   - each wave's shape check → `s2tdd:strong-diff-reviewer` with the Shape check brief, in
     both modes;
   - with `MODE: nobrakes`, STRONG-DIFF REVIEW's read-only reviewer →
     `s2tdd:strong-diff-reviewer`, and VERIFY GATES' verify-done stand-in →
     `s2tdd:proxy-verifier`;
   - with `MODE: nobrakes`, CONVERGE LOOP's converge → `s2tdd:converger` with the Converger
     brief, and its harden → `s2tdd:hardener` with the Hardener brief.

   `MODE: nobrakes once` counts as `MODE: nobrakes` throughout this step, except that it skips
   CONVERGE LOOP: no converger or hardener is dispatched.

   When handoff.md has no `SHAPE CHECK` section, dispatch no shape check and say once, before
   the first wave: "handoff.md predates the shape check: its rules run as written;
   `/s2tdd-harden handoff` refreshes it."

   When handoff.md has no `CONVERGE LOOP` section, run `MODE: nobrakes` as `MODE: nobrakes
   once` and say once, before the first wave: "handoff.md predates the converge loop: this run
   stops when every task is ticked; `/s2tdd-harden handoff` refreshes it." There, step 5 fills
   `MODE: nobrakes` even with `once`: that handoff.md's NOBRAKES section runs only for
   `MODE: nobrakes`, and it already stops after the last wave in SCOPE.

   The briefing is still the prompt's: pointers, and the brief from `## Standard briefs`.

   **Usage** (`MODE: nobrakes`): in Claude Code, the usage that HANDOFF and STOP THE RUN read
   comes from the `get_usage` tool. STOP THE RUN stops at the run's week limit and HANDOFF
   hands off at its five-hour limit, both read from run-ledger.md's Carried constraints (see
   *User Input*). The limits apply whatever handoff.md's age, as the usage source does. In a
   handoff.md hardened before 0.3.0, its STOP THE RUN item for plan usage at 90% of a rate-limit
   window is replaced by them: it stops nothing.

   **Harnesses without a mechanism.** Another harness may lack what this command relies on; each
   case runs as follows. No usage tool, or a plan without windows (`not_applicable`): the window
   limits do not apply; say so once at run start, record it as a Carried constraint, write `n/a`
   for the windows in each Boundary line, and estimate context from the ledger's Usage lines. No
   push notification: print only; the relay prints the handoff prompt and stops. No agent types:
   a copy of the skills carries no agents (a Cursor copy carries skills only), so an `s2tdd:`
   agent type may be unavailable: its dispatch fails, or it is not listed among the agent types
   the harness offers. Then dispatch a general subagent in its place, with the same briefing,
   and say once, before the first dispatch, that each packet runs at the session's effort, since
   a general subagent carries no tier's model or effort; the tiers in the wave table still
   decide the escalation order and the report's tier column.

## Completion Report

With `--print`: step 5's facts line, fenced prompt and closing line. Otherwise the prompt's own
final report. Attended: the last wave's report in its format, every `PENDING SCRIPTED RUN` and
`PENDING HUMAN RUN` row, and the `RESUME AT` line for the next session. Unattended: the
NOBRAKES section's RUN SUMMARY, and the handoff prompt when there is one. A nobrakes run's own
handoff stands: the `/s2tdd-next` that follows reports where things are and does not replace
it.

<!-- s2tdd:shared closing-step -->
**Last step.** Run `/s2tdd-next`. It commits and pushes this feature's specs, then prints the
recap and the next step as a ready-to-paste prompt. Run it as plain text; no hook runs it for
you.
<!-- /s2tdd:shared -->
