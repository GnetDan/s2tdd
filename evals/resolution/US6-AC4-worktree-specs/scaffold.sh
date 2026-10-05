#!/usr/bin/env bash
# Scaffold for US6-AC4: a worktree with no ./specs, beside the main checkout.
# Runs in the case's working directory, which becomes the project (acme-notes stand-in);
# its bare remotes land in ../remotes. Neutral names only (acme, 004-csv-export, ...).
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
# The main checkout is ./acme-notes (with its own specs/ repository); its worktree is
# ./acme-notes-worktree on branch claude/004-csv-export, with no specs/ of its own.
project="$(pwd)/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" worktree
