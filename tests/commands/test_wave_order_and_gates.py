"""T041 (US11): one suite per wave, and gates that don't hold the tree.

Pins the wave order in harden's HOW TO WORK (003 II-3's HW1 since 003 T002; it supersedes
002 II-4's clause per 003 FR-011), II-6's suite-lock phrases in harden's ground
rule 17 and in the three packet agents, II-8's VERIFY GATES phrases in harden's NOBRAKES block,
II-7's gate-worktree and suite-lock lines in harden's Proxy verifier brief and in
`agents/proxy-verifier.md`, and II-11's gate-worktree run, suite lock and `worktree <path>`
argument-hint in verify-done. Phrases are transcribed from
specs/002-pilot-refresh/contracts/internal-interfaces.md; assertion style per II-0.
"""

from __future__ import annotations

import pytest

HARDEN = "s2tdd-harden"
VERIFY_DONE = "s2tdd-verify-done"
PACKET_AGENTS = ("agents/packet-cheap.md", "agents/packet-medium.md", "agents/packet-strong.md")
PROXY_AGENT = "agents/proxy-verifier.md"

# 003 II-3 HW1: HOW TO WORK's wave-order clause. Supersedes 002 II-4's clause per 003 FR-011
# (supersedes 002 FR-025's "full suite once"): the wave's test run, not the full suite.
HOW_TO_WORK = (
    "after each wave: its reviews and shape check, then their fixes, then the wave's test run "
    "once, then the commit (never a second test run in a wave for a review fix)",
)
# 003 II-3: gone from harden.
HOW_TO_WORK_GONE = "then the full suite once"

# II-6: harden's ground rule 17 gains these suite-lock phrases.
RULE_17_LOCK = (
    "Before running any test, a packet waits while .sdd-run/<NNN>/suite.lock exists",
    "A lock older than twice its expected minutes is stale: report Unexpected: stale suite lock "
    "and go on.",
    "A packet that cannot wait reports Blocked: suite lock",
)

# II-6: each packet agent's lock phrases, in the second person.
AGENT_LOCK = (
    "Before running any test, wait while .sdd-run/<NNN>/suite.lock exists",
    "A lock older than twice its expected minutes is stale: report Unexpected: stale suite lock "
    "and go on.",
)

# II-8: VERIFY GATES.
VERIFY_GATES = (
    "the proxy verifier verifies in a scratch worktree at the gate's commit "
    "(.sdd-run/<NNN>/gate-<k>)",
    "start the next wave at once; its packets hold their test runs while "
    ".sdd-run/<NNN>/suite.lock exists",
    "Gates verify in the tree from wave <n>: <environment failure line>",
    "every later gate verifies in the tree, holding the next wave",
    "Not done: the unticked tasks lead the first wave not yet dispatched",
)

# II-7: the Proxy verifier's gate-worktree and suite-lock lines (harden's brief and the agent).
PROXY_GATE = (
    "Verify in a gate worktree: git worktree add .sdd-run/<NNN>/gate-<k> <sha>, the commit the "
    "gate's tag will name; copy <gate files> in by name",
    "write .sdd-run/<NNN>/suite.lock (pid, started, command, minutes) before the suite and "
    "delete it after",
    "remove the worktree when done",
    "On an environment failure in the worktree (collection or import errors the last wave's "
    "suite did not show), say so in the hand-back.",
)

# II-11: verify-done's gate-worktree run and suite lock, and its argument-hint addition.
VERIFY_DONE_WORKTREE = (
    "When the input names a gate worktree (worktree <path>), run the suite there",
    "write .sdd-run/<NNN>/suite.lock (pid, started, command, minutes) before the suite and "
    "delete it after",
)
ARGUMENT_HINT_WORKTREE = "worktree <path>"

HOW_TO_WORK_START = "- `HOW TO WORK`"
RULE_17_START = "17. **"
RULE_18_START = "18. **"
NOBRAKES_START = "NOBRAKES (only when MODE is nobrakes; otherwise skip this section)"
PROXY_HEADING = "### Proxy verifier"


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


def _ground_rule_17(body: str) -> str:
    """Harden's ground rule 17: its numbered line through the line before rule 18."""
    lines = body.split("\n")
    at = next((i for i, ln in enumerate(lines) if ln.strip().startswith(RULE_17_START)), None)
    assert at is not None, "harden's ground rule 17 not found"
    end = next(
        (j for j in range(at + 1, len(lines)) if lines[j].strip().startswith(RULE_18_START)),
        None,
    )
    assert end is not None, "harden's ground rule 18 (the end of rule 17) not found"
    return "\n".join(lines[at:end])


def _nobrakes(body: str) -> str:
    """The NOBRAKES block: its opening line through its closing ```` fence."""
    lines = body.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.strip().startswith(NOBRAKES_START)), None)
    assert start is not None, f"NOBRAKES opening line not found: {NOBRAKES_START}"
    end = next((j for j in range(start + 1, len(lines)) if lines[j].strip() == "````"), None)
    assert end is not None, "NOBRAKES block's closing ```` fence not found"
    return "\n".join(lines[start:end])


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


# --- harden's main prompt (wave 2) -------------------------------------------------------------


def test_harden_how_to_work_wave_order(skill):
    item = _prompt_item(skill(HARDEN).body, HOW_TO_WORK_START)
    missing = _missing(item, *HOW_TO_WORK)
    assert not missing, f"harden's HOW TO WORK lacks: {missing}"
    assert _flatten(HOW_TO_WORK_GONE) not in _flatten(skill(HARDEN).body), (
        f"harden still holds {HOW_TO_WORK_GONE!r}"
    )


def test_harden_rule_17_suite_lock(skill):
    rule = _ground_rule_17(skill(HARDEN).body)
    missing = _missing(rule, *RULE_17_LOCK)
    assert not missing, f"harden's ground rule 17 lacks: {missing}"


# --- harden's NOBRAKES block and Proxy verifier brief (wave 3) ---------------------------------


def test_harden_nb_verify_gates_in_worktree(skill):
    block = _nobrakes(skill(HARDEN).body)
    missing = _missing(block, *VERIFY_GATES)
    assert not missing, f"harden's NOBRAKES lacks: {missing}"


def test_harden_nb_proxy_verifier_gate_worktree_and_lock(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    missing = _missing(brief, *PROXY_GATE)
    assert not missing, f"harden's Proxy verifier brief lacks: {missing}"


# --- verify-done (wave 2) ----------------------------------------------------------------------


def test_verify_done_gate_worktree_and_lock(skill):
    d = skill(VERIFY_DONE)
    assert not d.missing(*VERIFY_DONE_WORKTREE), d.missing(*VERIFY_DONE_WORKTREE)


def test_verify_done_argument_hint_names_worktree(skill):
    hint = skill(VERIFY_DONE).frontmatter.get("argument-hint")
    assert isinstance(hint, str), f"verify-done has no argument-hint: {hint!r}"
    assert ARGUMENT_HINT_WORKTREE in hint, f"argument-hint {hint!r} lacks {ARGUMENT_HINT_WORKTREE!r}"


# --- agents (wave 2) ---------------------------------------------------------------------------


@pytest.mark.parametrize("agent", PACKET_AGENTS)
def test_agents_packet_suite_lock(doc, agent):
    d = doc(agent)
    assert not d.missing(*AGENT_LOCK), d.missing(*AGENT_LOCK)


def test_agents_proxy_verifier_gate_worktree_and_lock(doc):
    d = doc(PROXY_AGENT)
    assert not d.missing(*PROXY_GATE), d.missing(*PROXY_GATE)
