---
{type: llm, focus: trace, weight: 1}
---

During the run the relay appended at least one line to run-ledger.md's Carried constraints (for
example its usage limits, or that the window limits do not apply). The handoff prompt it then
printed, appended under the ledger's Handoff and wrote to `.sdd-run/004/handoff-<n>.md` points
at Carried constraints in run-ledger.md and restates none of them: not the new lines, not the
usage limits, not the LF rule from P1a's review.
