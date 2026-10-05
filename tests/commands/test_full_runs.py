"""T015 (003 US3, US2-AC5, FR-013, FR-016, research.md R9, R10): full runs are named and reused.

Verify-done runs the `Full suite:` command, pins an unexplained red on its first wave and marks
a clean green run (internal-interfaces.md II-10, run-records.md RR-6, RR-7); converge (II-9)
and close (II-11) read the same line and reuse a green full run at the same clean commit.
Phrases are transcribed from the contract and matched through `Doc.missing` (II-0); a
superseded phrase is asserted absent on `d.flat`.
"""

from __future__ import annotations

VERIFY_DONE = "s2tdd-verify-done"
CONVERGE = "s2tdd-converge"
CLOSE = "s2tdd-close"

# II-10 (verify-done)
V1 = (
    "run the project's full suite command (its Full suite: line in the agent guidance file, "
    "otherwise the obvious one)"
)
V1_GONE = (
    "run the project's test command (from the agent guidance file, otherwise the obvious one)"
)
V2 = (
    "Unexplained red: for each red in the full run that is neither expected red nor named in a "
    "wave report, run that test alone at each wave commit of the range, oldest first (detached "
    "checkouts in the gate worktree; in the main checkout, a scratch worktree), and stop at the "
    "first commit where it is red."
)
V3 = "Red first at W<n> (<sha>): <test id> — green at W<n-1> (<sha>)"
V4 = (
    "That wave's tasks are unticked as failed claims, with the failure attached, and the "
    "verdict is Not done."
)
V5 = (
    "A test red in the full run but green alone at every commit goes to flake diagnosis "
    "(orchestration.md ground rule 17), not to a wave: it unticks nothing."
)
V6 = (
    "Append · green at <sha> after the suite suffix when the suite was the full suite command, "
    "every test passed (no expected red either), and the tree it ran in was clean at <sha> (the "
    "gate worktree at the gate's commit, or the main checkout)."
)
SUITE_TIME_BUDGET = "Suite-time budget"  # V2's order anchor
SUITE_SUFFIX_END = "(no budget) when the guidance file states none"  # V6's order anchor

# II-9 (converge)
G2 = (
    "the test command comes from the agent guidance file's Full suite: line, otherwise from the "
    "project's README/CLAUDE.md"
)
G2_GONE = "the test command comes from the project's README/CLAUDE.md)"
G3 = (
    "Before running it, reuse a green full run: when the newest verification-log line that ends "
    "· green at <sha> has <sha> equal to git rev-parse --short HEAD and git status --porcelain "
    "prints nothing, run nothing; this round's verification-log line ends · suite reused (green "
    "at <sha>) in place of the suite suffix, and the budget comparison uses that line's wall time."
)
G4 = "When the suite was reused, the suffix is · suite reused (green at <sha>) instead."

# II-11 (close)
C1 = (
    "Run the project's full test command (its Full suite: line in the agent guidance file, "
    "otherwise from its agent guidance file or README), including the acceptance suite."
)
C1_GONE = "(from its agent guidance file or README)"
C1_KEPT = ("full test command", "green")  # tests/commands/test_close.py
# A2's own gate sentence: C1, C2 and C3 already hold "full test command" and "green", so the
# kept gate is checked inside the A2 paragraph (from A2_START up to A3_START).
A2_GATE = "Green is the gate."
A2_START = "**A2. Suite.**"
A3_START = "**A3. Checkpoints.**"
C2 = (
    "Before running it, reuse a green full run: when the newest verification-log line that ends "
    "· green at <sha> has <sha> equal to git rev-parse --short HEAD and git status --porcelain "
    "prints nothing, run nothing, and the close-out header says Suite: reused green run at <sha> "
    "(<the verification-log line's date> verify-done)."
)
C3 = (
    "**Suite**: [green | reused green run at <sha> (<date> verify-done) | red — accepted: <note>]"
)


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


# verify-done


def test_verify_done_runs_the_full_suite_line(skill):
    d = skill(VERIFY_DONE)
    assert not d.missing(V1), d.missing(V1)


def test_verify_done_old_test_command_is_gone(skill):
    d = skill(VERIFY_DONE)
    assert _flatten(V1_GONE) not in d.flat, V1_GONE


def test_verify_done_pins_an_unexplained_red(skill):
    d = skill(VERIFY_DONE)
    phrases = (V2, V3, V4, V5)
    assert not d.missing(*phrases), d.missing(*phrases)


def test_verify_done_unexplained_red_follows_the_budget(skill):
    d = skill(VERIFY_DONE)
    assert not d.missing(V2), d.missing(V2)
    budget = d.flat.index(_flatten(SUITE_TIME_BUDGET))
    assert budget < d.flat.index(_flatten(V2)), budget


def test_verify_done_marks_a_clean_green_run(skill):
    d = skill(VERIFY_DONE)
    assert not d.missing(V6, SUITE_SUFFIX_END), d.missing(V6, SUITE_SUFFIX_END)
    suffix = d.flat.index(_flatten(SUITE_SUFFIX_END))
    assert suffix < d.flat.index(_flatten(V6)), suffix


# converge


def test_converge_reads_the_full_suite_line(skill):
    d = skill(CONVERGE)
    assert not d.missing(G2), d.missing(G2)


def test_converge_old_test_command_is_gone(skill):
    d = skill(CONVERGE)
    assert _flatten(G2_GONE) not in d.flat, G2_GONE


def test_converge_reuses_a_green_full_run(skill):
    d = skill(CONVERGE)
    assert not d.missing(G2, G3), d.missing(G2, G3)
    assert d.flat.index(_flatten(G2)) < d.flat.index(_flatten(G3)), "G3 must follow G2"


def test_converge_reused_suffix(skill):
    d = skill(CONVERGE)
    assert not d.missing(G4), d.missing(G4)


# close


def test_close_runs_the_full_suite_line(skill):
    d = skill(CLOSE)
    assert not d.missing(C1), d.missing(C1)


def test_close_old_test_command_is_gone(skill):
    d = skill(CLOSE)
    assert _flatten(C1_GONE) not in d.flat, C1_GONE


def test_close_keeps_its_suite_gate(skill):
    d = skill(CLOSE)
    assert not d.missing(*C1_KEPT), d.missing(*C1_KEPT)
    start = d.flat.find(_flatten(A2_START))
    assert start >= 0, f"close has no {A2_START!r} paragraph"
    end = d.flat.find(_flatten(A3_START), start)
    a2 = d.flat[start:] if end < 0 else d.flat[start:end]
    assert _flatten(A2_GATE) in a2, f"close's A2 paragraph lacks its gate: {A2_GATE!r}"


def test_close_reuses_a_green_full_run(skill):
    d = skill(CLOSE)
    assert not d.missing(C2), d.missing(C2)


def test_close_out_header_names_the_reused_run(skill):
    d = skill(CLOSE)
    assert not d.missing(C3), d.missing(C3)
