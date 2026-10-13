---
name: drive-footage
description: Edit ben's footage from a Google Drive link in a cloud thread, with no Mac involved. Use when ben pastes a drive.google.com link or asks to edit a clip "from Drive" or "from my phone".
---

# Edit footage from Google Drive (no Mac needed)

ben can run edits from his phone: he shares a clip on Drive, Claude downloads it in the cloud, edits it with
ffmpeg (or uses it in a HyperFrames composition via `make-video`), and sends the result back in the thread.

1. **Get the link.** ben shares the file (or each file) as **"Anyone with the link"** and pastes the link.
   A private file comes back as a Google sign-in page, so the script stops and says so; ask ben to change
   the sharing. The Google Drive connector can find files but moves content through the conversation as text,
   so never use it to download video.
2. **Download** into scratch space, not the repo or the shared folder:
   `.claude/skills/drive-footage/drive-download.sh "<link>" <scratch>/footage` prints the saved path, with
   Drive's own filename. Measured ~34 MB/s (so ~30 s per GB); a session has roughly 30 GB of working disk.
3. **Inspect** with `ffprobe` (codec, size, frame rate, audio channels) and look at a contact sheet
   (`ffmpeg -i in -vf "fps=1/2,scale=320:-1,tile=4x2" -frames:v 1 sheet.png`) before cutting.
4. **Edit.** Keep the source frame rate and size unless ben says otherwise. Cuts at exact timecodes:
   `-ss`/`-to` after `-i` for frame accuracy. For something to watch on a phone: H.264 + AAC MP4,
   `-crf 18 -pix_fmt yuv420p -movflags +faststart`. For Premiere: match the source codec (ProRes stays ProRes).
5. **Deliver** to `/mnt/project-files/videos/<short-name>/` and attach it to the reply, saying what was cut and
   the file size. Results can't go back to Drive from the cloud yet (no Google login there).
6. **Clean up** the downloaded footage when done; raw footage never goes in git.

## Status

- 2026-10-13: tested end to end with a 31 MB ProRes Proxy clip (download 3.7 s, trim + fades + MP4 export 9 s),
  plus a 1 GB public file for speed. Private links fail cleanly.
- Not yet tested: ben's own files over 100 MB (Drive's virus-scan page; `confirm=t` should skip it), and
  delivering results larger than ~1.2 GB in the thread. Large results may need an upload-and-share service instead.
