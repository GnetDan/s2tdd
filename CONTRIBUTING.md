# Contributing to s2tdd

How work is done in this repository, for people and for agent sessions. The build, the checks,
the eval suite and the layout are in [docs/developing.md](docs/developing.md); this page holds
the rules around them.

## How a change is made

s2tdd is built with s2tdd. A change starts as a feature in the specs repository
(`GnetDan/s2tdd-specs`, cloned into `specs/` and excluded from this repository's git), on a
branch `NNN-short-name`: `/s2tdd-specify` → `/s2tdd-clarify` → `/s2tdd-plan` →
`/s2tdd-harden` → `/s2tdd-implement` → `/s2tdd-verify-done` → `/s2tdd-converge` →
`/s2tdd-pr-review` → `/s2tdd-close`, then the pull request is merged. Small fixes outside a
feature still go test-first, on a branch, through a pull request.

- **Test-first.** The commands are Markdown; their rules are pinned by text tests under
  `tests/` before the text is written. A change that breaks a test changes the test only when a
  spec says the old behaviour is superseded, and cites it.
- **Fenced text has one source.** Text between `<!-- s2tdd:shared … -->` fences, and the project
  pages under `skills/*/pages/`, are stamped by `tools/build.py` from `src/`. Edit `src/`, then
  rebuild; never edit a stamped copy.
- **Before a commit:** `tools/build.py --check` and `tools/check.py` pass, always. Outside an
  s2tdd run, `pytest tests` passes before a commit too; inside one, the wave rules decide the
  test run before a wave commit, and the full suite passes at slice ends, before merge and in
  CI (CI runs all three).
- **Use the project's `.venv`** (`.venv/Scripts/python` on Windows, `.venv/bin/python`
  elsewhere); a bare `python` may lack the dev requirements.

## Names

This repository never names a project s2tdd is piloted on: no file, test, fixture, eval case,
branch or commit message. Say "the first nobrakes pilot", "a pilot project", or use the
neutral fixture names (`acme`, `globex`, `004-csv-export`). The specs repository may name
pilot projects; that is where pilot evidence lives.

## Releasing

Development happens in a private repository, `GnetDan/s2tdd-dev`; the maintainer's own `s2tdd`
marketplace points at it, so **merging to its `main` is publishing to the maintainer**. The
public `GnetDan/s2tdd` gets a cleaned snapshot of `main` now and then, as one new commit; anyone
who installs the plugin from there gets it at that snapshot.
A release bumps `version` in `.claude-plugin/plugin.json` and adds its `CHANGELOG.md` section
in the feature that makes it; the merge and the GitHub release follow, when nothing depends on
the version installed today.

## Working while a pilot run uses the installed plugin

A pilot project may be running an unattended `/s2tdd-implement --nobrakes` on the installed
plugin while this repository changes. Nothing done here may change what that run sees or
starve it. While one is live:

- **Never push or merge to `main`**, and never update, reinstall or uninstall the s2tdd plugin
  or its marketplace. The installed plugin is a cached copy of a `main` commit; feature
  branches and tags here do not reach it.
- **Never run `claude plugin eval`**: it loads plugins. Eval runs wait until the pilot's run
  ends (they also need Linux, macOS or WSL).
- **Read the pilot project read-only.** No edits, no state-changing git there.
- **Share the plan's usage windows.** Both runs draw on the same five-hour and weekly windows,
  and the pilot's run has the stop line its ledger records (for example, the weekly window at
  99%). A run here leaves it room: it hands off at 70% of the five-hour window and at 90% of
  the weekly one, with the window's reset time in the handoff prompt, and resumes after the
  reset.
- **Share the CPU.** The pilot's tests may be timing-sensitive. Run every pytest at below-normal
  priority, which its child processes inherit (Windows):

  ```bash
  .venv/Scripts/python -c "import ctypes as c,sys,pytest; k=c.windll.kernel32; k.GetCurrentProcess.restype=c.c_void_p; k.SetPriorityClass.argtypes=[c.c_void_p,c.c_uint]; k.SetPriorityClass(k.GetCurrentProcess(),0x4000); sys.exit(pytest.main(sys.argv[1:]))" tests
  ```

  (the arguments after the script are pytest's, as with `python -m pytest`). Before a full
  suite, wait while another project's pytest runs (PowerShell:
  `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object CommandLine -match pytest`),
  up to 15 minutes; then run anyway and note it.
- **Relays print their handoff prompt and stop.** Never start a session with a scheduled task,
  a routine or a background `claude -p`: an unseen permission prompt stalls it.

When the pilot's run ends, these rules lapse; the merge and release can go ahead.
