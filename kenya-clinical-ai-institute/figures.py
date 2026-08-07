#!/usr/bin/env python3
"""Generate SVG figures for the Kenya Clinical AI Institute blueprint.
Deliberately uses presentation attributes (not CSS classes) so that WeasyPrint
renders them faithfully."""

import os, textwrap

# THEME=light  -> print palette, used for the PDF        (writes to ./figures)
# THEME=dark   -> drnealaggarwal.info palette, for the post (writes to ../static/img/kenya-clinical-ai)
#
#   python3 figures.py                  # light / print figures
#   FIGTHEME=dark python3 figures.py    # dark / web figures
#
THEME = os.environ.get("FIGTHEME", "light")
HERE  = os.path.dirname(os.path.abspath(__file__))
SITE  = os.path.dirname(HERE)

if THEME == "dark":
    OUT   = os.path.join(SITE, "static", "img", "kenya-clinical-ai")
    INK   = "#c9d6e8"   # body text
    TEAL  = "#00d4f5"   # cyan accent
    TEAL2 = "#10b981"   # green accent
    LTEAL = "#0a2833"
    BRICK = "#f87171"
    LBRICK= "#2a1519"
    GOLD  = "#f59e0b"
    LGOLD = "#2b2008"
    GREY  = "#6b82a0"
    LGREY = "#111827"
    BG    = "#080d16"   # page background
    CARD  = "#0d1424"   # raised panel
    ONCOL = "#061019"   # text sitting on a bright accent fill
else:
    OUT   = os.path.join(HERE, "figures")
    INK   = "#12262B"
    TEAL  = "#0B4F4A"
    TEAL2 = "#177A6E"
    LTEAL = "#E6F0EE"
    BRICK = "#A63A2B"
    LBRICK= "#F7EAE7"
    GOLD  = "#B5822A"
    LGOLD = "#FAF3E4"
    GREY  = "#66787E"
    LGREY = "#EEF1F2"
    BG    = "#FFFFFF"
    CARD  = "#FFFFFF"
    ONCOL = "#FFFFFF"

