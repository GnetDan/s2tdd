"""002 Phase 19 (T079; R15): the newest Usage limits line is the one in force.

Pins II-17e's sentence in harden's NOBRAKES STATE and implement's *User Input*, and its line
shape in harden's C3 line shapes (FR-021). Phrases are transcribed from
specs/002-pilot-refresh/contracts/internal-interfaces.md II-17e; assertion style per II-0.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"

# II-17e: NOBRAKES STATE and implement's User Input, exact.
LATER_RELAY_LIMITS = (
    "Limits given to a later relay, in its arguments or its pasted Context: block, are appended "
    "as a new Carried constraint, Usage limits: week <n>%, five-hour <n>% (given at relay <n>; "
    "supersedes relay <m>'s), and the newest Usage limits line is the one in force."
)
# II-17e: harden's C3 line shapes.
C3_SUPERSEDING_LINE = (
    "a later relay's Usage limits: week <n>%, five-hour <n>% (given at relay <n>; supersedes "
    "relay <m>'s)"
)


def test_harden_nb_later_relay_limits_supersede(skill):
    d = skill(HARDEN)
    absent = d.missing(LATER_RELAY_LIMITS)
    assert not absent, f"harden's NOBRAKES STATE lacks II-17e's sentence: {absent}"


def test_implement_later_relay_limits_supersede(skill):
    d = skill(IMPLEMENT)
    absent = d.missing(LATER_RELAY_LIMITS)
    assert not absent, f"implement's User Input lacks II-17e's sentence: {absent}"


def test_harden_c3_superseding_usage_limits_line(skill):
    d = skill(HARDEN)
    absent = d.missing(C3_SUPERSEDING_LINE)
    assert not absent, f"harden's C3 lacks II-17e's line shape: {absent}"
