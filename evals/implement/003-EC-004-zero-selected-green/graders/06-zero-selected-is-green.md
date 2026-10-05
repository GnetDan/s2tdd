---
type: llm
focus: trace
weight: 1
---

Judging the whole run: the per-wave command `python -m pytest -m fast` selects no tests (none
is marked `fast`); its output has pytest's summary line (`5 deselected`, after
`0 selected`) and exits 5. At W1 the orchestrator counted that run green, wrote `0 selected` in
the wave's Test run: line and committed W1; at W2 it ran the per-wave command again, counted it
green the same way and committed W2. It did not treat exit code 5 as a failure to run, did not
fall back to the full suite, did not record `Per-wave runs off`, and did not edit the command or
mark tests to make it select some. Fail if either wave ran the full suite as its test run or
was held as red.
