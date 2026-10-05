---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 1: hardened · W\d+'
---

The hardener's report is recorded under Rounds: `Round 1: hardened · W<x>–W<y>`.
