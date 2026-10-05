"""002 Phase 19 (T077): harden's "full fence set" is the packet's targeted fence commands.

Pins the TIER sentence (003 II-4's TI1 since 003 T002; it supersedes II-17b's per 003
FR-011) and Phase B4's *Dispatching the remaining judgment* (1) phrase, and the old (1) phrase
gone (FR-025, SC-007). Phrases are transcribed from
specs/002-pilot-refresh/contracts/internal-interfaces.md II-17b, and TI1 from
specs/003-nobrakes-ready-to-close/contracts/internal-interfaces.md II-4; assertion style per
II-0.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"

# 003 II-4 TI1: TIER. Supersedes 002 II-17b's sentence per 003 FR-011: the orchestrator's one
# test run per wave, not one full suite per wave.
TIER_FENCE_SET = (
    "The full fence set is the packet's targeted fence commands (its done-when and the checks "
    "its wave-table row names), never the full suite: the orchestrator's one test run per wave "
    "stays the only wave-level run."
)
# 003 II-4: gone from harden.
TIER_GONE = "stays the only full suite"
# II-17b: Dispatching the remaining judgment (1).
DISPATCHING_FENCE_SET = "the full fence set (targeted, never the full suite) before acceptance"
# II-17b: gone.
DISPATCHING_GONE = "the full fence set before acceptance"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def test_harden_tier_full_fence_set_is_targeted(skill):
    d = skill(HARDEN)
    absent = d.missing(TIER_FENCE_SET)
    assert not absent, f"harden's TIER lacks 003 II-4's TI1: {absent}"
    assert _flatten(TIER_GONE) not in d.flat, f"harden still holds {TIER_GONE!r}"


def test_harden_dispatching_full_fence_set(skill):
    d = skill(HARDEN)
    absent = d.missing(DISPATCHING_FENCE_SET)
    assert not absent, f"harden's Dispatching (1) lacks II-17b's phrase: {absent}"
    assert _flatten(DISPATCHING_GONE) not in d.flat, f"harden still holds {DISPATCHING_GONE!r}"
