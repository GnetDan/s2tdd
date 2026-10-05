"""T046, T100: the cloud rules of `skills/s2tdd-pr-review/SKILL.md` (US6-AC5, US6-AC6, US6-AC7).

Pins research.md R2 and II-8's pr-review row through `Doc.missing` (II-5): literals and
listed phrases only. Every test first requires that the command reads `CLAUDE_CODE_REMOTE`
at all: without it none of the cloud rules can hold, and that is the reason these fail
until T047.

T100 (US6-AC7, FR-019 as amended 2026-10-03): with `--cloud` the command reads the local
specs repository's remote and states its URL before the move, and the cloud copy clones it
between `--specs-repo` and the guidance file or README. Its tests first require the remote
read at all (`git -C specs remote get-url origin`), which is why they fail until T101.
"""

from __future__ import annotations

import re

SKILL = "s2tdd-pr-review"
VARIABLE = "CLAUDE_CODE_REMOTE"
REFUSAL = "This review was started in a cloud session: start it locally with `--cloud`."  # II-8
TOOL_PRESENCE_DETECTION = "no mcp__ccd_session__move_to_cloud tool"  # the preset's signal (R2)
MOVE_TOOL = "mcp__ccd_session__move_to_cloud"
REMOTE_READ = "git -C specs remote get-url origin"  # T100


def _reads_the_variable(d):
    assert not d.missing(VARIABLE), f"{VARIABLE} is missing from the command"


def test_reads_the_variable_in_either_shell(skill):
    d = skill(SKILL)
    phrases = (f"printenv {VARIABLE}", f"$env:{VARIABLE}")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_true_without_a_move_in_this_run_refuses(skill):
    """US6-AC6: started in the cloud (the transcript shows no move for this run) -> refuse."""
    d = skill(SKILL)
    _reads_the_variable(d)
    assert not d.missing("true", "transcript"), d.missing("true", "transcript")
    assert not d.missing(REFUSAL), d.missing(REFUSAL)


def test_true_after_this_runs_move_carries_on_and_prints_the_next_step(skill):
    """US6-AC5: moved for this run -> carry on; print the next step, do not run /s2tdd-next."""
    d = skill(SKILL)
    _reads_the_variable(d)
    phrases = ("next step", "instead of running /s2tdd-next")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_anything_but_true_is_local(skill):
    d = skill(SKILL)
    _reads_the_variable(d)
    assert re.search(r"(anything but|other than|not) true", d.flat), "no 'not true' rule"
    assert not d.missing("local"), d.missing("local")


def test_the_presets_tool_presence_test_is_no_longer_the_detection(skill):
    d = skill(SKILL)
    _reads_the_variable(d)
    assert d.missing(TOOL_PRESENCE_DETECTION) == [TOOL_PRESENCE_DETECTION], (
        "the command still detects a remote session by the absence of the move tool"
    )


# --- T100: the specs remote URL travels with the move (US6-AC7, FR-019) ---------------------


def _reads_the_specs_remote(d):
    assert not d.missing(REMOTE_READ), f"{REMOTE_READ} is missing from the command"


def _before_the_move(d) -> str:
    """The flattened text up to the first mention of the move tool (the local half)."""
    return d.flat[: d.flat.index(MOVE_TOOL)]


def _clone_order(d) -> str:
    """Phase 0's clone-order sentence: from its first `--specs-repo` up to the clone command."""
    phase0 = d.flat[d.flat.index("phase 0: ground") :]
    start = phase0.index("--specs-repo")
    return phase0[start : phase0.index("git clone --depth 1")]


def test_reads_the_specs_remote_before_the_move(skill):
    """US6-AC7: the local session reads the specs repository's remote before moving."""
    d = skill(SKILL)
    _reads_the_specs_remote(d)
    assert not d.missing(MOVE_TOOL), d.missing(MOVE_TOOL)
    assert d.flat.index(REMOTE_READ.lower()) < d.flat.index(MOVE_TOOL), (
        "the specs remote is read only after the move tool is named"
    )


def test_the_remote_read_covers_a_worktree_without_specs(skill):
    """T100: `specs/` is taken from the main worktree when `./specs` is missing."""
    d = skill(SKILL)
    _reads_the_specs_remote(d)
    local_half = d.flat[d.flat.index("where it runs") : d.flat.index("phase 0: ground")]
    phrases = ("main worktree", "./specs")
    assert not [p for p in phrases if p not in local_half], phrases


def test_states_the_url_in_the_conversation_before_calling_the_move(skill):
    """FR-019: the URL is stated in the conversation, ahead of the move tool call."""
    d = skill(SKILL)
    _reads_the_specs_remote(d)
    stated = d.flat[d.flat.index(REMOTE_READ.lower()) : d.flat.index(MOVE_TOOL)]
    assert re.search(r"\bstat(e|es|ed|ing)\b", stated), "no statement of the URL before the move"
    assert "url" in stated and "conversation" in stated, (
        "the URL is not stated in the conversation before the move"
    )


def test_cloud_clone_order_puts_the_stated_url_between_specs_repo_and_the_guidance_file(skill):
    """US6-AC7: `--specs-repo`, then the URL stated before this run's move, then guidance/README."""
    d = skill(SKILL)
    _reads_the_specs_remote(d)
    order = _clone_order(d)
    positions = {}
    for label, needle in (
        ("--specs-repo", "--specs-repo"),
        ("the stated URL", "stated"),
        ("the agent guidance file", "agent guidance file"),
        ("the README", "readme"),
    ):
        assert needle in order, f"{label} is missing from the clone order"
        positions[label] = order.index(needle)
    assert (
        positions["--specs-repo"]
        < positions["the stated URL"]
        < positions["the agent guidance file"]
    ), f"clone order is not --specs-repo, stated URL, guidance file: {positions}"
    assert positions["the stated URL"] < positions["the README"], positions
    assert "move" in order, "the stated URL is not tied to this run's move"


def test_no_remote_still_moves_and_says_the_spec_half_needs_specs_repo(skill):
    """US6-AC7: no remote (or `specs/` not its own repository) -> move anyway, say so."""
    d = skill(SKILL)
    _reads_the_specs_remote(d)
    local_half = d.flat[d.flat.index("where it runs") : d.flat.index("phase 0: ground")]
    phrases = ("no remote", "spec half", "--specs-repo")
    absent = [p for p in phrases if p not in local_half]
    assert not absent, f"missing from the local half: {absent}"
    assert local_half.count(MOVE_TOOL) >= 1, "the move is no longer called"
