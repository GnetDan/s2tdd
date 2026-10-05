---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Review:[^\n]*shape check: [^\n]*\(\d+ citations?, [1-9]\d* differ[);]'
weight: 1
---

W0's Review line carries the shape check with at least one citation that differs. The line may
be indented, as in a real report.
