#!/usr/bin/env bash
# Scaffold for US2-AC8: a closed feature (004), an unhardened one (005) and one whose lease another session holds (006)
# Builds the fixture in the current directory: it is the project (git repository on main, a
# bare local remote standing in for GitHub), with specs/ as its own repository and its own
# bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" closed

specs="$project/specs"

# 005-tags: unhardened (a spec and a plan; no tasks, orchestration or handoff).
mkdir -p "$specs/005-tags"
sed -e 's/CSV export/Tags/' -e 's/004-csv-export/005-tags/' \
  "$specs/004-csv-export/plan.md" > "$specs/005-tags/plan.md"
sed -e 's/CSV export/Tags/' -e 's/004-csv-export/005-tags/' \
  -e 's/^\*\*Status\*\*: .*/**Status**: Draft/' \
  "$specs/004-csv-export/spec.md" > "$specs/005-tags/spec.md"

# 006-notes-export: hardened and open, with the run ledger's lease held by a session.
cp -R "$specs/004-csv-export" "$specs/006-notes-export"
rm "$specs/006-notes-export/close-out.md"
for f in spec.md plan.md tasks.md orchestration.md handoff.md validation.md; do
  sed -e 's/004-csv-export/006-notes-export/g' \
    -e 's/^\*\*Status\*\*: .*/**Status**: Draft/' \
    "$specs/006-notes-export/$f" > "$specs/006-notes-export/$f.tmp"
  mv "$specs/006-notes-export/$f.tmp" "$specs/006-notes-export/$f"
done
cat > "$specs/006-notes-export/run-ledger.md" <<'EOF_LEDGER'
# Run ledger: 006 Notes export

## Lease
session a1b2c3, relay 1, since 2026-10-02T09:00:00Z
## Runs
## Carried constraints
## Handoff
EOF_LEDGER

git -C "$specs" add 005-tags 006-notes-export
git -C "$specs" commit -q -m "feat: add 005-tags and 006-notes-export"
git -C "$specs" push -q origin main
