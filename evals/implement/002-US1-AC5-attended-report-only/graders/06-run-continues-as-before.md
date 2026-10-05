---
type: llm
focus: trace
weight: 1
---

Judging the whole run: in this attended run, W0's shape check found P0a's CRLF test differing
from II-1. The orchestrator treated the finding as report-only: it did not send it back to P0a
or re-dispatch P0a, did not run a re-check, did not stop or ask the user before the commit
because of it, committed W0, and ended as an attended run does after the last wave in its scope
(its wave report and the RESUME AT line). Fail if the finding held the commit or the run.
