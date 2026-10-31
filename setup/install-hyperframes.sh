#!/bin/bash
# Install the HyperFrames CLI and its Claude skills at the ONE version that passed our security scan.
# The version lives in setup/hyperframes-version. Never install @latest: the weekly outside-skill scan
# (bennitka3/claude-skills system/skill-scan) checks each new release first and bumps that file only if it's clean
# (ben, 2026-10-31: "scan before installing; if something's wrong, pause and tell me first").
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
V="$(tr -d '[:space:]' < "$HERE/hyperframes-version")"
export DO_NOT_TRACK=1

npm install -g "hyperframes@$V"

# Skills from the same release tag. (`hyperframes skills update` would pull GitHub main, which is unreviewed.)
SRC="$(mktemp -d)"
git clone -q --depth 1 --branch "v$V" https://github.com/heygen-com/hyperframes.git "$SRC"
mkdir -p "$HOME/.claude/skills"
for d in "$SRC"/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  rm -rf "$HOME/.claude/skills/$(basename "$d")"
  cp -R "$d" "$HOME/.claude/skills/"
done
rm -rf "$SRC"
echo "HyperFrames $V installed (CLI + skills, reviewed release)"
