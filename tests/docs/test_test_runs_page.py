"""The pages and docs for per-wave test runs and the converge loop (T021; II-13, C-6, AT-3).

Expected red until T024 updates the pages and writes docs/test-runs.md. Each test file holds
its own constants (II-0), transcribed from the contract; tests/conftest.py is frozen, so the
row and section helpers live here.
"""

from __future__ import annotations

import re

import pytest

WORKFLOW_SRC = "src/pages/WORKFLOW.md"
WORKFLOW_COPIES = (
    "skills/s2tdd-specify/pages/WORKFLOW.md",
    "skills/s2tdd-epic/pages/WORKFLOW.md",
    "skills/s2tdd-constitution/pages/WORKFLOW.md",
)
TEST_RUNS_PAGE = "docs/test-runs.md"
NOBRAKES_PAGE = "docs/nobrakes.md"
MODELS_PAGE = "docs/models.md"
COMMANDS_PAGE = "docs/commands.md"
DEVELOPING_PAGE = "docs/developing.md"

# II-13 W1: the Suite speed row holds this; the old phrase is gone.
W1_PHRASE = (
    "packets run targeted tests, with one test run per wave: the project's per-wave command, "
    "the full suite at slice ends"
)
W1_GONE = "with one full suite per wave"

# II-13 W2 (amended 2026-10-04, T024): the same row names the three lines; the page links
# the test-runs page in its `## Unattended runs` section, never in `## Test upkeep` (whose
# links 001 US7-AC1 pins).
W2_PHRASES = ("Per-wave tests:", "Full suite:", "Per-wave sees:")
W2_LINK = "https://github.com/GnetDan/s2tdd/blob/main/docs/test-runs.md"
W2_UPKEEP_SECTION = "## Test upkeep"

# II-13 W3: the red-before-green bullet; the page lacks the old clause.
W3_PHRASE = (
    'then the implementation task whose done-when is "that test passes and the wave\'s test '
    'run is green"'
)
W3_GONE = "full suite is green"

# II-13 W4: the Unattended runs section holds each of these.
W4_SECTION = "## Unattended runs"
W4_PHRASES = ("carries on through converge to ready-to-close", "--nobrakes once")

# II-13: docs/test-runs.md links back and holds each of these.
TEST_RUNS_BACK_LINK = "[← Back to the README](../README.md)"
TEST_RUNS_PHRASES = (
    "Per-wave tests:",
    "Full suite:",
    "Per-wave sees:",
    "0 selected",
    "Per-wave runs off from wave <n>",
    "green at <sha>",
    "pytest-testmon",
    "--testmon-forceselect",
    "cache plugin",
    ".testmondata",
    ".gitignore",
    "Per-wave sees: *.py",
    "Keep testmon out of the Full suite: line",
    "modified files",
)

# II-13: docs/nobrakes.md holds each of these; step 5 is replaced.
NOBRAKES_PHRASES = (
    "--nobrakes once",
    "converger",
    "hardener",
    "READY TO CLOSE",
    # 003 FR-004, FR-003a: "When it stops" gains two bullets (II-13 amended 2026-10-04, round 3).
    "- the hardener stopping on one of harden's preconditions, with harden's message in the "
    "summary;",
    "- a packet still blocked when the waves end, before converge, naming it and the packets it "
    "skipped (a blocked MVP or guard test stops the run at once);",
)
NOBRAKES_STEP_5 = (
    "5. If it ended READY TO CLOSE, follow its Next block: pending checkpoints, the docs wave, "
    "then /s2tdd-pr-review and /s2tdd-close. A run started with --nobrakes once stops when "
    "every task is ticked: carry on with /s2tdd-converge."
)
NOBRAKES_STEP_5_GONE = "5. When every task is ticked, carry on with /s2tdd-converge."

