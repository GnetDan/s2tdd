---
type: llm
weight: 1
---

The agent's last message is what /s2tdd-next printed after /s2tdd-specify finished. Pass if it
shows, in this order: a one-line account of the save in the specs repository (committed and
pushed, or what stopped it), a short account of where things stand, and the next step as a
command in a fenced block, a prompt the user can paste. Fail if the save line is missing, comes
after the recap, or there is no ready-to-paste prompt.
