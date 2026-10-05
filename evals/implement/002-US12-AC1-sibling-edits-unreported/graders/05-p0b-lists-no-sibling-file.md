---
type: regex
target: {source: file, path: .sdd-run/004/reports/P0b.md}
pattern: '\btest_export_rows\.py|\bcli\.py'
match: not_contains
weight: 1
---

P0b's report (it owns `test_quoting.py`) lists none of its siblings' files: P0a's
`test_export_rows.py`, P0c's `cli.py`.
