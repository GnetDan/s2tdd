---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W3\b[\s\S]*?Test run: full \(changed assistant-prompt\.md outside Per-wave sees\) · python -m pytest · \d+ passed, \d+ failed'
weight: 1
---

W3's report says why the run was full: `changed assistant-prompt.md outside Per-wave sees`.
