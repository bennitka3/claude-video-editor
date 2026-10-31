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
   `bash setup/install-hyperframes.sh` from the claude-video-editor repo (pinned, security-scanned version; never `@latest`).
2. **Pin down the brief in one line:** audience (team or YouTube), length, format (see the table in the repo's
   `CLAUDE.md`), style. Pick sensible defaults for anything ben left out and say which ones you picked.
3. **Style.** Copy `styles/<style>/frame.md` (repo root) into the project as `frame.md`. No style named →
   `starter`, and say so.
4. **Build** in `projects/<short-name>/` (a git-ignored scratch folder) (`hyperframes init projects/<short-name> --non-interactive`, or copy a
   folder from `templates/`). Follow `/hyperframes-core`. Load GSAP from a local `gsap.min.js` if the CDN fails.
5. **Check.** `npx hyperframes check` must pass. Snapshot each scene's midpoint and look at the frames yourself.
6. **Preview first (480p).** Render with `--quality draft`, then shrink it:
   `ffmpeg -i draft.mp4 -vf scale=-2:480 -c:v libx264 -crf 23 -pix_fmt yuv420p -c:a aac -movflags +faststart preview-480p.mp4`.
   HyperFrames has no resolution flag, so this saves file size, not render time. Deliver it as a phone page
   (see **Phone preview page** below) with one short paragraph: what's in it, what defaults you picked, and what
   ben might want to change. Iterate on notes at 480p.
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

## Phone preview page

ben can't open MP4s attached in a thread from the mobile app. Publish an Artifact page instead: the MP4 as a
supporting file (`files`, 15 MB max per file), a `<video controls playsinline>` player, and a "Save video to
phone" button through the `downloads` capability (`capabilities: {downloads: true}`; fetch the MP4 as a blob,
then `downloads.save`). In the iPhone app that opens the share sheet, where Save Video puts it in Photos. Update the
same page for each new preview so the link stays the same. Example: the dog hype montage page from 2026-10-13.

## Status

- 2026-10-13: written from the first test video (skills-repo explainer); steps 4–7 worked in a cloud thread.
- 2026-10-13: ben asked for a 480p preview before every full-res render, delivered as a phone page.
- 2026-10-13: ben asked that users are always told which project files get saved (multiple users), and that
  project files stay out of git; they live in the shared project folder.
- Not yet tested as a skill from this repo, the transparent MOV export, or footage from ben's computer.
- 2026-10-25: points FilmCraft projects and shortcuts to the new `filmcraft` skill (ben asked for FilmCraft support).
