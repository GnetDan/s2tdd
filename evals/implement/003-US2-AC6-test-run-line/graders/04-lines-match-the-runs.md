---
type: llm
focus: trace
weight: 1
---

Judging the whole run and the wave reports it appended to
`specs/004-csv-export/s1-wave-reports.md`: each of W2 and W3 has a report whose `Test run:` line
names which run it was (per-wave for W2, which changed only `export.py`; full for W3, which
changed `README.md`, outside `Per-wave sees: *.py`), the command that ran, its counts (passed,
failed, and selected for the per-wave run) and its wall time. The line describes the run the
orchestrator actually made in the trace: the same command, counts that agree with that run's
summary line, and a plausible wall time. The suite's counts are not in the `Commands run +
results:` line instead. Fail if a wave's report has no Test run: line, or the line names a run,
command or counts the trace does not show.
