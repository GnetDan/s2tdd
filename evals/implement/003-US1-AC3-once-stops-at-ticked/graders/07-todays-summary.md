---
type: llm
focus: last_message
weight: 1
---

The final message is the nobrakes RUN SUMMARY of a run that stopped when every task in its
scope was ticked, as 0.3.0's runs did: its header line `NOBRAKES · 004 · run <id> · …`, then
its Waves, Gates, Blocked, Ledger, Pending, Docs and RESUME AT lines. It reports no converge
round (no Rounds line saying a round converged or appended tasks) and does not end with the
`READY TO CLOSE` block or a `Next:` list naming /s2tdd-pr-review and /s2tdd-close. Fail if
the message says the run converged, is ready to close, or is still running.
