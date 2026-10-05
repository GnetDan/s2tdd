"""003 T006 (US1): the converge loop to ready-to-close.

Pins II-7 (harden's NOBRAKES block: MODE, DOCS WAVE, CONVERGE LOOP, HANDOFF, RUN SUMMARY, the C3
ledger, the Validation Gates and the Standard briefs), II-8 (implement's `once`, MODEs, dispatch,
older-handoff note and phase in RESUME AT) and II-1 / II-12 (the converger and hardener agents,
and the proxy verifier's suite line, PV1). Phrases are transcribed from
specs/003-nobrakes-ready-to-close/contracts/internal-interfaces.md and agent-types.md (RR-4 as
amended 2026-10-04: the converger's no-report line, CL6); assertion style per II-0.
"""

from __future__ import annotations

import pytest

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"
CONVERGER_AGENT = "agents/converger.md"
HARDENER_AGENT = "agents/hardener.md"
PROXY_AGENT = "agents/proxy-verifier.md"

PROXY_HEADING = "### Proxy verifier"
CONVERGER_HEADING = "### Converger"
HARDENER_HEADING = "### Hardener"
REVIEWER_HEADING = "### Strong-diff reviewer (read-only)"

# --- II-7 N1. Mode ------------------------------------------------------------------------------
N1A = (
    "MODE: nobrakes once runs every rule here except CONVERGE LOOP; it stops after the last wave "
    "in SCOPE as 0.3.0 did."
)
N1B = (
    '"stop after the last wave in SCOPE" → VERIFY GATES, CONVERGE LOOP, HANDOFF and the RUN '
    "SUMMARY."
)
N1A_AFTER = "An unattended run always starts in a fresh session."
N1A_BEFORE = "STATE lives in files, never only in this context."
N1B_GONE ="→ VERIFY GATES, HANDOFF and the RUN SUMMARY."
# 003 FR-002 (converge round 3): II-7 N1d, added 2026-10-04, on the line right after the frozen
# NOBRAKES header (a chain-rules marker that stays), before the block's first rule.
N1D = "MODE: nobrakes once counts as nobrakes for this section."
NOBRAKES_HEADER = "NOBRAKES (only when MODE is nobrakes; otherwise skip this section)"
N1D_BEFORE = "You run every wave in SCOPE unattended."

# --- II-7 N2. DOCS WAVE -------------------------------------------------------------------------
DOCS_WAVE_FIRST = "DOCS WAVE (<docs wave>) runs last in the run"
N2A = (
    "In a looping run it runs once, after the round whose converge reports converged, and before "
    "the RUN SUMMARY; until then converge sets its tasks aside."
)

# --- II-7 N3. CONVERGE LOOP ---------------------------------------------------------------------
CL1 = "CONVERGE LOOP (MODE: nobrakes only)."
HANDOFF_ANCHOR = "HANDOFF. At each wave boundary"
CONVERGE_LOOP = {
    "CL1": (CL1,),
    "CL2": ("the run converges instead of stopping",),
    "CL3": (
        "A blocked packet's tasks left unticked stop the run before converge: record Waves done: "
        "stopped before converge · blocked <packets>; skipped <packets> under the ledger's "
        "Rounds, and print the RUN SUMMARY.",
    ),
    "CL4": (
        "Dispatch s2tdd:converger with the Converger brief (Standard briefs) for round <r>, "
        "counted from 1 over the whole run.",
    ),
    "CL5": (
        "Round <r>: converge at <sha> · converged",
        "Round <r>: converge at <sha> · <k> tasks appended (T<a>–T<b>) · cites T<a> <IDs>; "
        "T<a+1> <IDs>; …",
    ),
    "CL6": (
        "A converger that gives no report is retried once with a shortened brief; a second time "
        "stops the run: Round <r>: stopped · converger gave no report.",
    ),
    "CL7": (
        "Converged: build the DOCS WAVE (none: skip it), then print the RUN SUMMARY, ready to "
        "close.",
    ),
    "CL8": (
        "apply the stop rules in this order; the first that fires is recorded under Rounds and "
        "stops the run",
    ),
    "CL9": (
        "round 1 never stops on this",
        "Round <r>: stopped · no shrink (round <r-1> <k1>, round <r> <k2>)",
        "Round <r>: stopped · gap back (<ID>: T<n> now, T<m> in round <q>)",
        "Round <r>: stopped · cites nothing (T<n>)",
    ),
    "CL10": (
        "The test-upkeep task (T<n> upkeep) is exempt from rules 2 and 3 and left out of rule "
        "1's counts.",
    ),
    "CL11": (
        "Otherwise dispatch s2tdd:hardener with the Hardener brief on the appended tasks.",
        "Round <r>: hardened · W<x>–W<y>",
        "with gates at their slice ends and a final gate before the next converge",
        "A judgment the hardener deferred to a checkpoint is a pending checkpoint.",
        "Round <r>: stopped · harden: <harden's stop message>",
        "Round <r>: stopped · hardener gave no report",
    ),
    "CL12": (
        "BOUNDARY, BRAKES, STOP THE RUN and HANDOFF act at every phase change as at a wave "
        "boundary; HANDOFF's next-step estimate for a converge or harden step is one hand-back "
        "(about 5k tokens).",
    ),
    "CL13": ("No round cap",),
}

