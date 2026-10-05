"""T019: `skills/s2tdd-specify/SKILL.md`, the command that starts a feature.

Asserts the contract's required elements (II-1, II-6; US1-AC4, US1-AC5, US1-AC6) as literals and
the key phrases T019 lists, through `Doc.missing` over flattened text (II-5).
"""

from __future__ import annotations

# II-6: the credit line of a forked file.
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"

SKILL = "s2tdd-specify"


def test_specify_frontmatter_credit_and_input(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == "s2tdd-specify", d.frontmatter
    assert d.first_body_line == CREDIT_LINE, d.first_body_line
    absent = d.missing("mattpocock/skills (MIT)", "the text the user typed after the command")
    assert not absent, absent


def test_specify_holds_exactly_three_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == ["closing-step", "first-run-setup", "worktrees"], (
        d.shared_blocks
    )
    assert "feature-resolution" not in d.shared_blocks, d.shared_blocks


def test_specify_branch_numbering_past_specs_and_branches(skill):
    # US1-AC4 (T07): one past the highest of specs/ and every local and remote branch.
    d = skill(SKILL)
    absent = d.missing("git branch -a", "specs/", "NNN-<short-name>")
    assert not absent, absent


def test_specify_marks_every_gap_without_cap_or_guess(skill):
    # US1-AC5: no cap on open-gap markers, no informed guesses.
    d = skill(SKILL)
    absent = d.missing("no cap", "no informed guess")
    assert not absent, absent


def test_specify_grills_one_round_at_a_time(skill):
    # US1-AC5: a grilling loop with a recommended answer per question, until the gaps are
    # resolved or the user says enough.
    d = skill(SKILL)
    absent = d.missing("one round at a time", "recommended answer", "enough")
    assert not absent, absent


def test_specify_constitution_pointer(skill):
    # US1-AC6: names /s2tdd-constitution when specs/constitution.md is missing, then carries on.
    d = skill(SKILL)
    absent = d.missing("specs/constitution.md", "/s2tdd-constitution")
    assert not absent, absent


def test_specify_bundles_spec_template_with_scenario_ids(skill, doc):
    d = skill(SKILL)
    absent = d.missing("./spec-template.md")
    assert not absent, absent
    template = doc("skills/s2tdd-specify/spec-template.md")
    absent = template.missing("US<n>-AC<m>", "EC-<nnn>")
    assert not absent, absent


def test_specify_pages_are_bundled(skill):
    d = skill(SKILL)
    folder = d.path.parent
    for page in ("pages/README.md", "pages/WORKFLOW.md"):
        assert (folder / page).is_file(), f"missing bundled page: {folder / page}"
