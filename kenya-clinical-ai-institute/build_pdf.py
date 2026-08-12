#!/usr/bin/env python3
"""Build the typeset PDF from the markdown source."""
import subprocess, os, re, shutil, tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(BASE)
MD   = os.path.join(BASE, "kenya-clinical-ai-institute.md")
HTML = os.path.join(tempfile.gettempdir(), "_kcai_build.html")
PDF  = os.path.join(BASE, "Kenya-Institute-for-Clinical-AI-Blueprint.pdf")
# the copy the blog post links to
PUBLISHED = os.path.join(SITE, "static", "Kenya_Institute_for_Clinical_AI_Blueprint.pdf")

body = subprocess.run(
    ["pandoc", MD, "-f", "markdown-implicit_figures+pipe_tables", "-t", "html5", "--no-highlight"],
    capture_output=True, text=True, check=True).stdout

# Strip the YAML-derived title block if pandoc emitted one, and the first duplicated H1/H3
body = re.sub(r'<h1[^>]*>Another Arrow in the Quiver</h1>\s*', '', body, count=1)
body = re.sub(r'<h3[^>]*>What I would build to teach clinical artificial intelligence.*?</h3>\s*',
              '', body, count=1, flags=re.S)
# Remove the leading horizontal rules left over from the front matter
body = re.sub(r'^\s*(<hr\s*/?>\s*)+', '', body, count=1)

# WeasyPrint ignores <ol start="n">; translate it into a counter reset
body = re.sub(r'<ol start="(\d+)"([^>]*)>',
              lambda m: f'<ol style="counter-reset: list-item {int(m.group(1)) - 1}"{m.group(2)}>',
              body)

# Drop pandoc's colgroup width hints so tables use automatic layout
body = re.sub(r'<colgroup>.*?</colgroup>', '', body, flags=re.S)

# Let the widest diagrams break out of the text measure
for wide in ("fig3-curriculum-matrix", "fig6-org-chart", "fig7-roadmap", "fig1-architecture"):
    body = body.replace(f'src="figures/{wide}.svg"', f'class="wide" src="figures/{wide}.svg"')

# Mark the Part-level headings so each opens on a fresh page, and build the contents list
heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S)
def _strip(t):
    return re.sub(r'<[^>]+>', '', t).strip()

def _mark(m):
    hid, text = m.group(1), m.group(2)
    plain = _strip(text)
    if plain.startswith("Part ") or plain in ("References", "Closing"):
        return f'<h2 class="part" id="{hid}">{text}</h2>'
    return m.group(0)
body = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', _mark, body, flags=re.S)

toc_rows = []
for hid, text in heads:
    plain = _strip(text)
    if plain in ("Attribution",):
        continue
    cls = "toc-part" if (plain.startswith("Part ") or plain in ("References", "Closing", "A note on why I am writing this")) else "toc-sub"
    toc_rows.append(f'<li class="{cls}"><a href="#{hid}">{plain}</a></li>')
toc = ('<div class="toc"><h2 class="toc-head">Contents</h2><ul>'
       + "".join(toc_rows) + "</ul></div>")

