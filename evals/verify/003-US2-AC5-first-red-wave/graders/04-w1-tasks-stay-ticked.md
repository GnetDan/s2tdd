---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '\n- \[x\] T004 [^\n]*\n- \[x\] T005 '
match: contains
weight: 1
---

The test is green alone at W1's commit, so W1's tasks T004 and T005 stay ticked: only the first
red wave's tasks are unticked.
