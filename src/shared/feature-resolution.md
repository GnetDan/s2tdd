**Which feature.** Work out the feature this command is for, in this order; the first match
wins:

1. **Named.** The text the user typed after the command names a feature, as `NNN` or
   `NNN-name`, and `specs/` has that directory.
2. **Branch.** `git branch --show-current` prints a name, and `specs/<branch>/` exists.
3. **Branch number.** The branch name, after any `prefix/` such as `claude/`, starts with a
   number `NNN`, and exactly one directory `specs/NNN-*` has it.
4. **Ask.** Otherwise, list the open features (the directories in `specs/` whose spec's
   `**Status**:` does not begin with `Closed`) and ask which one.

If two directories share the number, ask; never pick one. Never write a pointer file: work the
answer out again on every run.
