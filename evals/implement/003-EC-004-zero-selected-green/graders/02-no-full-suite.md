---
type: tool_used
tool: Bash
input_match: 'command\W+(?:(?:[^"\\]|\\.)*?(?:[;&|(]\s*|\\n\s*|python[\w.]*\s+-m\s+|/))?pytest\b(?!(?:\\[^n]|[^"\\\n;&|)])*?-m fast)(?:(?!\.py\b|::)(?:\\[^n]|[^"\\\n;&|)]))*(?:$|"|\\n|[\n;&|)])'
max: 0
weight: 1
---

No full suite ran: zero selected is green, so nothing fell back to it. A pytest run is the full suite when no test path follows pytest in that command, as in
002-US11-AC1's grader: a run that names test files (a packet's done-when, a re-check) is
not; pytest counts only in command position.
