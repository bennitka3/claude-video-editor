---
version: alpha
name: Edit Bay — moody talking head
description: >
  ben's first talking-head style, inspired by Olufemii (YouTube): a moody, practical-lit talking head with
  small bold captions and one highlighted keyword, handwritten callouts beside the head, and a dark branded card
  for chapters and b-roll. Built for "notes from the edit bay" posts (AI in a real production team).
unit: the frame — 1920×1080 primary; 1080×1920 for reels (captions move up, callouts go above the head)
principle: the face leads · one keyword per caption · handwriting only for the line worth remembering

colors:
  night: "#15192A"        # card background (chapters, b-roll slots, end card)
  night-grid: "rgba(244,239,230,0.05)"
  paper: "#F4EFE6"        # handwriting and card text
  tally: "#F2A93B"        # the one accent: caption keyword, underlines, b-roll slot outline
  caption: "#FFFFFF"
  shadow: "rgba(0,0,0,0.6)"

typography:
  caption:  { fontFamily: "Archivo Black", px: 34, upper: true, tracking: "0.03em", color: "caption" }
  keyword:  { inherits: caption, color: "tally" }
  hand:     { fontFamily: "Caveat", weight: 700, px: 96, color: "paper", rotate: "-3deg" }
  hand-big: { fontFamily: "Caveat", weight: 700, px: 150, color: "paper" }
  label:    { fontFamily: "IBM Plex Mono", px: 24, tracking: "0.14em", upper: true, color: "tally" }
  body:     { fontFamily: "Inter", px: 40, weight: 400, color: "paper" }

footage:
  grade: "slightly darker and warmer than camera, lower saturation, soft vignette (ffmpeg: eq contrast 1.07, brightness -0.045, saturation 0.88; warm colorbalance; vignette PI/4.2)"
  punch-in: "alternate 1.00× and 1.14× on every cut, anchored left-of-centre on the face, to hide jump cuts"
  audio: "loudness -16 LUFS, 20–30 ms fades at every cut"

components:
  caption:
    description: "3–4 words at a time, bottom centre 96 px up, one keyword in tally. Pops in 0.12 s, hard cut out."
  callout:
    description: "Handwritten line (Caveat) beside the head, over the background (right third). Writes on left to
      right in ~0.5 s, tally underline draws under it. Max one on screen; 2–5 s each; 1 per 10–20 s."
  chapter-card:
    description: "Full-frame night card with a faint grid. Mono label top-left ('02 · WHAT IT'S GOOD AT') and a big
      handwritten line. Voice keeps running under it. 2–4 s."
  b-roll-slot:
    description: "Night card with a 16:9 frame outlined in dashed tally, slot number, what to shoot, and its length.
      Replace the frame's contents (inset) or the whole card (full-frame) with real b-roll."
  end-card:
    description: "Night card, handwritten takeaway, mono sign-off. 2–3 s, silent."
---

## Overview

A quiet, expensive-looking talking head. The room does the work: darker, warmer, practicals and the vignette pull
the eye to the face. Graphics are sparse and personal (handwriting), never corporate.

## Motion

Captions pop with a tiny rise (8 px, 0.12 s). Handwriting writes on with a left-to-right wipe (0.5 s, power2.out)
and a slight settle; underlines draw after it. Cards fade in 0.25 s and the grid drifts slowly so they never sit
still. No spins, bounces, or whooshes.

## Don'ts

- No second accent colour. The keyword, underline and slot outline are all tally.
- No handwriting over the face, and never more than one callout at a time.
- No full-width caption bars; text shadow only.
- No stock "tech" b-roll (glowing brains, robots). Real screens and real footage from the team only.

## Inspiration

Olufemii, "5 Steps to Edits Everyone Wants to Copy" (youtube.com/watch?v=1T0n_DCX3GQ): moody bookshelf set, small
captions with one red keyword, handwritten words beside the head, purple chapter card. We kept the structure and
swapped in our own colour (tally amber on night blue) and fonts.
