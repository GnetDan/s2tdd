"""003 PR #8 review fixes (packet nobrakes): a --nobrakes once run stays a once run across
relays (H-1, C-1), MODE: nobrakes once counts as MODE: nobrakes outside NOBRAKES too (H-2, C-2),
the once stop is spelled out (H-3), a converge stop and the phase-change Boundary line have
ledger shapes (H-4, H-8), rule 1's count survives a handoff (H-5), TEST RUN's slots and scope are
named (H-6, H-9), the proxy verifier runs the filled suite command (H-7), and a rerun after a stop
at the converge→harden phase change resumes at harden (S-1).

Every sentence here is added beside the pinned phrases it clarifies; none rewords them. The
sentences inside handoff.md's prompt and briefs are mirrored into the eval fixture's 0.4.0
handoff text (evals/fixtures/make-feature.sh, write_handoff_040), which transcribes harden.
"""

from __future__ import annotations

from pathlib import Path

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"
FIXTURE = "evals/fixtures/make-feature.sh"
FIXTURE_START = "write_handoff_040()"
FIXTURE_END = "\nEND_HANDOFF"

# H-1 / C-1: the handoff prompt carries once.
H1_TEMPLATE = "Handoff prompt: /s2tdd-implement --nobrakes[ once] <waves left in the run's scope>"
H1_ONCE = (
    "With MODE: nobrakes once, the prompt's first line carries once right after --nobrakes, at a "
    "wave or a phase (/s2tdd-implement --nobrakes once …), so the next relay is a once run too."
)
H1_AFTER = (
    "At a converge, harden or docs-wave phase, the prompt's first line is /s2tdd-implement "
    "--nobrakes, with no scope: the phase comes from RESUME AT."
)
H1_BEFORE = "Handoff prompt:"
C1 = (
    "A once run's handoff prompt carries once on its first line, so each of its relays is a once "
    "run too. A relay whose Context: block names a run that run-ledger.md's Runs line records as "
    "run <id> · nobrakes once · … runs as MODE: nobrakes once even when its first line lacks once."
)

# H-2: the once equivalence at SCOPE level, before every rule that branches on MODE.
H2 = (
    "With MODE: nobrakes once, every rule this prompt gives for MODE: nobrakes applies (SHAPE "
    "CHECK, MUST BREACH, the report's Boundary line, NOBRAKES), except CONVERGE LOOP."
)
H2_BEFORE_HARDEN = "SHAPE CHECK (both modes; every wave that holds a test packet)"
H2_BEFORE_FIXTURE = "HOW TO WORK"

# H-3: the once stop, after the pinned N1a.
N1A = (
    "MODE: nobrakes once runs every rule here except CONVERGE LOOP; it stops after the last wave "
    "in SCOPE as 0.3.0 did."
)
H3 = (
    "That stop is NOBRAKES's own, never the attended one: after the last wave in SCOPE come "
    "VERIFY GATES, the DOCS WAVE (none: skip it) and the RUN SUMMARY, with HANDOFF whenever it "
    "falls due."
)
H3_BEFORE = "STATE lives in files, never only in this context."

# H-4: a converge stop is a CONVERGE LOOP branch and a Rounds shape.
H4_AFTER = "Round <r>: stopped · converger gave no report"
H4 = (
    "A converger that hands back converge's stop on unticked tasks stops the run: Round <r>: "
    "stopped · converge: <its stop message>, then print the RUN SUMMARY."
)
H4_BEFORE = "- Converged: build the DOCS WAVE"
H4_C3 = "*Rounds* also holds Round <r>: stopped · converge: <converge's stop message>."

# H-5: rule 1's count without the upkeep task, read back from the ledger.
H5_AFTER = "left out of rule 1's counts."
H5 = (
    "The Rounds line's <k> counts every appended task, upkeep included, and its cites list writes "
    "the upkeep task as T<n> upkeep: rule 1 takes round <r-1>'s count from that cites list, "
    "without the upkeep task."
)

# H-6: TEST RUN's slots are on its second line, with no minutes slot.
H6_FILL = (
    "fill its Per-wave tests line, the block's second line under its header, from the project's "
    "test lines"
)
H6_GONE = "fill its first line from the project's test lines"
H6_L5 = (
    "TEST RUN's first line is its Per-wave tests line, right under the block's header, and takes "
    "the commands only; the measured minutes go to the Proxy verifier brief's <minutes>."
)

# H-7: the proxy verifier runs the command filled in, and looks for no other.
H7_AFTER = "found as before without one"
H7 = "Run that command as written; look for no other."
H7_BEFORE = "### Converger"

# H-8: the phase-change Boundary line's shape, in CONVERGE LOOP's phase-change bullet (BOUNDARY's
# paragraph must keep ending with II-7 BD2) and in C3's Usage shapes.
H8_AFTER = (
    "HANDOFF's next-step estimate for a converge or harden step is one hand-back (about 5k "
    "tokens)."
)
H8 = (
    "At a phase change, BOUNDARY's line under the ledger's Usage section starts with the phase: "
    "<converge (round <r>) | harden (round <r>) | docs wave> · Boundary: context <x>% · five-hour "
    "<y>% · week <z>% · BRAKES <none|found> · ledger +<n> lines."
)
H8_BEFORE = "No round cap"
H8_C3 = (
    "*Usage* also holds, at a phase change, <converge (round <r>) | harden (round <r>) | docs "
    "wave> · Boundary: context <x>% · five-hour <y>% · week <z>% · BRAKES <none|found> · ledger "
    "+<n> lines."
)

