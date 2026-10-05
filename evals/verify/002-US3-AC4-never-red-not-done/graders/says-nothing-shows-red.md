---
type: llm
focus: trace
weight: 1
---

verify-done says that nothing shows test_quoting.py red before quoting.py was written: not P1b's
report, not its test packet P0b's report, and neither W0's nor W1's wave report (their Red runs
lines name only test_export_rows.py and P0c's check). The case grades the reports' evidence, as
the skill does: verify-done's own re-run of the test at an earlier commit is not a report that
shows it red, and does not turn T005's Not done into a gap.
