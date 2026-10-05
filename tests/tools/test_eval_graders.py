"""Tests that the eval suite's graders and fixtures decide what the run did (II-14).

A grader over the whole trace also reads the skill text the Skill tool injects, so a pattern
the skills already contain passes (or, for an absence guard, fails) whatever the agent did.
Absence guards must spare the read-only commands the skills run. Spec-content graders read the
spec the run wrote, not the template it starts from. Fixture remotes carry an owner segment
after a host segment, as first-run setup reads it, and the cases whose Given is "a repository
the user owns" refuse to run while `gh` answers with another account, because setup asks `gh`
before `git config github.user`.
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

# The setup cases whose Given is a repository the user owns (acme's remote, acme's account).
OWN_REPOSITORY_SETUP_CASES = (
    "setup/US1-AC2-offers-specs-repo",
    "setup/US1-AC6-constitution-pointer",
    "setup/EC-007-setup-silent",
    "setup/EC-008-old-page-left",
)

# Graders that check the content of the spec the run drafts.
SPEC_CONTENT_GRADERS = (
    "specify/US1-AC5-gaps-and-grilling/graders/many-gaps-marked.md",
    "specify/US1-AC4-next-number-branch/graders/given-when-then.md",
    "specify/US1-AC4-next-number-branch/graders/scenario-ids.md",
)

FOREIGN_GUARD = "setup/US1-AC3-foreign-no-footprint/graders/no-tracked-file-touched.md"

# Commands a correct run makes: /s2tdd-next's gather step, specify's branch step and next's save
# in the specs repository. No absence guard may count them.
READ_ONLY_AND_SPECS_COMMANDS = (
    "git stash list",
    "git status --short",
    "git status --porcelain",
    'git log -15 --date=relative --format="%h %ad %s"',
    "git worktree list",
    "git branch -a --format='%(refname:short)'",
    "git rev-parse --is-inside-work-tree",
    "git switch -c 005-pin-notes",
    "git -C specs add -A",
    'git -C specs commit -m "docs(005-pin-notes): draft spec"',
    "cat docs/sdd-workflow.md",
)

# What a run must not do in a foreign repository: edit or stage what the project tracks.
PROJECT_EDITS = (
    "git add README.md",
    "git commit -am wip",
    "git stash",
    "git stash push -m wip",
    "git checkout -- README.md",
    "git reset --hard",
)

FILLED_SPEC = """# Feature Specification: Note sharing

## User Scenarios

- **US1-AC1**: **Given** a note owned by Ana, **When** she shares it with Ben, **Then** Ben sees
  it in his list.
- **US1-AC2**: **Given** a shared note, **When** Ana stops sharing it, **Then** Ben no longer
  sees it.

## Requirements

- **FR-001**: The system MUST let an owner share a note by [NEEDS CLARIFICATION: email or user name?]
- **FR-002**: A shared note MUST be [NEEDS CLARIFICATION: read-only or editable?]
- **FR-003**: Sharing MUST [NEEDS CLARIFICATION: notify the recipient, and how?]
- **FR-004**: An owner MUST [NEEDS CLARIFICATION: see who opened the note?]
"""


# ---------------------------------------------------------------------------------- helpers


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    assert match, f"{path}: no frontmatter"
    loaded = yaml.safe_load(match.group(1))
    assert isinstance(loaded, dict), f"{path}: frontmatter is not a mapping"
    return loaded


def _graders(repo_root: Path) -> list[tuple[str, dict]]:
    found = []
    for path in sorted((repo_root / "evals").glob("*/*/graders/*.md")):
        found.append((path.relative_to(repo_root / "evals").as_posix(), _frontmatter(path)))
    assert found, "no graders under evals/"
    return found


def _grader(repo_root: Path, rel: str) -> dict:
    return _frontmatter(repo_root / "evals" / rel)


def _regex(pattern: str, flags: str = "") -> re.Pattern[str]:
    value = 0
    for flag, bit in (("i", re.I), ("m", re.M), ("s", re.S)):
        if flag in flags:
            value |= bit
    return re.compile(pattern, value)


def _tool_input(command: str) -> str:
    """A Bash call's input as the eval runner serializes it for ``input_match``."""
    return json.dumps({"command": command, "description": "Run a command"},
                      separators=(",", ":"))


def _is_absence_guard(grader: dict) -> bool:
    if grader.get("type") == "regex" and grader.get("target") == "trace":
        return grader.get("match") in ("not_contains", "count:0")
    if grader.get("type") == "tool_used" and grader.get("tool") == "Bash":
        return grader.get("max") == 0
    return False


