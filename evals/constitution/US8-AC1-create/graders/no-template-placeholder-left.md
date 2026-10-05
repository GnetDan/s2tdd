---
type: regex
target: {source: file, path: acme-notes/specs/constitution.md}
match: not_contains
weight: 1
---

\[[A-Z][A-Z0-9_]{3,}\]