CSS = r"""
@page {
  size: A4;
  margin: 22mm 20mm 20mm 20mm;
  @bottom-center {
    content: counter(page);
    font-family: "Carlito", "DejaVu Sans", sans-serif;
    font-size: 8.5pt; color: #8A979C;
  }
  @top-center {
    content: "The Kenya Institute for Clinical Artificial Intelligence  ·  A Blueprint";
    font-family: "Carlito", "DejaVu Sans", sans-serif;
    font-size: 7.6pt; color: #A9B4B8; letter-spacing: 0.06em;
  }
}
@page :first { @top-center { content: ""; } @bottom-center { content: ""; } }
@page cover { margin: 0; @top-center{content:""} @bottom-center{content:""} }

html { font-size: 10.4pt; }
body {
  font-family: "Bitstream Charter", "Charter", "DejaVu Serif", serif;
  color: #16272C; line-height: 1.52; text-align: justify;
  hyphens: auto; -weasy-hyphens: auto;
}

/* ---------- cover ---------- */
.cover { page: cover; height: 297mm; position: relative; page-break-after: always; }
.cover-band { position: absolute; top: 0; left: 0; right: 0; height: 118mm; background: #0B4F4A; }
.cover-rule { position: absolute; top: 118mm; left: 0; right: 0; height: 3mm; background: #B5822A; }
.cover-inner { position: absolute; top: 26mm; left: 20mm; right: 20mm; color: #FFFFFF; }
.cover-kicker {
  font-family: "Carlito", sans-serif; font-size: 8.6pt; letter-spacing: 0.24em;
  text-transform: uppercase; color: #9FC9C2; margin-bottom: 12mm;
}
.cover-title {
  font-family: "Carlito", sans-serif; font-size: 33pt; font-weight: 700;
  line-height: 1.1; letter-spacing: -0.01em; margin: 0 0 7mm 0; text-align: left;
}
.cover-sub {
  font-size: 12.4pt; line-height: 1.45; color: #DCEBE8; text-align: left;
  max-width: 132mm; font-style: italic;
}
.cover-lower { position: absolute; top: 138mm; left: 20mm; right: 20mm; }
.cover-author { font-family: "Carlito", sans-serif; font-size: 15pt; font-weight: 700; color: #0B4F4A; }
.cover-role { font-size: 10.4pt; color: #5E6E74; margin-top: 2mm; }
.cover-date { font-family: "Carlito", sans-serif; font-size: 9pt; color: #8A979C;
  letter-spacing: 0.14em; text-transform: uppercase; margin-top: 9mm; }
.cover-abstract {
  margin-top: 16mm; padding: 7mm 8mm; background: #F2F6F5; border-left: 3px solid #0B4F4A;
  font-size: 9.8pt; line-height: 1.55; color: #2C3D43; text-align: left;
}
.cover-abstract strong { color: #0B4F4A; }
.cover-foot { position: absolute; bottom: 18mm; left: 20mm; right: 20mm;
  font-family: "Carlito", sans-serif; font-size: 8.2pt; color: #A9B4B8; text-align: left;
  border-top: 0.5pt solid #D9E1E3; padding-top: 3mm; }

/* ---------- headings ---------- */
h1 {
  font-family: "Carlito", sans-serif; font-size: 20pt; font-weight: 700; color: #0B4F4A;
  margin: 0 0 2mm 0; padding-top: 4mm; text-align: left; line-height: 1.15;
  page-break-before: always; page-break-after: avoid; letter-spacing: -0.005em;
}
h1:first-of-type { page-break-before: avoid; }
h1 + h3 { margin-top: -1mm; }
h2 {
  font-family: "Carlito", sans-serif; font-size: 13.6pt; font-weight: 700; color: #12262B;
  margin: 9mm 0 3mm 0; text-align: left; page-break-after: avoid; line-height: 1.22;
  border-bottom: 0.9pt solid #B5822A; padding-bottom: 1.6mm;
}
h3 {
  font-family: "Carlito", sans-serif; font-size: 11.2pt; font-weight: 700; color: #0B4F4A;
  margin: 6.5mm 0 2mm 0; text-align: left; page-break-after: avoid; line-height: 1.28;
}
h4 { font-family: "Carlito", sans-serif; font-size: 10pt; font-weight: 700; color: #12262B;
  margin: 5mm 0 1.5mm 0; text-align: left; page-break-after: avoid; }

p { margin: 0 0 2.6mm 0; orphans: 2; widows: 2; }
strong { color: #0B2E33; font-weight: 700; }
em { font-style: italic; }

/* ---------- blockquote ---------- */
blockquote {
  margin: 5mm 0 5mm 0; padding: 4.5mm 6mm; background: #EEF4F3;
  border-left: 3.5pt solid #0B4F4A; font-size: 11pt; line-height: 1.45;
  color: #0B3B3E; text-align: left; page-break-inside: avoid;
}
blockquote p { margin: 0; }
blockquote strong { color: #0B4F4A; }

/* ---------- lists ---------- */
ul, ol { margin: 0 0 3mm 0; padding-left: 6.5mm; }
li { margin-bottom: 1.4mm; }
li > p { margin-bottom: 1.2mm; }

/* ---------- tables ---------- */
table {
  width: 100%; border-collapse: collapse; margin: 4.5mm 0 5.5mm 0;
  font-size: 8.6pt; line-height: 1.34; page-break-inside: avoid;
  font-family: "Carlito", sans-serif; text-align: left;
}
thead { background: #0B4F4A; }
thead th {
  color: #FFFFFF; font-weight: 700; text-align: left; padding: 2.2mm 2.4mm;
  font-size: 8.3pt; letter-spacing: 0.02em; vertical-align: bottom;
}
tbody td { padding: 2mm 2.4mm; border-bottom: 0.4pt solid #DCE3E5; vertical-align: top; text-align: left; }
tbody tr:nth-child(even) { background: #F5F8F8; }
tbody tr:last-child td { border-bottom: 0.8pt solid #0B4F4A; }
table strong { color: #0B4F4A; }

/* ---------- figures ---------- */
img { width: 100%; height: auto; display: block; margin: 6mm 0 6mm 0;
      page-break-inside: avoid; }
img.wide { width: 117%; margin-left: -8.5%; }
table { table-layout: auto; hyphens: none; -weasy-hyphens: none; }
tbody td:first-child, thead th:first-child { width: 21%; }

/* ---------- contents ---------- */
.toc { page-break-after: always; }
.toc-head { border-bottom: 0.9pt solid #B5822A; margin-top: 0; }
.toc ul { list-style: none; padding: 0; margin: 5mm 0 0 0; }
.toc li { margin: 0; padding: 1.5mm 0; font-family: "Carlito", sans-serif; }
.toc a { display: block; }
.toc a::after {
  content: " " leader(". ") " " target-counter(attr(href), page);
  color: #8A979C;
}
.toc-part { font-size: 10.4pt; font-weight: 700; color: #0B4F4A;
  border-top: 0.4pt solid #E2E8E9; padding-top: 2.6mm !important; margin-top: 1.6mm !important; }
.toc-sub { font-size: 9.2pt; padding-left: 6mm; }
.toc-sub a { color: #37484E; }

h2.part { page-break-before: always; font-size: 17pt; color: #0B4F4A;
  border-bottom: 1.4pt solid #0B4F4A; padding-bottom: 2.2mm; margin-top: 2mm; }
p:has(> img) { page-break-inside: avoid; }

/* ---------- rules ---------- */
hr { border: none; border-top: 0.5pt solid #D9E1E3; margin: 7mm 0; }

/* ---------- references ---------- */
.refs ol { padding-left: 7mm; }
a { color: #0B4F4A; text-decoration: none; word-break: break-all; }

/* keep the closing signature block tight */
</style>
"""

