---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Lease\n(?:(?!## )[^\n]*\n)*?released by relay \d+: done\b'
---

The run ends as today's run does: its relay releases the lease `done`, not `ready to close`.
