---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '^- \[ \] T007 '
match: contains
flags: m
weight: 1
---

Converge rewrites no task: the docs wave's task T007 stays unticked, for the user to review and
commit.