# --- II-7 N4. HANDOFF (RR-5) --------------------------------------------------------------------
HANDOFF = {
    "H1": ("CONVERGE LOOP's phase changes are boundaries too.",),
    "H2": (
        "At a converge, harden or docs-wave phase, the prompt's first line is /s2tdd-implement "
        "--nobrakes, with no scope: the phase comes from RESUME AT.",
    ),
    # 003 FR-006/FR-008: II-7 H3 amended 2026-10-04 (run-ledger.md Open review notes, W2 P2a):
    # the docs wave is never committed by the run, so it needs no verify-done line.
    "H3": (
        "every committed wave before <m> (every committed wave, at a converge, harden or "
        "docs-wave phase) has a verify-done line in validation.md; the docs wave, never "
        "committed by the run, needs none",
        "the newest Rounds line is <line> (or none)",
    ),
    "H4": (
        "- RESUME AT: wave <m> | converge (round <r>) | harden (round <r>) | docs wave. If "
        "anything does not match, print the RUN SUMMARY from the ledger and stop without work or "
        "writes.",
    ),
}
H2_BEFORE = "Handoff prompt:"
H3_GONE = "every wave before <m> has a verify-done line in validation.md"
# 003 FR-006/FR-008: the W2 phrase II-7 H3's 2026-10-04 amendment replaced.
H3_GONE_W2 = (
    "every wave before <m> (every wave, at a converge, harden or docs-wave phase) has a "
    "verify-done line in validation.md"
)
# HANDOFF's first paragraph ends where its numbered steps begin.
HANDOFF_FIRST_PARAGRAPH_END = "In these steps:"
H4_GONE = "RESUME AT: wave <m>. If anything does not match"

# --- II-7 N5. RUN SUMMARY (RR-8) ----------------------------------------------------------------
S1 = "first append released by relay <n>: <done | ready to close | stopped: reason> to the Lease"
S1_GONE = "<done | stopped: reason>"
SUMMARY_LEDGER_LINE = "Ledger: amendments <n> · test-owner fixes <n>"
# 003 FR-002, US1-AC3: II-7 S2 as amended 2026-10-04 (converge round 3); the 0.4.0 S2 is its
# prefix, so it has no gone phrase.
S2 = (
    "Rounds: <r> · <k1>, <k2>, … tasks appended · converged | stopped: <rule> | none (a once run)"
)
S3 = (
    "Test runs: per-wave <n> (median <M>m<SS>s) · full <n> (median <M>m<SS>s) · per-wave runs "
    "<on | off from wave <n>>"
)
S4 = (
    "RESUME AT: <wave <m> | converge (round <r>) | harden (round <r>) | docs wave> (baseline "
    "<sha>) | done"
)
S4_GONE = "RESUME AT: wave <m> (baseline <sha>) | done"
S5 = (
    "A run whose last round converged ends the summary with:",
    "READY TO CLOSE",
    "Next:",
    "1. Pending checkpoints: <V-rows> | none",
    "2. Review and commit the docs wave: <files> | none",
    "3. /s2tdd-pr-review <PR number, once the PR is open>",
    "4. /s2tdd-close",
    "The loop never runs /s2tdd-pr-review or /s2tdd-close.",
)

