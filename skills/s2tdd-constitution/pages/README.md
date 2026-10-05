# specs/ — build context, not documentation

Each `NNN-name/` directory is context assembled to drive an implementing agent to one goal:
what to build, the shapes to build it to, and the order to build it in. It is **not
documentation of the application, in any way** — not while it is open, and not after. The
application is documented by its code and its tests (`tests/acceptance/` for behaviour,
`tests/contract/` and `tests/architecture/` for boundaries), then `CLAUDE.md`, `README.md`,
and `docs/`.

A directory is authoritative only while its feature is open, and only for that feature. Once
the goal is met and the spec is closed it **stops being maintained**, and nothing may depend on
it — no doc, no test, no agent instruction, no code comment. New work, including evolution of
something an earlier spec built, becomes a **new** spec, which is invalidated the same way once
its own goal is met.

**Status** — the `**Status**:` line in `spec.md` (free text after an em dash is fine):

- `Draft` — open. Skills read and write this directory. "Draft — deferred …" is still open.
- `Closed — YYYY-MM-DD — <sha>` — stamped by `/s2tdd-close`, which also writes `close-out.md`
  (delivered, not delivered, deviations from intent, checkpoints, where to look now) as the record
  of the close itself. The directory is inert from then on. Do not open a closed feature to
  learn what the system does, why it does it, or what was decided — read the code, the tests,
  and `docs/`.

Rules:

- Never edit a closed feature. A later feature that changes what an earlier spec defined adds a
  `**Supersedes**:` line to its own spec.
- Anything that must stay true after close-out lives in code, tests, or `docs/`, not here. If
  you find yourself wanting to cite a spec directory from outside `specs/`, that content is in
  the wrong place — move it before the feature closes.

List statuses: `grep -n "^\*\*Status\*\*" specs/*/spec.md`

## Epics — `specs/epics/<slug>/`

An epic plans work too big and too unclear for one spec (`/s2tdd-epic`): `map.md` indexes the
decisions, one file per ticket under `tickets/` holds each one. It is build context like a
feature directory, with the same lifecycle:

- `**Status**: Open` while charting and working.
- `**Status**: Closed — YYYY-MM-DD — <sha> — specs: <NNN-a>, …` once every feature spec it hands
  off to exists. From then on the specs own the work and the epic is frozen: never back-edited.
  A feature that changes an epic decision records `**Supersedes**:` in its own spec.

List epic statuses: `grep -n "^\*\*Status\*\*" specs/epics/*/map.md`
