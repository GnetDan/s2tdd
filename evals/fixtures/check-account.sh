#!/usr/bin/env bash
# check-account.sh <account>
#
# For a case whose Given is "a repository the user owns": first-run setup takes the user's
# account from `gh api user --jq .login` before `git config github.user`, so the fixture's
# local github.user only counts when gh does not answer. Exits 1 when gh answers with another
# account (ignoring case), since setup would then treat the fixture as foreign; exits 0 when gh
# is missing, signed out or answers <account>. Never prints the login gh answered with.
set -euo pipefail

[ "$#" -eq 1 ] && [ -n "$1" ] || { echo "usage: check-account.sh <account>" >&2; exit 2; }
account=$1

command -v gh > /dev/null 2>&1 || exit 0
login=$(gh api user --jq .login 2> /dev/null) || exit 0
[ -n "$login" ] || exit 0

if [ "$(printf '%s' "$login" | tr '[:upper:]' '[:lower:]')" != \
     "$(printf '%s' "$account" | tr '[:upper:]' '[:lower:]')" ]; then
  cat >&2 <<MSG
check-account.sh: gh is signed in as an account other than $account, and first-run setup asks
gh before git config github.user, so this case's repository would not count as the user's own.
Run the eval with gh signed out for the run: GH_CONFIG_DIR set to an empty directory, and
GH_TOKEN and GITHUB_TOKEN unset.
MSG
  exit 1
fi
