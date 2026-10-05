---
type: llm
focus: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
weight: 1
---

W0's wave report carries the shape check's finding that P0a's test (`test_export_rows.py`)
asserts CRLF row ends while contracts/internal-interfaces.md §II-1 says LF, and it carries it as
a recommendation (for the user to act on), in or beside its Review line. It does not say the
wave was blocked, held back, or that the test was fixed before the commit.