# AT-3 (II-13: exact): docs/models.md's agent table gains these two rows.
MODELS_ROWS = (
    "| `converger` | Runs converge for you in an [unattended run](nobrakes.md) that loops to "
    "ready-to-close | opus, medium |",
    "| `hardener` | Hardens converge's appended tasks for you in an "
    "[unattended run](nobrakes.md) | opus, high |",
)
MODELS_ROW_ENDS = {"converger": "opus, medium", "hardener": "opus, high"}

# II-13: docs/commands.md's two rows, by their first cell.
COMMANDS_ROWS = {
    "/s2tdd-implement --nobrakes": "then converge rounds until the feature is ready to close",
    "/s2tdd-implement --nobrakes once": "stopping when every task is ticked",
}

# II-13: README.md's docs table gains a row starting with this.
README_ROW_START = "| [Test runs](docs/test-runs.md) |"

# II-13: docs/developing.md's two rows, by their first cell.
DEVELOPING_ROWS = {
    "agents/": ("The seven agent types", "The five agent types"),
    "evals/": ("The eval suite: the cases that run the commands in a real session", None),
}


def _flat(text: str) -> str:
    """Same flattening as Doc.flat (II-0)."""
    return " ".join(text.lower().replace("`", "").replace("*", "").split())


def _rows(body: str) -> dict[str, str]:
    """Each markdown table row's flattened first cell mapped to the flattened row."""
    rows: dict[str, str] = {}
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = stripped.strip("|").split("|")
        rows.setdefault(_flat(cells[0]), _flat(stripped))
    return rows


def _row(d, first_cell: str) -> str:
    rows = _rows(d.body)
    key = _flat(first_cell)
    assert key in rows, f"{d.path.name} has no table row for {first_cell!r}"
    return rows[key]


def _section(body: str, heading: str) -> str | None:
    """The flattened `## ` section starting with heading, to the next `## ` heading."""
    match = re.search(rf"^{re.escape(heading)}", body, re.MULTILINE)
    if not match:
        return None
    following = re.search(r"^## ", body[match.end() :], re.MULTILINE)
    end = match.end() + following.start() if following else len(body)
    return _flat(body[match.start() : end])


def _lines(d) -> list[str]:
    return [line.rstrip() for line in d.text.replace("\r\n", "\n").split("\n")]


def test_docs_workflow_suite_speed_row_says_one_test_run_per_wave(doc):
    d = doc(WORKFLOW_SRC)
    row = _row(d, "Suite speed")
    assert _flat(W1_PHRASE) in row, f"the Suite speed row lacks: {W1_PHRASE}"
    assert _flat(W1_GONE) not in d.flat, f"{WORKFLOW_SRC} still says {W1_GONE!r}"


def test_docs_workflow_suite_speed_row_names_the_lines_and_the_page(doc):
    d = doc(WORKFLOW_SRC)
    row = _row(d, "Suite speed")
    absent = [p for p in W2_PHRASES if _flat(p) not in row]
    assert not absent, f"the Suite speed row lacks {absent}"
    unattended = _section(d.body, W4_SECTION)
    assert unattended is not None, f"{WORKFLOW_SRC} has no {W4_SECTION!r} section"
    assert _flat(W2_LINK) in unattended, f"the Unattended runs section does not link {W2_LINK}"
    upkeep = _section(d.body, W2_UPKEEP_SECTION)
    assert upkeep is not None, f"{WORKFLOW_SRC} has no {W2_UPKEEP_SECTION!r} section"
    assert _flat(W2_LINK) not in upkeep, f"the Test upkeep section links {W2_LINK}"


def test_docs_workflow_red_before_green_says_the_wave_test_run(doc):
    d = doc(WORKFLOW_SRC)
    assert not d.missing(W3_PHRASE), f"{WORKFLOW_SRC} lacks: {W3_PHRASE}"
    assert _flat(W3_GONE) not in d.flat, f"{WORKFLOW_SRC} still says {W3_GONE!r}"


