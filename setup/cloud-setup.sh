#!/bin/bash
# Setup script for the Video Studio project's cloud environment.
# Paste this file's contents into the environment's "Setup script" box.
# It runs before Claude starts and is cached, so threads start with HyperFrames ready.
set -e
export DO_NOT_TRACK=1

# HyperFrames CLI (open source, renders HTML to MP4/MOV locally; needs Node 22+ and FFmpeg, both preinstalled)
npm install -g hyperframes@latest

# HyperFrames core skills -> ~/.claude/skills, which Claude loads in the session
hyperframes skills update

# GSAP, so compositions can use a local copy when the CDN is blocked
mkdir -p /opt/hf-vendor && cd /opt/hf-vendor && npm install --silent gsap@3.14.2
