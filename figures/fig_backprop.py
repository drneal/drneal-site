#!/usr/bin/env python3
"""Three figures for the backpropagation post.

  fig-nudge.png      what a derivative is: a ratio of nudges
  fig-network.png    the worked 1-1-1 network, forward values and backward deltas
  fig-branching.png  why the contributions of two paths are added

Every number shown matches the worked example in the post, which was itself
checked against numerical gradients.

Two rendering constraints learned the hard way, both worth keeping:

  * Unicode subscripts (₁ ₂ ₃) are dropped by the bold sans face this renderer
    falls back to, but survive in the mono face. So anything carrying a
    subscript is set in MONO. Never put a subscript in a bold FONT string.
  * Fractions are drawn with a real rule line and two centred texts. Building
    them out of box-drawing characters relies on monospace column alignment
    that does not survive font fallback.

Writes ../static/img/backprop/
"""
import math
import os

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "static", "img", "backprop")
os.makedirs(OUT, exist_ok=True)

BG, CARD = "#080d16", "#0d1424"
INK, GREY, FAINT, LINE = "#c9d6e8", "#7f94b0", "#9AA9AE", "#1e2d45"
CY, GO, RD, GR, VI = "#00d4f5", "#f59e0b", "#f87171", "#10b981", "#a78bfa"
FONT = "Helvetica, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Menlo, Consolas, monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal",
      style="normal", ls="0", font=None, op=1.0):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font or FONT}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" letter-spacing="{ls}" '
            f'fill-opacity="{op}">{esc(s)}</text>')


def box(x, y, w, h, stroke=LINE, fill=CARD, sw=1.4, r=8):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def arrow(x1, y1, x2, y2, col, sw=2.0, head=9):
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - head * 0.85 * math.cos(ang), y2 - head * 0.85 * math.sin(ang)
    p2 = (x2 - head * math.cos(ang - 0.42), y2 - head * math.sin(ang - 0.42))
    p3 = (x2 - head * math.cos(ang + 0.42), y2 - head * math.sin(ang + 0.42))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{col}" stroke-width="{sw}"/>'
            f'<path d="M {x2:.1f} {y2:.1f} L {p2[0]:.1f} {p2[1]:.1f} '
            f'L {p3[0]:.1f} {p3[1]:.1f} Z" fill="{col}"/>')


def fraction(cx, cy, num, den, size=11.5, col=GREY, half=52):
    """A real fraction: two centred texts and a rule between them."""
    return [
        t(cx, cy - 7, num, size, col, "middle"),
        f'<line x1="{cx-half}" y1="{cy}" x2="{cx+half}" y2="{cy}" '
        f'stroke="{col}" stroke-width="1.2"/>',
        t(cx, cy + 19, den, size, col, "middle"),
    ]


def save(name, W, H, body, scale=1.6):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(body) + "\n</svg>\n")
    p = os.path.join(OUT, name)
    open(p + ".svg", "w").write(svg)
    cairosvg.svg2png(url=p + ".svg", write_to=p + ".png", scale=scale)
    os.remove(p + ".svg")
    print(f"  {name}.png  {os.path.getsize(p + '.png')//1024} KB")


