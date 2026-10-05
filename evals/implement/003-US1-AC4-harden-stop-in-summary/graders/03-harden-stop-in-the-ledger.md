---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 1: stopped · harden: [^\n]*assign scenario IDs first'
---

The hardener's stop is recorded under Rounds with harden's own stop message:
`Round 1: stopped · harden: assign scenario IDs first …`.
