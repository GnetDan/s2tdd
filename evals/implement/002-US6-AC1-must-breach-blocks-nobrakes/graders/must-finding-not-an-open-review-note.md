---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Open review notes\n(?:(?!## )[^\n]*\n)*?[^\n]*MUST (FR-\d+|US\d+-AC\d+|EC-\d+)'
match: not_contains
---

No line under run-ledger.md's Open review notes cites a spec MUST.
