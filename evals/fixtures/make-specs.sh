#!/usr/bin/env bash
# make-specs.sh <project-dir> [--no-remote]
#
# Makes <project-dir>/specs/ its own git repository on `main` with one commit and, unless
# --no-remote is given, its own bare remote at
# <project-dir>/../remotes/github.com/<owner>/<name>-specs.git
# (<owner> is the project's local user name, as make-project.sh set it). The project does not
# track specs/: it is excluded in the project's .git/info/exclude.
set -euo pipefail

usage() {
  echo "usage: make-specs.sh <project-dir> [--no-remote]" >&2
  exit 2
}

[ "$#" -ge 1 ] && [ "$#" -le 2 ] || usage
remote_wanted=1
if [ "$#" -eq 2 ]; then
  [ "$2" = "--no-remote" ] || usage
  remote_wanted=0
fi

[ -d "$1/.git" ] || { echo "make-specs.sh: $1 is not a git repository (run make-project.sh first)" >&2; exit 1; }
project=$(cd "$1" && pwd)
name=$(basename "$project")
owner=$(git -C "$project" config --get user.name)
specs="$project/specs"

mkdir -p "$specs"
git init -q -b main "$specs"
git -C "$specs" config user.name "$owner"
git -C "$specs" config user.email "$owner@example.com"
git -C "$specs" config commit.gpgsign false

exclude="$project/.git/info/exclude"
mkdir -p "$(dirname "$exclude")"
grep -qx 'specs/' "$exclude" 2>/dev/null || printf 'specs/\n' >> "$exclude"

: > "$specs/.gitkeep"
git -C "$specs" add .gitkeep
git -C "$specs" commit -q -m "chore: initial commit"

if [ "$remote_wanted" -eq 1 ]; then
  remote="$(dirname "$project")/remotes/github.com/$owner/$name-specs.git"
  mkdir -p "$(dirname "$remote")"
  git init -q --bare -b main "$remote"
  git -C "$specs" remote add origin "$remote"
  git -C "$specs" push -q -u origin main
  git -C "$specs" remote set-head origin main
fi
