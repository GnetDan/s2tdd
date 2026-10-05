---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'converge · at [0-9a-f]+ · \d+ tasks? appended'
match: contains
weight: 1
---

Converge records the tasks_appended outcome in validation.md's verification log.