# H-9: what "the run" means for per-wave runs off, and how they come back on.
H9_AFTER = "The wave report's Test run: line names the run, its command, its counts and its wall time."
H9 = (
    "The run is this session with MODE: attended, or every relay of the nobrakes run. A later "
    "session or run tries per-wave runs again and records the Carried constraint Per-wave runs on "
    "from wave <m>; the newest Per-wave runs line is in force."
)
H9_BEFORE = "RED TEST PROTOCOL"

# S-1: a rerun after a stop at the converge→harden phase change resumes at harden.
I9_END = "Later rounds count on from <r>."
S1 = (
    "A newest Rounds line Round <r>: converge at <sha> · <k> tasks appended (T<a>–T<b>) · …, with "
    "no later Round <r>: hardened or Round <r>: stopped line, resumes at harden (round <r>) on "
    "T<a>–T<b>: a stop at the phase change after that converge leaves it newest."
)
S1_BEFORE = "With a user-named scope"

# C-2: an older handoff.md is filled MODE: nobrakes; step 6 counts once as nobrakes.
I6_END = "stops when every task is ticked; /s2tdd-harden handoff refreshes it."
C2_OLD = (
    "There, step 5 fills MODE: nobrakes even with once: that handoff.md's NOBRAKES section runs "
    "only for MODE: nobrakes, and it already stops after the last wave in SCOPE."
)
C2_STEP6 = (
    "MODE: nobrakes once counts as MODE: nobrakes throughout this step, except that it skips "
    "CONVERGE LOOP: no converger or hardener is dispatched."
)
STEP6_START = "6. Run it."
STEP6_END = "## Completion Report"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _index(flat: str, phrase: str, start: int = 0) -> int:
    i = flat.find(_flatten(phrase), start)
    assert i >= 0, f"not found: {phrase!r}"
    return i


def _in_order(flat: str, *phrases: str) -> None:
    pos = 0
    for phrase in phrases:
        pos = _index(flat, phrase, pos)


def _fixture_040(repo_root: Path) -> str:
    text = (repo_root / FIXTURE).read_text(encoding="utf-8")
    start = text.find(FIXTURE_START)
    assert start >= 0, f"{FIXTURE} lacks {FIXTURE_START}"
    end = text.find(FIXTURE_END, start)
    assert end > start, f"{FIXTURE}: no END_HANDOFF after {FIXTURE_START}"
    return _flatten(text[start:end])


def test_harden_handoff_prompt_carries_once(skill):
    flat = skill(HARDEN).flat
    _in_order(flat, H1_AFTER, H1_ONCE, H1_BEFORE)
    assert _flatten(H1_TEMPLATE) in flat, f"harden lacks {H1_TEMPLATE!r}"


def test_implement_relay_of_a_once_run_stays_once(skill):
    assert _flatten(C1) in skill(IMPLEMENT).flat, f"implement lacks {C1!r}"


def test_harden_once_counts_as_nobrakes_before_shape_check(skill):
    _in_order(skill(HARDEN).flat, H2, H2_BEFORE_HARDEN)


def test_harden_once_stop_spelled_out_after_n1a(skill):
    _in_order(skill(HARDEN).flat, N1A, H3, H3_BEFORE)


def test_harden_converge_stop_branch_and_shape(skill):
    flat = skill(HARDEN).flat
    _in_order(flat, H4_AFTER, H4, H4_BEFORE)
    assert _flatten(H4_C3) in flat, f"harden's C3 lacks {H4_C3!r}"


def test_harden_rule_1_count_from_cites_list(skill):
    _in_order(skill(HARDEN).flat, H5_AFTER, H5)


def test_harden_test_run_slots_named(skill):
    flat = skill(HARDEN).flat
    assert _flatten(H6_GONE) not in flat, f"harden still holds {H6_GONE!r}"
    absent = [p for p in (H6_FILL, H6_L5) if _flatten(p) not in flat]
    assert not absent, f"harden lacks {absent}"


def test_harden_proxy_verifier_runs_filled_command(skill):
    _in_order(skill(HARDEN).flat, H7_AFTER, H7, H7_BEFORE)


def test_harden_phase_change_boundary_shape(skill):
    flat = skill(HARDEN).flat
    _in_order(flat, H8_AFTER, H8, H8_BEFORE)
    assert _flatten(H8_C3) in flat, f"harden's C3 lacks {H8_C3!r}"


def test_harden_per_wave_runs_off_scope(skill):
    _in_order(skill(HARDEN).flat, H9_AFTER, H9, H9_BEFORE)


def test_implement_resumes_at_harden_after_converge_line(skill):
    _in_order(skill(IMPLEMENT).flat, I9_END, S1, S1_BEFORE)


def test_implement_older_handoff_fills_nobrakes(skill):
    _in_order(skill(IMPLEMENT).flat, I6_END, C2_OLD)


def test_implement_step_6_counts_once_as_nobrakes(skill):
    flat = skill(IMPLEMENT).flat
    start = _index(flat, STEP6_START)
    end = _index(flat, STEP6_END, start)
    assert start < _index(flat, C2_STEP6, start) < end, (
        f"implement step 6 lacks {C2_STEP6!r}"
    )


def test_fixture_040_handoff_mirrors_harden(repo_root):
    flat = _fixture_040(repo_root)
    _in_order(flat, H2, H2_BEFORE_FIXTURE)
    _in_order(flat, H9_AFTER, H9, H9_BEFORE)
    _in_order(flat, N1A, H3, H3_BEFORE)
    _in_order(flat, H4_AFTER, H4, H4_BEFORE)
    _in_order(flat, H5_AFTER, H5)
    _in_order(flat, H1_AFTER, H1_ONCE, H1_BEFORE)
    assert _flatten(H1_TEMPLATE) in flat, f"fixture lacks {H1_TEMPLATE!r}"
    _in_order(flat, H8_AFTER, H8, H8_BEFORE)
    _in_order(flat, H7_AFTER, H7, H7_BEFORE)
