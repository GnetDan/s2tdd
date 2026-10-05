#!/usr/bin/env bash
# Scaffold for 002-US6-AC3 (ledger-notes-to-tasks).
# Given: run-ledger.md has open review notes and "carry to converge" constraints. Starts from
# make-feature.sh's ledger-notes state: two Open review notes (W0 · P0c's, resolved by the later
# commit "fix(004): export requires --csv (open review note W0 · P0c)"; W1 · P1a's, a note with
# no title key raising KeyError, still open) and one Carried constraint marked carry to converge
# (export --csv refuses to overwrite an existing file unless --force is given, still open). It
# finishes the feature so converge's implementation-complete guard lets it run: W2 (P2a, T006:
# write_csv, every field through quote_field) and W3 (P3a, T007: the README names the flag),
# both ticked, and verify-done's line in validation.md. Neither wave touches the open note or
# the constraint: export_csv still reads note[key], and write_csv overwrites without asking.
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
specs="$project/specs"
dir="$specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" ledger-notes

first=$(git -C "$project" log --format=%h --grep='^feat(004): wave 0' -n 1)

# W2: P2a (T006).
cat > "$project/export.py" <<'EOF'
"""CSV export of a notebook (II-1, II-2)."""
import json

from quoting import quote_field

HEADER = ("id", "title", "text")


def export_csv(notes):
    """The notebook as CSV text: a header row, then one row per note, every row ending in LF.
    Every field goes through quote_field."""
    rows = [",".join(HEADER)]
    rows += [",".join(quote_field(str(note[key])) for key in HEADER) for note in notes]
    return "\n".join(rows) + "\n"


def write_csv(path):
    """Read the notebook (notes.json in the working directory) and write it to path as CSV."""
    with open("notes.json", encoding="utf-8") as source:
        notes = json.load(source)
    with open(path, "w", encoding="utf-8", newline="") as target:
        target.write(export_csv(notes))
    return 0
EOF
git -C "$project" add export.py
git -C "$project" commit -q -m "feat(004): wave 2 — P2a"

# W3: P3a (T007).
cat >> "$project/README.md" <<'EOF'

## Export

`python cli.py export --csv notes.csv` writes the notebook (`notes.json`) to a CSV file: a
header row, then one row per note.
EOF
git -C "$project" add README.md
git -C "$project" commit -q -m "feat(004): wave 3 — P3a"
last=$(git -C "$project" rev-parse --short HEAD)
git -C "$project" push -q origin "$feature"

ticked=$(sed -e 's/^- \[ \] \(T00[67] \)/- [x] \1/' "$dir/tasks.md")
printf '%s\n' "$ticked" > "$dir/tasks.md"
printf -- '- 2026-10-02 · verify-done · waves W0–W3 (%s..%s) · Verified with gaps · proxy · suite 0m01s (no budget)\n' \
  "$first" "$last" >> "$dir/validation.md"

git -C "$specs" add "$feature"
git -C "$specs" commit -q -m "004: waves 2–3 ticked (T006–T007); verified"
git -C "$specs" push -q origin main
