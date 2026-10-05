# Developing s2tdd

[← Back to the README](../README.md)

## What's in the repository

| Path | What it holds |
|---|---|
| `skills/` | The 13 commands, one folder each (`skills/s2tdd-<name>/SKILL.md`), with the templates and project pages they use bundled beside them |
| `agents/` | The seven agent types |
| `evals/` | The eval suite: the cases that run the commands in a real session |
| `.claude-plugin/` | The plugin manifest and the marketplace listing |
| `src/` | The sources the build stamps into the commands. `src/shared/` holds the rules every command needs (feature resolution, worktrees, first-run setup, the closing next step); `src/pages/` holds the two project pages |
| `tools/` | The build and the checker, used in development and CI only, and the run benchmark's token script |
| `.claude/skills/` | Maintainer skills for working in this repository; the plugin does not ship them |
| `tests/` | The acceptance, command, agent-type, shared-rule, docs, eval-suite and tool tests |
| `docs/` | These pages |

## Build, check, test

The shared rules have one source each, in `src/shared/`. `tools/build.py` stamps them into
every command that holds a `<!-- s2tdd:shared <block> -->` fence, and copies the bundled files
`src/bundle.toml` lists. The stamped files are committed, because plugins install from git.

**Never hand-edit fenced text.** Edit the source and rebuild.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt   # .venv/Scripts/ on Windows
.venv/bin/python tools/build.py                 # stamp shared rules and bundled files
.venv/bin/python tools/check.py                 # frontmatter, command set, placeholders, old names, bundled files, credits, manifests
.venv/bin/python -m pytest tests
```

The tools need Python 3.11 or newer.

Inside an s2tdd run, each wave runs the per-wave command from `CLAUDE.md`'s `Per-wave tests:`
line, which leaves out the two slow eval-scaffold test files, and the full suite runs at slice
ends, before merge and in CI. [Test runs](test-runs.md) explains the three lines.

**CI** (`.github/workflows/ci.yml`) runs on every pull request and on pushes to `main`:
`tools/build.py --check` fails on any difference between the sources and the stamped files,
then `tools/check.py` and the test suite run.

## The eval suite

`evals/<area>/<ID>-<slug>/` holds one case per scenario that needs a live model, named by the
scenario's ID (`US6-AC6`, `EC-001`).

| File | What it is |
|---|---|
| `prompt.md` | The case. Its frontmatter `description` is the scenario text verbatim |
| `graders/*.md` | What the run is graded on |
| `case.yaml` | Only for a case that needs a project to run in. Its only content is `context.scaffold_script`, naming a script inside the case directory |

`evals/fixtures/` holds the bash helpers those scripts share. No case sets `env` (the runner
takes only `EVAL_*` names there), so the case that needs a cloud session runs as
`CLAUDE_CODE_REMOTE=true claude -p "/s2tdd-pr-review 1"`.

```bash
claude plugin eval . --scaffold --allow-tools Bash Write Edit --max-cost-usd 20 --threshold 1.0
```

- The runner refuses cases that grant Bash on Windows, so run the suite on Linux, macOS or WSL.
- `tests/tools/test_eval_suite.py` checks the cases' shape and runs anywhere.
- The suite costs real money and is not a gate for 0.2.0; run it when a command changes.

## The run benchmark

To judge what a workflow change did, compare two consecutive features' implement runs in a
project that uses s2tdd. `.claude/skills/run-benchmark/SKILL.md` is a maintainer skill: Claude
Code offers it as `/run-benchmark` in a clone of this repository, and the installed plugin does
not. It reads the project's feature directories and session transcripts read-only, and writes
its report to the project's own specs repository, never to this one.

`tools/run_benchmark_tokens.py` gives the skill its token and time figures from the
transcripts. It only reads:

```bash
python -X utf8 tools/run_benchmark_tokens.py ~/.claude/projects/C--Git-acme find 003 wave
python -X utf8 tools/run_benchmark_tokens.py ~/.claude/projects/C--Git-acme session <id-prefix>
```

## Releasing

Bump `version` in `.claude-plugin/plugin.json`, tag the release, and write the GitHub release
notes from [CHANGELOG.md](../CHANGELOG.md).
