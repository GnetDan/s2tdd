"""T063: the agent-type fallback of `skills/s2tdd-implement/SKILL.md` (US4, R10, II-9).

When an `s2tdd:` agent type is unavailable (a copy of the skills carries no agents), implement
dispatches a general subagent and says each packet runs at the session's effort. Every test
first requires the fallback's `general subagent` itself, and that is the reason these fail
until T065.
"""

from __future__ import annotations

import re

SKILL = "s2tdd-implement"
GENERAL = "general subagent"


def _has_the_fallback(d):
    assert not d.missing(GENERAL), f"the fallback's `{GENERAL}` is missing from the command"


def test_dispatches_a_general_subagent_when_an_agent_type_is_unavailable(skill):
    d = skill(SKILL)
    _has_the_fallback(d)
    assert not d.missing("s2tdd:"), d.missing("s2tdd:")
    pattern = r"(unavailable|not available|isn't available|is missing|are missing)"
    assert re.search(pattern, d.flat), "no statement of when an agent type is unavailable"


def test_says_each_packet_runs_at_the_sessions_effort(skill):
    d = skill(SKILL)
    _has_the_fallback(d)
    assert re.search(r"session.s effort", d.flat), "no mention of the session's effort"
    assert not d.missing("each packet"), d.missing("each packet")
