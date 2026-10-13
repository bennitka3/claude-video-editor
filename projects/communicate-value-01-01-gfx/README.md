# 01_01 with ben's graphics

Lesson 01_01 of course 2511, re-cut with ben's own animated graphics from `01_SOURCE/04_GFX` (the eight `2511_01_01_*` files),
in two versions: `h/` (1920×1080) and `v/` (1080×1920). It reuses the cut from `../communicate-value-01-01`.

- `plan.json` says where each graphic sits on the cut and how it is retimed (frame holds so each bullet lands on its line).
  Change times there, then run `python3 build.py` and render each folder with `npx hyperframes render`.
- `build.py` links the footage, retimes each graphic with ffmpeg into `*/assets/retimed/`, and writes both `index.html` files.
- Footage and graphics live on ben's Mac (`/Volumes/madecraft/...`); they are not in git. A cloud thread can edit the plan and
  compositions, but rendering needs those files.

Horizontal: the talent sits in the window ben's graphics leave open (x 106–944). Between graphics the window centers over a
blurred copy of the footage; when a graphic comes in, the panel slides in from the right and the talent slides left.
Vertical: ben's vertical graphics are full-frame, so they cut in and out with short fades; the four "Ask Deeper Questions"
bullets come back one at a time, each on the line that introduces it.
