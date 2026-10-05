#!/usr/bin/env bash
# Scaffold for EC-008: a project holding an earlier, unmigrated copy of a project page, docs/sdd-workflow.md.
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
# The older copy of the project page, tracked in the project.
mkdir -p "$project/docs"
printf '# Workflow (old)\n\nOlder, unmigrated copy of the project page.\n' > "$project/docs/sdd-workflow.md"
git -C "$project" add docs/sdd-workflow.md
git -C "$project" commit -q -m "docs: workflow page"
git -C "$project" push -q origin main
