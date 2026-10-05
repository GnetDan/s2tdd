---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'verify-done · waves [^\n]*· Verified(?! with gaps)'
match: not_contains
weight: 1
---

The verification-log line does not record a plain Verified.
