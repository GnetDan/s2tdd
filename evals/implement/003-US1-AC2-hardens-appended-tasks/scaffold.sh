#!/usr/bin/env bash
# Scaffold for 003-US1-AC2 (hardens-appended-tasks).
# Given: a nobrakes run whose converge appends three tasks. The looping state (II-15): every
# task of W0-W3 ticked and verified, the earlier `nobrakes once` run released `done`, its
# Rounds section empty. spec.md then gains three requirements the code does not meet and no
# scenario covers (FR-003, FR-004, FR-005), so the loop's first converge finds three gaps and
# appends one task for each; no acceptance test is red or absent, so no test task comes first.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" looping

fail() { echo "scaffold: $*" >&2; exit 1; }

cat >> "$dir/spec.md" <<'EOF'
- **FR-003**: `export --csv <path>` MUST refuse, with exit status 1 and the file left
  unchanged, when `<path>` already exists, unless `--force` is given.
- **FR-004**: `export --csv` MUST print `exported <n> notes to <path>` when it succeeds.
- **FR-005**: `export` MUST exit with status 2 and the message `no notebook: notes.json not
  found` when the working directory has no `notes.json`.
EOF
grep -qF -- '- **FR-005**:' "$dir/spec.md" || fail "spec.md: FR-005 not written"
if grep -q -- '--force' "$project/cli.py"; then fail "cli.py already has --force: FR-003 is no gap"; fi
if grep -q 'exported' "$project/export.py"; then fail "export.py already prints: FR-004 is no gap"; fi

git -C "$project/specs" add "$feature"
git -C "$project/specs" commit -q -m "004: spec: FR-003-FR-005"
git -C "$project/specs" push -q origin main
