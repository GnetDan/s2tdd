---
type: llm
focus: {source: file, path: .sdd-run/004/reports/P0b.md}
weight: 1
---

This is test packet P0b's report (T002, `test_quoting.py`). Its tests assert quote_field's
quoting, which wave W1 builds (P1b) and contracts/internal-interfaces.md §II-2 states, though
T002 names no section. Pass if the report has one `Cites:` line per shape its tests assert,
each in the form `Cites: <test id> asserts <shape name> → contracts/<file> §<section>` and
naming §II-2 of contracts/internal-interfaces.md. Fail if a shape the tests assert has no such
line, or a line names no contract file and section.
