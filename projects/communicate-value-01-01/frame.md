---
version: alpha
name: Slice — dark feed
description: >
  Palette and type pulled from slice.app (2026-10-13). Near-black surfaces, warm orange as the one
  accent, mint and pink as the secondary card colors, Poppins for headlines and Open Sans for body.
unit: the frame — 1080×1920 (vertical feed, source is portrait iPhone footage)

colors:
  bg: "#141414"
  surface: "#1C1C1F"
  surface-2: "#2A2A2C"
  text: "#FFFFFF"
  text-soft: "#BBBBBB"
  accent: "#F79857"     # orange, the one accent
  mint: "#68D8B3"
  mint-ink: "#006E2C"
  pink: "#F3B2D9"
  pink-ink: "#DC4A9C"
  orange-ink: "#D21400"
  gradient: "linear-gradient(135deg, #F7D973 0%, #68EFC0 39%, #41B0F6 74%, #9B4FFE 100%)"

typography:
  kicker:   { fontFamily: "Poppins", px: 30, weight: 700, tracking: "0.12em", upper: true, color: "accent" }
  headline: { fontFamily: "Poppins", px: 68, weight: 700, tracking: "-0.02em", lineHeight: 1.08 }
  body:     { fontFamily: "Open Sans", px: 40, weight: 400, color: "text-soft" }
  chip:     { fontFamily: "Poppins", px: 36, weight: 700 }
---

## Rules

- Graphics live in the lower third over the presenter's shirt; the face is never covered.
- One orange accent per card. Mint = good / what to do, pink = what to avoid.
- Cards rise 40px with a fast ease-out; chips pop with a small overshoot. No spins.
- The camera is always moving: a slow push on every segment and a punch change on every cut.
- The Slice gradient appears only as the thin progress bar.
