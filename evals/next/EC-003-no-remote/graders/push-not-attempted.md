---
type: tool_used
weight: 1
tool: Bash
input_match: 'git (-C \S+ )?push\b'
min: 0
max: 0
---

No push was run: there is no remote to push to. Graded on the agent's own Bash calls, not the
trace, whose skill text names `git -C specs push`.
