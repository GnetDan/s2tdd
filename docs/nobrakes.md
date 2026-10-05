# Running unattended: `--nobrakes`

[← Back to the README](../README.md)

```text
/s2tdd-implement --nobrakes
```

One command runs the rest of a hardened feature with nobody watching, and carries on through
converge until the feature is ready to close. Use it when you've put the time into the spec and
the plan and trust them: the build after that is following instructions, and it doesn't need you
in the room.

## Before you start

- **The feature is hardened.** `/s2tdd-harden` has written `tasks.md`, `orchestration.md`,
  `handoff.md` and `run-ledger.md`. Implement refuses otherwise.
- **The spec says what you mean.** An unattended run builds the spec faithfully, vague parts
  included. The time to catch a wrong scenario is before this command, not after.
- **Start in a fresh session.** With `--nobrakes`, implement only runs in a new conversation.
- **A cost-efficient model is fine** for the session. The packets run on their own agent types
  whatever the session uses; see [Models and budget](models.md).

With no scope, it runs every wave left. Name one to run less: `/s2tdd-implement S2 --nobrakes`
(or `W4-W10`, `T031-T034`, `US5`).

To build the waves and stop, without converging, add `once`:

```text
/s2tdd-implement --nobrakes once
```

A run started with `--nobrakes once` stops when every task in scope is ticked, as runs did
before 0.4.0. A feature hardened before 0.4.0 runs that way too, until `/s2tdd-harden handoff`
refreshes its `handoff.md`.

## Converging to ready to close

When no wave is left, the last verify gate has passed and only the docs wave and pending
checkpoints are unticked, the run converges instead of stopping. It goes in rounds:

1. **Converge.** The `converger` agent runs `/s2tdd-converge` for you. If the feature matches
   its spec, the round has converged.
2. **Harden.** If converge appended tasks, the `hardener` agent hardens them with
   `/s2tdd-harden`'s append mode.
3. **Build.** The run builds the new waves like any other, with verify gates at their slice
   ends and one before the next converge. Then the next round starts.

Each round writes a line under `## Rounds` in `run-ledger.md`. There's no round cap; instead the
run stops for you when the loop isn't getting anywhere:

- **No shrink:** a round appended at least as many tasks as the round before (round 1 never
  stops on this);
- **Gap back:** an appended task cites a scenario or requirement that an earlier round's task
  already fixed;
- **Cites nothing:** an appended task cites no scenario, edge case, requirement or success
  criterion.

The test-upkeep task converge adds when the suite is over its time budget doesn't count
toward these.

When a round converges, the run builds the docs wave and ends its summary like this:

```text
READY TO CLOSE
Next:
1. Pending checkpoints: <V-rows> | none
2. Review and commit the docs wave: <files> | none
3. /s2tdd-pr-review <PR number, once the PR is open>
4. /s2tdd-close
```

The loop never runs `/s2tdd-pr-review` or `/s2tdd-close`: those are yours.

## Usage limits

```text
/s2tdd-implement --nobrakes week=95 five-hour=90
```

`week=` and `five-hour=` each take a whole percent from 1 to 100, in any order after
`--nobrakes`. Leave them out for the defaults, 95 and 90.

- **The week limit stops the run**, with its summary, once weekly usage reaches it. It counts
  the higher of the weekly window and the weekly window of each model the run uses.
- **The five-hour limit hands off.** The run reaches a clean boundary and prints its handoff
  prompt with the window's reset time: paste it after the reset.

The first session records both limits in the feature's `run-ledger.md`, and later sessions read
them from there.

## What stands in for you

Subagents take your place only where a later check can catch their mistakes.

