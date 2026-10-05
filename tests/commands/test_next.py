"""T021: `skills/s2tdd-next/SKILL.md`.

Pins the contract's required elements (II-1 fences, II-6 shape, contracts/commands.md's next
row, FR-013, FR-015, EC-003) through `Doc.missing` (II-5): literals and listed phrases only.
The Watch out items other tasks add (T054, T060, T064, T069) have their own test files.
"""

from __future__ import annotations

import re

SKILL = "s2tdd-next"
NEXT_FENCES = ["epic-resolution", "feature-resolution", "worktrees"]  # II-1; no closing-step
COMMANDS = (  # II-3's constant (type home: tools/check.py); tests transcribe
    "epic", "specify", "clarify", "plan", "harden", "implement", "verify-done",
    "converge", "pr-review", "close", "next", "foundation-review", "constitution",
)
_COMMAND_REF = re.compile(r"(?<![\w.])/s2tdd-([a-z]+(?:-[a-z]+)*)")
_OLD_COMMAND_REF = re.compile(r"(?<![\w.])/speckit-")


def _outside_migration(d):
    """The body without its migration fences (those may name old commands, R6)."""
    text = d.body
    for passage in d.migration_passages:
        text = text.replace(passage, "")
    return text


def test_frontmatter_name(skill):
    d = skill(SKILL)
    assert d.frontmatter.get("name") == SKILL, d.frontmatter


def test_input_sentence(skill):
    d = skill(SKILL)
    assert not d.missing("the text the user typed after the command"), d.missing(
        "the text the user typed after the command"
    )


def test_save_stages_only_the_directory(skill):
    """The save stages the feature's or epic's directory and the first-run pages, nothing
    from other work; `constitution.md` is the one further file (FR-013, see the next test)."""
    d = skill(SKILL)
    phrases = (
        "git -C specs status --short",
        "git -C specs push",
        "specs/README.md",
        "specs/WORKFLOW.md",
        "specs/epics/<slug>/",
    )
    assert not d.missing(*phrases), d.missing(*phrases)
    assert re.search(r"never force[^.]*rebase[^.]*pull", d.flat), "no 'never force, rebase or pull'"


def test_save_stages_constitution_when_new_or_changed(skill):
    """T096 (FR-013, amended 2026-10-02, user): beside the feature's or epic's directory,
    next's save also stages `constitution.md` of the specs repository when it is new or
    changed. Only the literal is pinned."""
    d = skill(SKILL)
    assert not d.missing("constitution.md"), "the save step does not name constitution.md"


def test_ec003_no_upstream_commits_and_still_prints_next(skill):
    """EC-003: with no remote, next commits, says the push was skipped and why, and still
    prints the next step."""
    d = skill(SKILL)
    assert not d.missing("upstream", "next step"), d.missing("upstream", "next step")
    assert re.search(r"push[^.]*skipped|skip[^.]*push", d.flat), "no 'push was skipped' statement"


def test_specs_not_its_own_repository_commits_nothing(skill):
    d = skill(SKILL)
    phrases = ("git -C specs rev-parse --show-toplevel", "commit nothing")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_routing_names_only_s2tdd_commands(skill):
    d = skill(SKILL)
    outside = _outside_migration(d)
    assert not _OLD_COMMAND_REF.search(outside), "a /speckit- command outside a migration fence"
    named = set(_COMMAND_REF.findall(outside))
    assert named, "no /s2tdd- command named"
    assert named <= set(COMMANDS), f"not among the 13 commands: {sorted(named - set(COMMANDS))}"
    phrases = ("/s2tdd-specify", "/s2tdd-plan", "/s2tdd-harden", "/s2tdd-implement",
               "/s2tdd-converge", "/s2tdd-close")
    assert not d.missing(*phrases), d.missing(*phrases)


def test_routing_has_no_tasks_save_branch_or_handoff_row(skill):
    d = skill(SKILL)
    gone = [c for c in ("/s2tdd-tasks", "/s2tdd-save", "/s2tdd-branch", "/s2tdd-handoff")
            if c in d.text]
    assert not gone, f"commands that no longer exist: {gone}"


def test_offers_implement_print_for_another_harness(skill):
    d = skill(SKILL)
    assert not d.missing("/s2tdd-implement --print"), d.missing("/s2tdd-implement --print")


def test_no_sidebar_grouping_step(skill):
    d = skill(SKILL)
    lowered = d.text.lower()
    assert "ccd_sidebar" not in lowered, "ccd_sidebar named"
    assert "sidebar" not in lowered, "sidebar named"


def test_read_only_on_the_project(skill):
    d = skill(SKILL)
    stated = re.search(
        r"read-only|nothing in the project|never (commits|touches|modifies|writes)[^.]*project",
        d.flat,
    )
    assert stated, "the command does not say it stays read-only on the project"


def test_shared_fences(skill):
    d = skill(SKILL)
    assert sorted(d.shared_blocks) == NEXT_FENCES, d.shared_blocks


def _section(d, heading: str) -> str:
    """The flattened text from `heading` up to the next `###` heading."""
    start = d.body.index(heading)
    end = d.body.find("\n### ", start + len(heading))
    text = d.body[start : end if end != -1 else None]
    return " ".join(text.lower().replace("`", "").replace("*", "").split())


def test_routing_skips_pending_checkpoints(skill):
    """Close-time CHECKPOINT tasks stay unticked until /s2tdd-close decides them; the rows
    that count unticked tasks must ignore them, or a feature whose only open tasks are
    checkpoints is sent back to implement (or harden) forever instead of on to close."""
    table = _section(skill(SKILL), "### 4a. Decide the next step (feature mode")
    for phrase in (
        "whose description begins checkpoint",
        "after any [p] and [usn] markers",
        "every row above that counts unticked tasks ignores them",
        "only unticked tasks are pending checkpoints goes on to converge, the pr and close",
    ):
        assert phrase in table, (phrase, table)
