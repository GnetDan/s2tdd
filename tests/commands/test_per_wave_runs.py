"""T001 (003 US2): each wave runs only the tests its changes affect.

Pins II-2's project test lines (harden Phase C, its Mode section's refresh-mode paragraph and
its Completion Report), II-3's TEST RUN section and HOW TO WORK's wave-order clause, II-4's
ground rules 5 and 17 and the packet agents' rule 17, II-5's done-when wording (harden and
`skills/s2tdd-harden/tasks-template.md`) and II-6's wave report and attended stop. Phrases are
transcribed from specs/003-nobrakes-ready-to-close/contracts/internal-interfaces.md; assertion
style per II-0.
"""

from __future__ import annotations

import pytest

HARDEN = "s2tdd-harden"
TASKS_TEMPLATE = "skills/s2tdd-harden/tasks-template.md"
PACKET_AGENTS = ("agents/packet-cheap.md", "agents/packet-medium.md", "agents/packet-strong.md")

# II-2: the Project test lines paragraph in harden's Phase C, before C1.
PROJECT_TEST_LINES_START = "**Project test lines.**"
C1_START = "**C1."
PHASE_C_HEADING = "## Phase C"
L1 = (
    "Read three lines from the project's agent guidance file (CLAUDE.md, else AGENTS.md): "
    "Per-wave tests: <command>, Full suite: <command> and Per-wave sees: <glob>, <glob>, …"
)
L2 = (
    "Each label starts its line, after optional leading whitespace, and is matched "
    "case-insensitively; a line inside a fenced block counts, and a label anywhere else on a "
    "line does not. The command is the rest of the line, verbatim."
)
L3 = (
    "A second line with the same label, or Per-wave sees: without Per-wave tests:, is ignored "
    "and named in the Completion Report."
)
L4 = (
    "Without a Full suite: line, the full suite command is found as before: from the agent "
    "guidance file, otherwise the obvious one."
)
L5 = (
    "Copy them into TEST RUN's first line and the Proxy verifier brief's <full suite command>, "
    "with their measured minutes when known; a Per-wave tests: or Per-wave sees: line not "
    "declared is written none."
)
# II-2: refresh mode's paragraph in harden's Mode section.
REFRESH_START = "**Refresh mode**"
L6 = "Refresh mode also reads the project's test lines afresh (Phase C) and copies them in."
# II-2: the Completion Report's Phase C bullet.
COMPLETION_HEADING = "## Completion Report"
COMPLETION_PHASE_C_START = "- Phase C:"
L7 = "the project's test lines it copied, and each line it ignored with why"

# II-3: TEST RUN.
TR1 = "TEST RUN (both modes; once per wave)"
TR2 = (
    "Per-wave tests: <per-wave command | none> · Full suite: <full suite command> · "
    "Per-wave sees: <globs | none>"
)
TR3 = (
    "It is the per-wave command, run as written and passed nothing: picking the affected tests "
    "from the uncommitted tree is the project's tool's job, never yours."
)
TR4 = (
    "It is the full suite instead when no per-wave command is declared, when the wave changed a "
    "file outside Per-wave sees, or when per-wave runs are off."
)
TR5 = (
    "The wave's changed files are git diff --name-only HEAD and git ls-files --others "
    "--exclude-standard, in the app repository only; each Per-wave sees glob matches "
    "repository-relative paths, with * crossing /."
)
TR6 = (
    "A run whose output has the test runner's summary line ran, zero selected included: zero "
    "selected is green, written 0 selected."
)
TR7 = (
    "A run with no summary line failed to run: run the full suite for that wave, record the "
    "Carried constraint Per-wave runs off from wave <n>: <first error line>, and run the full "
    "suite at every later wave of the run."
)
TR8 = "The wave report's Test run: line names the run, its command, its counts and its wall time."
TEST_RUN = (TR1, TR2, TR3, TR4, TR5, TR6, TR7, TR8)
# 003 FR-011b (converge round 2, F2): II-3 TR9, added 2026-10-04, right after TR4, before TR5.
TR9 = (
    "Per-wave sees: none means the line was not declared: no change is outside it, and the "
    "per-wave command runs for every change."
)
HOW_TO_WORK_START = "- `HOW TO WORK`"
RED_TEST_PROTOCOL_START = "- `RED TEST PROTOCOL`"
NOBRAKES_START = "NOBRAKES (only when MODE is nobrakes; otherwise skip this section)"
# II-3: HOW TO WORK's wave-order clause, and the two phrases it replaces.
HW1 = (
    "after each wave: its reviews and shape check, then their fixes, then the wave's test run "
    "once, then the commit (never a second test run in a wave for a review fix)"
)
HW_GONE = ("then the full suite once", "never a second full suite in a wave for a review fix")

