"""T032: `skills/s2tdd-pr-review/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, contracts/commands.md's
pr-review row) through `Doc.missing` (II-5): literals and listed phrases only. The cloud
rules (R2, the refusal text) are T047's and have their own test file.
"""

from __future__ import annotations

SKILL = "s2tdd-pr-review"
FENCES = ["closing-step", "feature-resolution", "worktrees"]  # II-1
HINT_TOKENS = ("<PR number>", "[--fix]", "[--cloud]", "[--specs-repo")  # tasks.md T032's input


def test_frontmatter_name(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter


def test_input_sentence(skill):
    d = skill(SKILL)
    assert not d.missing("the text the user typed after the command"), d.missing(
        "the text the user typed after the command"
    )


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == FENCES, d.shared_blocks


def test_argument_hint(skill):
    d = skill(SKILL)
    hint = str(d.frontmatter.get("argument-hint", ""))
    absent = [token for token in HINT_TOKENS if token not in hint]
    assert not absent, f"argument-hint {hint!r} lacks {absent}"


def test_report_only_by_default(skill):
    d = skill(SKILL)
    assert not d.missing("report-only"), d.missing("report-only")


def test_fix_is_test_first_on_the_pr_branch(skill):
    d = skill(SKILL)
    phrases = ("--fix", "test-first", "PR branch")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_cloud_moves_a_local_desktop_session(skill):
    d = skill(SKILL)
    phrases = ("--cloud", "desktop", "cloud session")
    assert not d.missing(*phrases), d.missing(*phrases)
