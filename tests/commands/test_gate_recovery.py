"""002 Phase 19 (T078; R14): the verifier's PID record lives in the main checkout, and the
orchestrator recovers a killed gate.

Pins II-17c's PID phrase (and the relative form gone) and II-17d's brief sentences in harden's
`### Proxy verifier` brief and `agents/proxy-verifier.md`, II-17d's VERIFY GATES sentences and
ledger lines in harden's NOBRAKES, and II-17h's `004` phrase in the eval fixture (FR-026).
Phrases are transcribed from specs/002-pilot-refresh/contracts/internal-interfaces.md II-17;
assertion style per II-0.

002 Phase 20 (T084; R14 amended): the orchestrator writes the verifier's dispatch time as the
first line of its PID record, so a later relay's recovery can match it (II-17d's and II-17h's
2026-10-03 T083 amendments).

002 Phase 21 (T088; II-17i): the US11-AC2 eval case's grader 09 checks that the verifier recorded
something below the orchestrator's dispatched line, not only that the file exists.
"""

from __future__ import annotations

import re

HARDEN = "s2tdd-harden"
PROXY_AGENT = "agents/proxy-verifier.md"
PROXY_HEADING = "### Proxy verifier"
FIXTURE = "evals/fixtures/make-feature.sh"

# II-17c: the Proxy verifier brief and agents/proxy-verifier.md, exact.
PID_IN_MAIN_CHECKOUT = (
    "record its PID, start time and command line in the main checkout's "
    ".sdd-run/<NNN>/pids/verifier-<k>.txt (never the worktree's)"
)
# II-17c: gone from both (the relative path).
PID_RELATIVE_GONE = "command line in .sdd-run/<NNN>/pids/verifier-<k>.txt"

# II-17d: NOBRAKES VERIFY GATES.
GATE_RECOVERY = (
    "Before dispatching the verifier, recover a killed gate: when .sdd-run/<NNN>/gate-<k> is "
    "left over, sweep the processes its PID record names (the main checkout's "
    ".sdd-run/<NNN>/pids/verifier-<k>.txt; ground rule 17), then run git worktree remove --force "
    ".sdd-run/<NNN>/gate-<k> and git worktree prune.",
    "When Windows still holds its files, name a fresh path .sdd-run/<NNN>/gate-<k>-<n> in the "
    "brief, and say so in the ledger.",
    "At each wave boundary and before a gate, delete a .sdd-run/<NNN>/suite.lock whose recorded "
    "pid and start time match no live process; packets still only report a stale lock.",
)
# II-17d: ledger lines, under Processes killed.
RECOVERY_LEDGER_LINES = (
    "gate-<k> swept: <n> processes; worktree <removed | held, gate uses gate-<k>-<n>>",
    "suite.lock deleted: pid <pid> dead",
)
# II-17d: the Proxy verifier brief and agents/proxy-verifier.md.
FRESH_GATE_PATH = (
    "When the dispatch names a fresh gate path (gate-<k>-<n>), use it in place of gate-<k>.",
    "If git worktree add fails because the path exists, stop and say so in the hand-back: the "
    "orchestrator recovers gates.",
)

# II-17h: the eval fixture, with 004 for <NNN>.
FIXTURE_PID_IN_MAIN_CHECKOUT = (
    "the main checkout's .sdd-run/004/pids/verifier-<k>.txt (never the worktree's)"
)

# II-17d (amended 2026-10-03, T083): NOBRAKES VERIFY GATES, the dispatch time.
GATE_DISPATCH_TIME = (
    "After any recovery and before the dispatch, write the main checkout's "
    ".sdd-run/<NNN>/pids/verifier-<k>.txt afresh with one line, dispatched <ISO time>; the "
    "verifier adds its records below it.",
    "A recovery kills only processes that started after the record's dispatched line; a record "
    "without one kills nothing, and the ledger says so.",
)
# II-17d (amended 2026-10-03, T083): the third ledger line, under Processes killed.
NOT_SWEPT_LEDGER_LINE = (
    "gate-<k> not swept: no dispatched line; worktree <removed | held, gate uses gate-<k>-<n>>"
)
# II-17d (amended 2026-10-03, T083): the Proxy verifier brief and agents/proxy-verifier.md.
KEEPS_DISPATCHED_LINE = (
    "Add your records below the orchestrator's dispatched <ISO time> line; never rewrite or "
    "delete it."
)
# II-17h (amended 2026-10-03, T085): the eval fixture's VERIFY GATES, with 004 for <NNN>.
FIXTURE_GATE_DISPATCH_TIME = (
    "After any recovery and before the dispatch, write the main checkout's "
    ".sdd-run/004/pids/verifier-<k>.txt afresh with one line, dispatched <ISO time>; the "
    "verifier adds its records below it."
)


