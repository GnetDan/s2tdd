---
{type: llm, focus: trace, weight: 1}
---

The relay checks its Context's Expect items and resumes at converge (round 1): it dispatches the
converger, which appends tasks for spec.md's unbuilt US1-AC3 (a field holding a line break is
quoted), and records the round line under the ledger's Rounds. At the phase change after that
round it finds .sdd-run/004/BRAKES and hands off instead of hardening: the Lease gains
`handed off by relay 2 (brakes)`, the ledger's Handoff section and .sdd-run/004/handoff-3.md
hold the handoff prompt, and the specs repository is committed as `004: relay 2 handoff`. The
prompt it prints names the next phase, the harden of the appended tasks: its first line is
`/s2tdd-implement --nobrakes` with no scope, its Expect names round 1's converge line as the
newest Rounds line, and it ends `RESUME AT: harden (round 1)`, so the next relay starts at the
harden step, not at a wave or a second converge. The relay neither hardens nor implements the
appended tasks and starts no next relay itself. If round 1's converge appended no task, this
grader fails: the case's Given did not happen.
