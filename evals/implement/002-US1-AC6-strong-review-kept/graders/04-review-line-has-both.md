---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Review:[^\n]*P0c: (Accept|Reject)[^\n]*shape check: (Accept|Reject)'
weight: 1
---

W0's Review line carries P0c's review verdict and the shape check's. The line may be indented,
as in a real report.
