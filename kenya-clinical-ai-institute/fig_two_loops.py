#!/usr/bin/env python3
"""The two loops: Delegation/Diligence outside, Description/Discernment inside.

Draft for review — not yet referenced by any post.

Colours are kept consistent with fig_4d_structure.py so the same competency is
the same colour everywhere on the site: Delegation cyan, Description amber,
Discernment red, Diligence green.

Writes ../static/img/kenya-clinical-ai/fig-two-loops.png
"""
import math
import os

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "static", "img", "kenya-clinical-ai")
os.makedirs(OUT, exist_ok=True)

BG, CARD = "#080d16", "#0d1424"
INK, GREY, FAINT, LINE = "#c9d6e8", "#7f94b0", "#9AA9AE", "#1e2d45"
CY, GO, RD, GR = "#00d4f5", "#f59e0b", "#f87171", "#10b981"
FONT = "Helvetica, Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal",
      style="normal", ls="0", op=1.0):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}" letter-spacing="{ls}" '
            f'fill-opacity="{op}">{esc(s)}</text>')


def pt(cx, cy, r, deg):
    """Angle measured from 12 o'clock, increasing clockwise."""
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def arc(cx, cy, r, a0, a1, col, w, op=1.0):
    x0, y0 = pt(cx, cy, r, a0)
    x1, y1 = pt(cx, cy, r, a1)
    sweep = (a1 - a0) % 360
    large = 1 if sweep > 180 else 0
    # butt caps, not round: a round cap has radius w/2 and swallows the arrowhead
    return (f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" '
            f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="butt" '
            f'stroke-opacity="{op}"/>')


def arrowhead(cx, cy, r, deg, col, size=18):
    """Triangle beyond the arc's flat end, pointing the way the loop travels.

    Half-width is deliberately wider than the stroke so it reads as an arrow
    rather than a continuation of the band.
    """
    x, y = pt(cx, cy, r, deg)
    a = math.radians(deg)
    tx, ty = math.cos(a), math.sin(a)          # clockwise tangent
    nx, ny = -ty, tx
    p1 = (x + tx * size, y + ty * size)
    p2 = (x - tx * size * 0.12 + nx * size * 0.95,
          y - ty * size * 0.12 + ny * size * 0.95)
    p3 = (x - tx * size * 0.12 - nx * size * 0.95,
          y - ty * size * 0.12 - ny * size * 0.95)
    return (f'<path d="M {p1[0]:.1f} {p1[1]:.1f} L {p2[0]:.1f} {p2[1]:.1f} '
            f'L {p3[0]:.1f} {p3[1]:.1f} Z" fill="{col}"/>')


ROWS = [
    ("OUTER LOOP", None, "turns once per encounter", None, None),
    ("DELEGATION", CY, "what you decide to hand over", "CONSENT",
     "the non-delegable list, agreed before anything starts"),
    ("DILIGENCE", GR, "what you take responsibility for afterwards", "AUDIT",
     "documentation, disclosure, the signature that is yours"),
    ("INNER LOOP", None, "turns many times within one encounter", None, None),
    ("DESCRIPTION", GO, "how you ask", "HISTORY",
     "the query as handover — situation, background, constraints"),
    ("DISCERNMENT", RD, "how you judge what comes back", "EXAMINATION",
     "your own impression first, then compare, then accept or reject"),
]


