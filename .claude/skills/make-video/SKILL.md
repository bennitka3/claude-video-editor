---
name: make-video
description: ben's video workflow in this repo. Use for any request to make, edit or render a video, overlay or animation for ben's team or YouTube channel, before the hyperframes skills.
---

# Make a video (ben's way)

This wraps HyperFrames with ben's styles and delivery rules. HyperFrames' own skills (`/hyperframes`,
`/hyperframes-core`, `/hyperframes-cli`) say how to build a composition; this skill says what ben wants.
For a FilmCraft project (`.fcproj`) or FilmCraft shortcuts, use the `filmcraft` skill; the preview and
save rules below still apply.

1. **Check the tools.** If `hyperframes --version` fails or the `hyperframes` skills aren't listed, run
   `npm install -g hyperframes@latest && hyperframes skills update`.
2. **Pin down the brief in one line:** audience (team or YouTube), length, format (see the table in the repo's
   `CLAUDE.md`), style. Pick sensible defaults for anything ben left out and say which ones you picked.
3. **Style.** Copy `styles/<style>/frame.md` (repo root) into the project as `frame.md`. No style named →
   `starter`, and say so.
4. **Build** in `projects/<short-name>/` (a git-ignored scratch folder) (`hyperframes init projects/<short-name> --non-interactive`, or copy a
   folder from `templates/`). Follow `/hyperframes-core`. Load GSAP from a local `gsap.min.js` if the CDN fails.
5. **Check.** `npx hyperframes check` must pass. Snapshot each scene's midpoint and look at the frames yourself.
6. **Preview first, in the review room.** Render with `--quality draft`, then shrink it to a small review copy
   (240p unless ben asks otherwise; it keeps every cut under the 15 MB page limit):
   `ffmpeg -i draft.mp4 -vf scale=-2:240 -c:v libx264 -crf 26 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart <cut>-240p.mp4`.
   HyperFrames has no resolution flag, so this saves file size, not render time. Post it in the video's
   **review room** (below) with one short paragraph: what's in it, what defaults you picked, and what ben might
   want to change. Iterate on notes there.
7. **Full render, only after ben approves the preview.** Same composition, nothing else changed, with
   `--quality delivery` (a Premiere overlay is a transparent ProRes 4444 MOV). Copy it to
   `/mnt/project-files/videos/<short-name>/` and attach it. Over ~15 MB it won't fit on the page; say so and
   link the file (or R2 once it's set up).
8. **Save.** Project files never go in git. Copy the source (HTML, scripts, cut lists, `frame.md`; no snapshots,
   renders or footage) to `/mnt/project-files/projects/<short-name>/` so later threads can revise it, and update it
   after every revision. Then tell the user what was saved and where. Other people may use this project, so
   nothing gets saved silently, and anything that might be private gets asked about first. If it's worth reusing
   as a starting point, offer to copy it into `templates/` (that one does go in the repo, after ben's OK).
   To revise an existing video, start by copying its folder from `/mnt/project-files/projects/` into `projects/`.
   No `/mnt/project-files/` (not running in a Claude Project)? See "Where the shared project folder is" in `CLAUDE.md`.

## Review room

One Artifact page per video where ben watches each cut and leaves notes pinned to timecodes, so he never types
timecodes in chat. Template: `templates/review-room/index.html` (repo root). Same page, same link, for every cut
of that video.

- **First cut.** Copy the template to the scratchpad and fill `{{TITLE}}` (the video's title) and `{{CUTS}}`, a JSON
  list of `{id, video, label, tab?}`: `id` a short cut id (`v1`, `60s-v1`), `video` the mp4's file name, `label` e.g.
  `60 s cut · v1 · 240p review copy`. Two or more entries show tabs, for A/B versions of the same cut.
  Publish it with the mp4 in `files` and `capabilities: {db: {}, user: {scopes: ["profile"]}}` (load the
  `artifact-capabilities` skill first). Put the link in the reply and in project memory.
- **Reading notes.** When ben says his notes are in, read them with `ArtifactData` `list` on collection `notes`
  (fields: `cut`, `t` in seconds on that cut's timeline, `text`, `status` `open`/`done`, `reply`). Work only on
  notes for the current `cut`. `t` is on the old cut's timeline, so map it back to source time through the EDL.
- **Answering notes.** After each change, write back to the note (`update` with `if_version`): `reply` says in one
  line what changed, or why not, and `status: "done"`. ben sees the reply under his note. Questions go in `reply`
  too, with `status` left `open`.
- **Next cut.** New cut id(s) in `{{CUTS}}`, new mp4(s), republish the same file path so the link stays the same. Notes on
  earlier cuts stay visible (collapsed) with your replies.
- **Phone.** The page plays on the iPhone app. If ben wants the file on his phone, add a "Save video" button
  through the `downloads` capability (fetch the mp4 as a blob, then `downloads.save`; opens the share sheet).

## Status

- 2026-10-13: written from the first test video (skills-repo explainer); steps 4–7 worked in a cloud thread.
- 2026-10-13: ben asked for a 480p preview before every full-res render, delivered as a phone page.
- 2026-10-13: ben asked that users are always told which project files get saved (multiple users), and that
  project files stay out of git; they live in the shared project folder.
- Not yet tested as a skill from this repo, the transparent MOV export, or footage from ben's computer.
- 2026-10-25: points FilmCraft projects and shortcuts to the new `filmcraft` skill (ben asked for FilmCraft support).
- 2026-10-26: the review room replaces the phone preview page (ben asked for it on every edit). Tested on the
  "AI won't make your videos better" 60 s cut: ben left 7 notes, Claude read them, replied on each and posted
  v2 to the same page. Untested: more than one reviewer, the save-to-phone button inside the review room.
