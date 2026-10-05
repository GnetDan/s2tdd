"""T027, T068: reads by section (US5; II-4, II-9, II-10; FR-016, FR-017, FR-025, FR-031).

Implement's stale-name check searches both files with `grep -lE` inside its migration fence
(its pinned sentences kept, `read both files` gone) and its fill step reads by section;
harden's READ FIRST says how to read by section, B4 says each wave's row is one grep-able line,
and harden gains the old-command-name search (migration-fenced) and its gate. Every phrase is
transcribed from contracts/internal-interfaces.md (002; II-9 and II-10 as amended 2026-10-03).
These fail until T028, T029 and T069.
"""

from __future__ import annotations

import re

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"
FENCE = "<!-- s2tdd:migration -->"
FENCE_CLOSE = "<!-- /s2tdd:migration -->"

# II-10: the stale-name search (inside the migration fence; amended 2026-10-03, FR-031).
STALE_NAME_GREP = "grep -lE '/speckit-[a-z]'"
STALE_NAME_SEARCH = (
    "search both files with grep -lE '/speckit-[a-z]' <FEATURE_DIR>/handoff.md "
    "<FEATURE_DIR>/orchestration.md, which matches an old command name, never a bare quoted "
    "prefix; never read them into context for this check"
)
STALE_NAME_GONE = "read both files"

# The pinned sentences of tests/commands/test_migration_passages.py for implement (kept).
PINNED_PHRASES = (
    "/speckit-",
    "handoff.md",
    "orchestration.md",
    "before dispatching",
    "attended",
    "--nobrakes",
    "still names /speckit- commands: run `/s2tdd-harden handoff` first. "
    "Implement never rewrites it.",
)
PINNED_NEVER_REWRITES = r"never rewrites?"

# II-10: Fill.
FILL_PHRASES = (
    "read only handoff.md's fenced prompt, never the whole file",
    "read one Standard brief at a time, by its heading, when it is needed",
)

# II-4: READ FIRST (how to read).
READ_FIRST_PHRASES = (
    "list orchestration.md's headings with grep -n '^#' <FEATURE_DIR>/orchestration.md",
    "read the Ground rules section by its line range",
    "take the rows of the waves in SCOPE with grep '^| W<n> ' <FEATURE_DIR>/orchestration.md",
    "read each task by its ID",
    "During the wave loop, re-read a section only when run-ledger.md's Amendments show it "
    "changed since you read it.",
)

# II-4: Phase B, B4 (the wave table).
B4_ROW_SENTENCE = (
    "Each wave's row is one table line whose first cell begins W<n>, and each section sits "
    "under its own heading, so an orchestrator can read them by grep."
)

# II-9: old command names in the prompt files (FR-031; added 2026-10-03).
OLD_NAMES_SEARCH = (
    "grep -lE '/speckit-[a-z]' <FEATURE_DIR>/orchestration.md <FEATURE_DIR>/handoff.md"
)
OLD_NAMES_REWORD = "Reword every hit"
OLD_NAMES_QUOTE = "quote old command names only in tasks.md, contracts/ or tests"
OLD_NAMES_GATE = "orchestration.md and handoff.md name no old command"

# Structural anchors of harden and implement (each must exist today).
READ_FIRST_MARK = "- READ FIRST, IN THIS ORDER:"
SCOPE_MARK = "- SCOPE:"
B4_START = "**B4."
B5_START = "**B5."
VALIDATION_GATES_HEADING = "## Validation Gates"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _where(name: str) -> str:
    return f"skills/{name}/SKILL.md"


def _flat_passages(d) -> list[str]:
    assert d.migration_passages, f"no {FENCE} fence in {d.path.as_posix()}"
    return [_flatten(p) for p in d.migration_passages]


def _passages_holding(d, anchor: str) -> list[str]:
    """The flattened migration passages that hold the anchor; fail when none does."""
    found = [flat for flat in _flat_passages(d) if _flatten(anchor) in flat]
    assert found, f"`{anchor}` missing from {d.path.parent.name}'s migration passages"
    return found


def _missing_in(flat: str, phrases: tuple[str, ...]) -> list[str]:
    return [p for p in phrases if _flatten(p) not in flat]


def _at(flat: str, phrase: str, where: str, start: int = 0) -> int:
    i = flat.find(_flatten(phrase), start)
    assert i >= 0, f"`{phrase}` missing from {where}"
    return i


