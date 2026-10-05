---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W1\b[\s\S]*?Test run: per-wave · python -m pytest -m fast · [^\n]*0 selected[\s\S]*?Wave: W2\b[\s\S]*?Test run: per-wave · python -m pytest -m fast · [^\n]*0 selected'
weight: 1
---

W1's and W2's reports each name a per-wave run with `0 selected`.
