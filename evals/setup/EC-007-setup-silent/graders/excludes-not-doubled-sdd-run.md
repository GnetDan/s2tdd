---
type: regex
weight: 1
target:
  source: file
  path: .git/info/exclude
pattern: '^\.sdd-run/$'
flags: m
match: count:1
---

.sdd-run/ is listed once: setup appended nothing.
