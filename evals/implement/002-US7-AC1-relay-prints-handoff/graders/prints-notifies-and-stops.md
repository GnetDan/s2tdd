---
{type: llm, focus: trace, weight: 1}
---

The relay reaches its handoff (BRAKES) and hands off: it prints the handoff prompt whole, its
`Context:` block included; it sends a push notification where the harness offers a tool for one
(PushNotification), and otherwise prints only; then it stops. After its handoff commit it
dispatches no packet, starts no wave and writes no file. It never starts the next relay itself:
no scheduled task, routine, background `claude -p` or subagent runs the handoff prompt.
