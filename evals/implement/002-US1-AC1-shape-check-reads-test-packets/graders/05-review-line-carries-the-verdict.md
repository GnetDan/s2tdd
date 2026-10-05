---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Review:[^\n]*shape check: (Accept|Reject)[^\n]*\(\d+ citations?, \d+ differ[);]'
weight: 1
---

W0's wave report has a Review line with the shape check's verdict and its counts. The line may
be indented, as in a real report.
