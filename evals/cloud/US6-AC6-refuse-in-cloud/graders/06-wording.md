---
type: llm
name: refuses-and-points-to-cloud-flag
weight: 1
focus: last_message
---

The session is a cloud session (the environment variable `CLAUDE_CODE_REMOTE` is `true`) and the user ran `/s2tdd-pr-review 1`. The reply refuses to run the review here and says to start it locally with `--cloud`. It does not begin reviewing the pull request.
