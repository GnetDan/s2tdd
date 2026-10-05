---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 1: converge at [0-9a-f]+ · \d+ tasks? appended \(T\d+[–-]T\d+\)'
---

Round 1's converge ran and appended tasks: its round line is recorded under Rounds before the
stop rule's line.
