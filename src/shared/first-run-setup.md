**First-run setup.** Before this command's own work, check that this repository is set up for
s2tdd. Setup only adds: never delete or rewrite an existing file; the one file it changes is
`.git/info/exclude`, by appending lines.

1. **Whose repository.** Read the remote owner from `git remote get-url origin`: the path
   segment after the host, in the https or the ssh form. Find the user's account from the first
   of these that answers: `gh api user --jq .login`; `git config --get github.user`; otherwise
   ask the user once for their account name, and suggest they run
   `git config --global github.user <name>` themselves (setup never writes global config). An
   owner equal to the account (ignoring case), or no remote at all, makes the repository the
   user's own. Any other owner makes it foreign. If the user declines to answer, treat it as
   foreign.
2. **Specs repository.** If there is no `specs/` here or in the main worktree, offer to clone the
   user's existing specs repository into `specs/`, or to create one
   (`gh repo create <name>-specs --private`, then clone it into `specs/`). Write no spec until
   `specs/` is its own repository.
3. **Project pages.** Copy `./pages/README.md` to `specs/README.md` and `./pages/WORKFLOW.md` to
   `specs/WORKFLOW.md`, each only when it is missing; never overwrite one. Leave any older copy
   of a project page elsewhere in the project where it is.
4. **Local excludes.** Append to `.git/info/exclude` each of these lines that is not there yet:
   `specs/`, `.sdd-run/`, and, in a foreign repository only, `.claude/skills/s2tdd-*/`.
5. **Foreign check.** In a foreign repository, run `git status --porcelain` afterwards: nothing
   it shows may come from setup. If something does, stop and tell the user what it is.
6. **Silence.** When nothing was missing, say nothing about setup and go on.