# II-4: harden's ground rules 5 and 17, each with the phrase it replaces.
R5 = "the orchestrator runs the wave's test run (TEST RUN) after each wave"
R5_GONE = "the orchestrator runs the test suite after each wave"
R17H = "Targeted tests in packets, one test run per wave, no stray processes."
R17H_GONE = "one full suite per wave"
R17C = (
    "the orchestrator's test run after the wave discharges every \"wave's test run is green\" "
    "clause, and the older \"full suite is green\" in a tasks.md hardened before 0.4.0"
)
R17C_GONE = (
    "the orchestrator's suite after the wave discharges every \"full suite is green\" clause"
)
# II-4: the three packet agents' rule 17.
AG17 = (
    "Run your done-when and the tests it names, never the full suite; the orchestrator's test "
    "run after the wave discharges every \"wave's test run is green\" clause, and the older "
    "\"full suite is green\" in a tasks.md hardened before 0.4.0."
)
AG17_GONE = "the orchestrator's suite after the wave discharges"

# II-5: done-when wording.
D1 = "Done-when: T011 passes and the wave's test run is green"
D2 = (
    "the implementation task's is \"<that test> passes and the wave's test run is green\""
)
D3_GONE = "passes and the full suite is green"
D4_TASK_END = "passes and the wave's test run is green"
D4_NOTES = (
    "implementation tasks: \"that test passes and the wave's test run is green\"",
    "Each wave commits itself once the wave's test run is green (one commit per wave)",
)
D4_GONE = ("full suite is green", "once the full suite is green")
D4_SAMPLE_TASKS = 4

# II-6: the wave report and the attended stop.
REPORT_START = "- `REPORT AFTER EVERY WAVE"
RP1 = "Commands run + results: <done-when outputs>"
RP1_GONE = "Commands run + results: <test summary line, done-when outputs>"
RP2 = (
    "Test run: per-wave · <command> · <passed> passed, <failed> failed, <selected> selected · "
    "<M>m<SS>s | full (<why>) · <command> · <passed> passed, <failed> failed · <M>m<SS>s"
)
RP3 = (
    "(<why>: no per-wave command, changed <first file> outside Per-wave sees, or per-wave runs "
    "off from wave <n>; zero selected is written 0 selected.)"
)
ATTENDED_STOP = "stop after the last wave in SCOPE"
RP4 = (
    "With MODE: attended, when any wave in SCOPE ran a per-wave run, end with the line Full run "
    "for this slice: /s2tdd-verify-done reports: <FEATURE_DIR>/s<k>-wave-reports.md; commits "
    "<first>..<last>"
)


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _missing(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


def _present(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) in flat]


def _line_at(lines: list[str], start: str, after: int = 0) -> int | None:
    return next((i for i in range(after, len(lines)) if lines[i].startswith(start)), None)


def _prompt_item(body: str, start: str) -> str:
    """One `- `-bullet of harden's Phase C1 prompt list: its line through the next such bullet."""
    lines = body.split("\n")
    at = _line_at(lines, start)
    assert at is not None, f"prompt item not found: {start}"
    end = next((j for j in range(at + 1, len(lines)) if lines[j].startswith("- `")), len(lines))
    return "\n".join(lines[at:end])


