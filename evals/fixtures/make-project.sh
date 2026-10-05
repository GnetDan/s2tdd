#!/usr/bin/env bash
# make-project.sh <dir> <owner>
#
# Builds a fixture project in <dir>: a git repository on `main` with one commit and a bare
# remote standing in for GitHub, at <dir>/../remotes/github.com/<owner>/<name>.git. The path
# ends host/owner/name, so first-run setup reads <owner> as the segment after the host, as it
# does in an https or ssh URL. <owner> is also the repository's local user name, so a run that
# commits shows the same owner as the remote.
# Names are neutral (acme, acme-notes, ...): never pass a real project or person's name.
set -euo pipefail

usage() {
  echo "usage: make-project.sh <dir> <owner>" >&2
  exit 2
}

[ "$#" -eq 2 ] || usage
dir=$1
owner=$2
[ -n "$dir" ] && [ -n "$owner" ] || usage

mkdir -p "$dir"
project=$(cd "$dir" && pwd)
name=$(basename "$project")
remotes="$(dirname "$project")/remotes/github.com/$owner"
remote="$remotes/$name.git"

mkdir -p "$remotes"
git init -q --bare -b main "$remote"

git init -q -b main "$project"
git -C "$project" config user.name "$owner"
git -C "$project" config user.email "$owner@example.com"
git -C "$project" config commit.gpgsign false
git -C "$project" remote add origin "$remote"

printf '# %s\n\nA small notes app.\n' "$name" > "$project/README.md"
git -C "$project" add README.md
git -C "$project" commit -q -m "chore: initial commit"
git -C "$project" push -q -u origin main
git -C "$project" remote set-head origin main