# II-17i (added 2026-10-04, T088): grader 09 of the US11-AC2 eval case, its frontmatter exact.
VERIFIER_GRADER = (
    "evals/implement/002-US11-AC2-gate-in-worktree/graders/09-verifier-suite-recorded.md"
)
VERIFIER_GRADER_NAME = "09-verifier-suite-recorded.md"
VERIFIER_GRADER_TARGET = {"source": "file", "path": ".sdd-run/004/pids/verifier-1.txt"}
# II-17i: the samples, with D and R as the contract defines them.
_D = "dispatched 2026-10-04T01:10:00Z"
_R = "4242 2026-10-04T01:11:05Z .venv/Scripts/python -m pytest tests"
RECORD_MATCHES = (f"{_D}\n{_R}\n", f"{_D}\r\n{_R}\r\n")
RECORD_NO_MATCH = (f"{_D}\n", _D, f"{_D}\n\n", f"{_R}\n")
_REGEX_FLAGS = {"m": re.M, "i": re.I, "s": re.S}


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


# --- II-17c: the verifier's PID record in the main checkout -----------------------------------


def test_harden_nb_verifier_pid_in_main_checkout(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    absent = _missing(brief, PID_IN_MAIN_CHECKOUT)
    assert not absent, f"harden's Proxy verifier brief lacks II-17c's phrase: {absent}"
    assert _flatten(PID_RELATIVE_GONE) not in _flatten(brief), (
        f"harden's Proxy verifier brief still holds {PID_RELATIVE_GONE!r}"
    )


def test_agents_verifier_pid_in_main_checkout(doc):
    d = doc(PROXY_AGENT)
    absent = d.missing(PID_IN_MAIN_CHECKOUT)
    assert not absent, f"{PROXY_AGENT} lacks II-17c's phrase: {absent}"
    assert _flatten(PID_RELATIVE_GONE) not in d.flat, (
        f"{PROXY_AGENT} still holds {PID_RELATIVE_GONE!r}"
    )


# --- II-17d: recovering a killed gate ----------------------------------------------------------


def test_harden_nb_gate_recovery(skill):
    d = skill(HARDEN)
    absent = d.missing(*GATE_RECOVERY, *RECOVERY_LEDGER_LINES)
    assert not absent, f"harden's VERIFY GATES lacks II-17d's recovery: {absent}"


def test_harden_nb_brief_fresh_gate_path(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    absent = _missing(brief, *FRESH_GATE_PATH)
    assert not absent, f"harden's Proxy verifier brief lacks II-17d's sentences: {absent}"


def test_agents_fresh_gate_path(doc):
    d = doc(PROXY_AGENT)
    absent = d.missing(*FRESH_GATE_PATH)
    assert not absent, f"{PROXY_AGENT} lacks II-17d's sentences: {absent}"


# --- II-17h: the eval fixture follows (green at T082) ------------------------------------------


def test_fixture_verifier_pid_in_main_checkout(doc):
    d = doc(FIXTURE)
    absent = d.missing(FIXTURE_PID_IN_MAIN_CHECKOUT)
    assert not absent, f"{FIXTURE} lacks II-17h's phrase: {absent}"


# --- II-17d amended (T083): the dispatch time a later relay reads ------------------------------


def test_harden_nb_gate_dispatch_time(skill):
    d = skill(HARDEN)
    absent = d.missing(*GATE_DISPATCH_TIME, NOT_SWEPT_LEDGER_LINE)
    assert not absent, f"harden's VERIFY GATES lacks II-17d's dispatch time: {absent}"


def test_harden_nb_brief_keeps_dispatched_line(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    absent = _missing(brief, KEEPS_DISPATCHED_LINE)
    assert not absent, f"harden's Proxy verifier brief lacks II-17d's sentence: {absent}"


def test_agents_keeps_dispatched_line(doc):
    d = doc(PROXY_AGENT)
    absent = d.missing(KEEPS_DISPATCHED_LINE)
    assert not absent, f"{PROXY_AGENT} lacks II-17d's sentence: {absent}"


# --- II-17h amended (T085): the eval fixture follows -------------------------------------------


def test_fixture_gate_dispatch_time(doc):
    d = doc(FIXTURE)
    absent = d.missing(FIXTURE_GATE_DISPATCH_TIME)
    assert not absent, f"{FIXTURE} lacks II-17h's phrase: {absent}"


# --- II-17i (T088): grader 09 checks the verifier's records below the dispatched line ---------


def test_eval_verifier_record_has_a_line_below_dispatched(doc):
    fm = doc(VERIFIER_GRADER).frontmatter
    assert fm.get("type") == "regex", (
        f"{VERIFIER_GRADER_NAME} is type {fm.get('type')}, not regex"
    )
    assert fm.get("target") == VERIFIER_GRADER_TARGET, (
        f"{VERIFIER_GRADER_NAME}'s target is {fm.get('target')!r}, not {VERIFIER_GRADER_TARGET!r}"
    )
    flags = 0
    for ch in str(fm.get("flags") or ""):
        assert ch in _REGEX_FLAGS, f"{VERIFIER_GRADER_NAME} has an unknown flag {ch!r}"
        flags |= _REGEX_FLAGS[ch]
    rx = re.compile(fm["pattern"], flags)
    missed = [s for s in RECORD_MATCHES if not rx.search(s)]
    assert not missed, f"{VERIFIER_GRADER_NAME}'s pattern misses II-17i's passing samples: {missed}"
    wrong = [s for s in RECORD_NO_MATCH if rx.search(s)]
    assert not wrong, f"{VERIFIER_GRADER_NAME}'s pattern matches II-17i's failing samples: {wrong}"
