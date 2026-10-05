"""T028: `skills/s2tdd-harden/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, II-8's refusal texts,
II-9's tier mapping, contracts/commands.md's harden row) through `Doc.missing` (II-5):
literals and listed phrases only. The literals harden carries over from the preset
(NOBRAKES markers, standard briefs) belong to T025's acceptance tests.
"""

from __future__ import annotations

# II-6: the credit line of a forked file.
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"

SKILL = "s2tdd-harden"
HARDEN_FENCES = ["closing-step", "feature-resolution", "worktrees"]  # II-1
PHASES = ("hygiene", "interfaces", "judgments", "orchestration", "handoff")
WRITES = ("orchestration.md", "handoff.md", "validation.md", "run-ledger.md")
TIERS = ("cheap", "medium", "strong")
# II-8
CLOSED = "This feature is closed; new work is a new spec."
NO_PLAN = "no plan.md: run /s2tdd-plan first."


def test_frontmatter_credit_and_input(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter
    assert d.first_body_line == CREDIT_LINE, d.first_body_line
    phrases = ("the text the user typed after the command",)
    assert not d.missing(*phrases), d.missing(*phrases)


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == HARDEN_FENCES, d.shared_blocks


def test_generates_missing_tasks_test_first_from_bundled_template(skill):
    d = skill(SKILL)
    phrases = (
        "tasks.md",
        "./tasks-template.md",
        "test-first",
        "acceptance",
        "test task",
        "Scenarios:",
        "exactly once",
    )
    assert not d.missing(*phrases), d.missing(*phrases)


def test_bundled_template_sits_beside_the_skill(skill):
    d = skill(SKILL)
    template = d.path.parent / "tasks-template.md"
    assert template.is_file(), f"missing bundled file: {template}"


def test_single_phase_input_and_append_and_refresh_modes(skill):
    d = skill(SKILL)
    phrases = (*PHASES, "append mode", "refresh mode")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_writes_the_four_feature_files(skill):
    d = skill(SKILL)
    assert not d.missing(*WRITES), d.missing(*WRITES)


def test_tiers_map_to_agent_types(skill):
    d = skill(SKILL)
    phrases = ("cheap / medium / strong",)
    assert not d.missing(*phrases), d.missing(*phrases)
    # II-9: `s2tdd:packet-<tier>`, written either with the placeholder or one name per tier.
    generic = not d.missing("s2tdd:packet-<tier>")
    named = not d.missing(*(f"s2tdd:packet-{tier}" for tier in TIERS))
    assert generic or named, "no mapping of the tiers to s2tdd:packet-<tier>"


def test_validation_gates(skill):
    d = skill(SKILL)
    phrases = ("validation gates", "every task appears in exactly one packet")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_refuses_a_closed_feature(skill):
    d = skill(SKILL)
    phrases = ("**Status**:", "Closed", CLOSED)
    assert not d.missing(*phrases), d.missing(*phrases)


def test_refuses_a_missing_plan(skill):
    d = skill(SKILL)
    assert not d.missing(NO_PLAN), d.missing(NO_PLAN)
