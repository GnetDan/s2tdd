---
type: llm
focus: {source: file, path: .sdd-run/004/reports/P2a.md}
weight: 1
---

P2a's report shows `test_notes_store.py` (feature 003's test, not one of P2a's) failing in its
`pytest` run, then a run of that test alone (a command that names `test_notes_store.py` or its
test), which still failed (`notes.json not found`), and only after that reports it as still red.
Fail if the report names the red with no run of that test alone before it, or if it reports the
test as passing.
