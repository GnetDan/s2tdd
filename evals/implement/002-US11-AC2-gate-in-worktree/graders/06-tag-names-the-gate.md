---
type: tool_used
tool: Bash
input_match: '\bgit\b(?:\\.|[^"\\])*?\btag\b(?:\\.|[^"\\])*?\b004-s1\b'
min: 1
weight: 1
---

After the gate's verdict the orchestrator creates the tag `004-s1` for s1's gate (TAG). Graded
from the `git tag` command, not from a ref file, so a packed ref does not fail it; that the tag
names W0's commit, the gate worktree's commit, is graded by 04.