# ───────────────────────── 1. what a derivative is ───────────────────────────
def fig_nudge():
    W, H = 1180, 700
    o = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    o.append(t(W / 2, 44, "A DERIVATIVE IS A RATIO OF NUDGES", 14, INK,
               "middle", "bold", ls="2.6"))
    o.append(t(W / 2, 70, "Nudge the side of a square by a whisker. The area moves "
               "six times as far. That six is the derivative.", 11.6, GREY, "middle"))

    L, R, TOP, BOT = 160, 640, 122, 470
    x0, x1, y0, y1 = 1.6, 4.2, 0.0, 20.0

    def px(v): return L + (v - x0) / (x1 - x0) * (R - L)
    def py(v): return BOT - (v - y0) / (y1 - y0) * (BOT - TOP)

    for v in range(0, 21, 5):
        o.append(f'<line x1="{L}" y1="{py(v):.1f}" x2="{R}" y2="{py(v):.1f}" '
                 f'stroke="{LINE}" stroke-width="1"/>')
        o.append(t(L - 12, py(v) + 4, str(v), 10, GREY, "end"))
    for v in (2, 3, 4):
        o.append(f'<line x1="{px(v):.1f}" y1="{BOT}" x2="{px(v):.1f}" y2="{BOT+6}" '
                 f'stroke="{LINE}" stroke-width="1"/>')
        o.append(t(px(v), BOT + 22, str(v), 10, GREY, "middle"))
    o.append(t((L + R) / 2, BOT + 46, "SIDE LENGTH", 10.4, FAINT, "middle",
               "bold", ls="1.4"))
    o.append(t(L - 12, TOP - 22, "AREA", 10.4, FAINT, "end", "bold", ls="1.4"))

    pts, v = [], x0
    while v <= x1 + 1e-9:
        pts.append(f"{px(v):.1f},{py(v*v):.1f}")
        v += 0.02
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{CY}" '
             f'stroke-width="2.6"/>')
    # label parked well clear of the curve
    o.append(t(L + 22, TOP + 34, "the curve is side × side", 10.6, CY, "start", "bold"))

    s, h = 3.0, 0.9
    ax, ay, bx, by = px(s), py(s * s), px(s + h), py((s + h) ** 2)
    o.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{ay:.1f}" '
             f'stroke="{GO}" stroke-width="2.4"/>')
    o.append(f'<line x1="{bx:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
             f'stroke="{GR}" stroke-width="2.4"/>')
    o.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
             f'stroke="{INK}" stroke-width="1.6" stroke-dasharray="5,4"/>')
    for cx_, cy_ in ((ax, ay), (bx, by)):
        o.append(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="6" fill="{BG}" '
                 f'stroke="{CY}" stroke-width="2.6"/>')
    o.append(t((ax + bx) / 2, ay + 26, "nudge the side", 11, GO, "middle", "bold"))
    o.append(t((ax + bx) / 2, ay + 42, "by a tiny h", 10, GREY, "middle"))
    o.append(t(bx + 16, (ay + by) / 2 - 4, "area moves", 11, GR, "start", "bold"))
    o.append(t(bx + 16, (ay + by) / 2 + 12, "about 6 × h", 10, GREY, "start"))

    # the algebra, with a drawn fraction rather than typed rules
    kx, kw = 700, 440
    o.append(box(kx, 120, kw, 388, LINE, "#0b1220", 1))
    o.append(t(kx + 24, 152, "THE SAME THING, EXACTLY", 10.4, FAINT, "start",
               "bold", ls="1.6"))

    o.append(t(kx + 24, 194, "(s + h)²  =  s² + 2sh + h²", 13.4, INK, "start", "bold"))
    o.append(t(kx + 24, 230, "so the area changed by  2sh + h²", 11.6, GREY))

    fy = 296
    o += fraction(kx + 96, fy, "change in area", "change in side", 11, GREY, 58)
    o.append(t(kx + 176, fy + 5, "=", 13, GREY, "middle"))
    o += fraction(kx + 240, fy, "2sh + h²", "h", 11.5, GREY, 34)
    o.append(t(kx + 300, fy + 5, "=", 13, GREY, "middle"))
    o.append(t(kx + 322, fy + 5, "2s + h", 13, INK, "start", "bold"))

    o.append(t(kx + 24, 380, "now shrink h towards nothing:", 11.4, GREY))
    o.append(t(kx + 24, 414, "the h disappears and 2s is left", 13, CY, "start", "bold"))
    o.append(t(kx + 24, 462, "at s = 3   →   6", 18, GO, "start", "bold"))
    o.append(t(kx + 24, 486, "which is what the arithmetic showed", 10, FAINT, "start",
               style="italic"))

    o.append(box(24, 548, W - 48, 90, LINE, "#101a2e", 1))
    o.append(t(48, 580, "No rule was looked up. We wrote down what a nudge does, "
               "divided, and kept what survived as the nudge shrank.", 11.6, INK))
    o.append(t(48, 604, "Every derivative in the post is obtainable the same way — "
               "and every one is checked against an actual nudge.", 11, GREY))
    o.append(t(48, 626, "The triangle here is drawn far larger than a real nudge, "
               "so that you can see it.", 10, FAINT, style="italic"))
    save("fig-nudge", W, H, o)


