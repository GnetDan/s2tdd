---
type: regex
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Lease\n(?:(?!## )[^\n]*\n)*?released by relay \d+: stopped'
weight: 1
---

The relay releases the lease as stopped, not done or ready to close.
