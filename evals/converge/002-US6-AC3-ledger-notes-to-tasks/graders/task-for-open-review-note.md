---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '## Phase \d+: Convergence[\s\S]*\n- \[ \] T\d+ [^\n]*(keyerror|missing[^\n]*(key|title)|(key|title)[^\n]*missing|without (a |an |the )?(title|key)|no title)'
match: contains
flags: i
weight: 1
---

The open review note W1 · P1a (a note with no title key raises KeyError and stops the export)
becomes a task in the Convergence phase.
