#!/usr/bin/env python3
"""Two figures for the AI-OSCE companion post.

  fig-osce-station.png        anatomy of a single AI-OSCE station
  fig-borderline-regression.png   how a cut score is derived from examiner data

The regression figure is not a cartoon: the scatter is generated from a fixed
seed, the line is the actual least-squares fit through those points, and the
cut score printed on the figure is the fitted value at global rating = 2
(borderline). Change the data and the caption in the post must change too.

Writes ../static/img/ai-osce/
"""
import os
import random

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "static", "img", "ai-osce")
os.makedirs(OUT, exist_ok=True)

BG, CARD = "#080d16", "#0d1424"
INK, GREY, FAINT, LINE = "#c9d6e8", "#6b82a0", "#9AA9AE", "#1e2d45"
CY, GR, GO, RD = "#00d4f5", "#10b981", "#f59e0b", "#f87171"
FONT = "Helvetica, Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal",
      style="normal", ls="0"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}" letter-spacing="{ls}">{esc(s)}</text>')


def box(x, y, w, h, stroke=LINE, fill=CARD, sw=1, r=6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def wrap_lines(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def save(name, W, H, body, scale=1.6):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(body) + "\n</svg>\n")
    p = os.path.join(OUT, name)
    open(p + ".svg", "w").write(svg)
    cairosvg.svg2png(url=p + ".svg", write_to=p + ".png", scale=scale)
    os.remove(p + ".svg")
    print(f"  {name}.png  {os.path.getsize(p + '.png')//1024} KB")


# ───────────────────────────── Figure A: the station ─────────────────────────
def fig_station():
    W, H = 1180, 640
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']

    o.append(t(W / 2, 42, "ANATOMY OF ONE AI-OSCE STATION", 13, GREY,
               "middle", "bold", ls="1.8"))
    o.append(t(W / 2, 66, "Ten minutes. One simulated consultation. Every candidate "
               "meets the same three elements.", 11.5, FAINT, "middle"))

    cards = [
        ("THE STANDARDISED PATIENT", CY,
         "A trained lay actor who portrays the same case identically for every "
         "candidate, to the same script."),
        ("THE SANDBOX", GO,
         "An instrumented AI system. On some stations — undisclosed — one "
         "clinical error is seeded into its output."),
        ("THE EXAMINER", GR,
         "Scores a structured checklist and, separately, records a single "
         "global judgement of the performance."),
    ]
    cy0, ch, cw, gap = 92, 132, 364, 20
    for i, (name, col, desc) in enumerate(cards):
        x = 24 + i * (cw + gap)
        o.append(box(x, cy0, cw, ch, col, CARD, 1.6))
        o.append(f'<rect x="{x}" y="{cy0}" width="5" height="{ch}" fill="{col}"/>')
        o.append(t(x + 20, cy0 + 30, name, 11.4, col, "start", "bold", ls="1.0"))
        for j, ln in enumerate(wrap_lines(desc, 44)):
            o.append(t(x + 20, cy0 + 56 + j * 18, ln, 10.4, GREY))

    # converge
    my = cy0 + ch
    for i in range(3):
        x = 24 + i * (cw + gap) + cw / 2
        o.append(f'<path d="M {x} {my} L {x} {my + 16} L {W/2} {my + 16} '
                 f'L {W/2} {my + 32}" fill="none" stroke="{LINE}" stroke-width="1.4"/>')

    band_y = my + 34
    o.append(box(24, band_y, W - 48, 44, CY, "#101a2e", 1.4))
    o.append(t(W / 2, band_y + 28, "THE CANDIDATE IS SCORED ACROSS FOUR DOMAINS",
               12, CY, "middle", "bold", ls="1.4"))

    domains = [
        ("Appropriate delegation", 20, GR, "", False),
        ("Quality of description", 20, GO,
         "identifiable-data breach fails outright", False),
        ("Detection and correction of error", 40, RD,
         "fail this and you fail the station, whatever your total", True),
        ("Documentation and disclosure", 20, CY, "", False),
    ]
    ry0, rh = band_y + 62, 50
    bar_x, bar_max = 372, 300          # 40% -> 300px
    for i, (label, wt, col, note, conj) in enumerate(domains):
        y = ry0 + i * rh
        o.append(t(24, y + 22, label, 12.2, INK if conj else GREY,
                   "start", "bold" if conj else "normal"))
        if note:
            o.append(t(24, y + 38, note, 9.2, col if conj else FAINT,
                       "start", style="italic"))
        bw = bar_max * wt / 40
        o.append(box(bar_x, y + 8, bw, 22, col, col, 0, 4))
        o.append(t(bar_x + bw + 12, y + 24, f"{wt}%", 12, col, "start", "bold"))
        if conj:
            o.append(box(760, y + 6, 200, 26, RD, "#1c1114", 1.4, 13))
            o.append(t(860, y + 24, "CONJUNCTIVE", 10.6, RD, "middle", "bold", ls="1.0"))
        else:
            o.append(t(760, y + 24, "compensable", 10.2, FAINT, "start"))

    fy = ry0 + 4 * rh + 8
    o.append(box(24, fy, W - 48, 46, LINE, "#0b1220", 1))
    o.append(t(44, fy + 20, "Compensable means a weak score here can be offset by a "
               "strong score elsewhere. Conjunctive means it cannot.", 10.6, INK))
    o.append(t(44, fy + 37, "The cut score for the station is set by borderline "
               "regression, not by an arbitrary percentage.", 10.6, GREY))

    o.append(t(W / 2, H - 14, "Rubric weights as specified in Annex C, Level 1 — The "
               "Common Core, v0.1; conjunctive criteria per Annex B §8.4",
               8.8, FAINT, "middle"))
    save("fig-osce-station", W, H, o)


# ────────────────────── Figure B: borderline regression ──────────────────────
def fig_borderline():
    # synthetic examiner data: (global rating 1-5, checklist %)
    random.seed(11)
    means = {1: 34, 2: 57, 3: 70, 4: 82, 5: 92}
    n = {1: 5, 2: 9, 3: 14, 4: 11, 5: 6}
    pts = []
    for g, m in means.items():
        for _ in range(n[g]):
            pts.append((g, max(8, min(99, random.gauss(m, 7.0)))))

    # ordinary least squares of checklist score on global rating
    N = len(pts)
    mx = sum(p[0] for p in pts) / N
    my = sum(p[1] for p in pts) / N
    b = (sum((p[0] - mx) * (p[1] - my) for p in pts)
         / sum((p[0] - mx) ** 2 for p in pts))
    a = my - b * mx
    cut = a + b * 2                       # fitted value at "borderline"

    # R^2, quoted in the post as the quality check examiners actually run
    ss_res = sum((p[1] - (a + b * p[0])) ** 2 for p in pts)
    ss_tot = sum((p[1] - my) ** 2 for p in pts)
    r2 = 1 - ss_res / ss_tot

    W, H = 1020, 640
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']
    o.append(t(W / 2, 42, "HOW A PASS MARK IS SET: BORDERLINE REGRESSION", 13, GREY,
               "middle", "bold", ls="1.8"))
    o.append(t(W / 2, 66, "One station. Every candidate contributes one point. "
               "The pass mark is read off the fitted line.", 11.5, FAINT, "middle"))

    L, R, TOP, BOT = 150, 800, 106, 466
    def px(g):
        return L + (g - 1) * (R - L) / 4
    def py(s):
        return BOT - (s / 100) * (BOT - TOP)

    # grid
    for s in range(0, 101, 20):
        o.append(f'<line x1="{L}" y1="{py(s):.1f}" x2="{R}" y2="{py(s):.1f}" '
                 f'stroke="{LINE}" stroke-width="1"/>')
        o.append(t(L - 14, py(s) + 4, f"{s}", 10, GREY, "end"))
    o.append(t(L - 14, py(100) - 22, "Checklist", 10, FAINT, "end"))
    o.append(t(L - 14, py(100) - 8, "score %", 10, FAINT, "end"))

    labels = ["Clear\nfail", "Borderline", "Clear\npass", "Good", "Excellent"]
    for i, lab in enumerate(labels):
        g = i + 1
        col = GO if g == 2 else GREY
        for j, ln in enumerate(lab.split("\n")):
            o.append(t(px(g), BOT + 26 + j * 14, ln, 10.6, col, "middle",
                       "bold" if g == 2 else "normal"))
        o.append(f'<line x1="{px(g):.1f}" y1="{BOT}" x2="{px(g):.1f}" y2="{BOT + 6}" '
                 f'stroke="{LINE}" stroke-width="1"/>')
    o.append(t((L + R) / 2, BOT + 68, "EXAMINER'S GLOBAL JUDGEMENT", 10.4, FAINT,
               "middle", "bold", ls="1.2"))

    # scatter, jittered horizontally so overlapping points stay visible
    random.seed(4)
    for g, s in pts:
        jx = min(R - 6, max(L + 6, px(g) + random.uniform(-26, 26)))
        o.append(f'<circle cx="{jx:.1f}" cy="{py(s):.1f}" r="4.2" '
                 f'fill="{CY}" fill-opacity="0.55" stroke="{CY}" stroke-width="0.8"/>')

    # fitted line
    o.append(f'<line x1="{px(1):.1f}" y1="{py(a + b * 1):.1f}" '
             f'x2="{px(5):.1f}" y2="{py(a + b * 5):.1f}" '
             f'stroke="{INK}" stroke-width="2.4"/>')

    # the read-off
    o.append(f'<line x1="{px(2):.1f}" y1="{BOT}" x2="{px(2):.1f}" y2="{py(cut):.1f}" '
             f'stroke="{GO}" stroke-width="1.8" stroke-dasharray="5,4"/>')
    o.append(f'<line x1="{px(2):.1f}" y1="{py(cut):.1f}" x2="{L}" y2="{py(cut):.1f}" '
             f'stroke="{GO}" stroke-width="1.8" stroke-dasharray="5,4"/>')
    o.append(f'<circle cx="{px(2):.1f}" cy="{py(cut):.1f}" r="7" fill="{BG}" '
             f'stroke="{GO}" stroke-width="2.6"/>')

    o.append(box(R + 24, py(cut) - 30, 170, 60, GO, "#1a1408", 1.6))
    o.append(t(R + 40, py(cut) - 10, "CUT SCORE", 10, GO, "start", "bold", ls="1.2"))
    o.append(t(R + 40, py(cut) + 16, f"{cut:.1f}%", 22, GO, "start", "bold"))

    # label parked in empty space below the line, with a leader to it
    lx, ly = px(3.55), py(16)
    o.append(f'<line x1="{lx:.1f}" y1="{ly - 26:.1f}" x2="{px(3.55):.1f}" '
             f'y2="{py(a + b * 3.55) + 8:.1f}" stroke="{LINE}" stroke-width="1.2"/>')
    o.append(t(lx, ly, "fitted line", 10.4, INK, "middle", "bold"))
    # 2 dp, so a reader checking a + 2b against the printed cut score gets 54.7
    o.append(t(lx, ly + 16, f"score = {a:.2f} + {b:.2f} × rating", 9.6, GREY, "middle"))

    fy = 560
    o.append(box(24, fy, W - 48, 62, LINE, "#0b1220", 1))
    o.append(t(44, fy + 22, f"Each examiner records two things per candidate: a checklist "
               f"score and a global judgement. Regress one on the other ({N} candidates "
               f"here, R² = {r2:.2f}),", 10.4, INK))
    o.append(t(44, fy + 40, "and the height of the line above “borderline” is the "
               "pass mark for that station. The candidates set the standard; the examiners "
               "only judge.", 10.4, GREY))
    o.append(t(44, fy + 55, "Illustrative data, generated from a fixed seed. The line and the "
               "cut score are the true least-squares fit through the points shown.",
               8.8, FAINT))

    save("fig-borderline-regression", W, H, o)
    return cut, r2, N


if __name__ == "__main__":
    fig_station()
    cut, r2, N = fig_borderline()
    print(f"\n  cut score = {cut:.1f}%   R2 = {r2:.3f}   n = {N}")
