"""T033, T035: harden's wave-table checks (US9, US10; II-9; FR-023, FR-024).

Phase B keeps a contract section's consumer out of its producer's wave (same-wave tests) and
searches the test tree for every superseded shape, listing the searches in orchestration.md under
`### Superseded-shape searches` (superseded tests); *Validation Gates* gains a gate for each.
Every phrase is transcribed from contracts/internal-interfaces.md (002). These fail until T034
and T036.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
WHERE = f"skills/{HARDEN}/SKILL.md"

# II-9, first phrase: the same-wave rule (Phase B).
SAME_WAVE_ANCHOR = "the consumer moves to a later wave"
SAME_WAVE_RULE = (
    "No task goes in the same wave as a task that produces a contract section it cites: the "
    "consumer moves to a later wave. This is read from the contracts' citations, never from "
    "source analysis."
)
SAME_WAVE_GATE = "no task shares a wave with a task that produces a contract section it cites"

# II-9, second phrase: the superseded-shape search (Phase B).
SUPERSEDED_HEADING = "### Superseded-shape searches"
SUPERSEDED_RULE = (
    "For each contract section marked supersedes, or changing an existing signature, search the "
    "test tree for the shape's names; give each file found a test task in the first wave that "
    "changes the shape; list every search and its hits in orchestration.md under "
    "### Superseded-shape searches."
)
SUPERSEDED_GATE = "every superseded-shape search is listed in orchestration.md"

# Structural anchors of harden (each must exist today).
PHASE_B_HEADING = "## Phase B"
VALIDATION_GATES_HEADING = "## Validation Gates"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _section(body: str, heading: str) -> str:
    """The flattened `## ` section whose heading line starts with `heading`, up to the next
    `# ` or `## ` heading outside a code block; fail when the heading is absent."""
    lines = body.split("\n")
    starts = [i for i, line in enumerate(lines) if line.startswith(heading)]
    assert starts, f"heading `{heading}` missing from {WHERE}"
    out: list[str] = []
    in_code = False
    for line in lines[starts[0] + 1 :]:
        if line.lstrip().startswith("```"):
            in_code = not in_code
        elif not in_code and (line.startswith("# ") or line.startswith("## ")):
            break
        out.append(line)
    return _flatten("\n".join(out))


def _holds(flat: str, phrase: str, where: str) -> None:
    assert _flatten(phrase) in flat, f"`{phrase}` missing from {where}"


# --- same wave (US9) ------------------------------------------------------------------------


def test_harden_same_wave_consumer_moves_to_a_later_wave_in_phase_b(skill):
    phase_b = _section(skill(HARDEN).body, PHASE_B_HEADING)
    _holds(phase_b, SAME_WAVE_ANCHOR, f"{HARDEN}'s Phase B")
    _holds(phase_b, SAME_WAVE_RULE, f"{HARDEN}'s Phase B")


def test_harden_same_wave_gate_in_validation_gates(skill):
    gates = _section(skill(HARDEN).body, VALIDATION_GATES_HEADING)
    _holds(gates, SAME_WAVE_GATE, f"{HARDEN}'s Validation Gates")


# --- superseded shapes (US10) ---------------------------------------------------------------


def test_harden_superseded_shape_searches_heading_in_phase_b(skill):
    phase_b = _section(skill(HARDEN).body, PHASE_B_HEADING)
    _holds(phase_b, SUPERSEDED_HEADING, f"{HARDEN}'s Phase B")


def test_harden_superseded_shape_search_rule_in_phase_b(skill):
    phase_b = _section(skill(HARDEN).body, PHASE_B_HEADING)
    _holds(phase_b, SUPERSEDED_HEADING, f"{HARDEN}'s Phase B")
    _holds(phase_b, SUPERSEDED_RULE, f"{HARDEN}'s Phase B")


def test_harden_superseded_shape_gate_in_validation_gates(skill):
    gates = _section(skill(HARDEN).body, VALIDATION_GATES_HEADING)
    _holds(gates, SUPERSEDED_GATE, f"{HARDEN}'s Validation Gates")
