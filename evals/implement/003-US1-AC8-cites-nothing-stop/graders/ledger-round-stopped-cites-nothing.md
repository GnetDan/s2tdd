---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 1: stopped · cites nothing \(T\d+\)'
---

Round 1 stops on the cites-nothing rule, and its line under Rounds names the task:
`Round 1: stopped · cites nothing (T<n>)`.
