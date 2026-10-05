#!/usr/bin/env bash
# Scaffold for US3-AC4 (stale-handoff-names).
# Given: a hardened feature whose handoff.md and orchestration.md still name /speckit- commands.
# Builds ./acme-notes in the current directory, with its bare remotes beside it in ./remotes.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$PWD/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-old-names
