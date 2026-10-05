---
type: llm
focus: {source: file, path: .sdd-run/004/reports/P0a.md}
weight: 1
---

This is test packet P0a's report (T001, `test_export_rows.py`). Its tests assert export_csv's
shape (the header row, one row per note, rows ending in LF), which a later wave builds, and
contracts/internal-interfaces.md §II-1 states it. Pass if the report has one `Cites:` line per
shape its tests assert, each in the form `Cites: <test id> asserts <shape name> →
contracts/<file> §<section>` and naming §II-1 of contracts/internal-interfaces.md. Fail if a
shape the tests assert has no such line, or a line names no contract file and section.
