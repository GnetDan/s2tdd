"""002 US8 (T030): usage limits per window. `week=` stops the run, `five-hour=` hands off, both
are recorded as Carried constraints, and no usage tool means no window limits (II-8, II-10;
FR-021, R5).
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"

# II-8: Usage (transcribed).
USAGE = (
    "In Claude Code, read usage with the get_usage tool (the context window's percent used and "
    "the plan's five-hour, weekly and per-model weekly windows, each with its reset time).",
    "The week limit applies to the highest of the weekly window and the per-model weekly window "
    "of a model the run uses.",
    "Where no usage tool exists, or the plan is not_applicable, the window limits do not apply: "
    "say so once at run start, record it as a Carried constraint, write n/a for the windows in "
    "each Boundary line, and estimate context from the ledger's Usage lines.",
    "unavailable is retried at the next boundary",
)
# II-8: Limits (STOP THE RUN and HANDOFF).
LIMITS = (
    "weekly usage reaches the run's week limit (a Carried constraint; default 95%)",
    "or five-hour usage reaches the run's five-hour limit (default 90%): reach a clean boundary "
    "and hand off with the window's reset time in the handoff prompt",
    "The first relay records both limits as Carried constraints: Usage limits: week <n>%, "
    "five-hour <n>% (<given|default>)",
    "handed off by relay <n> (five-hour, resets <time>)",
)
# II-8: gone from harden.
LIMIT_GONE = "reaches 90% of a rate-limit window"

# II-10: implement.
# 003 FR-002 / II-8 I1 (supersedes 002 II-10's hint): --nobrakes gains [once].
ARGUMENT_HINT = (
    "Optional scope (S2, W4-W10, T031-T034, US5), --nobrakes [once] [week=<1-100>] "
    "[five-hour=<1-100>], --print"
)
LIMITS_PHRASE = (
    "week=<n> and five-hour=<n>, each an integer percent from 1 to 100, in any order after "
    "--nobrakes"
)
REFUSAL = (
    "Usage limits are week=<n> and five-hour=<n>, each an integer from 1 to 100 (for example "
    "week=99 five-hour=90)."
)
DEFAULTS = "week 95, five-hour 90"
RECORDING = (
    "The first relay records both limits, given or default, as Carried constraints; later "
    "relays read them from there."
)


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def test_harden_nb_usage(skill):
    d = skill(HARDEN)
    absent = d.missing(*USAGE)
    assert not absent, f"harden lacks II-8's Usage phrases: {absent}"


def test_harden_nb_limits(skill):
    d = skill(HARDEN)
    absent = d.missing(*LIMITS)
    assert not absent, f"harden lacks II-8's Limits phrases: {absent}"


def test_harden_nb_no_rate_limit_window_item(skill):
    d = skill(HARDEN)
    assert _flatten(LIMIT_GONE) not in d.flat, f"harden still holds {LIMIT_GONE!r}"


def test_implement_limit_arguments(skill):
    d = skill(IMPLEMENT)
    absent = d.missing(LIMITS_PHRASE, DEFAULTS, RECORDING)
    assert not absent, f"implement lacks II-10's limits: {absent}"


def test_implement_limit_refusal(skill):
    d = skill(IMPLEMENT)
    assert not d.missing(REFUSAL), f"implement lacks II-10's refusal: {REFUSAL!r}"


def test_implement_argument_hint(skill):
    d = skill(IMPLEMENT)
    hint = d.frontmatter.get("argument-hint")
    assert hint == ARGUMENT_HINT, f"argument-hint {hint!r} is not II-8's {ARGUMENT_HINT!r}"