# --- II-7 N6. C3 run ledger ---------------------------------------------------------------------
LG2 = "released by relay <n>: <done | ready to close | stopped: reason>"
LG3 = (
    "*Rounds* the lines CONVERGE LOOP writes (Round <r>: …, Waves done: stopped before converge "
    "· …)"
)

# --- II-7 N7. Validation Gates ------------------------------------------------------------------
N7 = (
    "handoff.md contains STEP 0, SCOPE with RESUME AT and MODE, the PREFLIGHT rule, RED TEST "
    "PROTOCOL, TEST RUN, SHAPE CHECK",
    "the NOBRAKES block with CONVERGE LOOP and every feature slot filled, and ## Standard briefs "
    "with all seven briefs",
)
N7_GONE = "all five briefs"

# --- II-7 N8 / II-12. Briefs and agent bodies (agent-types.md AT-1, AT-2) ----------------------
AT1 = (
    "You stand in for the user running /s2tdd-converge on <NNN>, round <r> of nobrakes run "
    "<run id>.",
    "Run /s2tdd-converge <NNN> in the main checkout.",
    "If it still stops on unticked tasks, hand back that stop verbatim.",
    "Hand back, and nothing else:",
    "Ignore the next-step prompt converge's closing /s2tdd-next prints; its save stands.",
)
AT2 = (
    "You stand in for the user running /s2tdd-harden on <NNN> in append mode, round <r> of "
    "nobrakes run <run id>, on the tasks converge appended: T<a>–T<b>.",
    "Never renumber, rewrite or reorder an existing task, wave or contract section.",
    "Harden asks the user nothing. If one of its preconditions stops it, hand back its stop "
    "message verbatim and change nothing.",
    "Ignore the next-step prompt harden's closing /s2tdd-next prints; its save stands.",
)
CONVERGER_FILL = (
    "The orchestrator's dispatch fills the <...> slots: the feature number, the round, the run id "
    "and the docs wave."
)
HARDENER_FILL = (
    "The orchestrator's dispatch fills the <...> slots: the feature number, the round, the run id "
    "and the appended task range."
)
PV1 = (
    "The suite is <full suite command> (the project's Full suite: line, or the command found as "
    "before without one; about <minutes> min)"
)
PV1_GONE = "The suite is <suite command>"

# --- II-1. The two new agent types --------------------------------------------------------------
AGENT_FRONTMATTER = {
    "converger": {
        "name": "converger",
        "description": (
            "Stands in for the user running /s2tdd-converge in an unattended run that loops to "
            "ready-to-close; proxy tier."
        ),
        "model": "opus",
        "effort": "medium",
    },
    "hardener": {
        "name": "hardener",
        "description": (
            "Stands in for the user running /s2tdd-harden in append mode on the tasks a converge "
            "round appended, in an unattended run; strong tier."
        ),
        "model": "opus",
        "effort": "high",
    },
}

# --- II-8. Implement ----------------------------------------------------------------------------
I1 = (
    "Optional scope (S2, W4-W10, T031-T034, US5), --nobrakes [once] [week=<1-100>] "
    "[five-hour=<1-100>], --print"
)
IMPLEMENT_PHRASES = {
    "I2": (
        "once after --nobrakes, in any order with the usage limits, makes the run MODE: nobrakes "
        "once: it stops when every task in scope is ticked and skips handoff.md's CONVERGE LOOP. "
        "Without once, --nobrakes carries on through CONVERGE LOOP to a ready-to-close summary.",
    ),
    "I3": (
        'If once comes without --nobrakes, or appears twice, stop: "once applies only after '
        '--nobrakes (for example --nobrakes once week=95)."',
    ),
    "I4": ("MODE (attended, nobrakes or nobrakes once)",),
    "I5": (
        "with MODE: nobrakes, CONVERGE LOOP's converge → s2tdd:converger with the Converger "
        "brief, and its harden → s2tdd:hardener with the Hardener brief.",
    ),
    "I6": (
        "When handoff.md has no CONVERGE LOOP section, run MODE: nobrakes as MODE: nobrakes once "
        'and say once, before the first wave: "handoff.md predates the converge loop: this run '
        'stops when every task is ticked; /s2tdd-harden handoff refreshes it."',
    ),
    "I7": (
        "A relay's RESUME AT may name a phase instead of a wave: converge (round <r>), harden "
        "(round <r>) or docs wave; an empty scope then means the phase named.",
    ),
}
I4_GONE = "MODE (attended, or nobrakes)"
# 003 FR-002 (converge round 3): II-8 I10, added 2026-10-04, in User Input's --print paragraph.
I10 = (
    "With --nobrakes as well, it prints the unattended form (MODE: nobrakes, or MODE: nobrakes "
    "once with once)."
)
I10_GONE = "it prints the unattended form (MODE: nobrakes)."
# 003 FR-004, US1-AC5 (converge round 2, F1): II-8 I9, added 2026-10-04 — a --nobrakes rerun
# after a harden or converger stop resumes at that phase from the ledger's newest Rounds line.
I9 = (
    "With --nobrakes and no relay Context: block, the ledger's newest Rounds line gives the "
    "resume point when it records a stop at a phase: Round <r>: stopped · harden: … or "
    "Round <r>: stopped · hardener gave no report resumes at harden (round <r>) on that "
    "round's appended tasks; Round <r>: stopped · converger gave no report resumes at "
    "converge (round <r>). Later rounds count on from <r>."
)
# I9 sits in step 3's run-ledger.md bullet: after its lease refusal, before the scope bullet.
I9_AFTER = "Only the user writes that line."
I9_BEFORE = "With a user-named scope"
I8 = ("ready to close", "--nobrakes once")


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _missing(text: str, *phrases: str) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


