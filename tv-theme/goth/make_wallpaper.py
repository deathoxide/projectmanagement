"""Draw a dark gothic wallpaper (1920x1080): blood moon, cathedral skyline, bare trees, mist, bats."""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
rnd = random.Random(1347)
out = sys.argv[1]

# Sky: near-black at the top, a faint wine colour towards the horizon.
sky = Image.new("RGB", (W, H))
px = sky.load()
for y in range(H):
    t = y / H
    r = int(4 + 26 * t ** 1.6)
    g = int(1 + 3 * t)
    b = int(6 + 10 * t ** 1.2)
    for x in range(W):
        px[x, y] = (r, g, b)
img = sky.convert("RGBA")

# Stars, sparse and dim.
stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(stars)
for _ in range(260):
    x, y = rnd.randrange(W), rnd.randrange(int(H * 0.6))
    a = rnd.randrange(30, 140)
    d.point((x, y), fill=(220, 200, 210, a))
img = Image.alpha_composite(img, stars)

# Blood moon with a wide halo, upper middle (clear of the clock and the top-right buttons).
MX, MY, MR = 1180, 360, 120
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
for i in range(40, 0, -1):
    rr = MR + i * 9
    hd.ellipse((MX - rr, MY - rr, MX + rr, MY + rr), fill=(140, 10, 20, 4))
halo = halo.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img, halo)

moon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
md = ImageDraw.Draw(moon)
for i in range(MR, 0, -1):
    t = i / MR
    c = (int(150 + 60 * (1 - t)), int(18 + 20 * (1 - t)), int(22 + 12 * (1 - t)), 255)
    md.ellipse((MX - i, MY - i, MX + i, MY + i), fill=c)
# Craters.
for _ in range(14):
    a = rnd.random() * 2 * math.pi
    dist = rnd.random() * MR * 0.75
    cx, cy = MX + math.cos(a) * dist, MY + math.sin(a) * dist
    cr = rnd.randrange(5, 15)
    md.ellipse((cx - cr, cy - cr, cx + cr, cy + cr), fill=(120, 12, 18, 40))
moon = moon.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img, moon)

# Thin clouds drifting across the moon.
clouds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(clouds)
for _ in range(9):
    cx = MX + rnd.randrange(-420, 420)
    cy = MY + rnd.randrange(-80, 140)
    w, h = rnd.randrange(260, 520), rnd.randrange(16, 34)
    cd.ellipse((cx - w, cy - h, cx + w, cy + h), fill=(6, 2, 6, 150))
clouds = clouds.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, clouds)


def cathedral(draw, base, colour):
    """A gothic skyline: twin spired towers, a nave with pointed windows, smaller spires."""
    def spire(x, w, top, tower_top):
        draw.rectangle((x - w // 2, tower_top, x + w // 2, base), fill=colour)
        draw.polygon([(x - w // 2 - 6, tower_top), (x + w // 2 + 6, tower_top), (x, top)], fill=colour)
        for k in (-1, 1):  # pinnacles
            px_ = x + k * (w // 2)
            draw.polygon([(px_ - 7, tower_top), (px_ + 7, tower_top), (px_, tower_top - 60)], fill=colour)

    # Nave and roof.
    draw.rectangle((520, 820, 1500, base), fill=colour)
    draw.polygon([(520, 820), (1500, 820), (1010, 700)], fill=colour)
    spire(700, 110, 470, 640)
    spire(1320, 110, 470, 640)
    spire(1010, 70, 560, 700)
    for x in (560, 860, 1160, 1460):
        spire(x, 36, 700, 790)
    # Side buildings.
    draw.rectangle((300, 880, 520, base), fill=colour)
    draw.polygon([(300, 880), (520, 880), (410, 800)], fill=colour)
    draw.rectangle((1500, 870, 1720, base), fill=colour)
    draw.polygon([(1500, 870), (1720, 870), (1610, 790)], fill=colour)


def windows(draw):
    """Faint candle-lit pointed windows."""
    for x in list(range(600, 1440, 70)):
        if abs(x - 1010) < 40:
            continue
        draw.rectangle((x - 9, 880, x + 9, 940), fill=(120, 24, 16, 120))
        draw.polygon([(x - 9, 880), (x + 9, 880), (x, 860)], fill=(120, 24, 16, 120))
    # Rose window.
    draw.ellipse((985, 760, 1035, 810), fill=(140, 30, 18, 110))


far = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cathedral(ImageDraw.Draw(far), H, (10, 3, 8, 255))
img = Image.alpha_composite(img, far)
win = Image.new("RGBA", (W, H), (0, 0, 0, 0))
windows(ImageDraw.Draw(win))
win = win.filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(img, win)


def branch(draw, x, y, angle, length, width, depth):
    if depth == 0 or length < 6:
        return
    x2 = x + math.cos(angle) * length
    y2 = y - math.sin(angle) * length
    draw.line((x, y, x2, y2), fill=(2, 0, 2, 255), width=max(1, int(width)))
    for _ in range(2 if depth > 2 else 3):
        branch(draw, x2, y2, angle + rnd.uniform(-0.7, 0.7), length * rnd.uniform(0.62, 0.78),
               width * 0.68, depth - 1)


trees = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(trees)
branch(td, 90, H, math.pi / 2 + 0.08, 260, 26, 9)
branch(td, 1860, H, math.pi / 2 - 0.12, 230, 22, 9)
img = Image.alpha_composite(img, trees)

# Ground mist, crimson-tinted.
mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
mdr = ImageDraw.Draw(mist)
for _ in range(26):
    cx = rnd.randrange(-200, W + 200)
    cy = rnd.randrange(820, 1060)
    w, h = rnd.randrange(250, 600), rnd.randrange(30, 70)
    mdr.ellipse((cx - w, cy - h, cx + w, cy + h), fill=(70, 12, 22, 34))
mist = mist.filter(ImageFilter.GaussianBlur(28))
img = Image.alpha_composite(img, mist)

# Bats against the moon.
bats = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(bats)
for bx, by, s in [(1090, 300, 1.0), (1250, 420, 0.8), (1330, 270, 0.6), (1000, 430, 0.5), (1450, 360, 0.45)]:
    pts = [(-30, 0), (-18, -10), (-10, -4), (-4, -8), (0, -2), (4, -8), (10, -4), (18, -10), (30, 0),
           (16, -2), (8, 4), (0, 2), (-8, 4), (-16, -2)]
    bd.polygon([(bx + x * s * 2.2, by + y * s * 2.2) for x, y in pts], fill=(4, 0, 3, 255))
img = Image.alpha_composite(img, bats)

# Vignette.
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse((-300, -250, W + 300, H + 250), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(220))
black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
img = Image.composite(img, black, vig)

img.convert("RGB").save(out, "JPEG", quality=90, optimize=True, progressive=True)
print("wrote", out)
