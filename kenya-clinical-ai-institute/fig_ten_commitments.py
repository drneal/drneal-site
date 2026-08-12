#!/usr/bin/env python3
"""Memory aid for the ten pedagogical commitments.

Designed to be recalled, not admired. The ten are chunked into four clusters
(2 / 3 / 3 / 2), each with its own colour, glyph set and one-line compression,
because ten unstructured items sit right at the edge of working memory and four
groups do not. The footer carries the whole thing as a single sentence.

Writes ../static/img/kenya-clinical-ai/fig-ten-commitments.png
"""
import os

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "static", "img", "kenya-clinical-ai")
os.makedirs(OUT, exist_ok=True)

BG, CARD = "#080d16", "#0d1424"
INK, GREY, FAINT, LINE = "#c9d6e8", "#7f94b0", "#9AA9AE", "#1e2d45"
CY, GO, GR, VI = "#00d4f5", "#f59e0b", "#10b981", "#a78bfa"
FONT = "Helvetica, Arial, sans-serif"

# (cluster label, colour, compression, [(n, glyph, title, gist), ...])
CLUSTERS = [
    ("WHAT WE TEACH", CY, "Teach judgement", [
        (1, "scale", "Judgement, not tools",
         "If the vendor vanished overnight, would this teaching still be worth "
         "anything? If not, it is a vendor manual."),
        (2, "lens", "Scepticism is drilled",
         "Not a lecture on limitations. A trained reflex, like recognising a "
         "deteriorating patient — and it is assessed."),
    ]),
    ("HOW WE TEACH", GO, "in Kenyan cases, safely, together", [
        (5, "pin", "Kenyan cases only",
         "No vignette with insurance codes, drugs we cannot obtain, or "
         "investigations we do not have."),
        (6, "shield", "Simulation before patients",
         "Uncontroversial for central lines. It should be uncontroversial here."),
        (8, "venn", "Interprofessional by default",
         "Ward AI use is not a doctor problem or a nurse problem. The failure "
         "modes live in the handover."),
    ]),
    ("WHAT COUNTS AS PROOF", GR, "prove it or it did not happen", [
        (3, "equals", "Taught = assessed",
         "Nothing is taught that is not assessed. Nothing is assessed that was "
         "not taught."),
        (4, "nocert", "No attendance awards",
         "No certificate for having been present. This will make us unpopular "
         "and it is not negotiable."),
        (7, "doc", "The learner produces something",
         "A logbook, a critique, an evaluation, a taught session — countersigned "
         "by a named senior person."),
    ]),
    ("HOW WE KNOW IT WORKED", VI, "and measure whether it held", [
        (9, "rosette", "Faculty are certified",
         "And their teaching is observed. Nobody teaches on this programme "
         "unexamined."),
        (10, "bars", "Kirkpatrick 3 and 4",
         "Behaviour and outcomes, or we admit we do not know. Satisfaction "
         "scores are close to worthless."),
    ]),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal",
      style="normal", ls="0", op=1.0):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}" letter-spacing="{ls}" '
            f'fill-opacity="{op}">{esc(s)}</text>')


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= n:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def glyph(kind, cx, cy, col, s=1.0):
    """Small mark drawn from primitives — a distinct visual hook per commitment."""
    g, o = [], []
    st = f'stroke="{col}" stroke-width="{2.0*s:.1f}" fill="none" stroke-linecap="round"'
    if kind == "scale":                                    # judgement
        o.append(f'<line x1="{cx-14*s}" y1="{cy-8*s}" x2="{cx+14*s}" y2="{cy-8*s}" {st}/>')
        o.append(f'<line x1="{cx}" y1="{cy-12*s}" x2="{cx}" y2="{cy+9*s}" {st}/>')
        o.append(f'<line x1="{cx-7*s}" y1="{cy+12*s}" x2="{cx+7*s}" y2="{cy+12*s}" {st}/>')
        o.append(f'<line x1="{cx}" y1="{cy+9*s}" x2="{cx-4*s}" y2="{cy+12*s}" {st}/>')
        o.append(f'<line x1="{cx}" y1="{cy+9*s}" x2="{cx+4*s}" y2="{cy+12*s}" {st}/>')
        for dx in (-14*s, 14*s):                           # pans, hung from the beam
            o.append(f'<line x1="{cx+dx}" y1="{cy-8*s}" x2="{cx+dx}" y2="{cy-3*s}" {st}/>')
            o.append(f'<path d="M {cx+dx-5.5*s} {cy-3*s} A {5.5*s} {5.5*s} 0 0 0 '
                     f'{cx+dx+5.5*s} {cy-3*s} Z" {st}/>')
    elif kind == "lens":                                   # scepticism
        o.append(f'<circle cx="{cx-2*s}" cy="{cy-3*s}" r="{9*s}" {st}/>')
        o.append(f'<line x1="{cx+5*s}" y1="{cy+4*s}" x2="{cx+12*s}" y2="{cy+11*s}" {st}/>')
        o.append(t(cx-2*s, cy+1*s, "?", 11*s, col, "middle", "bold"))
    elif kind == "pin":                                    # Kenyan cases
        o.append(f'<path d="M {cx} {cy+12*s} C {cx-11*s} {cy-2*s} {cx-9*s} {cy-13*s} '
                 f'{cx} {cy-13*s} C {cx+9*s} {cy-13*s} {cx+11*s} {cy-2*s} '
                 f'{cx} {cy+12*s} Z" {st}/>')
        o.append(f'<circle cx="{cx}" cy="{cy-6*s}" r="{3.4*s}" fill="{col}"/>')
    elif kind == "shield":                                 # simulation first
        o.append(f'<path d="M {cx} {cy-12*s} L {cx+11*s} {cy-7*s} L {cx+11*s} {cy+2*s} '
                 f'C {cx+11*s} {cy+8*s} {cx+5*s} {cy+11*s} {cx} {cy+13*s} '
                 f'C {cx-5*s} {cy+11*s} {cx-11*s} {cy+8*s} {cx-11*s} {cy+2*s} '
                 f'L {cx-11*s} {cy-7*s} Z" {st}/>')
        o.append(f'<path d="M {cx-4.5*s} {cy} L {cx-1*s} {cy+4*s} L {cx+5*s} '
                 f'{cy-4*s}" {st}/>')
    elif kind == "venn":                                   # interprofessional
        o.append(f'<circle cx="{cx-5*s}" cy="{cy}" r="{9*s}" {st}/>')
        o.append(f'<circle cx="{cx+5*s}" cy="{cy}" r="{9*s}" {st}/>')
    elif kind == "equals":                                 # taught = assessed
        o.append(f'<rect x="{cx-13*s}" y="{cy-11*s}" width="{26*s}" height="{22*s}" '
                 f'rx="{4*s}" {st}/>')
        o.append(f'<line x1="{cx-6*s}" y1="{cy-3*s}" x2="{cx+6*s}" y2="{cy-3*s}" {st}/>')
        o.append(f'<line x1="{cx-6*s}" y1="{cy+3*s}" x2="{cx+6*s}" y2="{cy+3*s}" {st}/>')
    elif kind == "nocert":                                 # no attendance awards
        o.append(f'<rect x="{cx-13*s}" y="{cy-9*s}" width="{26*s}" height="{18*s}" '
                 f'rx="{3*s}" {st}/>')
        o.append(f'<line x1="{cx-7*s}" y1="{cy-3*s}" x2="{cx+7*s}" y2="{cy-3*s}" {st}/>')
        o.append(f'<line x1="{cx-7*s}" y1="{cy+2*s}" x2="{cx+2*s}" y2="{cy+2*s}" {st}/>')
        o.append(f'<line x1="{cx-16*s}" y1="{cy+13*s}" x2="{cx+16*s}" y2="{cy-13*s}" '
                 f'stroke="{col}" stroke-width="{2.6*s:.1f}" stroke-linecap="round"/>')
    elif kind == "doc":                                    # produces something
        o.append(f'<path d="M {cx-10*s} {cy-13*s} L {cx+5*s} {cy-13*s} L {cx+11*s} '
                 f'{cy-7*s} L {cx+11*s} {cy+13*s} L {cx-10*s} {cy+13*s} Z" {st}/>')
        for i, dy in enumerate((-4, 1)):
            o.append(f'<line x1="{cx-5*s}" y1="{cy+dy*s}" x2="{cx+6*s}" '
                     f'y2="{cy+dy*s}" {st}/>')
        o.append(f'<path d="M {cx-5*s} {cy+8*s} q {4*s} {-5*s} {7*s} 0 q {2*s} {3*s} '
                 f'{4*s} {-2*s}" {st}/>')
    elif kind == "rosette":                                # certified faculty
        o.append(f'<circle cx="{cx}" cy="{cy-4*s}" r="{9*s}" {st}/>')
        o.append(f'<path d="M {cx-6*s} {cy+3*s} L {cx-8*s} {cy+14*s} L {cx-2*s} '
                 f'{cy+10*s}" {st}/>')
        o.append(f'<path d="M {cx+6*s} {cy+3*s} L {cx+8*s} {cy+14*s} L {cx+2*s} '
                 f'{cy+10*s}" {st}/>')
    elif kind == "bars":                                   # Kirkpatrick 3 and 4
        for i, h in enumerate((5, 9, 14, 19)):
            x = cx - 15*s + i * 9*s
            faint = i < 2
            o.append(f'<rect x="{x}" y="{cy+10*s-h*s}" width="{6*s}" height="{h*s}" '
                     f'rx="{1.5*s}" fill="{col}" '
                     f'fill-opacity="{0.28 if faint else 1.0}"/>')
    return g + o


