---
type: regex
target: {source: file, path: acme-notes/.git/refs/heads/004-csv-export}
match: contains
flags: m
weight: 1
---

^[0-9a-f]{40}$