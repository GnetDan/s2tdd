---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'converge · [^\n]*suite reused'
match: not_contains
weight: 1
---

Converge does not record a reused run: the green run is at a commit HEAD has moved past.
