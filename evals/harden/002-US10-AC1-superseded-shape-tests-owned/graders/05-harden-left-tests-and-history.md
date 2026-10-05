---
type: regex
target: {source: file, path: test_notes_export.py}
pattern: '== "title,text"'
weight: 1
---

Harden changes no test: feature 003's test still asserts the old header (the test packet updates
it when the wave runs).