cover = """
<div class="cover">
  <div class="cover-band"></div>
  <div class="cover-rule"></div>
  <div class="cover-inner">
    <div class="cover-kicker">A Proposal &nbsp;·&nbsp; Nairobi &nbsp;·&nbsp; 2026</div>
    <div class="cover-title">Another Arrow<br/>in the Quiver</div>
    <div class="cover-sub">What I would build to teach clinical artificial intelligence to Kenya&rsquo;s doctors, surgeons and nurses &mdash; and how I would make sure it works</div>
  </div>
  <div class="cover-lower">
    <div class="cover-author">Dr Neal Aggarwal</div>
    <div class="cover-role">Medicine &nbsp;·&nbsp; Surgery &nbsp;·&nbsp; Engineering &nbsp;·&nbsp; Information Technology &nbsp;·&nbsp; Artificial Intelligence</div>
    <div class="cover-date">August 2026</div>
    <div class="cover-abstract">
      <strong>A blueprint for the Kenya Institute for Clinical Artificial Intelligence.</strong>
      A permanent national institution whose sole mandate is the clinical AI competence of an entire
      country&rsquo;s health workforce &mdash; every cadre, from the consultant surgeon to the ward nurse to the
      hospital administrator. Competency-gated certification tied to professional licensure. Assessment by
      simulation and workplace observation rather than by attendance. Outcomes published whether or not they
      flatter us. No such institution exists anywhere in the world; Kenya is positioned to build the first.
      <br/><br/>
      This document sets out the case, the institutional architecture, the pedagogy I would insist on, the
      curriculum across five professional tracks and five gated levels, the quality system, the team required
      &mdash; seventy core posts, specified by position and qualification &mdash; and a thirty-six month sequence.
    </div>
  </div>
  <div class="cover-foot">
    Written in a personal capacity &nbsp;·&nbsp; Nine figures &nbsp;·&nbsp; Seventy-one references &nbsp;·&nbsp; Draft for review
  </div>
</div>
"""

html = f"""<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8">
<title>Another Arrow in the Quiver — The Kenya Institute for Clinical Artificial Intelligence</title>
<style>{CSS}
</head><body>
{cover}
{toc}
<div class="doc">
{body}
</div>
</body></html>"""

with open(HTML, "w") as f:
    f.write(html)

from weasyprint import HTML as WHTML
WHTML(filename=HTML, base_url=BASE).write_pdf(PDF)
shutil.copyfile(PDF, PUBLISHED)
print("built    ", PDF, os.path.getsize(PDF), "bytes")
print("published", PUBLISHED)
