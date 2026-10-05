---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'converge · at ([0-9a-f]{7,}) · [^\n]*· suite reused \(green at \1\)'
match: contains
weight: 1
---

Converge's verification-log line records that it reused the green run at X: it ends
`· suite reused (green at <sha>)`, the sha the one it ran at (the project's HEAD).
