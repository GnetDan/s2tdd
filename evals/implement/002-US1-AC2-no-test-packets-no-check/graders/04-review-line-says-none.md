---
type: regex
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W2\b[\s\S]*?Review:(\s*none\b|[^\n]*shape check: none)'
weight: 1
---

W2's wave report, appended after W0's and W1's, says `shape check: none` in its Review line, or `Review: none` (no reviewed packet and no
shape check).
The line may be indented, as in a real report.
