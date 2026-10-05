---
type: tool_used
tool: Agent
input_match: '(?=[\s\S]*[Ff]or each citation)(?=[\s\S]*(P0a|test_export_rows))(?=[\s\S]*(P0b|test_quoting))'
min: 1
arm: both
weight: 1
---

Whatever agent type runs it, W0's shape check is dispatched with the Shape check brief from
handoff.md's Standard briefs, filled for the test packets P0a and P0b (its per-citation line:
"For each citation: matches, or differs").
