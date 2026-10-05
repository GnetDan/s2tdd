"""T001: the per-wave shape check (US1; II-1, II-2, II-3, II-5, II-7, II-9, II-10).

Harden's handoff prompt gains a `SHAPE CHECK` section after `TIER` and before `CHECKPOINT ROWS`,
its TIER rewrite, the `Review:` line's shape-check slot, a `### Shape check` standard brief and
the shape check's share of the context budget; implement dispatches the shape check and says
once when an older handoff predates it; the strong-diff reviewer agent carries both briefs.
Every phrase is transcribed from contracts/internal-interfaces.md (002). These fail until T002,
T003 and T004.
"""

from __future__ import annotations

HARDEN = "s2tdd-harden"
IMPLEMENT = "s2tdd-implement"
REVIEWER_AGENT = "agents/strong-diff-reviewer.md"

# II-2, phrases 1-7: the SHAPE CHECK section of harden's prompt.
SHAPE_CHECK_HEAD = "SHAPE CHECK (both modes; every wave that holds a test packet)"
SHAPE_CHECK_PHRASES = (
    "one shape check per wave that holds test packets, after the wave's test packets have "
    "reported and you have confirmed their reds",
    "dispatch it as s2tdd:strong-diff-reviewer with the Shape check brief",
    "it reads every test packet's test diff in the wave, the Cites: lines in their reports and "
    "the contract sections they cite, with the packets' Decision lines",
    "With MODE: nobrakes, send its blockers and disputed citations back to the test packet's own "
    "agent, then a short re-check of the disputed items, before the wave commit; what it does not "
    "confirm goes under Open review notes.",
    "With MODE: attended, it is report-only: its findings go into the wave report's Review line "
    "as recommendations and block neither the commit nor the next wave.",
    "A wave with no test packet gets no shape check (shape check: none).",
)

# Section markers of harden's prompt template, flattened (the first occurrence of each).
TIER_MARK = "- TIER:"
CHECKPOINT_ROWS_MARK = "- CHECKPOINT ROWS:"
NOBRAKES_MARK = "NOBRAKES (only when MODE is nobrakes"
REPORT_MARK = "REPORT AFTER EVERY WAVE, in this format, no code"
BUDGET_MARK = "Context budget note"
BUDGET_END_MARK = "B5. Cross-link"

# II-3: TIER (the escalation phrase is T055's, not here).
TIER_PHRASES = (
    "tiers differ by effort on one model: the agent types set each tier's model and effort",
    "the diff review is the strong packets' in --nobrakes; every wave that holds test packets "
    "gets the shape check, in both modes",
    "and say that each packet runs at this session's effort; tiers then become fence strictness",
)
TIER_KEPT = "s2tdd:packet-<tier>"
TIER_GONE = (
    "with a single model for everything, tiers collapse into fence strictness",
    "tiers become fence strictness when one model does everything",
)

# II-5: the wave report's Review line, slots included.
REVIEW_LINE = (
    "Review: <packet>: <verdict>; …; shape check: <verdict> (<k> citations, <m> differ) | none"
)

# II-7: the Shape check standard brief.
SHAPE_BRIEF_HEADING = "### Shape check"
STRONG_DIFF_HEADING = "### Strong-diff reviewer (read-only)"
TEST_OWNER_HEADING = "### Test-owner fix"
SHAPE_BRIEF_PHRASES = (
    "Review wave <n>'s test packets <P…> before the wave commit.",
    "Edit nothing; run only the packets' own tests, never the full suite.",
    "Read: each packet's test diff (git diff -- <test files>), the Cites: lines in its report "
    "(<report paths>), each cited contract section, and <guidance file>'s invariants.",
    "For each citation: matches, or differs: <what the test asserts> vs <what the section says>.",
    "For each shape a test asserts that another packet or wave builds, with no citation: a "
    "finding.",
)
FINDING_LINE = (
    "<blocker|should|note>[ · MUST <FR-nnn|US<n>-AC<m>|EC-nnn>] · <file:line> · "
    "<failure scenario>"
)
VERDICT_LINE = "Verdict: Accept | Accept with fixes | Reject. At most 250 words."

# II-9: the context budget note.
BUDGET_PHRASES = (
    "about 15k tokens per packet when nothing better is measured",
    "plus one shape-check hand-back (about 1k tokens) per wave that holds test packets",
)

# II-10: implement.
IMPLEMENT_DISPATCH = (
    "each wave's shape check → s2tdd:strong-diff-reviewer with the Shape check brief, "
    "in both modes"
)
OLDER_HANDOFF = (
    "handoff.md predates the shape check: its rules run as written; /s2tdd-harden handoff "
    "refreshes it."
)
IMPLEMENT_DESCRIPTION_PHRASE = "shape check"

# II-1: the strong-diff reviewer agent.
REVIEWER_DESCRIPTION = (
    "Reads one packet's diff, or one wave's test packets against the contract sections they cite "
    "(the shape check), read-only before the wave commit, and returns a verdict; strong tier."
)
REVIEWER_BRIEF_LINE = "Your dispatch names your brief: Strong-diff reviewer or Shape check."


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _at(flat: str, phrase: str, where: str) -> int:
    """The index of the phrase's first occurrence in the flattened text; fail when absent."""
    i = flat.find(_flatten(phrase))
    assert i >= 0, f"`{phrase}` missing from {where}"
    return i


def _missing_in(text: str, phrases: tuple[str, ...]) -> list[str]:
    flat = _flatten(text)
    return [p for p in phrases if _flatten(p) not in flat]


def _heading_line(body: str, heading: str) -> int:
    lines = [line.rstrip() for line in body.split("\n")]
    assert heading in lines, f"heading `{heading}` missing from {HARDEN}"
    return lines.index(heading)


