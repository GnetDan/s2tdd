---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Carried constraints\n(?:(?!## )[^\n]*\n)*?[^\n]*(do(?:n''t| not) apply|not[ _]applicable|no usage tool)'
flags: i
---

run-ledger.md's Carried constraints record that the window limits do not apply.
