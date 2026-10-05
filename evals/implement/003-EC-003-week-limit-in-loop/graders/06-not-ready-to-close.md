---
type: regex
target: last_message
pattern: 'READY TO CLOSE'
match: not_contains
weight: 1
---

A run stopped by its week limit is not ready to close.
