---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Boundary: context [^\n]*(five-hour \d+%|week \d+%)'
match: not_contains
---

No Boundary line carries a window reading.
