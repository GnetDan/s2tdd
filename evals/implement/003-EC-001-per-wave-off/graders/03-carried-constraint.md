---
type: regex
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Carried constraints\n(?:(?!## )[^\n]*\n)*?[^\n]*Per-wave runs off from wave 1: [^\n]*\S'
weight: 1
---

run-ledger.md's Carried constraints hold `Per-wave runs off from wave 1: <first error line>`.
