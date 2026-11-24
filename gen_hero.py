#!/usr/bin/env python3
"""Generate cinematic GTA-VI-style launch hero SVG (1600x900) for GrandFrostAuto.
Realistic sunset key-art: layered sky, half-set sun, ocean reflection, clouds,
birds, and mathematically-built palm silhouettes (curved trunk + drooping fronds
with tapered leaflets). Output: hero.svg (inline-able)."""
import math, random

random.seed(6)
W, H = 1600, 900
HORIZON = 618
SUN_X, SUN_Y, SUN_R = 800, HORIZON, 148
INK = "#150b28"

def q(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    return x, y

def qtan(p0, p1, p2, t):
    dx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    dy = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    n = math.hypot(dx, dy) or 1
    return dx/n, dy/n

def palm(cx, base_y, height, lean, scale, flip=1):
    """Return SVG group string: tapered curved trunk + fronds with leaflets."""
    crown = (cx + lean*flip, base_y - height)
    # trunk centerline: quadratic from base to crown, bulge opposite lean
    p0 = (cx, base_y)
    p1 = (cx + lean*0.25*flip, base_y - height*0.55)
    p2 = crown
    w0, w1 = 16*scale, 6*scale
    left, right = [], []
    for i in range(25):
        t = i/24
        x, y = q(p0, p1, p2, t)
        tx, ty = qtan(p0, p1, p2, t)
        nx, ny = -ty, tx
        w = (w0*(1-t) + w1*t)/2
        left.append((x+nx*w, y+ny*w))
        right.append((x-nx*w, y-ny*w))
    poly = left + right[::-1]
    trunk = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in poly) + " Z"
    out = [f'<path d="{trunk}" fill="{INK}"/>']
    # fronds
    angles = [-96, -70, -44, -18, 6, 30, 56, 82, 104]
    for k, adeg in enumerate(angles):
        a = math.radians(adeg)
        dx, dy = math.sin(a)*flip, -math.cos(a)
        L = height*(0.42 + 0.10*math.sin(k*1.7)) * (1.0 if abs(adeg) < 90 else 0.8)
        droop = L*(0.30 + 0.22*abs(math.sin(a)))
        c = (crown[0] + dx*L*0.55, crown[1] + dy*L*0.55 - L*0.16)
        e = (crown[0] + dx*L, crown[1] + dy*L*0.35 + droop)
        rachis = f"M{crown[0]:.1f},{crown[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {e[0]:.1f},{e[1]:.1f}"
        out.append(f'<path d="{rachis}" stroke="{INK}" stroke-width="{3.4*scale:.1f}" fill="none" stroke-linecap="round"/>')
        # leaflets along rachis, both sides, tapered + drooping
        seg = []
        t = 0.10
        while t < 0.97:
            px, py = q(crown, c, e, t)
            tx, ty = qtan(crown, c, e, t)
            ll = L*0.20*math.sin(math.pi*min(t*1.05, 1))**0.8 + 2
            for side in (-1, 1):
                ang = math.atan2(ty, tx) + side*math.radians(64)
                lx, ly = math.cos(ang), math.sin(ang)
                ex, ey = px + lx*ll, py + ly*ll + ll*0.45   # droop
                mx, my = px + lx*ll*0.5, py + ly*ll*0.5 + ll*0.12
                seg.append(f"M{px:.1f},{py:.1f} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}")
            t += 0.055
        out.append(f'<path d="{" ".join(seg)}" stroke="{INK}" stroke-width="{2.3*scale:.1f}" fill="none" stroke-linecap="round"/>')
    # coconuts
    for ox, oy in ((-8, 6), (6, 9), (0, 14)):
        out.append(f'<circle cx="{crown[0]+ox*scale:.1f}" cy="{crown[1]+oy*scale:.1f}" r="{6.5*scale:.1f}" fill="{INK}"/>')
    return "<g>" + "".join(out) + "</g>"

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Vice City sunset key art">')
parts.append('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#120821"/><stop offset=".34" stop-color="#3b1d5a"/>
<stop offset=".60" stop-color="#a44a6f"/><stop offset=".80" stop-color="#e07a5f"/>
<stop offset="1" stop-color="#ffb26b"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#c06070"/><stop offset=".28" stop-color="#6b3168"/>
<stop offset="1" stop-color="#160b2a"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5">
<stop offset="0" stop-color="#ffd98a" stop-opacity=".85"/>
<stop offset=".55" stop-color="#ff9e6b" stop-opacity=".35"/>
<stop offset="1" stop-color="#ff9e6b" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".46" r=".75">
<stop offset=".55" stop-color="#0a0514" stop-opacity="0"/>
<stop offset="1" stop-color="#0a0514" stop-opacity=".62"/></radialGradient>
<filter id="soft"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .05 0"/></filter>
</defs>''')
parts.append(f'<rect width="{W}" height="{HORIZON}" fill="url(#sky)"/>')
# stars
stars = "".join(f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,240):.0f}" r="{random.uniform(.7,1.6):.1f}" fill="#ffe9f2" opacity="{random.uniform(.15,.6):.2f}"/>' for _ in range(70))
parts.append(stars)
# clouds
for cx, cy, rx, ry, op in ((300,180,220,26,.30),(1150,140,260,30,.26),(760,300,300,24,.30),(1400,330,200,22,.24),(180,400,240,20,.28)):
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ff9d8a" opacity="{op}" filter="url(#soft)"/>')
# sun glow + disc
parts.append(f'<circle cx="{SUN_X}" cy="{SUN_Y}" r="330" fill="url(#glow)"/>')
parts.append(f'<circle cx="{SUN_X}" cy="{SUN_Y}" r="{SUN_R}" fill="#ffd98a"/>')
parts.append(f'<circle cx="{SUN_X}" cy="{SUN_Y}" r="{SUN_R}" fill="#fff3c4" opacity=".55" filter="url(#soft)"/>')
# ocean
parts.append(f'<rect y="{HORIZON}" width="{W}" height="{H-HORIZON}" fill="url(#sea)"/>')
# sun reflection shimmer
refl = []
y = HORIZON + 6
w = SUN_R*1.5
while y < H:
    frac = (y-HORIZON)/(H-HORIZON)
    ww = w*(0.55+0.75*frac)*random.uniform(.5,1.0)
    op = .5*(1-frac)**1.4
    refl.append(f'<rect x="{SUN_X-ww/2+random.uniform(-30,30):.0f}" y="{y:.0f}" width="{ww:.0f}" height="{random.uniform(2,5):.1f}" rx="2" fill="#ffcf8a" opacity="{op:.2f}"/>')
    y += random.uniform(9,16)
parts.append("".join(refl))
# horizon line
parts.append(f'<rect y="{HORIZON-1}" width="{W}" height="2" fill="#ffd9a0" opacity=".5"/>')
# birds
for bx, by, s in ((520,240,1),(560,262,.8),(1080,210,1.1),(1120,236,.75),(980,300,.6)):
    parts.append(f'<path d="M{bx},{by} q{9*s:.0f},{-7*s:.0f} {18*s:.0f},0 q{9*s:.0f},{-7*s:.0f} {18*s:.0f},0" stroke="{INK}" stroke-width="{2.4*s:.1f}" fill="none" stroke-linecap="round" opacity=".85"/>')
# palms: foreground pair + mid pair
parts.append(palm(150, H+30, 620, 60, 1.5, flip=1))
parts.append(palm(1470, H+40, 660, 70, 1.6, flip=-1))
parts.append(palm(330, H+20, 430, 40, 1.0, flip=1))
parts.append(palm(1300, H+25, 460, 45, 1.05, flip=-1))
# vignette + grain
parts.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
parts.append(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".5"/>')
parts.append('</svg>')

svg = "".join(parts)
open("/Users/craigmac/craig/sites/grandfrostauto/hero.svg", "w").write(svg)
print("hero.svg bytes:", len(svg))
