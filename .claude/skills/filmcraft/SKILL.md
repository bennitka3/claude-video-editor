---
name: filmcraft
description: Read, edit and render FilmCraft projects (.fcproj, from the ArtCraft suite) and manage FilmCraft keyboard shortcuts. Use when ben mentions FilmCraft or ArtCraft, shares a .fcproj file, or asks to bring Premiere settings into FilmCraft.
---

# FilmCraft projects and shortcuts

FilmCraft (github.com/storytold/filmcraft, part of ArtCraft at getartcraft.com) is a free, open-source
Premiere Pro clone. ben uses it on his Mac. Every menu item is also a **command** with an id
(`sequence.addEdit`, `markers.add`…), and its command-line tool `filmcraft-cli` runs the same engine
headless on Linux, so a cloud thread can open, change and render a real project without the app.

## Set up (once per thread, about 30 s)

`.claude/skills/filmcraft/install-filmcraft.sh [version]` downloads the Linux release into
`/opt/filmcraft-<version>/` and prints the CLI's path. No version = the latest release. Use the version ben
runs (FilmCraft ▸ About) when it matters, because a project saved by a newer FilmCraft is refused by an
older one. Set `FILMCRAFT_DATA_DIR` to a scratch folder so the CLI's auto-saves stay out of the repo.

## The .fcproj file

UTF-8 JSON, written compact. Top level:
`{"format": "filmcraft.project", "schema_version": N, "generator": "FilmCraft 0.13.0", "project": {…}, "view": {…}}`.

- `project.items` maps an id to a bin item. `kind` is `Media` (media is a **path** in `kind.Media.media.File.path`,
  never embedded, plus `info` with size, frame rate and audio streams), `Sequence`, `Graphic` and others.
- A sequence (`kind.Sequence`) has `settings` (size, `frame_rate` as num/den), `video_tracks`, `audio_tracks`,
  `caption_tracks`, `markers`, `mark_in`/`mark_out`. Each track item has `item` (the media id), `start`,
  `duration`, `source_in`, `speed`, `effects` (Motion, Opacity, Lumetri… with keyframes) and `markers`.
- Times are **ticks: 254,016,000,000 per second** (Premiere's timebase). Most commands also take
  `seconds=`, `frame=` or `timecode=`.
- `view` is what was open (sequence tabs, zoom, playhead). It isn't part of the edit.
- FilmCraft migrates older schema versions on open and refuses newer ones.

Read it with the CLI rather than by hand: `filmcraft-cli --project P.fcproj inspect` (or `inspect sequence`)
prints the bins and the active sequence as readable JSON with frame counts. Use `python3 -c` on the
raw JSON only for things `inspect` leaves out.

## Edit and render (verified with FilmCraft 0.13.0 in a cloud thread)

- **Never overwrite ben's file.** Always `--save-as` a new version next to the copy you were given
  (`Cut v2.fcproj`), and tell him the name.
- One command: `filmcraft-cli --project in.fcproj --save-as out.fcproj exec sequence.addEdit seconds=3`.
  Many: write a `.jsonl` script, one `{"id": …, "params": {…}}` per line, then
  `filmcraft-cli --project in.fcproj --save-as out.fcproj run edit.jsonl`. Keep the script; it is the edit
  record, like a cut list.
- Find commands with `filmcraft-cli commands <word>` and `describe <id>` (labels match Premiere's menus).
- Render a frame to look at: `render --seconds 12 --out f.png --scale 0.5`.
  Export: `export out.mp4 --scale 0.25` for the 480p-ish preview (ben's preview-first rule in `make-video`),
  then the same project without `--scale` for full size. `export --list-presets` lists presets.
- **Media lives on ben's Mac**, so in the cloud it is offline: `exec media.findMissing` lists it, and export
  stops (exit 1) unless `--allow-offline`, which renders red "media not found" slates. To render for real,
  get the footage (Drive: `drive-footage` skill), then
  `exec media.autoRelink from=/Volumes/… to=<scratch folder>` (or `folder=<scratch>`) and save as a new
  version. The relinked copy has cloud paths, so ben keeps his own file; give him the edit script or the
  render, or relink back (`from=<scratch> to=/Volumes/…`) before handing over a project file.
- On ben's Mac (Remote Control session) the CLI is a separate download
  (`filmcraft-cli-<ver>-macos-universal.zip` on the GitHub release). With `--bridge` it can drive the open
  app (FilmCraft's `docs/control-protocol.md`), but ask ben first: he may be mid-edit.
- Interchange when ben needs Premiere: FilmCraft reads and writes FCPXML, Premiere XML, EDL, OTIO and AAF
  (`commands file.export`, `commands file.import`). It can't open `.prproj`.

## Keyboard shortcuts

FilmCraft's shortcuts are editable (⌥⌘K, or the `shortcuts.*` commands) and live in presets: JSON files
`{"format": "filmcraft-keyboard-shortcuts", "version": 1, "name", "platform": "mac", "bindings":
[{"command", "keys", "panel"?}]}` in `~/Library/Application Support/FilmCraft/Keyboard Shortcuts/`.
Keys use `Cmd`, `Ctrl` (the Mac Control key), `Alt`, `Shift`; `Backspace` is the Mac delete key and
`Delete` is forward delete. It can't import Premiere's `.kys`, but it ships a *Premiere Pro Compatible*
preset.

To carry ben's Premiere keys over:

1. ben copies his list from Premiere's Keyboard Shortcuts dialog as text and pastes it (tabs mark the menu
   levels; save it as a .txt).
2. The headless CLI lacks the app's own commands (tools, transport, panels), so get the full list from
   the desktop app under Xvfb: `install-filmcraft.sh <ver> --gui`, then with
   `FILMCRAFT_CONTROL_TOKEN=$(python3 -c 'import secrets;print(secrets.token_hex(32))')` exported,
   `xvfb-run -a filmcraft --control 9876 --empty --no-recover --graphics software &`, and through
   `filmcraft-cli --bridge 127.0.0.1:9876`: `exec shortcuts.loadPreset "name=Premiere Pro Compatible"`,
   then `exec shortcuts.list platform=mac > fc.json`.
3. `python3 premiere_to_filmcraft_shortcuts.py premiere.txt fc.json preset.json report.json` matches by
   menu and name, then by the key FilmCraft's Premiere preset uses, then a short hand-checked list.
   Read `report.json` (`unmatched`, `displaced`) before trusting it.
4. Check it in the cloud app: `exec shortcuts.import path=…` then `exec shortcuts.conflicts platform=mac`
   must list no conflicts.
5. ben imports `preset.json` himself (Keyboard Shortcuts ▸ Import…). Don't write into his Library folder.

ben's current preset and its report are in `/mnt/project-files/filmcraft/shortcuts/` (`README.md` lists
what had no FilmCraft equivalent). Rebuild it when FilmCraft adds commands; the source list is saved there.

## Status

- 2026-10-25: written. Reading, editing (`exec`, `run`, `--save-as`), relinking, frame render and export
  tested on FilmCraft 0.9.0 and 0.13.0 in a cloud thread with the demo project and a test clip.
  Shortcut preset for ben built and import-tested on 0.13.0 (594 Premiere commands matched, no conflicts).
  Not yet tested: one of ben's own .fcproj files, the CLI on his Mac, `--bridge` to his running app.
