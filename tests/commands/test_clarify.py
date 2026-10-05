"""T026: `skills/s2tdd-clarify/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, II-8's closed-feature text,
contracts/commands.md's clarify row) through `Doc.missing` (II-5): literals and listed phrases only.
"""

from __future__ import annotations

# II-6: the credit line of a forked or derived file.
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"

SKILL = "s2tdd-clarify"
CLARIFY_FENCES = ["closing-step", "feature-resolution", "worktrees"]  # II-1
# II-8, clarify row (the last column's text).
CLOSED_FEATURE = (
    "This feature is closed; its spec is a historical intent record. New or changed behavior "
    "belongs in a new feature (`/s2tdd-specify`) with a `**Supersedes**:` line."
)


def test_frontmatter_name(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter


def test_input_sentence(skill):
    d = skill(SKILL)
    assert not d.missing("the text the user typed after the command"), d.missing(
        "the text the user typed after the command"
    )


def test_credits_kept(skill):
    d = skill(SKILL)
    assert d.first_body_line == CREDIT_LINE, d.first_body_line
    assert not d.missing("mattpocock/skills (MIT)"), d.missing("mattpocock/skills (MIT)")


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == CLARIFY_FENCES, d.shared_blocks


def test_decisions_written_as_r_entries_in_research_md(skill):
    d = skill(SKILL)
    phrases = ("research.md", "## R<n>.", "Decision", "Rationale", "Alternatives considered")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_closed_feature_refusal(skill):
    d = skill(SKILL)
    assert not d.missing(CLOSED_FEATURE), d.missing(CLOSED_FEATURE)
