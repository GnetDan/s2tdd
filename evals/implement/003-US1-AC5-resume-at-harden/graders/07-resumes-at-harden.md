---
type: llm
focus: trace
weight: 1
---

Judging the whole run: the ledger showed an earlier nobrakes run whose round 1 converge
appended T008 and whose harden step then stopped (`Round 1: stopped · harden: assign scenario
IDs first …`); the user has since given the edge case its ID (EC-001). The rerun read the
ledger and resumed at that harden step: its first loop action was to dispatch s2tdd:hardener
with the Hardener brief on T008 (round 1), recording `Round 1: hardened · W<x>–W<y>`. It did
not run round 1's converge again before hardening, did not re-run or re-verify waves W0–W3 as
if they were unbuilt, did not ask the user what to do, and did not stop because every
originally planned task was already ticked. Carrying on afterwards (implementing the new wave
and converging again) is expected, not a failure.
