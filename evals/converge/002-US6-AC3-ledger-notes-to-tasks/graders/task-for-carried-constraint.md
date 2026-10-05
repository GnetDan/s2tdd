---
type: regex
target: {source: file, path: specs/004-csv-export/tasks.md}
pattern: '## Phase \d+: Convergence[\s\S]*\n- \[ \] T\d+ [^\n]*(--force|overwrit)'
match: contains
flags: i
weight: 1
---

The Carried constraint marked carry to converge (export --csv refuses to overwrite an existing
file unless --force is given) becomes a task in the Convergence phase.
