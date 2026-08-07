#!/usr/bin/env python3
"""Build the three annexes into typeset PDFs, in the house style of the blueprint.

    python3 build_annexes.py

Reads  ./annexes/*.md
Writes ./annexes/*.pdf
"""
import os
import re
import subprocess
import tempfile

from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
ANNEX = os.path.join(HERE, "annexes")

DOCS = [
    ("A-business-case.md", "A", "The Business Case",
     "Kenya Institute for Clinical Artificial Intelligence — a proposal to the Board",
     "Annex A"),
    ("B-competency-standards.md", "B", "Competency Standards in Clinical Artificial Intelligence",
     "A draft for consideration by KMPDC and the Nursing Council of Kenya",
     "Annex B"),
    ("C-level-1-common-core.md", "C", "Level 1 — The Common Core",
     "Twelve hours, every cadre, taught together. Facilitator edition.",
     "Annex C"),
]

CSS = r"""
@page {
  size: A4;
  margin: 22mm 20mm 20mm 20mm;
  @bottom-center { content: counter(page);
    font-family: "Carlito", "DejaVu Sans", sans-serif; font-size: 8.5pt; color: #8A979C; }
  @top-center { content: "%RUNNING%";
    font-family: "Carlito", "DejaVu Sans", sans-serif;
    font-size: 7.6pt; color: #A9B4B8; letter-spacing: 0.06em; }
}
@page :first { @top-center { content: ""; } @bottom-center { content: ""; } }
@page cover { margin: 0; @top-center{content:""} @bottom-center{content:""} }

html { font-size: 10.4pt; }
body { font-family: "Bitstream Charter", "Charter", "DejaVu Serif", serif;
  color: #16272C; line-height: 1.52; text-align: justify; hyphens: auto; -weasy-hyphens: auto; }

.cover { page: cover; height: 297mm; position: relative; page-break-after: always; }
.cover-band { position: absolute; top:0; left:0; right:0; height: 112mm; background: %BAND%; }
.cover-rule { position: absolute; top: 112mm; left:0; right:0; height: 3mm; background: #B5822A; }
.cover-inner { position: absolute; top: 26mm; left: 20mm; right: 20mm; color: #FFFFFF; }
.cover-kicker { font-family:"Carlito",sans-serif; font-size: 8.6pt; letter-spacing: .24em;
  text-transform: uppercase; color: #9FC9C2; margin-bottom: 10mm; }
.cover-letter { font-family:"Carlito",sans-serif; font-size: 74pt; font-weight:700;
  color: rgba(255,255,255,0.18); line-height: 1; margin: 0 0 2mm 0; }
.cover-title { font-family:"Carlito",sans-serif; font-size: 30pt; font-weight:700;
  line-height: 1.12; margin: 0 0 6mm 0; text-align:left; }
.cover-sub { font-size: 12pt; line-height: 1.45; color: #DCEBE8; text-align:left;
  max-width: 130mm; font-style: italic; }
.cover-lower { position:absolute; top: 132mm; left: 20mm; right: 20mm; }
.cover-author { font-family:"Carlito",sans-serif; font-size: 14pt; font-weight:700; color: %BAND%; }
.cover-role { font-size: 10pt; color:#5E6E74; margin-top: 2mm; }
.cover-date { font-family:"Carlito",sans-serif; font-size: 9pt; color:#8A979C;
  letter-spacing:.14em; text-transform:uppercase; margin-top: 8mm; }
.cover-foot { position:absolute; bottom: 18mm; left: 20mm; right: 20mm;
  font-family:"Carlito",sans-serif; font-size: 8.2pt; color:#A9B4B8;
  border-top: .5pt solid #D9E1E3; padding-top: 3mm; }

h1 { font-family:"Carlito",sans-serif; font-size: 19pt; font-weight:700; color: %BAND%;
  margin: 0 0 2mm 0; padding-top: 3mm; text-align:left; line-height:1.15;
  page-break-before: always; page-break-after: avoid; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-family:"Carlito",sans-serif; font-size: 13.4pt; font-weight:700; color:#12262B;
  margin: 8mm 0 3mm 0; text-align:left; page-break-after: avoid; line-height:1.22;
  border-bottom: .9pt solid #B5822A; padding-bottom: 1.6mm; }
h3 { font-family:"Carlito",sans-serif; font-size: 11.2pt; font-weight:700; color: %BAND%;
  margin: 6mm 0 2mm 0; text-align:left; page-break-after: avoid; }
h4 { font-family:"Carlito",sans-serif; font-size: 10pt; font-weight:700; color:#12262B;
  margin: 4.5mm 0 1.5mm 0; text-align:left; page-break-after: avoid; }

p { margin: 0 0 2.6mm 0; orphans:2; widows:2; }
strong { color:#0B2E33; font-weight:700; }

blockquote { margin: 5mm 0; padding: 4.5mm 6mm; background:#EEF4F3;
  border-left: 3.5pt solid %BAND%; font-size: 10.4pt; line-height:1.45; color:#0B3B3E;
  text-align:left; page-break-inside: avoid; }
blockquote p { margin: 0 0 2mm 0; }
blockquote p:last-child { margin: 0; }

ul, ol { margin: 0 0 3mm 0; padding-left: 6.5mm; }
li { margin-bottom: 1.4mm; }

table { width:100%; border-collapse: collapse; margin: 4.5mm 0 5.5mm 0;
  font-size: 8.6pt; line-height:1.34; page-break-inside: avoid;
  font-family:"Carlito",sans-serif; text-align:left; table-layout:auto;
  hyphens:none; -weasy-hyphens:none; }
thead { background: %BAND%; }
thead th { color:#FFFFFF; font-weight:700; text-align:left; padding: 2.2mm 2.4mm;
  font-size: 8.3pt; vertical-align:bottom; }
tbody td { padding: 2mm 2.4mm; border-bottom: .4pt solid #DCE3E5; vertical-align: top; }
tbody tr:nth-child(even) { background:#F5F8F8; }
tbody tr:last-child td { border-bottom: .8pt solid %BAND%; }
table strong { color: %BAND%; }

hr { border:none; border-top: .5pt solid #D9E1E3; margin: 7mm 0; }
a { color: %BAND%; text-decoration:none; word-break: break-all; }

.caution { background:#FAEEEB; border-left: 3.5pt solid #A63A2B;
  padding: 4.5mm 6mm; margin: 5mm 0; font-size: 9.8pt; text-align:left;
  page-break-inside: avoid; }
.caution p { margin: 0 0 2mm 0; }
.caution p:last-child { margin: 0; }
"""

