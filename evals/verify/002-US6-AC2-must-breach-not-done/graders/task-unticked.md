---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '^- \[ \] T006 '
match: contains
flags: m
weight: 1
---

T006 (W2's P2a, export.py), whose committed change breaks FR-001, is unticked in tasks.md.
