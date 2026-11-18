"""Boil bubble: a face (or any clip) in a hand-drawn round bubble whose two pencil lines boil like stop motion.

Each of the two lines wobbles on its own (own noise, own timing) around the same near-circle, and the clip is masked
to the innermost line at every frame, so the picture breathes with the drawing. ben's spec, 2026-10-26.

Writes PNG sequences: m%04d.png (grayscale mask) and o%04d.png (RGBA outlines), one per frame.
Usage:  python3 boil_bubble.py OUT_DIR SECONDS [--size 400] [--fps 23.976] [--color F2A93B] [--every 2]
Overlay with ffmpeg (clip already cropped/scaled to SIZE x SIZE):
  -framerate FPS -i OUT_DIR/m%04d.png -framerate FPS -i OUT_DIR/o%04d.png
  [clip]format=rgba[c];[m]format=gray[mk];[c][mk]alphamerge[ca];[bg][ca]overlay=X:Y[t];[t][o]overlay=X:Y
"""
import argparse, math, os, random
from PIL import Image, ImageDraw

N = 72  # points around the circle


def radii(seed, step, amp=0.035):
    """Smooth random wobble for one line at one 'drawing' (step): a few low-frequency sines with random phases."""
    r = random.Random(seed * 1000 + step)
    waves = [(k, r.uniform(0, 2 * math.pi), r.uniform(0.3, 1.0) * amp / k ** 0.5) for k in (2, 3, 4, 6)]
    jitter = [r.uniform(-amp * 0.15, amp * 0.15) for _ in range(N)]
    return [1 + sum(a * math.sin(k * 2 * math.pi * j / N + ph) for k, ph, a in waves) + jitter[j] for j in range(N)]


def frames(out_dir, seconds, size=400, fps=24000 / 1001, color="F2A93B", every=2, width=6):
    os.makedirs(out_dir, exist_ok=True)
    S = 2; c = size * S / 2; R = (size / 2 - width * 1.5) * S
    rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    n = int(math.ceil(seconds * fps)) + 4
    for f in range(n):
        # the two lines redraw on different frames, so they never move together
        r1 = radii(1, f // every); r2 = radii(2, (f + every // 2 + 1) // (every + 1))
        pts = lambda rr, k=1.0: [(c + R * k * rr[j] * math.cos(2 * math.pi * j / N), c + R * k * rr[j] * math.sin(2 * math.pi * j / N)) for j in range(N)]
        inner = [min(a, b) for a, b in zip(r1, r2)]
        m = Image.new("L", (size * S, size * S), 0)
        ImageDraw.Draw(m).polygon(pts(inner), fill=255)
        m.resize((size, size), Image.LANCZOS).save(f"{out_dir}/m{f:04d}.png")
        o = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
        for rr in (r1, r2):
            p = pts(rr); d.line(p + [p[0]], fill=rgb + (255,), width=width * S // 2 + 1, joint="curve")
        o.resize((size, size), Image.LANCZOS).save(f"{out_dir}/o{f:04d}.png")
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir"); ap.add_argument("seconds", type=float)
    ap.add_argument("--size", type=int, default=400); ap.add_argument("--fps", type=float, default=24000 / 1001)
    ap.add_argument("--color", default="F2A93B"); ap.add_argument("--every", type=int, default=2)
    a = ap.parse_args()
    print(frames(a.out_dir, a.seconds, a.size, a.fps, a.color, a.every), "frames")
