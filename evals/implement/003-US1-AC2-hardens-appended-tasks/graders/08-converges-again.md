---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 2: converge at [0-9a-f]+ · '
---

After the new waves, the run converges again: Rounds records round 2's converge line.