def _guard_counts(grader: dict, command: str) -> bool:
    """Whether the guard would count this command against the run."""
    if grader.get("type") == "regex":
        return bool(_regex(grader["pattern"], grader.get("flags", "")).search(command))
    if grader.get("type") == "tool_used":
        pattern = grader.get("input_match")
        return pattern is None or bool(re.search(pattern, _tool_input(command)))
    raise AssertionError(f"not an absence guard: {grader}")


def _skill_texts(repo_root: Path) -> dict[str, str]:
    return {p.relative_to(repo_root).as_posix(): p.read_text(encoding="utf-8")
            for p in sorted((repo_root / "skills").rglob("*.md"))}


@pytest.fixture(scope="module")
def bash_exe() -> str:
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


@pytest.fixture
def run_env(tmp_path: Path) -> dict[str, str]:
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


def _fake_gh(tmp_path: Path, env: dict[str, str], body: str) -> dict[str, str]:
    """``env`` with a ``gh`` first on PATH that runs ``body``."""
    bin_dir = tmp_path / "fake-bin"
    bin_dir.mkdir(exist_ok=True)
    script = bin_dir / "gh"
    script.write_bytes(f"#!/usr/bin/env bash\n{body}\n".encode("utf-8"))
    script.chmod(0o755)
    faked = dict(env)
    faked["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
    return faked


def _bash(bash_exe: str, script: Path, *args: object, cwd: Path,
          env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    cwd.mkdir(parents=True, exist_ok=True)
    argv = [Path(a).as_posix() if isinstance(a, Path) else str(a) for a in args]
    return subprocess.run([bash_exe, script.as_posix(), *argv], cwd=cwd, env=env,
                          capture_output=True, text=True, encoding="utf-8", timeout=300)


def _git(repo: Path, env: dict[str, str], *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], env=env, capture_output=True,
                          text=True, encoding="utf-8", timeout=120)
    assert proc.returncode == 0, f"git {' '.join(args)} in {repo}: {proc.stderr.strip()}"
    return proc.stdout.strip()


# --------------------------------------------------------------------------- trace graders


def test_trace_regex_graders_are_not_decided_by_skill_text(repo_root):
    skills = _skill_texts(repo_root)
    vacuous = []
    for rel, grader in _graders(repo_root):
        if grader.get("type") != "regex" or grader.get("target") != "trace":
            continue
        pattern = _regex(grader["pattern"], grader.get("flags", ""))
        hits = sorted(name for name, text in skills.items() if pattern.search(text))
        if hits:
            vacuous.append(f"{rel} ({grader.get('match', 'contains')}) matches {hits[:3]}")
    assert not vacuous, ("trace graders the injected skill text already decides:\n  "
                         + "\n  ".join(vacuous))


def test_absence_guards_spare_read_only_and_specs_commands(repo_root):
    wrong = []
    for rel, grader in _graders(repo_root):
        if not _is_absence_guard(grader):
            continue
        for command in READ_ONLY_AND_SPECS_COMMANDS:
            if _guard_counts(grader, command):
                wrong.append(f"{rel} counts `{command}`")
    assert not wrong, "absence guards that fail a correct run:\n  " + "\n  ".join(wrong)


def test_foreign_case_guard_still_counts_project_edits(repo_root):
    grader = _grader(repo_root, FOREIGN_GUARD)
    assert _is_absence_guard(grader), f"{FOREIGN_GUARD} is no longer an absence guard: {grader}"
    missed = [c for c in PROJECT_EDITS if not _guard_counts(grader, c)]
    assert not missed, f"{FOREIGN_GUARD} lets these project edits through: {missed}"


def test_foreign_case_checks_the_tracked_readme_is_unchanged(repo_root):
    case = repo_root / "evals" / "setup" / "US1-AC3-foreign-no-footprint" / "graders"
    readme = [g for g in (_frontmatter(p) for p in sorted(case.glob("*.md")))
              if g.get("type") == "regex" and isinstance(g.get("target"), dict)
              and g["target"].get("path") == "README.md"]
    assert readme, "US1-AC3 has no grader over the tracked README.md"
    pattern = _regex(readme[0]["pattern"], readme[0].get("flags", ""))
    original = "# work\n\nA small notes app.\n"
    assert pattern.search(original), "the README grader fails the scaffold's own README"
    assert not pattern.search(original + "\nTags: see specs/.\n"), \
        "the README grader passes an edited README"


@pytest.mark.parametrize("rel", SPEC_CONTENT_GRADERS,
                         ids=lambda r: r.split("/")[1].split("-")[0] + "_" + r.split("/")[-1][:-3])
def test_spec_content_graders_read_the_written_spec(repo_root, rel):
    grader = _grader(repo_root, rel)
    target = grader.get("target")
    assert isinstance(target, dict) and target.get("source") == "file", \
        f"{rel} grades {target!r}, not the spec the run wrote"
    match = re.fullmatch(r"specs/\d{3}-([a-z0-9-]+)/spec\.md", target["path"])
    assert match, f"{rel}: {target['path']} is not a feature's spec.md"
    prompt = (repo_root / "evals" / Path(rel).parent.parent / "prompt.md").read_text(
        encoding="utf-8")
    assert f"`{match.group(1)}`" in prompt, \
        f"{rel}: the prompt does not give the short name {match.group(1)} the path assumes"
    pattern = _regex(grader["pattern"], grader.get("flags", ""))
    template = (repo_root / "skills" / "s2tdd-specify" / "spec-template.md").read_text(
        encoding="utf-8")
    assert not pattern.search(template), f"{rel} passes on the unfilled spec template"
    assert pattern.search(FILLED_SPEC), f"{rel} fails a filled spec"


# ------------------------------------------------------------------------- fixture remotes


@pytest.mark.parametrize("owner", ["acme", "globex"])
def test_project_remote_has_owner_after_a_host_segment(repo_root, bash_exe, run_env, tmp_path,
                                                       owner):
    project = tmp_path / "acme-notes"
    proc = _bash(bash_exe, repo_root / "evals" / "fixtures" / "make-project.sh", project, owner,
                 cwd=tmp_path, env=run_env)
    assert proc.returncode == 0, proc.stderr
    url = _git(project, run_env, "remote", "get-url", "origin").replace("\\", "/")
    assert re.search(rf"/github\.com/{owner}/acme-notes\.git$", url), \
        f"origin is {url}: no host segment for setup to read the owner {owner} after"


def test_specs_remote_has_owner_after_a_host_segment(repo_root, bash_exe, run_env, tmp_path):
    fixtures = repo_root / "evals" / "fixtures"
    project = tmp_path / "acme-notes"
    assert _bash(bash_exe, fixtures / "make-project.sh", project, "acme", cwd=tmp_path,
                 env=run_env).returncode == 0
    proc = _bash(bash_exe, fixtures / "make-specs.sh", project, cwd=tmp_path, env=run_env)
    assert proc.returncode == 0, proc.stderr
    url = _git(project / "specs", run_env, "remote", "get-url", "origin").replace("\\", "/")
    assert re.search(r"/github\.com/acme/acme-notes-specs\.git$", url), \
        f"specs/'s origin is {url}: no host segment before the owner"


# -------------------------------------------------------------------------- the gh account


def test_check_account_helper_is_lf_strict_bash(repo_root, bash_exe, run_env):
    script = repo_root / "evals" / "fixtures" / "check-account.sh"
    assert script.is_file(), "evals/fixtures/check-account.sh not found"
    data = script.read_bytes()
    assert b"\r" not in data and b"set -euo pipefail" in data
    syntax = subprocess.run([bash_exe, "-n", script.as_posix()], env=run_env,
                            capture_output=True, text=True, encoding="utf-8")
    assert syntax.returncode == 0, syntax.stderr


@pytest.mark.parametrize("gh_body, passes", [
    ("echo someone-else", False),
    ("echo acme", True),
    ("echo ACME", True),
    ("echo 'To get started with GitHub CLI, please run:  gh auth login' >&2; exit 4", True),
], ids=["other_account", "same_account", "same_account_other_case", "signed_out"])
def test_check_account_refuses_a_gh_signed_in_as_another_account(
        repo_root, bash_exe, run_env, tmp_path, gh_body, passes):
    script = repo_root / "evals" / "fixtures" / "check-account.sh"
    assert script.is_file(), "evals/fixtures/check-account.sh not found"
    proc = _bash(bash_exe, script, "acme", cwd=tmp_path / "work",
                 env=_fake_gh(tmp_path, run_env, gh_body))
    assert (proc.returncode == 0) is passes, (proc.returncode, proc.stderr)
    if not passes:
        assert "GH_CONFIG_DIR" in proc.stderr, f"the refusal says no way out: {proc.stderr}"
        assert "someone-else" not in proc.stderr, "the refusal echoes the operator's login"


@pytest.mark.parametrize("case", OWN_REPOSITORY_SETUP_CASES, ids=lambda c: c.split("/")[1][:7])
def test_own_repository_scaffold_refuses_gh_signed_in_as_another_account(
        repo_root, bash_exe, run_env, tmp_path, case):
    scaffold = repo_root / "evals" / case / "scaffold.sh"
    other = _bash(bash_exe, scaffold, cwd=tmp_path / "a" / "work",
                  env=_fake_gh(tmp_path, run_env, "echo someone-else"))
    assert other.returncode != 0, \
        f"{case}: the scaffold built an 'own repository' while gh answers another account"
    same = _bash(bash_exe, scaffold, cwd=tmp_path / "b" / "work",
                 env=_fake_gh(tmp_path, run_env, "echo acme"))
    assert same.returncode == 0, f"{case}: {same.stderr.strip()}"
