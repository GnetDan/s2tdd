---
{type: llm, focus: trace, weight: 1}
---

The relay checks its Context's Expect items and resumes at converge (round 2), the run's second
round. Its converger reports spec.md's US1-AC3 open again (a field holding a carriage return
comes back unquoted, though T009, ticked in round 1, quoted line breaks) and appends a task
citing US1-AC3 or FR-003, IDs that round 1's ticked T008 and T009 cited. When the round ends the
no-shrink rule does not fire (fewer tasks than round 1's four) and the run stops on the
gap-back rule: it records `Round 2: stopped · gap back (<ID>: T<n> now, T<m> in round 1)` under
the ledger's Rounds, naming the gap (the ID) and the round 1 task that closed it before (T008
or T009), appends `released by relay 2: stopped: …` to the Lease, and prints the RUN SUMMARY,
which says the run stopped on gap back and names the gap and that task. It never hardens or
implements round 2's tasks, and runs no third converge. If round 2's converge did not report
US1-AC3 (or FR-003) again, this grader fails: the case's Given did not happen.
