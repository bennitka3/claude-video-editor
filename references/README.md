# Style references

Editing styles ben likes, broken down so Claude can borrow from them. One file per reference reel or video. A
reference is not a style yet: it records what someone else did. When ben wants "his version", the parts he picks
become a real style in `styles/<name>/frame.md` (and maybe a template), and the reference links to it.

## How a reference gets added

1. ben shares a link. Download it (`yt-dlp`; see `findings/instagram-cloud-access.md` in `bennitka3/research-testing`
   when Instagram blocks). If it won't download, ask ben to upload or screen-record it.
2. Watch it properly: 6 fps contact sheets, ffmpeg scene detection for cut times, whisper word timings for any
   voiceover, a loudness pass and a spectrogram for the sound.
3. Copy `_template.md` to `references/<slug>.md`. The slug names the look, not the creator (`paper-pixel-poem`).
   Fill every section in editor language (shots, holds, frames at 24/30 fps), with exact times and sampled colours.
4. Save the downloaded clip and a contact sheet to `/mnt/project-files/references/<slug>/` (never in git; it's
   someone else's video).
5. Add a row to the table below, and file the breakdown as a source in the research knowledge base
   (`bennitka3/research-testing`, `sources/style-ref-<slug>.md`) per the `ben-os` filing map.
6. Offer ben one opinionated idea for his version. Don't build it until he asks.

## Library

| Reference | Look in one line | Best for | ben's take | Became |
|---|---|---|---|---|
| [paper-pixel-poem](paper-pixel-poem.md) | Spoken one-line poem: lowercase type-on, pixel-art icons and gradient-mapped silhouettes, cutting between paper white, black and red | Short manifesto / channel opener, 15–25 s | Likes it (2026-10-26) | Not yet |

## Status

- 2026-10-26: library started with its first entry (ben: "I am going to start sharing editing styles I really like
  so you can create our versions of them or take elements from them to make my editing styles").
- Not yet used to build a video.