def _line_at(lines: list[str], prefix: str, where: str, start: int = 0) -> int:
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    raise AssertionError(f"`{prefix}` missing from {where}")


def _section_lines(body: str, heading: str, where: str) -> list[str]:
    """The lines of the `## ` section whose heading line starts with `heading`, up to the next
    `# ` or `## ` heading outside a code block; fail when the heading is absent."""
    lines = body.split("\n")
    start = _line_at(lines, heading, where)
    out: list[str] = []
    in_code = False
    for line in lines[start + 1 :]:
        if line.lstrip().startswith("```"):
            in_code = not in_code
        elif not in_code and (line.startswith("# ") or line.startswith("## ")):
            break
        out.append(line)
    return out


def _outside_fences(lines: list[str]) -> list[str]:
    out: list[str] = []
    inside = False
    for line in lines:
        if line == FENCE:
            inside = True
        elif line == FENCE_CLOSE:
            inside = False
        elif not inside:
            out.append(line)
    return out


# --- implement (II-10) ----------------------------------------------------------------------


def test_implement_stale_name_check_searches_inside_the_migration_fence(skill):
    d = skill(IMPLEMENT)
    passages = _passages_holding(d, STALE_NAME_GREP)
    gaps = []
    for flat in passages:
        gap = _missing_in(flat, (STALE_NAME_SEARCH, *PINNED_PHRASES))
        if not re.search(PINNED_NEVER_REWRITES, flat):
            gap.append("never rewrites")
        gaps.append(gap)
    assert any(not gap for gap in gaps), (
        f"no migration passage in {_where(IMPLEMENT)} holds II-10's stale-name search with the "
        f"pinned sentences; the closest lacks {min(gaps, key=len)}"
    )


def test_implement_lacks_read_both_files(skill):
    d = skill(IMPLEMENT)
    assert _flatten(STALE_NAME_GONE) not in d.flat, (
        f"`{STALE_NAME_GONE}` still in {_where(IMPLEMENT)}"
    )


def test_implement_fill_reads_by_section(skill):
    d = skill(IMPLEMENT)
    missing = d.missing(*FILL_PHRASES)
    assert not missing, f"missing from {_where(IMPLEMENT)}: {missing}"


# --- harden: reading by section (II-4) ------------------------------------------------------


def test_harden_read_first_reads_by_section(skill):
    d = skill(HARDEN)
    where = _where(HARDEN)
    start = _at(d.flat, READ_FIRST_MARK, where)
    end = _at(d.flat, SCOPE_MARK, where, start)
    missing = _missing_in(d.flat[start:end], READ_FIRST_PHRASES)
    assert not missing, f"missing from {HARDEN}'s READ FIRST: {missing}"


def test_harden_b4_wave_rows_are_one_line_each(skill):
    d = skill(HARDEN)
    where = _where(HARDEN)
    lines = d.body.split("\n")
    start = _line_at(lines, B4_START, where)
    end = _line_at(lines, B5_START, where, start + 1)
    missing = _missing_in(_flatten("\n".join(lines[start:end])), (B4_ROW_SENTENCE,))
    assert not missing, f"missing from {HARDEN}'s B4: {missing}"


# --- harden: old command names (II-9, FR-031) -----------------------------------------------


def test_harden_old_names_search_inside_a_migration_fence(skill):
    d = skill(HARDEN)
    passages = _passages_holding(d, OLD_NAMES_REWORD)
    phrases = (OLD_NAMES_SEARCH, OLD_NAMES_REWORD, OLD_NAMES_QUOTE)
    gaps = [_missing_in(flat, phrases) for flat in passages]
    assert any(not gap for gap in gaps), (
        f"no migration passage in {_where(HARDEN)} holds II-9's old-command-name search; "
        f"the closest lacks {min(gaps, key=len)}"
    )


def test_harden_old_names_gate_in_validation_gates(skill):
    d = skill(HARDEN)
    where = _where(HARDEN)
    section = _outside_fences(_section_lines(d.body, VALIDATION_GATES_HEADING, where))
    missing = _missing_in(_flatten("\n".join(section)), (OLD_NAMES_GATE,))
    assert not missing, (
        f"missing from {HARDEN}'s Validation Gates (outside a migration fence): {missing}"
    )
