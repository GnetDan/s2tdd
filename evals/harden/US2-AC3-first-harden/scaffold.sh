#!/usr/bin/env bash
# Scaffold for US2-AC3: a planned feature with no tasks.md
# Builds the fixture in the current directory: it is the project (git repository on main, a
# bare local remote standing in for GitHub), with specs/ as its own repository and its own
# bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" planned

cat > "$project/specs/constitution.md" <<'EOF_CONSTITUTION'
# acme-notes Constitution

## Core Principles

### I. Plain files only
Notes live as plain files on disk. No database server, no network service.

### II. Standard library first
A feature uses the Python standard library unless a dependency is justified in its plan.

### III. Test-first
Tests are written and seen failing before the code that makes them pass.

**Version**: 1.0.0 | **Ratified**: 2026-10-02 | **Last Amended**: 2026-10-02
EOF_CONSTITUTION
git -C "$project/specs" add constitution.md
git -C "$project/specs" commit -q -m "docs: constitution 1.0.0"
git -C "$project/specs" push -q origin main
