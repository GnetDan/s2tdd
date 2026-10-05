---
type: regex
weight: 1
target:
  source: file
  path: .git/info/exclude
pattern: '^specs/$'
flags: m
match: count:1
---

specs/ is listed once: setup appended nothing.
