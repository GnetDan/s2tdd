---
type: regex
target: {source: file, path: specs/004-csv-export/validation.md}
pattern: 'converge · at [0-9a-f]+ · [^\n]*· suite \d+m\d+s \((no budget|budget)'
match: contains
weight: 1
---

Converge's verification-log line ends with the suite suffix of a run it made
(`· suite <M>m<SS>s (no budget)`).
