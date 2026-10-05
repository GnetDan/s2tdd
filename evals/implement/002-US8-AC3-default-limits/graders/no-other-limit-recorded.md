---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: 'Usage limits: week (?!95%)\d+%|Usage limits: [^\n]*five-hour (?!90%)\d+%'
match: not_contains
---

No other limit is recorded.
