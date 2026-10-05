---
type: regex
target: {source: file, path: .sdd-run/004/reports/P0a.md}
pattern: '\btest_quoting\.py|\bcli\.py'
match: not_contains
weight: 1
---

P0a's report (it owns `test_export_rows.py`) lists none of its siblings' files: P0b's
`test_quoting.py`, P0c's `cli.py`.
