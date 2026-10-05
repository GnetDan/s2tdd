---
type: tool_used
tool: Bash
input_match: '\bgrep\b[^\n]*speckit-\\?[''"][^\n]*(handoff|orchestration)\.md'
min: 0
max: 0
weight: 1
---

No search of handoff.md or orchestration.md on the bare prefix (`grep -l '/speckit-' …`),
which would list orchestration.md for its quoted prefix. Other searches (such as a leftover
check for old skills) are not this check.
