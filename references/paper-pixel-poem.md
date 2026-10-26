---
slug: paper-pixel-poem
source: https://www.instagram.com/reel/DeKDmkmh_gM/
creator: "Jordan Watkins (@jordans.archivess)"
published: 2026-10-06
captured: 2026-10-26
length: "20.4 s"
format: "1440×1080 (4:3), 24 fps"
look: "Spoken one-line poem: lowercase type-on, pixel-art icons and gradient-mapped silhouettes, cutting between paper white, black and red."
best_for: "Short manifesto, channel opener or brand sting, 15–25 s, one sentence of VO."
ben_keeps: "Pacing, cuts on music beats, an SFX on every cut, speed-ramp motion (fast in, slow middle, fast out)."
clip: /mnt/project-files/references/paper-pixel-poem/
research_source: sources/style-ref-paper-pixel-poem.md (bennitka3/research-testing)
became: ""
---
# Paper & pixel poem

A 20-second piece built on one spoken sentence: "How do you communicate that you're going through a change? You
don't. You just show it through action, intention, curiosity, through one's own ability to love." Every word is
typed on screen as it's said, and each keyword gets its own object and its own hard cut. Caption: "Visual Test 01 -
Change (No AI used)"; the creator sells editing tools and a plugin from their bio. 488,590 likes when captured.

Why it works: the edit has one idea per beat and the picture changes exactly when a new idea arrives. It holds while a
line is spoken and cuts hard on the keywords; the phrases come from the voiceover, but the cuts themselves snap to the
music's eighth-note grid (measured below). The look
mixes three textures (paper, pixel art, glowing silhouette) but only one palette.

## Beat map

Cut times from ffmpeg scene detection, words from whisper word timings. 24 fps, so 1 frame ≈ 0.04 s.

| Time | Shot | Type / VO | Cut out |
|---|---|---|---|
| 0.00–0.08 | Red frame, giant black "how" stretched tall | VO starts: "How" | 2-frame flash, hard cut |
| 0.08–2.00 | Off-white paper. Big "how do you co…" glitches (pixelated letters, black redaction bar), then collapses to a small caption that types on word by word. Hand-drawn pen strokes draw on and scribble around words | "do you communicate that you're going through a change?" | 2-frame yellow flash with a yellow four-point star |
| 2.08–~3.9 | Paper with a dark vignette "spotlight"; a cyan/blue four-point star swings in from the left; small pixel icons (book, clapper, coin, camera) float. Full question sits as one line | **Silence 2.4–3.3** (near-total drop) then "you" highlights white | Blur/smear into dark |
| ~3.9–6.33 | Profile silhouette on black, gradient-mapped like a heat camera (orange to yellow). Text on the left with a type cursor. Background lifts from black to grey, silhouette goes dark on white | "You don't." / "you just show it" | Orange-to-black gradient bar wipe (5 frames), grey blur (2 frames) |
| 6.63–8.33 | White paper, pixel icons snap into a ring (record, camera, cat, coin, controller, cap, heart, cash, plant, clapper, skateboard). Ink blots and brush streaks fly through, sparks "burn" icons orange | "through" | Hard cut |
| 8.33–9.17 | Black. Pixel camera with a red star burst, word "action." with a block cursor | "action" | White slide: icons streak across (motion blur), ~17 frames |
| 9.87–10.54 | Black. Pixel book, red streak sweeps behind | "intention" | White slide, ~12 frames |
| 11.04–11.92 | Black. Pixel vinyl with red music notes popping on | "curiosity" | 1-frame grey negative flash of the icons |
| 11.96–13.79 | White. Icon ring spins, then scatters across the frame, icons go black like ink | (music) | Blur/smear into dark |
| 13.79–15.92 | Hand reaching up, same heat gradient on black, text split either side of it | "through one's own ability to" | Fast cuts begin |
| 15.92–17.25 | Six cuts in 1.3 s (6–10 frames each): heart on white, heart on vignette, camera on black, camera on red, book on red, vinyl on black. Letters L O V E spread across the frame, one more each cut | "love" | Hard cut |
| 17.25–20.40 | White paper, L O V E scattered, drifting and rotating, red hand-drawn loops scribble around them | Music tail only, quiet | End |

## Ingredients

- **Pacing and cut rhythm:** about 22 shots in 20.4 s (average 0.9 s), but it doesn't feel busy because it moves in
  phrases: holds of 1.5–2.5 s while a line is spoken, then a burst. "action / intention / curiosity" are one keyword
  per shot at about 1.2–1.4 s each. "love" is the climax: six cuts in 1.3 s. It opens with a 2-frame flash and ends on
  the longest hold (3.1 s) so the last word can breathe.
- **Transitions:** mostly hard cuts. Accents are 1–2 frame flash frames (red, yellow, a negative), short blur smears
  into dark scenes, one gradient bar wipe, and "slide" shots where the icon row whips across with motion blur. No
  dissolves.
- **Type:** small, bold, lowercase geometric sans (think Gilroy or General Sans; not identified), tight tracking,
  near-black on paper or white on black. Words type on in sync with the VO, often with a typewriter cursor. The
  only big type is the opening "how". Keywords end with a full stop ("action.").
