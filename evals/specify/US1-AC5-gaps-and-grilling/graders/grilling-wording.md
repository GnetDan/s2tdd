---
type: llm
weight: 1
---

The agent's last message is one round of questions about a draft spec for sharing notes. Pass
only if all of these hold: every question is followed by a recommended answer with a one-line
reason; there is one round, with no second round invented; none of the questions is answered by
the agent itself, and the message says the answers are the user's; no open design question was
settled by an informed guess in the draft (settled choices must be marked as questions, not
filled in). Fail otherwise.
