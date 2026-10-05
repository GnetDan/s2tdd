#!/usr/bin/env bash
# Scaffold for US1-AC7: a set-up repository; /s2tdd-specify is the command that finishes.
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
