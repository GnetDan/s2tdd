---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's own tool calls in a run of `/s2tdd-implement W0`, from the start up
to the closing `/s2tdd-next` (ignore that command and what it runs). Pass if it never loaded
orchestration.md, tasks.md or handoff.md whole (a Read with no line range, or `cat`), reading
them by section, row and task ID instead. A Read of tasks.md immediately followed by an Edit of
tasks.md (the read the Edit tool requires before ticking) is allowed. Fail otherwise.
