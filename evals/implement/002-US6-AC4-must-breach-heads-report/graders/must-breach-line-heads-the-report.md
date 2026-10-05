---
{type: llm, focus: trace, weight: 1}
---

Wave 0's shape check returned a finding that cites a spec MUST (`MUST FR-002`: test_quoting.py
asserts that a field holding a line break comes back unquoted; the scaffold seeds it). The wave
report written for wave 0, in s1-wave-reports.md and as the orchestrator printed it, begins with
`MUST breach: fix before the next wave · <finding line>` naming that finding, before its
`Wave:` line; the finding is not only a recommendation on the Review line. If no finding in the
run cites a spec MUST, this grader fails: the case's Given did not happen.
