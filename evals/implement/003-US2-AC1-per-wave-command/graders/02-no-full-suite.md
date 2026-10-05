---
type: tool_used
tool: Bash
input_match: 'command\W+(?:(?:[^"\\]|\\.)*?(?:[;&|(]\s*|\\n\s*|python[\w.]*\s+-m\s+|/))?pytest\b(?!(?:\\[^n]|[^"\\\n;&|)])*?not slow)(?:(?!\.py\b|::)(?:\\[^n]|[^"\\\n;&|)]))*(?:$|"|\\n|[\n;&|)])'
max: 0
weight: 1
---

No full suite ran: no pytest run that names no test file and is not the per-wave command
(`-m "not slow"`). A run that names test files (P2a's done-when, a re-check) is not the full
suite. pytest counts only in command position, as in 002-US11-AC1's grader.
