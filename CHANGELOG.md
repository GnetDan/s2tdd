# Changelog

## 0.4.0 — unreleased

Unattended runs that end ready to close, and a test run per wave that fits the wave.

- **`--nobrakes` loops to ready to close**: when the last wave is verified, the run converges
  instead of stopping. The new `converger` agent type (opus, medium) runs `/s2tdd-converge`; when
  it appends tasks, the new `hardener` agent type (opus, high) hardens them in append mode and
  the run builds the new waves, with gates, before the next converge. Each round is a line under
  the ledger's new `## Rounds`. The loop stops when a round appends no fewer tasks than the one
  before, a gap comes back, or an appended task cites no scenario or requirement. A round that
  converges builds the docs wave and ends the summary with `READY TO CLOSE` and a Next block:
  pending checkpoints, the docs wave, `/s2tdd-pr-review` and `/s2tdd-close`, which the loop
  never runs. Hand-offs can resume at a converge, harden or docs-wave phase.
- **`--nobrakes once`** keeps 0.3.0's run: it stops when every task in scope is ticked.
- **One test run per wave**: a project names its commands in its agent guidance file with
  `Per-wave tests:`, `Full suite:` and the optional `Per-wave sees:` globs, and harden copies them
  into handoff.md's new `TEST RUN` section. After each wave the orchestrator runs the per-wave
  command as written, or the full suite when none is declared, when the wave changed a file
  outside `Per-wave sees:`, or once per-wave runs are off. Zero selected is green (`0 selected`);
  a run with no summary line turns per-wave runs off for the rest of the run. Every wave report
  names its run, command, counts and wall time, and harden writes implementation done-whens as
  "the wave's test run is green".
- **The full suite at slice ends**: every verify gate runs the `Full suite:` command, and a red
  no per-wave run showed is Not done, naming the first wave commit where that test goes red.
  Attended, your `/s2tdd-verify-done` is the slice's full run.
- **A green full run is reused**: verify-done's log line ends `· green at <sha>` after a full,
  green run on a clean tree, and converge and close reuse it while `HEAD` is still `<sha>` and
  the tree is clean.
- **License**: s2tdd is now Apache-2.0 (was MIT). The files adapted from spec-kit and
  mattpocock/skills keep their MIT notices in LICENSE.
- **Docs**: a new [Test runs](docs/test-runs.md) page with a pytest recipe (pytest-testmon),
  and this repository's own `Per-wave tests:` line.
- Features hardened before 0.4.0 run as before and stop when every task is ticked:
  /s2tdd-harden handoff refreshes their handoff.md for the converge loop and the per-wave run.
- Projects whose specs/WORKFLOW.md predates 0.4.0: delete it, and the next /s2tdd-specify,
  /s2tdd-epic or /s2tdd-constitution copies in the new one.

## 0.3.0 — 2026-10-04

What the first nobrakes pilot taught: a review of each wave's tests, every agent type on Opus,
and unattended runs that hand off by printing and stay within your usage.

- **The shape check**: before each wave commit, every wave that holds test packets gets one
  read-only review of those packets against the contract sections they cite, by
  `s2tdd:strong-diff-reviewer` with harden's new *Shape check* brief. A test packet that
  asserts a shape another packet or wave defines cites the contract section in its report, and
  the check flags a cross-wave shape with no citation. Attended, its findings are
  recommendations in the wave report; under `--nobrakes` they go back to the test packet before
  the commit, and what it does not confirm becomes an open review note. A handoff.md hardened
  before 0.3.0 runs as written: implement says so once, and `/s2tdd-harden handoff` refreshes it.
- **Every agent type runs on `opus`**, the tiers set by effort: `packet-cheap` low,
  `packet-medium` medium, `packet-strong` high, `strong-diff-reviewer` high, `proxy-verifier`
  medium.
- **A spec MUST breach is a blocker**, never a note: in `--nobrakes` the packet fixes it before
  the commit or is blocked; attended, it heads the wave report. verify-done gives Not done for
  a committed breach, and converge turns open review notes and carried constraints marked
  "carry to converge" into tasks, or cites what resolved them.
- **Red before green, checked in full**: verify-done reads the red run of every implementation
  packet report in the range, never a sample, and says how many it read. A missing red run is a
  gap; a task nothing shows red is Not done.
