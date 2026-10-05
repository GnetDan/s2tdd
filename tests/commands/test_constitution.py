"""T057: `skills/s2tdd-constitution/SKILL.md` and its bundled template and pages.

Pins the contract's required elements (II-1 fences, II-4 bundled pages, II-6 shape,
contracts/commands.md's constitution row, US8-AC1, US8-AC2) through `Doc.missing` (II-5):
literals and listed phrases only.
"""

from __future__ import annotations

# II-6: the credit line of a forked or derived file.
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"

SKILL = "s2tdd-constitution"
CONSTITUTION_FENCES = ["closing-step", "first-run-setup", "worktrees"]  # II-1
TEMPLATE = "./constitution-template.md"  # P5: named as ./<file>, beside SKILL.md


def test_frontmatter_name_and_credit(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter
    assert d.first_body_line == CREDIT_LINE, d.first_body_line


def test_input_sentence(skill):
    d = skill(SKILL)
    assert not d.missing("the text the user typed after the command"), d.missing(
        "the text the user typed after the command"
    )


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == CONSTITUTION_FENCES, d.shared_blocks


def test_grills_to_create_from_bundled_template(skill):
    # US8-AC1: no constitution yet, so it grills and writes specs/constitution.md from the template.
    d = skill(SKILL)
    phrases = ("grill", "specs/constitution.md", TEMPLATE)
    assert not d.missing(*phrases), d.missing(*phrases)
    template = d.path.parent / "constitution-template.md"
    assert template.is_file(), f"missing bundled template: {template}"


def test_amendment_bumps_version_and_adds_dated_change_note(skill):
    # US8-AC2: an amendment bumps the semantic version and adds a dated change note in the file.
    d = skill(SKILL)
    phrases = ("semantic version", "bump", "dated", "change note")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_no_propagation_into_project_templates(skill):
    # Upstream's propagation into the project's templates goes; templates are bundled.
    d = skill(SKILL)
    present = [s for s in (".specify/", "propagation checklist") if s in d.flat]
    assert not present, f"template propagation or spec-kit paths remain: {present}"


def test_pages_bundled(skill):
    # II-4: both project pages are copied into the skill folder.
    d = skill(SKILL)
    pages = d.path.parent / "pages"
    absent = [name for name in ("README.md", "WORKFLOW.md") if not (pages / name).is_file()]
    assert not absent, f"missing bundled pages under {pages}: {absent}"
