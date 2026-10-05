"""T033: `skills/s2tdd-close/SKILL.md`, the command that closes a feature.

Asserts the contract's required elements (II-1 fences, II-6 shape, II-8's already-closed text,
contracts/commands.md's close row) as literals and the key phrases T033 lists, through
`Doc.missing` over flattened text (II-5).
"""

from __future__ import annotations

SKILL = "s2tdd-close"
# II-1: close holds feature-resolution, worktrees and closing-step (not epic-resolution or
# first-run-setup).
CLOSE_FENCES = ["closing-step", "feature-resolution", "worktrees"]
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
    assert sorted(d.shared_blocks) == CLOSE_FENCES, d.shared_blocks


def test_refuses_an_already_closed_feature(skill):
    # II-6 closed guard and II-8's close row: `already closed on <date>; see close-out.md`.
    d = skill(SKILL)
    phrases = ("begins with Closed", "already closed on", "see close-out.md")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_gate_on_delivered_tasks(skill):
    # Phase A1: every unchecked task is delivered (with named evidence) or dropped.
    d = skill(SKILL)
    phrases = ("- [ ] T", "delivered", "dropped")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_gate_on_a_green_suite(skill):
    # Phase A2: the full test command runs; green is the gate.
    d = skill(SKILL)
    phrases = ("full test command", "green")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_gate_on_converge_at_or_after_the_last_wave(skill):
    # Phase A4, under II-15's rename (the stop names `/s2tdd-converge`).
    d = skill(SKILL)
    phrases = (
        "/s2tdd-converge",
        "git merge-base --is-ancestor",
        "no converged result at or after the last wave commit",
    )
    assert not d.missing(*phrases), d.missing(*phrases)


def test_writes_close_out_and_stamps_closed(skill):
    d = skill(SKILL)
    phrases = ("close-out.md", "spec.md", "**Status**: Closed")
    assert not d.missing(*phrases), d.missing(*phrases)
