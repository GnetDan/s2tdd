"""MIGRATING.md, README.md and CHANGELOG.md carry the migration material (T093, US3).

Shapes: II-15 (rename table), II-16 (product strings), the epic ticket's nine steps.
Assertion style (II-5): literals and listed phrases through `Doc.missing`, flattened text.
Red until MIGRATING.md (T072), README.md (T074) and CHANGELOG.md (T075) are written.

002 (T007; II-15, R10): README's FR-032 note gives way to the pilot note; the CHANGELOG 0.2.0
test keeps `FR032_NOTE`.
"""

from __future__ import annotations

import datetime
import re

import pytest

# tools/check.py COMMANDS (II-3), transcribed.
COMMANDS = (
    "epic",
    "specify",
    "clarify",
    "plan",
    "harden",
    "implement",
    "verify-done",
    "converge",
    "pr-review",
    "close",
    "next",
    "foundation-review",
    "constitution",
)

INSTALL_LINES = (
    "/plugin marketplace add GnetDan/s2tdd",
    "/plugin install s2tdd@s2tdd",
)

# II-16, exact.
FR032_NOTE = (
    "`--nobrakes`'s hand-off to a fresh session (including the scheduled-task start) "
    "and its brakes are carried over from the preset but untried in the field."
)
# 002 II-15, exact: replaces FR032_NOTE in README.md.
PILOT_NOTE = (
    "`--nobrakes` ran end to end in a first pilot on 0.2.0; from 0.3.0 a relay hands off by "
    "printing its prompt for you to paste, and never starts a session by itself."
)
COPY_FALLBACK = "Use the plugin or the copy, never both."

AUTO_DELETE_BRANCHES = "automatic deletion of head branches"

# II-15: (old forms, new form). Each row must sit on one line (a table row).
RENAME_ROWS = (
    (("/speckit-<x>",), "/s2tdd-<x>"),
    (("/speckit-tasks", "/speckit-harden"), "/s2tdd-harden"),
    (("/speckit-handoff",), "/s2tdd-implement --print"),
    (("/speckit-save",), "/s2tdd-next"),
    (("/speckit-branch",), "/s2tdd-specify"),
    (("/speckit-analyze", "/speckit-checklist", "/speckit-taskstoissues"), "none"),
    ((".specify/memory/constitution.md",), "specs/constitution.md"),
    (("docs/sdd-workflow.md",), "specs/WORKFLOW.md"),
)

# The epic ticket's nine steps, in order: one phrase per step, found as an ordered
# subsequence (each phrase after the end of the previous one).
STEP_PHRASES = (
    "close or pause",
    "uninstall",
    "/plugin install s2tdd@s2tdd",
    "keep and move",
    "rename table",
    "mid-flight",
    "verify",
    "start fresh",
    "uv tool uninstall specify-cli",
)

# The 0.2.0 heading reads "unreleased" until the release step (T089) dates it with an ISO date.
CHANGELOG_HEADING_RE = re.compile(
    r"^## 0\.2\.0 — (?P<when>unreleased|\d{4}-\d{2}-\d{2})[ \t]*$", re.MULTILINE
)
CHANGELOG_HEADING_WORDS = "'## 0.2.0 — unreleased' or '## 0.2.0 — YYYY-MM-DD'"
CHANGELOG_PHRASES = (
    "standalone plugin",
    "agent types",
    "first-run setup",
    "Test upkeep",
    "--print",
    "MIGRATING.md",
)


def _flat(text: str) -> str:
    """Same flattening as Doc.flat: lowercase, no backticks or asterisks, one space."""
    text = text.lower().replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", text).strip()


def _changelog_heading(text: str) -> "re.Match[str]":
    """The 0.2.0 heading match; a dated heading must be a real calendar date."""
    match = CHANGELOG_HEADING_RE.search(text)
    assert match, f"no {CHANGELOG_HEADING_WORDS} heading in CHANGELOG.md"
    when = match.group("when")
    if when != "unreleased":
        try:
            datetime.date.fromisoformat(when)
        except ValueError:
            raise AssertionError(f"the 0.2.0 heading date {when!r} is not a real date") from None
    return match


def _changelog_section(text: str) -> str:
    match = _changelog_heading(text)
    rest = text[match.end() :]
    following = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: following.start()] if following else rest


def _step(d, number: int) -> str:
    """The flattened text of the `## N.` section of MIGRATING.md (to the next `## `)."""
    match = re.search(rf"^## {number}\. .*$", d.body, re.MULTILINE)
    assert match, f"no '## {number}.' heading in MIGRATING.md"
    rest = d.body[match.end() :]
    following = re.search(r"^## ", rest, re.MULTILINE)
    return _flat(rest[: following.start()] if following else rest)


def _absent(section: str, *phrases: str) -> list[str]:
    return [p for p in phrases if _flat(p) not in section]


# --- MIGRATING.md -------------------------------------------------------------


def test_migrating_has_the_install_lines(doc):
    d = doc("MIGRATING.md")
    assert not d.missing(*INSTALL_LINES), d.missing(*INSTALL_LINES)


def test_migrating_has_the_nine_steps_in_order(doc):
    d = doc("MIGRATING.md")
    position = 0
    for phrase in STEP_PHRASES:
        found = d.flat.find(_flat(phrase), position)
        assert found != -1, f"step phrase {phrase!r} not found after offset {position}"
        position = found + len(_flat(phrase))


@pytest.mark.parametrize(
    ("olds", "new"), RENAME_ROWS, ids=[row[1] for row in RENAME_ROWS]
)
def test_migrating_rename_table_row(doc, olds, new):
    d = doc("MIGRATING.md")
    wanted = [_flat(item) for item in (*olds, new)]
    lines = [_flat(line) for line in d.body.split("\n")]
    assert any(all(w in line for w in wanted) for line in lines), (
        f"no line holds the rename row {olds} -> {new!r}"
    )


