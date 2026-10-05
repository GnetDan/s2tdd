---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's own tool calls in a run of `/s2tdd-implement W0` (tasks T001-T003),
from its first packet dispatch to the wave commit. Ignore everything before the first
dispatch, and everything from the closing `/s2tdd-next` on. Pass if, in that span, the
orchestrator never read T001-T003 from tasks.md again (a grep naming them, a grep of open
tasks, a Read or `cat` of tasks.md) after having read them before the first dispatch. A Read of
tasks.md immediately followed by an Edit of tasks.md (the read the Edit tool requires before
ticking the tasks) is not a re-read, and neither is a sed or Edit that ticks them. Fail on any
other re-read.
