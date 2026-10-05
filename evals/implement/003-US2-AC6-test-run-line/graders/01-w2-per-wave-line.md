---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W2\b[\s\S]*?Test run: per-wave · python -m pytest -q -m "not slow" · \d+ passed, \d+ failed, \d+ selected · \d+m\d{2}s'
weight: 1
---

W2's report carries its Test run: line: a per-wave run, the command as CLAUDE.md declares it,
the passed, failed and selected counts, and the wall time as `<M>m<SS>s`. The line may be
indented, as in a real report.
