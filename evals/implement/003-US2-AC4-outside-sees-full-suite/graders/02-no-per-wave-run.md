---
type: tool_used
tool: Bash
input_match: 'pytest(?:\\.|[^"\\])*not slow'
max: 0
weight: 1
---

The per-wave command (`python -m pytest -q -m "not slow"`) never ran: the wave changed a file outside Per-wave sees.
