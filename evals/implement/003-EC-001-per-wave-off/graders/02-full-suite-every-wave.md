---
type: tool_used
tool: Bash
input_match: 'command\W+(?:(?:[^"\\]|\\.)*?(?:[;&|(]\s*|\\n\s*|python[\w.]*\s+-m\s+|/))?pytest\b(?!(?:\\[^n]|[^"\\\n;&|)])*?acme_fast)(?:(?!\.py\b|::)(?:\\[^n]|[^"\\\n;&|)]))*(?:$|"|\\n|[\n;&|)])'
min: 2
weight: 1
---

The full suite ran at W1 (after the per-wave run failed to run) and at W2: at least twice. A pytest run is the full suite when no test path follows pytest in that command, as in
002-US11-AC1's grader: a run that names test files (a packet's done-when, a re-check) is
not; pytest counts only in command position.
