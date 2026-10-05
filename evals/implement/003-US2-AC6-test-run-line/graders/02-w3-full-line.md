---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W3\b[\s\S]*?Test run: full \(changed README\.md outside Per-wave sees\) · python -m pytest · \d+ passed, \d+ failed · \d+m\d{2}s'
weight: 1
---

W3's report carries its Test run: line: a full run, why (`changed README.md outside Per-wave
sees`), the `Full suite:` command, the passed and failed counts, and the wall time.
