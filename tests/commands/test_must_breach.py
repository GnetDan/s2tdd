"""T013 (US6): a spec MUST breach is never parked as a note.

Pins II-2 phrases 8-11 (harden's prompt, outside NOBRAKES), II-5's `MUST breach:` report line,
II-7's finding line (harden's Strong-diff reviewer brief and `agents/strong-diff-reviewer.md`),
II-11's MUST sentence (verify-done) and II-12's phrases (converge). Phrases are transcribed from
specs/002-pilot-refresh/contracts/internal-interfaces.md; assertion style per II-0.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
VERIFY_DONE = "s2tdd-verify-done"
CONVERGE = "s2tdd-converge"
REVIEWER_AGENT = "agents/strong-diff-reviewer.md"

# II-2, phrases 8-11 (MUST BREACH; harden's prompt, in the main rules, not inside NOBRAKES).
MUST_BREACH = (
    "MUST BREACH. A review or shape-check finding that cites a spec MUST (MUST <FR-nnn | "
    "US<n>-AC<m> | EC-nnn>) is a blocker.",
    "It is never recorded under Open review notes.",
    "With MODE: nobrakes, the packet fixes it before the wave commit, or it is BLOCKED under "
    "FAILED FENCES.",
    "With MODE: attended, it heads the wave report: MUST breach: fix before the next wave · "
    "<finding line>.",
)

# II-5: the first line of harden's REPORT AFTER EVERY WAVE format (attended).
MUST_BREACH_REPORT_LINE = "MUST breach: fix before the next wave · <finding line>"
REPORT_FIRST_LINE_BEFORE = "Wave: <id>"

# II-7: the finding line, exact.
FINDING_LINE = (
    "<blocker|should|note>[ · MUST <FR-nnn|US<n>-AC<m>|EC-nnn>] · <file:line> · "
    "<failure scenario>"
)
# II-7: the Strong-diff reviewer brief's Findings line "becomes" this.
STRONG_DIFF_FINDINGS = f"Findings, one per line: {FINDING_LINE}."
OLD_FINDINGS = "Findings: blocker | should | note"  # the line II-7 replaces

# II-11: verify-done's MUST sentence.
VERIFY_DONE_MUST = (
    "A committed change that contradicts a spec MUST (a MUST <id> finding, or a change you can "
    "tie to an FR, scenario or MUST sentence in spec.md) is Not done."
)

# II-12: converge's From run-ledger.md paragraph in Load Artifacts.
CONVERGE_PHRASES = (
    "**From run-ledger.md**",
    "every line under Open review notes, and every Carried constraint marked carry to converge",
    "Each one still open becomes a finding and a task like any other gap; each one resolved is "
    "cited (the commit, test or decision that resolved it) in the summary, with no task.",
)

# II-2, phrase 1: the SHAPE CHECK head; MUST BREACH comes after it ("Then MUST BREACH").
SHAPE_CHECK_HEAD = "SHAPE CHECK (both modes; every wave that holds a test packet)"

NOBRAKES_START ="NOBRAKES (only when MODE is nobrakes; otherwise skip this section)"
STRONG_DIFF_HEADING = "### Strong-diff reviewer (read-only)"
REPORT_MARKER = "REPORT AFTER EVERY WAVE"
LOAD_ARTIFACTS_HEADING = "### 2. Load Artifacts"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _missing(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


def _outside_nobrakes(body: str) -> str:
    """The body without the NOBRAKES block (its first line through its closing ```` fence)."""
    lines = body.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.strip().startswith(NOBRAKES_START)), None)
    assert start is not None, f"NOBRAKES opening line not found: {NOBRAKES_START}"
    end = next((j for j in range(start + 1, len(lines)) if lines[j].strip() == "````"), None)
    assert end is not None, "NOBRAKES block's closing ```` fence not found"
    return "\n".join(lines[:start] + lines[end + 1 :])


def _subsection(body: str, heading: str) -> str:
    """From the line starting with `heading` to the next heading of the same or higher level."""
    lines = body.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.startswith(heading)), None)
    assert start is not None, f"heading not found: {heading}"
    level = len(heading) - len(heading.lstrip("#"))
    for j in range(start + 1, len(lines)):
        stripped = lines[j].lstrip("#")
        hashes = len(lines[j]) - len(stripped)
        if 0 < hashes <= level and stripped.startswith(" "):
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


def _report_format(body: str) -> str:
    """The code block that follows harden's REPORT AFTER EVERY WAVE item."""
    at = body.find(REPORT_MARKER)
    assert at >= 0, f"{REPORT_MARKER} not found in harden"
    opening = body.find("```", at)
    assert opening >= 0, "no report format block after REPORT AFTER EVERY WAVE"
    content_start = body.find("\n", opening) + 1
    closing = body.find("```", content_start)
    return body[content_start:closing]


