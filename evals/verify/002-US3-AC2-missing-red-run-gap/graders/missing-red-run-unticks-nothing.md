---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '^- \[x\] T003 '
match: contains
flags: m
weight: 1
---

A missing red run, with the wave report showing the check red before dispatch, is a gap that
needs no code change: T003 stays ticked.
