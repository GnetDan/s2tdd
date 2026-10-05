---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Lease\n(?:(?!## )[^\n]*\n)*?released by relay \d+: stopped'
---

The run stops: its relay releases the lease `stopped: <reason>`, not `done` or `ready to
close`.
