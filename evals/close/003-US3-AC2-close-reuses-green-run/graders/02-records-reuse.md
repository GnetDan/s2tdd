---
type: regex
target: {source: file, path: specs/004-csv-export/close-out.md}
pattern: 'Suite\**:?\**\s*reused green run at `?[0-9a-f]{7,}`?\s*\(2026-10-03 verify-done\)'
match: contains
weight: 1
---

The close-out header records that close reused the green run at X:
`Suite: reused green run at <sha> (2026-10-03 verify-done)`.
