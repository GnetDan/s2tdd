#!/usr/bin/env bash
# Scaffold for US1-AC4: a set-up repository on main, features 001-003 in specs/, and a remote-only branch 004-x.
# Runs in the case's empty working directory, which becomes the project.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
project=$(pwd)

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
# First-run setup already ran: both project pages are in specs/ and both excludes are set.
printf '# Specs

Existing page, keep as is.
' > "$project/specs/README.md"
printf '# Workflow

Existing page, keep as is.
' > "$project/specs/WORKFLOW.md"
printf '.sdd-run/
' >> "$project/.git/info/exclude"
git -C "$project/specs" add README.md WORKFLOW.md
git -C "$project/specs" commit -q -m "docs: project pages"
git -C "$project/specs" push -q origin main
# Features 001-003 are in specs/ already; 004-x exists only on the remote.
for feature in 001-csv-export 002-tags 003-notes; do
  mkdir -p "$project/specs/$feature"
  printf '# Feature Specification: %s\n\n**Status**: Closed\n' "$feature" > "$project/specs/$feature/spec.md"
done
git -C "$project/specs" add 001-csv-export 002-tags 003-notes
git -C "$project/specs" commit -q -m "feat: earlier features"
git -C "$project/specs" push -q origin main
git -C "$project" switch -q -c 004-x
git -C "$project" push -q -u origin 004-x
git -C "$project" switch -q main
git -C "$project" branch -q -D 004-x
