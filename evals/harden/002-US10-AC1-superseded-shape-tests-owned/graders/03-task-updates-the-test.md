---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '^- \[ \] T\d+\w* [^\n]*\btest_notes_export\.py'
flags: m
weight: 1
---

tasks.md has an unticked task that names `test_notes_export.py`: the task that updates it to
the widened header.