def main():
    W, H = 1420, 860
    M, GAP = 30, 16
    CW = (W - 2*M - 3*GAP) / 4
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']

    o.append(t(W/2, 48, "THE PEDAGOGY I WOULD INSIST ON", 15, INK, "middle",
               "bold", ls="3.0"))
    o.append(t(W/2, 74, "Ten commitments, written into the founding documents so that a "
               "future director has to argue publicly to abandon them.",
               11.6, GREY, "middle"))
    o.append(t(W/2, 95, "Grouped in four, because ten loose items do not stay in the head.",
               10.2, FAINT, "middle", style="italic"))

    HEAD_Y, CARD_Y = 124, 176
    CARD_H, CARD_GAP = 168, 16
    BLOCK_H = 3*CARD_H + 2*CARD_GAP              # tallest column: 3 cards
    for ci, (label, col, comp, items) in enumerate(CLUSTERS):
        x = M + ci * (CW + GAP)

        o.append(f'<rect x="{x}" y="{HEAD_Y - 22}" width="{CW}" height="{BLOCK_H + 96}" '
                 f'rx="10" fill="#0a1020" stroke="{col}" stroke-width="1" '
                 f'stroke-opacity="0.35"/>')
        o.append(f'<rect x="{x}" y="{HEAD_Y - 22}" width="{CW}" height="4" rx="2" '
                 f'fill="{col}"/>')
        o.append(t(x + CW/2, HEAD_Y + 6, label, 11.4, col, "middle", "bold", ls="1.6"))
        o.append(t(x + CW/2, HEAD_Y + 26, f"“{comp}”", 10.4, FAINT, "middle",
                   style="italic"))

        # cards are a fixed height in every column; short columns are centred
        # vertically rather than stretched, which otherwise leaves dead space
        stack = len(items) * CARD_H + (len(items) - 1) * CARD_GAP
        y0 = CARD_Y + (BLOCK_H - stack) / 2
        for k, (n, gl, title, gist) in enumerate(items):
            y = y0 + k * (CARD_H + CARD_GAP)
            o.append(f'<rect x="{x+12}" y="{y}" width="{CW-24}" height="{CARD_H}" rx="8" '
                     f'fill="{CARD}" stroke="{col}" stroke-width="1.4" '
                     f'stroke-opacity="0.55"/>')
            o.append(t(x + 30, y + 44, str(n), 34, col, "start", "bold", op=0.38))
            o += glyph(gl, x + CW - 46, y + 34, col, 1.0)
            for j, ln in enumerate(wrap(title, 22)):
                o.append(t(x + 30, y + 68 + j*19, ln, 13.2, INK, "start", "bold"))
            gy = y + 68 + len(wrap(title, 22))*19 + 10
            for j, ln in enumerate(wrap(gist, 38)):
                o.append(t(x + 30, gy + j*16, ln, 10.0, GREY))

    fy = HEAD_Y - 22 + BLOCK_H + 96 + 22
    o.append(f'<rect x="{M}" y="{fy}" width="{W-2*M}" height="66" rx="8" '
             f'fill="#101a2e" stroke="{LINE}" stroke-width="1"/>')
    parts = [(c[2], c[1]) for c in CLUSTERS]
    total = " · ".join(p[0] for p in parts)
    o.append(t(W/2, fy + 24, "THE WHOLE THING IN ONE SENTENCE", 9.6, FAINT,
               "middle", "bold", ls="1.6"))
    # each segment is centred under its own column. No text-width estimation and
    # no tspans (cairosvg mis-positions those under a centred anchor), and it
    # ties each phrase to the cluster it compresses.
    for i, (txt_, col) in enumerate(parts):
        colx = M + i * (CW + GAP) + CW/2
        for j, ln in enumerate(wrap(txt_, 36)):     # keeps each phrase on one line
            o.append(t(colx, fy + 46 + j*17, ln, 12.6, col, "middle", "bold"))
        if i < len(parts) - 1:
            o.append(t(colx + CW/2 + GAP/2, fy + 46, "·", 13.0, GREY, "middle"))

    o.append(t(W/2, H - 12, "Another Arrow in the Quiver — Kenya Institute for Clinical "
               "Artificial Intelligence · drnealaggarwal.info", 8.8, FAINT, "middle"))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(o) + "\n</svg>\n")
    p = os.path.join(OUT, "fig-ten-commitments")
    open(p + ".svg", "w").write(svg)
    cairosvg.svg2png(url=p + ".svg", write_to=p + ".png", scale=1.6)
    os.remove(p + ".svg")
    print(f"  wrote {p}.png  {os.path.getsize(p + '.png')//1024} KB")
    print("  full sentence:", total)


if __name__ == "__main__":
    main()
