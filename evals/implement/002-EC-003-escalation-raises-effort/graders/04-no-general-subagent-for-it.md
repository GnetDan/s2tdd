---
type: tool_used
tool: Agent
input_match: '(?=[\s\S]*subagent_type\W+(general-purpose|claude|Explore|Plan)\b)(?=[\s\S]*\bP1b\b)'
min: 0
max: 0
weight: 1
---

Every P1b attempt, the escalated one included, goes to an s2tdd agent type, which carries its
tier's effort; never a general subagent, which carries none.
