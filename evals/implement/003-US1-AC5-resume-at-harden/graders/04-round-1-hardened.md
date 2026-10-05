---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 1: stopped · harden: [^\n]*\n(?:(?!## )[^\n]*\n)*?Round 1: hardened · W\d+'
---

The ledger shows the resume: after `Round 1: stopped · harden: …`, Rounds records
`Round 1: hardened · W<x>–W<y>` for the same round.
