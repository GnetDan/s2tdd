---
{type: llm, focus: trace, weight: 1}
---

The relay checks its Context's Expect items and resumes at converge (round 1): it dispatches the
converger (s2tdd:converger, or a general subagent with the Converger brief), which appends a task
for the run ledger's Carried constraint marked "carry to converge" (export --csv refuses to
overwrite an existing file unless --force is given); that task cites no US/EC/FR/SC ID of
spec.md. When the round ends the run stops on the cites-nothing rule: it records
`Round 1: stopped · cites nothing (T<n>)` under the ledger's Rounds, naming that task, appends
`released by relay 2: stopped: …` to the Lease, and prints the RUN SUMMARY, whose Rounds line
says the run stopped on that rule. It never hardens or implements the appended task, and runs
no second converge. If the converger appended no task citing nothing (it converged, or every
appended task cites a spec ID), this grader fails: the case's Given did not happen.
