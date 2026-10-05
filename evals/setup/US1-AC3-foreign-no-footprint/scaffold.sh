#!/usr/bin/env bash
# Scaffold for US1-AC3: a repository whose remote belongs to someone other than the user.
# Runs in the case's empty working directory, which becomes the project.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixtures="$here/../../fixtures"
project=$(pwd)

# The remote belongs to someone else; the user's account is acme.
bash "$fixtures/make-project.sh" "$project" globex
git -C "$project" config user.name acme
git -C "$project" config user.email acme@example.com
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
