---
type: regex
weight: 1
target: last_message
pattern: 'push[^.\n]{0,40}skipped|skipped[^.\n]{0,40}push'
flags: i
---

The Saved line says the push was skipped.
