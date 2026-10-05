---
type: llm
focus: {source: file, path: specs/004-csv-export/orchestration.md}
weight: 1
---

In the wave table, `test_notes_export.py` (feature 003's test, which asserts the old header
`title,text`) is an owned file of a test packet: a packet that owns test files only, never
`export.py`. That packet's tasks include the task that updates the test to II-1's header
`id,title,text`. The Superseded-shape searches table lists the search (for `export_csv` or the
header) with `test_notes_export.py` among its hits and that packet, or its task, as owner. Fail
if the file is owned by an implementation packet, by no packet, or only mentioned in a
done-when.
