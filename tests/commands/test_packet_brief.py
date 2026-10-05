"""T024 (US4), T046 (US12): the packet rules every packet brief carries.

Pins II-6: harden's ground rule 4 (the `Cites:` line a test packet adds), harden's ground rule 17
(sibling edits and the lone rerun), harden's refresh mode (rule 17 among the rules it replaces),
and the second-person forms in rules 4 and 17 of `agents/packet-{cheap,medium,strong}.md`.
Phrases are transcribed from specs/002-pilot-refresh/contracts/internal-interfaces.md; assertion
style per II-0.
"""

from __future__ import annotations

import re

import pytest

HARDEN = "s2tdd-harden"
PACKET_AGENTS = ("agents/packet-cheap.md", "agents/packet-medium.md", "agents/packet-strong.md")

# II-6: harden's ground rule 4 gains this line.
HARDEN_CITATION = (
    "A test packet adds one line per shape its tests assert that another packet or wave builds: "
    "Cites: <test id> asserts <shape name> → contracts/<file> §<section>"
)
# II-6: each packet agent's rule 4 carries it in the second person.
AGENT_CITATION = (
    "If you are a test packet, add one line per shape your tests assert that another packet or "
    "wave builds: Cites: <test id> asserts <shape name> → contracts/<file> §<section>"
)

# II-6: harden's ground rule 17 gains the sibling and lone-rerun sentences.
HARDEN_SIBLING = (
    "Sibling packets' edits in the tree are expected and not reported.",
    "A red outside the packet's own tests is rerun alone before it is reported, and reported "
    "only if still red.",
)
# II-6: each packet agent's rule 17 carries them in the second person.
AGENT_SIBLING = (
    "Sibling packets' edits in the tree are expected and not reported.",
    "A red outside your own tests is rerun alone before it is reported, and reported only if "
    "still red.",
)
# 003 FR-011, II-4 RF1 (supersedes 002 II-6's list): harden's refresh mode replaces rules
# 1, 2, 4, 5, 12 and 17 with B4's current text.
REFRESH_REPLACED_RULES = "rules 1, 2, 4, 5, 12 and 17 with B4's current text"
REFRESH_REPLACED_RULES_GONE = "rules 1, 2, 4, 12 and 17"
REFRESH_MODE_ANCHOR = "**Refresh mode**"
# 003 FR-001, LG1 (converge round 3): II-7 RF2, added 2026-10-04: refresh mode adds the C3
# headings an existing run-ledger.md lacks; and C3's opening says so.
REFRESH_LEDGER = (
    "Write run-ledger.md (C3) if it is missing; when it exists, add each C3 heading it lacks, in "
    "C3's order, and rewrite no line."
)
REFRESH_LEDGER_GONE = "Write run-ledger.md (C3) if it is missing."
C3_ANCHOR = "**C3. Write `run-ledger.md`**"
C3_OPENING = (
    "(first harden, or refresh mode: written when it is missing, its missing headings added when "
    "it exists)"
)
C3_OPENING_GONE = "(first harden, or refresh mode when it is missing)"

# Structural anchors: the numbered rule's opening, as harden's B4 and the agents write it today.
RULE_4_ANCHOR = "4. **Reports by exception"
RULE_17_ANCHOR = "17. **Targeted tests"
_RULE_START = re.compile(r"^\d+\. \*\*")


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _missing(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


def _rule(body: str, anchor: str) -> str:
    """A numbered rule: from the line opening with `anchor` to the next blank line or the next
    numbered bold rule, whichever comes first."""
    lines = body.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.strip().startswith(anchor)), None)
    assert start is not None, f"rule not found: {anchor}"
    for j in range(start + 1, len(lines)):
        if not lines[j].strip() or _RULE_START.match(lines[j].strip()):
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


def _paragraph(body: str, anchor: str) -> str:
    """From the line opening with `anchor` to the next blank line."""
    lines = body.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.startswith(anchor)), None)
    assert start is not None, f"paragraph not found: {anchor}"
    end = next((j for j in range(start + 1, len(lines)) if not lines[j].strip()), len(lines))
    return "\n".join(lines[start:end])


# --- citations (T024; harden wave 2, agents wave 2) --------------------------------------------


def test_harden_ground_rule_4_citation_line(skill):
    rule = _rule(skill(HARDEN).body, RULE_4_ANCHOR)
    missing = _missing(rule, HARDEN_CITATION)
    assert not missing, f"missing from harden's ground rule 4: {missing}"


@pytest.mark.parametrize("agent", PACKET_AGENTS)
def test_agents_packet_rule_4_citation_line(doc, agent):
    rule = _rule(doc(agent).body, RULE_4_ANCHOR)
    missing = _missing(rule, AGENT_CITATION)
    assert not missing, f"missing from {agent}'s rule 4: {missing}"


# --- sibling edits and the lone rerun (T046; harden wave 2, agents wave 2) ---------------------


def test_harden_ground_rule_17_sibling_and_lone_rerun(skill):
    rule = _rule(skill(HARDEN).body, RULE_17_ANCHOR)
    missing = _missing(rule, *HARDEN_SIBLING)
    assert not missing, f"missing from harden's ground rule 17: {missing}"


def test_harden_refresh_mode_replaces_rule_17_sibling(skill):
    paragraph = _paragraph(skill(HARDEN).body, REFRESH_MODE_ANCHOR)
    missing = _missing(paragraph, REFRESH_REPLACED_RULES)
    assert not missing, f"missing from harden's refresh mode: {missing}"


def test_harden_refresh_mode_old_rule_list_gone(skill):
    paragraph = _paragraph(skill(HARDEN).body, REFRESH_MODE_ANCHOR)
    assert _flatten(REFRESH_REPLACED_RULES_GONE) not in _flatten(paragraph), (
        f"harden's refresh mode still holds {REFRESH_REPLACED_RULES_GONE!r}"
    )


def test_harden_refresh_mode_adds_missing_ledger_headings(skill):
    # 003 FR-001: II-7 RF2 in refresh mode's paragraph, and its gone phrase.
    paragraph = _paragraph(skill(HARDEN).body, REFRESH_MODE_ANCHOR)
    missing = _missing(paragraph, REFRESH_LEDGER)
    assert not missing, f"missing from harden's refresh mode: {missing}"
    assert _flatten(REFRESH_LEDGER_GONE) not in _flatten(paragraph), (
        f"harden's refresh mode still holds {REFRESH_LEDGER_GONE!r}"
    )


def test_harden_c3_opening_names_missing_headings(skill):
    # 003 FR-001: II-7 RF2's C3 opening, and its gone phrase.
    paragraph = _paragraph(skill(HARDEN).body, C3_ANCHOR)
    missing = _missing(paragraph, C3_OPENING)
    assert not missing, f"missing from harden's C3 opening: {missing}"
    assert _flatten(C3_OPENING_GONE) not in _flatten(paragraph), (
        f"harden's C3 opening still holds {C3_OPENING_GONE!r}"
    )


@pytest.mark.parametrize("agent", PACKET_AGENTS)
def test_agents_packet_rule_17_sibling_and_lone_rerun(doc, agent):
    rule = _rule(doc(agent).body, RULE_17_ANCHOR)
    missing = _missing(rule, *AGENT_SIBLING)
    assert not missing, f"missing from {agent}'s rule 17: {missing}"
