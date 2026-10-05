---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '^- \[x\] T004 [\s\S]*^- \[x\] T005 '
match: contains
flags: m
weight: 1
---

A missing Boundary: line needs no code change: W1's tasks T004 and T005 stay ticked.
