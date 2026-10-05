---
type: regex
target: {source: file, path: specs/004-csv-export/orchestration.md}
pattern: '^\| W(\d+)\b[^|\n]*\|[^|\n]*\|[^|\n]*\|[^|\n]*\bquoting\.py\b[^|\n]*\|[\s\S]*^\| W(?!\1\b)\d+\b[^|\n]*\|[^|\n]*\|[^|\n]*\|[^|\n]*\bexport\.py\b'
flags: m
weight: 1
---

In the wave table (Wave | Packets | Tasks | Owned files | ...), the row whose owned files hold
`quoting.py` (the producer of `quote_field`) comes before a row of a different wave whose owned
files hold `export.py` (the consumer). The test files `test_quoting.py` and `test_export_rows.py`
do not count: the pattern needs the bare module names.
