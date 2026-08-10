#!/usr/bin/env python3
"""Figure: the internal structure of the 4D AI Fluency Framework.

Subcategories are taken verbatim from the authors' own Practical Summary
Document (Dakan & Feller, v1.1). Note that only Description and Discernment
follow the Product / Process / Performance pattern — Delegation and Diligence
have their own triads, and the figure says so rather than tidying it up.

Writes ../static/img/ai-fluency/fig-4d-structure.png
"""
import os

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "static", "img", "ai-fluency")
os.makedirs(OUT, exist_ok=True)

BG, CARD = "#080d16", "#0d1424"
INK, GREY, FAINT, LINE = "#c9d6e8", "#6b82a0", "#9AA9AE", "#1e2d45"
CY, GR, GO, RD = "#00d4f5", "#10b981", "#f59e0b", "#f87171"
FONT = "Helvetica, Arial, sans-serif"

ROWS = [
    ("DELEGATION", CY, "What may I hand over?",
     ["Goal & Task Awareness", "Platform Awareness", "Task Delegation"], False),
    ("DESCRIPTION", GO, "How do I ask?",
     ["Product Description", "Process Description", "Performance Description"], True),
    ("DISCERNMENT", RD, "How do I judge what comes back?",
     ["Product Discernment", "Process Discernment", "Performance Discernment"], True),
    ("DILIGENCE", GR, "How do I stay accountable?",
     ["Creation Diligence", "Transparency Diligence", "Deployment Diligence"], False),
]
MODALITIES = [
    ("AUTOMATION", "AI performs a defined task on instruction"),
    ("AUGMENTATION", "human and AI work the problem together"),
    ("AGENCY", "AI configured to act on future cases"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=12, fill=INK, anchor="start", weight="normal", style="normal", ls="0"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}" letter-spacing="{ls}">{esc(s)}</text>')


def main():
    W, H = 1180, 690
    LX, CW, GAP = 300, 268, 14          # label column, cell width, gap
    TOP, RH = 172, 106
    o = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']

    o.append(t(W / 2, 44, "THE INTERNAL STRUCTURE OF THE 4Ds", 13, GREY,
               "middle", "bold", ls="1.8"))
    o.append(t(W / 2, 68, "Each competency has three subcategories. Two of the four follow the same "
               "Product / Process / Performance pattern.", 11.5, FAINT, "middle"))

    # modality column headers
    for i, (name, desc) in enumerate(MODALITIES):
        x = LX + i * (CW + GAP)
        o.append(f'<rect x="{x}" y="104" width="{CW}" height="46" rx="6" '
                 f'fill="{CARD}" stroke="{LINE}" stroke-width="1"/>')
        o.append(t(x + CW / 2, 124, name, 11, INK, "middle", "bold", ls="1.2"))
        o.append(t(x + CW / 2, 140, desc, 9.2, GREY, "middle"))

    for r, (name, col, q, subs, patterned) in enumerate(ROWS):
        y = TOP + r * RH
        # row label
        o.append(f'<rect x="24" y="{y}" width="{LX - 48}" height="{RH - 14}" rx="6" '
                 f'fill="{CARD}" stroke="{col}" stroke-width="1.8"/>')
        o.append(f'<rect x="24" y="{y}" width="5" height="{RH - 14}" fill="{col}"/>')
        o.append(t(46, y + 32, name, 13.5, col, "start", "bold", ls="0.8"))
        o.append(t(46, y + 54, q, 10.2, GREY, "start", style="italic"))
        if patterned:
            o.append(t(46, y + 74, "follows the P/P/P pattern", 8.8, FAINT, "start"))

        for i, sub in enumerate(subs):
            x = LX + i * (CW + GAP)
            solid = patterned
            o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH - 14}" rx="6" '
                     f'fill="{CARD}" stroke="{col if solid else LINE}" '
                     f'stroke-width="{1.6 if solid else 1}" '
                     f'stroke-dasharray="{"" if solid else "4,4"}"/>')
            words = sub.split()
            if len(words) > 2:
                o.append(t(x + CW / 2, y + 38, " ".join(words[:-1]), 11.5,
                           INK if solid else GREY, "middle", "bold" if solid else "normal"))
                o.append(t(x + CW / 2, y + 56, words[-1], 11.5,
                           INK if solid else GREY, "middle", "bold" if solid else "normal"))
            else:
                o.append(t(x + CW / 2, y + 48, sub, 11.5,
                           INK if solid else GREY, "middle", "bold" if solid else "normal"))

    # footnote
    fy = TOP + 4 * RH + 16
    o.append(f'<rect x="24" y="{fy}" width="{W - 48}" height="52" rx="6" '
             f'fill="#101a2e" stroke="{CY}" stroke-width="1.2"/>')
    o.append(t(44, fy + 22, "Description and Discernment share the Product / Process / Performance "
               "triad, and it lines up with the three modalities above.", 10.6, INK))
    o.append(t(44, fy + 39, "Delegation and Diligence have their own triads. The mapping is elegant "
               "but partial — worth knowing before you build on it.", 10.6, GREY))

    o.append(t(W / 2, H - 16, "Subcategories verbatim from Dakan & Feller, Framework for AI Fluency "
               "(Practical Summary Document) v1.1  ·  CC BY-NC-ND 4.0", 8.8, FAINT, "middle"))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">\n' + "\n".join(o) + "\n</svg>\n")
    p = os.path.join(OUT, "fig-4d-structure")
    open(p + ".svg", "w").write(svg)
    cairosvg.svg2png(url=p + ".svg", write_to=p + ".png", scale=1.6)
    os.remove(p + ".svg")
    print("wrote", p + ".png", os.path.getsize(p + ".png") // 1024, "KB")


if __name__ == "__main__":
    main()
