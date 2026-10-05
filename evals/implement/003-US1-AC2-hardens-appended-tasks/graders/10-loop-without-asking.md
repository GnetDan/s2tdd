---
type: llm
focus: trace
weight: 1
---

Judging the whole run: the run started on a feature whose waves W0–W3 were all ticked and
verified, so it went straight to the converge loop. Round 1's converger appended tasks for the
three requirements no code met (FR-003, FR-004, FR-005). When that round ended, the run did not
stop and did not ask the user anything: it applied the stop rules (none fired in round 1),
dispatched s2tdd:hardener with the Hardener brief on the appended tasks (harden in append
mode, adding new waves and never renumbering or rewriting the existing tasks or waves),
recorded `Round 1: hardened · W<x>–W<y>`, ran the new waves as any other waves (packets, the
wave commits, a verify gate before the next converge), and then dispatched the converger again
for round 2. Fail if the run stopped after round 1's converge, asked the user to run harden,
ran /s2tdd-harden or implemented the tasks in its own context instead of through subagents, or
never converged a second time.