def _index(flat: str, phrase: str, start: int = 0) -> int:
    i = flat.find(_flatten(phrase), start)
    assert i >= 0, f"not found: {phrase!r}"
    return i


def _heading_line(lines: list[str], heading: str) -> int:
    i = next((n for n, ln in enumerate(lines) if ln.rstrip() == heading), None)
    assert i is not None, f"heading not found: {heading}"
    return i


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


# --- harden's NOBRAKES block (wave 2, T014) -----------------------------------------------------


def test_harden_nb_converge_loop_section(skill):
    d = skill(HARDEN)
    assert not d.missing(CL1), f"{CL1!r} missing from {HARDEN}"


def test_harden_nb_converge_loop_order(skill):
    flat = skill(HARDEN).flat
    docs = _index(flat, DOCS_WAVE_FIRST)
    loop = _index(flat, CL1)
    handoff = _index(flat, HANDOFF_ANCHOR)
    assert docs < loop < handoff, (
        f"{CL1!r} must sit after {DOCS_WAVE_FIRST!r} and before {HANDOFF_ANCHOR!r}"
    )


@pytest.mark.parametrize("item", sorted(CONVERGE_LOOP, key=lambda k: int(k[2:])))
def test_harden_nb_converge_loop_phrases(skill, item):
    absent = skill(HARDEN).missing(*CONVERGE_LOOP[item])
    assert not absent, f"harden lacks II-7 {item}: {absent}"


def test_harden_nb_mode_once(skill):
    d = skill(HARDEN)
    absent = d.missing(N1A, N1B)
    assert not absent, f"harden lacks II-7 N1: {absent}"
    assert _flatten(N1B_GONE) not in d.flat, f"harden still holds {N1B_GONE!r}"


def test_harden_nb_mode_once_after_fresh_session(skill):
    flat = skill(HARDEN).flat
    fresh = _index(flat, N1A_AFTER)
    n1a = _index(flat, N1A, fresh)
    assert n1a < _index(flat, N1A_BEFORE, fresh), (
        f"N1a must sit between {N1A_AFTER!r} and {N1A_BEFORE!r}"
    )
    after = flat[fresh + len(_flatten(N1A_AFTER)):].lstrip()
    assert after.startswith(_flatten(N1A)), (
        f"N1a must sit right after {N1A_AFTER!r}, with nothing between them"
    )


def test_harden_nb_mode_once_counts_as_nobrakes(skill):
    # 003 FR-002: II-7 N1d on the line right after the frozen NOBRAKES header.
    lines = skill(HARDEN).body.split("\n")
    header = next(
        (i for i, ln in enumerate(lines) if ln.strip().startswith(NOBRAKES_HEADER)), None
    )
    assert header is not None, f"NOBRAKES header not found: {NOBRAKES_HEADER!r}"
    after = lines[header + 1] if header + 1 < len(lines) else ""
    assert _flatten(N1D) in _flatten(after), (
        f"II-7 N1d {N1D!r} must be the line right after {NOBRAKES_HEADER!r}; found {after!r}"
    )
    rest = _flatten("\n".join(lines[header + 1:]))
    assert _index(rest, N1D) < _index(rest, N1D_BEFORE), f"N1d must come before {N1D_BEFORE!r}"


