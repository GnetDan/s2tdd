---
type: tool_used
tool: Bash
input_match: '\bpytest\b(?![^\n]*test_(export_rows|quoting)\.py)'
min: 0
max: 0
weight: 1
---

It ran only the packets' own tests (test_export_rows.py, test_quoting.py), never the full
suite.
