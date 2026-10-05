#!/usr/bin/env bash
# make-copy.sh <project-dir> <plugin-root>
#
# Copies <plugin-root>/skills/ into <project-dir>/.claude/skills/: the project-copy install, as
# the README's copy fallback describes it. Nothing is committed.
set -euo pipefail

usage() {
  echo "usage: make-copy.sh <project-dir> <plugin-root>" >&2
  exit 2
}

[ "$#" -eq 2 ] || usage
[ -d "$1" ] || { echo "make-copy.sh: $1 is not a directory" >&2; exit 1; }
[ -d "$2/skills" ] || { echo "make-copy.sh: $2/skills not found" >&2; exit 1; }
project=$(cd "$1" && pwd)
plugin=$(cd "$2" && pwd)

mkdir -p "$project/.claude/skills"
cp -R "$plugin/skills/." "$project/.claude/skills/"
