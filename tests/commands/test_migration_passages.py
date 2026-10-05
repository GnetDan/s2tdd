"""T068: the migration passages of next, implement and harden (US3-AC2, US3-AC4, US3-AC7, FR-010, FR-022).

Each of the three commands holds one fenced migration passage (`<!-- s2tdd:migration -->`, II-1).
The tests read the passages through `Doc.migration_passages`, check each passage's literals and
listed phrases the way `Doc.missing` does (II-5), and finish with the repository-wide old-names
rule (II-3). The implement refusal text is II-8's; the rename table is II-15's. Test names carry
the command for `-k`.
"""

from __future__ import annotations

import dataclasses
import re

FENCE = "<!-- s2tdd:migration -->"


def _flatten(text: str) -> str:
    """Same flattening as `Doc.flat` (II-5): lowercase, no backticks or asterisks, one space."""
    return re.sub(r"\s+", " ", text.lower().replace("`", "").replace("*", "")).strip()


def _flat_passages(d) -> list[str]:
    assert d.migration_passages, f"no {FENCE} fence in {d.path.as_posix()}"
    return [_flatten(p) for p in d.migration_passages]


def _one_passage_holds(d, *phrases: str) -> None:
    """Some one migration passage holds every phrase (`Doc.missing` on that passage's text)."""
    passages = _flat_passages(d)
    gaps = [dataclasses.replace(d, flat=flat).missing(*phrases) for flat in passages]
    assert any(not gap for gap in gaps), (
        f"no migration passage in {d.path.as_posix()} holds every phrase; "
        f"the closest lacks {min(gaps, key=len)}"
    )


def _one_passage_matches(d, pattern: str, what: str) -> None:
    passages = _flat_passages(d)
    assert any(re.search(pattern, flat) for flat in passages), what


# next -------------------------------------------------------------------------------------


def test_next_has_a_migration_fence(skill):
    d = skill("s2tdd-next")
    assert d.migration_passages, f"no {FENCE} fence in skills/s2tdd-next/SKILL.md"


def test_next_fence_lists_the_spec_kit_leftovers_under_watch_out(skill):
    d = skill("s2tdd-next")
    _one_passage_holds(
        d,
        ".specify/",
        ".claude/skills/speckit-*/",
        "docs/sdd-workflow.md",
        "spec-kit",
        "leftovers",
        "watch out",
    )


# implement --------------------------------------------------------------------------------


def test_implement_has_a_migration_fence(skill):
    d = skill("s2tdd-implement")
    assert d.migration_passages, f"no {FENCE} fence in skills/s2tdd-implement/SKILL.md"


def test_implement_fence_stops_before_dispatching_attended_and_nobrakes(skill):
    d = skill("s2tdd-implement")
    _one_passage_holds(
        d,
        "/speckit-",
        "handoff.md",
        "orchestration.md",
        "before dispatching",
        "attended",
        "--nobrakes",
    )


def test_implement_fence_says_to_run_harden_handoff_first(skill):
    d = skill("s2tdd-implement")
    # II-8's refusal, after its `<file>` placeholder
    _one_passage_holds(
        d,
        "still names /speckit- commands: run `/s2tdd-harden handoff` first. "
        "Implement never rewrites it.",
    )


def test_implement_fence_never_rewrites_the_files(skill):
    d = skill("s2tdd-implement")
    _one_passage_matches(
        d,
        r"never rewrites?",
        "no migration passage says it never rewrites handoff.md or orchestration.md",
    )


# harden -----------------------------------------------------------------------------------

# II-15's command rows, old and new (the file rows are not applied by the `handoff` phase)
RENAME_COMMAND_ROWS = (
    "/speckit-<x>",
    "/s2tdd-<x>",
    "/speckit-tasks",
    "/speckit-harden",
    "/s2tdd-harden",
    "/speckit-handoff",
    "/s2tdd-implement --print",
    "/speckit-save",
    "/s2tdd-next",
    "/speckit-branch",
    "/s2tdd-specify",
    "/speckit-analyze",
    "/speckit-checklist",
    "/speckit-taskstoissues",
)


def test_harden_has_a_migration_fence(skill):
    d = skill("s2tdd-harden")
    assert d.migration_passages, f"no {FENCE} fence in skills/s2tdd-harden/SKILL.md"


def test_harden_fence_applies_the_rename_table_to_handoff_and_orchestration(skill):
    d = skill("s2tdd-harden")
    _one_passage_holds(
        d, "handoff", "handoff.md", "orchestration.md", "rename table", *RENAME_COMMAND_ROWS
    )


def test_harden_fence_leaves_validation_run_ledger_and_tasks_unchanged(skill):
    d = skill("s2tdd-harden")
    _one_passage_holds(d, "validation.md", "run-ledger.md", "tasks.md")
    _one_passage_matches(
        d,
        r"(unchanged|untouched|never (rewrites?|edits?|touch\w*|modif\w*|chang\w*)"
        r"|not (rewrit\w*|edit\w*|touch\w*|modif\w*|chang\w*))",
        "no migration passage says validation.md, run-ledger.md and tasks.md are left unchanged",
    )


# all files --------------------------------------------------------------------------------


def test_all_files_old_names_rule_exits_0(tool):
    result = tool("check", "--rule", "old-names")
    assert result.returncode == 0, result.stdout + result.stderr
