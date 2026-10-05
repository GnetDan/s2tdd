#!/usr/bin/env bash
# Scaffold for US1-AC6: a set-up repository with no specs/constitution.md.
# Runs in the case's empty working directory, which becomes the project.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
project=$(pwd)

# The user's account is acme: setup must not find another one through gh first.
bash "$fixtures/check-account.sh" acme
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
