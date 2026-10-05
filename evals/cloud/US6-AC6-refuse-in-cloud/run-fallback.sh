#!/usr/bin/env bash
# run-fallback.sh [plugin-root]
#
# US6-AC6's `claude -p` fallback (II-14 J-17; contracts/eval-suite.md): a case cannot set
# CLAUDE_CODE_REMOTE, so this builds the case's fixture and runs the command with the variable
# set. Exit 0 when the reply refuses and says to start it locally with `--cloud`.
set -euo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
plugin_root=$(cd "${1:-$here/../../..}" && pwd)

work=$(mktemp -d)
cd "$work"
bash "$here/scaffold.sh"

reply=$(CLAUDE_CODE_REMOTE=true claude -p "/s2tdd-pr-review 1" \
  --plugin-dir "$plugin_root" \
  --allowedTools "Read" "Glob" "Grep" "Skill" "Bash(printenv:*)" \
  --max-turns 6)
printf '%s\n' "$reply"

fail=0
printf '%s\n' "$reply" | grep -qiF -- 'start it locally with' || { echo "FAIL: no 'start it locally with'" >&2; fail=1; }
printf '%s\n' "$reply" | grep -qF -- '--cloud' || { echo "FAIL: no '--cloud'" >&2; fail=1; }
[ ! -e .review ] || { echo "FAIL: .review/ written" >&2; fail=1; }
[ "$fail" -eq 0 ] && echo "PASS: US6-AC6 refused in a cloud session"
exit "$fail"
