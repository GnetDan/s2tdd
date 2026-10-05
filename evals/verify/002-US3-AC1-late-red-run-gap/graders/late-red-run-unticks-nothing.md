---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '^- \[x\] T005 '
match: contains
flags: m
weight: 1
---

A late red run, with the wave report showing the test red before dispatch, is a gap that needs
no code change: T005 stays ticked.
