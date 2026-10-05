---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 2: stopped · no shrink \(round 1 1, round 2 [1-9]\d*\)'
---

Round 2 stops on the no-shrink rule, and its line under Rounds names both rounds' counts:
`Round 2: stopped · no shrink (round 1 1, round 2 <k2>)`.
