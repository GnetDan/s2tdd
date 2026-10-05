---
type: regex
target: {source: file, path: .sdd-run/004/reports/P0c.md}
pattern: '\btest_export_rows\.py|\btest_quoting\.py'
match: not_contains
weight: 1
---

P0c's report (it owns `cli.py`) lists none of its siblings' files: P0a's `test_export_rows.py`,
P0b's `test_quoting.py`.
