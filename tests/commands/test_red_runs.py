"""T022 (US3): verify-done reads every red run.

Pins II-11's first three phrases in `skills/s2tdd-verify-done/SKILL.md`, the fix line exact, and
`red runs read:` in its Output. Phrases are transcribed from
specs/002-pilot-refresh/contracts/internal-interfaces.md; assertion style per II-0.
"""

from __future__ import annotations

VERIFY_DONE = "s2tdd-verify-done"

# II-11, phrases 1-3.
RED_RUN_PHRASES = (
    "Read the red run of every implementation packet report in the range, never a sample, and "
    "say how many you read: red runs read: <k> of <k>.",
    "A red run that is missing, or that the report says was taken after the packet's "
    "implementation edits, is a gap when the wave report's Red runs line shows the test red "
    "before dispatch.",
    'When nothing shows the test red, the task is Not done: untick it, with the fix line "the '
    "test's own packet shows it red at the commit before the implementation\".",
)

# II-11: the fix line, exact (case, apostrophe and double quotes kept; whitespace folded).
FIX_LINE = "\"the test's own packet shows it red at the commit before the implementation\""

# II-11: the count verify-done states, in its Output (T023: the claim table's count).
COUNT = "red runs read:"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _section(body: str, heading: str) -> str:
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


def test_verify_done_red_run_phrases(skill):
    d = skill(VERIFY_DONE)
    assert not d.missing(*RED_RUN_PHRASES), d.missing(*RED_RUN_PHRASES)


def test_verify_done_fix_line_exact(skill):
    folded = " ".join(skill(VERIFY_DONE).body.split())
    assert FIX_LINE in folded, f"fix line not verbatim: {FIX_LINE}"


def test_verify_done_output_states_red_runs_read(skill):
    output = _section(skill(VERIFY_DONE).body, "## Output")
    assert _flatten(COUNT) in _flatten(output), f"Output lacks: {COUNT}"
