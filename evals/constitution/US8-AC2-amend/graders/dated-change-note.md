---
type: regex
target: {source: file, path: acme-notes/specs/constitution.md}
match: contains
weight: 1
---

- \d{4}-\d{2}-\d{2} · 1\.1\.0 → \d+\.\d+\.\d+ \((MAJOR|MINOR|PATCH)\)