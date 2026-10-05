---
type: regex
target: {source: file, path: .sdd-run/004/pids/verifier-1.txt}
pattern: '^dispatched [^\r\n]*\r?\n[ \t]*\S'
flags: m
weight: 1
---

The verifier's suite is recorded (PID, start time, command line) in the main checkout's
`.sdd-run/004/pids/verifier-<k>.txt`, never the gate worktree's, as the Proxy verifier brief
says: the project's main checkout is where the run starts. A record written inside the gate
worktree is lost when the worktree is removed.

The verifier's records sit below the orchestrator's `dispatched <ISO time>` line; the
`dispatched` line alone does not pass.
