---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '## Phase \d+: Convergence[\s\S]*\n- \[ \] T\d+ [^\n]*(write_csv\(None\)|requires? --csv|--csv is required|without --csv)'
match: not_contains
flags: i
weight: 1
---

The review note W0 · P0c (export without --csv called write_csv(None)), resolved by a later
commit, gets no task.
