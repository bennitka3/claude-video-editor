"""Map a Premiere Pro keyboard shortcut list (copied as text from Premiere's Keyboard Shortcuts
dialog) onto FilmCraft command ids and write a FilmCraft keyboard shortcuts preset.

usage: python3 premiere_to_filmcraft_shortcuts.py <premiere.txt> <filmcraft_commands.json> <out_preset.json> <report.json>

filmcraft_commands.json is `shortcuts.list platform=mac` from the running FilmCraft app (not the
headless CLI, which lacks the UI commands) with the "Premiere Pro Compatible" preset loaded.
"""
import json
import re
import sys

PANELS = {
    "Timeline Panel": "Timeline", "Program Monitor Panel": "Program", "Source Monitor Panel": "Source",
    "Project Panel": "Project", "Effect Controls Panel": "Effect Controls", "Effects Panel": "Effects",
    "History Panel": "History", "Markers Panel": "Markers", "Media Browser Panel": "Media Browser",
    "Metadata Panel": "Metadata", "Audio Track Mixer Panel": "Audio Track Mixer",
    "Audio Clip Mixer Panel": "Audio Clip Mixer", "Text Panel": "Text", "Properties Panel": "Properties",
    "Lumetri Color Panel": "Lumetri Color",
}
GLYPHS = {"⌘": "Cmd", "⌥": "Alt", "⇧": "Shift", "⌃": "Ctrl"}
KEYNAMES = {"forward delete": "Delete", "delete": "Backspace", "return": "Enter", "page up": "PageUp",
            "page down": "PageDown", "space": "Space", "tab": "Tab"}


def conv_key(k):
    """Premiere's text (⇧+⌘+K, Forward Delete, 1 (Num)) → FilmCraft canonical, or None if unsupported."""
    k = k.strip()
    if "(Num)" in k:
        return None  # FilmCraft does not tell numeric-keypad keys from the main row
    parts = k.split("+") if k not in ("+",) else [k]
    mods, key = [], parts[-1].strip()
    for p in parts[:-1]:
        mods.append(GLYPHS.get(p.strip(), p.strip()))
    key = KEYNAMES.get(key.lower(), key)
    if len(key) == 1:
        key = key.upper()
    order = ["Cmd", "Ctrl", "Alt", "Shift"]
    mods = sorted(set(mods), key=order.index)
    return "+".join(mods + [key])


def parse(path):
    rows, stack = [], []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        depth = len(line) - len(line.lstrip("\t"))
        fields = line.lstrip("\t").split("\t")
        label = fields[0].strip()
        keys = fields[1].strip() if len(fields) > 1 else ""
        stack = stack[:depth] + [label]
        rows.append({"path": stack[:-1], "label": label, "raw": keys, "depth": depth})
    # an entry with children is a menu, not a command
    out = []
    for i, r in enumerate(rows):
        nxt = rows[i + 1] if i + 1 < len(rows) else None
        if nxt and nxt["depth"] > r["depth"]:
            continue
        if not r["path"]:
            continue
        root, rest = r["path"][0], r["path"][1:]
        if root == "Panels":
            scope = PANELS.get(rest[0], "?" + rest[0]) if rest else None
            rest = [p for p in rest[1:] if not p.endswith("Panel Menu")]
        else:
            scope = None
        out.append({"scope": scope, "path": rest, "label": r["label"],
                    "raw": r["raw"], "keys": [k for k in (s.strip() for s in r["raw"].split(", ")) if k]})
    return out


def norm(s):
    s = s.lower().replace("…", "").replace("...", "").replace("&", "and")
    s = re.sub(r"\b1\b", "one", s)
    s = re.sub(r"[^a-z0-9%/ ]+", " ", s)
    return " ".join(s.split())


def words(s):
    return set(norm(s).split()) - {"the", "to", "a", "of", "for", "on", "in"}


# Premiere names that FilmCraft words differently. Checked by hand against the command list.
MANUAL = {
    ("Application", "Play-Stop Toggle"): "playback.toggle",
    ("Application", "Step Back Many Frames - Units"): "playhead.stepBack5",
    ("Application", "Step Forward Many Frames - Units"): "playhead.stepForward5",
    ("Application", "Go to Sequence-Clip Start"): "playhead.start",
    ("Application", "Go to Sequence-Clip End"): "playhead.end",
    ("Application", "Window ▸ Projects"): "window.panel.Project",
    ("Application", "Window ▸ Timelines"): "window.panel.Timeline",
    ("History", "Step Backward"): "edit.undo",
    ("History", "Step Forward"): "edit.redo",
    ("Metadata", "Play"): "playback.toggle",
    ("Project", "Delete"): "project.delete",
    # Premiere's Project panel Zoom In / Out resize the thumbnails
    ("Project", "Zoom In"): "projectPanel.thumbnailLarger",
    ("Project", "Zoom Out"): "projectPanel.thumbnailSmaller",
    ("Application", "File ▸ Export ▸ Media..."): "mode.export",
    # Premiere's Workspace 1-9 are the first nine workspaces; FilmCraft's Premiere preset keys them in its own order
    **{("Application", "Workspace %d" % i): "window.workspace." + w for i, w in enumerate(
        ["editing", "assembly", "color", "effects", "audio", "captionsandgraphics", "learning", "review", "allpanels"], 1)},
}
# Premiere's app-menu Settings live under Edit > Preferences in FilmCraft
PATH_ALIAS = {("premiere pro", "settings"): ["edit", "preferences"]}


