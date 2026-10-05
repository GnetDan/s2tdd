#!/usr/bin/env bash
# Scaffold for US6-AC2: the project on `claude/004-fix-flake`, one specs/004-* directory.
# Runs in the case's working directory, which becomes the project (acme-notes stand-in);
# its bare remotes land in ../remotes. Neutral names only (acme, 004-csv-export, ...).
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
project=$(pwd)

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" specified
git -C "$project" checkout -q main
git -C "$project" checkout -q -b claude/004-fix-flake
