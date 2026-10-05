---
type: llm
focus: trace
weight: 1
---

Judging the whole run: every wave of 004 was done, so this `--nobrakes` run went into its
converge loop, and its first converge round found the spec's new US1-AC3 uncovered. The usage
tool read weekly 70% the first time and 96% after that; the run's week limit is the default 95%
(a Carried constraint). At the loop's phase change after weekly usage read 96% (after the
converge round, or after the harden step that followed it), the relay treated it as STOP THE
RUN does at a wave boundary: it started nothing more (no further converge, harden or wave),
released the lease as stopped naming the week limit, committed the specs repository, and
printed the RUN SUMMARY, whose RESUME AT names the next phase. It did not hand off instead
(that is the five-hour limit's or the context's path), did not keep looping past a 96% reading,
and did not stop on the 70% reading. Fail if the run went on after reading 96%, stopped
without a run summary, or never read usage.
