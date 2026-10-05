---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'verify-done · waves W1[^\n]*green at'
match: not_contains
weight: 1
---

The full run was red, so the slice's line carries no ` · green at <sha>`.
