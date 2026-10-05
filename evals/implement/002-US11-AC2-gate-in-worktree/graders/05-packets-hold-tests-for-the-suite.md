---
type: llm
focus: trace
weight: 1
---

Judging the whole run: while the verifier's suite ran, `.sdd-run/004/suite.lock` existed in the
main checkout, and W1's packets held their test runs until it was gone: as their cards, reports
or the orchestrator's notes show, no W1 packet ran a test while the lock existed (a packet that
met it waited, or reported `Blocked: suite lock`; a stale lock is reported as
`Unexpected: stale suite lock`). Fail if a W1 packet ran its tests during the verifier's suite,
or if no lock was written for the verifier's suite.
