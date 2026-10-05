---
type: llm
focus: trace
weight: 1
---

Judging the orchestrator's dispatches of the cheap packet P1b (T005, quoting.py) in this
`--nobrakes` run of wave W1. P1b's fence is `pytest test_quoting.py` and the guard `python
check_quoting.py`, which checks quote_field against contracts/internal-interfaces.md §II-2's
full rule; T005's line summarizes only part of it, so an attempt can fail the guard. The guard
agrees with the contract and the tests: a failure is the packet's, to be retried, not a
contract need or a test defect.
If P1b failed its fence twice at `s2tdd:packet-cheap` (effort low), pass only if its third
attempt went to a fresh agent one tier up, `s2tdd:packet-medium` (effort medium, a higher
effort than the first), with both earlier failure reports attached (the guard's failure lines,
or both reports' paths together with their failure lines). Fail if that attempt stayed at
cheap, skipped to strong, went to a general subagent, carried fewer than both failure reports,
or if P1b was escalated before failing twice, or if a guard failure was routed to a contract
amendment or a test-owner fix instead.
If P1b passed its fence within its first two attempts, the escalation did not arise: pass if
P1b was dispatched as `s2tdd:packet-cheap` and never to a higher tier.
