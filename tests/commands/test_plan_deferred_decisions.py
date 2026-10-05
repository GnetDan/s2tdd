"""Plan never settles a decision the user deferred (review finding Q3-2).

specify leaves `[NEEDS CLARIFICATION]` markers in spec.md for questions the user deferred, and
clarify writes `- Deferred:` bullets; both say a deferred decision is still the user's, not
something planning resolves by research. Plan must stop on them and point at /s2tdd-clarify
before any research, and its Phase 0 must research only the technical unknowns plan itself
marked in Technical Context.
"""

from __future__ import annotations

SKILL = "s2tdd-plan"


def _before_outline(text: str) -> str:
    return text.split("## Outline", 1)[0]


def test_guard_on_open_spec_decisions_before_outline(skill):
    head = _before_outline(skill(SKILL).text)
    phrases = ("[NEEDS CLARIFICATION", "- Deferred:", "/s2tdd-clarify")
    missing = [p for p in phrases if p not in head]
    assert not missing, f"no open-decisions guard before the Outline; missing {missing}"


def test_deferred_decisions_are_never_researched(skill):
    d = skill(SKILL)
    assert not d.missing("never research"), d.missing("never research")


def test_phase_0_does_not_resolve_every_marker(skill):
    # The unscoped upstream wording reads as licence to research spec-level markers away.
    d = skill(SKILL)
    stale = [p for p in ("resolve all NEEDS CLARIFICATION", "with all NEEDS CLARIFICATION resolved")
             if p in d.text]
    assert not stale, f"Phase 0 still resolves every marker: {stale}"


def test_error_rule_names_what_it_errors_on(skill):
    d = skill(SKILL)
    assert "ERROR on gate failures or unresolved clarifications" not in d.text, (
        "the ERROR rule still leaves 'unresolved clarifications' undefined"
    )
