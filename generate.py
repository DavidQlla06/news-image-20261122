"""Draw the 22 November 2026 front page (1024x1024) from stories.json.

Fresh build for this edition: masthead naming the day, one lead panel
with a missile-over-sea pictogram, a 2x2 grid (globe flame, prison
bars, struck building, cracked ground) and a two-item bottom strip.
Pillow only; deterministic output.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024
M = 34
PAPER = (250, 247, 240)
INK = (22, 22, 22)
SOFT = (95, 92, 85)
WHITE = (255, 255, 255)
SKY = (205, 226, 240)
SEA = (110, 160, 200)
RED = (178, 34, 34)
NAVY = (24, 52, 110)
GREEN = (38, 120, 60)
AMBER = (190, 130, 20)
GREY = (120, 120, 120)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    out, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            line = trial
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def block(d, x, y, text, fnt, fill, max_w, leading, limit=99):
    for ln in wrap(d, text, fnt, max_w)[:limit]:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def tag(d, x, y, text, bg):
    fnt = F(SANSB, 18)
    w = d.textlength(text, font=fnt) + 20
    d.rounded_rectangle([x, y, x + w, y + 27], radius=4, fill=bg)
    d.text((x + 10, y + 4), text, font=fnt, fill=WHITE)
    return w


def motif_missile_sea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=SEA)
    # base: low buildings on shore
    d.rectangle([x, y + int(h * 0.64), x + w, y + int(h * 0.72)], fill=(200, 180, 140))
    for bx in (0.08, 0.30, 0.55, 0.78):
        d.rectangle([x + int(w * bx), y + int(h * 0.50), x + int(w * bx) + 46, y + int(h * 0.64)], fill=WHITE, outline=INK, width=2)
    # missile diagonal with flame + smoke trail
    mx, my = x + int(w * 0.62), y + int(h * 0.30)
    d.line([x + 10, y + 12, mx - 26, my + 10], fill=(170, 170, 170), width=5)
    d.polygon([(mx - 30, my + 14), (mx + 34, my - 16), (mx + 48, my - 2), (mx - 18, my + 28)], fill=(60, 60, 60))
    d.polygon([(mx - 30, my + 14), (mx - 52, my + 34), (mx - 34, my + 40), (mx - 18, my + 28)], fill=RED)
    d.polygon([(mx - 48, my + 32), (mx - 72, my + 52), (mx - 52, my + 56)], fill=(240, 140, 20))
    # explosion over a building
    ex, ey = x + int(w * 0.40), y + int(h * 0.48)
    for r, c in ((30, (240, 140, 20)), (20, (250, 200, 40))):
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=c)
    for sx, sy, r in ((ex + 24, ey - 36, 12), (ex + 44, ey - 52, 15)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=GREY)
    # tanker on sea
    ty = y + int(h * 0.80)
    d.polygon([(x + 30, ty), (x + 170, ty), (x + 150, ty + 22), (x + 48, ty + 22)], fill=(50, 50, 50))
    d.rectangle([x + 60, ty - 18, x + 140, ty], fill=RED, outline=INK)


def motif_globe_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 240, 220))
    cx, cy, r = x + w // 2, y + int(h * 0.56), 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 165, 205), outline=INK, width=2)
    d.ellipse([cx - 24, cy - 20, cx + 4, cy + 6], fill=(90, 170, 90))
    d.ellipse([cx + 6, cy + 10, cx + 28, cy + 30], fill=(90, 170, 90))
    # flame above globe
    fx, fy = cx, cy - r - 6
    d.polygon([(fx - 14, fy), (fx, fy - 34), (fx + 14, fy)], fill=(240, 120, 20))
    d.polygon([(fx - 7, fy), (fx, fy - 18), (fx + 7, fy)], fill=(250, 205, 50))
    # deadlock: two opposing arrows
    d.line([x + 12, y + h - 16, cx - 8, y + h - 16], fill=RED, width=4)
    d.polygon([(cx - 8, y + h - 16), (cx - 20, y + h - 23), (cx - 20, y + h - 9)], fill=RED)
    d.line([x + w - 12, y + h - 16, cx + 8, y + h - 16], fill=NAVY, width=4)
    d.polygon([(cx + 8, y + h - 16), (cx + 20, y + h - 23), (cx + 20, y + h - 9)], fill=NAVY)


def motif_bars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 235, 235))
    # silhouette head behind bars
    cx, cy = x + w // 2, y + int(h * 0.42)
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(70, 70, 70))
    d.rectangle([cx - 34, cy + 22, cx + 34, cy + 58], fill=(70, 70, 70))
    for i in range(5):
        bx = x + 14 + i * int((w - 28) / 4)
        d.rectangle([bx, y + 8, bx + 7, y + h - 8], fill=INK)
    d.rectangle([x + 8, y + 8, x + w - 8, y + 15], fill=INK)
    d.rectangle([x + 8, y + h - 15, x + w - 8, y + h - 8], fill=INK)


def motif_building(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    bx, bw = x + int(w * 0.28), int(w * 0.44)
    d.rectangle([bx, y + int(h * 0.22), bx + bw, y + h - 10], fill=(210, 200, 180), outline=INK, width=2)
    for r in range(4):
        for c in range(3):
            wx = bx + 8 + c * int(bw / 3)
            wy = y + int(h * 0.28) + r * int(h * 0.16)
            d.rectangle([wx, wy, wx + 12, wy + 12], fill=NAVY)
    # blast hole + smoke
    ex, ey = bx + bw // 2, y + int(h * 0.36)
    d.ellipse([ex - 18, ey - 18, ex + 18, ey + 18], fill=(40, 40, 40))
    for sx, sy, r in ((ex - 6, ey - 34, 11), (ex + 12, ey - 50, 14)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=GREY)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 110, 90))


def motif_crack(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 238, 220))
    # mountains
    d.polygon([(x, y + int(h * 0.62)), (x + int(w * 0.34), y + int(h * 0.26)), (x + int(w * 0.62), y + int(h * 0.62))], fill=(130, 120, 105))
    d.polygon([(x + int(w * 0.5), y + int(h * 0.62)), (x + int(w * 0.78), y + int(h * 0.36)), (x + w, y + int(h * 0.62))], fill=(150, 140, 125))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(190, 165, 120))
    # zigzag crack
    pts = [(x + 8, y + int(h * 0.72)), (x + int(w * 0.3), y + int(h * 0.80)), (x + int(w * 0.45), y + int(h * 0.70)), (x + int(w * 0.68), y + int(h * 0.84)), (x + w - 8, y + int(h * 0.74))]
    d.line(pts, fill=INK, width=5, joint="curve")
    # shaking house
    hx, hy = x + int(w * 0.40), y + int(h * 0.44)
    d.polygon([(hx - 4, hy), (hx + 20, hy - 18), (hx + 44, hy)], fill=RED)
    d.rectangle([hx, hy, hx + 40, hy + 28], fill=WHITE, outline=INK, width=2)


MOTIFS = {"missile_sea": motif_missile_sea, "globe_flame": motif_globe_flame,
          "bars": motif_bars, "building": motif_building, "crack": motif_crack}
TAG_COLORS = {"GULF CRISIS": RED, "CLIMATE": GREEN, "MEXICO": NAVY,
              "UKRAINE WAR": RED, "EARTHQUAKE": INK}


def render(spec, out_path):
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    eye = F(SANSB, 21)
    d.text(((SIZE - d.textlength("THE WORLD IN ONE IMAGE", font=eye)) / 2, 24), "THE WORLD IN ONE IMAGE", font=eye, fill=SOFT)
    ds = 54
    while ds > 30 and d.textlength(spec["date"], font=F(SERIF, ds)) > SIZE - 2 * M - 8:
        ds -= 2
    df = F(SERIF, ds)
    d.text(((SIZE - d.textlength(spec["date"], font=df)) / 2, 54), spec["date"], font=df, fill=INK)
    d.line([M, 138, SIZE - M, 138], fill=INK, width=4)
    d.line([M, 146, SIZE - M, 146], fill=INK, width=1)
    # lead
    lead = spec["lead"]
    ly, lh = 160, 318
    d.rectangle([M, ly, SIZE - M, ly + lh], fill=WHITE, outline=INK, width=2)
    MOTIFS[lead["motif"]](d, M + 2, ly + 2, 374, lh - 4)
    d.line([M + 376, ly, M + 376, ly + lh], fill=INK, width=2)
    tx = M + 398
    tw = SIZE - M - tx - 16
    tag(d, tx, ly + 18, lead["kicker"], TAG_COLORS.get(lead["kicker"], INK))
    y = block(d, tx, ly + 60, lead["headline"], F(SANSB, 39), INK, tw, 47, 3)
    block(d, tx, y + 6, lead["summary"], F(SANS, 25), (50, 50, 50), tw, 32, 4)
    # day marker under the lead text so the date reads at thumbnail size
    d.text((tx, ly + lh - 34), "22 NOV 2026", font=F(SANSB, 19), fill=SOFT)
    # grid
    gy = ly + lh + 16
    cw, ch, gap = 468, 196, 16
    for i, s in enumerate(spec["grid"]):
        cx = M + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=WHITE, outline=INK, width=2)
        MOTIFS[s["motif"]](d, cx + 2, cy + 2, 122, ch - 4)
        tx2 = cx + 138
        tw2 = cx + cw - tx2 - 12
        tag(d, tx2, cy + 11, s["kicker"], TAG_COLORS.get(s["kicker"], INK))
        y2 = block(d, tx2, cy + 46, s["headline"], F(SANSB, 25), INK, tw2, 30, 3)
        block(d, tx2, y2 + 3, s["summary"], F(SANS, 20), (60, 60, 60), tw2, 25, 2)
    # bottom strip
    by = gy + 2 * ch + gap + 14
    d.rectangle([M, by, SIZE - M, by + 52], fill=(238, 233, 220), outline=INK, width=1)
    left = "•  " + spec["bottom"][0]
    right = "•  " + spec["bottom"][1]
    bs = 22
    while bs > 15 and d.textlength(left, font=F(SANSB, bs)) + d.textlength(right, font=F(SANSB, bs)) + 40 > SIZE - 2 * M - 16:
        bs -= 1
    bf = F(SANSB, bs)
    total = d.textlength(left, font=bf) + d.textlength(right, font=bf) + 40
    x0 = (SIZE - total) / 2
    d.text((x0, by + 14), left, font=bf, fill=INK)
    d.text((x0 + d.textlength(left, font=bf) + 40, by + 14), right, font=bf, fill=INK)
    ff = F(SANS, 18)
    d.text(((SIZE - d.textlength(spec["footer"], font=ff)) / 2, by + 66), spec["footer"], font=ff, fill=SOFT)
    img.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    spec = json.load(open(os.path.join(HERE, "stories.json")))
    out = os.path.join(HERE, "entry.png")
    render(spec, out)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