| When | What happens |
|---|---|
| **After each wave** | The project's per-wave test command runs once, or the full suite when the wave changed files it can't see. See [Test runs](test-runs.md) |
| **At each slice end** | The proxy verifier runs `/s2tdd-verify-done` for you, with the full suite, in a scratch worktree while the next wave starts. A failed claim's tasks go first in the next wave |
| **When every wave is built** | The converger runs `/s2tdd-converge` and the hardener hardens what it appends, round by round, until the feature is ready to close |
| **Before each strong packet's wave commit** | A read-only reviewer reads its diff and confirms or disputes each decision it made |
| **Before each wave commit with test packets** | The shape check: a read-only reviewer reads the wave's test packets against the contract sections they cite. Its findings go back to the test packet before the commit; what that doesn't settle is noted for converge |
| **A finding breaks a spec MUST** | It's a blocker, never a note: the packet fixes it before the commit, or is blocked |
| **A packet fails twice** | It gets one more try a notch up, then is blocked. Its dependents are skipped; waves that don't depend on it carry on |
| **A live checkpoint comes up** | It's written up as a pending run with its exact commands, for you to run later |
| **The docs wave** | Built and checked last in the run (in a looping run, only once a round converges; a run that stops first leaves it unbuilt), and left for you to commit |
| **After each verified slice** | Matching tags go into the app and specs repositories, and both are pushed (never forced) |
| **Before its context is half full** | The session verifies what it has, prints a handoff prompt for a fresh session, and stops |
| **After each wave commit** | It reads its usage, checks for brakes and writes a `Boundary:` line into the wave report |

## It doesn't run out of context

A long run is several sessions, each handing off to the next before its context is half full.

- **You start each session.** A hand-off prints the prompt, sends a push notification where the
  harness can (Claude Code), and stops. Paste the prompt into a fresh session to carry on. No
  session ever starts another by itself.
- In Claude Code it reads its usage from the `get_usage` tool, never an estimate. Where there's
  no usage tool, the window limits don't apply and the run says so once at the start.
- After each wave commit it writes one line into the wave report, so you can see how the run
  went at a glance:

  ```text
  Boundary: context 31% · five-hour 44% · week 62% · BRAKES none · ledger +3 lines
  ```

  Without a usage tool the windows read `n/a`. `/s2tdd-verify-done` flags a wave that has no
  such line.
- All the state lives in the feature's `run-ledger.md`, so every session resumes from files
  and nothing depends on a summary.

## When it stops

It stops the run, with a summary, on anything a person must decide:

- a blocked MVP or guard test;
- a contract change that would break committed code;
- a file another session holds;
- a secret in any output;
- the verifier failing twice;
- a converge round that stops the loop (no shrink, gap back, cites nothing), or a converger or
  hardener that gives no report twice;
- the hardener stopping on one of harden's preconditions, with harden's message in the summary;
- a packet still blocked when the waves end, before converge, naming it and the packets it
  skipped (a blocked MVP or guard test stops the run at once);
- weekly usage reaching the week limit.

## What it never does

- Merge.
- Run `/s2tdd-pr-review` or `/s2tdd-close`.
- Use a credential.
- Run a live checkpoint.
- Commit the docs wave.
- Take a decision that's yours: design and UX calls, rulings on failing tests, the close-out
  gate.

## Pulling the brakes

Say "brakes" in chat, or create `.sdd-run/<NNN>/BRAKES`. It finishes the current wave, then
hands the next verify back to you.

## When you come back

Read the run summary, or run `/s2tdd-next` to see where the feature stands. The summary's
`Rounds:` line says how the loop went, and its `Test runs:` line counts the per-wave and full
runs. Then:

1. If it handed off, paste the prompt it printed into a fresh session (after the reset time, if
   it names one). The run carries on from there.
2. Run any pending checkpoints it wrote up.
3. Commit the docs wave once you've read it.
4. If it stopped, make the decision it stopped for and run `/s2tdd-implement --nobrakes` again.
   It resumes from the ledger.
5. If it ended READY TO CLOSE, follow its Next block: pending checkpoints, the docs wave, then
   `/s2tdd-pr-review` and `/s2tdd-close`. A run started with `--nobrakes once` stops when every
   task is ticked: carry on with `/s2tdd-converge`.

## Field status

`--nobrakes` ran end to end in a first pilot on 0.2.0. 0.3.0 carries what it taught: the
per-wave shape check, hand-offs you start yourself, a limit per usage window, and the
`Boundary:` line. 0.4.0 adds the converge loop and a test run per wave sized to the wave.

The rules the run follows are in the feature's own `handoff.md` (the NOBRAKES section and
*Standard briefs*), and the [workflow guide](../src/pages/WORKFLOW.md) has the short version.
