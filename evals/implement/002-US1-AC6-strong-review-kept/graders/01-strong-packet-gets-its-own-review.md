---
type: tool_used
tool: Agent
input_match: '^(?=[\s\S]*s2tdd:strong-diff-reviewer)(?=[\s\S]*(P0c|cli\.py))(?![\s\S]*Shape check)'
min: 1
weight: 1
---

The strong packet P0c gets its own strong-diff review: a reviewer dispatch for P0c that is not
the shape check.
