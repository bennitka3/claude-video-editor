---
version: alpha
name: Starter — warm explainer
description: >
  Placeholder style taken from the first test video (the skills-repo explainer). Warm paper background,
  one terracotta accent, near-black ink, system sans for everything and monospace for file names and code.
  Replace or copy this when ben defines a real style.
unit: the frame — 1920×1080 primary; 1080×1920 for Shorts
principle: one accent per frame · generous space · content leads the eye

colors:
  ink: "#1F1D1A"
  ink-soft: "#5E5A54"
  paper: "#F5F0E8"
  glow: "#F3D9C9"
  card: "#FFFFFF"
  card-border: "#E4DDD2"
  accent: "#C25E3C"
  success: "#2F7A4A"

typography:
  kicker:   { fontFamily: "system sans", px: 34, weight: 600, tracking: "0.08em", upper: true, color: "accent" }
  headline: { fontFamily: "system sans", px: 96, weight: 700, tracking: "-0.03em", lineHeight: 1.05 }
  step:     { fontFamily: "system sans", px: 72, weight: 700, tracking: "-0.02em" }
  body:     { fontFamily: "system sans", px: 44, weight: 400, color: "ink-soft" }
  code:     { fontFamily: "monospace", px: 40, weight: 400 }

spacing:
  gap: "48px"
  card-pad: "44px 60px"
  radius-card: "28px"
  radius-badge: "50%"

components:
  step-badge:
    backgroundColor: "{colors.accent}"
    textColor: "#FFFFFF"
    size: "96px circle"
    description: "Numbered step marker next to the step title."
  card:
    backgroundColor: "{colors.card}"
    border: "3px solid {colors.card-border}"
    rounded: "{spacing.radius-card}"
    shadow: "0 24px 60px rgba(60,40,20,0.12)"
    description: "Holds the one detail of a step: a repo name, a file tree, a settings path."
---

## Overview

Calm, friendly explainer look. Each scene says one thing: a step title plus one card.

## Motion

Elements rise in about 40px with a fast ease-out (0.5s). Cards can overshoot slightly (back ease). Scenes
exit with a short fade up (0.3s). No spins, no bounces on text.

## Don'ts

- No second accent color in a frame.
- No pure black or pure white backgrounds.
- No gradient text.
