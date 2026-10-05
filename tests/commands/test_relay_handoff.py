"""002 US7 (T019): relays hand off by printing and notifying; the handoff prompt points at the
Carried constraints and restates none (II-8, II-10; FR-020, R10).

Supersedes 001 EC-004: `tests/commands/test_harden_handoff_prompt.py` and
`test_001_ec004_git_bash_handoff` are retired with this file.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"

# II-8: HANDOFF step 4 (transcribed).
HANDOFF_STEP_4 = (
    "4. print the handoff prompt, send a push notification where the harness can "
    "(PushNotification in Claude Code; elsewhere print only), and stop.",
    "Never start the next relay as a scheduled task or a background session: the user pastes "
    "the prompt to start it.",
)
# II-8: gone from harden.
GONE_FROM_HARDEN = ("MSYS_NO_PATHCONV", "claude -p", "one-shot scheduled task")
# HANDOFF step 3, kept.
HANDOFF_FILE = "write the handoff prompt to `.sdd-run/<NNN>/handoff-<n+1>.md`"

# II-8: the handoff prompt template's `Context:` gains these two lines.
CONTEXT_LINES = (
    "- Carried constraints: see <FEATURE_DIR>/run-ledger.md; this prompt restates none of them.",
    "- Five-hour window resets at <reset time>: start after it.",
)
# The template's header and the NOBRAKES marker that follows HANDOFF (test_chain_rules.py).
TEMPLATE_START = "Handoff prompt:\n    /s2tdd-implement --nobrakes"
TEMPLATE_END = "BRAKES. When the user asks for brakes in chat"

# II-10: implement's frontmatter `description`.
DESCRIPTION_GONE = "hands off to a fresh session"
DESCRIPTION_HAS = "hands off by printing"


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def test_harden_nb_handoff_step_4_prints_notifies_and_stops(skill):
    d = skill(HARDEN)
    absent = d.missing(*HANDOFF_STEP_4)
    assert not absent, f"harden lacks II-8's HANDOFF step 4: {absent}"


def test_harden_nb_starts_no_session(skill):
    d = skill(HARDEN)
    present = [p for p in GONE_FROM_HARDEN if _flatten(p) in d.flat]
    assert not present, f"harden still holds what II-8 removes: {present}"


def test_harden_nb_keeps_the_handoff_file(skill):
    d = skill(HARDEN)
    assert not d.missing(HANDOFF_FILE), d.missing(HANDOFF_FILE)


def test_harden_nb_handoff_prompt_template_context_lines(skill):
    d = skill(HARDEN)
    start = d.flat.find(_flatten(TEMPLATE_START))
    assert start >= 0, f"harden lacks the handoff prompt template: {TEMPLATE_START!r}"
    end = d.flat.find(_flatten(TEMPLATE_END), start)
    assert end > start, f"no {TEMPLATE_END!r} after the handoff prompt template"
    template = d.flat[start:end]
    absent = [line for line in CONTEXT_LINES if _flatten(line) not in template]
    assert not absent, f"the handoff prompt template lacks II-8's Context: lines: {absent}"


def test_implement_description_hands_off_by_printing(skill):
    d = skill(IMPLEMENT)
    description = _flatten(str(d.frontmatter.get("description", "")))
    assert _flatten(DESCRIPTION_GONE) not in description, (
        f"implement's description still says {DESCRIPTION_GONE!r}"
    )
    assert _flatten(DESCRIPTION_HAS) in description, (
        f"implement's description lacks {DESCRIPTION_HAS!r}"
    )