def test_harden_nb_docs_wave_in_a_looping_run(skill):
    flat = skill(HARDEN).flat
    assert _flatten(N2A) in flat, f"harden lacks II-7 N2a: {N2A!r}"
    assert _index(flat, DOCS_WAVE_FIRST) < _index(flat, N2A), (
        f"N2a must follow {DOCS_WAVE_FIRST!r}"
    )


@pytest.mark.parametrize("item", sorted(HANDOFF))
def test_harden_nb_handoff_phrases(skill, item):
    absent = skill(HARDEN).missing(*HANDOFF[item])
    assert not absent, f"harden lacks II-7 {item}: {absent}"


def test_harden_nb_handoff_phase_line_before_prompt(skill):
    flat = skill(HARDEN).flat
    h2 = _index(flat, HANDOFF["H2"][0])
    assert h2 < _index(flat, H2_BEFORE, h2), f"H2 must come before {H2_BEFORE!r}"


def test_harden_nb_handoff_h1_in_first_paragraph(skill):
    flat = skill(HARDEN).flat
    start = _index(flat, HANDOFF_ANCHOR)
    h1 = _index(flat, HANDOFF["H1"][0], start)
    assert h1 < _index(flat, HANDOFF_FIRST_PARAGRAPH_END, start), (
        f"H1 must sit in HANDOFF's first paragraph, before {HANDOFF_FIRST_PARAGRAPH_END!r}"
    )


def test_harden_nb_handoff_old_expect_gone(skill):
    flat = skill(HARDEN).flat
    assert _flatten(H3_GONE) not in flat, f"harden still holds {H3_GONE!r}"


def test_harden_nb_handoff_w2_expect_gone(skill):
    flat = skill(HARDEN).flat
    assert _flatten(H3_GONE_W2) not in flat, f"harden still holds {H3_GONE_W2!r}"


def test_harden_nb_handoff_old_resume_at_gone(skill):
    flat = skill(HARDEN).flat
    assert _flatten(H4_GONE) not in flat, f"harden still holds {H4_GONE!r}"


def test_harden_nb_run_summary_lease(skill):
    d = skill(HARDEN)
    assert not d.missing(S1), f"harden lacks II-7 S1: {S1!r}"
    assert _flatten(S1_GONE) not in d.flat, f"harden still holds {S1_GONE!r}"


def test_harden_nb_run_summary_rounds_and_test_runs(skill):
    flat = skill(HARDEN).flat
    ledger = _index(flat, SUMMARY_LEDGER_LINE)
    s2 = _index(flat, S2, ledger)
    s3 = _index(flat, S3, s2)
    assert ledger < s2 < s3


def test_harden_nb_run_summary_resume_at(skill):
    d = skill(HARDEN)
    assert not d.missing(S4), f"harden lacks II-7 S4: {S4!r}"
    assert _flatten(S4_GONE) not in d.flat, f"harden still holds {S4_GONE!r}"


def test_harden_nb_run_summary_ready_to_close(skill):
    flat = skill(HARDEN).flat
    position = 0
    for phrase in S5:
        position = _index(flat, phrase, position) + 1


def test_harden_nb_ledger_rounds_heading(skill):
    lines = skill(HARDEN).body.split("\n")
    runs = _heading_line(lines, "## Runs")
    rounds = _heading_line(lines, "## Rounds")
    usage = _heading_line(lines, "## Usage")
    assert runs < rounds < usage, "## Rounds must sit between ## Runs and ## Usage"


def test_harden_nb_ledger_line_shapes(skill):
    absent = skill(HARDEN).missing(LG2, LG3)
    assert not absent, f"harden lacks II-7 N6: {absent}"


def test_harden_nb_validation_gate_briefs(skill):
    d = skill(HARDEN)
    absent = d.missing(*N7)
    assert not absent, f"harden lacks II-7 N7: {absent}"
    assert _flatten(N7_GONE) not in d.flat, f"harden still holds {N7_GONE!r}"


