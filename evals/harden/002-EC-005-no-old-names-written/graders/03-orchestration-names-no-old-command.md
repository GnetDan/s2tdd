---
type: regex
target: {source: file, path: specs/004-csv-export/orchestration.md}
pattern: '/speckit-[a-z]'
match: not_contains
weight: 1
---

orchestration.md names no old command: the slash, the old prefix and a letter (the pattern of
harden's gate and of implement's stale-name stop). A bare quoted prefix is not an old command.
