---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '\n- \[x\] T006 [^\n]*\n[\s\S]*\n- \[x\] T007 Document'
match: contains
weight: 1
---

Converge rewrites no existing task: T006 and T007 stay as they were, ticked.
