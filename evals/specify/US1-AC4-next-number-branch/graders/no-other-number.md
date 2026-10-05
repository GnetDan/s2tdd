---
type: regex
weight: 1
target: trace
pattern: 'git (switch -c|checkout -b) (00[1-4]|00[6-9]|0[1-9]\d|[1-9]\d\d)-'
match: not_contains
---

The agent did not create a branch with any number but 005.
