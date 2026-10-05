---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 1: converge at [0-9a-f]+ · \d+ tasks? appended'
---

The converge round appended the task: Rounds records `Round 1: converge at <sha> · <k> tasks
appended (T<a>–T<b>) · cites …`.
