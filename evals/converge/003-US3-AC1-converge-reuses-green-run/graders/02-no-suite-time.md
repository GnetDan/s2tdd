---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'converge · [^\n]*· suite \d+m\d+s'
match: not_contains
weight: 1
---

Converge's line carries no measured suite time: no suite ran.
