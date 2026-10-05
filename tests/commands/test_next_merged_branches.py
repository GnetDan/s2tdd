"""T059: the merged-branches Watch out item of `skills/s2tdd-next/SKILL.md` (US9-AC1, FR-014).

Pins the item's literals and listed phrases through `Doc.missing` (II-5). Every test first
requires `git branch --merged` itself: without the item none of the rest can hold, and that
is the reason these fail until T060.
"""

from __future__ import annotations

import re

SKILL = "s2tdd-next"
LOCAL_MERGED = "git branch --merged"
REMOTE_MERGED = "git branch -r --merged"


def _has_the_item(d):
    assert not d.missing(LOCAL_MERGED), f"`{LOCAL_MERGED}` is missing from the command"


def test_finds_local_and_remote_merged_branches(skill):
    d = skill(SKILL)
    _has_the_item(d)
    assert not d.missing(REMOTE_MERGED), d.missing(REMOTE_MERGED)


def test_only_branches_that_lead_with_a_feature_number(skill):
    d = skill(SKILL)
    _has_the_item(d)
    assert not d.missing("feature number"), d.missing("feature number")


def test_lists_them_under_watch_out_with_the_delete_commands(skill):
    d = skill(SKILL)
    _has_the_item(d)
    phrases = ("watch out", "git branch -d", "git push origin --delete")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_deletes_nothing(skill):
    d = skill(SKILL)
    _has_the_item(d)
    pattern = r"(deletes? nothing|nothing (is |gets )?deleted|never deletes?|does not delete)"
    assert re.search(pattern, d.flat), "no statement that nothing is deleted"


def test_recommends_automatic_deletion_of_head_branches(skill):
    d = skill(SKILL)
    _has_the_item(d)
    pattern = r"automatic(ally)? delet\w* (of )?head branches"
    assert re.search(pattern, d.flat), "no recommendation of automatic deletion of head branches"


def test_a_branch_with_no_commits_of_its_own_is_not_merged(skill):
    """PR #3 review Q3-3: specs live in their own repository, so a feature branch has no
    project commits until implement, and `git branch --merged` then lists it. Next must
    keep such a branch off the list unless its feature is closed or its PR has merged."""
    d = skill(SKILL)
    _has_the_item(d)
    assert re.search(r"no commits? of its own", d.flat), "no rule for branches with no commits of their own"
    assert not d.missing("rev-list --count", "Closed", "gh pr list"), d.missing("rev-list --count", "Closed", "gh pr list")
