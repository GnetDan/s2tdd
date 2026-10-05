"""PR review fixes (#5 at 94cc1a3): the gate's code, the gate's checks, the suite lock, new files in
review diffs, an attended MUST breach, old handoffs' rate-limit stop, and B1's wave.

Findings: A1-harden-1 (II-18a), A2-2 (II-18b), A2-1 (II-18c), A2-3 (II-18d), A1-harden-4
(II-18e), SPEC-2/A1-5 (II-18f), SPEC-3 (II-18g) and A1-3 (II-18h). Pins harden's Proxy verifier,
Shape check and Strong-diff reviewer briefs, its NOBRAKES VERIFY GATES, SHAPE CHECK, MUST BREACH,
B1 and Validation Gates; agents/proxy-verifier.md and agents/strong-diff-reviewer.md;
verify-done's User Input, Suite and Invariants items; implement's Usage paragraph. Phrases are
transcribed from specs/002-pilot-refresh/contracts/internal-interfaces.md II-18; assertion style
per II-0.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
VERIFY_DONE = "s2tdd-verify-done"
IMPLEMENT = "s2tdd-implement"
PROXY_AGENT = "agents/proxy-verifier.md"
REVIEWER_AGENT = "agents/strong-diff-reviewer.md"

PROXY_HEADING = "### Proxy verifier"
SHAPE_BRIEF_HEADING = "### Shape check"
STRONG_DIFF_HEADING = "### Strong-diff reviewer (read-only)"
NOBRAKES_START = "NOBRAKES (only when MODE is nobrakes; otherwise skip this section)"
SHAPE_CHECK_ITEM = "- `SHAPE CHECK"
MUST_BREACH_ITEM = "- `MUST BREACH`"
B1_START = "**B1. File-ownership map.**"
B2_START = "**B2."
VALIDATION_GATES_HEADING = "## Validation Gates"
USER_INPUT_HEADING = "## User Input"
USAGE_START = "**Usage** (`MODE: nobrakes`)"
AGENT_SHAPE_CHECK_START = "**Shape check.**"

# II-18a: the gate's code loads from the worktree.
CODE_FROM_WORKTREE = (
    "Check before the suite that the code under test loads from the worktree: print where one of "
    "the project's own modules loads from (in Python, its __file__). When it loads from the main "
    "checkout (an editable install points there), put the worktree first on the import path (in "
    "Python, PYTHONPATH=<the worktree's source root>) and check again; when it still loads from "
    "outside the worktree, that is an environment failure."
)
# II-7 / agent: the suite's interpreter sentence (II-18a goes after it).
INTERPRETER_ANCHOR = "never one expected inside the worktree"
# II-11: verify-done's gate-worktree sentence (II-18a goes after it).
VD_WORKTREE_ANCHOR = "When the input names a gate worktree (worktree <path>), run the suite there"

# II-18b: an environment failure unticks nothing.
VD_ENV_FAILURE = (
    "In a gate worktree, collection or import errors that the last wave's suite did not show, or "
    "code that loads from outside the worktree, are an environment failure, not a red test: "
    "untick nothing, write no verification-log line, and report Environment failure in worktree: "
    "<the first error line> in place of a verdict."
)
PROXY_ENV_FAILURE = (
    "verify-done then unticks nothing and logs no verdict: hand back its Environment failure in "
    "worktree: line in place of the verdict line."
)
ENV_FAILURE_ANCHOR = "On an environment failure in the worktree"

# II-18c: the invariant checks run in the worktree.
VD_INVARIANTS_IN_WORKTREE = (
    "When the input names a gate worktree, run the guardrail command, or the check commands, there "
    "too, the same way as the suite: the main checkout holds the next wave's uncommitted edits."
)
VD_USER_INPUT = (
    "worktree <path> names a gate worktree at the commit under review, where Scope's status, the "
    "suite and the invariant checks run (below)."
)

# II-18d: the suite lock names a live process.
LOCK_PID = (
    "Write the lock's pid as starting; once the suite runs, rewrite its pid and started with the "
    "suite's own PID and start time."
)
LOCK_ANCHOR = (
    "write .sdd-run/<NNN>/suite.lock (pid, started, command, minutes) before the suite and "
    "delete it after"
)
STARTING_LOCK = (
    "A lock whose pid is starting is never deleted for its pid: only once it is older than twice "
    "its minutes."
)
STALE_LOCK_ANCHOR = (
    "pid and start time match no live process; packets still only report a stale lock."
)

# II-18e: new files are read whole.
NEW_FILES_WHOLE = (
    "New files are untracked, and git diff shows nothing for them: read each file git status "
    "--short marks ?? whole."
)
READ_ANCHOR = "- Read:"

# II-18f: an attended MUST breach stops the run after the wave's commit.
SHAPE_CHECK_EXCEPTION = "A MUST breach is the exception (MUST BREACH)."
SHAPE_CHECK_PHRASE_6 = (
    "With MODE: attended, it is report-only: its findings go into the wave report's Review line "
    "as recommendations and block neither the commit nor the next wave."
)
MUST_BREACH_STOP = (
    "With MODE: attended, commit the wave, then stop: start no next wave while a MUST breach is "
    "open."
)
MUST_BREACH_PHRASE_11 = (
    "With MODE: attended, it heads the wave report: MUST breach: fix before the next wave · "
    "<finding line>."
)

# II-18g: new limits replace an older handoff's rate-limit stop.
OLD_HANDOFF_STOP = (
    "In a handoff.md hardened before 0.3.0, its STOP THE RUN item for plan usage at 90% of a "
    "rate-limit window is replaced by them: it stops nothing."
)
USAGE_ANCHOR = "The limits apply whatever handoff.md's age, as the usage source does."

# II-18h: B1's wave is the red test wave.
RED_TEST_WAVE = (
    "The first wave that changes the shape is the red test wave that comes before the "
    "implementation that changes the shape, never the implementation's own wave."
)
B1_ANCHOR = "give each file found a test task in the first wave that changes the shape"
GATE_ANCHOR = "each file it found is owned by a test task in the first wave that changes the shape"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _missing(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


def _after(text: str, anchor: str, phrase: str) -> bool:
    """True when `phrase` appears in `text` after `anchor` (both flattened)."""
    flat = _flatten(text)
    at = flat.find(_flatten(anchor))
    return at >= 0 and flat.find(_flatten(phrase), at) > at


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


def _between(body: str, start: str, end: str) -> str:
    """From the first line starting with `start` (stripped) to the next line starting with `end`."""
    lines = body.split("\n")
    at = next((i for i, ln in enumerate(lines) if ln.strip().startswith(start)), None)
    assert at is not None, f"start not found: {start}"
    stop = next((j for j in range(at + 1, len(lines)) if lines[j].strip().startswith(end)), None)
    assert stop is not None, f"end not found after {start}: {end}"
    return "\n".join(lines[at:stop])


def _prompt_item(body: str, start: str) -> str:
    """One `- `-bullet of harden's Phase C1 prompt list: its line through the next such bullet."""
    lines = body.split("\n")
    at = next((i for i, ln in enumerate(lines) if ln.startswith(start)), None)
    assert at is not None, f"prompt item not found: {start}"
    end = next((j for j in range(at + 1, len(lines)) if lines[j].startswith("- `")), len(lines))
    return "\n".join(lines[at:end])


