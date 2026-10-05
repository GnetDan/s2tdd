---
type: regex
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 1: converge at [0-9a-f]{7,40} · '
weight: 1
---

The loop ran its first converge round and recorded it under Rounds.
