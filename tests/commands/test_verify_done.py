"""T030: `skills/s2tdd-verify-done/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, contracts/commands.md's
verify-done row) through `Doc.missing` (II-5): literals and listed phrases only.
"""

from __future__ import annotations

SKILL = "s2tdd-verify-done"
FENCES = ["closing-step", "feature-resolution", "worktrees"]  # II-1
VERDICTS = ("Verified", "Verified with gaps", "Not done")


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


def test_verdicts_recorded_in_verification_log(skill):
    d = skill(SKILL)
    phrases = (*VERDICTS, "validation.md", "## Verification log")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_unticks_failed_tasks(skill):
    d = skill(SKILL)
    phrases = ("untick", "tasks.md")
    assert not d.missing(*phrases), d.missing(*phrases)
