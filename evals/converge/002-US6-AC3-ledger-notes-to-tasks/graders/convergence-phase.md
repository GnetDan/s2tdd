---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '^## Phase \d+: Convergence'
match: contains
flags: m
weight: 1
---

Converge appends a Convergence phase to tasks.md.