def test_migrating_reconciles_the_constitution_by_diff(doc):
    d = doc("MIGRATING.md")
    assert not d.missing("reconcile", "by diff"), d.missing("reconcile", "by diff")


def test_migrating_uninstalls_the_spec_kit_cli(doc):
    d = doc("MIGRATING.md")
    assert not d.missing("uv tool uninstall specify-cli"), "uv tool uninstall specify-cli"


def test_migrating_recommends_automatic_deletion_of_head_branches(doc):
    d = doc("MIGRATING.md")
    assert not d.missing(AUTO_DELETE_BRANCHES), AUTO_DELETE_BRANCHES


def test_migrating_is_worded_for_both_starting_points(doc):
    d = doc("MIGRATING.md")
    phrases = ("the tests-as-spec preset", "plain spec-kit")
    assert not d.missing(*phrases), d.missing(*phrases)


# --- MIGRATING.md, executable by an agent end to end (T102; amended 2026-10-03) ----


def test_migrating_step_2_says_the_remove_commands_are_optional(doc):
    step = _step(doc("MIGRATING.md"), 2)
    absent = _absent(step, "specify preset remove", "specify extension remove", "optional")
    assert not absent, f"step 2 lacks {absent}: the remove commands must be called optional"


def test_migrating_step_2_saves_the_constitution_before_removing_specify(doc):
    step = _step(doc("MIGRATING.md"), 2)
    saved = step.find("specs/constitution.md")
    assert saved != -1, "step 2 never moves the constitution into specs/constitution.md"
    assert "reconcil" in step, "step 2 never says to reconcile the constitution"
    removal = re.search(r"\b(delete|remov\w*|mov\w*|back\w*)\b[^.]*\.specify/(?!memory)", step)
    assert removal, "step 2 never removes or moves aside .specify/"
    assert saved < removal.start(), (
        f"step 2 saves the constitution (offset {saved}) after removing .specify/ "
        f"(offset {removal.start()})"
    )


def test_migrating_step_2_suggests_a_backup_outside_the_repository(doc):
    step = _step(doc("MIGRATING.md"), 2)
    assert "backup" in step, "step 2 never mentions a backup of the old folders"
    assert re.search(r"outside (the|this|your) (repository|repo|project)", step), (
        "step 2 never says the backup sits outside the repository"
    )


def test_migrating_step_3_gives_the_cli_form_beside_the_plugin_lines(doc):
    step = _step(doc("MIGRATING.md"), 3)
    wanted = (
        *INSTALL_LINES,
        "claude plugin marketplace add GnetDan/s2tdd",
        "claude plugin install s2tdd@s2tdd --scope user",
    )
    assert not _absent(step, *wanted), _absent(step, *wanted)


def test_migrating_step_7_or_8_starts_a_new_session_for_the_plugin_commands(doc):
    d = doc("MIGRATING.md")
    section = f"{_step(d, 7)} {_step(d, 8)}"
    assert re.search(r"\bnew session\b", section), "steps 7 and 8 never say to start a new session"
    assert re.search(r"\bload", section), "steps 7 and 8 never say the plugin's commands load"


# --- README.md ----------------------------------------------------------------


def test_readme_has_the_install_lines(doc):
    d = doc("README.md")
    assert not d.missing(*INSTALL_LINES), d.missing(*INSTALL_LINES)


def test_readme_has_the_copy_fallback_sentence(doc):
    d = doc("README.md")
    assert not d.missing(COPY_FALLBACK), COPY_FALLBACK


def test_readme_has_the_pilot_note(doc):
    d = doc("README.md")
    assert not d.missing(PILOT_NOTE), f"README.md lacks the new sentence: {PILOT_NOTE}"
    assert _flat(FR032_NOTE) not in d.flat, (
        f"README.md still holds the old sentence: {FR032_NOTE}"
    )


def test_readme_recommends_automatic_deletion_of_head_branches(doc):
    d = doc("README.md")
    assert not d.missing(AUTO_DELETE_BRANCHES), AUTO_DELETE_BRANCHES


def test_readme_names_each_of_the_13_commands(doc):
    d = doc("README.md")
    names = [f"/s2tdd-{name}" for name in COMMANDS]
    assert not d.missing(*names), d.missing(*names)


def test_readme_has_no_preset_packaging_instructions(doc):
    d = doc("README.md")
    assert d.missing("specify preset add") == ["specify preset add"], (
        "README still tells the reader to run `specify preset add`"
    )


# --- CHANGELOG.md -------------------------------------------------------------


def test_changelog_has_the_0_2_0_heading_above_0_1_0(doc):
    d = doc("CHANGELOG.md")
    match = _changelog_heading(d.text)
    assert match.start() < d.text.index("## 0.1.0"), (
        "the 0.2.0 entry is not above the 0.1.0 entry"
    )


def test_changelog_0_2_0_has_the_fr032_note(doc):
    section = _changelog_section(doc("CHANGELOG.md").text)
    assert _flat(FR032_NOTE) in _flat(section), FR032_NOTE


def test_changelog_0_2_0_names_what_changed(doc):
    section = _flat(_changelog_section(doc("CHANGELOG.md").text))
    absent = [p for p in CHANGELOG_PHRASES if _flat(p) not in section]
    assert not absent, absent


def test_changelog_0_2_0_mentions_ci(doc):
    section = _changelog_section(doc("CHANGELOG.md").text)
    assert re.search(r"\bCI\b", section), "the 0.2.0 entry never says CI"
