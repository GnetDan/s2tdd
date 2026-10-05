"""T055: escalation raises the effort, and the harness fallbacks (EC-003, FR-029; II-3, II-10).

Harden's TIER and Phase B4's *Dispatching the remaining judgment* (5) gain II-3's escalation
phrase, and TIER's general-subagent fallback ends `tiers then become fence strictness`.
Implement gathers the harnesses that lack a mechanism into one paragraph headed
`**Harnesses without a mechanism.**`: no usage tool or plan windows, no push notification, no
agent types. Every phrase is transcribed from contracts/internal-interfaces.md (002). These
fail until T056 and T057.
"""

from __future__ import annotations

import re

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"

# II-3: the escalation phrase, and the end of the general-subagent fallback.
ESCALATION = "each escalation step raises the effort (cheap low → medium medium → strong high)"
FALLBACK_START = "dispatch a general subagent"
FALLBACK_END = (
    "and say that each packet runs at this session's effort; tiers then become fence strictness"
)

# Section markers of harden, flattened (searched from the previous marker on).
TIER_MARK = "- TIER:"
SHAPE_CHECK_HEAD = "SHAPE CHECK (both modes; every wave that holds a test packet)"
CHECKPOINT_ROWS_MARK = "- CHECKPOINT ROWS:"
DISPATCHING_MARK = "Dispatching the remaining judgment"
ITEM_5_MARK = "(5)"
BUDGET_MARK = "Context budget note"

# II-10: implement's one place for the harnesses without a mechanism.
HARNESSES_LEAD = "**Harnesses without a mechanism.**"
NO_USAGE_TOOL = ("the window limits do not apply", "n/a")
NO_PUSH = "no push notification: print only"
NO_AGENT_TYPES = "general subagent"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _at(flat: str, phrase: str, where: str, start: int = 0) -> int:
    """The index of the phrase's first occurrence at or after start; fail when absent."""
    i = flat.find(_flatten(phrase), start)
    assert i >= 0, f"`{phrase}` missing from {where}"
    return i


def _tier_section(flat: str) -> str:
    """Harden's TIER item: from `- TIER:` to the start of the next item, which is the bullet
    holding the SHAPE CHECK head when that comes before `- CHECKPOINT ROWS:`, else that one."""
    where = f"skills/{HARDEN}/SKILL.md"
    start = _at(flat, TIER_MARK, where)
    end = _at(flat, CHECKPOINT_ROWS_MARK, where, start)
    head = flat.find(_flatten(SHAPE_CHECK_HEAD), start)
    if 0 <= head < end:
        bullet = flat.rfind(" - ", start, head)  # a line-start "- ", flattened
        assert bullet > start, f"no list item holds the SHAPE CHECK head after TIER in {where}"
        end = bullet
    return flat[start:end]


def _harnesses_paragraph(body: str) -> str:
    """Implement's paragraph headed by the lead: its lines up to the next blank line."""
    lines = body.split("\n")
    starts = [i for i, line in enumerate(lines) if line.strip().startswith(HARNESSES_LEAD)]
    assert starts, f"`{HARNESSES_LEAD}` missing from {IMPLEMENT}"
    paragraph = []
    for line in lines[starts[0]:]:
        if not line.strip():
            break
        paragraph.append(line)
    return "\n".join(paragraph)


# --- harden: escalation (II-3; EC-003) ------------------------------------------------------


def test_harden_tier_says_each_escalation_step_raises_the_effort(skill):
    d = skill(HARDEN)
    section = _tier_section(d.flat)
    assert _flatten(ESCALATION) in section, (
        f"`each escalation step raises the effort` missing from {HARDEN}'s TIER: `{ESCALATION}`"
    )


def test_harden_dispatching_judgment_item_5_says_each_escalation_step_raises_the_effort(skill):
    d = skill(HARDEN)
    where = f"skills/{HARDEN}/SKILL.md"
    start = _at(d.flat, DISPATCHING_MARK, where)
    five = _at(d.flat, ITEM_5_MARK, f"{where}'s {DISPATCHING_MARK}", start)
    end = _at(d.flat, BUDGET_MARK, where, five)
    assert _flatten(ESCALATION) in d.flat[five:end], (
        f"`each escalation step raises the effort` missing from {HARDEN}'s "
        f"{DISPATCHING_MARK} (5): `{ESCALATION}`"
    )


def test_harden_general_subagent_fallback_ends_with_fence_strictness(skill):
    d = skill(HARDEN)
    section = _tier_section(d.flat)
    start = section.find(_flatten(FALLBACK_START))
    assert start >= 0, f"`{FALLBACK_START}` missing from {HARDEN}'s TIER"
    end = section.find(_flatten(FALLBACK_END), start)
    assert end >= 0, f"{HARDEN}'s general-subagent fallback does not end `…{FALLBACK_END}`"
    rest = section[end + len(_flatten(FALLBACK_END)):]
    assert re.match(r"^\s*(\.|$)", rest), (
        f"{HARDEN}'s general-subagent fallback goes on after `tiers then become fence "
        f"strictness`: `{rest[:80]}`"
    )


# --- implement: harnesses without a mechanism (II-10; FR-029) -------------------------------


def test_implement_harnesses_without_a_mechanism_is_one_place(skill):
    d = skill(IMPLEMENT)
    count = d.body.count(HARNESSES_LEAD)
    assert count == 1, f"`{HARNESSES_LEAD}` appears {count} times in {IMPLEMENT}, not once"


def test_implement_harnesses_no_usage_tool_window_limits_do_not_apply(skill):
    d = skill(IMPLEMENT)
    flat = _flatten(_harnesses_paragraph(d.body))
    missing = [p for p in NO_USAGE_TOOL if _flatten(p) not in flat]
    assert not missing, f"missing from {IMPLEMENT}'s `{HARNESSES_LEAD}` paragraph: {missing}"


def test_implement_harnesses_no_push_notification_prints_only(skill):
    d = skill(IMPLEMENT)
    flat = _flatten(_harnesses_paragraph(d.body))
    assert _flatten(NO_PUSH) in flat, (
        f"`{NO_PUSH}` missing from {IMPLEMENT}'s `{HARNESSES_LEAD}` paragraph"
    )


def test_implement_harnesses_no_agent_types_general_subagent(skill):
    d = skill(IMPLEMENT)
    flat = _flatten(_harnesses_paragraph(d.body))
    assert _flatten(NO_AGENT_TYPES) in flat, (
        f"`{NO_AGENT_TYPES}` missing from {IMPLEMENT}'s `{HARNESSES_LEAD}` paragraph"
    )