# --- harden: SHAPE CHECK (II-2 1-7) ---------------------------------------------------------


def test_harden_shape_check_section_after_tier_before_checkpoint_rows(skill):
    d = skill(HARDEN)
    where = f"skills/{HARDEN}/SKILL.md"
    head = _at(d.flat, SHAPE_CHECK_HEAD, where)
    tier = _at(d.flat, TIER_MARK, where)
    rows = _at(d.flat, CHECKPOINT_ROWS_MARK, where)
    nobrakes = _at(d.flat, NOBRAKES_MARK, where)
    assert tier < head < rows, (
        "the SHAPE CHECK section is not after TIER and before CHECKPOINT ROWS"
    )
    assert head < nobrakes and rows < nobrakes, "the SHAPE CHECK section is inside NOBRAKES"
    section = d.flat[head:rows]
    missing = _missing_in(section, SHAPE_CHECK_PHRASES)
    assert not missing, f"missing from harden's SHAPE CHECK section: {missing}"


# --- harden: TIER (II-3) --------------------------------------------------------------------


def test_harden_tier_differs_by_effort_and_keeps_the_agent_types(skill):
    d = skill(HARDEN)
    missing = d.missing(*TIER_PHRASES, TIER_KEPT)
    assert not missing, f"missing from {HARDEN}: {missing}"


def test_harden_lacks_the_removed_fence_strictness_sentences(skill):
    d = skill(HARDEN)
    present = [p for p in TIER_GONE if _flatten(p) in d.flat]
    assert not present, f"still in {HARDEN}: {present}"


# --- harden: the Review line (II-5) ---------------------------------------------------------


def test_harden_report_format_has_the_review_line_with_the_shape_check(skill):
    d = skill(HARDEN)
    where = f"skills/{HARDEN}/SKILL.md"
    report = _at(d.flat, REPORT_MARK, where)
    nobrakes = _at(d.flat, NOBRAKES_MARK, where)
    missing = _missing_in(d.flat[report:nobrakes], (REVIEW_LINE,))
    assert not missing, f"missing from {HARDEN}'s REPORT AFTER EVERY WAVE format: {missing}"


# --- harden: the Shape check brief (II-7) ---------------------------------------------------


def test_harden_shape_check_brief_between_strong_diff_and_test_owner_fix(skill):
    d = skill(HARDEN)
    shape = _heading_line(d.body, SHAPE_BRIEF_HEADING)
    strong = _heading_line(d.body, STRONG_DIFF_HEADING)
    owner = _heading_line(d.body, TEST_OWNER_HEADING)
    assert strong < shape < owner, (
        f"`{SHAPE_BRIEF_HEADING}` is not between `{STRONG_DIFF_HEADING}` and `{TEST_OWNER_HEADING}`"
    )


def test_harden_shape_check_brief_phrases_and_finding_line(skill):
    d = skill(HARDEN)
    shape = _heading_line(d.body, SHAPE_BRIEF_HEADING)
    owner = _heading_line(d.body, TEST_OWNER_HEADING)
    brief = "\n".join(d.body.split("\n")[shape:owner])
    missing = _missing_in(brief, (*SHAPE_BRIEF_PHRASES, FINDING_LINE, VERDICT_LINE))
    assert not missing, f"missing from harden's Shape check brief: {missing}"
    flat = _flatten(brief)
    assert flat.find(_flatten(FINDING_LINE)) < flat.find(_flatten(VERDICT_LINE)), (
        "the Shape check brief's finding line does not come before its Verdict line"
    )


# --- harden: context budget (II-9) ----------------------------------------------------------


def test_harden_context_budget_note_counts_the_shape_check(skill):
    d = skill(HARDEN)
    where = f"skills/{HARDEN}/SKILL.md"
    start = _at(d.flat, BUDGET_MARK, where)
    end = _at(d.flat, BUDGET_END_MARK, where)
    missing = _missing_in(d.flat[start:end], BUDGET_PHRASES)
    assert not missing, f"missing from harden's Context budget note: {missing}"


# --- implement (II-10) ----------------------------------------------------------------------


def test_implement_dispatches_the_shape_check_in_both_modes(skill):
    d = skill(IMPLEMENT)
    missing = d.missing(IMPLEMENT_DISPATCH)
    assert not missing, f"missing from {IMPLEMENT}: {missing}"


def test_implement_says_an_older_handoff_predates_the_shape_check(skill):
    d = skill(IMPLEMENT)
    missing = d.missing(OLDER_HANDOFF)
    assert not missing, f"missing from {IMPLEMENT}: {missing}"


def test_implement_description_names_the_shape_check(skill):
    d = skill(IMPLEMENT)
    description = _flatten(str(d.frontmatter.get("description", "")))
    assert IMPLEMENT_DESCRIPTION_PHRASE in description, (
        f"{IMPLEMENT}'s description lacks `{IMPLEMENT_DESCRIPTION_PHRASE}`"
    )


# --- agents (II-1) --------------------------------------------------------------------------


def test_agents_strong_diff_reviewer_description_names_the_shape_check(doc):
    d = doc(REVIEWER_AGENT)
    description = " ".join(str(d.frontmatter.get("description", "")).split())
    assert description == REVIEWER_DESCRIPTION, (
        f"{REVIEWER_AGENT}'s description is `{description}`, not II-1's"
    )


def test_agents_strong_diff_reviewer_body_names_both_briefs(doc):
    d = doc(REVIEWER_AGENT)
    missing = d.missing(REVIEWER_BRIEF_LINE)
    assert not missing, f"missing from {REVIEWER_AGENT}: {missing}"
