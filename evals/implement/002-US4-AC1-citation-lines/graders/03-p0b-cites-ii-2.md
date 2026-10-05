---
type: regex
target: {source: file, path: .sdd-run/004/reports/P0b.md}
pattern: 'Cites:[^\n]*contracts/internal-interfaces\.md §II-2\b'
weight: 1
---

P0b's tests assert quote_field's quoting, which wave W1 builds (P1b), although T002 names no
section: its report has a Cites: line naming contracts/internal-interfaces.md §II-2.
