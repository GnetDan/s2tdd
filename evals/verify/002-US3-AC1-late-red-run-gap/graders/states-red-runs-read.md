---
type: regex
target: trace
pattern: 'red runs read:\**\s*\**3\**\s+of\s+\**3(?!\d)\**'
match: contains
flags: i
weight: 1
---

verify-done states how many implementation packet reports' red runs it read: all three (P0c,
P1a, P1b).
