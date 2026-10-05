---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W2\b[\s\S]*?Test run: full \(per-wave runs off from wave 1\) · python -m pytest · \d+ passed, \d+ failed'
weight: 1
---

W2's report names its run as full because per-wave runs are off from wave 1.
