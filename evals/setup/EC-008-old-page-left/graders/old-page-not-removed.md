---
type: regex
weight: 1
target: trace
pattern: '\brm\b[^\n]*sdd-workflow|git (mv|rm)\b[^\n]*sdd-workflow|mv [^\n]*sdd-workflow'
match: not_contains
---

The agent never moved or deleted the old page.
