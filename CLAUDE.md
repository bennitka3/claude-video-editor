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
references/<slug>.md         # breakdowns of editing styles ben likes (other people's videos); see references/README.md
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

**Where the shared project folder is.** Nothing needs to be mounted or set up. In a Claude Project (the
claude.ai Projects app), every thread gets the project's shared folder at `/mnt/project-files/` automatically; create
`projects/` and `videos/` inside it as needed. If `/mnt/project-files/` doesn't exist (a plain Claude Code session,
not a Project), there is no shared folder: say so once, keep the project files in `projects/<short-name>/` for this
session only, and offer to save the source files (small text files only, never video) to a `Claude video projects`
folder in Google Drive if the Drive connector is connected. Never fall back to committing them.

Deliverable defaults (ben can override):

| For | Format |
|---|---|
| Team update | 1920×1080 MP4, 30 fps |
| YouTube | 1920×1080 (or 3840×2160 if asked) MP4 |
| YouTube Shorts / social | 1080×1920 MP4 |
| Overlay for Premiere (lower third, title, end card) | transparent ProRes 4444 MOV, background unset |

## Cloud environment (decided 2026-10-13, updated 2026-10-25)

Video threads have so far run in ben's shared "Code Cloud 1" environment, which also holds the Cast project's
production keys. A "Video Editor" cloud environment exists (created 2026-10-13); the 2026-10-25 system review
proposes making it the no-secrets environment for video, research and skills, with `setup/cloud-setup.sh` plus
`pip install yt-dlp faster-whisper` as its setup script (item in `bennitka3/claude-skills` `system/BACKLOG.md`).
Until ben switches, HyperFrames installs on demand (`make-video` step 1), about a minute per thread.

Watching or transcribing a video someone links (reels, YouTube, a direct .mp4) is already covered by the
`social-intake` and `watch-video` skills in `bennitka3/claude-skills-testing`; attach that repo rather than
rebuilding it here.

**Flag it to ben** (once, in one line) the first time any of these comes up, and add it to that backlog item:

- A heavy tool every thread would re-download: ben's style fonts, LUTs, a bigger speech model, Python libraries.
- An API key for a paid service (voiceover, music, HeyGen). Keep it in the video environment only, never in the
  repo; on Pro/Max plans it can be a network secret that Claude never sees.
- A need to pin the HyperFrames version so templates keep rendering the same across a series.

Don't create or change environments yourself; ben does that in settings.

## Footage and Premiere

- Raw footage never goes in git. Work from a folder on ben's computer (device folder tools) or Google Drive.
- From ben's phone (no Mac): he shares a Drive link set to "Anyone with the link"; follow the `drive-footage` skill.
- HyperFrames can't open Premiere projects. The bridge is exporting overlays as transparent MOVs for ben's
  timeline. A `.prproj` is gzipped XML, so reading markers or cut timings from one is possible but untested.
- ben also edits in **FilmCraft** (open-source Premiere clone, ArtCraft suite). Its `.fcproj` projects are JSON and
  its CLI runs in the cloud, so Claude can read, edit and render them: see the `filmcraft` skill.

## Styles and skills

- When ben shares a video whose editing style he likes, add it to `references/` (steps in `references/README.md`).
  When he asks for a video "like" one of them, read that reference first. A reference becomes a style only when
  ben asks for his version.
- A new style starts as `styles/<name>/frame.md` (YAML frontmatter tokens + prose rules; see HyperFrames'
  `hyperframes-creative/references/design-spec.md`). Quote its colors and fonts exactly.
- ben's own skills live in `.claude/skills/`. Each keeps a `## Status` note at the end. A skill only moves to the
  account-wide repo (`bennitka3/claude-skills`) if ben asks.
- Never change a style or skill's behavior without ben's OK. Back suggestions with what you checked; if ben's
  choice differs, say so once, then follow it.
