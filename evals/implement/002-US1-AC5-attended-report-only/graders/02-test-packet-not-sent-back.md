---
type: tool_used
tool: Agent
input_match: '^(?=[\s\S]*s2tdd:packet-)(?=[\s\S]*test_export_rows)(?![\s\S]*test_quoting)(?![\s\S]*cli\.py)'
min: 1
max: 1
weight: 1
---

P0a's own dispatch (its owned file, `test_export_rows.py`, and neither sibling's) happens once: attended, the shape check is report-only, so no fix is sent back to the
test packet before the commit.
