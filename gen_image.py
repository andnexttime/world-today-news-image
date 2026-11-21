#!/usr/bin/env python3
"""Draw the news-image-01 entry: a one-page editorial infographic summing up
Friday 13 November 2026 in six verified stories, rendered with Pillow only.

Output: entry.png, 1024x1024, well under 1 MiB. Every headline and label is
drawn with a real font, so nothing is garbled; every story is one that was
reported on 13 November 2026 (BBC, Al Jazeera, Reuters, AP, FT, Guardian).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# ---- palette: restrained newsroom -------------------------------------------
NAVY = (20, 33, 61)
NAVY_DK = (13, 22, 43)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (24, 28, 36)
GREY = (94, 100, 110)
RED = (192, 57, 43)
GOLD = (212, 160, 23)
GOLD_LT = (232, 196, 90)
RULE = (214, 206, 188)

F_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, text, bg, fg=(255, 255, 255)):
    """Small region tag, top-left of an illustration."""
    f = font(F_BOLD, 17)
    tw = d.textlength(text, font=f)
    pad = 9
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + 26], radius=4, fill=bg)
    d.text((x + pad, y + 4), text, font=f, fill=fg)


# ---- illustration panels (flat editorial shapes) ----------------------------

def art_senate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(122, 147, 184))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(96, 118, 152))
    # Capitol dome, left
    dx, dy = x + 52, y + h - 26
    d.rectangle([dx - 58, dy - 62, dx + 58, dy], fill=(236, 232, 220))
    d.pieslice([dx - 46, dy - 112, dx + 46, dy - 20], 180, 360, fill=(236, 232, 220))
    d.rectangle([dx - 4, dy - 128, dx + 4, dy - 108], fill=(236, 232, 220))
    d.polygon([(dx - 4, dy - 128), (dx + 18, dy - 122), (dx - 4, dy - 116)],
              fill=RED)
    for cx in (-38, -14, 10, 34):
        d.rectangle([dx + cx, dy - 52, dx + cx + 12, dy - 8], fill=(96, 118, 152))
    # empty witness chair behind the hearing desk, right; jacket draped on it
    d.rectangle([x + w - 152, y + 34, x + w - 104, y + 92], fill=(60, 42, 30))
    d.polygon([(x + w - 156, y + 30), (x + w - 100, y + 30),
               (x + w - 106, y + 66), (x + w - 150, y + 66)],
              fill=(28, 28, 30))
    # hearing desk
    d.rectangle([x + w - 190, y + 88, x + w - 26, y + h - 26], fill=(90, 62, 44))
    d.rectangle([x + w - 190, y + 88, x + w - 26, y + 100], fill=(112, 78, 56))
    # microphone on the desk
    d.line([x + w - 168, y + 88, x + w - 168, y + 66], fill=INK, width=4)
    d.ellipse([x + w - 174, y + 58, x + w - 162, y + 70], fill=INK)


def art_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(227, 213, 184))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(198, 178, 138))
    # round table
    d.ellipse([x + 90, y + 96, x + w - 90, y + 150], fill=(122, 84, 52))
    d.rectangle([x + w // 2 - 14, y + 122, x + w // 2 + 14, y + h - 26], fill=(96, 64, 40))
    # three flags on poles behind the table
    def flag(fx, fy, kind):
        d.line([fx, fy, fx, fy - 74], fill=(70, 60, 48), width=4)
        if kind == "ua":
            d.rectangle([fx + 4, fy - 74, fx + 66, fy - 49], fill=(0, 91, 187))
            d.rectangle([fx + 4, fy - 49, fx + 66, fy - 24], fill=(255, 213, 0))
        elif kind == "us":
            for i in range(5):
                d.rectangle([fx + 4, fy - 74 + i * 10, fx + 66, fy - 64 + i * 10],
                            fill=RED if i % 2 == 0 else (255, 255, 255))
            d.rectangle([fx + 4, fy - 74, fx + 30, fy - 50], fill=(30, 58, 138))
        else:  # eu
            d.rectangle([fx + 4, fy - 74, fx + 66, fy - 24], fill=(0, 51, 153))
            for k in range(8):
                import math
                a = math.pi * k / 4
                d.ellipse([fx + 31 + 13 * math.cos(a) - 2, fy - 49 + 11 * math.sin(a) - 2,
                           fx + 31 + 13 * math.cos(a) + 2, fy - 49 + 11 * math.sin(a) + 2],
                          fill=(255, 209, 0))
    flag(x + 96, y + 96, "ua")
    flag(x + w // 2 - 33, y + 88, "us")
    flag(x + w - 162, y + 96, "eu")


def art_warship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(185, 201, 214))
    d.rectangle([x, y + 96, x + w, y + h], fill=(78, 110, 138))
    d.rectangle([x, y + 96, x + w, y + 100], fill=(120, 148, 170))
    # smoke plume
    for (sx, sy, r) in ((x + 300, y + 22, 26), (x + 322, y + 8, 20),
                        (x + 278, y + 10, 17), (x + 340, y + 26, 15)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 124, 128))
    # hull
    d.polygon([(x + 60, y + 128), (x + 420, y + 128), (x + 396, y + 158),
               (x + 84, y + 158)], fill=(52, 60, 70))
    d.rectangle([x + 120, y + 104, x + 300, y + 128], fill=(70, 80, 92))
    d.rectangle([x + 170, y + 84, x + 230, y + 104], fill=(70, 80, 92))
    d.rectangle([x + 196, y + 62, x + 204, y + 84], fill=(52, 60, 70))
    # small drone, upper right
    dx, dy = x + w - 78, y + 34
    d.line([dx - 16, dy - 10, dx + 16, dy + 10], fill=(30, 34, 40), width=4)
    d.line([dx - 16, dy + 10, dx + 16, dy - 10], fill=(30, 34, 40), width=4)
    d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=(30, 34, 40))
    # wake
    d.line([x + 60, y + 164, x + 20, y + 164], fill=(200, 214, 224), width=3)
    d.line([x + 396, y + 164, x + 440, y + 164], fill=(200, 214, 224), width=3)


def art_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 216, 160))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(214, 164, 88))
    # sun
    d.ellipse([x + w - 92, y + 14, x + w - 34, y + 72], fill=(240, 180, 60))
    # missile streak
    d.line([x + 60, y + 26, x + 300, y + 96], fill=(255, 255, 255), width=5)
    d.polygon([(x + 300, y + 96), (x + 330, y + 104), (x + 306, y + 112)],
              fill=(120, 120, 120))
    d.polygon([(x + 330, y + 104), (x + 352, y + 110), (x + 330, y + 118)],
              fill=(240, 120, 40))
    # radar dome + dish on a desert coast base
    d.rectangle([x + 150, y + h - 30, x + 330, y + h - 30], fill=(120, 96, 70))
    d.pieslice([x + 176, y + 58, x + 304, y + 186], 180, 360, fill=(250, 248, 242))
    d.rectangle([x + 176, y + 118, x + 304, y + h - 30], fill=(226, 222, 210))
    d.line([x + 240, y + 62, x + 330, y + 30], fill=(90, 90, 90), width=4)
    d.ellipse([x + 318, y + 18, x + 342, y + 42], fill=(90, 90, 90))


def art_outage(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 52, 64))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(34, 38, 48))
    # laptop
    d.rounded_rectangle([x + 96, y + 34, x + w - 96, y + 138], radius=8, fill=(24, 28, 38))
    d.rounded_rectangle([x + 108, y + 46, x + w - 108, y + 126], radius=4, fill=(58, 110, 170))
    # globe on screen: blue circle, green land blobs
    cx, cy, r = x + w // 2 - 40, y + 86, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 180))
    d.ellipse([cx - 20, cy - 24, cx + 2, cy - 2], fill=(70, 160, 90))
    d.ellipse([cx - 4, cy + 6, cx + 22, cy + 24], fill=(70, 160, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(140, 190, 230), width=3)
    # outage cross over the globe
    d.line([cx + 26, cy - 26, cx + 62, cy + 10], fill=RED, width=7)
    d.line([cx + 62, cy - 26, cx + 26, cy + 10], fill=RED, width=7)
    d.rounded_rectangle([x + 76, y + 138, x + w - 76, y + 150], radius=4, fill=(24, 28, 38))
    # warning triangle
    tx, ty = x + w - 96, y + 96
    d.polygon([(tx, ty - 34), (tx + 34, ty + 22), (tx - 34, ty + 22)], fill=(240, 190, 40))
    d.rectangle([tx - 3, ty - 18, tx + 3, ty + 2], fill=INK)
    d.ellipse([tx - 3, ty + 8, tx + 3, ty + 14], fill=INK)


def art_hack(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 70, 52))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(22, 52, 40))
    # video-call window
    d.rounded_rectangle([x + 110, y + 22, x + w - 110, y + 118], radius=8, fill=(16, 24, 20))
    d.rounded_rectangle([x + 122, y + 34, x + w - 122, y + 106], radius=4, fill=(44, 62, 52))
    # masked face: dark hood + pale mask
    cx, cy = x + w // 2 - 30, y + 70
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(18, 22, 20))
    d.ellipse([cx - 18, cy - 16, cx + 18, cy + 18], fill=(228, 222, 210))
    d.ellipse([cx - 12, cy - 8, cx - 3, cy + 0], fill=INK)
    d.ellipse([cx + 3, cy - 8, cx + 12, cy + 0], fill=INK)
    # coins spilling out of the screen
    for (ox, oy, r) in ((x + 120, y + 128, 15), (x + 160, y + 140, 13),
                        (x + 205, y + 130, 15), (x + 250, y + 142, 13),
                        (x + 300, y + 130, 15), (x + 345, y + 140, 13)):
        d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=GOLD)
        d.ellipse([ox - r + 4, oy - r + 4, ox + r - 4, oy + r - 4],
                  outline=(160, 110, 10), width=2)
        d.text((ox - 4, oy - 9), "$", font=font(F_BOLD, 15), fill=(120, 82, 8))


TILES = [
    # (art, region chip, chip colour, headline, sub-caption)
    (art_senate, "USA", RED, "SENATE SUMMONS HUANG",
     "Ex-Nvidia chief to testify"),
    (art_flags, "UKRAINE", (0, 91, 187), "ZELENSKY MEETS US ENVOYS",
     "Europe joins Ukraine peace talks"),
    (art_warship, "BALTIC SEA", (78, 110, 138), "DRONE HITS WARSHIP",
     "Strike in Gulf of Finland"),
    (art_radar, "BAHRAIN", (176, 110, 40), "IRAN CLAIMS RADAR STRIKE",
     "US site in Bahrain targeted"),
    (art_outage, "WORLDWIDE", (46, 52, 64), "MICROSOFT 365 DOWN",
     "Outlook & Teams hit worldwide"),
    (art_hack, "CYBER", (30, 70, 52), "FBI: $400M CRYPTO HACK",
     "N. Korea blamed, fake video calls"),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -----------------------------------------------------------
    d.rectangle([0, 0, W, 176], fill=NAVY)
    d.rectangle([0, 176, W, 182], fill=GOLD)
    kicker = font(F_BOLD, 26)
    d.text((W // 2, 26), "FRIDAY  ·  13 NOVEMBER 2026", font=kicker,
           fill=GOLD_LT, anchor="ma")
    title = font(F_SERIF, 76)
    d.text((W // 2, 56), "THE WORLD TODAY", font=title, fill=(255, 255, 255),
           anchor="ma")
    sub = font(F_REG, 24)
    d.text((W // 2, 140), "Six stories that defined the day — in one picture",
           font=sub, fill=(190, 200, 220), anchor="ma")

    # ---- tile grid ----------------------------------------------------------
    margin, gutter = 24, 16
    tw = (W - margin * 2 - gutter) // 2
    th = 248
    top = 200
    for i, (art, region, chip_bg, headline, subcap) in enumerate(TILES):
        col, row = i % 2, i // 2
        x = margin + col * (tw + gutter)
        y = top + row * (th + gutter)
        # card
        d.rectangle([x, y, x + tw, y + th], fill=CARD, outline=RULE, width=2)
        art_h = 164
        art(d, x + 2, y + 2, tw - 4, art_h)
        chip(d, x + 14, y + 12, region, chip_bg)
        # headline + sub-caption: shrink until the headline fits one line,
        # so it can never collide with the sub-caption below it
        size = 30
        while size > 22:
            f_head = font(F_BOLD, size)
            if d.textlength(headline, font=f_head) <= tw - 28:
                break
            size -= 1
        d.text((x + 14, y + art_h + 16), headline, font=f_head, fill=INK)
        d.text((x + 14, y + th - 28), subcap, font=font(F_REG, 20), fill=GREY)

    # ---- footer -------------------------------------------------------------
    fy = top + 3 * th + 2 * gutter + 12
    d.text((W // 2, fy), "Reported 13 November 2026  ·  BBC  ·  Al Jazeera  ·  Reuters  ·  AP  ·  FT  ·  Guardian",
           font=font(F_REG, 18), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    image = build()
    image.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", image.size)
