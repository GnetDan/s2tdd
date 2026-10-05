---
type: tool_used
tool: Bash
input_match: 'pytest(?:\\.|[^"\\])*not slow'
min: 1
weight: 1
---

The orchestrator ran the project's per-wave command, `python -m pytest -q -m "not slow"`, as
written (CLAUDE.md's `Per-wave tests:` line, copied into handoff.md's TEST RUN).
