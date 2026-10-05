---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'verify-done · waves [^\n]*· (Verified with gaps|Not done)'
match: contains
weight: 1
---

The verification-log line records Verified with gaps or Not done, never a plain Verified.