def _nobrakes(body: str) -> str:
    """The NOBRAKES block: its opening line through its closing ```` fence."""
    lines = body.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.strip().startswith(NOBRAKES_START)), None)
    assert start is not None, f"NOBRAKES opening line not found: {NOBRAKES_START}"
    end = next((j for j in range(start + 1, len(lines)) if lines[j].strip() == "````"), None)
    assert end is not None, "NOBRAKES block's closing ```` fence not found"
    return "\n".join(lines[start:end])


def _vd_item(body: str, label: str) -> str:
    """One `- **<label>**` item of verify-done's checks, through the next item at its indent."""
    lines = body.split("\n")
    marker = f"- **{label}**"
    at = next((i for i, ln in enumerate(lines) if ln.strip().startswith(marker)), None)
    assert at is not None, f"verify-done item not found: {marker}"
    indent = lines[at][: len(lines[at]) - len(lines[at].lstrip())]
    def ends(line: str) -> bool:
        if line.startswith(indent + "- "):
            return True
        return bool(line.strip()) and not line.startswith(indent + " ")

    end = next((j for j in range(at + 1, len(lines)) if ends(lines[j])), len(lines))
    return "\n".join(lines[at:end])


def _agent_briefs(body: str) -> tuple[str, str]:
    """agents/strong-diff-reviewer.md's Strong-diff reviewer brief and its Shape check brief."""
    at = body.find(AGENT_SHAPE_CHECK_START)
    assert at >= 0, f"{REVIEWER_AGENT}: {AGENT_SHAPE_CHECK_START} not found"
    return body[:at], body[at:]