- **Graphics:** a fixed cast of about 12 pixel-art icons that keep coming back (ring, row, scatter, single hero
  object). Hand-drawn pen strokes and loops that draw on, ink blots, brush streaks, four-point stars, small sparks.
  Everything moves with slight wobble, like stop-motion on paper.
- **Colour:** three backgrounds it cuts between: paper `#DBD9DC`, near-black `#141114`, signal red `#D61A18` (opening
  red `#B10E16`). People are gradient-mapped to orange `#DE6118` through yellow. One-off accents: yellow and cyan/blue
  stars. Film grain and a soft vignette on everything.
- **Sound:** soft, close, dry voiceover carries the edit. A light tonal music bed underneath, whoosh and hit
  transients on the cuts. The key move is the **silence after the question** (2.4–3.3 s, around −35 to −40 dB) before
  "you don't." The end is music only at about −30 dB for 3 s. Overall about −17 dB average, peaks −1.4 dB.

## What ben takes from it (measured 2026-10-26)

ben: "what I really like about this is the pacing, the cut to music beats, and the sound effects. I also like the
smoothness of each animation feeling like a speed ramp that transitions quickly and smoothly slows for the middle of
a segment. actual composition is exchangeable." So these four are the recipe; the pixel icons, paper and type are not.

- **Cuts on the music.** The bed is about 108 BPM (one beat ≈ 0.55 s, 13 frames at 24 fps). 16 of 22 cuts land within
  60 ms (about 1.5 frames) of an eighth note, on the beat or on the "and". Cuts placed at random would hit that only
  44% of the time, so it's deliberate, if not frame-perfect (librosa beat tracking; the tempo estimate could be off by
  a factor of two). Phrase lengths follow the VO; the exact cut frame snaps to the grid.
- **An SFX on every cut.** High-frequency energy (above 4 kHz) jumps 15–33 dB above the track's median at 13 of 15
  cuts checked, mostly within ±75 ms of the cut. Several peak 110–155 ms *after* the cut, which reads as a whoosh
  into the cut with its impact or tail just after. The biggest (+33 dB) is the gradient wipe at 6.3 s. Whispers in
  the VO also carry high frequencies, so treat these numbers as approximate.
- **Speed ramp inside every moving segment.** Measured as how much the picture changes per frame. Each moving
  segment is fast in the first third, slow in the middle, and speeds up again into the cut:

  | Segment | First third | Middle | Last third |
  |---|---|---|---|
  | Paper type-on (0.1–2.1 s) | 14.4 | 3.8 | 10.3 |
  | Icon ring (6.6–8.3 s) | 24.4 | 10.0 | 17.5 |
  | White slide 1 (9.2–9.9 s) | 15.9 | 8.0 | 13.9 |
  | White slide 2 (10.5–11.0 s) | 22.1 | 10.3 | 23.6 |
  | Ring scatter (12.0–13.8 s) | 20.2 | 7.6 | 10.0 |

  The shape: a hard ease-out of about 0.3–0.5 s into the shot (the icon ring drops from 35 to 7 over ~1 s), a slow
  drift through the middle, then an ease-in of about 0.3–0.5 s so the move is at full speed when it cuts. The next
  shot starts at that same speed, so the cut is hidden inside the motion (plus blur and the whoosh). The
  keyword holds ("action.", "intention.", "curiosity.", the hand) barely move (1–4) but still get a small kick in and
  out.
- **Recipe for our own builds:** in HyperFrames/GSAP, enter with `expo.out` (0.35–0.5 s), drift with a slow linear
  move, exit with `expo.in` (0.3–0.4 s) ending on the cut frame, and start the next shot moving at that same speed.
  Put cuts on the music's eighth notes and lay a whoosh ending on, or a hit starting at, each cut. In Premiere, this
  is Time Remapping speed ramps or Bezier keyframes on position/scale with steep handles, cut at peak speed.

## How we'd build it

- **HyperFrames can do most of it:** the paper/black/red frames, type-on synced to VO word timings (whisper gives
  them), the pixel icons moving as sprites, flash frames, the slide whips, the L O V E letter layout and the drifting
  end. Pen strokes are SVG paths drawn on with GSAP.
- **Footage work:** the heat-gradient silhouettes are filmed profile and hand shots, keyed, then gradient-mapped (in
  ffmpeg or Premiere/After Effects). Easy in the cloud with ffmpeg once we have the footage.
- **We'd need:** a VO line (ben's or recorded), a font pick (check `styles/` and ben's fonts), an icon set (our own;
  never reuse the creator's icons), a music bed and a few whoosh/hit SFX.

## ben's version (idea)

A 15-second 9:16 channel manifesto with the same structure (question, silence, "you don't", three keywords each on
its own object, one word spelled out across fast cuts), but with ben's real kit instead of pixel art: his camera,
slate, headphones and a Premiere timeline shot on his phone against white paper, and ben's own silhouette
gradient-mapped in a single brand colour. The pixel icons are this creator's signature; real objects make it his.

## ben's notes

- 2026-10-26: shared as the first style he "really likes" to build his editing styles from.
- 2026-10-26: likes the pacing, cuts on music beats, the sound effects and the speed-ramp feel of every move;
  the composition (icons, paper, type) is exchangeable. Measured in "What ben takes from it" above.
