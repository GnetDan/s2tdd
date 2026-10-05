---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 2: converge at [0-9a-f]+ · \d+ tasks? appended \(T\d+[–-]T\d+\)'
---

Round 2's converge ran and appended tasks: its round line is recorded under Rounds before the
stop rule's line, counted as round 2 of the run, not a new round 1.
