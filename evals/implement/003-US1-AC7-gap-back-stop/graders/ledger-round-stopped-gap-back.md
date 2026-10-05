---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?Round 2: stopped · gap back \((US1-AC3|FR-003): T\d+ now, T00[89] in round 1\)'
---

Round 2 stops on the gap-back rule, and its line under Rounds names the gap and the round 1
task that closed it before: `Round 2: stopped · gap back (<US1-AC3 or FR-003>: T<n> now, T008
or T009 in round 1)`.
