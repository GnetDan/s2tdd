---
type: tool_used
weight: 1
tool: Bash
input_match: 'git (-C (?!\S*specs\b)\S+ )?(commit|push)\b'
min: 0
max: 0
---

The project repository itself got no commit or push: every commit and push names git -C specs.
Graded on the agent's own Bash calls, not the trace, whose skill text names `git push -u origin`.
