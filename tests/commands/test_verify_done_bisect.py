"""PR #8 review C-3, C-8: verify-done's unexplained-red bisect and its green-at sha.

C-3: the bisect checks older commits out; the gate worktree goes back to the gate's commit
before Invariants runs there, the main-checkout scratch worktree gets a named path, the gate
files, the suite's loads-from-the-worktree check and removal, and a test already red at the
range's oldest commit is reported red before the range, never as a wave's failed claim.
C-8: the sha in ` · green at <sha>` is the short sha converge and close compare against.
Phrases are flattened the II-0 way (whitespace runs, backticks and asterisks) and matched in
order.
"""

from __future__ import annotations

SKILL = "s2tdd-verify-done"

BISECT = "and stop at the first commit where it is red."
SCRATCH = (
    "In the main checkout, the scratch worktree is git worktree add .sdd-run/<NNN>/bisect "
    "<sha>, with the gate files (the ignored files the suite needs) copied in by name"
)
SCRATCH_LOADS = (
    "before the first run there, check that the code under test loads from it, the same way "
    "as the Suite item"
)
SCRATCH_REMOVED = "remove it (and the copied gate files) after the last run."
RED_BEFORE = "Red before the range: <test id> — red alone at W<a> (<sha>)"
RED_BEFORE_MEANING = (
    "an environment problem or a flake, not a wave's failed claim: it unticks nothing"
)
RESTORE = (
    "After the bisect, check the gate worktree out at the gate's commit again "
    "(git -C <worktree> checkout --detach <the gate's commit>) before Invariants runs there."
)
INVARIANTS = "Invariants: when the repo has a guardrail command"
GREEN_AT = "Append · green at <sha> after the suite suffix"
SHORT_SHA = (
    "<sha> is the short sha, git rev-parse --short <commit>, the form converge and close "
    "compare against git rev-parse --short HEAD."
)


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _in_order(flat: str, *phrases: str) -> list[str]:
    """The phrases missing from flat, or out of order after the previous one found."""
    bad, pos = [], 0
    for p in phrases:
        i = flat.find(_flatten(p), pos)
        if i < 0:
            bad.append(p)
        else:
            pos = i
    return bad


def test_scratch_worktree_is_named_loaded_and_removed(skill):
    d = skill(SKILL)
    phrases = (BISECT, SCRATCH, SCRATCH_LOADS, SCRATCH_REMOVED, INVARIANTS)
    assert not _in_order(d.flat, *phrases), _in_order(d.flat, *phrases)


def test_red_at_the_oldest_commit_is_red_before_the_range(skill):
    d = skill(SKILL)
    phrases = (BISECT, RED_BEFORE, RED_BEFORE_MEANING, INVARIANTS)
    assert not _in_order(d.flat, *phrases), _in_order(d.flat, *phrases)


def test_gate_worktree_returns_to_the_gate_commit_before_invariants(skill):
    d = skill(SKILL)
    phrases = (BISECT, RESTORE, INVARIANTS)
    assert not _in_order(d.flat, *phrases), _in_order(d.flat, *phrases)


def test_green_at_sha_is_the_short_sha(skill):
    d = skill(SKILL)
    phrases = (GREEN_AT, SHORT_SHA)
    assert not _in_order(d.flat, *phrases), _in_order(d.flat, *phrases)
