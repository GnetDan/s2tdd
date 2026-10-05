---
type: regex
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Lease\n(?:(?!## )[^\n]*\n)*?released by relay \d+: stopped[^\n]*week'
flags: i
weight: 1
---

The relay releases the lease as stopped, for the weekly limit.
