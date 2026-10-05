---
type: llm
focus: trace
weight: 1
---

Judging the whole run: an attended session ran W2, its last wave, with the project's per-wave
command as the wave's test run, and committed it. Its final report (the last message) says that
the slice's full run is the user's `/s2tdd-verify-done`, in the line `Full run for this slice:
/s2tdd-verify-done reports: specs/004-csv-export/s1-wave-reports.md; commits <first>..<last>`,
where the commits are real commits of the slice (the range covers W2's commit). The session did
not run the full suite itself in place of that, nor start verify-done or a proxy verifier. Fail
if the final report has no such line, names another file, or the session ran verify-done.
