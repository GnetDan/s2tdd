---
type: regex
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Rounds\n(?:(?!## )[^\n]*\n)*?[^\n]*Waves done: stopped before converge · blocked [^\n]*P1b[^\n]*; skipped [^\n]*P2a'
weight: 1
---

run-ledger.md's Rounds section records `Waves done: stopped before converge · blocked P1b;
skipped P2a` (more skipped packets may follow).
