---
type: tool_used
tool: Bash
input_match: '\bgrep\b[^\n]*speckit-\[a-z\]'
min: 1
weight: 1
---

The stale-name check ran as implement's search for an old command name (the prefix followed by
a letter, `grep -lE '/speckit-[a-z]'`).
