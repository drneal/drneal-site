#!/usr/bin/env python3
"""Worked modified-Angoff panel: two rounds, eight items, five judges.

Every number quoted in the blog post is computed here from the estimate
matrix below, not typed into the prose by hand. The matrix is illustrative —
it is what a plausible panel might produce on eight Level 1 items — but the
judge cut scores, the panel cut score and the between-judge standard
deviation are the true arithmetic on it.

    python3 fig_angoff.py

Prints the full table and writes ../static/img/angoff/fig-angoff-rounds.png
"""
import os
import statistics as st

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "static", "img", "angoff")
os.makedirs(OUT, exist_ok=True)

BG, CARD = "#080d16", "#0d1424"
INK, GREY, FAINT, LINE = "#c9d6e8", "#6b82a0", "#9AA9AE", "#1e2d45"
CY, GR, GO, RD, VI = "#00d4f5", "#10b981", "#f59e0b", "#f87171", "#a78bfa"
FONT = "Helvetica, Arial, sans-serif"

JUDGES = ["A", "B", "C", "D", "E"]
JCOL = [CY, GR, GO, RD, VI]

# (label, unit, short description of what the item asks)
ITEMS = [
    ("1", "1.3", "Identify which listed task is non-delegable"),
    ("2", "1.1", "What fluent, correctly formatted output does and does not establish"),
    ("3", "1.2", "Classify a pre-sorting triage assistant: automation, augmentation or agency"),
    ("4", "1.6", "Which action breaches the Data Protection Act 2019"),
    ("5", "1.5", "At which step of the independent-impression rule must the clinician write"),
    ("6", "1.5", "Correct response to a differential that omits TB in a wasting patient"),
    ("7", "1.6", "Which documentation phrasing correctly discloses AI involvement"),
    ("8", "1.5", "Classify a described behaviour: under-trust, calibrated or automation bias"),
]

# rows = items 1..8, columns = judges A..E. Probability that a borderline
# candidate answers the item correctly.
ROUND1 = [
    [0.88, 0.80, 0.92, 0.75, 0.85],
    [0.75, 0.68, 0.82, 0.60, 0.72],
    [0.55, 0.45, 0.68, 0.40, 0.57],
    [0.90, 0.82, 0.93, 0.80, 0.88],
    [0.85, 0.78, 0.88, 0.71, 0.82],
    [0.62, 0.55, 0.73, 0.45, 0.60],
    [0.72, 0.62, 0.78, 0.58, 0.68],
    [0.73, 0.60, 0.76, 0.62, 0.69],
]
ROUND2 = [
    [0.88, 0.82, 0.92, 0.80, 0.85],
    [0.74, 0.70, 0.79, 0.66, 0.72],
    [0.50, 0.47, 0.52, 0.45, 0.51],
    [0.90, 0.85, 0.92, 0.84, 0.88],
    [0.85, 0.80, 0.85, 0.78, 0.82],
    [0.58, 0.56, 0.64, 0.53, 0.58],
    [0.72, 0.66, 0.72, 0.63, 0.68],
    [0.68, 0.67, 0.71, 0.66, 0.68],
]


def judge_cuts(matrix):
    """Each judge's cut score = mean of their item estimates, as a percentage."""
    n_items = len(matrix)
    return [100.0 * sum(row[j] for row in matrix) / n_items
            for j in range(len(JUDGES))]


def summarise(matrix):
    cuts = judge_cuts(matrix)
    return cuts, st.mean(cuts), st.stdev(cuts)      # stdev = sample SD, n-1


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal",
      style="normal", ls="0"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}" letter-spacing="{ls}">{esc(s)}</text>')


def report():
    print("=" * 76)
    print("ITEM-LEVEL ESTIMATES  (probability a borderline candidate answers correctly)")
    print("=" * 76)
    hdr = f"  {'item':5}{'unit':7}" + "".join(f"{'R1 '+j:>8}" for j in JUDGES) \
        + "   |" + "".join(f"{'R2 '+j:>8}" for j in JUDGES) + f"{'mean R1':>10}{'mean R2':>9}"
    print(hdr)
    for i, (lab, unit, _) in enumerate(ITEMS):
        r1, r2 = ROUND1[i], ROUND2[i]
        print(f"  {lab:5}{unit:7}" + "".join(f"{v:>8.2f}" for v in r1) + "   |"
              + "".join(f"{v:>8.2f}" for v in r2)
              + f"{st.mean(r1):>10.3f}{st.mean(r2):>9.3f}")

    print()
    print("=" * 76)
    print("PANEL RESULT")
    print("=" * 76)
    out = {}
    for name, m in (("Round 1", ROUND1), ("Round 2", ROUND2)):
        cuts, mean, sd = summarise(m)
        out[name] = (cuts, mean, sd)
        print(f"  {name}   judge cuts: " + ", ".join(f"{c:.1f}" for c in cuts))
        print(f"  {'':9}panel cut : {mean:.1f}%     between-judge SD: {sd:.1f} points")
    d = out["Round 1"][2] - out["Round 2"][2]
    print(f"\n  cut score moved {abs(out['Round 2'][1]-out['Round 1'][1]):.2f} points; "
          f"spread fell {d:.1f} points ({100*d/out['Round 1'][2]:.0f}% reduction)")
    print(f"  item 3 mean: {st.mean(ROUND1[2]):.2f} -> {st.mean(ROUND2[2]):.2f}")
    return out


