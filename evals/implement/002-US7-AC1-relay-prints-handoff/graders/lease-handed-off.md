---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Lease\n(?:(?!## )[^\n]*\n)*?[^\n]*handed off by relay \d+'
---

The relay handed off: its line in run-ledger.md's Lease is `handed off by relay <n>`.