def _paragraph(body: str, start: str) -> str:
    """The blank-line-delimited paragraph whose first line starts with `start`."""
    lines = body.split("\n")
    at = _line_at(lines, start)
    assert at is not None, f"paragraph not found: {start}"
    end = next((j for j in range(at + 1, len(lines)) if not lines[j].strip()), len(lines))
    return "\n".join(lines[at:end])


def _section(body: str, heading: str) -> str:
    """From the line starting with `heading` to the next heading of the same or higher level."""
    lines = body.split("\n")
    start = _line_at(lines, heading)
    assert start is not None, f"heading not found: {heading}"
    level = len(heading) - len(heading.lstrip("#"))
    for j in range(start + 1, len(lines)):
        stripped = lines[j].lstrip("#")
        hashes = len(lines[j]) - len(stripped)
        if 0 < hashes <= level and stripped.startswith(" "):
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


# --- harden: II-2 project test lines (wave 1) ---------------------------------------------------


def test_harden_project_test_lines_before_c1(skill):
    body = skill(HARDEN).body
    lines = body.split("\n")
    phase_c = _line_at(lines, PHASE_C_HEADING)
    assert phase_c is not None, f"heading not found: {PHASE_C_HEADING}"
    at = _line_at(lines, PROJECT_TEST_LINES_START, phase_c)
    assert at is not None, f"harden's Phase C has no paragraph opening {PROJECT_TEST_LINES_START}"
    c1 = _line_at(lines, C1_START, phase_c)
    assert c1 is not None, f"harden's Phase C has no {C1_START}"
    assert at < c1, f"{PROJECT_TEST_LINES_START} is not before {C1_START}"
    missing = _missing("\n".join(lines[at:c1]), L1, L2, L3, L4, L5)
    assert not missing, f"harden's Project test lines paragraph lacks: {missing}"


def test_harden_refresh_mode_reads_test_lines(skill):
    para = _paragraph(skill(HARDEN).body, REFRESH_START)
    missing = _missing(para, L6)
    assert not missing, f"harden's refresh-mode paragraph lacks: {missing}"


def test_harden_completion_report_names_test_lines(skill):
    report = _section(skill(HARDEN).body, COMPLETION_HEADING)
    lines = report.split("\n")
    at = _line_at(lines, COMPLETION_PHASE_C_START)
    assert at is not None, f"Completion Report bullet not found: {COMPLETION_PHASE_C_START}"
    end = next((j for j in range(at + 1, len(lines)) if lines[j].startswith("- ")), len(lines))
    bullet = "\n".join(lines[at:end])
    missing = _missing(bullet, L7)
    assert not missing, f"harden's Completion Report Phase C bullet lacks: {missing}"


# --- harden: II-3 TEST RUN and HOW TO WORK (wave 1) ---------------------------------------------


def test_harden_test_run_phrases(skill):
    d = skill(HARDEN)
    missing = d.missing(*TEST_RUN)
    assert not missing, f"harden lacks II-3's TEST RUN phrases: {missing}"


def test_harden_test_run_per_wave_sees_none(skill):
    # 003 FR-011b (converge round 2, F2): II-3 TR9 sits after TR4 and before TR5.
    flat = _flatten(skill(HARDEN).body)
    assert _flatten(TR9) in flat, f"harden's TEST RUN lacks II-3 TR9: {TR9!r}"
    tr4 = flat.index(_flatten(TR4))
    tr9 = flat.index(_flatten(TR9))
    tr5 = flat.index(_flatten(TR5))
    assert tr4 < tr9 < tr5, "II-3 TR9 must sit after TR4 and before TR5"


def test_harden_test_run_between_how_to_work_and_red_test_protocol(skill):
    lines = skill(HARDEN).body.split("\n")
    how = _line_at(lines, HOW_TO_WORK_START)
    red = _line_at(lines, RED_TEST_PROTOCOL_START)
    assert how is not None, f"prompt item not found: {HOW_TO_WORK_START}"
    assert red is not None, f"prompt item not found: {RED_TEST_PROTOCOL_START}"
    span = "\n".join(lines[how:red])
    assert not _missing(span, TR1), (
        f"{TR1!r} is not between the HOW TO WORK and RED TEST PROTOCOL bullets"
    )
    nb = next((i for i, ln in enumerate(lines) if ln.strip().startswith(NOBRAKES_START)), None)
    assert nb is None or not (how <= nb < red), "the NOBRAKES block sits inside that span"


