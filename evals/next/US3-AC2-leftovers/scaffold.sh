#!/usr/bin/env bash
# Scaffold for US3-AC2 (leftovers).
# Given: a project that still has .specify/, a speckit-* skill and docs/sdd-workflow.md.
# Builds ./acme-notes in the current directory, with its bare remotes beside it in ./remotes.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$PWD/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened

# The spec-kit leftovers, all untracked in the project.
mkdir -p "$project/.specify" "$project/.claude/skills/speckit-plan" "$project/docs"
cat > "$project/.specify/README.md" <<'EOF'
# Old spec-kit install

Left behind by an earlier version of the workflow.
EOF
cat > "$project/.claude/skills/speckit-plan/SKILL.md" <<'EOF'
---
name: speckit-plan
description: "An old planning skill."
---

An old planning skill, left behind by an earlier version of the workflow.
EOF
cat > "$project/docs/sdd-workflow.md" <<'EOF'
# Workflow

The old workflow page, kept from before the move to the plugin.
EOF
