---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Lease\n(?:(?!## )[^\n]*\n)*?released by relay 1: stopped: harden: [^\n]*\n[^\n#][^\n]*, relay \d+, since '
---

The rerun takes the lease after the stopped run's release, as a new run reading the ledger.
