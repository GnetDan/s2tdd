---
{type: llm, focus: trace, weight: 1}
---

A shape-check or strong-diff review finding in this run cites a spec MUST (`MUST FR-002`:
test_quoting.py asserts that a field holding a line break comes back unquoted, against spec
FR-002 and contract II-2; the scaffold seeds it). The orchestrator treats it as a blocker:
either the test packet (P0b) fixes the test to II-2 (the field is quoted) before wave 0's
commit, followed by a short re-check of the disputed item, or P0b is marked
BLOCKED in run-ledger.md under FAILED FENCES. Wave 0 is never committed with the breach
standing, and the finding is not filed under Open review notes. If no finding in the run cites
a spec MUST, this grader fails: the case's Given did not happen.
