#!/bin/bash
# Install FilmCraft for Linux into /opt/filmcraft-<version> and print the CLI's path.
# usage: install-filmcraft.sh [version] [--gui]
#   version  e.g. 0.9.0; default: the latest GitHub release
#   --gui    also install the libraries the desktop app needs to run under Xvfb (for the full
#            command list, which the headless CLI lacks: see "Keyboard shortcuts" in SKILL.md)
set -euo pipefail
ver="" gui=0
for a in "$@"; do
  case "$a" in
    --gui) gui=1 ;;
    *) ver="${a#v}" ;;
  esac
done
if [ -z "$ver" ]; then
  # the releases/latest page redirects to .../tag/vX.Y.Z
  ver=$(curl -sSI https://github.com/storytold/filmcraft/releases/latest | tr -d '\r' | sed -n 's|^[Ll]ocation: .*/tag/v||p')
  [ -n "$ver" ] || ver=$(git ls-remote --tags https://github.com/storytold/filmcraft.git 'v*' | sed 's|.*refs/tags/v||' | grep -v '\^' | sort -V | tail -1)
fi
dir=/opt/filmcraft-$ver
if [ ! -x "$dir/bin/filmcraft-cli" ]; then
  tmp=$(mktemp -d)
  curl -sSfL -o "$tmp/fc.tgz" "https://github.com/storytold/filmcraft/releases/download/v$ver/filmcraft-$ver-linux-x86_64.tar.gz"
  mkdir -p "$dir" && tar xzf "$tmp/fc.tgz" -C "$dir" --strip-components=1 && rm -rf "$tmp"
fi
if [ "$gui" = 1 ] && ! ldconfig -p | grep -q libxkbcommon-x11; then
  (apt-get install -y -qq libxkbcommon-x11-0 libxcursor1 libxrandr2 libxi6 libgl1 libegl1 mesa-vulkan-drivers \
    || (apt-get update -qq && apt-get install -y -qq libxkbcommon-x11-0 libxcursor1 libxrandr2 libxi6 libgl1 libegl1 mesa-vulkan-drivers)) >/dev/null
fi
echo "$dir/bin/filmcraft-cli"
