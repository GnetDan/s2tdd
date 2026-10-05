---
type: regex
weight: 1
target: {source: file, path: specs/004-csv-export/run-ledger.md}
pattern: '## Handoff[\s\S]*(LF on every platform|Windows included|week 95%|five-hour 90%|limits do not apply|not_applicable)'
match: not_contains
---

The handoff prompt under Handoff restates no carried constraint: neither the review's
LF rule, nor a usage limit, nor that the window limits do not apply.
