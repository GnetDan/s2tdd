---
type: regex
target: {source: file, path: specs/004-csv-export/orchestration.md}
pattern: '^\| W\d+\b[^|\n]*\|[^|\n]*\|[^|\n]*\|[^|\n]*\btest_notes_export\.py'
flags: m
weight: 1
---

A wave row lists `test_notes_export.py` in its owned-files cell (Wave | Packets | Tasks | Owned
files | ...).
