#!/usr/bin/env bash
# Scaffold for 002-US5-AC5 (quoted-prefix-no-stop).
# Given: an orchestration.md that quotes the bare old command prefix (the slash and `speckit-`,
# followed by no command name) and names no old command. The hardened-shapes state (II-16),
# whose orchestration.md gains one line after its title paragraph quoting the bare prefix in
# backticks; handoff.md stays clean. Implement's stale-name check (II-10, FR-031, J-18:
# `grep -lE '/speckit-[a-z]'`) matches only an old command name, so it lists neither file.
# Committed and pushed in the specs repository.
# Builds the fixture in the current directory: it is the project (a git repository on the
# branch 004-csv-export, a bare local remote standing in for GitHub), with specs/ as its own
# repository and its own bare remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
dir="$project/specs/$feature"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" hardened-shapes

fail() { echo "scaffold: $*" >&2; exit 1; }

# insert_after <file> <ERE> <text>: the text goes after the first line matching the ERE.
insert_after() {
  PAT="$2" TEXT="$3" awk '{ print } !done && $0 ~ ENVIRON["PAT"] { print ENVIRON["TEXT"]; done = 1 }' \
    "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
}

prefix="/speckit-"
insert_after "$dir/orchestration.md" '^Regenerate it with `/s2tdd-harden`\.$' \
  "Commands that began \`$prefix\` under the preset are renamed; this file names only \`/s2tdd-\` commands."

grep -qF -- "\`$prefix\`" "$dir/orchestration.md" || fail "orchestration.md: the bare prefix is not quoted"
if grep -qE -- '/speckit-[a-z]' "$dir/orchestration.md" "$dir/handoff.md"; then
  fail "an old command name is planted; only the bare prefix may be"
fi

git -C "$project/specs" add "$feature/orchestration.md"
git -C "$project/specs" commit -q -m "004: orchestration.md quotes the old prefix"
git -C "$project/specs" push -q origin main
