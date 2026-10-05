---
type: llm
name: asks-instead-of-picking
weight: 1
focus: last_message
---

The user ran `/s2tdd-harden` with no argument on branch `claude/004-fix-flake`, where two directories (`004-csv-export` and `004-tags`) share the number 004. The reply lists the open features and asks which one to work on. It does not pick one or start work on either.