def main():
    W, H = 1320, 940
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']

    o.append(t(W / 2, 46, "THE FOUR COMPETENCIES ARE NOT A LIST — THEY ARE TWO LOOPS",
               14, INK, "middle", "bold", ls="2.4"))
    o.append(t(W / 2, 72, "Consent-and-audit on the outside. History-and-examination on "
               "the inside.", 12, GREY, "middle"))

    cx, cy = 470, 500
    R1, W1 = 268, 28          # outer loop
    R2, W2 = 130, 24          # inner loop

    # faint guide ring so the annulus reads as a single field
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{(R1+R2)/2:.0f}" fill="none" '
             f'stroke="{LINE}" stroke-width="1" stroke-dasharray="2,6"/>')

    # ---- outer loop: Delegation across the top, Diligence across the bottom
    o.append(arc(cx, cy, R1, 275, 85, CY, W1))
    o.append(arrowhead(cx, cy, R1, 85, CY))
    o.append(arc(cx, cy, R1, 95, 265, GR, W1))
    o.append(arrowhead(cx, cy, R1, 265, GR))

    # ---- inner loop: Description down the left, Discernment up the right
    o.append(arc(cx, cy, R2, 185, 355, GO, W2))
    o.append(arrowhead(cx, cy, R2, 355, GO, 15))
    o.append(arc(cx, cy, R2, 5, 175, RD, W2))
    o.append(arrowhead(cx, cy, R2, 175, RD, 15))

    # ---- centre
    o.append(f'<circle cx="{cx}" cy="{cy}" r="86" fill="{CARD}" stroke="{LINE}" '
             f'stroke-width="1.4"/>')
    o.append(t(cx, cy - 8, "ONE", 15, INK, "middle", "bold", ls="2.0"))
    o.append(t(cx, cy + 14, "ENCOUNTER", 15, INK, "middle", "bold", ls="1.6"))
    o.append(t(cx, cy + 38, "one patient, one decision", 9.4, FAINT, "middle",
               style="italic"))

    # ---- outer labels, above and below the whole figure
    o.append(t(cx, cy - R1 - W1/2 - 40, "DELEGATION", 17, CY, "middle", "bold", ls="2.2"))
    o.append(t(cx, cy - R1 - W1/2 - 20, "what you decide to hand over  ·  CONSENT",
               11.4, GREY, "middle"))
    o.append(t(cx, cy + R1 + W1/2 + 32, "DILIGENCE", 17, GR, "middle", "bold", ls="2.2"))
    o.append(t(cx, cy + R1 + W1/2 + 52,
               "what you take responsibility for afterwards  ·  AUDIT",
               11.4, GREY, "middle"))

    # ---- inner labels, parked in the annulus at 9 and 3 o'clock
    band = (R2 + W2/2 + R1 - W1/2) / 2
    o.append(t(cx - band, cy - 6, "DESCRIPTION", 13, GO, "middle", "bold", ls="1.2"))
    o.append(t(cx - band, cy + 12, "how you ask", 10, GREY, "middle"))
    o.append(t(cx - band, cy + 28, "HISTORY", 9.6, GO, "middle", "bold", ls="1.0"))
    o.append(t(cx + band, cy - 6, "DISCERNMENT", 13, RD, "middle", "bold", ls="1.2"))
    o.append(t(cx + band, cy + 12, "how you judge", 10, GREY, "middle"))
    o.append(t(cx + band, cy + 28, "EXAMINATION", 9.6, RD, "middle", "bold", ls="1.0"))

    # ---- the dynamic that matters: the inner loop turns many times
    bx, by = cx + 132, cy - 200
    o.append(f'<rect x="{bx}" y="{by}" width="188" height="46" rx="23" '
             f'fill="#1a1408" stroke="{GO}" stroke-width="1.5"/>')
    o.append(t(bx + 94, by + 20, "INNER LOOP TURNS", 9.4, GO, "middle", "bold", ls="1.2"))
    o.append(t(bx + 94, by + 36, "many times per encounter", 10.4, INK, "middle"))
    o.append(f'<path d="M {bx+16} {by+46} L {cx+46} {cy-96}" stroke="{GO}" '
             f'stroke-width="1.2" stroke-dasharray="3,4" fill="none"/>')

    ox, oy = cx - 320, cy + 196
    o.append(f'<rect x="{ox}" y="{oy}" width="188" height="46" rx="23" '
             f'fill="#06140f" stroke="{GR}" stroke-width="1.5"/>')
    o.append(t(ox + 94, oy + 20, "OUTER LOOP TURNS", 9.4, GR, "middle", "bold", ls="1.2"))
    o.append(t(ox + 94, oy + 36, "once per encounter", 10.4, INK, "middle"))
    o.append(f'<path d="M {ox+172} {oy} L {cx-186} {cy+152}" stroke="{GR}" '
             f'stroke-width="1.2" stroke-dasharray="3,4" fill="none"/>')

    # ---- key on the right
    kx, ky, kw = 880, 140, 400
    for i, (name, col, gloss, clin, detail) in enumerate(ROWS):
        if col is None:
            ky += 10 if i else 0
            o.append(f'<line x1="{kx}" y1="{ky+6}" x2="{kx+kw}" y2="{ky+6}" '
                     f'stroke="{LINE}" stroke-width="1"/>')
            o.append(t(kx, ky, name, 10.4, FAINT, "start", "bold", ls="2.0"))
            o.append(t(kx + kw, ky, gloss, 10.0, GREY, "end", style="italic"))
            ky += 34
            continue
        o.append(f'<rect x="{kx}" y="{ky - 14}" width="{kw}" height="84" rx="8" '
                 f'fill="{CARD}" stroke="{col}" stroke-width="1.2" '
                 f'stroke-opacity="0.5"/>')
        o.append(f'<rect x="{kx}" y="{ky - 14}" width="5" height="84" rx="2.5" '
                 f'fill="{col}"/>')
        o.append(t(kx + 20, ky + 8, name, 13.2, col, "start", "bold", ls="1.2"))
        o.append(t(kx + kw - 18, ky + 8, clin, 11.4, INK, "end", "bold", ls="1.0"))
        o.append(t(kx + 20, ky + 30, gloss, 10.6, GREY))
        o.append(t(kx + 20, ky + 50, detail, 9.6, FAINT))
        ky += 100

    # ---- where the loops are actually taught, filling the space under the key
    ty0 = ky + 6
    o.append(t(kx, ty0, "WHERE EACH LOOP IS TAUGHT", 10.4, FAINT, "start",
               "bold", ls="2.0"))
    o.append(f'<line x1="{kx}" y1="{ty0+6}" x2="{kx+kw}" y2="{ty0+6}" '
             f'stroke="{LINE}" stroke-width="1"/>')
    units = [("Unit 1.3", CY, "Delegation boundaries — the reversibility test"),
             ("Unit 1.4", GO, "Description as clinical handover"),
             ("Unit 1.5", RD, "Discernment and the independent-impression rule"),
             ("Unit 1.6", GR, "Law, consent and documentation")]
    for j, (u, col, desc) in enumerate(units):
        yy = ty0 + 30 + j * 26
        o.append(f'<rect x="{kx}" y="{yy-11}" width="4" height="16" rx="2" fill="{col}"/>')
        o.append(t(kx + 16, yy, u, 10.6, col, "start", "bold"))
        o.append(t(kx + 78, yy, desc, 10.2, GREY))

    # ---- footer
    fy = H - 86
    o.append(f'<rect x="30" y="{fy}" width="{W-60}" height="52" rx="8" '
             f'fill="#101a2e" stroke="{LINE}" stroke-width="1"/>')
    o.append(t(W/2, fy + 22, "A clinician recognises the shape immediately. You take "
               "consent once and you audit once; you ask and judge, ask and judge, "
               "many times in between.", 11.4, INK, "middle"))
    o.append(t(W/2, fy + 40, "The failure the curriculum is built to prevent is running "
               "the inner loop without ever having closed the outer one.",
               10.6, GREY, "middle"))

    o.append(t(W/2, H - 14, "Two-loop structure from the AI Fluency Framework teaching "
               "course (Dakan & Feller) · clinical mapping mine",
               8.8, FAINT, "middle"))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(o) + "\n</svg>\n")
    p = os.path.join(OUT, "fig-two-loops")
    open(p + ".svg", "w").write(svg)
    cairosvg.svg2png(url=p + ".svg", write_to=p + ".png", scale=1.5)
    os.remove(p + ".svg")
    print(f"  wrote {p}.png  {os.path.getsize(p + '.png')//1024} KB")


if __name__ == "__main__":
    main()
