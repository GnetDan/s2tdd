#!/usr/bin/env bash
# Scaffold for US7-AC4 (pruning-findings).
# Given: a project with a duplicated test file and an obsolete test file.
# Builds ./acme-notes in the current directory, with its bare remotes beside it in ./remotes.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$PWD/acme-notes"

bash "$fixtures/make-project.sh" "$project" acme
git -C "$project" config github.user acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" specified

# A duplicated test file and a test that pins a feature removed long ago.
cat > "$project/export.py" <<'EOF'
LEGACY_XML_ENABLED = False  # the XML export was removed in 0.3


def quote(text):
    return f'"{text}"' if "," in text else text


def export_csv(notes):
    return "\n".join(["text"] + [quote(note) for note in notes]) + "\n"
EOF
cat > "$project/test_export.py" <<'EOF'
from export import export_csv, quote


def test_export_has_a_header_and_one_row_per_note():
    assert export_csv(["a", "b"]).splitlines() == ["text", "a", "b"]


def test_field_with_a_comma_is_quoted():
    assert quote("a,b") == '"a,b"'
EOF
cp "$project/test_export.py" "$project/test_export_copy.py"
cat > "$project/test_legacy_xml.py" <<'EOF'
import export


def test_xml_export_is_off():
    assert export.LEGACY_XML_ENABLED is False
EOF

git -C "$project" add -- export.py test_export.py test_export_copy.py test_legacy_xml.py
git -C "$project" commit -q -m "feat: export notes to CSV"
git -C "$project" push -q origin 004-csv-export
