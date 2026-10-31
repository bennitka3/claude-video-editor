#!/bin/bash
# Setup script for the Video Studio project's cloud environment.
# Paste ONLY these two lines into the environment's "Setup script" box (one time). They fetch this repo and run
# this file, so version bumps land through a reviewed PR here with no re-paste:
#   git clone -q --depth 1 https://github.com/bennitka3/claude-video-editor /tmp/cve-setup
#   bash /tmp/cve-setup/setup/cloud-setup.sh
set -e
export DO_NOT_TRACK=1
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# HyperFrames CLI + skills, pinned to the security-scanned release (needs Node 22+, FFmpeg, git; preinstalled)
bash "$HERE/install-hyperframes.sh"

# GSAP, so compositions can use a local copy when the CDN is blocked
mkdir -p /opt/hf-vendor && cd /opt/hf-vendor && npm install --silent gsap@3.14.2
