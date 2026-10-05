---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: 'Round 2: stopped · no shrink'
match: not_contains
---

The run does not stop on the no-shrink rule: round 2 appended fewer tasks than round 1.
