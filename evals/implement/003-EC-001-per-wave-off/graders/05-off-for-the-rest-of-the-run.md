---
type: llm
focus: trace
weight: 1
---

Judging the whole run: the project's per-wave command, `python -m pytest -q -p acme_fast`,
fails to run (pytest cannot import the plugin `acme_fast`; its output has no summary line). At
W1 the orchestrator ran it, saw no summary line, treated that as a failure to run (not as red
tests), ran the full suite (`python -m pytest`) for W1, and recorded the Carried constraint
`Per-wave runs off from wave 1: <first error line>` in run-ledger.md, the first error line taken
from that output. At W2 it ran the full suite directly and did not run the per-wave command
again. Neither wave was treated as red because of the per-wave failure, and nobody edited
CLAUDE.md or installed a plugin to make it run. Fail if the per-wave command ran at W2, if a wave
was committed with no full-suite run, or if the constraint is missing.
