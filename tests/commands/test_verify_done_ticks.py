"""PR #3 review Q2-2: verify-done must see ticks already committed in a separate specs repo.

Harden's HOW TO WORK commits the ticks in the specs repository after every green wave, so a
bare `git -C <specs repo> diff -- <tasks.md>` (working tree vs index) prints nothing for them.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

SKILL = "s2tdd-verify-done"
BARE_DIFF = "else `git -C <specs repo> diff -- <tasks.md>`"
BASE_DIFF = (
    "git -C <specs repo> diff $(git -C <specs repo> rev-list -1 "
    "--before=<first wave commit's committer date> HEAD) -- <tasks.md>"
)


def test_unclaimed_tick_check_does_not_use_a_bare_working_tree_diff(skill):
    d = skill(SKILL)
    assert d.missing(BARE_DIFF), "verify-done still diffs tasks.md against the index only"


def test_unclaimed_tick_check_diffs_from_the_specs_state_before_the_waves(skill):
    d = skill(SKILL)
    phrases = (BASE_DIFF, "git log -1 --format=%cI <first>",
               "committed and uncommitted ticks alike")
    assert not d.missing(*phrases), d.missing(*phrases)


def _git(repo: Path, *args: str, date: str | None = None) -> str:
    env = None
    if date:
        import os
        env = {**os.environ, "GIT_COMMITTER_DATE": date, "GIT_AUTHOR_DATE": date}
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True, env=env).stdout


def test_the_documented_diff_finds_a_committed_tick(tmp_path):
    """The recipe the skill names catches a tick committed after the first wave commit."""
    specs, app = tmp_path / "specs", tmp_path / "app"
    for repo in (specs, app):
        repo.mkdir()
        _git(repo, "init", "-q")
        _git(repo, "config", "user.email", "t@example.com")
        _git(repo, "config", "user.name", "t")
    tasks = specs / "tasks.md"
    tasks.write_text("- [ ] T040 thing\n", encoding="utf-8")
    _git(specs, "add", "tasks.md")
    _git(specs, "commit", "-qm", "tasks", date="2026-01-01T10:00:00+00:00")
    (app / "a.txt").write_text("x\n", encoding="utf-8")
    _git(app, "add", "a.txt")
    _git(app, "commit", "-qm", "feat(004): wave 1", date="2026-01-01T11:00:00+00:00")
    tasks.write_text("- [x] T040 thing\n", encoding="utf-8")
    _git(specs, "commit", "-qam", "ticks", date="2026-01-01T11:05:00+00:00")

    assert _git(specs, "diff", "--", "tasks.md") == ""  # the old check sees nothing
    first_date = _git(app, "log", "-1", "--format=%cI", "HEAD").strip()
    base = _git(specs, "rev-list", "-1", f"--before={first_date}", "HEAD").strip()
    assert "+- [x] T040" in _git(specs, "diff", base, "--", "tasks.md")