def figure(res):
    W, H = 1180, 660
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']
    o.append(t(W / 2, 42, "WHAT THE SECOND ROUND ACTUALLY DOES", 13, GREY,
               "middle", "bold", ls="1.8"))
    o.append(t(W / 2, 66, "Five judges, eight items. The cut score barely moves. "
               "The disagreement between judges halves.", 11.5, FAINT, "middle"))

    L, R, TOP, BOT = 200, 760, 110, 470
    LO, HI = 55.0, 85.0

    def py(v):
        return BOT - (v - LO) / (HI - LO) * (BOT - TOP)

    x1, x2 = L + 90, R - 90

    for v in range(55, 86, 5):
        o.append(f'<line x1="{L}" y1="{py(v):.1f}" x2="{R}" y2="{py(v):.1f}" '
                 f'stroke="{LINE}" stroke-width="1"/>')
        o.append(t(L - 12, py(v) + 4, f"{v}%", 10, GREY, "end"))
    o.append(t(L - 12, py(85) - 20, "cut score", 10, FAINT, "end"))

    (c1, m1, s1), (c2, m2, s2) = res["Round 1"], res["Round 2"]

    # panel cut score — flat across both rounds
    o.append(f'<line x1="{L}" y1="{py(m1):.1f}" x2="{R}" y2="{py(m2):.1f}" '
             f'stroke="{INK}" stroke-width="2.6" stroke-dasharray="7,5"/>')
    # parked clear of the value labels and the SD bracket
    pcx = R + 170
    o.append(f'<rect x="{pcx}" y="{py(m2) - 34:.1f}" width="176" height="68" rx="6" '
             f'fill="#101a2e" stroke="{INK}" stroke-width="1.4"/>')
    o.append(t(pcx + 88, py(m2) - 12, "PANEL CUT SCORE", 9.6, GREY, "middle",
               "bold", ls="1.1"))
    o.append(t(pcx + 88, py(m2) + 14, f"{m2:.1f}%", 24, INK, "middle", "bold"))
    o.append(t(pcx + 88, py(m2) + 28, "identical in both rounds", 8.8, FAINT, "middle"))

    # spread brackets
    for x, cs, sd, lab in ((x1, c1, s1, "ROUND 1"), (x2, cs2 := c2, s2, "ROUND 2")):
        top, bot = py(max(cs)), py(min(cs))
        bx = x - 58 if lab == "ROUND 1" else x + 108
        o.append(f'<line x1="{bx}" y1="{top:.1f}" x2="{bx}" y2="{bot:.1f}" '
                 f'stroke="{GO}" stroke-width="2"/>')
        for yy in (top, bot):
            o.append(f'<line x1="{bx - 7}" y1="{yy:.1f}" x2="{bx + 7}" y2="{yy:.1f}" '
                     f'stroke="{GO}" stroke-width="2"/>')
        anchor = "end" if lab == "ROUND 1" else "start"
        off = -14 if lab == "ROUND 1" else 14
        o.append(t(bx + off, (top + bot) / 2 - 4, "SD", 10, GO, anchor, "bold"))
        o.append(t(bx + off, (top + bot) / 2 + 12, f"{sd:.1f} pts", 11.5, GO,
                   anchor, "bold"))

    # judges
    for j, name in enumerate(JUDGES):
        col = JCOL[j]
        a, b = c1[j], c2[j]
        o.append(f'<line x1="{x1}" y1="{py(a):.1f}" x2="{x2}" y2="{py(b):.1f}" '
                 f'stroke="{col}" stroke-width="2.2" stroke-opacity="0.85"/>')
        for xx, vv in ((x1, a), (x2, b)):
            o.append(f'<circle cx="{xx}" cy="{py(vv):.1f}" r="6" fill="{BG}" '
                     f'stroke="{col}" stroke-width="2.6"/>')
        o.append(t(x1 - 16, py(a) + 4, f"{name}  {a:.1f}", 10.4, col, "end", "bold"))
        # nudge clear of the dashed panel-cut line when a judge lands on it
        dy = -9 if abs(b - m2) < 1.6 else 4
        o.append(t(x2 + 16, py(b) + dy, f"{b:.1f}", 10.4, col, "start", "bold"))

    for xx, lab in ((x1, "ROUND 1"), (x2, "ROUND 2")):
        o.append(t(xx, BOT + 30, lab, 11.4, INK, "middle", "bold", ls="1.4"))
    o.append(t(x1, BOT + 48, "estimated independently", 9.6, GREY, "middle"))
    o.append(t(x2, BOT + 48, "after discussion of divergences", 9.6, GREY, "middle"))

    fy = 530
    o.append(f'<rect x="24" y="{fy}" width="{W-48}" height="72" rx="6" '
             f'fill="#0b1220" stroke="{LINE}" stroke-width="1"/>')
    o.append(t(44, fy + 24, f"The panel cut score moved by "
               f"{abs(m2-m1):.2f} of a point. That is not the achievement.", 10.8, INK))
    o.append(t(44, fy + 43, f"The achievement is that between-judge disagreement fell "
               f"from {s1:.1f} points to {s2:.1f} — the panel now means the same thing "
               f"by “borderline.”", 10.8, GREY))
    o.append(t(44, fy + 61, "A cut score with judges twenty points apart is a number "
               "without a shared standard behind it.", 10.8, GREY))

    o.append(t(W / 2, H - 12, "Illustrative panel data; judge cut scores, panel cut and "
               "standard deviations are computed from the published estimate matrix.",
               8.8, FAINT, "middle"))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(o) + "\n</svg>\n")
    p = os.path.join(OUT, "fig-angoff-rounds")
    open(p + ".svg", "w").write(svg)
    cairosvg.svg2png(url=p + ".svg", write_to=p + ".png", scale=1.6)
    os.remove(p + ".svg")
    print(f"\n  wrote {p}.png  {os.path.getsize(p + '.png')//1024} KB")


if __name__ == "__main__":
    figure(report())
