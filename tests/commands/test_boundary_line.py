"""T037 (US13): wave-boundary bookkeeping cannot be skipped silently.

Pins II-5's `Boundary:` report line (slots included) and its sentence in harden's REPORT AFTER
EVERY WAVE, II-8's BOUNDARY paragraph in harden's NOBRAKES block (after HANDOFF), and II-11's
Boundary sentence in verify-done. Phrases are transcribed from
specs/002-pilot-refresh/contracts/internal-interfaces.md; assertion style per II-0.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
VERIFY_DONE = "s2tdd-verify-done"

# II-5: the Boundary line of the wave report format, slots included (--nobrakes only).
BOUNDARY_LINE = (
    "Boundary: context <x>% · five-hour <y>% · week <z>% · BRAKES <none|found> · "
    "ledger +<n> lines"
)
# II-5: the sentence the report format in harden carries with it.
BOUNDARY_SENTENCE = (
    "With MODE: nobrakes, every wave report carries the Boundary line, written from the steps "
    "you ran at that boundary."
)

# II-8: the BOUNDARY paragraph (a NOBRAKES paragraph after HANDOFF).
BOUNDARY_PARAGRAPH = (
    "BOUNDARY. After each wave commit, read usage, check for BRAKES and append the ledger's "
    "lines, then write Boundary: context <x>% · five-hour <y>% · week <z>% · BRAKES "
    "<none|found> · ledger +<n> lines in that wave's report."
)

# II-11: verify-done's Boundary sentence.
VERIFY_DONE_BOUNDARY = (
    "A wave that run-ledger.md places in a --nobrakes run, whose wave report has no Boundary: "
    "line, is a gap."
)

# 003 FR-006, EC-003 (converge round 3): II-7 BD2, added 2026-10-04, ends the BOUNDARY paragraph,
# after BD2_AFTER; the pinned BOUNDARY sentence above is unchanged.
BD2 = (
    "At a phase change, which has no wave report, write the Boundary line under the ledger's "
    "Usage section instead."
)
BD2_AFTER = "so none is skipped silently."
BOUNDARY_MARKER = "BOUNDARY. "

REPORT_ITEM_START = "- `REPORT AFTER EVERY WAVE"
REPORT_MARKER = "REPORT AFTER EVERY WAVE"
NOBRAKES_START = "NOBRAKES (only when MODE is nobrakes; otherwise skip this section)"
HANDOFF_MARKER = "HANDOFF. "


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _missing(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


def _prompt_item(body: str, start: str) -> str:
    """One `- `-bullet of harden's Phase C1 prompt list: its line through the next such bullet."""
    lines = body.split("\n")
    at = next((i for i, ln in enumerate(lines) if ln.startswith(start)), None)
    assert at is not None, f"prompt item not found: {start}"
    end = next((j for j in range(at + 1, len(lines)) if lines[j].startswith("- `")), len(lines))
    return "\n".join(lines[at:end])


def _report_format(body: str) -> str:
    """The code block inside harden's REPORT AFTER EVERY WAVE prompt item (never a later one)."""
    item = _prompt_item(body, REPORT_ITEM_START)
    assert REPORT_MARKER in item, f"{REPORT_MARKER} not found in harden"
    opening = item.find("```")
    assert opening >= 0, "no report format block inside REPORT AFTER EVERY WAVE"
    content_start = item.find("\n", opening) + 1
    closing = item.find("```", content_start)
    assert content_start > 0 and closing >= 0, "report format block is not closed in its item"
    return item[content_start:closing]


def _nobrakes(body: str) -> list[str]:
    """The NOBRAKES block's lines: its opening line through its closing ```` fence."""
    lines = body.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.strip().startswith(NOBRAKES_START)), None)
    assert start is not None, f"NOBRAKES opening line not found: {NOBRAKES_START}"
    end = next((j for j in range(start + 1, len(lines)) if lines[j].strip() == "````"), None)
    assert end is not None, "NOBRAKES block's closing ```` fence not found"
    return lines[start:end]


# --- harden's main prompt (wave 2) -------------------------------------------------------------


def test_harden_report_format_boundary_line(skill):
    block = _report_format(skill(HARDEN).body)
    missing = _missing(block, BOUNDARY_LINE)
    assert not missing, f"harden's report format lacks: {missing}"


def test_harden_report_boundary_sentence(skill):
    item = _prompt_item(skill(HARDEN).body, REPORT_ITEM_START)
    missing = _missing(item, BOUNDARY_SENTENCE)
    assert not missing, f"harden's REPORT AFTER EVERY WAVE lacks: {missing}"


# --- harden's NOBRAKES block (wave 3) ----------------------------------------------------------


def test_harden_nb_boundary_paragraph(skill):
    block = "\n".join(_nobrakes(skill(HARDEN).body))
    missing = _missing(block, BOUNDARY_PARAGRAPH)
    assert not missing, f"harden's NOBRAKES lacks BOUNDARY.: {missing}"


def test_harden_nb_boundary_paragraph_after_handoff(skill):
    lines = _nobrakes(skill(HARDEN).body)
    at = next((i for i, ln in enumerate(lines) if ln.strip().startswith(HANDOFF_MARKER)), None)
    assert at is not None, f"NOBRAKES has no {HANDOFF_MARKER.strip()} paragraph"
    missing = _missing("\n".join(lines[at:]), BOUNDARY_PARAGRAPH)
    assert not missing, f"no BOUNDARY. paragraph after HANDOFF in NOBRAKES: {missing}"


def test_harden_nb_boundary_paragraph_ends_with_phase_change_line(skill):
    # 003 FR-006, EC-003: II-7 BD2 is the BOUNDARY paragraph's last sentence.
    lines = _nobrakes(skill(HARDEN).body)
    at = next((i for i, ln in enumerate(lines) if ln.strip().startswith(BOUNDARY_MARKER)), None)
    assert at is not None, f"NOBRAKES has no {BOUNDARY_MARKER.strip()} paragraph"
    end = next((j for j in range(at + 1, len(lines)) if not lines[j].strip()), len(lines))
    paragraph = _flatten("\n".join(lines[at:end]))
    assert paragraph.endswith(_flatten(BD2)), (
        f"harden's BOUNDARY paragraph does not end with II-7 BD2: {BD2!r}"
    )
    assert paragraph.find(_flatten(BD2_AFTER)) >= 0, f"BOUNDARY paragraph lacks {BD2_AFTER!r}"
    assert paragraph.find(_flatten(BD2_AFTER)) < paragraph.find(_flatten(BD2)), (
        f"II-7 BD2 must follow {BD2_AFTER!r}"
    )
    assert paragraph.endswith(_flatten(BD2_AFTER + " " + BD2)), (
        f"II-7 BD2 must follow {BD2_AFTER!r} directly, with nothing between them"
    )


# --- verify-done (wave 2) ----------------------------------------------------------------------


def test_verify_done_missing_boundary_line_is_a_gap(skill):
    d = skill(VERIFY_DONE)
    assert not d.missing(VERIFY_DONE_BOUNDARY), d.missing(VERIFY_DONE_BOUNDARY)
