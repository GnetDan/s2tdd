---
{type: llm, focus: trace, weight: 1}
---

The relay checks its Context's Expect items and resumes at converge (round 2), the run's second
round (rounds count from 1 over the whole run, so it is not a new round 1). Its converger
appends tasks for spec.md's unbuilt US1-AC4 (a field beginning with `=` gets a single quote):
as many as round 1's one task, or more. When the round ends the run stops on the no-shrink
rule, the first stop rule: it records `Round 2: stopped · no shrink (round 1 1, round 2 <k2>)`
under the ledger's Rounds, appends `released by relay 2: stopped: …` to the Lease, and prints
the RUN SUMMARY, which names both rounds' counts (round 1: 1, round 2: <k2>). It never hardens
or implements round 2's tasks, and runs no third converge. If round 2's converge appended no
task, this grader fails: the case's Given did not happen.
