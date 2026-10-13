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
6. **Render** with `--quality delivery`. For a Premiere overlay, render a transparent ProRes 4444 MOV.
7. **Deliver.** Copy the render to `/mnt/project-files/videos/<short-name>/` and attach it to the reply.
   One short paragraph: what's in it, what defaults you picked, and what ben might want to change.
8. **Save.** When ben is happy, commit the project source (renders are git-ignored). If it's worth reusing, offer to
   copy it into `templates/`.

## Status

- 2026-10-13: written from the first test video (skills-repo explainer); steps 4–7 worked in a cloud thread.
- Not yet tested as a skill from this repo, the transparent MOV export, or footage from ben's computer.
