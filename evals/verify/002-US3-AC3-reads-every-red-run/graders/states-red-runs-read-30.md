---
type: regex
target: trace
pattern: 'red runs read:\**\s*\**30\**\s+of\s+\**30(?!\d)\**'
match: contains
flags: i
weight: 1
---

verify-done states that it read the red runs of all 30 implementation packet reports.