- **`--nobrakes` hands off by printing**: a relay prints the handoff prompt, sends a push
  notification where the harness can, and stops; it never starts a session as a scheduled task
  or in the background. The prompt points at the ledger's Carried constraints instead of
  restating them.
- **Usage limits per window**: `--nobrakes week=<n> five-hour=<n>` (defaults 95 and 90),
  recorded as Carried constraints. The week limit stops the run; the five-hour limit hands off
  at a clean boundary with the window's reset time in the prompt.
- **The Boundary line**: every `--nobrakes` wave report carries `Boundary: context <x>% ·
  five-hour <y>% · week <z>% · BRAKES <none|found> · ledger +<n> lines`, and verify-done flags a
  wave without it.
- **Wave order and gates**: each wave runs its reviews and shape check, then their fixes, then
  the full suite once. The proxy verifier runs in a scratch worktree at the gate's commit while
  the next wave starts; packets hold their test runs while its suite runs. Packets expect
  sibling packets' edits in the tree and rerun a red outside their own tests alone before
  reporting it. The Proxy verifier brief gains slots for expected-red rows and accepted
  deviations.
- **Harden's wave table**: no task shares a wave with a task that produces a contract section it
  cites; each superseded shape gets a search of the test tree, listed in orchestration.md; and
  orchestration.md and handoff.md must name no old command. The context budget note adds one
  shape-check hand-back per wave that holds test packets.
- **A leaner orchestrator**: implement finds old command names with `grep` instead of reading
  handoff.md and orchestration.md, reads only the handoff's prompt, one standard brief at a time
  and only the waves in scope, and says once, under *Harnesses without a mechanism*, what runs
  without a usage tool, push notifications or agent types.
- **Run benchmark**: a maintainer skill under `.claude/skills/run-benchmark/`, with
  `tools/run_benchmark_tokens.py`, measures a finished run's token use. It is not a shipped
  command.
- Projects whose specs/WORKFLOW.md predates 0.3.0: delete it, and the next /s2tdd-specify,
  /s2tdd-epic or /s2tdd-constitution copies in the new one.

## 0.2.0 — 2026-10-03

s2tdd: the workflow becomes a standalone plugin, renamed from a spec-kit preset and extension.

- **One Claude Code plugin**, `s2tdd`, installed with `/plugin marketplace add GnetDan/s2tdd`
  and `/plugin install s2tdd@s2tdd`; no spec-kit component and no `specify` CLI at any point.
  Copying `skills/` into a project's `.claude/skills/` is the documented fallback (use the
  plugin or the copy, never both). Cursor is supported best-effort.
- **13 commands, named `/s2tdd-<name>`**: epic, specify, clarify, plan, harden, implement,
  verify-done, converge, pr-review, close, next, foundation-review and constitution. The
  command merges: specify creates the branch (was `/speckit-branch`) and grills until the
  design is settled; harden generates `tasks.md` test-first before hardening it (was
  `/speckit-tasks`); `/s2tdd-implement --print` prints the filled prompt for another harness,
  model or window (was `/speckit-handoff`); next saves before it reports (was `/speckit-save`).
  Plan and constitution are forked from spec-kit's: research decisions are R-entries, and the
  constitution lives at `specs/constitution.md`. Analyze, checklist and taskstoissues are gone.
- **Agent types**: `packet-cheap`, `packet-medium`, `packet-strong`, `strong-diff-reviewer` and
  `proxy-verifier`, each with its own model and effort; implement dispatches packets and its
  unattended stand-ins to them, so a lower-effort orchestrator no longer lowers its packets.
