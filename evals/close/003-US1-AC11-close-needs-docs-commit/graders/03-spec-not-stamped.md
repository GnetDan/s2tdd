---
type: regex
target: {source: file, path: specs/004-csv-export/spec.md}
pattern: 'Status\**:\**\s*Closed'
match: not_contains
weight: 1
---

spec.md is not stamped Closed.
