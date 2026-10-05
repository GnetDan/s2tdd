---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 2: converge at [0-9a-f]+ · [1-3] tasks? appended \(T\d+[–-]T\d+\)'
---

Round 2's converge ran and appended fewer tasks than round 1's four (so the no-shrink rule,
which comes first, does not fire): its round line is under Rounds before the stop rule's line.
