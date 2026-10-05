"""US2 acceptance tests: no Sonnet in the default agent types (T005; II-1, II-15).

Expected red until T010 (AC1, AC2: the agents' frontmatter) and T011 (AC3: the pages).
Each test file holds its own constants (II-0), transcribed from the contract.
"""

from __future__ import annotations

# II-1 (002 FR-004; supersedes 001 research.md R10's models): file stem -> (model, effort).
AGENT_MODELS = {
    "packet-cheap": ("opus", "low"),
    "packet-medium": ("opus", "medium"),
    "packet-strong": ("opus", "high"),
    "strong-diff-reviewer": ("opus", "high"),
    "proxy-verifier": ("opus", "medium"),
}

# II-15: the user-facing pages, README first.
PAGES = (
    "README.md",
    "docs/models.md",
    "docs/nobrakes.md",
    "src/pages/WORKFLOW.md",
    "skills/s2tdd-specify/pages/WORKFLOW.md",
    "skills/s2tdd-epic/pages/WORKFLOW.md",
    "skills/s2tdd-constitution/pages/WORKFLOW.md",
)
SHAPE_CHECK = "shape check"
SONNET = "sonnet"
MODELS_PAGE = "docs/models.md"
REVIEWER_ROW_PHRASE = "and each wave's shape check"


def _flat(text: str) -> str:
    """Same flattening as Doc.flat (II-0)."""
    return " ".join(text.lower().replace("`", "").replace("*", "").split())


def _cells(line: str) -> list[str]:
    """A Markdown table row's cells, stripped; [] when the line is not a table row."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _agent_rows(body: str, stem: str) -> list[list[str]]:
    """The table rows whose first cell names the agent type `stem`."""
    rows = []
    for line in body.split("\n"):
        cells = _cells(line)
        if cells and cells[0].replace("`", "").strip() == stem:
            rows.append(cells)
    return rows


def test_002_us2_ac1_no_sonnet(doc):
    """US2-AC1: **Given** the plugin's agent types, **When** their model settings are read,
    **Then** none of them is Sonnet.

    Provenance: 002 spec.md
    """
    for stem in sorted(AGENT_MODELS):
        d = doc(f"agents/{stem}.md")
        model = str(d.frontmatter.get("model", ""))
        assert model.lower() != SONNET, f"agents/{stem}.md has model: {model}"
    for stem in sorted(AGENT_MODELS):
        d = doc(f"agents/{stem}.md")
        assert SONNET not in d.text.lower(), f"agents/{stem}.md contains {SONNET!r}"


def test_002_us2_ac2_models_and_efforts(doc):
    """US2-AC2: **Given** the plugin's agent types, **When** each one's model and effort are
    read, **Then** they match FR-004's table.

    Provenance: 002 spec.md
    """
    for stem in sorted(AGENT_MODELS):
        d = doc(f"agents/{stem}.md")
        model, effort = AGENT_MODELS[stem]
        actual_model = d.frontmatter.get("model")
        actual_effort = d.frontmatter.get("effort")
        assert actual_model == model, (
            f"agents/{stem}.md has model: {actual_model}, not {model}"
        )
        assert actual_effort == effort, (
            f"agents/{stem}.md has effort: {actual_effort}, not {effort}"
        )


def test_002_us2_ac3_pages_match(doc):
    """US2-AC3: **Given** the user-facing pages (README, the models page, the unattended-runs
    page and the project workflow page), **When** they describe the agent types and the
    reviews, **Then** they match the shipped agent types and describe the per-wave shape check.

    Provenance: 002 spec.md
    """
    for page in PAGES:
        d = doc(page)
        assert not d.missing(SHAPE_CHECK), f"{page} lacks `{SHAPE_CHECK}`"
    for page in PAGES:
        d = doc(page)
        assert SONNET not in d.text.lower(), f"{page} contains {SONNET!r}"

    models = doc(MODELS_PAGE)
    for stem in sorted(AGENT_MODELS):
        agent = doc(f"agents/{stem}.md")
        wanted = f"{agent.frontmatter.get('model')}, {agent.frontmatter.get('effort')}"
        rows = _agent_rows(models.body, stem)
        assert len(rows) == 1, f"{MODELS_PAGE} has {len(rows)} agent-type rows for {stem}, not 1"
        last = rows[0][-1]
        assert _flat(last) == _flat(wanted), (
            f"{MODELS_PAGE}'s {stem} row ends {last!r}, not {wanted!r}"
        )

    reviewer = _agent_rows(models.body, "strong-diff-reviewer")[0]
    row = _flat(" | ".join(reviewer))
    assert _flat(REVIEWER_ROW_PHRASE) in row, (
        f"{MODELS_PAGE}'s strong-diff-reviewer row lacks {REVIEWER_ROW_PHRASE!r}"
    )
