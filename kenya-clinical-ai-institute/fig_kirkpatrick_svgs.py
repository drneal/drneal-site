#!/usr/bin/env python3
"""Inline SVG figures for the Kirkpatrick companion post.

Emits standalone .svg files to ./_svg/ so they can be render-checked, and the
same markup is pasted inline into
content/posts/2026-08-17-measuring-what-actually-matters.md.

Figures
  1. mindmap        — the ten pedagogical commitments as a colour-coded mind map
  2. ladder         — Kirkpatrick's four levels against Miller's pyramid
  3. backwards      — the chain of evidence, planned backwards from Level 4
  4. decay          — Level 3 decay curves, measurement windows, booster
  5. triangulation  — three Level 3 data sources and the bias each carries
  6. wedge          — the stepped-wedge rollout grid
  7. its            — segmented regression vs the naive before-and-after chart
"""
import os
import math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_svg")
os.makedirs(OUT, exist_ok=True)

# ── house palette ────────────────────────────────────────────────────────────
BG, CARD, CARD2 = "#0d1424", "#111c30", "#16233a"
LINE = "#1e2d45"
INK, GREY, DIM = "#c9d6e8", "#8ea4c0", "#6b82a0"
CY, GO, GR, VI, RD = "#00d4f5", "#f59e0b", "#10b981", "#a78bfa", "#f87171"
FONT = "Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal",
      style="normal", ls="0", op=1.0, font=FONT):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" letter-spacing="{ls}" '
            f'fill-opacity="{op}">{esc(s)}</text>')


def rect(x, y, w, h, rx=8, fill=CARD, stroke=LINE, sw=1, op=1.0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'fill-opacity="{op}"/>')


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= n:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{esc(label)}">\n{body}\n</svg>')


def write(name, s):
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(s)
    return s


