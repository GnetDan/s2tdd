"""PR #8 review fixes D-2 and S-2: the docs wave's place in docs/nobrakes.md's table, and
close's docs-wave stop in docs/commands.md and WORKFLOW (II-0 style: own helpers, flattened).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NOBRAKES_PAGE = ROOT / "docs" / "nobrakes.md"
COMMANDS_PAGE = ROOT / "docs" / "commands.md"
WORKFLOW_PAGES = (
    ROOT / "src" / "pages" / "WORKFLOW.md",
    ROOT / "skills" / "s2tdd-specify" / "pages" / "WORKFLOW.md",
    ROOT / "skills" / "s2tdd-epic" / "pages" / "WORKFLOW.md",
    ROOT / "skills" / "s2tdd-constitution" / "pages" / "WORKFLOW.md",
)

# D-2: the docs wave is built last in every run; a looping run builds it only once a round
# converges, so a run that stops first leaves it unbuilt.
DOCS_WAVE_ROW_PHRASES = (
    "built and checked last in the run",
    "in a looping run, only once a round converges",
    "a run that stops first leaves it unbuilt",
    "left for you to commit",
)
DOCS_WAVE_STALE = "built and checked once the loop converges"

# S-2: close also stops while a docs wave a run built is uncommitted.
CLOSE_DOCS_WAVE = "the docs wave a run built is still uncommitted"


def _flat(text: str) -> str:
    return " ".join(text.lower().replace("`", "").replace("*", "").split())


def _row(path: Path, first_cell: str) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and _flat(cells[0]) == _flat(first_cell):
            return _flat(line)
    raise AssertionError(f"no table row starting {first_cell!r} in {path}")


def test_docs_wave_row_says_when_the_wave_is_built() -> None:
    row = _row(NOBRAKES_PAGE, "The docs wave")
    assert DOCS_WAVE_STALE not in row
    positions = []
    for phrase in DOCS_WAVE_ROW_PHRASES:
        assert phrase in row, phrase
        positions.append(row.index(phrase))
    assert positions == sorted(positions)


def test_commands_close_row_names_the_docs_wave_stop() -> None:
    row = _row(COMMANDS_PAGE, "/s2tdd-close")
    assert "converge hasn't passed since the last wave" in row
    assert CLOSE_DOCS_WAVE in row
    assert row.index("converge hasn't passed") < row.index(CLOSE_DOCS_WAVE)


def test_workflow_close_row_names_the_docs_wave_stop() -> None:
    for page in WORKFLOW_PAGES:
        row = _row(page, "Close")
        assert "needs a converge after the last wave" in row, page
        assert CLOSE_DOCS_WAVE in row, page
