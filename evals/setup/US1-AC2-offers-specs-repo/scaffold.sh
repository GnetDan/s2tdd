#!/usr/bin/env bash
# Scaffold for US1-AC2: a repository the user owns, with no specs/ directory.
# Runs in the case's empty working directory, which becomes the project.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
project=$(pwd)

# The user's account is acme: setup must not find another one through gh first.
bash "$fixtures/check-account.sh" acme
bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
# No specs/ directory: make-specs.sh is not run.