# ═════════════════════════════════════════════════════════════════════════════
# GLYPHS — small figurines, boxes and diagrams, drawn at a 26x26 unit box
# ═════════════════════════════════════════════════════════════════════════════
def glyph(kind, x, y, c, s=1.0):
    """Return a small pictogram centred on (x, y). Unit box roughly 26x26."""
    g = f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" ' \
        f'stroke="{c}" fill="none" stroke-width="1.6" ' \
        f'stroke-linecap="round" stroke-linejoin="round">'
    p = ""

    if kind == "scale":            # judgement — a balance
        p = (f'<path d="M0,-10 L0,8"/><path d="M-9,-6 L9,-6"/>'
             f'<path d="M-9,-6 L-13,2 L-5,2 Z" fill="{c}" fill-opacity="0.25"/>'
             f'<path d="M9,-6 L5,2 L13,2 Z" fill="{c}" fill-opacity="0.25"/>'
             f'<path d="M-6,8 L6,8"/><circle cx="0" cy="-11" r="1.8" fill="{c}"/>')

    elif kind == "lens":           # scepticism — magnifier over a flaw
        p = (f'<circle cx="-2" cy="-2" r="7.5"/><path d="M3.5,3.5 L10,10"/>'
             f'<path d="M-5,-2 L-2,1 L2,-5" stroke="{RD}"/>')

    elif kind == "pin":            # Kenyan cases — map pin
        p = (f'<path d="M0,10 C0,10 8,0 8,-4 A8,8 0 1,0 -8,-4 C-8,0 0,10 0,10 Z" '
             f'fill="{c}" fill-opacity="0.18"/><circle cx="0" cy="-4" r="3"/>')

    elif kind == "shield":         # simulation before patients
        p = (f'<path d="M0,-10 L9,-6 V1 C9,7 0,11 0,11 C0,11 -9,7 -9,1 V-6 Z" '
             f'fill="{c}" fill-opacity="0.18"/>'
             f'<path d="M-4,0 L-1,3.5 L4.5,-4"/>')

    elif kind == "venn":           # interprofessional — two figurines
        p = (f'<circle cx="-5" cy="-5" r="3"/>'
             f'<path d="M-10,7 C-10,1 -8,-1 -5,-1 C-2,-1 0,1 0,7"/>'
             f'<circle cx="5" cy="-5" r="3" stroke="{GO}"/>'
             f'<path d="M0,7 C0,1 2,-1 5,-1 C8,-1 10,1 10,7" stroke="{GO}"/>'
             f'<path d="M-2.5,-8 L2.5,-8" stroke-dasharray="1.5 1.5"/>')

    elif kind == "equals":         # taught = assessed
        p = (f'<rect x="-11" y="-8" width="8" height="16" rx="2" '
             f'fill="{c}" fill-opacity="0.18"/>'
             f'<rect x="3" y="-8" width="8" height="16" rx="2" '
             f'fill="{c}" fill-opacity="0.18"/>'
             f'<path d="M-1.5,-2 L1.5,-2 M-1.5,2 L1.5,2"/>')

    elif kind == "nocert":         # attendance certificates abolished
        p = (f'<rect x="-10" y="-7" width="20" height="14" rx="2"/>'
             f'<path d="M-6,-2 L2,-2 M-6,2 L0,2"/>'
             f'<circle cx="0" cy="0" r="10.5" stroke="{RD}"/>'
             f'<path d="M-7.5,7.5 L7.5,-7.5" stroke="{RD}" stroke-width="2"/>')

    elif kind == "doc":            # the learner produces something
        p = (f'<path d="M-7,-10 H4 L8,-6 V10 H-7 Z" fill="{c}" fill-opacity="0.14"/>'
             f'<path d="M4,-10 V-6 H8"/><path d="M-4,-2 H5 M-4,2 H5 M-4,6 H1"/>'
             f'<path d="M-9,8 L-3,8" stroke="{GO}" stroke-width="2"/>')

    elif kind == "rosette":        # faculty certified
        p = (f'<circle cx="0" cy="-3" r="6.5" fill="{c}" fill-opacity="0.16"/>'
             f'<path d="M-3,3 L-5,11 L0,8.5 L5,11 L3,3"/>'
             f'<path d="M-2.5,-3.5 L-0.5,-1.5 L3,-5.5"/>')

    elif kind == "bars":           # Kirkpatrick 3 and 4
        p = (f'<rect x="-10" y="2" width="4" height="7" fill="{c}" fill-opacity="0.3"/>'
             f'<rect x="-3.5" y="-3" width="4" height="12" fill="{c}" fill-opacity="0.55"/>'
             f'<rect x="3" y="-9" width="4" height="18" fill="{c}" fill-opacity="0.85"/>'
             f'<path d="M-12,10 L11,10" stroke="{DIM}"/>')

    elif kind == "eye":
        p = (f'<path d="M-10,0 C-6,-6 6,-6 10,0 C6,6 -6,6 -10,0 Z"/>'
             f'<circle cx="0" cy="0" r="2.6" fill="{c}"/>')

    elif kind == "clip":           # chart audit
        p = (f'<rect x="-8" y="-9" width="16" height="19" rx="2" '
             f'fill="{c}" fill-opacity="0.14"/>'
             f'<rect x="-3.5" y="-12" width="7" height="4" rx="1.2" fill="{c}"/>'
             f'<path d="M-4.5,-3 L-2.5,-1 L1,-5" />'
             f'<path d="M-4.5,3 L-2.5,5 L1,1" />')

    elif kind == "log":            # sandbox logs
        p = (f'<rect x="-9" y="-8" width="18" height="16" rx="2" '
             f'fill="{c}" fill-opacity="0.14"/>'
             f'<path d="M-5.5,-4 L-2.5,-1 L-5.5,2"/><path d="M-0.5,3 H5"/>'
             f'<path d="M-9,-4.5 H9" stroke-opacity="0.4"/>')

    g += p + "</g>"
    return g


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — THE MIND MAP
# ═════════════════════════════════════════════════════════════════════════════
def fig_mindmap():
    W, H = 1240, 1040
    b = []

    # defs: gradients, arrowheads, glow
    b.append('<defs>')
    for nm, c in [("cy", CY), ("go", GO), ("gr", GR), ("vi", VI)]:
        b.append(f'<marker id="mm-{nm}" markerWidth="13" markerHeight="13" '
                 f'refX="10.5" refY="6.5" orient="auto" '
                 f'markerUnits="userSpaceOnUse">'
                 f'<path d="M1,1 L12,6.5 L1,12 z" fill="{c}"/></marker>')
        b.append(f'<linearGradient id="mmg-{nm}" x1="0" y1="0" x2="1" y2="0">'
                 f'<stop offset="0%" stop-color="{c}" stop-opacity="0.15"/>'
                 f'<stop offset="100%" stop-color="{c}" stop-opacity="0.9"/>'
                 f'</linearGradient>')
    b.append('<radialGradient id="mm-core"><stop offset="0%" stop-color="#1b2e4d"/>'
             '<stop offset="100%" stop-color="#0f1a2e"/></radialGradient>')
    b.append(f'<filter id="mm-glow" x="-60%" y="-60%" width="220%" height="220%">'
             f'<feGaussianBlur stdDeviation="6" result="bl"/>'
             f'<feMerge><feMergeNode in="bl"/><feMergeNode in="SourceGraphic"/>'
             f'</feMerge></filter>')
    b.append('</defs>')

    b.append(rect(0, 0, W, H, 14, BG, "#182742"))

    # title
    b.append(t(W / 2, 40, "THE TEN COMMITMENTS", 19, INK, "middle", "bold",
               ls="2.5", font=MONO))
    b.append(t(W / 2, 62, "the pedagogy the Institute would be founded on — "
                          "four clusters, ten promises, one of which this post is about",
               11.5, DIM, "middle"))

    CX, CY_ = 620, 512
    RX, RY = 104, 56
    CW, CH = 280, 112

    # ── clusters ────────────────────────────────────────────────────────────
    # (key, colour, label, compression, hub xy, [(n, glyph, title, gist, card y)])
    clusters = [
        ("cy", CY, "WHAT WE TEACH", "teach judgement", (430, 252), [
            (1, "scale", "Judgement, not tools",
             "If the vendor vanished overnight, would this still be worth "
             "teaching? If not, it is a manual.", 134),
            (2, "lens", "Scepticism is drilled",
             "Not a lecture on limitations. A reflex, like spotting a "
             "deteriorating patient — and it is assessed.", 300),
        ]),
        ("go", GO, "HOW WE TEACH", "in Kenyan cases, safely, together",
         (810, 252), [
            (5, "pin", "Kenyan cases only",
             "No vignette with insurance codes, drugs we cannot obtain, or "
             "investigations we do not have.", 102),
            (6, "shield", "Simulation before patients",
             "Uncontroversial for central lines. It should be uncontroversial "
             "here too.", 240),
            (8, "venn", "Interprofessional by default",
             "Ward AI use is not a doctor problem or a nurse problem. The "
             "failure modes live in the handover.", 378),
        ]),
        ("gr", GR, "WHAT COUNTS AS PROOF", "prove it or it did not happen",
         (430, 772), [
            (3, "equals", "Taught = assessed",
             "Nothing is taught that is not assessed. Nothing is assessed that "
             "was not taught.", 592),
            (4, "nocert", "No attendance awards",
             "No certificate for having been present. This will make us "
             "unpopular and it is not negotiable.", 730),
            (7, "doc", "The learner produces work",
             "A logbook, a critique, an evaluation, a taught session — "
             "countersigned by a named senior.", 868),
        ]),
        ("vi", VI, "HOW WE KNOW IT WORKED", "and measure whether it held",
         (810, 772), [
            (9, "rosette", "Faculty are certified",
             "And their teaching is observed. Nobody teaches on this "
             "programme unexamined.", 676),
            (10, "bars", "Kirkpatrick 3 and 4",
             "Behaviour and results, or we admit we do not know. Satisfaction "
             "scores are close to worthless.", 838),
        ]),
    ]

    HW, HH = 212, 58
    LX, RXc = 26, 934          # card left-edge x for the two columns

    def bez(p0, p1, p2, p3, tt=0.5):
        u = 1 - tt
        return (u ** 3 * p0[0] + 3 * u * u * tt * p1[0] + 3 * u * tt * tt * p2[0]
                + tt ** 3 * p3[0],
                u ** 3 * p0[1] + 3 * u * u * tt * p1[1] + 3 * u * tt * tt * p2[1]
                + tt ** 3 * p3[1])

    for key, col, label, gist, (hx, hy), leaves in clusters:
        left = hx < CX
        up = hy < CY_
        # ── artery: core corner -> hub corner. Thickness ∝ cluster size ──────
        thick = 8 + 4.6 * len(leaves)
        p0 = (CX + (-0.65 * RX if left else 0.65 * RX),
              CY_ + (-0.78 * RY if up else 0.78 * RY))
        p3 = (hx + (44 if left else -44), hy + (HH / 2 + 4 if up else -HH / 2 - 4))
        p1 = (p0[0] + (-18 if left else 18), p0[1] + (-70 if up else 70))
        p2 = (p3[0] + (12 if left else -12), p3[1] + (76 if up else -76))
        d = (f"M{p0[0]:.0f},{p0[1]:.0f} C{p1[0]:.0f},{p1[1]:.0f} "
             f"{p2[0]:.0f},{p2[1]:.0f} {p3[0]:.0f},{p3[1]:.0f}")
        b.append(f'<path d="{d}" fill="none" stroke="{col}" '
                 f'stroke-width="{thick:.1f}" stroke-opacity="0.22" '
                 f'stroke-linecap="round"/>')
        b.append(f'<path d="{d}" fill="none" stroke="{col}" '
                 f'stroke-width="{thick / 3.4:.1f}" stroke-opacity="0.9" '
                 f'marker-end="url(#mm-{key})" stroke-linecap="round"/>')
        # count pip riding on the artery
        mid = bez(p0, p1, p2, p3, 0.52)
        b.append(f'<circle cx="{mid[0]:.0f}" cy="{mid[1]:.0f}" r="12" '
                 f'fill="{BG}" stroke="{col}" stroke-width="1.5"/>')
        b.append(t(mid[0], mid[1] + 4, str(len(leaves)), 12, col, "middle",
                   "bold", font=MONO))

        # ── hub ─────────────────────────────────────────────────────────────
        b.append(rect(hx - HW / 2, hy - HH / 2, HW, HH, 12, CARD2, col, 1.8))
        b.append(f'<rect x="{hx - HW / 2:.0f}" y="{hy - HH / 2:.0f}" width="6" '
                 f'height="{HH}" rx="3" fill="{col}"/>')
        b.append(t(hx + 3, hy - 6, label, 10.4, col, "middle", "bold", ls="0.9",
                   font=MONO))
        b.append(t(hx + 3, hy + 14, gist, 9.9, GREY, "middle", style="italic"))

        # ── leaves ──────────────────────────────────────────────────────────
        for n, gk, title, txt, ly in leaves:
            lx = LX if left else RXc
            cyy = ly + CH / 2
            hub_edge = hx + (-HW / 2 if left else HW / 2)
            card_edge = (lx + CW + 8) if left else (lx - 8)
            bmx = (card_edge + hub_edge) / 2
            bd = (f"M{hub_edge:.0f},{hy:.0f} C{bmx:.0f},{hy:.0f} "
                  f"{bmx:.0f},{cyy:.0f} {card_edge:.0f},{cyy:.0f}")
            hot = (n == 10)
            b.append(f'<path d="{bd}" fill="none" stroke="{col}" '
                     f'stroke-width="{5.2 if hot else 2.2 + 0.9 * (n % 3)}" '
                     f'stroke-opacity="{0.95 if hot else 0.55}" '
                     f'marker-end="url(#mm-{key})"/>')

            # card
            hh_ = CH + (22 if hot else 0)
            if hot:
                b.append(f'<g filter="url(#mm-glow)">'
                         f'{rect(lx, ly, CW, hh_, 11, "#15243c", col, 2.4)}</g>')
            else:
                b.append(rect(lx, ly, CW, hh_, 11, CARD, LINE, 1))
            b.append(f'<rect x="{lx:.0f}" y="{ly:.0f}" width="{CW}" height="3.5" '
                     f'rx="1.75" fill="{col}" fill-opacity="{1 if hot else 0.55}"/>')
            b.append(f'<circle cx="{lx + 27:.0f}" cy="{ly + 30:.0f}" r="14" '
                     f'fill="{col}" fill-opacity="0.16" stroke="{col}" '
                     f'stroke-width="1.4"/>')
            b.append(t(lx + 27, ly + 34.5, str(n), 12.5, col, "middle", "bold",
                       font=MONO))
            b.append(glyph(gk, lx + CW - 28, ly + 32, col, 0.98))
            b.append(t(lx + 50, ly + 35, title, 12.8, INK, "start", "bold"))
            for i, ln in enumerate(wrap(txt, 47)):
                b.append(t(lx + 16, ly + 60 + i * 14.5, ln, 10.3, GREY))
            if hot:
                b.append(t(lx + 16, ly + CH + 12,
                           "▸ this post unpacks this one, completely",
                           10.3, col, "start", "bold"))

    # ── core ────────────────────────────────────────────────────────────────
    b.append('<g filter="url(#mm-glow)">')
    b.append(f'<ellipse cx="{CX}" cy="{CY_}" rx="{RX}" ry="{RY}" '
             f'fill="url(#mm-core)" stroke="#31507f" stroke-width="2"/>')
    b.append('</g>')
    b.append(t(CX, CY_ - 12, "TEN", 24, INK, "middle", "bold", ls="5", font=MONO))
    b.append(t(CX, CY_ + 11, "COMMITMENTS", 14.5, INK, "middle", "bold", ls="2",
               font=MONO))
    b.append(t(CX, CY_ + 32, "written into the founding documents", 9.4, DIM,
               "middle", style="italic"))

    # footer sentence
    fy = H - 26
    b.append(f'<line x1="40" y1="{fy - 26}" x2="{W - 40}" y2="{fy - 26}" '
             f'stroke="{LINE}"/>')
    parts = [("teach judgement", CY),
             ("in Kenyan cases, safely, together", GO),
             ("prove it or it did not happen", GR),
             ("and measure whether it held", VI)]
    # fixed slots, each phrase centred in its own slot — no reliance on text flow
    AVAIL, GAP = 1120, 30
    chars = sum(len(s) for s, _ in parts)
    span = AVAIL - GAP * (len(parts) - 1)
    cur = (W - AVAIL) / 2
    for i, (s, c) in enumerate(parts):
        w_ = len(s) / chars * span
        b.append(f'<text x="{cur + w_ / 2:.1f}" y="{fy}" font-family="{FONT}" '
                 f'font-size="13" fill="{c}" text-anchor="middle" '
                 f'font-weight="bold" font-style="italic">{esc(s)}</text>')
        cur += w_
        if i < len(parts) - 1:
            b.append(f'<circle cx="{cur + GAP / 2:.1f}" cy="{fy - 4}" r="2.4" '
                     f'fill="{DIM}"/>')
            cur += GAP
    return write("mindmap", svg(W, H, "\n".join(b),
                 "Mind map of the ten pedagogical commitments in four colour-coded "
                 "clusters — what we teach, how we teach, what counts as proof, "
                 "and how we know it worked — with commitment ten, Kirkpatrick 3 "
                 "and 4, highlighted"))


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — THE LADDER, WITH MILLER ALONGSIDE
# ═════════════════════════════════════════════════════════════════════════════
def fig_ladder():
    W, H = 1010, 646
    b = ['<defs>'
         f'<marker id="ld-a" markerWidth="10" markerHeight="10" refX="8" '
         f'refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="{DIM}"/>'
         f'</marker>'
         f'<marker id="ld-r" markerWidth="10" markerHeight="10" refX="8" '
         f'refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="{RD}"/>'
         f'</marker></defs>']
    b.append(rect(0, 0, W, H, 14, BG, "#182742"))
    b.append(t(W / 2, 36, "THE FOUR LEVELS — AND WHAT EACH ONE ACTUALLY ASKS",
               16, INK, "middle", "bold", ls="1.6", font=MONO))
    b.append(t(W / 2, 57, "climbing costs more at every step; the answers get "
                          "more useful at exactly the same rate",
               11, DIM, "middle", style="italic"))

    levels = [
        (1, "REACTION", "Did they like it?", RD,
         "Happy sheets. Attendance. Star ratings.",
         "Correlates poorly with anything. Collect it to catch a broken "
         "room, not to claim an effect.", "—"),
        (2, "LEARNING", "Did they learn it?", GO,
         "MCQ, OSCE, AI-OSCE, simulation scores.",
         "Real, but a classroom fact. Proves capability under observation, "
         "not conduct on a Tuesday ward round.", "KNOWS · KNOWS HOW · SHOWS HOW"),
        (3, "BEHAVIOUR", "Do they do it at work?", CY,
         "Observation, chart audit, interaction logs.",
         "The first level that is about practice. Costly, awkward, and the "
         "point of the whole exercise.", "DOES"),
        (4, "RESULTS", "Did the patient benefit?", GR,
         "Facility indicators, safety incidents, escalation times.",
         "What everybody claims and almost nobody measures. Requires a "
         "design, agreed before you start.", "PATIENT & SYSTEM OUTCOMES"),
    ]

    x0, base, sw, step = 104, 506, 216, 44
    for i, (n, name, q, col, how, note, miller) in enumerate(levels):
        x = x0 + i * sw
        ch = 186 + i * step
        y = base - ch
        b.append(rect(x, y, sw - 16, ch, 10, CARD, col, 1.6))
        b.append(f'<rect x="{x}" y="{y}" width="{sw - 16}" height="4" rx="2" '
                 f'fill="{col}"/>')
        b.append(t(x + 16, y + 30, f"LEVEL {n}", 11, col, "start", "bold",
                   ls="1.4", font=MONO))
        b.append(t(x + 16, y + 54, name, 17, INK, "start", "bold", ls="0.6"))
        b.append(t(x + 16, y + 75, q, 11.8, col, "start", style="italic"))
        yy = y + 100
        for j, ln in enumerate(wrap(how, 31)):
            b.append(t(x + 16, yy + j * 13, ln, 9.9, GREY))
        yy += len(wrap(how, 31)) * 13 + 12
        b.append(f'<line x1="{x + 16}" y1="{yy - 8}" x2="{x + sw - 32}" '
                 f'y2="{yy - 8}" stroke="{LINE}"/>')
        for j, ln in enumerate(wrap(note, 32)):
            b.append(t(x + 16, yy + 8 + j * 13, ln, 9.7, DIM, style="italic"))
        # Miller band
        b.append(rect(x, base + 16, sw - 16, 38, 7, "#0f1b2d", LINE, 1))
        ml = wrap(miller, 24)
        for j, ln in enumerate(ml):
            b.append(t(x + (sw - 16) / 2,
                       base + 34 + j * 12 + (6 if len(ml) == 1 else 0), ln, 9.2,
                       col if miller != "—" else DIM, "middle", "bold",
                       font=MONO))

    b.append(t(x0 - 14, base + 36, "MILLER", 9.5, DIM, "end", "bold", font=MONO))
    b.append(t(x0 - 14, base + 48, "level", 9.5, DIM, "end", font=MONO))

    # cost / value arrow, clear of the Miller band
    ay = base + 92
    b.append(f'<path d="M{x0},{ay} L{x0 + 4 * sw - 26},{ay}" '
             f'stroke="{DIM}" stroke-width="1.6" marker-end="url(#ld-a)"/>')
    b.append(t(x0 + 4, ay + 20, "cheap · fast · nearly meaningless", 10.2, DIM))
    b.append(t(x0 + 4 * sw - 32, ay + 20,
               "expensive · slow · the only evidence worth having",
               10.2, GR, "end"))

    # the gap warning, above the cards
    gx = x0 + 2 * sw - 8
    gy = base - 186 - 2 * step - 24
    b.append(f'<path d="M{gx - 22},{gy} L{gx + 10},{gy}" stroke="{RD}" '
             f'stroke-width="2.2" stroke-dasharray="5 4" '
             f'marker-end="url(#ld-r)"/>')
    b.append(t(gx - 6, gy - 12, "THE GAP WHERE MOST PROGRAMMES STOP", 10, RD,
               "middle", "bold", font=MONO))
    return write("ladder", svg(W, H, "\n".join(b),
                 "Kirkpatrick's four levels drawn as an ascending staircase — "
                 "reaction, learning, behaviour, results — with Miller's pyramid "
                 "levels mapped underneath and a marker showing where most "
                 "programmes stop"))


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — PLAN BACKWARDS
# ═════════════════════════════════════════════════════════════════════════════
def fig_backwards():
    W, H = 940, 470
    b = ['<defs>'
         f'<marker id="bw-g" markerWidth="10" markerHeight="10" refX="8" '
         f'refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="{GR}"/>'
         f'</marker>'
         f'<marker id="bw-c" markerWidth="10" markerHeight="10" refX="8" '
         f'refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="{CY}"/>'
         f'</marker></defs>']
    b.append(rect(0, 0, W, H, 14, BG, "#182742"))
    b.append(t(W / 2, 36, "DESIGN RUNS RIGHT TO LEFT. EVIDENCE RUNS LEFT TO RIGHT.",
               15, INK, "middle", "bold", ls="1.4", font=MONO))
    b.append(t(W / 2, 57, "you choose the Level 4 indicator first, then work "
                          "backwards to what you teach on Monday morning",
               11, DIM, "middle", style="italic"))

    cards = [
        ("CURRICULUM", "What we teach\non Monday morning", CY,
         "the independent-impression rule; naming the modality; error drills"),
        ("LEVEL 2", "What they can do\nunder observation", CY,
         "AI-OSCE with a seeded error; conjunctive pass on detection"),
        ("LEVEL 3", "What they actually do\nin the workplace", GO,
         "observed encounters, chart audit, interaction logs at 3 and 12 months"),
        ("LEVEL 4", "What changes\nfor the patient", GR,
         "escalation time, documentation completeness, AI-contributed harm"),
    ]
    cw, cx0, cy0, gap = 196, 46, 130, 34
    for i, (tag, title, col, sub) in enumerate(cards):
        x = cx0 + i * (cw + gap)
        b.append(rect(x, cy0, cw, 150, 11, CARD, col, 1.6))
        b.append(f'<rect x="{x}" y="{cy0}" width="{cw}" height="4" rx="2" '
                 f'fill="{col}"/>')
        b.append(t(x + 14, cy0 + 28, tag, 11, col, "start", "bold", ls="1.3",
                   font=MONO))
        for j, ln in enumerate(title.split("\n")):
            b.append(t(x + 14, cy0 + 52 + j * 18, ln, 13.5, INK, "start", "bold"))
        for j, ln in enumerate(wrap(sub, 30)):
            b.append(t(x + 14, cy0 + 100 + j * 13, ln, 9.6, GREY))
        if i < 3:
            xa = x + cw + 6
            b.append(f'<path d="M{xa},{cy0 + 75} L{xa + gap - 12},{cy0 + 75}" '
                     f'stroke="{CY}" stroke-width="2.4" marker-end="url(#bw-c)"/>')

    # backwards planning arrow, above
    ya = cy0 - 26
    b.append(f'<path d="M{cx0 + 3 * (cw + gap) + cw - 20},{ya} '
             f'L{cx0 + 20},{ya}" stroke="{GR}" stroke-width="3" '
             f'stroke-dasharray="9 5" marker-end="url(#bw-g)"/>')
    b.append(t(W / 2, ya - 10, "PLANNING — start here, at the outcome you care about",
               11, GR, "middle", "bold"))
    b.append(t(W / 2, cy0 + 176, "DELIVERY AND EVIDENCE — this is the direction "
                                 "the causal claim has to travel",
               11, CY, "middle", "bold"))

    # required drivers band
    by = 336
    b.append(rect(46, by, W - 92, 96, 11, "#131f36", VI, 1.6))
    b.append(t(66, by + 26, "REQUIRED DRIVERS", 11.5, VI, "start", "bold",
               ls="1.3", font=MONO))
    b.append(t(66, by + 44, "the reinforcement that sits under Level 3 — without "
                            "it, Level 2 never becomes Level 3", 11, GREY,
               style="italic"))
    drv = [("REINFORCE", "pocket card, sandbox prompt, ward round question"),
           ("ENCOURAGE", "named senior who asks about it and means it"),
           ("REWARD", "counts for CPD points and appraisal, visibly"),
           ("MONITOR", "audit that somebody actually reads and returns")]
    dw = (W - 132) / 4
    for i, (k, v) in enumerate(drv):
        x = 66 + i * dw
        b.append(f'<circle cx="{x + 6}" cy="{by + 62}" r="3.4" fill="{VI}"/>')
        b.append(t(x + 16, by + 66, k, 9.8, VI, "start", "bold", font=MONO))
        for j, ln in enumerate(wrap(v, 30)):
            b.append(t(x + 16, by + 80 + j * 11, ln, 9, DIM))
    return write("backwards", svg(W, H, "\n".join(b),
                 "Backwards design: the Level 4 patient outcome is chosen first "
                 "and the curriculum derived from it, while evidence and causal "
                 "claims travel in the opposite direction, with the four required "
                 "drivers shown underneath"))


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — LEVEL 3 DECAY
# ═════════════════════════════════════════════════════════════════════════════
def fig_decay():
    W, H = 940, 560
    PX, PY, PW, PH = 96, 86, 700, 330
    b = ['<defs>'
         f'<marker id="dc-a" markerWidth="12" markerHeight="12" refX="9.5" '
         f'refY="6" orient="auto" markerUnits="userSpaceOnUse">'
         f'<path d="M1,1 L11,6 L1,11 z" fill="{GR}"/></marker>'
         f'<linearGradient id="dc-band" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0%" stop-color="{RD}" stop-opacity="0.16"/>'
         f'<stop offset="100%" stop-color="{RD}" stop-opacity="0.02"/>'
         f'</linearGradient></defs>']
    b.append(rect(0, 0, W, H, 14, BG, "#182742"))
    b.append(t(W / 2, 36, "WHAT LEVEL 3 IS LOOKING FOR — AND WHEN TO LOOK",
               16, INK, "middle", "bold", ls="1.6", font=MONO))
    b.append(t(W / 2, 57, "the hypothesis: the independent-impression rule decays "
                          "fastest, so it needs the earliest booster",
               11, DIM, "middle", style="italic"))

    def X(m):   # months 0..12 -> px
        return PX + (m / 12.0) * PW

    def Y(p):   # 0..100 -> px
        return PY + PH - (p / 100.0) * PH

    # axes
    b.append(f'<line x1="{PX}" y1="{PY - 8}" x2="{PX}" y2="{PY + PH}" '
             f'stroke="{LINE}" stroke-width="1.4"/>')
    b.append(f'<line x1="{PX}" y1="{PY + PH}" x2="{PX + PW + 10}" '
             f'y2="{PY + PH}" stroke="{LINE}" stroke-width="1.4"/>')
    for p in (0, 25, 50, 75, 100):
        b.append(f'<line x1="{PX}" y1="{Y(p):.1f}" x2="{PX + PW}" y2="{Y(p):.1f}" '
                 f'stroke="{LINE}" stroke-opacity="0.55" stroke-dasharray="3 5"/>')
        b.append(t(PX - 10, Y(p) + 4, f"{p}", 9.5, DIM, "end", font=MONO))
    b.append(t(PX - 52, PY + 34, "% of", 9.6, DIM, "middle", font=MONO))
    b.append(t(PX - 52, PY + 47, "encounters", 9.6, DIM, "middle", font=MONO))
    b.append(t(PX - 52, PY + 60, "at standard", 9.6, DIM, "middle", font=MONO))

    for m, lab in [(0, "end of\ncourse"), (3, "3 months"), (6, "6"), (9, "9"),
                   (12, "12 months")]:
        b.append(f'<line x1="{X(m):.1f}" y1="{PY + PH}" x2="{X(m):.1f}" '
                 f'y2="{PY + PH + 6}" stroke="{LINE}"/>')
        for j, ln in enumerate(lab.split("\n")):
            b.append(t(X(m), PY + PH + 22 + j * 12, ln, 9.6, DIM, "middle",
                       font=MONO))

    # threshold band
    b.append(f'<rect x="{PX}" y="{Y(60):.1f}" width="{PW}" '
             f'height="{PY + PH - Y(60):.1f}" fill="url(#dc-band)"/>')
    b.append(f'<line x1="{PX}" y1="{Y(60):.1f}" x2="{PX + PW}" y2="{Y(60):.1f}" '
             f'stroke="{RD}" stroke-width="1.6" stroke-dasharray="7 4"/>')
    b.append(t(PX + 8, Y(60) - 8, "acceptable-practice threshold "
                                  "(set in advance, not after)",
               9.8, RD, "start", "bold"))

    # curves: (label, colour, half-life-ish k, floor, dashed)
    curves = [
        ("Independent impression before opening the model", CY, 0.30, 34),
        ("Naming the modality — automation / augmentation / agency", GO, 0.16, 56),
        ("Documenting that AI was used, and how", GR, 0.09, 74),
        ("Factual knowledge of what the model is", VI, 0.045, 86),
    ]
    for lab, col, k, floor in curves:
        pts = []
        for i in range(0, 121):
            m = i / 10.0
            v = floor + (96 - floor) * math.exp(-k * m)
            pts.append(f"{X(m):.1f},{Y(v):.1f}")
        b.append(f'<polyline points="{" ".join(pts)}" fill="none" '
                 f'stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>')
        vend = floor + (96 - floor) * math.exp(-k * 12)
        b.append(f'<circle cx="{X(12):.1f}" cy="{Y(vend):.1f}" r="3.6" '
                 f'fill="{col}"/>')

    # measurement windows
    for m, txt in [(3, "MEASURE"), (12, "MEASURE")]:
        b.append(f'<rect x="{X(m) - 15:.1f}" y="{PY - 8}" width="30" '
                 f'height="{PH + 8}" fill="{INK}" fill-opacity="0.05" '
                 f'stroke="{INK}" stroke-opacity="0.18"/>')
        b.append(t(X(m), PY - 16, txt, 9.4, INK, "middle", "bold", font=MONO))

    # booster — annotated from below, clear of every curve
    b.append(f'<path d="M{X(5.4):.1f},{Y(18):.1f} L{X(3.45):.1f},{Y(51):.1f}" '
             f'stroke="{GR}" stroke-width="2.2" marker-end="url(#dc-a)"/>')
    b.append(t(X(5.7), Y(18) + 4, "booster here — 45 minutes, one seeded-error "
                                  "case, not a repeat of the course",
               10.2, GR, "start", "bold"))

    # legend
    ly = PY + PH + 58
    b.append(t(PX, ly, "WHAT DECAYS, FASTEST FIRST", 10, INK, "start", "bold",
               ls="1.2", font=MONO))
    for i, (lab, col, k, floor) in enumerate(curves):
        yy = ly + 20 + i * 17
        b.append(f'<line x1="{PX}" y1="{yy - 4}" x2="{PX + 26}" y2="{yy - 4}" '
                 f'stroke="{col}" stroke-width="2.8"/>')
        b.append(t(PX + 34, yy, lab, 10.4, GREY))
        hl = math.log(2) / k
        b.append(t(PX + 600, yy, f"half-life ≈ {hl:.1f} months (hypothesised)",
                   9.6, col, "start", font=MONO))
    return write("decay", svg(W, H, "\n".join(b),
                 "Hypothesised decay curves for four trained behaviours over "
                 "twelve months, with measurement windows at three and twelve "
                 "months, an acceptable-practice threshold, and a booster placed "
                 "just after the three-month measurement"))


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — TRIANGULATION
# ═════════════════════════════════════════════════════════════════════════════
def fig_triangulation():
    W, H = 940, 560
    b = ['<defs>'
         f'<marker id="tr-a" markerWidth="10" markerHeight="10" refX="8" '
         f'refY="5" orient="auto"><path d="M0,0 L9,5 L0,10 z" fill="{DIM}"/>'
         f'</marker></defs>']
    b.append(rect(0, 0, W, H, 14, BG, "#182742"))
    b.append(t(W / 2, 36, "NO SINGLE LEVEL 3 SOURCE IS TRUSTWORTHY. THREE, "
                          "TRIANGULATED, ARE.",
               15, INK, "middle", "bold", ls="1.3", font=MONO))
    b.append(t(W / 2, 57, "each source is biased in a direction you can name in "
                          "advance — which is what makes the combination usable",
               11, DIM, "middle", style="italic"))

    srcs = [
        ("clip", "OBSERVED ENCOUNTER", CY, "mini-CEX / DOPS, trained observer",
         "Sees reasoning and disclosure. Nothing else does.",
         "HAWTHORNE — they behave well because you are watching. "
         "Ceiling effects; observer stringency is a real variance component."),
        ("doc", "CHART AUDIT", GO, "structured retrospective note review",
         "Unobtrusive, cheap at scale, covers everyone.",
         "Measures documentation, not thought. A clinician can write the "
         "right note after doing the wrong thing."),
        ("log", "SANDBOX INTERACTION LOG", GR, "consented, governed, "
                                               "purpose-limited",
         "The only source that sees the order of operations.",
         "Consent and governance are not optional. Timestamps prove "
         "sequence, never understanding."),
    ]
    cw, cx0, cy0 = 272, 46, 96
    for i, (gk, name, col, how, strength, weak) in enumerate(srcs):
        x = cx0 + i * (cw + 30)
        b.append(rect(x, cy0, cw, 214, 11, CARD, col, 1.6))
        b.append(f'<rect x="{x}" y="{cy0}" width="{cw}" height="4" rx="2" '
                 f'fill="{col}"/>')
        b.append(glyph(gk, x + 28, cy0 + 34, col, 1.0))
        b.append(t(x + 52, cy0 + 32, name, 11.5, col, "start", "bold", ls="0.8",
                   font=MONO))
        b.append(t(x + 52, cy0 + 48, how, 9.6, DIM, style="italic"))
        b.append(f'<line x1="{x + 14}" y1="{cy0 + 62}" x2="{x + cw - 14}" '
                 f'y2="{cy0 + 62}" stroke="{LINE}"/>')
        b.append(t(x + 14, cy0 + 82, "SEES", 9.4, GR, "start", "bold", font=MONO))
        for j, ln in enumerate(wrap(strength, 42)):
            b.append(t(x + 14, cy0 + 98 + j * 13, ln, 10, GREY))
        yy = cy0 + 98 + len(wrap(strength, 42)) * 13 + 12
        b.append(t(x + 14, yy, "MISSES / BIASED BY", 9.4, RD, "start", "bold",
                   font=MONO))
        for j, ln in enumerate(wrap(weak, 42)):
            b.append(t(x + 14, yy + 16 + j * 13, ln, 10, GREY))
        # arrow down to the hub
        b.append(f'<path d="M{x + cw / 2},{cy0 + 220} L{x + cw / 2},{cy0 + 256} '
                 f'L{W / 2},{cy0 + 276} L{W / 2},{cy0 + 300}" fill="none" '
                 f'stroke="{col}" stroke-width="2.2" stroke-opacity="0.7"/>')

    hy = cy0 + 306
    b.append(rect(W / 2 - 300, hy, 600, 74, 12, "#132339", VI, 1.8))
    b.append(t(W / 2, hy + 28, "ONE DEFENSIBLE STATEMENT ABOUT BEHAVIOUR", 12.5,
               VI, "middle", "bold", ls="1.2", font=MONO))
    b.append(t(W / 2, hy + 50, "concordant across three sources with "
                               "non-overlapping biases — or reported as "
                               "discordant, which is itself a finding",
               10.4, GREY, "middle", style="italic"))

    b.append(rect(46, hy + 92, W - 92, 78, 10, "#1a0f14", RD, 1.4))
    b.append(t(66, hy + 116, "IF THE THREE DISAGREE", 10.5, RD, "start", "bold",
               ls="1.2", font=MONO))
    for j, ln in enumerate(wrap(
            "do not average them. Ask which bias explains the gap — good notes "
            "with poor observed reasoning is a documentation-theatre signal, "
            "and a different curriculum problem entirely.", 105)):
        b.append(t(66, hy + 136 + j * 14, ln, 10.4, GREY))
    return write("triangulation", svg(W, H, "\n".join(b),
                 "Three Level 3 data sources — observed encounter, chart audit "
                 "and sandbox interaction log — each with what it sees and the "
                 "bias it carries, converging on a single defensible statement "
                 "about behaviour"))


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — STEPPED WEDGE
# ═════════════════════════════════════════════════════════════════════════════
def fig_wedge():
    W, H = 940, 560
    b = ['<defs>'
         f'<marker id="sw-a" markerWidth="9" markerHeight="9" refX="7" '
         f'refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="{GR}"/>'
         f'</marker></defs>']
    b.append(rect(0, 0, W, H, 14, BG, "#182742"))
    b.append(t(W / 2, 36, "THE STEPPED WEDGE — EVERYBODY GETS IT, IN A "
                          "RANDOMISED ORDER",
               15.5, INK, "middle", "bold", ls="1.3", font=MONO))
    b.append(t(W / 2, 57, "the design that makes a rollout you were going to do "
                          "anyway into evidence you can defend",
               11, DIM, "middle", style="italic"))

    rows = ["Facility A", "Facility B", "Facility C", "Facility D", "Facility E"]
    steps = 6
    gx, gy, cw, ch = 190, 104, 96, 46
    # column headers
    for s in range(steps):
        b.append(t(gx + s * cw + cw / 2, gy - 26, f"PERIOD {s}", 9.6, DIM,
                   "middle", "bold", font=MONO))
        b.append(t(gx + s * cw + cw / 2, gy - 12,
                   ["baseline", "month 3", "month 6", "month 9", "month 12",
                    "month 15"][s], 9, DIM, "middle", font=MONO))
    for r, name in enumerate(rows):
        y = gy + r * (ch + 8)
        b.append(t(gx - 14, y + ch / 2 + 4, name, 11, INK, "end", "bold"))
        for s in range(steps):
            x = gx + s * cw
            on = s > r
            col = GR if on else CY
            b.append(rect(x + 3, y, cw - 6, ch, 6,
                          "#10321f" if on else "#0f2036", col, 1.3,
                          0.9 if on else 0.55))
            b.append(t(x + cw / 2, y + ch / 2 + 4,
                       "TRAINED" if on else "control", 9.4,
                       GR if on else DIM, "middle", "bold" if on else "normal",
                       font=MONO))
        # crossover marker
        if r + 1 < steps:
            x = gx + (r + 1) * cw
            b.append(f'<path d="M{x + 3},{y - 4} L{x + 3},{y + ch + 4}" '
                     f'stroke="{GO}" stroke-width="2.6"/>')

    # the staircase
    pts = []
    for r in range(len(rows)):
        pts.append((gx + (r + 1) * cw + 3, gy + r * (ch + 8)))
        pts.append((gx + (r + 1) * cw + 3, gy + r * (ch + 8) + ch + 8))
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    b.append(f'<path d="{d}" fill="none" stroke="{GO}" stroke-width="3" '
             f'stroke-opacity="0.85"/>')
    b.append(t(gx + 6 * cw + 14, gy + 5 * (ch + 8) - 14, "the wedge", 11.5, GO,
               "start", "bold", style="italic"))

    ny = gy + len(rows) * (ch + 8) + 34
    notes = [
        (GR, "Why it works here",
         "Every facility is trained eventually, so nobody is denied the "
         "programme. Randomising the order — not the receipt — is what buys "
         "you the counterfactual."),
        (GO, "What it costs you",
         "Time and secular trend are confounded with the intervention, so the "
         "analysis must adjust for period. Contamination between facilities is "
         "a real and reportable risk."),
        (RD, "When you cannot run it",
         "Fewer than about four clusters, or a rollout order you do not control. "
         "Then say so, use segmented regression, and call it what it is."),
    ]
    nw = (W - 92 - 32) / 3
    for i, (col, head, body) in enumerate(notes):
        x = 46 + i * (nw + 16)
        b.append(rect(x, ny, nw, 116, 10, CARD, col, 1.4))
        b.append(f'<rect x="{x}" y="{ny}" width="4" height="116" rx="2" '
                 f'fill="{col}"/>')
        b.append(t(x + 16, ny + 24, head, 11, col, "start", "bold"))
        for j, ln in enumerate(wrap(body, 38)):
            b.append(t(x + 16, ny + 44 + j * 13, ln, 9.7, GREY))
    return write("wedge", svg(W, H, "\n".join(b),
                 "A stepped-wedge design: five facilities across six periods, "
                 "each crossing from control to trained in a randomised order, "
                 "forming a staircase, with notes on why it works, what it costs "
                 "and when it cannot be run"))


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 7 — BEFORE/AFTER VS SEGMENTED REGRESSION
# ═════════════════════════════════════════════════════════════════════════════
def fig_its():
    W, H = 940, 470
    b = ['<defs>'
         f'<marker id="it-r" markerWidth="9" markerHeight="9" refX="7" '
         f'refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 z" fill="{RD}"/>'
         f'</marker></defs>']
    b.append(rect(0, 0, W, H, 14, BG, "#182742"))
    b.append(t(W / 2, 36, "THE SAME DATA, HONESTLY AND DISHONESTLY DRAWN",
               15.5, INK, "middle", "bold", ls="1.4", font=MONO))
    b.append(t(W / 2, 57, "the left-hand chart is the one that gets into the "
                          "annual report; the right-hand one is the one that is true",
               11, DIM, "middle", style="italic"))

    def panel(px, py, pw, ph, title, col, mode):
        b.append(rect(px, py, pw, ph, 11, CARD, col, 1.6))
        b.append(t(px + 16, py + 26, title, 12, col, "start", "bold", font=MONO))
        ax, ay, aw, ah = px + 46, py + 48, pw - 76, ph - 110
        b.append(f'<line x1="{ax}" y1="{ay}" x2="{ax}" y2="{ay + ah}" '
                 f'stroke="{LINE}"/>')
        b.append(f'<line x1="{ax}" y1="{ay + ah}" x2="{ax + aw}" '
                 f'y2="{ay + ah}" stroke="{LINE}"/>')

        def PX(i):
            return ax + (i / 11.0) * aw

        def PY(v):
            return ay + ah - (v / 100.0) * ah

        # underlying data: pre-existing upward trend + small step
        vals = [30, 34, 37, 41, 45, 49, 56, 59, 63, 67, 70, 74]
        if mode == "naive":
            b.append(f'<rect x="{PX(0)}" y="{PY(45)}" width="{PX(5) - PX(0)}" '
                     f'height="{ay + ah - PY(45)}" fill="{DIM}" '
                     f'fill-opacity="0.25"/>')
            b.append(f'<rect x="{PX(6)}" y="{PY(70)}" width="{PX(11) - PX(6)}" '
                     f'height="{ay + ah - PY(70)}" fill="{GR}" '
                     f'fill-opacity="0.45"/>')
            b.append(t((PX(0) + PX(5)) / 2, PY(45) - 8, "BEFORE  45%", 10.5, DIM,
                       "middle", "bold", font=MONO))
            b.append(t((PX(6) + PX(11)) / 2, PY(70) - 8, "AFTER  70%", 10.5, GR,
                       "middle", "bold", font=MONO))
            b.append(t(px + pw / 2, py + ph - 42,
                       '"a 25-point improvement"', 13, RD, "middle", "bold"))
            b.append(t(px + pw / 2, py + ph - 24,
                       "every point of which the trend would have delivered anyway",
                       9.8, RD, "middle", style="italic"))
        else:
            # points
            for i, v in enumerate(vals):
                b.append(f'<circle cx="{PX(i):.1f}" cy="{PY(v):.1f}" r="3.4" '
                         f'fill="{CY if i < 6 else GR}"/>')
            # pre trend and its extrapolation
            b.append(f'<line x1="{PX(0):.1f}" y1="{PY(30):.1f}" '
                     f'x2="{PX(5):.1f}" y2="{PY(49):.1f}" stroke="{CY}" '
                     f'stroke-width="2.4"/>')
            b.append(f'<line x1="{PX(5):.1f}" y1="{PY(49):.1f}" '
                     f'x2="{PX(11):.1f}" y2="{PY(72):.1f}" stroke="{CY}" '
                     f'stroke-width="1.8" stroke-dasharray="6 4" '
                     f'stroke-opacity="0.7"/>')
            b.append(f'<line x1="{PX(6):.1f}" y1="{PY(56):.1f}" '
                     f'x2="{PX(11):.1f}" y2="{PY(74):.1f}" stroke="{GR}" '
                     f'stroke-width="2.4"/>')
            b.append(f'<line x1="{PX(5.5):.1f}" y1="{ay}" '
                     f'x2="{PX(5.5):.1f}" y2="{ay + ah}" stroke="{GO}" '
                     f'stroke-width="1.8" stroke-dasharray="5 4"/>')
            b.append(t(PX(5.5), ay - 6, "TRAINING", 9.2, GO, "middle", "bold",
                       font=MONO))
            # the honest effect
            b.append(f'<path d="M{PX(10.4):.1f},{PY(70.5):.1f} '
                     f'L{PX(10.4):.1f},{PY(73.6):.1f}" stroke="{RD}" '
                     f'stroke-width="2"/>')
            b.append(t(px + pw / 2, py + ph - 42,
                       "level change ≈ +3 points, slope unchanged", 12, GR,
                       "middle", "bold"))
            b.append(t(px + pw / 2, py + ph - 24,
                       "small, real, and the only number you can defend",
                       9.8, GREY, "middle", style="italic"))

    panel(46, 88, 410, 340, "BEFORE-AND-AFTER BAR CHART", RD, "naive")
    panel(486, 88, 410, 340, "SEGMENTED REGRESSION (ITS)", GR, "its")
    b.append(f'<path d="M462,258 L478,258" stroke="{RD}" stroke-width="2.4" '
             f'marker-end="url(#it-r)"/>')
    return write("its", svg(W, H, "\n".join(b),
                 "Two charts of the same underlying data: a before-and-after bar "
                 "chart claiming a 25-point improvement, and a segmented "
                 "regression showing a pre-existing trend with only a small "
                 "genuine level change at the point of training"))


if __name__ == "__main__":
    for fn in (fig_mindmap, fig_ladder, fig_backwards, fig_decay,
               fig_triangulation, fig_wedge, fig_its):
        fn()
        print("wrote", fn.__name__)
