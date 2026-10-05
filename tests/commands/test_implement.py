"""T029: `skills/s2tdd-implement/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, II-8's refusal texts, II-9's
agent types, R4's `--print`, contracts/commands.md's implement row) through `Doc.missing`
(II-5): literals and listed phrases only. The stale-name refusal (migration fence) is T070's,
the Cursor fallback is T065's; neither is tested here.
"""

from __future__ import annotations

import re

# II-6: the credit line of a forked file.
CREDIT_LINE = "<!-- Adapted from github/spec-kit (MIT). -->"

SKILL = "s2tdd-implement"
IMPLEMENT_FENCES = ["closing-step", "feature-resolution", "worktrees"]  # II-1
TIERS = ("cheap", "medium", "strong")

# II-8 (the parts in backticks of the last column; placeholders such as <date> excluded).
CLOSED = "This feature is closed; new work belongs in a new feature."
UNHARDENED = "run /s2tdd-harden first — s2tdd implements hardened tasks only."
PREDATES = "handoff.md predates --nobrakes: run /s2tdd-harden handoff to refresh it."
LEASE_PARTS = (
    "another orchestrator holds this feature:",
    "If that session is gone, append",
    "released by user",
    "under Lease in run-ledger.md and run this again.",
)


def test_frontmatter_credit_and_input(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter
    assert d.first_body_line == CREDIT_LINE, d.first_body_line
    phrases = ("the text the user typed after the command",)
    assert not d.missing(*phrases), d.missing(*phrases)


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == IMPLEMENT_FENCES, d.shared_blocks


def test_print_prints_the_filled_prompt_and_runs_nothing(skill):
    """R4: `--print` prints the filled prompt for another harness; with `--nobrakes`, the
    unattended form."""
    d = skill(SKILL)
    phrases = ("--print", "--nobrakes", "unattended", "handoff.md")
    assert not d.missing(*phrases), d.missing(*phrases)
    runs_nothing = re.search(
        r"runs? nothing|nothing (is )?(run|executed)|does not (run|execute)|without running",
        d.flat,
    )
    assert runs_nothing, "--print is not said to run nothing"


def test_nobrakes_keeps_the_run_ledger_and_lease(skill):
    d = skill(SKILL)
    phrases = ("--nobrakes", "run-ledger.md", "Lease")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_refuses_an_unhardened_feature(skill):
    d = skill(SKILL)
    phrases = ("handoff.md", "orchestration.md", UNHARDENED)
    assert not d.missing(*phrases), d.missing(*phrases)


def test_refuses_a_closed_feature(skill):
    d = skill(SKILL)
    phrases = ("**Status**:", "Closed", CLOSED)
    assert not d.missing(*phrases), d.missing(*phrases)


def test_refuses_nobrakes_on_a_handoff_that_predates_it(skill):
    d = skill(SKILL)
    assert not d.missing(PREDATES), d.missing(PREDATES)


def test_refuses_when_the_lease_is_held_by_another_session(skill):
    d = skill(SKILL)
    assert not d.missing(*LEASE_PARTS), d.missing(*LEASE_PARTS)


def test_refuses_when_owned_files_are_held(skill):
    """II-8 gives this refusal no text; the check is the preflight's `git status --short`."""
    d = skill(SKILL)
    phrases = ("git status --short", "owned file")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_dispatches_to_the_agent_types(skill):
    d = skill(SKILL)
    phrases = ("s2tdd:strong-diff-reviewer", "s2tdd:proxy-verifier")
    assert not d.missing(*phrases), d.missing(*phrases)
    # II-9: `s2tdd:packet-<tier>`, written either with the placeholder or one name per tier.
    generic = not d.missing("s2tdd:packet-<tier>")
    named = not d.missing(*(f"s2tdd:packet-{tier}" for tier in TIERS))
    assert generic or named, "no dispatch to s2tdd:packet-<tier>"
