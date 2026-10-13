#!/usr/bin/env python3
"""Build the horizontal (h/) and vertical (v/) HyperFrames projects for 01_01 with ben's 04_GFX graphics.

Reads plan.json, links the footage cut and graphic files into each project's assets/, pulls the
hold frames out of the graphics with ffmpeg, and writes h/index.html and v/index.html.
Run:  python3 build.py   then render each folder with hyperframes.
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))
DUR = plan["duration"]

H_WIN_L, H_WIN_W, H_WIN_CENTER = 106, 838, (1920 - 838) // 2  # the window ben's horizontal graphics leave open
PANEL_X = 944                                                   # where the opaque right panel starts
PANEL_COLOR = "#212121"
SLIDE_IN, SLIDE_OUT = 0.45, 0.4


def run(*cmd):
    subprocess.run(cmd, check=True)


def link(src, dst):
    if os.path.lexists(dst):
        os.remove(dst)
    os.symlink(src, dst)


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def cut_bounds():
    """Timeline times where the footage cut changes, from the kept ranges of 01_01.MOV."""
    ranges = json.load(open(os.path.join(HERE, plan["cut_ranges"])))
    t, out = 0.0, [0.0]
    for a, b in ranges:
        t += b - a
        out.append(round(t, 3))
    out[-1] = DUR
    return out


def poses(scale_lo, scale_hi, drift):
    """A punch change on every cut and a slow push inside each segment (same idea as the v1 edit)."""
    b = cut_bounds()
    out = []
    for i in range(len(b) - 1):
        tight = i % 2 == 1
        s0 = scale_hi if tight else scale_lo
        s1 = s0 + 0.05
        x0, x1 = (drift, -drift) if i % 3 == 0 else ((-drift, drift) if i % 3 == 1 else (0, 0))
        out.append([b[i], b[i + 1], round(s0, 3), round(s1, 3), x0, x1])
    return out


def pieces(p, file_dur):
    ps = p.get("pieces") or [[p["in"], 0, None]]
    res = []
    for i, (at, frm, to) in enumerate(ps):
        nxt = ps[i + 1][0] if i + 1 < len(ps) else p["out"]
        if to is None:
            to = min(file_dur - 0.05, frm + (nxt - at))
        play = to - frm
        if at + play < nxt - 0.02:  # stop just short of the next build so the held frame is clean
            play -= 0.07
        res.append({"at": at, "from": frm, "play": round(play, 3), "hold_until": nxt})
    return res


def build(orient):
    proj = os.path.join(HERE, orient)
    assets = os.path.join(proj, "assets")
    os.makedirs(assets, exist_ok=True)
    link(os.path.abspath(os.path.join(HERE, plan["cut_file"])), os.path.join(assets, "cut.mp4"))

    clips, js = [], []
    track = 10
    for p in plan[orient]:
        src = os.path.join(plan["gfx_dir"], p["file"])
        fdur = probe_duration(src)
        # Retime the graphic into one clip: play each piece, hold its last frame until the next piece (a frame hold).
        os.makedirs(os.path.join(assets, "retimed"), exist_ok=True)
        out_name = f"retimed/{orient}_{p['id']}.mov"
        parts, labels = [], []
        for k, pc in enumerate(pieces(p, fdur)):
            hold = max(0.0, pc["hold_until"] - (pc["at"] + pc["play"]))
            parts.append(f"[0:v]trim={pc['from']}:{pc['from'] + pc['play']:.3f},setpts=PTS-STARTPTS,fps=30,"
                         f"tpad=stop_mode=clone:stop_duration={hold:.3f}[p{k}]")
            labels.append(f"[p{k}]")
        graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=1:a=0[o]"
        codec = ["-c:v", "qtrle", "-pix_fmt", "argb"] if orient == "h" else ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p"]
        run("ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", graph, "-map", "[o]",
            "-t", f"{p['out'] - p['in']:.3f}", *codec, os.path.join(assets, out_name))
        inner = [f'<video id="{orient}-{p["id"]}" class="clip gf" src="assets/{out_name}" muted playsinline '
                 f'data-start="{p["in"]}" data-duration="{round(p["out"] - p["in"], 3)}" data-track-index="{track}"></video>']
        clips.append(f'<div class="gw" id="g-{p["id"]}">\n        ' + "\n        ".join(inner) + "\n      </div>")
        track += 1

        sel = f"#g-{p['id']}"
        if orient == "h":
            if p["in"] > 0:
                js.append(f'tl.fromTo("{sel}", {{x: {1920 - PANEL_X}}}, {{x: 0, duration: {SLIDE_IN}, ease: "power3.out"}}, {p["in"]});')
            if p["out"] < DUR:
                js.append(f'tl.to("{sel}", {{x: {1920 - PANEL_X}, duration: {SLIDE_OUT}, ease: "power2.in"}}, {round(p["out"] - SLIDE_OUT, 3)});')
        else:
            if p["in"] > 0:
                js.append(f'tl.fromTo("{sel}", {{opacity: 0, scale: 1.04}}, {{opacity: 1, scale: 1, duration: 0.3, ease: "power2.out"}}, {p["in"]});')
            if p["out"] < DUR:
                js.append(f'tl.to("{sel}", {{opacity: 0, duration: 0.25, ease: "power1.in"}}, {round(p["out"] - 0.25, 3)});')

    if orient == "h":
        # The talent window sits centered between graphics and slides into the graphics' window while one is up.
        spans = []
        for p in plan["h"]:
            if spans and p["in"] - spans[-1][1] < 1.5:
                spans[-1][1] = p["out"]
            else:
                spans.append([p["in"], p["out"]])
        for a, b in spans:
            if a > 0:
                js.append(f'tl.fromTo("#win", {{x: 0}}, {{x: {H_WIN_L - H_WIN_CENTER}, duration: {SLIDE_IN}, ease: "power3.out"}}, {a});')
                js.append(f'tl.fromTo("#bar", {{x: -{H_WIN_L}}}, {{x: 0, duration: {SLIDE_IN}, ease: "power3.out"}}, {a});')
            else:
                js.append(f'tl.set("#win", {{x: {H_WIN_L - H_WIN_CENTER}}}, 0); tl.set("#bar", {{x: 0}}, 0);')
            if b < DUR:
                js.append(f'tl.to("#win", {{x: 0, duration: {SLIDE_OUT + 0.15}, ease: "power3.inOut"}}, {round(b - SLIDE_OUT, 3)});')
                js.append(f'tl.to("#bar", {{x: -{H_WIN_L}, duration: {SLIDE_OUT}, ease: "power2.in"}}, {round(b - SLIDE_OUT, 3)});')
        if plan["h"][0]["in"] > 0:
            js.insert(0, f'tl.set("#bar", {{x: -{H_WIN_L}}}, 0);')
        cam = poses(1.0, 1.1, 0.8)
    else:
        cam = poses(1.0, 1.16, 0.5)

    html = TEMPLATE[orient].format(
        dur=DUR, clips="\n      ".join(clips), js="\n      ".join(js), poses=json.dumps(cam),
        win_l=H_WIN_CENTER, win_w=H_WIN_W, panel_x=PANEL_X, panel_color=PANEL_COLOR, bar_w=H_WIN_L,
        fade_at=round(DUR - 0.5, 3))
    open(os.path.join(proj, "index.html"), "w").write(html)
    print("wrote", os.path.join(proj, "index.html"))


COMMON_JS = """
      const poses = {poses};
      poses.forEach(([a, b, s0, s1, x0, x1]) => {{
        tl.set("#cam", {{ scale: s0, xPercent: x0 }}, a);
        tl.to("#cam", {{ scale: s1, xPercent: x1, duration: b - a, ease: "sine.inOut" }}, a);
      }});
      tl.fromTo("#fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "none" }}, {fade_at});
"""

TEMPLATE = {
    "h": """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>01_01 horizontal, ben's graphics</title>
    <script src="gsap.min.js"></script>
    <style>
      body {{ margin: 0; background: {panel_color}; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {panel_color}; }}
      #bg {{ position: absolute; inset: -60px; width: calc(100% + 120px); height: calc(100% + 120px); object-fit: cover;
             filter: blur(36px) brightness(0.38) saturate(0.8); }}
      #win {{ position: absolute; top: 0; left: {win_l}px; width: {win_w}px; height: 1080px; overflow: hidden; background: #000; }}
      #cam {{ position: absolute; inset: 0; transform-origin: 50% 28%; }}
      #a-roll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%; }}
      #bar {{ position: absolute; top: 0; left: 0; width: {bar_w}px; height: 1080px; background: {panel_color}; }}
      .gw {{ position: absolute; inset: 0; clip-path: inset(0 0 0 {panel_x}px); }}
      .gf {{ position: absolute; inset: 0; width: 1920px; height: 1080px; }}
      #fade {{ position: absolute; inset: 0; background: #000; opacity: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{dur}">
      <video id="bg" class="clip" src="assets/cut.mp4" muted playsinline data-start="0" data-duration="{dur}" data-track-index="0"></video>
      <div id="win">
        <div id="cam">
          <video id="a-roll" class="clip" src="assets/cut.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{dur}" data-track-index="1" data-volume="1"></video>
        </div>
      </div>
      <div id="bar"></div>
      {clips}
      <div id="fade"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
""" + COMMON_JS + """
      {js}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""",
    "v": """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>01_01 vertical, ben's graphics</title>
    <script src="gsap.min.js"></script>
    <style>
      body {{ margin: 0; background: #1f1f1f; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #1f1f1f; }}
      #cam {{ position: absolute; inset: 0; transform-origin: 47% 27%; }}
      #a-roll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .gw {{ position: absolute; inset: 0; }}
      .gf {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      #fade {{ position: absolute; inset: 0; background: #000; opacity: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{dur}">
      <div id="cam">
        <video id="a-roll" class="clip" src="assets/cut.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{dur}" data-track-index="0" data-volume="1"></video>
      </div>
      {clips}
      <div id="fade"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
""" + COMMON_JS + """
      {js}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""",
}

if __name__ == "__main__":
    for o in ("h", "v"):
        build(o)
