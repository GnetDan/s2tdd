---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'converge · at [0-9a-f]+ · (converged|\d+ tasks? appended)'
match: contains
weight: 1
---

Converge does not refuse: it records its outcome in validation.md's verification log, although
the docs wave's task T007 is unticked.
