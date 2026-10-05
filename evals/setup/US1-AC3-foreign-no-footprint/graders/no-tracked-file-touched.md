---
type: tool_used
weight: 1
tool: Bash
input_match: 'git (-C (?!\S*specs\b)\S+ )?(add|commit|reset|restore|rm|mv|clean)\b|git (-C (?!\S*specs\b)\S+ )?checkout( \S+)? -- |git (-C (?!\S*specs\b)\S+ )?stash(?! (list|show)\b)'
min: 0
max: 0
---

Nothing tracked in the project was edited: no Bash command the agent ran adds, commits, resets,
restores, removes, moves, cleans, checks out over or stashes files in the project. Read-only
forms (`git stash list`, `git status`) and commands in the specs repository (`git -C specs ...`)
do not count. Graded on the agent's own Bash calls, not the trace, whose skill text names these
commands.
