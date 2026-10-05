# Test runs: one per wave, the full suite at slice ends

[← Back to the README](../README.md)

Implement builds a feature one wave at a time. Packets run only their own targeted tests; after
each wave the orchestrator runs the project's tests once, before the wave commit. That run
doesn't have to be the whole suite. A project can name a faster **per-wave** command that runs
only the tests the wave's changes affect, and keep the **full suite** for the points where every
test must pass: each verify gate, converge, close and CI.

Per-wave runs apply attended and unattended alike. Attended, your `/s2tdd-verify-done` after
each implement session is the slice's full run, and implement's final report says so.

## The three lines

Put them in the project's agent guidance file (`CLAUDE.md`, else `AGENTS.md`), each at the
start of its own line:

```text
Per-wave tests: <the command run once after each wave>
Full suite: <the command that runs every test, slow ones included>
Per-wave sees: <glob>, <glob>, …
```

- **`Per-wave tests:`** is the per-wave command. s2tdd runs it exactly as written and passes it
  nothing: picking the tests the uncommitted changes affect is the project's tool's job, never
  the model's.
- **`Full suite:`** is the command verify gates, converge and close run. Without it, s2tdd finds
  the full suite command as before: from the agent guidance file, otherwise the obvious one.
- **`Per-wave sees:`** (optional) names the files the per-wave command can trace, as
  comma-separated globs over repository-relative paths, with `*` crossing `/`. A wave that
  changes a file outside them runs the full suite instead. Without the line, the per-wave command
  is trusted for every change.

Labels match case-insensitively and may sit inside a fenced block; a label anywhere else on a
line doesn't count, and the command is the rest of the line, verbatim. A second line with the
same label, or `Per-wave sees:` without `Per-wave tests:`, is ignored, and harden says so in its
report.

`/s2tdd-harden` copies the lines into the feature's `handoff.md` (its `TEST RUN` section). After
you change them, `/s2tdd-harden handoff` copies them in afresh.

## What runs after each wave

The per-wave command, unless one of these makes it the full suite:

- the project declares no `Per-wave tests:` line;
- the wave changed a file outside `Per-wave sees:` (the changed files are `git diff --name-only
  HEAD` plus untracked files, in the app repository only);
- per-wave runs are off for the rest of the run (below).

**Zero selected is green.** A run whose output has the test runner's summary line ran, even when
it selected no tests; the wave report says `0 selected`. (pytest prints "no tests ran" and exits
5 when nothing is selected: that still counts as a run.)

**A run with no summary failed to run.** That wave runs the full suite, the run records the
Carried constraint `Per-wave runs off from wave <n>: <first error line>` in its ledger, and every
later wave of the run uses the full suite. The run summary shows it.

Every wave report has a `Test run:` line naming the run (per-wave or full), its command, its
counts and its wall time, so you can see what each wave actually checked.

## Full runs, and reusing a green one

Every verify gate runs the full suite: the proxy verifier in an unattended run, your
`/s2tdd-verify-done` when attended. A red there that no per-wave run in the slice showed makes
the verdict Not done, naming the red test and the first wave commit where it alone goes red.

When verify-done's full run passed in full on a clean tree, its verification-log line ends
`· green at <sha>`. Converge and close reuse that run instead of running the suite again, when
`<sha>` is still `HEAD` and `git status --porcelain` prints nothing.

## A pytest recipe: pytest-testmon

[pytest-testmon](https://testmon.org/) records which code each test runs and, on the next run,
selects only the tests whose code changed since. It suits a per-wave command:

```text
Per-wave tests: .venv/bin/python -m pytest --testmon -q
Full suite: .venv/bin/python -m pytest
Per-wave sees: *.py
```

- **Add `--testmon-forceselect` whenever `-m` or `-k` narrows the run.** Without it, testmon
  turns its selection off when either is given and runs every test the marker or keyword
  allows. With a `slow` marker, for example:
  `Per-wave tests: .venv/bin/python -m pytest --testmon --testmon-forceselect -m "not slow" -q`.
- **Keep pytest's cache plugin.** testmon needs it, so the command must not pass
  `-p no:cacheprovider`.
- **Add `.testmondata` to `.gitignore`.** It is testmon's local database, rebuilt on any machine;
  a committed copy dirties the tree on every run.
- **`Per-wave sees: *.py`.** testmon traces Python code only. An edit to a prompt, a template, a
  fixture file or the project's config selects nothing, even when it turns a test red, so a wave
  that changes any of those runs the full suite.
- **Record a baseline first.** testmon's first run in a checkout runs every test and records
  them; run the per-wave command once on a clean tree before the first wave, so wave 1's run is
  already selective.

### Keep testmon out of the Full suite: line

The full suite is the run every gate trusts, so it runs every test, plainly. testmon collects
coverage while it runs, and in the trial behind this recipe that made every run 23–45% slower,
which the full suite would pay at every gate for nothing.

### Selecting tests by modified files

A lighter alternative to testmon is a per-wave command that runs only the test files git shows
as modified files (for example with a plugin such as pytest-picked). It sees no link between a
source file and its tests, so pair it with a narrow `Per-wave sees:` line, such as the test
directory alone.
