#!/usr/bin/env bash
# Download a Google Drive file that ben shared as "Anyone with the link".
# Usage: drive-download.sh <drive link or file id> [output folder]
# Prints the saved file's path. Fails if Drive sends back a web page instead of the file.
set -euo pipefail

link="${1:?usage: drive-download.sh <drive link or file id> [output folder]}"
out_dir="${2:-.}"

# Accept .../file/d/<id>/view, ...?id=<id>, or a bare id.
id=$(printf '%s' "$link" | sed -nE 's#.*/d/([A-Za-z0-9_-]+).*#\1#p; s#.*[?&]id=([A-Za-z0-9_-]+).*#\1#p' | head -1)
[ -n "$id" ] || id="$link"

mkdir -p "$out_dir"
tmp="$out_dir/.drive-$id.part"
headers="$out_dir/.drive-$id.headers"

# confirm=t skips Drive's "can't scan this file for viruses" page on files over ~100 MB.
type=$(curl -sSL --fail --retry 3 -D "$headers" -o "$tmp" -w '%{content_type}' \
  "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t")

if [[ "$type" == text/html* ]]; then
  rm -f "$tmp" "$headers"
  echo "Drive sent a web page, not the file. Ask ben to set sharing to 'Anyone with the link'." >&2
  exit 1
fi

name=$(grep -i '^content-disposition:' "$headers" | sed -nE 's/.*filename="([^"]+)".*/\1/p' | tail -1)
name="${name:-$id}"
name="${name//\//_}"
mv "$tmp" "$out_dir/$name"
rm -f "$headers"
echo "$out_dir/$name"
