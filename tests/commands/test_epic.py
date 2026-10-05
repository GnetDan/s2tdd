"""T020: `skills/s2tdd-epic/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, II-8's closed-epic text,
contracts/commands.md's epic row) through `Doc.missing` (II-5): literals and listed phrases only.
"""

from __future__ import annotations

SKILL = "s2tdd-epic"
EPIC_FENCES = ["closing-step", "epic-resolution", "first-run-setup", "worktrees"]  # II-1
CLOSED_EPIC = "This epic is closed; its specs exist and own the work now. New direction is a new epic."  # II-8


def test_frontmatter_name(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter


def test_input_sentence(skill):
    d = skill(SKILL)
    assert not d.missing("the text the user typed after the command"), d.missing(
        "the text the user typed after the command"
    )


def test_mattpocock_credit_kept(skill):
    d = skill(SKILL)
    assert not d.missing("mattpocock/skills (MIT)"), d.missing("mattpocock/skills (MIT)")


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == EPIC_FENCES, d.shared_blocks


def test_constitution_pointer(skill):
    d = skill(SKILL)
    phrases = ("specs/constitution.md", "/s2tdd-constitution")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_handoff_seeds_name_specify(skill):
    d = skill(SKILL)
    assert not d.missing("/s2tdd-specify"), d.missing("/s2tdd-specify")
    assert "seed" in d.flat, "the hand-off seeds are not mentioned"


def test_closed_epic_refusal(skill):
    d = skill(SKILL)
    assert not d.missing(CLOSED_EPIC), d.missing(CLOSED_EPIC)


def test_pages_bundled(skill):
    d = skill(SKILL)
    pages = d.path.parent / "pages"
    absent = [name for name in ("README.md", "WORKFLOW.md") if not (pages / name).is_file()]
    assert not absent, f"missing bundled pages under {pages}: {absent}"
