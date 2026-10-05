---
type: llm
focus: trace
weight: 1
---

Judging the whole run: at s1's end (after W0's commit) the orchestrator dispatched the proxy
verifier for W0 and did not wait for its verdict before starting W1: W1's packets were
dispatched while the verifier was still running, before its verdict came back. The verifier
verified in a scratch worktree (`.sdd-run/004/gate-1`) at W0's wave commit, the commit the gate's
tag (`004-s1`) then named; it did not verify in the main checkout. Fail if the orchestrator
waited for the verdict before dispatching W1's first packet, or if the gate verified in the main
checkout.
