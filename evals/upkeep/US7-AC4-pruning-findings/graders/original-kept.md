---
type: regex
target: {source: file, path: acme-notes/test_export.py}
match: contains
flags: i
weight: 1
---

^(?![\s\S]*(skip|xfail))[\s\S]*def test_