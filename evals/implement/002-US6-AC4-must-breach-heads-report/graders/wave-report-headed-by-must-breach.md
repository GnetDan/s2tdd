---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'MUST breach: fix before the next wave[^\n]*\n(?:[ \t]*MUST breach: fix before the next wave[^\n]*\n)*[ \t]*Wave: W?0\b'
---

Wave 0's report in s1-wave-reports.md begins with the MUST breach line, before its Wave: line.
Report lines may be indented.
