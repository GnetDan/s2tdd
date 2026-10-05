---
type: tool_used
tool: Bash
input_match: 'command\W+(?:(?:[^"\\]|\\.)*?(?:[;&|(]\s*|\\n\s*|python[\w.]*\s+-m\s+|/))?pytest\b(?:(?!\.py\b|::)(?:\\[^n]|[^"\\\n;&|)]))*(?:$|"|\\n|[\n;&|)])'
min: 1
max: 1
weight: 1
---

The orchestrator ran the full suite exactly once in the wave. A pytest run is the full suite
when no test path follows pytest in that command: flags and their values (`-q`, `-p X`,
`-k "..."`, `-n auto`) and `.` are not test paths; a `.py` file or a `::` node id is. A run that
names test files (a test packet's done-when, a re-check) is not the full suite. The command ends
at the end of the string, a newline (escaped or not), or a shell separator. pytest counts only
in command position (first word, after a separator or newline, after `python -m`, or as a path's
last part), not inside a quoted message.
