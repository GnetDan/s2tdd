# The SDD workflow: BDD specs → ATDD/TDD implementation → tests as the documentation

Living page. The executable definition is the
[s2tdd plugin](https://github.com/GnetDan/s2tdd); the
normative rules are in the project's constitution, [`specs/constitution.md`](constitution.md).
Specs are intent records ([`specs/README.md`](README.md)); the tests a feature leaves behind
are its documentation.

## The loop

| Step | Command | Produces |
|---|---|---|
| Constitution (once per project, amended as needed) | `/s2tdd-constitution` | `specs/constitution.md`: the project's normative rules, created by grilling or amended with a version bump and a dated change note |
| Review (hardening only) | `/s2tdd-foundation-review` | measured findings + SC baselines |
| Epic (large or unclear work only) | `/s2tdd-epic` | `specs/epics/<slug>/`: a map of decision tickets resolved one per session (research in parallel), then one seed per feature spec for `/s2tdd-specify`; frozen once those specs exist |
| Specify | `/s2tdd-specify` (creates the branch first) | the `NNN-short-name` branch, then `spec.md` — stories and edge cases as **Given/When/Then scenarios with stable IDs** (`US1-AC2`, `EC-003`) |
| Clarify | `/s2tdd-clarify` | a grilling session, no question cap: rounds with recommended answers until the design tree is resolved or you say "enough"; answers folded into the spec (new scenarios take the next free ID, terms go in Key Entities/Terminology, hard-to-reverse decisions become `research.md` R-entries) |
| Plan | `/s2tdd-plan` | `plan.md`, `research.md`, `contracts/`, `quickstart.md`; names where acceptance tests live and which scenarios are checkpoints |
| Harden | `/s2tdd-harden` | `tasks.md` (generated test-first when missing, else rewritten test-first); every scenario mapped (`**Scenarios**:` line); pinned seams + judgments; `orchestration.md`, `handoff.md`, `validation.md` |
| Implement | `/s2tdd-implement` in a fresh session (fills `handoff.md` and orchestrates the next slice); `--nobrakes` runs the rest of the feature unattended, through converge to ready-to-close (below); `/s2tdd-implement --print` prints the same prompt for another harness | code, red→green, a shape check of each wave's test packets, wave commits, `s<k>-wave-reports.md` |
| Verify | `/s2tdd-verify-done reports: <the wave-reports file>`, in a fresh session (a proxy subagent does it in an unattended run) | verdict per claim (ticks, diff, test ownership, real suite run, invariant checks) on the committed waves, recorded in `validation.md`; gaps become a corrective wave |
| Converge | `/s2tdd-converge` once every task is ticked (unticked `CHECKPOINT` tasks wait for close); in an unattended run a converger agent runs it, round by round | remaining gaps as tasks (hardened by `/s2tdd-harden`'s append mode, then implemented), or a `converged` record; runs the acceptance suite; cited deviations are `superseded`, not gaps |
| PR | push the branch and open a pull request | |
| Review | `/s2tdd-pr-review <PR>` | the PR reviewed against its spec and as an outside reviewer, every finding verified; a hitlist (`--fix` fixes confirmed findings test-first and posts it) |
| Close | `/s2tdd-close` (needs a converge after the last wave; stops while the docs wave a run built is still uncommitted) | `close-out.md`; spec stamped `Closed`; the directory freezes. Then merge |

Every step ends by running `/s2tdd-next`, which commits and pushes the feature's spec files,
and `constitution.md` when it is new or changed (when `specs/` is its own repository), reads them and prints the next step as a ready-to-paste
prompt (with any context the next session needs, and whether it belongs in a fresh session).
Run it yourself any time to get oriented after a break.
`validation.md`'s `## Verification log` records each verify-done, converge and pr-review, so it
can tell where the feature stands.

## The rules that make tests the documentation

- One acceptance test per scenario, in the acceptance directory (e.g. `tests/acceptance/`), in a
  file named by capability (never by feature number), named `test_<NNN>_us<n>_ac<m>_<slug>`
  (or the runner's equivalent), scenario text verbatim in the description plus `Supersedes:` /
  `Superseded by:` provenance. A scenario that needs a live
  service (a live model, the network) is a **scripted** checkpoint: fixed inputs in a script
  the implementer or orchestrator runs, with no human. A **human** checkpoint is only for
  a step that needs a person (a verdict on feel or quality, open-ended exploration, a UX or
  design call), one
  that benefits heavily from the user interacting before work proceeds, or, rarely, a
  critical control gate where missing something would cost far more than the manual check.
  No human checkpoint repeats inputs a script can play, and no rule forces a live
  re-recording of scripted inputs. Both kinds are recorded in `validation.md`,
  never faked.
- **Three roles, three contexts.** The orchestrator dispatches and decides — it never
  implements (handoff STEP 0 makes it report `Subagents: yes/no`; without subagents it runs
  one packet per session, never the whole feature in one window). Test packets own `tests/**`.
  Implementation packets own their `src/**` files and never touch tests. **One live writer per
  file, across sessions**: the orchestrator preflights a packet's owned files (`git status
  --short`) before dispatching — unexpectedly dirty means a stale packet or another session
  holds it, so stop rather than race it; cancel the old packet first, and when resuming an
  interrupted one, state the baseline to keep rather than re-derive.
- **Agent types.** Implement dispatches each packet and each wave's shape check, and in an
  unattended run the strong-diff read and the proxy verifier, as s2tdd's own agent types (a
  copy of the skills without the plugin falls back to a general subagent), and every agent
  type runs on Opus: packets at low, medium or high effort by tier, the strong-diff reviewer at
  high and the proxy verifier at medium. In an unattended run that loops to ready-to-close, the
  converger (medium) and the hardener (high) stand in for converge and harden's append mode. The plugin's
  [Models and budget](https://github.com/GnetDan/s2tdd/blob/main/docs/models.md) page has the
  table.
- **Red-test protocol.** A red acceptance test is an implementation defect until the
  orchestrator rules otherwise. A ruling is one line — `Decision: <test> diverges per <spec>
  <scenario>; Supersedes …` — and then the *test owner* rewrites the scenario and test (red
  against the old behavior) before the implementer makes it green. A test changed in the same
  step as the code that failed it is a violation. A red test no open spec supersedes is a
  breaking change: stop and surface it. A hygiene guard in the acceptance suite (the project
  writes one, e.g. `tests/acceptance/test_hygiene.py`) forbids skipped or expected-to-fail
  acceptance tests and enforces the description shape.
- **Red before green, always.** Test task first, failing for the expected reason (quoted),
  then the implementation task whose done-when is "that test passes and the wave's test run is
  green". No task writes and passes the same test.

## Test upkeep

s2tdd links a trusted source only where it follows that source's advice and the advice works
for this workflow. Everything else (test style, mocking philosophy, coverage targets, the test
pyramid) is left to the project.

| Topic | What s2tdd does | Link |
|---|---|---|
| Suite speed | The project states a suite-time budget in its agent guidance file; verify-done and converge record the wall time; over budget shows under `/s2tdd-next`'s Watch out, and converge adds a test-upkeep task (it surfaces, it doesn't block); packets run targeted tests, with one test run per wave: the project's per-wave command, the full suite at slice ends. The agent guidance file names them on its `Per-wave tests:`, `Full suite:` and `Per-wave sees:` lines, which the plugin's Test runs page explains (linked under *Unattended runs* below) | *Software Engineering at Google* ch. 11, Adam Bender, "Testing Overview" ([test size](https://abseil.io/resources/swe-book/html/ch11.html#test_size), [the pitfalls of a large test suite](https://abseil.io/resources/swe-book/html/ch11.html#the_pitfalls_of_a_large_test_suite)); for pytest projects, [`--durations`](https://docs.pytest.org/en/stable/how-to/usage.html#profiling-test-execution-duration) and [a `slow` marker with `--runslow`](https://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option) |
| Determinism and flakes | Seeded randomness and a wrapped clock; a red that passes when run alone goes to flake diagnosis before any re-dispatch; a test is never skipped or quarantined to get green | Martin Fowler, ["Eradicating Non-Determinism in Tests"](https://martinfowler.com/articles/nonDeterminism.html), for its causes and fixes, **not** its quarantine advice; Kent Beck, ["Test Desiderata"](https://testdesiderata.com/), as a checklist for the reader to weigh |
| Fixtures and platforms | Fixtures checked by their bytes get `eol=lf` in `.gitattributes`; processes are killed only by PID plus start time plus command line; harden carries the platform notes | Git documentation, ["gitattributes", `eol`](https://git-scm.com/docs/gitattributes#_eol) |
| Over-specified tests | The test-owner fix (ground rule 14 in the feature's `orchestration.md`) | *SWE at Google* ch. 12, Erik Kuefler, ["Unit Testing"](https://abseil.io/resources/swe-book/html/ch12.html#preventing_brittle_tests) (preventing brittle tests); ch. 13, Andrew Trenk and Dillon Bly, ["Test Doubles"](https://abseil.io/resources/swe-book/html/ch13.html#avoid_overspecification) (avoid overspecification) |
| Pruning | foundation-review and close list duplicate or obsolete tests as findings; retiring one is a later spec's `Supersedes` decision, carried out by a test packet, and never a way to get green | *SWE at Google* ch. 11, ["refactor slow or marginal tests"](https://abseil.io/resources/swe-book/html/ch11.html#the_pitfalls_of_a_large_test_suite) |

**Not linked:** Google Testing Blog, "Flaky Tests at Google and How We Mitigate Them" (John
Micco, 2016). It relies on reruns and auto-quarantine, which s2tdd forbids, and the post itself
warns that quarantine can mask a real race condition.

## Unattended runs (`/s2tdd-implement --nobrakes`)

One command runs the rest of a hardened feature with nobody watching, over as many sessions as
it takes. When the last wave is verified, the run carries on through converge to ready-to-close:
a converger agent runs `/s2tdd-converge`, a hardener agent hardens any tasks it appends, the run
builds them, and the rounds repeat until a converge comes back clean. A round that appends no
fewer tasks than the one before, brings a gap back or appends a task that cites no scenario stops
the run for you. A converged run builds the docs wave and ends `READY TO CLOSE`, with the steps
left to you: pending checkpoints, the docs wave, `/s2tdd-pr-review` and `/s2tdd-close`.
`/s2tdd-implement --nobrakes once` skips the loop and stops when every task is ticked. Subagents stand in
for the steps that wait on a person only where a later check can catch their mistakes: a proxy
`/s2tdd-verify-done` at each slice end (and before every handoff), and a read-only reviewer for
each strong packet's diff before its wave commit. Every run, attended or not, also gives each
wave that holds test packets a shape check before its commit: a read-only reviewer reads the
test packets against the contract sections they cite. Attended, its findings are recommendations
in the wave report; unattended, they go back to the test packet before the commit. A finding
that breaks a spec MUST is a blocker in both. A packet that fails its fence twice gets one more
attempt a notch up, then is blocked; its dependents are skipped and independent waves go on.
Live checkpoints become `PENDING SCRIPTED RUN` blocks; the docs wave is built and checked but
left uncommitted. Each wave runs the project's per-wave test command once, and every verify gate
runs the full suite; the plugin's
[Test runs](https://github.com/GnetDan/s2tdd/blob/main/docs/test-runs.md) page has the three
lines and a pytest recipe. After each verified slice, matching annotated tags go into both repositories
and both are pushed (never forced). Before the context passes half full, the session verifies
what it has, prints a short handoff prompt, sends a push notification where the harness can, and
stops: you paste the prompt into a fresh session, and no relay ever starts one by itself. Usage
limits are set at the start (`--nobrakes week=<n> five-hour=<n>`, defaults 95 and 90): the week
limit stops the run, the five-hour limit hands off with the window's reset time. After each wave
commit the run writes a `Boundary:` line (context, five-hour and week usage, BRAKES, ledger
lines) into the wave report. The rules are in the feature's `handoff.md` (NOBRAKES and *Standard
briefs*); the running state is in `run-ledger.md`, so every session resumes from files. It stops
the run, with a summary, on a blocked MVP or guard packet, a dirty owned file, a contract change
under committed code, a secret in any output, or the verifier failing twice. Ask for brakes in
chat (or create `.sdd-run/<NNN>/BRAKES`) and it finishes the wave and hands the next verify back
to you.

Packets report **by exception**: the full report goes to `.sdd-run/<NNN>/reports/` (excluded
from git, then appended to `s<k>-wave-reports.md`), and the orchestrator gets a card listing
only what it must act on. This holds for attended runs too.

## Human decisions (everything else is dispatchable)

Epic destinations and grilling/prototype tickets · clarify answers · human checkpoints (a verdict on feel or quality,
open-ended exploration, a UX or design call, a critical control gate; scripted checkpoints are dispatchable) · tier and fence policy · `Decision:` rulings on red tests · the close-out gate (drop vs deliver, reference audit). An unattended run never takes these, and never merges, runs a live checkpoint, uses a credential, commits the docs wave, or runs `/s2tdd-pr-review` or `/s2tdd-close`.

## Install and updates

Install the s2tdd plugin; see the package [README](https://github.com/GnetDan/s2tdd#install).
The first `/s2tdd-specify`, `/s2tdd-epic` or `/s2tdd-constitution` in a repository runs first-run
setup: it finds or creates the `specs/` directory and copies this page and the README into it
when they are missing. Updating the plugin updates the commands; the copies in `specs/` are
yours, and setup never rewrites an existing file.
