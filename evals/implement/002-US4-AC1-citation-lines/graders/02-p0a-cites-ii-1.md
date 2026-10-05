---
type: regex
target: {source: file, path: .sdd-run/004/reports/P0a.md}
pattern: 'Cites:[^\n]*contracts/internal-interfaces\.md §II-1\b'
weight: 1
---

P0a's tests assert export_csv's header and rows, which wave W1 builds: its report has a Cites:
line naming contracts/internal-interfaces.md §II-1. The line may be indented.
