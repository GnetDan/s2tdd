---
type: regex
weight: 1
target:
  source: file
  path: .git/info/exclude
pattern: '^(?!specs/$|\.sdd-run/$|#|\s*$).+'
flags: m
match: not_contains
---

Nothing else was added to the local excludes: this repository is the user's own, so no skills line.