# ─────────────────── 2. the worked network, both directions ──────────────────
def fig_network():
    W, H = 1320, 640
    o = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    o.append(t(W / 2, 42, "THE WORKED NETWORK, IN BOTH DIRECTIONS", 14, INK,
               "middle", "bold", ls="2.6"))
    o.append(t(W / 2, 68, "Forward along the top: the numbers. Backward along the "
               "bottom: how much the cost cares about each one.", 11.6, GREY, "middle"))

    # names carry subscripts, so they are set in MONO (see module docstring)
    nodes = [("x",  "the input",   "2.0000", CY,   60),
             ("z1", "w1·x + b1",   "1.0000", GO,  270),
             ("a1", "squash(z1)",  "0.7311", GO,  480),
             ("z2", "w2·a1 + b2",  "0.7311", RD,  690),
             ("a2", "squash(z2)",  "0.6750", RD,  900),
             ("C",  "(a2 − y)²",   "0.1056", VI, 1130)]
    NY, NW, NH = 148, 150, 96

    for i, (name, sub, val, col, x) in enumerate(nodes):
        o.append(box(x, NY, NW, NH, col, CARD, 1.8))
        o.append(t(x + NW / 2, NY + 34, name, 21, col, "middle", "bold", font=MONO))
        o.append(t(x + NW / 2, NY + 56, sub, 10, GREY, "middle", font=MONO))
        o.append(t(x + NW / 2, NY + 80, val, 14, INK, "middle", "bold", font=MONO))
        if i:
            o.append(arrow(nodes[i - 1][4] + NW + 6, NY + 30, x - 6, NY + 30, CY, 2.2))

    for lab, x in [("× w1 = 0.5", 220), ("squash", 430), ("× w2 = 1.0", 640),
                   ("squash", 850), ("score it", 1075)]:
        o.append(t(x, NY - 16, lab, 10, CY, "middle", font=MONO))
    o.append(t(60, NY - 42, "FORWARD  →", 11.4, CY, "start", "bold", ls="1.8"))

    BY = NY + NH + 64
    for x, lab, sub, col in [(270, "δ1 = −0.02803", "how much C cares about z1", GO),
                             (690, "δ2 = −0.14257", "how much C cares about z2", RD)]:
        o.append(box(x - 24, BY, NW + 48, 62, col, "#0b1220", 1.6))
        o.append(t(x + NW / 2, BY + 26, lab, 13.4, col, "middle", "bold", font=MONO))
        o.append(t(x + NW / 2, BY + 46, sub, 9.2, GREY, "middle"))
        o.append(f'<line x1="{x + NW/2}" y1="{NY + NH}" x2="{x + NW/2}" y2="{BY}" '
                 f'stroke="{col}" stroke-width="1.2" stroke-dasharray="3,4"/>')

    AY = BY + 92
    for x1_, x2_ in ((1130, 900), (900, 690), (690, 480), (480, 270)):
        o.append(arrow(x1_ - 6, AY, x2_ + NW + 6, AY, RD, 2.2))
    o.append(t(1215, AY + 4, "BACKWARD", 11.4, RD, "start", "bold", ls="1.8"))
    for x, lab in [(1015, "× 2(a2−y)"), (795, "× a2(1−a2)"),
                   (585, "× w2"), (375, "× a1(1−a1)")]:
        o.append(t(x, AY + 22, lab, 10, RD, "middle", font=MONO))

    ay0 = AY + 52
    o.append(t(60, ay0, "WHAT WE WANTED ALL ALONG", 10.4, FAINT, "start",
               "bold", ls="1.8"))
    for lab, val, how, col, x in [("dC/dw1", "−0.05606", "= δ1 × x", GO, 60),
                                  ("dC/db1", "−0.02803", "= δ1", GO, 380),
                                  ("dC/dw2", "−0.10423", "= δ2 × a1", RD, 700),
                                  ("dC/db2", "−0.14257", "= δ2", RD, 1020)]:
        o.append(box(x, ay0 + 16, 240, 64, col, CARD, 1.4))
        o.append(t(x + 16, ay0 + 42, lab, 12.4, col, "start", "bold", font=MONO))
        o.append(t(x + 224, ay0 + 42, val, 13.4, INK, "end", "bold", font=MONO))
        o.append(t(x + 16, ay0 + 62, how, 9.8, GREY, "start", font=MONO))

    o.append(t(W / 2, H - 18, "Only two moves exist: step back through a squash "
               "(multiply by a(1−a)), and step back through a weight (multiply by w).",
               10.6, FAINT, "middle"))
    save("fig-network", W, H, o)