def test_harden_nb_brief_order(skill):
    lines = skill(HARDEN).body.split("\n")
    proxy = _heading_line(lines, PROXY_HEADING)
    converger = _heading_line(lines, CONVERGER_HEADING)
    hardener = _heading_line(lines, HARDENER_HEADING)
    reviewer = _heading_line(lines, REVIEWER_HEADING)
    assert proxy < converger < hardener < reviewer, (
        "the briefs must run Proxy verifier, Converger, Hardener, Strong-diff reviewer"
    )


def test_harden_nb_converger_brief(skill):
    brief = _subsection(skill(HARDEN).body, CONVERGER_HEADING)
    absent = _missing(brief, *AT1)
    assert not absent, f"missing from harden's Converger brief: {absent}"


def test_harden_nb_hardener_brief(skill):
    brief = _subsection(skill(HARDEN).body, HARDENER_HEADING)
    absent = _missing(brief, *AT2)
    assert not absent, f"missing from harden's Hardener brief: {absent}"


def test_harden_nb_proxy_verifier_suite_line(skill):
    d = skill(HARDEN)
    brief = _subsection(d.body, PROXY_HEADING)
    assert not _missing(brief, PV1), f"harden's Proxy verifier brief lacks PV1: {PV1!r}"
    assert _flatten(PV1_GONE) not in d.flat, f"harden still holds {PV1_GONE!r}"


# --- implement (wave 1, T010) -------------------------------------------------------------------


def test_implement_argument_hint_once(skill):
    hint = skill(IMPLEMENT).frontmatter.get("argument-hint")
    # 003 FR-002 / II-8 I1 (supersedes 002 II-10's hint).
    assert hint == I1, f"argument-hint {hint!r} is not II-8's {I1!r}"


@pytest.mark.parametrize("item", sorted(IMPLEMENT_PHRASES))
def test_implement_converge_loop_phrases(skill, item):
    absent = skill(IMPLEMENT).missing(*IMPLEMENT_PHRASES[item])
    assert not absent, f"implement lacks II-8 {item}: {absent}"


def test_implement_old_mode_gone(skill):
    flat = skill(IMPLEMENT).flat
    assert _flatten(I4_GONE) not in flat, f"implement still holds {I4_GONE!r}"


def test_implement_print_once_form(skill):
    # 003 FR-002 (converge round 3): II-8 I10 and its gone phrase.
    d = skill(IMPLEMENT)
    assert not d.missing(I10), f"implement lacks II-8 I10: {I10!r}"
    assert _flatten(I10_GONE) not in d.flat, f"implement still holds {I10_GONE!r}"


def test_implement_resume_after_harden_stop(skill):
    # 003 FR-004, US1-AC5 (converge round 2, F1): II-8 I9 in step 3's run-ledger.md bullet.
    flat = skill(IMPLEMENT).flat
    lease = _index(flat, I9_AFTER)
    i9 = _index(flat, I9, lease)
    assert i9 < _index(flat, I9_BEFORE, lease), (
        f"II-8 I9 must sit after {I9_AFTER!r} and before {I9_BEFORE!r}"
    )


def test_implement_description(skill):
    description = skill(IMPLEMENT).frontmatter.get("description", "")
    absent = [p for p in I8 if p not in description]
    assert not absent, f"implement's description lacks II-8 I8: {absent}"


# --- agents (wave 1, T011) ----------------------------------------------------------------------


@pytest.mark.parametrize("stem", sorted(AGENT_FRONTMATTER))
def test_agents_new_frontmatter(doc, stem):
    d = doc(f"agents/{stem}.md")
    assert d.frontmatter == AGENT_FRONTMATTER[stem], (
        f"agents/{stem}.md frontmatter {d.frontmatter!r} is not II-1's"
    )


def test_agents_converger_body(doc):
    d = doc(CONVERGER_AGENT)
    absent = d.missing(CONVERGER_FILL, *AT1)
    assert not absent, f"missing from {CONVERGER_AGENT}: {absent}"


def test_agents_hardener_body(doc):
    d = doc(HARDENER_AGENT)
    absent = d.missing(HARDENER_FILL, *AT2)
    assert not absent, f"missing from {HARDENER_AGENT}: {absent}"


def test_agents_proxy_verifier_suite_line(doc):
    d = doc(PROXY_AGENT)
    assert not d.missing(PV1), f"{PROXY_AGENT} lacks PV1: {PV1!r}"
    assert _flatten(PV1_GONE) not in d.flat, f"{PROXY_AGENT} still holds {PV1_GONE!r}"
