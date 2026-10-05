"""US4 acceptance tests for this repository's test rules (T019; II-14)."""

from __future__ import annotations

import re
from pathlib import Path

RT1 = "Outside an s2tdd run, `pytest tests` passes before a commit too"
RT2 = (
    "inside one, the wave rules decide the test run before a wave commit, and the full suite "
    "passes at slice ends, before merge and in CI"
)
RT3 = ("tools/build.py --check", "tools/check.py")
GONE = {
    "CLAUDE.md": "tools/build.py --check, tools/check.py and pytest tests pass before a commit",
    "CONTRIBUTING.md": "tools/build.py --check, tools/check.py and pytest tests pass (CI runs",
}
PER_WAVE_TESTS = (
    "pytest tests --ignore=tests/tools/test_eval_suite.py "
    "--ignore=tests/tools/test_eval_case_fixes.py"
)
FULL_SUITE = "pytest tests"
PER_WAVE_SEES = (
    "skills/*, agents/*, src/*, docs/*, tools/*, .claude/*, .claude-plugin/*, .github/*, "
    "tests/conftest.py, tests/acceptance/*, tests/agents/*, tests/commands/*, tests/docs/*, "
    "tests/shared/*, tests/tools/__init__.py, tests/tools/test_build.py, "
    "tests/tools/test_check.py, tests/tools/test_eval_graders.py, "
    "tests/tools/test_run_benchmark_counts.py, README.md, CHANGELOG.md, CLAUDE.md, "
    "CONTRIBUTING.md, MIGRATING.md, pyproject.toml, requirements-dev.txt"
)
FILES = ("CLAUDE.md", "CONTRIBUTING.md")


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _bullets(text: str) -> list[str]:
    """Top-level bullets, each with its continuation lines, flattened."""
    out: list[str] = []
    for line in text.split("\n"):
        if line.startswith("- "):
            out.append(line)
        elif out and line.startswith("  ") and line.strip():
            out[-1] += " " + line
        elif out and not line.strip():
            out.append("")
    return [_flatten(b) for b in out if b]


def _labelled(text: str, label: str) -> list[str]:
    """RR-1: the label starts the line after optional whitespace, case-insensitive; fenced
    lines count. Returns the rest of each matching line, verbatim (stripped)."""
    pat = re.compile(r"^\s*" + re.escape(label), re.IGNORECASE)
    return [ln.strip()[len(label):].strip() for ln in text.split("\n") if pat.match(ln)]


def test_003_us4_ac1_wave_rules_in_a_run(doc):
    """US4-AC1: **Given** an s2tdd run in this repository, **When** a wave commits, **Then**
    CLAUDE.md and CONTRIBUTING.md require `tools/build.py --check`, `tools/check.py` and the
    test run the wave rules name, not `pytest tests`.

    Provenance: 003 spec.md
    """
    for name in FILES:
        d = doc(name)
        assert not d.missing(RT2), f"{name} lacks RT2"
        assert not d.missing(*RT3), f"{name} lacks RT3"
        assert _flatten(GONE[name]) not in d.flat, f"{name} still holds its gone phrase"


def test_003_us4_ac2_full_suite_outside_a_run(doc, repo_root: Path):
    """US4-AC2: **Given** a commit outside an s2tdd run, **When** it is made, **Then** CLAUDE.md
    and CONTRIBUTING.md still require `tools/build.py --check`, `tools/check.py` and
    `pytest tests` to pass first.

    Provenance: 003 spec.md
    """
    for name in FILES:
        d = doc(name)
        assert not d.missing(RT1), f"{name} lacks RT1"
        text = (repo_root / name).read_text(encoding="utf-8")
        holding = [b for b in _bullets(text) if _flatten(RT1) in b]
        assert holding, f"{name}: no bullet holds RT1"
        assert all(_flatten(p) in holding[0] for p in RT3), f"{name}: RT3 not in RT1's bullet"


def test_003_us4_ac3_test_lines(repo_root: Path):
    """US4-AC3: **Given** this repository's CLAUDE.md, **When** harden reads it for the test
    commands, **Then** it finds a `Per-wave tests:` line and a `Full suite: pytest tests` line.

    Provenance: 003 spec.md
    """
    text = (repo_root / "CLAUDE.md").read_text(encoding="utf-8")
    tests = _labelled(text, "Per-wave tests:")
    assert len(tests) == 1, f"Per-wave tests: lines in CLAUDE.md: {len(tests)}"
    assert tests[0] == PER_WAVE_TESTS
    full = _labelled(text, "Full suite:")
    assert len(full) == 1, f"Full suite: lines in CLAUDE.md: {len(full)}"
    assert full[0] == FULL_SUITE
    sees = _labelled(text, "Per-wave sees:")
    assert len(sees) == 1, f"Per-wave sees: lines in CLAUDE.md: {len(sees)}"
    assert sees[0] == PER_WAVE_SEES
