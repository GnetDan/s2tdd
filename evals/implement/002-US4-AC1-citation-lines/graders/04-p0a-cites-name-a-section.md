---
type: regex
target: {source: file, path: .sdd-run/004/reports/P0a.md}
pattern: 'Cites:(?![^\n]*contracts/[\w./-]+\.md §II-\d)[^\n]*'
match: not_contains
weight: 1
---

Every Cites: line in P0a's report names a contract file and a section.