WHITE = CARD          # every historical "WHITE" fill is a panel fill
os.makedirs(OUT, exist_ok=True)
FONT  = "Helvetica, Arial, sans-serif"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def txt(x, y, s, size=12, fill=INK, anchor="middle", weight="normal", style="normal", ls="0"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" letter-spacing="{ls}">{esc(s)}</text>')


def wrap(x, y, s, width, size=12, fill=INK, anchor="middle", weight="normal", lh=None):
    lh = lh or size * 1.32
    lines = textwrap.wrap(s, width=width)
    out = []
    for i, ln in enumerate(lines):
        out.append(txt(x, y + i * lh, ln, size, fill, anchor, weight))
    return "\n".join(out)


def rect(x, y, w, h, fill=WHITE, stroke=GREY, sw=1, rx=6, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def line(x1, y1, x2, y2, stroke=GREY, sw=1, dash=None, cap="round", marker=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#arrow)"' if marker else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}"{d}{m}/>')


def path(d, fill="none", stroke=GREY, sw=1, dash=None, marker=False):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#arrow)"' if marker else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{ds}{m}/>'


def svg(w, h, body, title=""):
    defs = f'''<defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{GREY}"/>
    </marker>
    <marker id="arrowteal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{TEAL}"/>
    </marker>
  </defs>'''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
            f'{defs}\n<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>\n{body}\n</svg>\n')


def write(name, content):
    p = os.path.join(OUT, name)
    with open(p, "w") as f:
        f.write(content)
    print("wrote", p)


# ---------------------------------------------------------------- Figure 1
# Institutional architecture: foundation -> five pillars -> mandate
def fig1():
    W, H = 1000, 552
    b = []
    b.append(txt(500, 34, "FIGURE 1 — INSTITUTIONAL ARCHITECTURE", 12, GREY, weight="bold", ls="1.6"))

    # Roof / mandate
    b.append(rect(60, 56, 880, 74, LTEAL, TEAL, 1.6, 8))
    b.append(txt(500, 84, "MANDATE", 11, TEAL, weight="bold", ls="2"))
    b.append(txt(500, 108, "Every clinician in Kenya can use AI safely, sceptically and to the patient's benefit — and can prove it.",
                 13.5, INK))

    pillars = [
        ("01", "TEACHING", TEAL, [
            "Tiered curriculum, five",
            "professional tracks",
            "Ladder: Foundation to Fellow",
            "Residential, hybrid, mobile",
        ]),
        ("02", "ASSESSMENT\n& CERTIFICATION", GOLD, [
            "Blueprinted, psychometric",
            "item banks",
            "Simulation-based OSCE-style",
            "exams (AI-OSCE)",
            "Council-recognised CPD",
        ]),
        ("03", "SIMULATION\n& SANDBOX", BRICK, [
            "Synthetic-patient environment",
            "De-identified Kenyan case",
            "corpus",
            "Failure-injection rigs",
        ]),
        ("04", "EVALUATION\n& RESEARCH", TEAL2, [
            "Model evaluation against",
            "Kenyan case mix",
            "Outcome studies, Kirkpatrick 3-4",
            "Publication and open data",
        ]),
        ("05", "STANDARDS\n& ADVISORY", GREY, [
            "Competency standards for",
            "councils and faculties",
            "Procurement and deployment",
            "guidance",
            "Incident review",
        ]),
    ]
    x0, gap, pw = 60, 16, (880 - 4 * 16) / 5
    for i, (num, name, col, bullets) in enumerate(pillars):
        x = x0 + i * (pw + gap)
        b.append(rect(x, 158, pw, 254, WHITE, col, 1.6, 8))
        b.append(rect(x, 158, pw, 6, col, col, 0, 0))
        b.append(txt(x + pw / 2, 194, num, 20, col, weight="bold"))
        for j, part in enumerate(name.split("\n")):
            b.append(txt(x + pw / 2, 218 + j * 15, part, 11.5, INK, weight="bold", ls="0.6"))
        yy = 218 + len(name.split("\n")) * 15 + 18
        b.append(line(x + 22, yy - 10, x + pw - 22, yy - 10, col, 0.8))
        for j, bl in enumerate(bullets):
            b.append(txt(x + pw / 2, yy + 10 + j * 15, bl, 9.6, GREY))

    # connectors
    for i in range(5):
        x = x0 + i * (pw + gap) + pw / 2
        b.append(line(x, 130, x, 158, col if False else GREY, 0.9, dash="3,3"))
        b.append(line(x, 412, x, 438, GREY, 0.9, dash="3,3"))

    # Foundation
    b.append(rect(60, 438, 880, 82, LGREY, GREY, 1.4, 8))
    b.append(txt(500, 462, "FOUNDATION", 10.5, GREY, weight="bold", ls="2"))
    b.append(txt(500, 485, "Clinical governance  ·  Data protection and patient consent  ·  Faculty development  ·  Digital infrastructure and connectivity",
                 11.5, INK))
    b.append(txt(500, 505, "Independence from vendors  ·  Public reporting of outcomes  ·  Council and university accreditation",
                 11.5, INK))
    write("fig1-architecture.svg", svg(W, H, "\n".join(b)))


# ---------------------------------------------------------------- Figure 2
# Clinical 4D
def fig2():
    W, H = 1000, 648
    b = []
    b.append(txt(500, 34, "FIGURE 2 — THE CLINICAL 4Ds", 12, GREY, weight="bold", ls="1.6"))
    b.append(txt(500, 58, "The 4D AI-Fluency Framework (Dakan & Feller) translated into clinical acts", 12.5, GREY))

    quads = [
        ("DELEGATION", TEAL, LTEAL, 60, 84,
         "What may I hand over — and what must never leave my hands?",
         [["Triage the task, not the patient"],
          ["A named non-delegable list: consent, breaking",
           "bad news, the decision to operate, the final",
           "diagnosis, the signature"],
          ["Distinguish automation / augmentation / agency"],
          ["Ask: would I delegate this to an intern I have",
           "never met?"]]),
        ("DESCRIPTION", GOLD, LGOLD, 510, 84,
         "How do I state a clinical problem so the answer is worth reading?",
         [["Structured clinical context: setting, level of",
           "facility, formulary, what tests actually exist"],
          ["Local epidemiology stated explicitly"],
          ["Ask for reasoning, differentials and the case",
           "against — not just an answer"],
          ["Never paste identifiable patient data"],
          ["Prompt as a clinical handover, not a search"]]),
        ("DISCERNMENT", BRICK, LBRICK, 60, 372,
         "How do I judge what comes back — before it reaches a patient?",
         [["Read the reasoning before the conclusion"],
          ["Independent-verification discipline: form your",
           "own impression before you look at the output"],
          ["Recognise plausible-but-wrong output"],
          ["Detect training-data bias against African",
           "presentations, skin tones, local drug names"],
          ["Calibrated trust — see Figure 8"]]),
        ("DILIGENCE", TEAL2, LTEAL, 510, 372,
         "How do I own the result and remain accountable?",
         [["Documentation: what was AI-assisted, and how"],
          ["Disclosure to patients and to colleagues"],
          ["Data protection and consent under Kenyan law"],
          ["Incident reporting when AI contributes to harm"],
          ["Guarding your own skills against decay"],
          ["The signature — and the liability — is yours"]]),
    ]
    for name, col, lcol, x, y in [(q[0], q[1], q[2], q[3], q[4]) for q in quads]:
        pass
    for name, col, lcol, x, y, q, bullets in quads:
        b.append(rect(x, y, 430, 232, lcol, col, 1.6, 8))
        b.append(rect(x, y, 430, 6, col, col, 0, 0))
        b.append(txt(x + 24, y + 36, name, 15, col, anchor="start", weight="bold", ls="1.4"))
        b.append(txt(x + 24, y + 60, q, 11, INK, anchor="start", style="italic"))
        b.append(line(x + 24, y + 74, x + 406, y + 74, col, 0.8))
        yy = y + 96
        for bl in bullets:
            for k, ln in enumerate(bl):
                b.append(txt(x + 24 if k == 0 else x + 38, yy,
                             ("— " + ln) if k == 0 else ln, 10.4, INK, anchor="start"))
                yy += 15.5
            yy += 3.5

    # centre hub
    b.append(f'<circle cx="500" cy="350" r="46" fill="{WHITE}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(txt(500, 344, "THE", 9, GREY, weight="bold", ls="1.4"))
    b.append(txt(500, 358, "PATIENT", 11.5, INK, weight="bold", ls="0.6"))

    b.append(txt(500, 628, "Every module in every track is blueprinted against one or more of these four competencies.",
                 11, GREY, style="italic"))
    write("fig2-clinical-4d.svg", svg(W, H, "\n".join(b)))


# ---------------------------------------------------------------- Figure 3
# Curriculum matrix: tracks x levels
def fig3():
    W, H = 1040, 616
    b = []
    b.append(txt(520, 30, "FIGURE 3 — CURRICULUM MATRIX: FIVE TRACKS, FIVE LEVELS", 12, GREY, weight="bold", ls="1.4"))

    tracks = ["TRACK A\nPhysicians", "TRACK B\nSurgeons &\nProceduralists",
              "TRACK C\nNursing &\nMidwifery", "TRACK D\nAdministrators &\nManagers",
              "TRACK E\nHealth\nInformaticians"]
    levels = [
        ("L5", "FELLOW", "Clinical AI Fellowship — 12 months, full time", BRICK),
        ("L4", "FACULTY", "Certified Instructor / Train-the-Trainer", GOLD),
        ("L3", "ADVANCED", "Specialty-specific deep practice", TEAL2),
        ("L2", "PRACTITIONER", "Supervised workplace application", TEAL),
        ("L1", "FOUNDATION", "Common core — the Clinical 4Ds", GREY),
    ]

    left = 190
    colw = (W - left - 40) / 5
    top = 96
    rowh = 88

    # headers
    for i, t in enumerate(tracks):
        x = left + i * colw
        b.append(rect(x + 4, top - 56, colw - 8, 48, LGREY, GREY, 1, 6))
        for j, part in enumerate(t.split("\n")):
            b.append(txt(x + colw / 2, top - 39 + j * 12.5, part, 9.6, INK,
                         weight="bold" if j == 0 else "normal"))

    for r, (code, name, desc, col) in enumerate(levels):
        y = top + r * rowh
        # left label
        b.append(rect(20, y + 4, left - 32, rowh - 8, WHITE, col, 1.4, 6))
        b.append(rect(20, y + 4, 5, rowh - 8, col, col, 0, 0))
        b.append(txt(38, y + 28, code, 13, col, anchor="start", weight="bold"))
        b.append(txt(72, y + 28, name, 11.5, INK, anchor="start", weight="bold", ls="0.5"))
        b.append(wrap(38, y + 47, desc, 30, 9.2, GREY, anchor="start"))

        for c in range(5):
            x = left + c * colw
            if r == 4:  # foundation: shared
                if c == 0:
                    b.append(rect(left + 4, y + 4, colw * 5 - 8, rowh - 8, LGREY, col, 1.2, 6))
                    b.append(txt(left + colw * 2.5, y + 34, "SHARED COMMON CORE — identical for every cadre", 11.5, INK, weight="bold"))
                    b.append(txt(left + colw * 2.5, y + 54, "12 h  ·  What these systems are and are not  ·  The 4Ds  ·  Law, consent, documentation  ·  First supervised use", 9.4, GREY))
            else:
                fill = WHITE
                b.append(rect(x + 4, y + 4, colw - 8, rowh - 8, fill, col, 1.1, 6))
                cell = {
                    (0, 0): ["Fellowship", "cohort of 8", "Any cadre —", "competitive entry"],
                    (1, 0): ["Case-based", "teaching", "Assessment", "design"],
                    (2, 0): ["Ambulatory &", "inpatient", "reasoning", "36 h + logbook"],
                    (3, 0): ["Ward &", "clinic", "practicum", "40 h"],
                }
                b.append(txt(x + colw / 2, y + 30, "", 9))
        # per-cell text for rows 0-3
    cells = {
        # (row, col) : lines
        (0, 0): ["Clinical AI Fellowship — one cohort, all cadres, 12 months"],
        (1, 0): ["Instructor certification — common pedagogy core + track-specific practicum"],
        (2, 0): ["Diagnostic", "reasoning under", "uncertainty;", "specialty deep-dives"],
        (2, 1): ["Peri-operative", "planning; imaging;", "intra-op decision", "support; robotics"],
        (2, 2): ["Triage &", "early-warning", "scores; handover;", "documentation"],
        (2, 3): ["Procurement,", "evaluation,", "deployment", "governance"],
        (2, 4): ["Model evaluation,", "integration,", "monitoring,", "local validation"],
        (3, 0): ["Supervised", "clinic use;", "logbook of", "20 encounters"],
        (3, 1): ["Supervised", "pre-op use;", "logbook of", "20 cases"],
        (3, 2): ["Supervised ward", "use; logbook of", "20 shifts"],
        (3, 3): ["Supervised", "service-level", "project"],
        (3, 4): ["Supervised", "evaluation", "of one", "deployed model"],
    }
    for (r, c), lines in cells.items():
        y = top + r * rowh
        if r in (0, 1):
            b.append(rect(left + 4, y + 4, colw * 5 - 8, rowh - 8, WHITE,
                          levels[r][3], 1.2, 6))
            b.append(txt(left + colw * 2.5, y + 34, lines[0], 11.5, INK, weight="bold"))
            sub = ("Deep specialisation, original evaluation work, one publishable output, and a commitment to teach."
                   if r == 0 else
                   "No one teaches on this programme without being certified to teach on this programme.")
            b.append(txt(left + colw * 2.5, y + 54, sub, 9.4, GREY))
        else:
            x = left + c * colw
            for j, ln in enumerate(lines):
                b.append(txt(x + colw / 2, y + 28 + j * 13, ln, 9.4, INK))

    b.append(txt(520, top + 5 * rowh + 30,
                 "Progression is gated, not automatic: each level requires a passed assessment and a countersigned workplace logbook before the next may be attempted.",
                 10.4, GREY, style="italic"))
    write("fig3-curriculum-matrix.svg", svg(W, H, "\n".join(b)))


# ---------------------------------------------------------------- Figure 4
# Miller's pyramid x 4D x assessment
def fig4():
    W, H = 1000, 560
    b = []
    b.append(txt(500, 32, "FIGURE 4 — ASSESSMENT BLUEPRINT: MILLER'S PYRAMID APPLIED TO AI COMPETENCE", 12, GREY, weight="bold", ls="1.2"))

    tiers = [
        ("DOES", TEAL, 4, "Uses AI appropriately in real practice, unobserved",
         "Workplace-based assessment · countersigned logbook · chart audit · patient-outcome review", "Kirkpatrick 3–4"),
        ("SHOWS HOW", TEAL2, 3, "Demonstrates safe use in a simulated encounter",
         "AI-OSCE: simulated consultation with a seeded-error AI · structured examiner rubric", "Kirkpatrick 3"),
        ("KNOWS HOW", GOLD, 2, "Applies knowledge to a clinical vignette",
         "Extended-matching questions · script-concordance test · written critique of an AI output", "Kirkpatrick 2"),
        ("KNOWS", GREY, 1, "Recalls facts about capability, limitation and law",
         "MCQ from a blueprinted, psychometrically monitored item bank", "Kirkpatrick 2"),
    ]

    cx = 262
    base_w = 372
    th = 92
    top = 76
    for i, (name, col, lvl, desc, method, kirk) in enumerate(tiers):
        y = top + i * th
        wt = base_w * (0.30 + 0.70 * i / 3)
        wb = base_w * (0.30 + 0.70 * (i + 1) / 3)
        d = (f"M {cx - wt/2} {y} L {cx + wt/2} {y} L {cx + wb/2} {y + th - 6} L {cx - wb/2} {y + th - 6} Z")
        b.append(path(d, fill=col, stroke=BG, sw=2))
        b.append(txt(cx, y + th / 2 - 4, name, 13.5, ONCOL, weight="bold", ls="1.2"))
        b.append(txt(cx, y + th / 2 + 14, f"Level {5 - lvl if False else lvl}", 9, ONCOL))

        # right panel
        px = 500
        b.append(rect(px, y + 4, 460, th - 14, WHITE, col, 1.2, 6))
        b.append(rect(px, y + 4, 4, th - 14, col, col, 0, 0))
        b.append(txt(px + 16, y + 24, desc, 10.6, INK, anchor="start", weight="bold"))
        b.append(wrap(px + 16, y + 42, method, 74, 9.4, GREY, anchor="start"))
        b.append(txt(px + 448, y + 24, kirk, 8.6, col, anchor="end", weight="bold"))
        b.append(line(px + 4, y + 4, px - 40 + 4, y + 4, BG, 0))
        b.append(line(cx + (base_w * (0.30 + 0.70 * (i + 0.5) / 3)) / 2, y + th / 2 - 3, px - 6, y + th / 2 - 3,
                      col, 1, dash="2,3", marker=False))

    b.append(rect(50, top + 4 * th + 12, 900, 52, LTEAL, TEAL, 1.2, 6))
    b.append(txt(500, top + 4 * th + 34, "No certificate is issued on 'KNOWS' alone.", 12, TEAL, weight="bold"))
    b.append(txt(500, top + 4 * th + 53,
                 "A pass at every level of this pyramid — including a countersigned workplace logbook — is required before any award is made.",
                 10.4, INK))
    write("fig4-assessment-pyramid.svg", svg(W, H, "\n".join(b)))


# ---------------------------------------------------------------- Figure 5
# QA closed loop
def fig5():
    W, H = 940, 700
    b = []
    b.append(txt(470, 32, "FIGURE 5 — THE QUALITY LOOP", 12, GREY, weight="bold", ls="1.6"))
    b.append(txt(470, 55, "Nothing is taught that is not measured; nothing is measured that does not change what is taught.", 11.5, GREY, style="italic"))

    import math
    cx, cy, r = 470, 380, 218
    stations = [
        ("1", "STANDARD SET", "Competency standards agreed with councils, faculties and the hospital"),
        ("2", "BLUEPRINT", "Every module mapped to a standard and an assessment before it is written"),
        ("3", "BUILD", "Content authored by a clinician–educator pair; peer-reviewed; version-controlled"),
        ("4", "PILOT", "Every new module run against a pilot cohort with think-aloud observation"),
        ("5", "DELIVER", "Only by certified instructors; sessions sampled and observed"),
        ("6", "ASSESS", "Psychometric monitoring of every item; standard-setting by Angoff panel"),
        ("7", "AUDIT", "Workplace practice audited at 3 and 12 months; incidents reviewed"),
        ("8", "REPORT & REVISE", "Outcomes published annually; failing modules retired, not defended"),
    ]
    n = len(stations)
    for i, (num, name, desc) in enumerate(stations):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        col = [TEAL, TEAL2, GOLD, BRICK][i % 4]
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="{WHITE}" stroke="{col}" stroke-width="2"/>')
        b.append(txt(x, y + 6, num, 17, col, weight="bold"))
        # label placement
        lx = cx + (r + 78) * math.cos(a)
        ly = cy + (r + 78) * math.sin(a)
        anchor = "middle"
        if math.cos(a) > 0.35:
            anchor = "start"; lx = x + 40
        elif math.cos(a) < -0.35:
            anchor = "end"; lx = x - 40
        else:
            lx = x
            ly = y - 78 if math.sin(a) < 0 else y + 52
        b.append(txt(lx, ly, name, 11.2, INK, anchor=anchor, weight="bold", ls="0.5"))
        b.append(wrap(lx, ly + 15, desc, 34, 8.8, GREY, anchor=anchor))

        # arc arrow to next
        a2 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        ax1 = cx + (r - 34) * math.cos(a + 0.20)
        ay1 = cy + (r - 34) * math.sin(a + 0.20)
        ax2 = cx + (r - 34) * math.cos(a2 - 0.20)
        ay2 = cy + (r - 34) * math.sin(a2 - 0.20)
        b.append(path(f"M {ax1:.1f} {ay1:.1f} A {r-34} {r-34} 0 0 1 {ax2:.1f} {ay2:.1f}",
                      stroke=GREY, sw=1.3, marker=True))

    b.append(f'<circle cx="{cx}" cy="{cy}" r="96" fill="{LTEAL}" stroke="{TEAL}" stroke-width="1.6"/>')
    b.append(txt(cx, cy - 18, "QUALITY", 13, TEAL, weight="bold", ls="1.6"))
    b.append(txt(cx, cy - 1, "OF DELIVERABLES", 10.5, TEAL, weight="bold", ls="0.8"))
    b.append(txt(cx, cy + 22, "Owned by an office", 9.2, GREY))
    b.append(txt(cx, cy + 35, "that does not report", 9.2, GREY))
    b.append(txt(cx, cy + 48, "to the trainers", 9.2, GREY))
    write("fig5-quality-loop.svg", svg(W, H, "\n".join(b)))


# ---------------------------------------------------------------- Figure 6
# Org chart
def fig6():
    W, H = 1180, 680
    b = []
    b.append(txt(590, 32, "FIGURE 6 — ORGANISATIONAL STRUCTURE AT STEADY STATE", 12, GREY, weight="bold", ls="1.4"))
    b.append(txt(590, 54, "Figures in the coloured tags are full-time-equivalent posts. Total core establishment: 71 FTE.", 11, GREY))

    def box(x, y, w, h, title, sub, col, fte=None, fill=WHITE):
        o = [rect(x, y, w, h, fill, col, 1.5, 6), rect(x, y, w, 5, col, col, 0, 0)]
        o.append(txt(x + w / 2 + 16, y + 27, title, 11.2, INK, weight="bold", ls="0.4"))
        if sub:
            for j, s in enumerate(sub):
                o.append(txt(x + w / 2 + 16, y + 44 + j * 12.5, s, 8.9, GREY))
        if fte:
            o.append(rect(x + 10, y + 15, 32, 16, col, col, 0, 8))
            o.append(txt(x + 26, y + 27, fte, 9.6, ONCOL, weight="bold"))
        return "\n".join(o)

    # Board
    b.append(box(420, 74, 340, 58, "INDEPENDENT GOVERNING BOARD", ["Chair · councils · patient representative · academia · ethics"], INK, fill=LGREY))
    # CEO
    b.append(line(590, 132, 590, 158, GREY, 1.2))
    b.append(box(460, 158, 260, 62, "CHIEF EXECUTIVE / DIRECTOR", ["Clinician. Accountable to the Board."], BRICK, "1"))

    # staff functions to the side
    b.append(box(50, 158, 270, 62, "OFFICE OF QUALITY & EVALUATION", ["Reports to the Board, not the CEO"], GOLD, "6"))
    b.append(line(320, 189, 460, 189, GOLD, 1.2, dash="4,3"))
    b.append(box(860, 158, 270, 62, "ETHICS & DATA GOVERNANCE", ["Standing committee + secretariat"], GREY, "3"))
    b.append(line(720, 189, 860, 189, GREY, 1.2, dash="4,3"))

    # Spine
    b.append(line(590, 220, 590, 262, GREY, 1.2))
    b.append(line(150, 262, 1030, 262, GREY, 1.2))

    depts = [
        ("CURRICULUM &\nPEDAGOGY", TEAL, "15", ["Director 1", "Instructional designers 4", "Clinical content leads 6", "Assessment psychometrician 1", "Medical editor / translator 3"]),
        ("FACULTY &\nDELIVERY", TEAL2, "18", ["Track leads 5", "Certified instructors 10", "Simulation faculty 2", "Programme manager 1"]),
        ("ENGINEERING &\nPLATFORM", GOLD, "13", ["Head of engineering 1", "Full-stack developers 5", "ML / eval engineers 3", "Data engineer 2", "DevSecOps 1", "QA engineer 1"]),
        ("SIMULATION &\nCLINICAL LABS", BRICK, "7", ["Sim centre director 1", "Sim technicians 3", "Standardised-patient lead 1", "Clinical skills tutors 2"]),
        ("OPERATIONS &\nREGISTRY", GREY, "8", ["Registrar / records 2", "Finance & procurement 2", "Partnerships 1", "Communications 1", "M&E officer 1", "Administration 1"]),
    ]
    w, gp, x0 = 202, 18, 50
    for i, (name, col, fte, roles) in enumerate(depts):
        x = x0 + i * (w + gp)
        b.append(line(x + w / 2, 262, x + w / 2, 296, GREY, 1.2))
        b.append(rect(x, 296, w, 66, WHITE, col, 1.6, 6))
        b.append(rect(x, 296, w, 5, col, col, 0, 0))
        b.append(rect(x + 8, 306, 30, 16, col, col, 0, 8))
        b.append(txt(x + 23, 318, fte, 9.6, ONCOL, weight="bold"))
        for j, part in enumerate(name.split("\n")):
            b.append(txt(x + w / 2 + 14, 322 + j * 14, part, 10.4, INK, weight="bold", ls="0.3"))
        b.append(rect(x, 372, w, 22 + len(roles) * 15, LGREY, col, 0.9, 6))
        for j, rr in enumerate(roles):
            b.append(txt(x + 12, 393 + j * 15, rr, 8.9, INK, anchor="start"))

    # affiliated
    b.append(rect(50, 546, 1080, 96, WHITE, GREY, 1.4, 6, dash="5,4"))
    b.append(txt(590, 570, "AFFILIATED AND SESSIONAL — not counted in the 71 FTE core establishment", 10.6, GREY, weight="bold", ls="0.6"))
    aff = [
        ("Clinical Champions", "2 per participating hospital,", "0.2 FTE sessional"),
        ("Visiting Faculty", "International and regional,", "short-course delivery"),
        ("Fellows", "8 per annual cohort —", "teach as they learn"),
        ("Patient & Public Panel", "12 lay members,", "curriculum and ethics review"),
    ]
    for i, (t, l1, l2) in enumerate(aff):
        x = 84 + i * 268
        b.append(txt(x, 596, t, 10, INK, anchor="start", weight="bold"))
        b.append(txt(x, 611, l1, 8.8, GREY, anchor="start"))
        b.append(txt(x, 624, l2, 8.8, GREY, anchor="start"))
    write("fig6-org-chart.svg", svg(W, H, "\n".join(b)))


# ---------------------------------------------------------------- Figure 7
# Roadmap
def fig7():
    W, H = 1080, 640
    b = []
    b.append(txt(540, 32, "FIGURE 7 — PHASED ROADMAP, MONTHS 0–36", 12, GREY, weight="bold", ls="1.4"))
    b.append(txt(540, 54, "Headcount shown is cumulative core establishment at the end of each phase.", 11, GREY))

    left, right = 250, 1040
    top = 116
    months = 36
    def mx(m):
        return left + (right - left) * m / months

    # axis
    b.append(line(left, top - 22, right, top - 22, GREY, 1))
    for m in range(0, months + 1, 3):
        b.append(line(mx(m), top - 26, mx(m), top - 18, GREY, 1))
        b.append(txt(mx(m), top - 32, f"M{m}", 8.8, GREY))

    # phase bands
    phases = [
        (0, 6, "PHASE 0 — FOUNDING", TEAL, "9 FTE"),
        (6, 15, "PHASE 1 — PROVE IT", TEAL2, "26 FTE"),
        (15, 27, "PHASE 2 — SCALE", GOLD, "50 FTE"),
        (27, 36, "PHASE 3 — INSTITUTIONALISE", BRICK, "71 FTE"),
    ]
    for s, e, name, col, hc in phases:
        b.append(rect(mx(s), top - 12, mx(e) - mx(s), 26, col, col, 0, 4, op=0.14))
        b.append(txt((mx(s) + mx(e)) / 2, top + 5, name, 9.4, col, weight="bold", ls="0.6"))
        b.append(txt((mx(s) + mx(e)) / 2, top + 480, hc, 11, col, weight="bold"))
        b.append(line(mx(e), top - 12, mx(e), top + 462, col, 0.8, dash="3,4"))

    rows = [
        ("Governance, legal form, Board appointed", 0, 5, TEAL),
        ("Founding team recruited (9 FTE)", 0, 6, TEAL),
        ("Competency standards agreed with councils", 2, 9, TEAL),
        ("Common core (L1) written and peer-reviewed", 3, 9, TEAL),
        ("Sandbox + de-identified case corpus built", 4, 12, TEAL2),
        ("Instructor certification (L4) first cohort", 7, 11, TEAL2),
        ("Pilot: 120 learners, one teaching hospital", 9, 15, TEAL2),
        ("Independent evaluation of pilot published", 13, 17, TEAL2),
        ("Tracks A–C at L2/L3 in full delivery", 15, 30, GOLD),
        ("Tracks D–E launched", 17, 27, GOLD),
        ("Simulation centre and AI-OSCE operational", 15, 22, GOLD),
        ("Mobile/hybrid delivery to county hospitals", 19, 34, GOLD),
        ("Clinical AI Fellowship — first cohort of 8", 22, 34, BRICK),
        ("Council-recognised CPD accreditation secured", 20, 26, BRICK),
        ("Regional (EAC) faculty exchange opens", 27, 36, BRICK),
        ("First annual public outcomes report", 30, 33, BRICK),
    ]
    rh = 27
    for i, (name, s, e, col) in enumerate(rows):
        y = top + 34 + i * rh
        if i % 2 == 0:
            b.append(rect(20, y - 12, right - 20, rh - 4, LGREY, LGREY, 0, 3, op=0.55))
        b.append(txt(30, y + 4, name, 9.8, INK, anchor="start"))
        b.append(rect(mx(s), y - 6, max(mx(e) - mx(s), 6), 15, col, col, 0, 7, op=0.88))
        if e >= 33:
            b.append(txt(mx(s) - 8, y + 4, f"M{s}–{e}", 8, GREY, anchor="end"))
        else:
            b.append(txt(mx(e) + 8, y + 4, f"M{s}–{e}", 8, GREY, anchor="start"))

    write("fig7-roadmap.svg", svg(W, H, "\n".join(b)))


# ---------------------------------------------------------------- Figure 8
# Trust calibration
def fig8():
    W, H = 980, 560
    b = []
    b.append(txt(490, 32, "FIGURE 8 — CALIBRATED TRUST: THE CENTRAL PEDAGOGICAL TARGET", 12, GREY, weight="bold", ls="1.4"))
    b.append(txt(490, 55, "Training that raises confidence without raising scepticism makes clinicians more dangerous, not less.", 11.5, GREY, style="italic"))

    ox, oy = 130, 440
    aw, ah = 700, 330
    b.append(line(ox, oy, ox + aw, oy, GREY, 1.4, marker=True))
    b.append(line(ox, oy, ox, oy - ah, GREY, 1.4, marker=True))
    b.append(txt(ox + aw / 2, oy + 42, "TRUST PLACED IN THE AI  →", 10.6, INK, weight="bold", ls="0.8"))
    b.append(f'<text x="{28}" y="{oy - ah/2}" font-family="{FONT}" font-size="10.6" fill="{INK}" '
             f'text-anchor="middle" font-weight="bold" letter-spacing="0.8" '
             f'transform="rotate(-90 28 {oy - ah/2})">PATIENT SAFETY  →</text>')

    # inverted-U curve
    b.append(path(f"M {ox+20} {oy-40} Q {ox+230} {oy-330} {ox+400} {oy-300} Q {ox+560} {oy-274} {ox+680} {oy-24}",
                  stroke=TEAL, sw=3))

    zones = [
        (ox + 20, ox + 210, "UNDER-TRUST", BRICK,
         ["Refuses a tool that would have helped.", "Misses the retinopathy the screening", "model flagged. Slower, not safer."]),
        (ox + 230, ox + 470, "CALIBRATED TRUST", TEAL,
         ["Consults deliberately, forms an", "independent impression first,", "verifies, documents, owns it.", "THIS IS WHAT WE TEACH."]),
        (ox + 490, ox + 690, "OVER-TRUST", BRICK,
         ["Accepts a confident, fluent,", "wrong answer. Automation bias.", "Skill decay. Harm."]),
    ]
    for x1, x2, name, col, lines in zones:
        b.append(rect(x1, oy - ah - 6, x2 - x1, ah + 6, col, col, 0, 4, op=0.07))
        ty = oy - ah + 16 if col != TEAL else oy - 150
        b.append(txt((x1 + x2) / 2, ty, name, 11.4, col, weight="bold", ls="1"))
        for j, ln in enumerate(lines):
            b.append(txt((x1 + x2) / 2, ty + 20 + j * 13.5, ln, 9,
                         INK if col == TEAL else GREY,
                         weight="bold" if ln.startswith("THIS") else "normal"))

    # marker at peak
    b.append(f'<circle cx="{ox+400}" cy="{oy-300}" r="7" fill="{WHITE}" stroke="{TEAL}" stroke-width="3"/>')

    # evidence note
    b.append(rect(130, 486, 700, 56, LBRICK, BRICK, 1.3, 6))
    b.append(txt(146, 506, "The evidence we are designing against:", 10, BRICK, anchor="start", weight="bold"))
    b.append(txt(146, 522, "A 2025 randomised trial found that physicians who had already completed 20 hours of AI-literacy training still deferred to", 9.2, INK, anchor="start"))
    b.append(txt(146, 535, "deliberately erroneous LLM output. Literacy alone does not confer discernment. Discernment must be trained and tested directly.", 9.2, INK, anchor="start"))
    write("fig8-calibrated-trust.svg", svg(W, H, "\n".join(b)))


for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8):
    f()

# The blog post wants 2x PNGs named fig-01..fig-08; the PDF consumes the SVGs directly.
if THEME == "dark":
    import cairosvg
    for i, stem in enumerate([
        "fig1-architecture", "fig2-clinical-4d", "fig3-curriculum-matrix",
        "fig4-assessment-pyramid", "fig5-quality-loop", "fig6-org-chart",
        "fig7-roadmap", "fig8-calibrated-trust"], start=1):
        src = os.path.join(OUT, stem + ".svg")
        cairosvg.svg2png(url=src, write_to=os.path.join(OUT, f"fig-{i:02d}.png"), scale=2.0)
        os.remove(src)
    print("converted to 2x PNG, removed intermediate SVGs")

print("done")
