"""PR #8 review fixes for converge and the converger (C-4, C-5, C-6, C-7).

C-4: a converger retried or resumed after its round's converge already appended tasks hands
back that outcome instead of rerunning converge into its own unticked-task guard. C-5: the
docs-wave set-aside holds only in a nobrakes run. C-6: a reused suite time appends no
test-upkeep task, and the reused suffix keeps the budget comparison. C-7: converge writes and
reports user-story scenario IDs in one form, US<n>-AC<m>. Assertion style per II-0: flattened
phrases, asserted present and in order; the pinned sentences they extend stay.
"""

from __future__ import annotations

CONVERGE = "s2tdd-converge"
CONVERGER_AGENT = "agents/converger.md"

# C-5
G1_KEPT = (  # II-9 G1, tests/commands/test_docs_wave_checkpoint.py
    "whether the ledger records it built or not; list them in the summary as docs wave (pending)."
)
C5 = (
    "Set the docs wave aside only in a nobrakes run: run-ledger.md records one (a Runs line naming "
    "nobrakes) or a Docs wave <n> built, uncommitted line; otherwise the docs wave's tasks count "
    "as unticked like any other."
)

# C-6
G3_KEPT = "and the budget comparison uses that line's wall time."  # test_full_runs.py G3
G4_KEPT = "When the suite was reused, the suffix is · suite reused (green at <sha>) instead."
C6_TASK = (
    "A reused run appends no test-upkeep task: its wall time is the full suite's, not this "
    "converge's acceptance run, so the task comes only from a run this converge timed and "
    "whether reuse fired never changes the task list."
)
C6_SUFFIX = (
    "When the guidance file states a budget, the reused suffix carries the comparison inside its "
    "parentheses: · suite reused (green at <sha>; <M>m<SS>s, budget <N>m), or · suite reused "
    "(green at <sha>; <M>m<SS>s, budget <N>m, over) when that time exceeds it."
)
UPKEEP_HEADING = "When the suite is over budget"

# C-7
C7_FORM = (
    "A user-story scenario is cited in the spec's ID form, US<n>-AC<m> (e.g. US1-AC2), in the "
    "intent inventory, in task source-refs and in the report."
)
C7_NORMALIZE = (
    "A task an earlier round wrote with US<n>/AC<m> is reported as US<n>-AC<m>, never as none."
)
OLD_FORM = "us1/ac2"

# C-4
GUARD_STOP_KEPT = (
    "task(s) in tasks.md are unticked; finish implementing (and verify) them before converging."
)
C4_GUARD = (
    "When those unticked tasks are exactly the newest Convergence phase's and the newest "
    "verification-log line is a converge line at this HEAD reporting them appended, add: "
    '"Converge at <sha> appended T<a>–T<b>; harden them (/s2tdd-harden) and implement them."'
)
CONVERGER_KEPT = "If it still stops on unticked tasks, hand back that stop verbatim."
C4_AGENT = (
    "Before running it, read validation.md's Verification log: when its newest line is a "
    "converge line at this HEAD (git rev-parse --short HEAD) that ends <k> tasks appended "
    "(T<a>–T<b>) and those tasks are still unticked, an earlier attempt of this round already "
    "appended them. Do not rerun converge: hand back that outcome, one line per task from "
    "tasks.md, that log line and its suite part."
)


def _flatten(s: str) -> str:
    return " ".join(s.lower().replace("`", "").replace("*", "").split())


def _at(d, phrase: str) -> int:
    return d.flat.index(_flatten(phrase))


def test_c5_docs_wave_set_aside_only_in_a_nobrakes_run(skill):
    d = skill(CONVERGE)
    assert not d.missing(G1_KEPT, C5), d.missing(G1_KEPT, C5)
    assert _at(d, G1_KEPT) < _at(d, C5) < _at(d, GUARD_STOP_KEPT), "C-5 follows G1, before the stop"


def test_c6_reused_run_appends_no_upkeep_task(skill):
    d = skill(CONVERGE)
    assert not d.missing(G3_KEPT, UPKEEP_HEADING, C6_TASK), d.missing(
        G3_KEPT, UPKEEP_HEADING, C6_TASK
    )
    assert _at(d, UPKEEP_HEADING) < _at(d, C6_TASK), "C-6 sits in step 7's upkeep item"


def test_c6_reused_suffix_keeps_the_budget(skill):
    d = skill(CONVERGE)
    assert not d.missing(G4_KEPT, C6_SUFFIX), d.missing(G4_KEPT, C6_SUFFIX)
    assert _at(d, G4_KEPT) < _at(d, C6_SUFFIX), "C-6's suffix follows G4"


def test_c7_one_scenario_id_form(skill):
    d = skill(CONVERGE)
    assert not d.missing(C7_FORM, C7_NORMALIZE), d.missing(C7_FORM, C7_NORMALIZE)
    assert OLD_FORM not in d.flat, "converge still gives US1/AC2 as an example"


def test_c4_guard_names_an_earlier_append(skill):
    d = skill(CONVERGE)
    assert not d.missing(GUARD_STOP_KEPT, C4_GUARD), d.missing(GUARD_STOP_KEPT, C4_GUARD)
    assert _at(d, GUARD_STOP_KEPT) < _at(d, C4_GUARD), "C-4's note follows the stop message"


def test_c4_converger_hands_back_an_earlier_append(doc):
    d = doc(CONVERGER_AGENT)
    assert not d.missing(CONVERGER_KEPT, C4_AGENT), d.missing(CONVERGER_KEPT, C4_AGENT)
    assert _at(d, C4_AGENT) < _at(d, CONVERGER_KEPT), "the check comes before the run"