# --- II-18a: the gate's code loads from the worktree (A1-harden-1) -----------------------------


def test_harden_nb_proxy_brief_code_loads_from_worktree(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    assert not _missing(brief, CODE_FROM_WORKTREE), (
        "harden's Proxy verifier brief lacks II-18a's sentence"
    )
    assert _after(brief, INTERPRETER_ANCHOR, CODE_FROM_WORKTREE), (
        "II-18a's sentence is not after the suite's interpreter sentence"
    )


def test_agents_proxy_verifier_code_loads_from_worktree(doc):
    d = doc(PROXY_AGENT)
    assert not d.missing(CODE_FROM_WORKTREE), f"{PROXY_AGENT} lacks II-18a's sentence"
    assert _after(d.body, INTERPRETER_ANCHOR, CODE_FROM_WORKTREE), (
        "II-18a's sentence is not after the suite's interpreter sentence"
    )


def test_verify_done_suite_code_loads_from_worktree(skill):
    item = _vd_item(skill(VERIFY_DONE).body, "Suite")
    assert not _missing(item, CODE_FROM_WORKTREE), "verify-done's Suite item lacks II-18a"
    assert _after(item, VD_WORKTREE_ANCHOR, CODE_FROM_WORKTREE), (
        "II-18a's sentence is not after the Suite item's gate-worktree sentence"
    )


# --- II-18b: an environment failure unticks nothing (A2-2) -------------------------------------


def test_verify_done_suite_environment_failure_unticks_nothing(skill):
    item = _vd_item(skill(VERIFY_DONE).body, "Suite")
    assert not _missing(item, VD_ENV_FAILURE), "verify-done's Suite item lacks II-18b"


def test_harden_nb_proxy_brief_environment_failure_no_verdict(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    assert not _missing(brief, PROXY_ENV_FAILURE), "harden's Proxy verifier brief lacks II-18b"
    assert _after(brief, ENV_FAILURE_ANCHOR, PROXY_ENV_FAILURE), (
        "II-18b's sentence is not after II-7's environment-failure line"
    )


def test_agents_proxy_verifier_environment_failure_no_verdict(doc):
    d = doc(PROXY_AGENT)
    assert not d.missing(PROXY_ENV_FAILURE), f"{PROXY_AGENT} lacks II-18b's sentence"
    assert _after(d.body, ENV_FAILURE_ANCHOR, PROXY_ENV_FAILURE), (
        "II-18b's sentence is not after II-7's environment-failure line"
    )


# --- II-18c: the invariant checks run in the worktree (A2-1) -----------------------------------


def test_verify_done_invariants_run_in_worktree(skill):
    item = _vd_item(skill(VERIFY_DONE).body, "Invariants")
    assert not _missing(item, VD_INVARIANTS_IN_WORKTREE), (
        "verify-done's Invariants item lacks II-18c"
    )


def test_verify_done_user_input_names_invariant_checks(skill):
    section = _subsection(skill(VERIFY_DONE).body, USER_INPUT_HEADING)
    assert not _missing(section, VD_USER_INPUT), "verify-done's User Input lacks II-18c"


# --- II-18d: the suite lock names a live process (A2-3) ----------------------------------------


def test_verify_done_suite_lock_pid(skill):
    item = _vd_item(skill(VERIFY_DONE).body, "Suite")
    assert not _missing(item, LOCK_PID), "verify-done's Suite item lacks II-18d"
    assert _after(item, LOCK_ANCHOR, LOCK_PID), "II-18d's sentence is not after the lock sentence"


def test_harden_nb_proxy_brief_suite_lock_pid(skill):
    brief = _subsection(skill(HARDEN).body, PROXY_HEADING)
    assert not _missing(brief, LOCK_PID), "harden's Proxy verifier brief lacks II-18d"
    assert _after(brief, LOCK_ANCHOR, LOCK_PID), "II-18d's sentence is not after the lock sentence"


def test_agents_proxy_verifier_suite_lock_pid(doc):
    d = doc(PROXY_AGENT)
    assert not d.missing(LOCK_PID), f"{PROXY_AGENT} lacks II-18d's sentence"
    assert _after(d.body, LOCK_ANCHOR, LOCK_PID), "II-18d's sentence is not after the lock sentence"


def test_harden_nb_verify_gates_starting_lock(skill):
    block = _nobrakes(skill(HARDEN).body)
    assert not _missing(block, STARTING_LOCK), "harden's NOBRAKES VERIFY GATES lacks II-18d"
    assert _after(block, STALE_LOCK_ANCHOR, STARTING_LOCK), (
        "II-18d's sentence is not after II-17d's stale-lock sentence"
    )


# --- II-18e: new files are read whole (A1-harden-4) --------------------------------------------


def test_harden_shape_check_brief_reads_new_files(skill):
    brief = _subsection(skill(HARDEN).body, SHAPE_BRIEF_HEADING)
    assert not _missing(brief, NEW_FILES_WHOLE), "harden's Shape check brief lacks II-18e"
    assert _after(brief, READ_ANCHOR, NEW_FILES_WHOLE), "II-18e is not after the Read: line"


def test_harden_nb_strong_diff_brief_reads_new_files(skill):
    brief = _subsection(skill(HARDEN).body, STRONG_DIFF_HEADING)
    assert not _missing(brief, NEW_FILES_WHOLE), "harden's Strong-diff reviewer brief lacks II-18e"
    assert _after(brief, READ_ANCHOR, NEW_FILES_WHOLE), "II-18e is not after the Read: line"


def test_agents_strong_diff_reviewer_both_briefs_read_new_files(doc):
    strong_diff, shape_check = _agent_briefs(doc(REVIEWER_AGENT).body)
    for name, brief in (("Strong-diff reviewer", strong_diff), ("Shape check", shape_check)):
        assert not _missing(brief, NEW_FILES_WHOLE), f"{REVIEWER_AGENT}'s {name} lacks II-18e"
        assert _after(brief, READ_ANCHOR, NEW_FILES_WHOLE), (
            f"{REVIEWER_AGENT}'s {name}: II-18e is not after the Read: line"
        )


# --- II-18f: an attended MUST breach stops after the wave's commit (SPEC-2, A1-5) --------------


def test_harden_shape_check_must_breach_exception(skill):
    item = _prompt_item(skill(HARDEN).body, SHAPE_CHECK_ITEM)
    assert not _missing(item, SHAPE_CHECK_EXCEPTION), "harden's SHAPE CHECK lacks II-18f"
    assert _after(item, SHAPE_CHECK_PHRASE_6, SHAPE_CHECK_EXCEPTION), (
        "II-18f's sentence is not after II-2 phrase 6"
    )


def test_harden_must_breach_attended_stop(skill):
    item = _prompt_item(skill(HARDEN).body, MUST_BREACH_ITEM)
    assert not _missing(item, MUST_BREACH_STOP), "harden's MUST BREACH lacks II-18f"
    assert _after(item, MUST_BREACH_PHRASE_11, MUST_BREACH_STOP), (
        "II-18f's sentence is not after II-2 phrase 11"
    )


# --- II-18g: new limits replace an older handoff's rate-limit stop (SPEC-3) --------------------


def test_implement_usage_replaces_old_rate_limit_stop(skill):
    paragraph = _between(skill(IMPLEMENT).body, USAGE_START, "**Harnesses without a mechanism.**")
    assert not _missing(paragraph, OLD_HANDOFF_STOP), "implement's Usage paragraph lacks II-18g"
    assert _after(paragraph, USAGE_ANCHOR, OLD_HANDOFF_STOP), (
        "II-18g's sentence is not after II-10's limits sentence"
    )


# --- II-18h: B1's wave is the red test wave (A1-3) ---------------------------------------------


def test_harden_b1_red_test_wave(skill):
    b1 = _between(skill(HARDEN).body, B1_START, B2_START)
    assert not _missing(b1, RED_TEST_WAVE), "harden's B1 lacks II-18h"
    assert _after(b1, B1_ANCHOR, RED_TEST_WAVE), "II-18h's sentence is not after B1's phrase"


def test_harden_validation_gate_red_test_wave(skill):
    gates = _subsection(skill(HARDEN).body, VALIDATION_GATES_HEADING)
    assert not _missing(gates, RED_TEST_WAVE), "harden's Validation Gates lack II-18h"
    assert _after(gates, GATE_ANCHOR, RED_TEST_WAVE), (
        "II-18h's sentence is not after the superseded-shape gate"
    )
