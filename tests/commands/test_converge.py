"""T031: `skills/s2tdd-converge/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, II-8's closed-feature text,
contracts/commands.md's converge row) through `Doc.missing` (II-5): literals and listed
phrases only.
"""

from __future__ import annotations

SKILL = "s2tdd-converge"
FENCES = ["closing-step", "feature-resolution", "worktrees"]  # II-1
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"  # II-3 constant (type home: tools/check.py)
CLOSED = (  # II-8
    "This feature is closed (see close-out.md); its spec is a historical intent record and is "
    "neither assessed nor edited. Further work belongs in a new feature: `/s2tdd-specify`."
)


def test_frontmatter_name(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter


def test_input_sentence(skill):
    d = skill(SKILL)
    assert not d.missing("the text the user typed after the command"), d.missing(
        "the text the user typed after the command"
    )


def test_spec_kit_credit(skill):
    d = skill(SKILL)
    assert d.first_body_line == CREDIT_LINE, d.first_body_line


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == FENCES, d.shared_blocks


def test_closed_feature_refusal(skill):
    d = skill(SKILL)
    assert not d.missing(CLOSED), d.missing(CLOSED)


def test_recorded_cited_deviations_are_superseded_not_gaps(skill):
    d = skill(SKILL)
    phrases = ("superseded", "Supersedes")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_appends_tasks_to_tasks_md(skill):
    d = skill(SKILL)
    phrases = ("append", "tasks.md")
    assert not d.missing(*phrases), d.missing(*phrases)


def _paragraph(d, opening: str) -> str:
    """The flattened paragraph of the skill body that starts with `opening`, plus the list
    right after it (if any)."""
    blocks = d.body.split("\n\n")
    for i, block in enumerate(blocks):
        if block.lstrip().startswith(opening):
            text = block
            for after in blocks[i + 1 :]:
                if not after.lstrip().startswith("- "):
                    break
                text += "\n" + after
            return " ".join(text.lower().replace("`", "").replace("*", "").split())
    raise AssertionError(f"no paragraph starts with {opening!r}")


def test_guard_sets_aside_pending_checkpoints(skill):
    # Close-time CHECKPOINT tasks (and ones whose Done-when accepts a PENDING block) stay
    # unticked until /s2tdd-close, which needs a converged line first: the guard must not
    # count them, or a feature whose only open tasks are checkpoints can never close.
    guard = _paragraph(skill(SKILL), "**Implementation-complete guard**")
    for phrase in (
        "whose description begins checkpoint",
        "after any [p] and [usn] markers",
        "pending checkpoints",
        "if any other unticked task remains, stop without writing anything",
        "task(s) in tasks.md are unticked; finish implementing (and verify) them before converging.",
    ):
        assert phrase in guard, (phrase, guard)


def test_summary_lists_pending_checkpoints(skill):
    metrics = _paragraph(skill(SKILL), "**Summary metrics:**")
    assert "pending checkpoints" in metrics, metrics
