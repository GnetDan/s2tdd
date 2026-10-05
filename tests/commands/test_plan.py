"""T027: `skills/s2tdd-plan/SKILL.md` and its bundled `plan-template.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, II-8's closed-feature text,
contracts/commands.md's plan row) through `Doc.missing` (II-5): literals and listed phrases only.
"""

from __future__ import annotations

# II-6: the credit line of a forked or derived file.
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"

SKILL = "s2tdd-plan"
PLAN_FENCES = ["closing-step", "feature-resolution", "worktrees"]  # II-1
# II-8, plan row (the last column's text).
CLOSED_FEATURE = (
    "This feature is closed; its spec is a historical intent record. New or changed behavior "
    "belongs in a new feature (`/s2tdd-specify`) with a `**Supersedes**:` line."
)


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
    assert sorted(d.shared_blocks) == PLAN_FENCES, d.shared_blocks


def test_no_setup_script(skill):
    d = skill(SKILL)
    present = [s for s in (".specify/scripts", "{SCRIPT}") if s in d.text]
    assert not present, f"the setup script is still referenced: {present}"


def test_reads_constitution_at_specs(skill):
    d = skill(SKILL)
    assert not d.missing("specs/constitution.md"), d.missing("specs/constitution.md")


def test_constitution_gate(skill):
    # An unjustified violation stops the plan; a justified one goes in Complexity Tracking.
    d = skill(SKILL)
    phrases = ("violation", "justif", "Complexity Tracking")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_phase_0_dispatches_research_agents(skill):
    d = skill(SKILL)
    phrases = ("Phase 0", "research agents")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_research_r_entries_appended_never_renumbered(skill):
    d = skill(SKILL)
    phrases = ("research.md", "## R<n>.", "append", "renumber")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_phase_1_artifacts_and_quickstart_run_marking(skill):
    d = skill(SKILL)
    phrases = ("Phase 1", "data-model.md", "contracts/", "quickstart.md", "scripted", "human")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_plan_template_bundled_with_acceptance_tests_field(skill, doc):
    d = skill(SKILL)
    assert not d.missing("./plan-template.md"), d.missing("./plan-template.md")
    template = doc("skills/s2tdd-plan/plan-template.md")
    assert not template.missing("**Acceptance tests**"), template.missing("**Acceptance tests**")


def test_closed_feature_refusal(skill):
    d = skill(SKILL)
    assert not d.missing(CLOSED_FEATURE), d.missing(CLOSED_FEATURE)