def main():
    ben = parse(sys.argv[1])
    fc = json.load(open(sys.argv[2]))
    ids = {c["id"]: c for c in fc}

    PANEL_PREFIX = {"textPanel.": "Text", "projectPanel.": "Project", "mediaBrowser.": "Media Browser"}

    def fits_scope(c, scope):
        for pre, panel in PANEL_PREFIX.items():
            if c["id"].startswith(pre):
                return scope == panel
        return True

    def candidates(e):
        nl = norm(e["label"])
        same = [c for c in fc if norm(c["label"]) == nl and fits_scope(c, e["scope"])]
        if e["scope"]:
            # panel keys: the command FilmCraft's Premiere preset already puts on this key in this panel
            for k in filter(None, map(conv_key, e["keys"])):
                hit = {c["id"]: c for c in fc for s in c["shortcuts"] if s["keys"] == k and s["panel"] == e["scope"]}
                hit = [c for c in hit.values() if c in same or len(words(c["label"]) & words(e["label"])) >= 1]
                if len(hit) == 1:
                    return hit, "panel key"
        if e["path"]:
            np = [norm(p) for p in e["path"]]
            np = PATH_ALIAS.get(tuple(np), np)
            exact = [c for c in same if [norm(m) for m in c["menu"]] == np]
            if exact:
                return exact, "menu+label"
            tail = [c for c in same if c["menu"] and norm(c["menu"][-1]) == np[-1]]
            if len(tail) == 1:
                return tail, "menu tail+label"
        # a menu command only matches a FilmCraft command with no menu, or one in the same menu
        nomenu = [c for c in same if not c["menu"]]
        if len(nomenu) == 1:
            return nomenu, "label"
        if len(same) == 1 and not e["path"]:
            return same, "label"
        # key anchor: FilmCraft's Premiere preset puts this Premiere key on exactly one command
        for k in filter(None, map(conv_key, e["keys"])):
            hit = [c for c in fc for s in c["shortcuts"] if s["keys"] == k and s["panel"] == e["scope"]]
            hit = [c for c in hit if len(words(c["label"]) & words(e["label"])) >= max(1, len(words(e["label"])) // 2)]
            if len(hit) == 1:
                return hit, "key+similar label"
        return [], None

    matched, unmatched, unsupported = [], [], []
    for e in ben:
        if e["scope"] and e["scope"].startswith("?"):
            unmatched.append({**e, "why": "FilmCraft has no %s" % e["scope"][1:]})
            continue
        key = (e["scope"] or "Application", e["label"])
        full = (e["scope"] or "Application", " ▸ ".join(e["path"] + [e["label"]]))
        if full in MANUAL or (key in MANUAL and not e["path"]) or (key in MANUAL and e["scope"]):
            cs, how = [ids[MANUAL.get(full) or MANUAL[key]]], "manual"
        else:
            cs, how = candidates(e)
        if not cs:
            unmatched.append({**e, "why": "no FilmCraft command"})
            continue
        keys = []
        for k in e["keys"]:
            ck = conv_key(k)
            if ck is None:
                unsupported.append({**e, "key": k, "why": "numeric keypad keys are not supported"})
            else:
                keys.append(ck)
        for c in cs:
            matched.append({"premiere": " ▸ ".join(e["path"] + [e["label"]]), "scope": e["scope"],
                            "id": c["id"], "fc_label": c["label"], "how": how, "keys": keys, "raw": e["raw"]})

    # start from FilmCraft's Premiere Pro Compatible preset
    bindings = {(c["id"], s["panel"], s["keys"]) for c in fc for s in c["shortcuts"]}
    owned = {}  # (scope, key) -> ids ben puts there
    for m in matched:
        bindings = {b for b in bindings if not (b[0] == m["id"] and b[1] == m["scope"])}
    for m in matched:
        for k in m["keys"]:
            bindings.add((m["id"], m["scope"], k))
            owned.setdefault((m["scope"], k), set()).add(m["id"])
    displaced = []
    for (scope, k), mine in owned.items():
        for b in list(bindings):
            if b[1] == scope and b[2] == k and b[0] not in mine:
                bindings.discard(b)
                displaced.append({"id": b[0], "label": ids[b[0]]["label"], "keys": k, "panel": scope,
                                  "now_on": sorted(mine)})

    # Premiere's Close (⌘W) closes whatever the focused panel shows; in the Timeline that is the
    # sequence. FilmCraft's Premiere preset has both commands on ⌘W there; keep Close Sequence.
    if ("file.close", None, "Cmd+W") in bindings:
        bindings.discard(("file.close", "Timeline", "Cmd+W"))
        bindings.add(("sequence.close", "Timeline", "Cmd+W"))
    preset = {"format": "filmcraft-keyboard-shortcuts", "version": 1, "name": "ben (from Premiere)",
              "platform": "mac", "modified": False,
              "bindings": [dict(command=i, keys=k, **({"panel": p} if p else {}))
                           for i, p, k in sorted(bindings, key=lambda b: (b[1] or "", b[0], b[2]))]}
    json.dump(preset, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
    report = {"matched": matched, "unmatched": unmatched, "unsupported": unsupported, "displaced": displaced}
    json.dump(report, open(sys.argv[4], "w"), indent=1, ensure_ascii=False)
    with_keys = [u for u in unmatched if u["keys"]]
    print("ben entries:", len(ben), "| matched:", len(matched), "| unmatched:", len(unmatched),
          "(with a key: %d)" % len(with_keys), "| unsupported keys:", len(unsupported),
          "| displaced FilmCraft defaults:", len(displaced), "| bindings:", len(preset["bindings"]))


if __name__ == "__main__":
    main()