def test_docs_workflow_unattended_runs_loop_to_ready_to_close(doc):
    section = _section(doc(WORKFLOW_SRC).body, W4_SECTION)
    assert section is not None, f"{WORKFLOW_SRC} has no {W4_SECTION!r} section"
    absent = [p for p in W4_PHRASES if _flat(p) not in section]
    assert not absent, f"the Unattended runs section lacks {absent}"


@pytest.mark.parametrize("copy", WORKFLOW_COPIES)
def test_docs_workflow_stamped_copies_equal_the_source(repo_root, copy):
    source = (repo_root / WORKFLOW_SRC).read_bytes()
    assert (repo_root / copy).read_bytes() == source, f"{copy} differs from {WORKFLOW_SRC}"


def test_docs_test_runs_page_exists_and_links_back(repo_root, doc):
    assert (repo_root / TEST_RUNS_PAGE).is_file(), f"{TEST_RUNS_PAGE} not found"
    assert TEST_RUNS_BACK_LINK in doc(TEST_RUNS_PAGE).text, (
        f"{TEST_RUNS_PAGE} lacks {TEST_RUNS_BACK_LINK!r}"
    )


def test_docs_test_runs_page_holds_the_recipe(repo_root, doc):
    assert (repo_root / TEST_RUNS_PAGE).is_file(), f"{TEST_RUNS_PAGE} not found"
    absent = doc(TEST_RUNS_PAGE).missing(*TEST_RUNS_PHRASES)
    assert not absent, f"{TEST_RUNS_PAGE} lacks {absent}"


def test_docs_nobrakes_page_names_the_loop(doc):
    absent = doc(NOBRAKES_PAGE).missing(*NOBRAKES_PHRASES)
    assert not absent, f"{NOBRAKES_PAGE} lacks {absent}"


def test_docs_nobrakes_page_step_5_is_replaced(doc):
    d = doc(NOBRAKES_PAGE)
    assert not d.missing(NOBRAKES_STEP_5), f"{NOBRAKES_PAGE} lacks step 5: {NOBRAKES_STEP_5}"
    assert _flat(NOBRAKES_STEP_5_GONE) not in d.flat, (
        f"{NOBRAKES_PAGE} still holds the old step 5: {NOBRAKES_STEP_5_GONE}"
    )


def test_docs_models_page_has_the_converger_and_hardener_rows(doc):
    d = doc(MODELS_PAGE)
    lines = _lines(d)
    absent = [row for row in MODELS_ROWS if row not in lines]
    assert not absent, f"{MODELS_PAGE} lacks the rows {absent}"
    for agent, end in MODELS_ROW_ENDS.items():
        row = _row(d, agent)
        assert row.endswith(_flat(f"| {end} |")), f"the {agent} row does not end {end!r}"


@pytest.mark.parametrize("first_cell", sorted(COMMANDS_ROWS))
def test_docs_commands_page_implement_rows(doc, first_cell):
    phrase = COMMANDS_ROWS[first_cell]
    row = _row(doc(COMMANDS_PAGE), first_cell)
    assert _flat(phrase) in row, f"the {first_cell!r} row lacks {phrase!r}"


def test_docs_readme_lists_the_test_runs_page(doc):
    lines = _lines(doc("README.md"))
    assert any(line.startswith(README_ROW_START) for line in lines), (
        f"README.md has no row starting {README_ROW_START!r}"
    )


@pytest.mark.parametrize("first_cell", sorted(DEVELOPING_ROWS))
def test_docs_developing_page_rows(doc, first_cell):
    present, gone = DEVELOPING_ROWS[first_cell]
    d = doc(DEVELOPING_PAGE)
    row = _row(d, first_cell)
    assert _flat(present) in row, f"the {first_cell!r} row lacks {present!r}"
    if gone is not None:
        assert _flat(gone) not in d.flat, f"{DEVELOPING_PAGE} still says {gone!r}"
