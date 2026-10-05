---
type: regex
target: {source: file, path: specs/004-csv-export/handoff.md}
pattern: 'SHAPE CHECK|Shape check'
match: not_contains
weight: 1
---

Implement never modifies handoff.md: it still has no shape check (only `/s2tdd-harden handoff`
adds one).
