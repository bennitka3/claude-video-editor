# claude-video-editor

ben's video studio. Claude makes videos here for two audiences: ben's **production team** and ben's
**YouTube channel**. ben is an experienced editor (Premiere Pro), so treat their notes as direction from an
editor: precise timing, pacing and style feedback. Keep explanations plain; ben is not an engineer.

## Tools

- **HyperFrames, open source** (github.com/heygen-com/hyperframes). Claude writes each video as HTML and renders it
  locally with `npx hyperframes`: no account, no watermark. The `hyperframes*` skills are the reference; read
  `/hyperframes` first for any video request.
- If the skills or CLI are missing (no setup script ran), run `npm install -g hyperframes@latest && hyperframes skills update`.
- **Do not use the HeyGen HyperFrames connector** unless ben asks for a HeyGen-hosted project. It needs a HeyGen
  plan, and the free tier watermarks exports.
- GSAP: if `cdn.jsdelivr.net` is blocked for the renderer, copy `gsap.min.js` into the project
  (`/opt/hf-vendor/node_modules/gsap/dist/` after the setup script, otherwise `npm i gsap@3.14.2`) and load it locally.
- Don't send `hyperframes feedback` reports unless ben says so; they post publicly.

## Layout

```
styles/<style>/frame.md      # one visual style per folder; HyperFrames reads frame.md as the brand spec
.claude/skills/<name>/       # ben's own video skills, built on top of HyperFrames
templates/<name>/            # finished compositions worth reusing as a starting point
projects/<name>/             # scratch build folder, git-ignored; project files are kept in the shared project folder
setup/cloud-setup.sh         # the project cloud environment's setup script
```

## How a video gets made

1. Ask which style if ben didn't say. Copy `styles/<style>/frame.md` into the project folder as `frame.md`.
2. Build in `projects/<short-name>/`. Start from a template when one fits.
3. Run `npx hyperframes check` until it passes, look at snapshots, then render.
4. Deliver the render through `/mnt/project-files/videos/<short-name>/` so ben can open it from the thread.
5. **Project files never go in git** (ben, 2026-10-13). Compositions, edit scripts, cut lists and graphics source
   are kept in the shared project folder at `/mnt/project-files/projects/<short-name>/`, where every cloud thread
   can read them for revisions. To revise, copy that folder into `projects/<short-name>/`, edit, and copy the
   changed source back. Snapshots, renders and footage are not kept there; they are scratch.
   Edits done on ben's Mac keep their project files next to the output there, and the thread copies the source
   files (not footage or renders) into the shared project folder when the edit is done.
6. **Say what was saved and where.** Several people may use this project. Whenever Claude saves project files
   (shared project folder) or commits anything to the repo (styles, skills, templates), the reply that reports it
   lists the folder and files saved, plus the branch and a commit or PR link for the repo. Never save something
   without saying so; if a file might be private (client material, people's faces, unreleased work), ask first.

Deliverable defaults (ben can override):

| For | Format |
|---|---|
| Team update | 1920×1080 MP4, 30 fps |
| YouTube | 1920×1080 (or 3840×2160 if asked) MP4 |
| YouTube Shorts / social | 1080×1920 MP4 |
| Overlay for Premiere (lower third, title, end card) | transparent ProRes 4444 MOV, background unset |

## Cloud environment (decided 2026-10-13)

For now the project uses ben's existing full-access cloud environment, with no video-specific one. HyperFrames
installs on demand (`make-video` step 1), which costs a minute or so per thread. `setup/cloud-setup.sh` is ready
for when a dedicated environment is worth it.

**Flag it to ben** (once, in one line) the first time any of these comes up, and suggest creating a separate
"Video Studio" cloud environment with that script plus the new need:

- A heavy tool every thread would re-download: a speech model for captions or transcription (~0.5 GB),
  ben's style fonts, LUTs, yt-dlp, Python libraries.
- An API key for a paid service (voiceover, music, HeyGen). Keep it in the video environment only, never in the
  repo; on Pro/Max plans it can be a network secret that Claude never sees.
- A need to pin the HyperFrames version so templates keep rendering the same across a series.
- Video setup that would slow down or clutter ben's other projects if it lived in the shared environment.

Don't create or change environments yourself; ben does that in Project settings.

## Footage and Premiere

- Raw footage never goes in git. Work from a folder on ben's computer (device folder tools) or Google Drive.
- From ben's phone (no Mac): he shares a Drive link set to "Anyone with the link"; follow the `drive-footage` skill.
- HyperFrames can't open Premiere projects. The bridge is exporting overlays as transparent MOVs for ben's
  timeline. A `.prproj` is gzipped XML, so reading markers or cut timings from one is possible but untested.

## Styles and skills

- A new style starts as `styles/<name>/frame.md` (YAML frontmatter tokens + prose rules; see HyperFrames'
  `hyperframes-creative/references/design-spec.md`). Quote its colors and fonts exactly.
- ben's own skills live in `.claude/skills/`. Each keeps a `## Status` note at the end. A skill only moves to the
  account-wide repo (`bennitka3/claude-skills`) if ben asks.
- Never change a style or skill's behavior without ben's OK. Back suggestions with what you checked; if ben's
  choice differs, say so once, then follow it.
