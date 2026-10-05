---
type: regex
target: {source: file, path: specs/004-csv-export/handoff.md}
pattern: '/speckit-[a-z]'
match: not_contains
weight: 1
---

handoff.md names no old command, by the same pattern.
