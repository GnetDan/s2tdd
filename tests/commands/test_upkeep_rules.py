"""T049: the suite-time budget and test-upkeep rules (II-12) across five commands.

Pins II-12's literals and the task's listed phrases through `Doc.missing` (II-5): nothing
beyond them. Test names carry the command so each implementation task selects its cases
with `-k` (verify_done, converge, next, foundation_review, close).
"""

from __future__ import annotations

# II-12: how the budget is stated and where it is read from.
STATED = "Suite-time budget: <N> minutes"
GUIDANCE_FILES = ("CLAUDE.md", "AGENTS.md")

# II-12: the suffix of the verification-log line (a leading ' · suite ' in the log).
SUFFIX_WITH_BUDGET = "suite <M>m<SS>s (budget <N>m)"
SUFFIX_OVER = "suite <M>m<SS>s (budget <N>m, over)"
SUFFIX_NO_BUDGET = "suite <M>m<SS>s (no budget)"

# II-12: what next surfaces, and the task converge appends when over budget.
OVER_BUDGET_LINE = "Suite over budget: <M>m<SS>s against <N>m (<date>, <command>)."
UPKEEP_TASK = (
    "- [ ] T<n> Test upkeep: bring the suite under its <N>-minute budget "
    "(last run <M>m<SS>s); see specs/WORKFLOW.md#test-upkeep"
)

BUDGET_READERS = ("s2tdd-verify-done", "s2tdd-converge")


def _assert_has(d, *phrases):
    assert not d.missing(*phrases), d.missing(*phrases)


# verify-done ---------------------------------------------------------------------------


def test_verify_done_reads_the_stated_budget(skill):
    _assert_has(skill("s2tdd-verify-done"), STATED, *GUIDANCE_FILES)


def test_verify_done_records_wall_time_suffix(skill):
    _assert_has(
        skill("s2tdd-verify-done"),
        SUFFIX_WITH_BUDGET,
        SUFFIX_OVER,
        "wall time",
    )


def test_verify_done_records_no_budget(skill):
    _assert_has(skill("s2tdd-verify-done"), SUFFIX_NO_BUDGET)


# converge ------------------------------------------------------------------------------


def test_converge_reads_the_stated_budget(skill):
    _assert_has(skill("s2tdd-converge"), STATED, *GUIDANCE_FILES)


def test_converge_records_wall_time_suffix(skill):
    _assert_has(
        skill("s2tdd-converge"),
        SUFFIX_WITH_BUDGET,
        SUFFIX_OVER,
        "wall time",
    )


def test_converge_records_no_budget(skill):
    _assert_has(skill("s2tdd-converge"), SUFFIX_NO_BUDGET)


def test_converge_appends_the_upkeep_task_when_over_budget(skill):
    _assert_has(skill("s2tdd-converge"), UPKEEP_TASK)


def test_converge_never_refuses_for_the_budget(skill):
    _assert_has(skill("s2tdd-converge"), "never refuses")


# next ----------------------------------------------------------------------------------


def test_next_shows_the_over_budget_line(skill):
    _assert_has(skill("s2tdd-next"), OVER_BUDGET_LINE, "Watch out")


def test_next_reads_the_newest_suite_record(skill):
    _assert_has(skill("s2tdd-next"), " · suite ", "over")


# foundation-review and close -------------------------------------------------------------


def test_foundation_review_lists_duplicate_and_obsolete_tests(skill):
    _assert_has(skill("s2tdd-foundation-review"), "duplicate", "obsolete", "findings")


def test_foundation_review_removes_or_skips_no_test(skill):
    _assert_has(skill("s2tdd-foundation-review"), "removed or skipped")


def test_close_lists_duplicate_and_obsolete_tests(skill):
    _assert_has(skill("s2tdd-close"), "duplicate", "obsolete", "findings")


def test_close_removes_or_skips_no_test(skill):
    _assert_has(skill("s2tdd-close"), "removed or skipped")
