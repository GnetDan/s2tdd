---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/s1-wave-reports.md}
pattern: 'Wave: W?2\b(?:(?!Wave: W?\d)[\s\S])*?Boundary: context (\d+|n/a|unavailable)%?\s*·\s*five-hour (\d+|n/a|unavailable)%?\s*·\s*week (\d+|n/a|unavailable)%?\s*·\s*BRAKES (none|found)\s*·\s*ledger \+\d+ lines?'
---

Wave 2's report in s1-wave-reports.md carries the Boundary line in its format (each
window an integer, n/a or unavailable). Report lines may be indented.
