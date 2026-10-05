"""T049 (US14): the proxy verifier gets the expected reds and the accepted deviations.

Pins II-7's `Expected red:`, `Accepted deviations:` and `Ticks and commits after <last>` lines in
harden's `### Proxy verifier` brief (Standard briefs) and in `agents/proxy-verifier.md`. Phrases
are transcribed from specs/002-pilot-refresh/contracts/internal-interfaces.md; assertion style
per II-0.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
PROXY_AGENT = "agents/proxy-verifier.md"
PROXY_HEADING = "### Proxy verifier"

# II-7: the Proxy verifier brief gains (and agents/proxy-verifier.md likewise).
PROXY_LINES = (
    "Expected red: <the expected-red rows for waves <a>–<b>, from orchestration.md>",
    "Accepted deviations: <the Decision and Deviation lines the orchestrator accepted, by wave>",
    "Ticks and commits after <last> belong to waves still running: not a gap.",
)


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _missing(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


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


# --- harden's Proxy verifier brief (wave 3) ----------------------------------------------------


def test_harden_nb_proxy_verifier_brief_slots(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    missing = _missing(brief, *PROXY_LINES)
    assert not missing, f"missing from harden's Proxy verifier brief: {missing}"


# --- agents/proxy-verifier.md (wave 2) ---------------------------------------------------------


def test_agents_proxy_verifier_slots(doc):
    d = doc(PROXY_AGENT)
    missing = d.missing(*PROXY_LINES)
    assert not missing, f"missing from {PROXY_AGENT}: {missing}"