- **First-run setup** replaces `/sdd-init` and `specify init`: the first `/s2tdd-specify`,
  `/s2tdd-epic` or `/s2tdd-constitution` in a repository offers to clone or create the specs
  repository, copies `specs/README.md` and `specs/WORKFLOW.md` in when missing, and appends the
  local excludes (`specs/`, `.sdd-run/`, plus `.claude/skills/s2tdd-*/` in a repository you
  don't own). It only adds; it never deletes or rewrites a file.
- **Feature resolution without scripts**: every command finds the active feature (and epic)
  from the feature you name, else the branch, else by asking, with no pointer file, and uses the main worktree's `specs/`
  when run from a git worktree. Every command except next ends by running `/s2tdd-next` as
  plain text, with no hooks. Templates are bundled inside the commands that use them.
- **Test upkeep**: the workflow guide's new section, with its sources. verify-done and converge
  record suite wall time against the project's budget, converge adds a test-upkeep task when
  over, and foundation-review and close list duplicate or obsolete tests as findings.
- **`/s2tdd-next` Watch out** also lists merged feature branches with the commands to delete
  them, a suite over budget, spec-kit leftovers, and a project copy of the skills that shadows
  the plugin. The README recommends turning on automatic deletion of head branches.
- **`/s2tdd-implement --nobrakes`** reads its usage from the `get_usage` tool in Claude Code,
  never an estimate. `--nobrakes`'s hand-off to a fresh session (including the scheduled-task
  start) and its brakes are carried over from the preset but untried in the field.
- **The build and CI**: the shared rules have one source each under `src/shared/`;
  `tools/build.py` stamps them into the commands, which are committed, and `tools/check.py`
  checks frontmatter, the command set, placeholders, old names, bundled files, credits and
  the manifests. CI rebuilds and fails on any difference, then runs the checker and the tests.
- **Migration**: [MIGRATING.md](MIGRATING.md) moves a spec-kit project, with or without the
  preset, to s2tdd; the README's "Coming from spec-kit" section and
  [docs/coming-from-spec-kit.md](docs/coming-from-spec-kit.md) cover plain spec-kit users. A
  feature hardened under the old names needs `/s2tdd-harden handoff` once, and implement stops
  until it has run. The feature layout (`specs/NNN-name/`) is unchanged.
- **`/s2tdd-next`'s save** also commits `specs/constitution.md` when it is new or changed.
- **`/s2tdd-pr-review --cloud`** states the local specs repository's URL before the move, so
  the cloud session clones it and runs the spec half without `--specs-repo`. Only the review
  runs in the cloud; every other command runs locally.
- **An eval suite** under `evals/`: one case per scenario that needs a live model, run with
  `claude plugin eval . --scaffold --allow-tools Bash Write Edit --max-cost-usd 20 --threshold 1.0`
  on Linux, macOS or WSL. Its shape is tested everywhere; the live run is not a release gate.
- The spec-kit preset and extension packaging (`preset/`, `extension/`) is removed.
- The release zips and their packaging script are gone; a release tags the repository and
  bumps `.claude-plugin/plugin.json`.

## 0.1.0 — unreleased

First public version.

- The chain: `/speckit-epic`, `/speckit-branch` (before specify), `/speckit-clarify`,
  `/speckit-harden` (with an append mode for converge's gap tasks), `/speckit-implement`,
  `/speckit-handoff`, `/speckit-verify-done`, `/speckit-converge`, `/speckit-pr-review`,
  `/speckit-close`, `/speckit-foundation-review`, and BDD spec, plan and tasks templates.
- `/speckit-next` ends every step (via the extension's `after_*` hooks) with the next step as a
  ready-to-paste prompt, and recaps where a feature stands when run on its own. `/speckit-save`
  runs just before it and commits and pushes the feature's files in the specs repository.
- `validation.md`'s verification log records verify-done, converge and pr-review results;
  close requires a converge after the last wave.
- `/speckit-pr-review` reports by default; `--fix` fixes, pushes and posts.
- `/speckit-implement --nobrakes` runs several slices unattended: a proxy verify-done at each
  slice end, a read-only reviewer for each strong packet's diff, a third attempt then a block
  for a failing packet, pending blocks for live checkpoints, tags and pushes in both
  repositories, and a handoff to a fresh session before the context is half full. The rules
  live in handoff.md's NOBRAKES section and *Standard briefs*; the state in `run-ledger.md`.
  `/speckit-harden handoff` refreshes an older feature's handoff.md.
- Packets report by exception (a card listing only what the orchestrator must act on; the full
  report on disk), wave reports go to `s<k>-wave-reports.md` and verify-done reads them by path.
  New ground rules: an amendment rubric, test-owner fixes, ownership exceptions, amended
  expected red, targeted tests in packets, process sweeps, secrets by name only.
- Requires spec-kit 0.16.3 or later.
