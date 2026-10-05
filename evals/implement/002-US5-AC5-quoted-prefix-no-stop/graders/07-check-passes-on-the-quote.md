---
type: llm
focus: trace
weight: 1
---

Judging the run of `/s2tdd-implement W0 --print` on a feature whose orchestration.md quotes the
bare old command prefix (a slash and `speckit-` in backticks, followed by no command name) and
names no old command, and whose handoff.md names none. Pass if the orchestrator ran its
stale-name check as a search for an old command name (the prefix followed by a letter), found
nothing, did not stop or warn about stale names, did not ask to run `/s2tdd-harden handoff`, and
went on to print the filled prompt. Fail if it stopped on the quoted prefix, searched for the
bare prefix, or edited orchestration.md or handoff.md.
