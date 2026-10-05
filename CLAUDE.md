# s2tdd

The source of the s2tdd Claude Code plugin. Read [CONTRIBUTING.md](CONTRIBUTING.md) before
changing anything: how a change is made, the naming rule, releasing, and what not to do while a
pilot project's run uses the installed plugin. Layout, build, checks and evals:
[docs/developing.md](docs/developing.md).

Invariants:

- Never name a pilot project in this repository: files, tests, evals, branches, commit messages.
- Never push or merge to `main`, update the installed s2tdd plugin, or run `claude plugin eval`
  while a pilot's unattended run uses the plugin.
- Fenced shared text is edited in `src/` and stamped with `tools/build.py`; never by hand.
- `tools/build.py --check` and `tools/check.py` pass before every commit, under `.venv`.
  Outside an s2tdd run, `pytest tests` passes before a commit too; inside one, the wave rules
  decide the test run before a wave commit, and the full suite passes at slice ends, before
  merge and in CI.

Test commands (s2tdd reads these lines; run them under .venv):

```text
Per-wave tests: pytest tests --ignore=tests/tools/test_eval_suite.py --ignore=tests/tools/test_eval_case_fixes.py
Full suite: pytest tests
Per-wave sees: skills/*, agents/*, src/*, docs/*, tools/*, .claude/*, .claude-plugin/*, .github/*, tests/conftest.py, tests/acceptance/*, tests/agents/*, tests/commands/*, tests/docs/*, tests/shared/*, tests/tools/__init__.py, tests/tools/test_build.py, tests/tools/test_check.py, tests/tools/test_eval_graders.py, tests/tools/test_run_benchmark_counts.py, README.md, CHANGELOG.md, CLAUDE.md, CONTRIBUTING.md, MIGRATING.md, pyproject.toml, requirements-dev.txt
```
