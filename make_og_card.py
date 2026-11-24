#!/usr/bin/env python3
"""Generate og-card.png for GrandFrostAuto — 1200x630 social share card."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
SUN_CY = 430          # sun circle center-y
SUN_R = 180

# --- sky gradient: deep purple -> hot pink -> orange (Vice City sunset) ---
sky_stops = [
    (18, 8, 48),      # deep night purple
    (58, 28, 113),    # purple
    (215, 109, 119),  # pink
    (255, 175, 123),  # peach
    (255, 220, 160),  # warm horizon
]
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
n = len(sky_stops) - 1
for y in range(H):
    t = y / H
    seg = min(int(t * n), n - 1)
    lt = t * n - seg
    a, b = sky_stops[seg], sky_stops[seg + 1]
    c = tuple(int(a[i] + (b[i] - a[i]) * lt) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# --- sun circle with horizontal gap bands (retro sun) ---
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
sd.ellipse([W//2 - SUN_R, SUN_CY - SUN_R, W//2 + SUN_R, SUN_CY + SUN_R],
           fill=(255, 214, 92, 255))
# horizontal cut lines growing wider toward bottom of the sun
yy = SUN_CY
gap = 6
w_gap = 10
while yy < SUN_CY + SUN_R:
    sd.rectangle([0, yy, W, yy + gap], fill=(0, 0, 0, 0))
    mask_row = sd
    yy += gap + w_gap
    w_gap += 10
# simpler: redraw stripes over sun region
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
sd.ellipse([W//2 - SUN_R, SUN_CY - SUN_R, W//2 + SUN_R, SUN_CY + SUN_R],
           fill=(255, 214, 92, 255))
yy, w_gap = SUN_CY - 30, 8
while yy < SUN_CY + SUN_R:
    stripe_h = 7
    sd.rectangle([0, yy, W, yy + stripe_h], fill=(255, 214, 92, 0))
    # need alpha-erase: use separate mask approach below instead
    yy += stripe_h + w_gap
    w_gap += 6
# proper stripe erase via alpha composite
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
sd.ellipse([W//2 - SUN_R, SUN_CY - SUN_R, W//2 + SUN_R, SUN_CY + SUN_R],
           fill=(255, 214, 92, 255))
erase = Image.new("L", (W, H), 0)
ed = ImageDraw.Draw(erase)
yy, w_gap = SUN_CY - 30, 8
while yy < SUN_CY + SUN_R:
    ed.rectangle([0, yy, W, yy + 7], fill=255)
    yy += 7 + w_gap
    w_gap += 6
sun.putalpha(Image.composite(erase, Image.new("L", (W, H), 255), erase))
# hmm: putalpha replaces alpha; do channel math instead
# final simple approach: draw sun on sky, then draw sky-colored stripes over it
img.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (0,0,0,0)), sun),
          (0, 0), sun)
# The stripes were erased into sun's alpha already via composite (wrong); do it directly:
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
n = len(sky_stops) - 1
for y in range(H):
    t = y / H
    seg = min(int(t * n), n - 1)
    lt = t * n - seg
    a, b = sky_stops[seg], sky_stops[seg + 1]
    c = tuple(int(a[i] + (b[i] - a[i]) * lt) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)
# sun
sd = ImageDraw.Draw(img)
sd.ellipse([W//2 - SUN_R, SUN_CY - SUN_R, W//2 + SUN_R, SUN_CY + SUN_R],
           fill=(255, 214, 92))
# stripes over sun: sample sky color per row
for y in range(SUN_CY - 30, SUN_CY + SUN_R):
    t = y / H
    seg = min(int(t * n), n - 1)
    lt = t * n - seg
    a, b = sky_stops[seg], sky_stops[seg + 1]
    c = tuple(int(a[i] + (b[i] - a[i]) * lt) for i in range(3))
    # stripe pattern
    pass
yy, w_gap = SUN_CY - 30, 8
while yy < SUN_CY + SUN_R:
    t = yy / H
    seg = min(int(t * n), n - 1)
    lt = t * n - seg
    a, b = sky_stops[seg], sky_stops[seg + 1]
    c = tuple(int(a[i] + (b[i] - a[i]) * lt) for i in range(3))
    sd.rectangle([0, yy, W, yy + 7], fill=c)
    yy += 7 + w_gap
    w_gap += 6

# --- palms (drawn as stroke curves, mirrored sides) ---
def palm(dr, cx, base_y, s, col, flip=False):
    import math
    # trunk
    dr.line([(cx, base_y), (cx + 18*s, base_y - 190*s)], fill=col, width=max(3, int(9*s)))
    topx, topy = cx + 18*s, base_y - 190*s
    for ang_deg in (-80, -50, -15, 15, 50, 80):
        ang = math.radians(ang_deg if not flip else 180 - ang_deg)
        x2 = topx + 95*s*math.cos(ang)
        y2 = topy - 55*s*math.sin(ang) - 20*s
        dr.line([(topx, topy), (x2, y2)], fill=col, width=max(3, int(8*s)))
        # droop tip
        x3 = x2 + 28*s*math.cos(ang)
        y3 = y2 + 30*s
        dr.line([(x2, y2), (x3, y3)], fill=col, width=max(2, int(6*s)))

dark = (14, 11, 31)
palm(d, 90, H, 1.15, dark)
palm(d, W-90, H, 1.15, dark, flip=True)
palm(d, 210, H, 0.8, dark)
palm(d, W-210, H, 0.8, dark, flip=True)

# --- text ---
try:
    big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", 250)
    med = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", 64)
    small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
except Exception:
    big = med = small = ImageFont.load_default()

# VI — huge, centered on sun, gold->pink feel (two-pass offset glow)
vi = "VI"
bbox = d.textbbox((0, 0), vi, font=big)
vw = bbox[2] - bbox[0]
vh = bbox[3] - bbox[1]
vx = (W - vw) // 2 - bbox[0]
vy = SUN_CY - vh // 2 - bbox[1] - 40
# shadow pass
d.text((vx + 6, vy + 8), vi, font=big, fill=(120, 20, 70))
d.text((vx, vy), vi, font=big, fill=(255, 222, 89))

# title bar bottom
bar_y = H - 150
d.rectangle([0, bar_y, W, H], fill=(14, 11, 31))
# accent line
d.rectangle([0, bar_y, W, bar_y + 6], fill=(255, 62, 138))

t1 = "GRANDFROSTAUTO"
b1 = d.textbbox((0, 0), t1, font=med)
d.text(((W - (b1[2]-b1[0])) // 2, bar_y + 30), t1, font=med, fill=(255, 255, 255))
t2 = "GTA VI × Cyberleek — Leak Archive · Free Downloads + Official Hashes"
b2 = d.textbbox((0, 0), t2, font=small)
d.text(((W - (b2[2]-b2[0])) // 2, bar_y + 108), t2, font=small, fill=(53, 224, 200))

img.save("/Users/craigmac/craig/sites/grandfrostauto/og-card.png", "PNG")
print("saved", img.size)
