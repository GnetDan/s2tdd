#!/usr/bin/env bash
# Scaffold for US7-AC3 (upkeep-task).
# Given: a converge run over the stated suite-time budget (1 minute; the suite takes longer).
# Builds ./acme-notes in the current directory, with its bare remotes beside it in ./remotes.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$PWD/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened

# A one-minute budget, and an acceptance suite that takes longer: one fast test that is still
# red (the exporter is unbuilt) and one slow one.
printf '# acme-notes\n\nSuite-time budget: 1 minutes.\n\nRun the tests with `python -m pytest -q`.\n' \
  > "$project/CLAUDE.md"
cat > "$project/test_export.py" <<'EOF'
import time


def test_header_and_one_row_per_note():
    from export import export_csv

    assert export_csv(["a", "b"]).splitlines() == ["text", "a", "b"]


def test_large_notebook_is_exported():
    time.sleep(75)  # stands in for a slow fixture
EOF

git -C "$project" add -- CLAUDE.md test_export.py
git -C "$project" commit -q -m "test: add the export tests"
git -C "$project" push -q origin 004-csv-export

printf '\n**Acceptance tests**: `test_export.py` at the project root.\n' \
  >> "$project/specs/004-csv-export/plan.md"

git -C "$project/specs" add -A
git -C "$project/specs" commit -q -m "feat(004): name the acceptance tests"
git -C "$project/specs" push -q origin main
