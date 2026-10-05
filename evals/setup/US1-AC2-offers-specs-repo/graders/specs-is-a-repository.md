---
type: regex
weight: 1
target:
  source: file
  path: specs/.git/HEAD
pattern: '^ref: refs/heads/\S+'
---

specs/ is its own repository: it has its own .git (made by git init, git clone, or gh repo
create and a clone).
