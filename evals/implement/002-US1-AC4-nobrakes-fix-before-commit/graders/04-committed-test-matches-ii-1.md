---
type: llm
focus: {source: file, path: test_export_rows.py}
weight: 1
---

The test file asserts that `export_csv`'s rows end with LF (`\n`), as contracts/internal-interfaces.md
§II-1 says. It does not assert CRLF (`\r\n`) row ends.
