---
type: regex
target: last_message
pattern: 'READY TO CLOSE'
match: not_contains
weight: 1
---

A run stopped before converge is not ready to close.
