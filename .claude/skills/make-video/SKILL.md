---
name: make-video
description: ben's video workflow in this repo. Use for any request to make, edit or render a video, overlay or animation for ben's team or YouTube channel, before the hyperframes skills.
---

# Make a video (ben's way)

This wraps HyperFrames with ben's styles and delivery rules. HyperFrames' own skills (`/hyperframes`,
`/hyperframes-core`, `/hyperframes-cli`) say how to build a composition; this skill says what ben wants.

1. **Check the tools.** If `hyperframes --version` fails or the `hyperframes` skills aren't listed, run
   `npm install -g hyperframes@latest && hyperframes skills update`.
2. **Pin down the brief in one line:** audience (team or YouTube), length, format (see the table in the repo's
   `CLAUDE.md`), style. Pick sensible defaults for anything ben left out and say which ones you picked.
3. **Style.** Copy `styles/<style>/frame.md` (repo root) into the project as `frame.md`. No style named →
   `starter`, and say so.
4. **Build** in `projects/<short-name>/` (`hyperframes init projects/<short-name> --non-interactive`, or copy a
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
8. **Save.** When ben is happy, commit the project source (renders are git-ignored). Then tell the user what was
   saved: the folder and files, the branch, and a link to the commit or PR. Other people may use this repo, so
   nothing gets committed silently, and anything that might be private gets asked about first. If it's worth
   reusing, offer to copy it into `templates/`.

## Phone preview page

ben can't open MP4s attached in a thread from the mobile app. Publish an Artifact page instead: the MP4 as a
supporting file (`files`, 15 MB max per file), a `<video controls playsinline>` player, and a "Save video to
phone" button through the `downloads` capability (`capabilities: {downloads: true}`; fetch the MP4 as a blob,
then `downloads.save`). In the iPhone app that opens the share sheet, where Save Video puts it in Photos. Update the
same page for each new preview so the link stays the same. Example: the dog hype montage page from 2026-10-13.

## Status

- 2026-10-13: written from the first test video (skills-repo explainer); steps 4–7 worked in a cloud thread.
- 2026-10-13: ben asked for a 480p preview before every full-res render, delivered as a phone page.
- 2026-10-13: ben asked that users are always told which project files get saved to the repo (multiple users).
- Not yet tested as a skill from this repo, the transparent MOV export, or footage from ben's computer.
