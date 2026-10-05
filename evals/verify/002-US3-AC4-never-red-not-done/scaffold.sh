#!/usr/bin/env bash
# Scaffold for 002-US3-AC4 (never-red-not-done).
# Given: an implementation packet whose test neither its report nor the orchestrator's
# pre-dispatch check ever shows red. Starts from make-feature.sh's wave-reports state and takes
# every sign of test_quoting.py's red out of the reports: W1's P1b (T005, quoting.py) quotes no
# red run, P0b (its test packet, T002) quotes none either, and neither W0's nor W1's wave report
# shows test_quoting.py red. The reports are edited both in the project's .sdd-run/004/reports/
# and in s1-wave-reports.md, and the specs commit that wrote them is amended (as if written so).
# Builds the project in the current directory (on branch 004-csv-export, with a bare local
# remote beside it standing in for GitHub), with specs/ as its own repository and its own bare
# remote. Helpers: evals/fixtures/. Neutral names only.
set -euo pipefail

fixtures="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../fixtures" && pwd)"
project="$(pwd)"
feature=004-csv-export
specs="$project/specs"
dir="$specs/$feature"
reports="$project/.sdd-run/004/reports"

bash "$fixtures/make-project.sh" "$project" acme
bash "$fixtures/make-specs.sh" "$project"
bash "$fixtures/make-feature.sh" "$project" wave-reports

# drop_section <file> <heading prefix>: removes the `## ` section whose heading starts so, up to
# the next `## ` or `# ` heading.
drop_section() {
  HEADING="$2" awk '
    skip && /^##? / { skip = 0 }
    index($0, ENVIRON["HEADING"]) == 1 { skip = 1 }
    !skip
  ' "$1" > "$1.tmp"
  mv "$1.tmp" "$1"
}

# P0b's red run (09:09Z) and P1b's late one (09:48Z) are gone from every copy of the reports.
for file in "$reports/P0b.md" "$reports/P1b.md" "$dir/s1-wave-reports.md"; do
  drop_section "$file" "## Red run (09:09Z"
  drop_section "$file" "## Red run (09:48Z"
done

# Neither wave report shows test_quoting.py red.
waves="$dir/s1-wave-reports.md"
sed -e "s/P0b red as expected (No module named 'quoting'); /P0b wrote test_quoting.py; /" \
    -e "s/suite python -m pytest: 2 errors (P0a's and P0b's tests, expected red until W1)/suite python -m pytest: 1 error (P0a's test_export_rows.py, expected red until W1)/" \
    -e "s/; test_quoting.py: No module named 'quoting'; /; /" \
    -e "s/test_export_rows.py and test_quoting.py, red at W0 and again before dispatch (No module named 'export'; No module named 'quoting')/test_export_rows.py, red at W0 and again before dispatch (No module named 'export')/" \
    "$waves" > "$waves.tmp"
mv "$waves.tmp" "$waves"

if grep -n "No module named 'quoting'" "$waves" "$reports/P0b.md" "$reports/P1b.md"; then
  echo "scaffold: a red run of test_quoting.py is still in the reports" >&2
  exit 1
fi

git -C "$specs" add "$feature"
git -C "$specs" commit -q --amend --no-edit
git -C "$specs" push -q -f origin main
