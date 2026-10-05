**Which epic.** Work out the epic, in this order; the first match wins:

1. **Named.** The text the user typed after the command names a slug, and
   `specs/epics/<slug>/` exists.
2. **Single open epic.** Exactly one epic in `specs/epics/` has a `map.md` whose `**Status**:`
   does not begin with `Closed`.
3. **Ask.** Otherwise, list the open epics and ask which one.
