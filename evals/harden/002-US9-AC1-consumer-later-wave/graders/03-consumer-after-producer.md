---
type: llm
focus: {source: file, path: specs/004-csv-export/orchestration.md}
weight: 1
---

In the wave table, the implementation packet that owns `export.py` (the task that writes
`export_csv`, which uses `quote_field` and cites II-2) is in a strictly later wave than the
implementation packet that owns `quoting.py` (the task that writes `quote_field`, the producer of
II-2). Fail if the two are in the same wave, if one packet owns both files, or if `export.py`'s
packet comes first.
