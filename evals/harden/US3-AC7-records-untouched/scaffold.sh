#!/usr/bin/env bash
# Scaffold for US3-AC7 (records-untouched).
# Given: a carried-over feature whose validation.md, run-ledger.md and tasks.md name /speckit- commands.
# Builds ./acme-notes in the current directory, with its bare remotes beside it in ./remotes.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$PWD/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-old-names

# History that names the old commands: harden's handoff phase must leave it alone.
cat >> "$project/specs/004-csv-export/tasks.md" <<'EOF'

## Notes

Hardened with /speckit-harden; saved with /speckit-save.
EOF
printf -- '- 2026-09-30 · verify-done via /speckit-verify-done · Verified\n' \
  >> "$project/specs/004-csv-export/validation.md"
cat > "$project/specs/004-csv-export/run-ledger.md" <<'EOF'
# Run ledger: CSV export

## Lease

- released by user 2026-09-30 (the preset's /speckit-implement run)
EOF

git -C "$project/specs" add -A
git -C "$project/specs" commit -q -m "feat(004): history from the preset"
git -C "$project/specs" push -q origin main
