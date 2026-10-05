"""T009 (003 US1, FR-007, FR-008, research.md R7): the docs wave is a checkpoint, not a gap.

Converge sets the docs wave's unticked tasks aside whether the ledger records it built or not
(internal-interfaces.md II-9 G1), close gates on a built, uncommitted docs wave (II-11 C0), and
harden's DOCS WAVE paragraph says when a looping run builds it (II-7 N2a). Phrases are
transcribed from the contract and matched through `Doc.missing` (II-0).
"""

from __future__ import annotations

CONVERGE = "s2tdd-converge"
CLOSE = "s2tdd-close"
HARDEN = "s2tdd-harden"

G1 = (  # II-9 G1
    "Also set aside the docs wave's unticked tasks when run-ledger.md exists and handoff.md names "
    "a docs wave (DOCS WAVE (W<n>)), whether the ledger records it built or not; list them in the "
    "summary as docs wave (pending)."
)
GUARD_KEPT = (  # tests/commands/test_converge.py::test_guard_sets_aside_pending_checkpoints
    "whose description begins checkpoint",
    "after any [p] and [usn] markers",
    "pending checkpoints",
    "if any other unticked task remains, stop without writing anything",
    "task(s) in tasks.md are unticked; finish implementing (and verify) them before converging.",
)
C0_HEADING = (  # II-11 C0
    "**A0. Docs wave (gate — check first, before A4, so a STOP here writes nothing).**"
)
C0_BODY = (  # II-11 C0
    "When run-ledger.md records a docs wave built and uncommitted (Docs wave <n> built, "
    "uncommitted: <files>) and its files are still uncommitted, STOP with no writes: "
    '"Review and commit the docs wave first: <files>."'
)
N2_FIRST = "DOCS WAVE (<docs wave>) runs last in the run"  # II-7 N2, kept
N2A = (  # II-7 N2a
    "In a looping run it runs once, after the round whose converge reports converged, and before "
    "the RUN SUMMARY; until then converge sets its tasks aside."
)
CL1 = "CONVERGE LOOP (MODE: nobrakes only)."  # II-7 N3 CL1, the section after DOCS WAVE


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _paragraph(d, opening: str) -> str:
    """The flattened paragraph of the skill body that starts with `opening`, plus the list
    right after it (if any)."""
    blocks = d.body.split("\n\n")
    for i, block in enumerate(blocks):
        if block.lstrip().startswith(opening):
            text = block
            for after in blocks[i + 1 :]:
                if not after.lstrip().startswith("- "):
                    break
                text += "\n" + after
            return _flatten(text)
    raise AssertionError(f"no paragraph starts with {opening!r}")


def test_converge_guard_sets_aside_the_docs_wave(skill):
    guard = _paragraph(skill(CONVERGE), "**Implementation-complete guard**")
    assert _flatten(G1) in guard, (G1, guard)
    assert guard.index(_flatten(G1)) < guard.index("if any other unticked task remains"), guard


def test_converge_guard_keeps_its_pending_checkpoint_phrases(skill):
    guard = _paragraph(skill(CONVERGE), "**Implementation-complete guard**")
    for phrase in GUARD_KEPT:
        assert phrase in guard, (phrase, guard)


def test_close_docs_wave_gate(skill):
    d = skill(CLOSE)
    assert not d.missing(C0_HEADING, C0_BODY), d.missing(C0_HEADING, C0_BODY)


def test_close_docs_wave_gate_is_phase_a_first_item(skill):
    d = skill(CLOSE)
    assert "a0. docs wave" in d.flat, "A0. Docs wave missing from close"
    assert d.flat.index("a0. docs wave") < d.flat.index("a1. tasks"), d.flat


def test_harden_nb_docs_wave_runs_once_after_the_loop(skill):
    d = skill(HARDEN)
    assert not d.missing(N2_FIRST, N2A), d.missing(N2_FIRST, N2A)
    first = d.flat.index(_flatten(N2_FIRST))
    n2a = d.flat.index(_flatten(N2A))
    assert first < n2a < d.flat.index(_flatten(CL1)), (first, n2a)
