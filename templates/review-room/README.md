# Review room

Artifact page where ben watches a cut and leaves notes pinned to timecodes; Claude reads them from the page's
database and answers under each note. How to use it: the **Review room** section of
`.claude/skills/make-video/SKILL.md`.

Placeholders in `index.html`: `{{TITLE}}` and `{{CUTS}}` (JSON list of `{id, video, label, tab?}`; two or more show tabs for A/B versions). Fill them with `sed` (or a short
script) in a scratch copy; never commit a filled copy or the video.

First used for "AI won't make your videos better" (60 s cut, 2026-10-26).
