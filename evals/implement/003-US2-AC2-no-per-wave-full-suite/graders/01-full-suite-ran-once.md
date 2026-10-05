---
type: tool_used
tool: Bash
input_match: 'command\W+(?:(?:[^"\\]|\\.)*?(?:[;&|(]\s*|\\n\s*|python[\w.]*\s+-m\s+|/))?pytest\b(?:(?!\.py\b|::)(?:\\[^n]|[^"\\\n;&|)]))*(?:$|"|\\n|[\n;&|)])'
min: 1
max: 1
weight: 1
---

The orchestrator ran the full suite exactly once in W2. A pytest run is the full suite when no test path follows pytest in that command, as in
002-US11-AC1's grader: a run that names test files (a packet's done-when, a re-check) is
not; pytest counts only in command position.
