---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W2\b[\s\S]*?Test run: full \(no per-wave command\) · python -m pytest · \d+ passed, \d+ failed'
weight: 1
---

W2's report names its run: `full (no per-wave command)`, the `Full suite:` command and its counts.
