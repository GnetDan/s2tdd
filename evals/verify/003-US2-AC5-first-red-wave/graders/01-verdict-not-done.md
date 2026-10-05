---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'verify-done · waves W1[–-]W2 [^\n]*· Not done \(unticked T006\)'
match: contains
weight: 1
---

The verification-log line for the slice W1–W2 records Not done and unticks W2's task alone:
`Not done (unticked T006)`.