# --- harden's main prompt (wave 2) -------------------------------------------------------------


def test_harden_must_breach_phrases_outside_nobrakes(skill):
    body = skill(HARDEN).body
    outside = _outside_nobrakes(body)
    missing = _missing(outside, *MUST_BREACH)
    assert not missing, missing
    # II-2: "Then MUST BREACH" -- its head lies after the SHAPE CHECK head (phrase 1).
    flat = _flatten(body)
    shape_at = flat.find(_flatten(SHAPE_CHECK_HEAD))
    assert shape_at >= 0, f"harden lacks: {SHAPE_CHECK_HEAD}"
    assert flat.find(_flatten(MUST_BREACH[0])) > shape_at, "MUST BREACH must follow SHAPE CHECK"


def test_harden_report_format_must_breach_line(skill):
    block = _report_format(skill(HARDEN).body)
    flat = _flatten(block)
    line = _flatten(MUST_BREACH_REPORT_LINE)
    assert line in flat, f"report format lacks: {MUST_BREACH_REPORT_LINE}"
    assert flat.index(line) < flat.index(_flatten(REPORT_FIRST_LINE_BEFORE)), (
        "the MUST breach line must head the report format (II-5: first line)"
    )


# --- harden's Strong-diff reviewer brief (wave 3) ----------------------------------------------


def test_harden_nb_strong_diff_findings_line(skill):
    brief = _subsection(skill(HARDEN).body, STRONG_DIFF_HEADING)
    missing = _missing(brief, STRONG_DIFF_FINDINGS)
    assert not missing, missing


def test_harden_nb_strong_diff_old_findings_line_gone(skill):
    brief = _subsection(skill(HARDEN).body, STRONG_DIFF_HEADING)
    assert _flatten(OLD_FINDINGS) not in _flatten(brief), f"still holds: {OLD_FINDINGS}"


# --- verify-done (wave 2) ----------------------------------------------------------------------


def test_verify_done_must_sentence_in_check_each_claim(skill):
    steps = _subsection(skill(VERIFY_DONE).body, "## Steps")
    missing = _missing(steps, VERIFY_DONE_MUST)
    assert not missing, missing


def test_verify_done_must_sentence_in_not_done(skill):
    output = _subsection(skill(VERIFY_DONE).body, "## Output")
    missing = _missing(output, VERIFY_DONE_MUST)
    assert not missing, missing


# --- converge (wave 2) -------------------------------------------------------------------------


def test_converge_run_ledger_paragraph_in_load_artifacts(skill):
    load = _subsection(skill(CONVERGE).body, LOAD_ARTIFACTS_HEADING)
    missing = _missing(load, *CONVERGE_PHRASES)
    assert not missing, missing


# --- agents/strong-diff-reviewer.md (wave 2) ---------------------------------------------------


def test_agents_strong_diff_reviewer_finding_line(doc):
    d = doc(REVIEWER_AGENT)
    assert not d.missing(FINDING_LINE), d.missing(FINDING_LINE)


def test_agents_strong_diff_reviewer_old_findings_line_gone(doc):
    d = doc(REVIEWER_AGENT)
    assert _flatten(OLD_FINDINGS) not in d.flat, f"still holds: {OLD_FINDINGS}"