BANDS = {"A": "#0B4F4A", "B": "#1E3A5F", "C": "#7A4A18"}


def build(fname, letter, title, subtitle, kicker):
    src = os.path.join(ANNEX, fname)
    body = subprocess.run(
        ["pandoc", src, "-f", "markdown-implicit_figures+pipe_tables",
         "-t", "html5", "--no-highlight"],
        capture_output=True, text=True, check=True).stdout

    # drop the h1/h3 pandoc lifts from the YAML-styled heading block
    body = re.sub(r'<h1[^>]*>' + re.escape(title) + r'</h1>\s*', '', body, count=1)
    # strip the leading subtitle h3 (whatever its wording) if it precedes the first h2
    m3, m2 = re.search(r'<h3[^>]*>.*?</h3>\s*', body, re.S), re.search(r'<h2', body)
    if m3 and (not m2 or m3.start() < m2.start()):
        body = body[:m3.start()] + body[m3.end():]
    body = re.sub(r'^\s*(<hr\s*/?>\s*)+', '', body, count=1)
    body = re.sub(r'<ol start="(\d+)"([^>]*)>',
                  lambda m: f'<ol style="counter-reset: list-item {int(m.group(1))-1}"{m.group(2)}>',
                  body)
    body = re.sub(r'<colgroup>.*?</colgroup>', '', body, flags=re.S)

    band = BANDS[letter]
    css = (CSS.replace("%BAND%", band)
              .replace("%RUNNING%", f"{kicker} · {title}"))

    cover = f"""
    <div class="cover">
      <div class="cover-band"></div><div class="cover-rule"></div>
      <div class="cover-inner">
        <div class="cover-kicker">{kicker} &nbsp;·&nbsp; Kenya Institute for Clinical AI</div>
        <div class="cover-letter">{letter}</div>
        <div class="cover-title">{title}</div>
        <div class="cover-sub">{subtitle}</div>
      </div>
      <div class="cover-lower">
        <div class="cover-author">Dr Neal Aggarwal</div>
        <div class="cover-role">Written in a personal capacity</div>
        <div class="cover-date">August 2026</div>
      </div>
      <div class="cover-foot">Annex to <em>Another Arrow in the Quiver</em> &nbsp;·&nbsp;
        drnealaggarwal.info</div>
    </div>"""

    html = (f'<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">'
            f'<title>{title}</title><style>{css}</style></head><body>'
            f'{cover}<div class="doc">{body}</div></body></html>')

    tmp = os.path.join(tempfile.gettempdir(), f"_annex_{letter}.html")
    open(tmp, "w").write(html)
    out = os.path.join(ANNEX, fname.replace(".md", ".pdf"))
    HTML(filename=tmp, base_url=ANNEX).write_pdf(out)
    return out


if __name__ == "__main__":
    for args in DOCS:
        p = build(*args)
        print(f"  {os.path.basename(p)}  {os.path.getsize(p)//1024} KB")
