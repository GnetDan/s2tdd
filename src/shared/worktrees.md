**Where specs/ is.** If `./specs` does not exist here, this may be a worktree: run
`git worktree list --porcelain` and use `specs/` in the first worktree it lists (the main
checkout). Say so in one line ("Using specs/ from the main worktree at <path>."), and write every
spec file there, so it lands in the one specs repository.
