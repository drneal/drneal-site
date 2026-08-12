#!/usr/bin/env python3
"""The two loops: Delegation/Diligence outside, Description/Discernment inside.

Theme-switched exactly as figures.py is:

    python3 fig_two_loops.py                 # light / print -> ./figures/fig9-two-loops.svg
    FIGTHEME=dark python3 fig_two_loops.py   # dark / web    -> ../static/img/.../fig-two-loops.png

In the dark web palette the competencies keep the colours they carry elsewhere
on the site (Delegation cyan, Description amber, Discernment red, Diligence
green). In the light print palette the outer loop is the teal family and the
inner loop the warm family, which makes the two-loop grouping legible in a
document that will also be read in monochrome.
"""
import math
import os

THEME = os.environ.get("FIGTHEME", "light")
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
FONT = "Helvetica, Arial, sans-serif"

if THEME == "dark":
    OUT = os.path.join(SITE, "static", "img", "kenya-clinical-ai")
    BG, CARD = "#080d16", "#0d1424"
    INK, GREY, FAINT, LINE = "#c9d6e8", "#7f94b0", "#9AA9AE", "#1e2d45"
    CY, GO, RD, GR = "#00d4f5", "#f59e0b", "#f87171", "#10b981"
    TINT = {"CY": "#06202b", "GO": "#1a1408", "RD": "#1c1114", "GR": "#06140f"}
    PANEL = "#101a2e"
    TITLE = "THE FOUR COMPETENCIES ARE NOT A LIST — THEY ARE TWO LOOPS"
    FS = 1.0
else:
    OUT = os.path.join(HERE, "figures")
    BG, CARD = "#FFFFFF", "#FFFFFF"
    INK, GREY, FAINT, LINE = "#12262B", "#66787E", "#8A979C", "#D9E1E3"
    CY, GO, RD, GR = "#0B4F4A", "#B5822A", "#A63A2B", "#177A6E"
    TINT = {"CY": "#E6F0EE", "GO": "#FAF3E4", "RD": "#F7EAE7", "GR": "#E9F3F0"}
    PANEL = "#F5F8F8"
    TITLE = "FIGURE 9 — THE FOUR COMPETENCIES ARE NOT A LIST: THEY ARE TWO LOOPS"
    # the print figure is reproduced at ~170mm, so 1px of the viewBox is
    # ~0.13mm; without this the smallest labels land near 3.5pt on paper
    FS = 1.25

os.makedirs(OUT, exist_ok=True)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal",
      style="normal", ls="0", op=1.0):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size*FS:.2f}" '
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
    W, H = 1320, 960
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']

    o.append(t(W / 2, 46, TITLE, 14, INK if THEME == "dark" else GREY,
               "middle", "bold", ls="2.4"))
    o.append(t(W / 2, 72, "Consent-and-audit on the outside. History-and-examination on "
               "the inside.", 12, GREY, "middle"))

    cx, cy = 470, 500
    R1, W1 = 280, 28          # outer loop
    R2, W2 = 122, 24          # inner loop — annulus widened so the inner
                              # labels still fit once type is scaled for print

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
             f'fill="{TINT["GO"]}" stroke="{GO}" stroke-width="1.5"/>')
    o.append(t(bx + 94, by + 20, "INNER LOOP TURNS", 9.4, GO, "middle", "bold", ls="1.2"))
    o.append(t(bx + 94, by + 36, "many times per encounter", 10.4, INK, "middle"))
    o.append(f'<path d="M {bx+16} {by+46} L {cx+46} {cy-96}" stroke="{GO}" '
             f'stroke-width="1.2" stroke-dasharray="3,4" fill="none"/>')

    ox, oy = cx - 320, cy + 196
    o.append(f'<rect x="{ox}" y="{oy}" width="188" height="46" rx="23" '
             f'fill="{TINT["GR"]}" stroke="{GR}" stroke-width="1.5"/>')
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
        tint = TINT[{CY: "CY", GO: "GO", RD: "RD", GR: "GR"}[col]]
        o.append(f'<rect x="{kx}" y="{ky - 14}" width="{kw}" height="84" rx="8" '
                 f'fill="{CARD if THEME == "dark" else tint}" stroke="{col}" '
                 f'stroke-width="1.2" stroke-opacity="0.5"/>')
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
             f'fill="{PANEL}" stroke="{LINE}" stroke-width="1"/>')
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

    if THEME == "dark":
        import cairosvg
        p = os.path.join(OUT, "fig-two-loops")
        open(p + ".svg", "w").write(svg)
        cairosvg.svg2png(url=p + ".svg", write_to=p + ".png", scale=1.5)
        os.remove(p + ".svg")
        print(f"  wrote {p}.png  {os.path.getsize(p + '.png')//1024} KB")
    else:
        # WeasyPrint renders the SVG directly, as it does for every other
        # figure in the blueprint — no rasterisation step
        p = os.path.join(OUT, "fig9-two-loops.svg")
        open(p, "w").write(svg)
        print(f"  wrote {p}  {os.path.getsize(p)//1024} KB")


if __name__ == "__main__":
    main()
