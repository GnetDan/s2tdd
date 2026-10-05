"""T034: `skills/s2tdd-foundation-review/SKILL.md`, the read-only review of the whole codebase.

Asserts the contract's required elements (II-1 fences, II-6 shape, contracts/commands.md's
foundation-review row) as literals and the key phrases T034 lists, through `Doc.missing` over
flattened text (II-5).
"""

from __future__ import annotations

import re

SKILL = "s2tdd-foundation-review"
# II-1: project-wide, so no feature-resolution or epic-resolution; worktrees and closing-step.
FOUNDATION_REVIEW_FENCES = ["closing-step", "worktrees"]
# II-6: frontmatter keeps name, description and the optional argument-hint, nothing else.
FRONTMATTER_KEYS = {"name", "description", "argument-hint"}


def test_frontmatter_name_and_keys(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter
    assert d.frontmatter.get("description"), d.frontmatter
    assert set(d.frontmatter) <= FRONTMATTER_KEYS, sorted(set(d.frontmatter) - FRONTMATTER_KEYS)


def test_input_sentence(skill):
    d = skill(SKILL)
    phrase = "the text the user typed after the command"
    assert not d.missing(phrase), d.missing(phrase)


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == FOUNDATION_REVIEW_FENCES, d.shared_blocks


def test_read_only_never_modifies_source_tests_or_specs(skill):
    d = skill(SKILL)
    assert not d.missing("read-only"), d.missing("read-only")
    stated = re.search(r"never[^.]*modify[^.]*source[^.]*tests[^.]*specs", d.flat)
    assert stated, "no statement that it never modifies the source, the tests or specs/"
