"""Tests for two eval-case fixes from the PR review of 002 (II-18j; II-16 for the case shape).

EC-002 runs an attended W0 in a one-prompt eval with no user to read a strong packet's diff, so
its scaffold demotes P0c from ``strong`` to ``medium`` in orchestration.md's W0 row, as the
sibling cases do; otherwise the run stops before the W0 commit. EC-003's grader 05 counts an
escalated P1b briefing as carrying the failures when it quotes any guard failure line, the
summary line ``check_quoting: <n> of <m> cases failed`` included, not only ``check_quoting: FAIL``.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

EC_002 = "evals/implement/002-EC-002-old-handoff-note"
EC_003_GRADER_05 = ("evals/implement/002-EC-003-escalation-raises-effort/graders/"
                    "05-escalation-carries-the-failures.md")


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    assert match, f"{path}: no frontmatter"
    loaded = yaml.safe_load(match.group(1))
    assert isinstance(loaded, dict), f"{path}: frontmatter is not a mapping"
    return loaded


def _bash_exe() -> str:
    found = shutil.which("bash")
    if found and "system32" not in found.lower():  # not the WSL launcher
        return found
    for candidate in (r"C:\Program Files\Git\bin\bash.exe",
                      r"C:\Program Files\Git\usr\bin\bash.exe"):
        if Path(candidate).is_file():
            return candidate
    if found:
        return found
    pytest.fail("bash not found on PATH")


def _env(tmp_path: Path) -> dict[str, str]:
    """No inherited git identity and no signed-in gh: a scaffold sets what it needs itself."""
    home = tmp_path / "home"
    home.mkdir()
    (home / "gitconfig").write_text("", encoding="utf-8")
    gh_config = tmp_path / "gh-config"
    gh_config.mkdir()
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k not in ("GH_TOKEN", "GITHUB_TOKEN",
                                                       "GH_ENTERPRISE_TOKEN",
                                                       "GITHUB_ENTERPRISE_TOKEN")}
    env.update(HOME=str(home), USERPROFILE=str(home), GIT_CONFIG_GLOBAL=str(home / "gitconfig"),
               GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", GH_CONFIG_DIR=str(gh_config))
    return env


# ------------------------------------------------------------------------ EC-002 (A5-1)


def test_ec_002_scaffold_leaves_no_strong_packet_in_w0(repo_root, tmp_path):
    script = repo_root / EC_002 / "scaffold.sh"
    work = tmp_path / "work"
    work.mkdir()
    proc = subprocess.run([_bash_exe(), script.as_posix()], cwd=work, env=_env(tmp_path),
                          capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert proc.returncode == 0, f"EC-002 scaffold exited {proc.returncode}: {proc.stderr}"
    orchestration = work / "specs" / "004-csv-export" / "orchestration.md"
    w0_rows = [line for line in orchestration.read_text(encoding="utf-8").splitlines()
               if re.match(r"^\| W0[^|]*\|", line)]
    assert w0_rows, "orchestration.md has no W0 rows"
    strong = [row for row in w0_rows if "| strong |" in row]
    assert not strong, f"W0 still holds a strong packet: {strong}"


def test_ec_002_scaffold_guards_a_strong_w0_row(repo_root):
    text = (repo_root / EC_002 / "scaffold.sh").read_text(encoding="utf-8")
    assert "orchestration.md: W0 still holds a strong packet" in text


# ------------------------------------------------------------------------ EC-003 (A5-3)


def _agent_input(subagent_type: str, prompt: str) -> str:
    """An Agent call's input as the eval runner serializes it for ``input_match``."""
    return json.dumps({"description": "Implement P1b", "prompt": prompt,
                       "subagent_type": subagent_type}, separators=(",", ":"))


def _violates(repo_root: Path, subagent_type: str, prompt: str) -> bool:
    grader = _frontmatter(repo_root / EC_003_GRADER_05)
    assert grader.get("type") == "tool_used" and grader.get("tool") == "Agent"
    assert grader.get("max") == 0
    return bool(re.search(grader["input_match"], _agent_input(subagent_type, prompt)))


BRIEF = ("Packet P1b (T005, quoting.py), escalated one tier. Read "
         "specs/004-csv-export/orchestration.md and the earlier attempts' reports "
         ".sdd-run/004/reports/P1b.md, P1b-2.md.\n")


def test_grader_05_accepts_the_guard_summary_line(repo_root):
    prompt = BRIEF + "The guard printed:\ncheck_quoting: 5 of 14 cases failed\n"
    assert not _violates(repo_root, "s2tdd:packet-medium", prompt)


def test_grader_05_accepts_the_guard_fail_line(repo_root):
    prompt = BRIEF + "The guard printed:\ncheck_quoting: FAIL (3 cases)\n"
    assert not _violates(repo_root, "s2tdd:packet-medium", prompt)


def test_grader_05_counts_a_medium_briefing_without_the_failures(repo_root):
    assert _violates(repo_root, "s2tdd:packet-medium", BRIEF)


def test_grader_05_spares_a_cheap_briefing(repo_root):
    assert not _violates(repo_root, "s2tdd:packet-cheap", BRIEF)


def test_grader_05_prose_says_any_guard_failure_line_counts(repo_root):
    text = (repo_root / EC_003_GRADER_05).read_text(encoding="utf-8")
    body = text.split("\n---", 2)[-1]
    assert "check_quoting: 5 of 14 cases failed" in body or "cases failed" in body