# ───────────────────────── 3. why paths are added ────────────────────────────
def fig_branching():
    W, H = 1180, 660
    o = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    o.append(t(W / 2, 42, "WHEN A NEURON FEEDS TWO OTHERS, ADD THE PATHS", 14, INK,
               "middle", "bold", ls="2.4"))
    o.append(t(W / 2, 68, "One nudge, two routes to the cost. Both arrive. Neither "
               "cancels the other.", 11.6, GREY, "middle"))

    o.append(box(70, 240, 170, 100, GO, CARD, 1.8))
    o.append(t(155, 278, "a1", 22, GO, "middle", "bold", font=MONO))
    o.append(t(155, 302, "nudge it", 10.4, GREY, "middle"))
    o.append(t(155, 320, "by a tiny h", 10.4, GREY, "middle"))

    for x, y, dl, wl, col, side in [(500, 118, "δ2", "w2", RD, -1),
                                    (500, 362, "δ3", "w3", VI, +1)]:
        o.append(box(x, y, 180, 100, col, CARD, 1.8))
        o.append(t(x + 90, y + 40, dl, 21, col, "middle", "bold", font=MONO))
        o.append(t(x + 90, y + 64, "an output neuron", 10, GREY, "middle"))
        o.append(t(x + 90, y + 82, "and its error signal", 9.6, FAINT, "middle"))

        o.append(arrow(248, 282, x - 8, y + 54, col, 2.2))
        mx, my = (248 + x) / 2, (282 + y + 54) / 2
        o.append(t(mx, my + (-26 if side < 0 else 30),
                   f"through {wl}", 11, col, "middle", "bold", font=MONO))
        o.append(t(mx, my + (-10 if side < 0 else 46),
                   f"C moves by {dl}·{wl}·h", 10, GREY, "middle", font=MONO))
        o.append(arrow(x + 186, y + 54, 892, 282 + side * 8, col, 2.2))

    o.append(box(900, 240, 170, 100, CY, CARD, 1.8))
    o.append(t(985, 288, "C", 24, CY, "middle", "bold", font=MONO))
    o.append(t(985, 312, "one number", 10.4, GREY, "middle"))

    fy = 496
    o.append(box(24, fy, W - 48, 142, LINE, "#101a2e", 1))
    o.append(t(48, fy + 30, "The cost is one number, and both effects land on it. "
               "So the total change is the sum of the two changes:", 11.6, INK))
    o.append(t(W / 2, fy + 68, "total change in C   ≈   δ2·w2·h  +  δ3·w3·h",
               15.5, INK, "middle", "bold", font=MONO))
    o.append(t(W / 2, fy + 100, "divide by h   →   dC/da1  =  δ2·w2  +  δ3·w3",
               15.5, GO, "middle", "bold", font=MONO))
    o.append(t(W / 2, fy + 126, "Two taps filling one bath: the level rises at the "
               "sum of the two rates.", 10.4, FAINT, "middle", style="italic"))
    save("fig-branching", W, H, o)


if __name__ == "__main__":
    fig_nudge()
    fig_network()
    fig_branching()