def test_harden_how_to_work_test_run_once(skill):
    item = _prompt_item(skill(HARDEN).body, HOW_TO_WORK_START)
    missing = _missing(item, HW1)
    assert not missing, f"harden's HOW TO WORK lacks: {missing}"
    present = _present(skill(HARDEN).body, *HW_GONE)
    assert not present, f"harden still holds: {present}"


# --- harden: II-4 ground rules 5 and 17 (wave 1) ------------------------------------------------


@pytest.mark.parametrize(
    ("new", "gone"),
    [(R5, R5_GONE), (R17H, R17H_GONE), (R17C, R17C_GONE)],
    ids=["rule_5", "rule_17_heading", "rule_17_clause"],
)
def test_harden_ground_rules_test_run(skill, new, gone):
    d = skill(HARDEN)
    assert not d.missing(new), f"harden lacks: {new!r}"
    assert _flatten(gone) not in d.flat, f"harden still holds: {gone!r}"


# --- harden: II-5 done-when wording (wave 1) ----------------------------------------------------


def test_harden_done_when_wave_test_run(skill):
    d = skill(HARDEN)
    missing = d.missing(D1, D2)
    assert not missing, f"harden lacks: {missing}"
    assert _flatten(D3_GONE) not in d.flat, f"harden still holds: {D3_GONE!r}"


def test_tasks_template_done_when_wave_test_run(doc):
    d = doc(TASKS_TEMPLATE)
    ends = [
        ln for ln in d.body.split("\n")
        if ln.startswith("- [ ] T") and _flatten(ln).endswith(_flatten(D4_TASK_END))
    ]
    assert len(ends) >= D4_SAMPLE_TASKS, (
        f"tasks-template has {len(ends)} sample tasks ending {D4_TASK_END!r}, "
        f"fewer than {D4_SAMPLE_TASKS}"
    )
    missing = d.missing(*D4_NOTES)
    assert not missing, f"tasks-template's Notes lack: {missing}"
    present = [p for p in D4_GONE if _flatten(p) in d.flat]
    assert not present, f"tasks-template still holds: {present}"


# --- harden: II-6 wave report and attended stop (wave 1) ----------------------------------------


def test_harden_report_test_run_line(skill):
    item = _prompt_item(skill(HARDEN).body, REPORT_START)
    missing = _missing(item, RP1, RP2, RP3)
    assert not missing, f"harden's REPORT AFTER EVERY WAVE lacks: {missing}"
    flat = _flatten(item)
    assert _flatten(RP1_GONE) not in flat, f"harden still holds: {RP1_GONE!r}"
    after_rp1 = flat[flat.index(_flatten(RP1)) + len(_flatten(RP1)):].lstrip()
    assert after_rp1.startswith(_flatten(RP2)), "RP2 is not the line right after RP1"


def test_harden_attended_stop_names_full_run(skill):
    item = _prompt_item(skill(HARDEN).body, REPORT_START)
    flat = _flatten(item)
    assert _flatten(ATTENDED_STOP) in flat, f"harden's report bullet lacks {ATTENDED_STOP!r}"
    assert _flatten(RP4) in flat, f"harden's attended stop lacks: {RP4!r}"
    assert flat.index(_flatten(RP4)) > flat.index(_flatten(ATTENDED_STOP)), (
        "RP4 is not after the attended stop instruction"
    )


# --- agents: II-4 AG17 (wave 1) -----------------------------------------------------------------


@pytest.mark.parametrize("agent", PACKET_AGENTS)
def test_agents_packet_rule_17_test_run(doc, agent):
    d = doc(agent)
    assert not d.missing(AG17), f"{agent} lacks AG17: {AG17!r}"
    assert _flatten(AG17_GONE) not in d.flat, f"{agent} still holds: {AG17_GONE!r}"
