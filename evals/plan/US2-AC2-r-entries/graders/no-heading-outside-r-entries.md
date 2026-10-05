---
type: regex
target: {source: file, path: specs/004-csv-export/research.md}
pattern: ^## (?!R\d+\. )
flags: m
match: not_contains
weight: 1
---
