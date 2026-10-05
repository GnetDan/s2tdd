"""002 Phase 19 (T076): harden names the producer of the "carry to converge" marker.

Pins II-17a's sentence in harden's C3 line shapes and its bullet in NOBRAKES STATE (FR-019,
II-12). Phrases are transcribed from specs/002-pilot-refresh/contracts/internal-interfaces.md
II-17a; assertion style per II-0.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"

# II-17a: harden's C3 line shapes.
C3_CARRY = (
    "an Open review notes or Carried constraints line ends (carry to converge) when the item "
    "needs a ruling before close and no task covers it"
)
# II-17a: NOBRAKES STATE's bullet.
NB_STATE_CARRY = (
    "Mark a Carried constraint or Open review note (carry to converge) when it needs a ruling "
    "before close and no task covers it; converge turns each into a task or cites what "
    "resolved it."
)


def test_harden_c3_carry_marker(skill):
    d = skill(HARDEN)
    absent = d.missing(C3_CARRY)
    assert not absent, f"harden's C3 lacks II-17a's carry marker: {absent}"


def test_harden_nb_state_carry_marker(skill):
    d = skill(HARDEN)
    absent = d.missing(NB_STATE_CARRY)
    assert not absent, f"harden's NOBRAKES STATE lacks II-17a's bullet: {absent}"
