#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build typeset, cover-paged A4 PDFs for the four companion essays to
"Another Arrow in the Quiver", matching the visual identity of the
already-published Blueprint PDF (see ../build_pdf.py).

Output goes to ./companion-essays/*.pdf — a holding area, NOT ../static/.
Nothing here touches content/posts/*.md or static/. Review first.
"""
import os
import re
import subprocess
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))          # .../kenya-clinical-ai-institute/companion-essays
KCAI = os.path.dirname(BASE)                                # .../kenya-clinical-ai-institute
SITE = os.path.dirname(KCAI)                                # .../drnealaggarwal.info  (weasyprint base_url)
POSTS = os.path.join(SITE, "content", "posts")
OUT = BASE

SITE_URL = "https://drnealaggarwal.info"

CSS_TEMPLATE = r"""
@page {
  size: A4;
  margin: 22mm 20mm 20mm 20mm;
  @bottom-center {
    content: counter(page);
    font-family: "Carlito", "DejaVu Sans", sans-serif;
    font-size: 8.5pt; color: #8A979C;
  }
  @top-center {
    content: "__RUNNING_HEAD__";
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
  font-family: "Carlito", sans-serif; font-size: 29pt; font-weight: 700;
  line-height: 1.14; letter-spacing: -0.01em; margin: 0 0 7mm 0; text-align: left;
}
.cover-sub {
  font-size: 12.4pt; line-height: 1.45; color: #DCEBE8; text-align: left;
  max-width: 138mm; font-style: italic;
}
.cover-lower { position: absolute; top: 138mm; left: 20mm; right: 20mm; }
.cover-author { font-family: "Carlito", sans-serif; font-size: 15pt; font-weight: 700; color: #0B4F4A; }
.cover-role { font-size: 10.4pt; color: #5E6E74; margin-top: 2mm; }
.cover-date { font-family: "Carlito", sans-serif; font-size: 9pt; color: #8A979C;
  letter-spacing: 0.14em; text-transform: uppercase; margin-top: 9mm; }
.cover-abstract {
  margin-top: 14mm; padding: 7mm 8mm; background: #F2F6F5; border-left: 3px solid #0B4F4A;
  font-size: 9.6pt; line-height: 1.55; color: #2C3D43; text-align: left;
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
table { table-layout: auto; hyphens: none; -weasy-hyphens: none; }

/* ---------- figures ---------- */
img { width: 100%; height: auto; display: block; margin: 6mm 0 6mm 0;
      page-break-inside: avoid; border-radius: 6px; }
figure { margin: 6mm 0 7mm 0; page-break-inside: avoid; }
figure img, .kcai-fig img, .kp-fig img, .kp-fig svg { margin: 0 0 2.5mm 0; }
figcaption, .kcai-fig figcaption, .kp-fig figcaption {
  font-family: "Carlito", sans-serif; font-size: 8.6pt; font-style: italic;
  color: #5E6E74; text-align: center; margin: 1mm 4mm 0 4mm; line-height: 1.4;
}
p:has(> img) { page-break-inside: avoid; }

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
.toc-part { font-size: 10.1pt; font-weight: 700; color: #0B4F4A;
  border-top: 0.4pt solid #E2E8E9; padding-top: 2.6mm !important; margin-top: 1.6mm !important; }
.toc-sub { font-size: 9.2pt; padding-left: 6mm; }
.toc-sub a { color: #37484E; }

h2.part { page-break-before: always; font-size: 17pt; color: #0B4F4A;
  border-bottom: 1.4pt solid #0B4F4A; padding-bottom: 2.2mm; margin-top: 2mm; }

/* ---------- rules ---------- */
hr { border: none; border-top: 0.5pt solid #D9E1E3; margin: 7mm 0; }
a { color: #0B4F4A; text-decoration: none; word-break: break-word; }

/* ---------- print-safe overrides for the blog's dark inline/class callouts ----------
   Source palette (from the site's dark theme): cyan #101a2e/#00d4f5,
   green #0e1e1a/#10b981, red #1a0f14/#f87171, grey #111827/#6b82a0,
   amber aside #0d1424/#f59e0b, indigo aside #1a1f2e/#1a237e,
   violet note #141033/#a78bfa. Re-tinted light for a printed page. */
div[style*="background:#101a2e"] { background:#EAF7FB !important; border-left-color:#00B7D6 !important; color:#123A42 !important; }
div[style*="background:#0e1e1a"] { background:#EAF7F0 !important; border-left-color:#0E9F73 !important; color:#0B3B2C !important; }
div[style*="background:#1a0f14"] { background:#FBEAEA !important; border-left-color:#E15C5C !important; color:#4A0F14 !important; }
div[style*="background:#111827"] { background:#EEF1F4 !important; border-left-color:#6B82A0 !important; color:#2C3D43 !important; }
div[style*="background:#0d1424"] { background:#FFF6E8 !important; border-left-color:#D98A1D !important; color:#4A2C0F !important; }
div[style*="background:#1a1f2e"] { background:#EEF0FA !important; border-left-color:#3949AB !important; color:#232C56 !important; }
div[style*="background:#141033"] { background:#F3EFFF !important; border-left-color:#8B6FE0 !important; color:#3B2E66 !important; }
div[style*="color:#9fb3cc"] { color:#37484E !important; }
div[style*="color:#c9d6e8"] { color:#33424E !important; }
a[style*="color:#00d4f5"] { color:#0B4F4A !important; }

/* class-based callouts used by the Kirkpatrick post (its own <style> block is stripped) */
.kp-callout { font-size: 0.92em; background:#EAF7FB; border-left:4px solid #00B7D6; padding:0.9em 1.3em; margin:1.4em 0; border-radius:0 4px 4px 0; color:#123A42; }
.kp-warn    { font-size: 0.92em; background:#FBEAEA; border-left:4px solid #E15C5C; padding:0.9em 1.3em; margin:1.4em 0; border-radius:0 4px 4px 0; color:#4A0F14; }
.kp-key     { font-size: 0.95em; background:#EAF7F0; border-left:4px solid #0E9F73; padding:0.9em 1.3em; margin:1.4em 0; border-radius:0 4px 4px 0; color:#0B3B2C; }
.kp-note    { font-size: 0.9em;  background:#F3EFFF; border-left:4px solid #8B6FE0; padding:0.9em 1.3em; margin:1.4em 0; border-radius:0 4px 4px 0; color:#3B2E66; }
.kp-fig     { margin: 5mm 0 6mm 0; }
"""

COVER_TEMPLATE = """
<div class="cover">
  <div class="cover-band"></div>
  <div class="cover-rule"></div>
  <div class="cover-inner">
    <div class="cover-kicker">__KICKER__</div>
    <div class="cover-title">__TITLE__</div>
    <div class="cover-sub">__DEK__</div>
  </div>
  <div class="cover-lower">
    <div class="cover-author">Dr Neal Aggarwal</div>
    <div class="cover-role">Medicine &nbsp;·&nbsp; Surgery &nbsp;·&nbsp; Engineering &nbsp;·&nbsp; Information Technology &nbsp;·&nbsp; Artificial Intelligence</div>
    <div class="cover-date">__DATE__</div>
    <div class="cover-abstract">
      __ABSTRACT__
    </div>
  </div>
  <div class="cover-foot">
    Written in a personal capacity &nbsp;·&nbsp; Essay __NUM__ of 5 in &ldquo;The Argument in Order&rdquo; &nbsp;·&nbsp; __READTIME__ read &nbsp;·&nbsp; Draft for review
  </div>
</div>
"""

ENTRIES = [
    dict(
        md="2026-08-10-borrowed-from-an-art-school.md",
        num=2,
        main_title="Borrowed From an Art School",
        dek="Where the competency framework came from, and why its provenance outside "
            "medicine is the reason it transfers to clinical work.",
        date_human="10 August 2026",
        read_time="11 min",
        outfile="Borrowed-From-an-Art-School.pdf",
        summary=(
            "<strong>The competency framework underneath my clinical AI blueprint was not built "
            "for medicine.</strong> It came out of an art school in Sarasota and a business school "
            "in Cork, developed by a novelist-turned-AI-coordinator and an information systems "
            "professor. That provenance is not a curiosity — it is the reason the framework "
            "transfers to clinical work at all. A framework built for medicine would have "
            "hard-coded medicine into it. This essay sets out what Dakan and Feller built, what I "
            "kept, what I reframed, and the one thing I had to add because creative work does not "
            "kill anyone."
        ),
    ),
    dict(
        md="2026-08-11-one-hidden-error.md",
        num=3,
        main_title="One Hidden Error",
        dek="What an OSCE is, and what an AI-OSCE would be — the examination the whole "
            "blueprint rests on.",
        date_human="11 August 2026",
        read_time="21 min",
        outfile="One-Hidden-Error.pdf",
        summary=(
            "<strong>The blueprint rests on an examination that does not yet exist.</strong> This "
            "essay explains the machinery it borrows: what an OSCE is, the problem Harden was "
            "solving in Dundee when he built the first one, why a written paper can never certify "
            "a clinical skill, and what changes when the thing being examined is a doctor&rsquo;s "
            "judgement about a machine. Along the way: what conjunctive failure means and why some "
            "errors cannot be compensated, why a standardised patient is a trained professional and "
            "not a volunteer, and why the pass mark is never 50%."
        ),
    ),
    dict(
        md="2026-08-12-the-angoff-panel-for-testing-clinicians.md",
        num=4,
        main_title="The Angoff Panel for Testing Clinicians",
        dek="Where the pass mark comes from, and why an arbitrary 50% cannot be defended when a "
            "certificate is a safety claim.",
        date_human="12 August 2026",
        read_time="21 min",
        outfile="The-Angoff-Panel-for-Testing-Clinicians.pdf",
        summary=(
            "One line on one slide of the Level 1 deck reads: <em>Standard set by modified Angoff "
            "panel (No arbitrary 50% pass rate).</em> It is the least glamorous sentence in the "
            "whole curriculum and possibly the most consequential. <strong>This essay unpacks it "
            "completely</strong> — what a cut score actually is, why 50% is indefensible and "
            "norm-referencing is worse, who the borderline candidate is and how you build one, the "
            "mechanism step by step with a full worked panel whose arithmetic you can check, what "
            "&ldquo;modified&rdquo; really means, what the 2025 meta-analysis of 91 studies says "
            "about which variant to choose, and precisely where Angoff stops working."
        ),
    ),
    dict(
        md="2026-08-17-measuring-what-actually-matters.md",
        num=5,
        main_title="Measuring What Actually Matters",
        dek="Kirkpatrick levels 3 and 4: how you find out whether any of it changed behaviour or "
            "helped a patient.",
        date_human="17 August 2026",
        read_time="41 min",
        outfile="Measuring-What-Actually-Matters.pdf",
        summary=(
            "The tenth of the Institute&rsquo;s ten pedagogical commitments is one sentence long: "
            "<em>we measure at Kirkpatrick 3 and 4, or we admit we do not know.</em> "
            "<strong>This essay unpacks that sentence completely</strong>, starting from zero: what "
            "the four Kirkpatrick levels are and why almost every training programme stops at the "
            "second one; what &ldquo;behaviour&rdquo; means when the behaviour in question is a "
            "habit of mind; how you would actually observe, audit and log a student-clinician at "
            "three and twelve months without fooling yourself; why the independent-impression rule "
            "is the fastest-decaying thing taught, and what would refute that; what a stepped-wedge "
            "design buys you and costs; and a working catalogue of the other pedagogical instruments "
            "— entrustment, programmatic assessment, Angoff, retrospective pre-post, logic "
            "models, audit and feedback."
        ),
    ),
]

RUNNING_HEAD = "The Kenya Institute for Clinical Artificial Intelligence  ·  The Argument in Order"


def strip_front_matter(raw):
    return re.sub(r"^---\n.*?\n---\n", "", raw, count=1, flags=re.S)


def strip_hero_image(body):
    return re.sub(r'\s*<a href="[^"]*"[^>]*>\s*<img[^>]*/?>\s*</a>\s*', "\n\n", body, count=1)


def strip_companion_disclaimer(body):
    return re.sub(
        r'<div style="font-size:0\.85em; background:#111827;.*?</div>\s*',
        "",
        body,
        count=1,
        flags=re.S,
    )


def strip_embedded_style_block(body):
    return re.sub(r"<style>.*?</style>\s*", "", body, count=1, flags=re.S)


def fix_links(body):
    body = re.sub(r'href="/', f'href="{SITE_URL}/', body)
    body = re.sub(r'src="' + re.escape(SITE_URL) + r'/static/', 'src="static/', body)
    body = re.sub(r'src="/static/', 'src="static/', body)
    return body


def build_one(entry):
    md_path = os.path.join(POSTS, entry["md"])
    with open(md_path, encoding="utf-8") as f:
        raw = f.read()

    body_md = strip_front_matter(raw)
    body_md = strip_hero_image(body_md)
    body_md = strip_companion_disclaimer(body_md)
    if entry["md"].startswith("2026-08-17"):
        body_md = strip_embedded_style_block(body_md)

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(body_md)
        tmp_md = tmp.name
    try:
        body = subprocess.run(
            ["pandoc", tmp_md, "-f", "markdown-implicit_figures+pipe_tables",
             "-t", "html5", "--no-highlight"],
            capture_output=True, text=True, check=True,
        ).stdout
    finally:
        os.unlink(tmp_md)

    body = fix_links(body)

    body = re.sub(
        r'<ol start="(\d+)"([^>]*)>',
        lambda m: f'<ol style="counter-reset: list-item {int(m.group(1)) - 1}"{m.group(2)}>',
        body,
    )
    body = re.sub(r"<colgroup>.*?</colgroup>", "", body, flags=re.S)

    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S)

    def _strip_tags(t):
        return re.sub(r"<[^>]+>", "", t).strip()

    has_parts = any(_strip_tags(t).startswith("Part ") for _, t in heads)

    def _mark(m):
        hid, text = m.group(1), m.group(2)
        plain = _strip_tags(text)
        if has_parts and (plain.startswith("Part ") or plain in ("References", "Coda")):
            return f'<h2 class="part" id="{hid}">{text}</h2>'
        return m.group(0)

    body = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', _mark, body, flags=re.S)

    toc_rows = []
    for hid, text in heads:
        plain = _strip_tags(text)
        if has_parts:
            cls = "toc-part" if (plain.startswith("Part ") or plain in ("References", "Coda")) else "toc-sub"
        else:
            cls = "toc-part"
        toc_rows.append(f'<li class="{cls}"><a href="#{hid}">{plain}</a></li>')
    toc = ('<div class="toc"><h2 class="toc-head">Contents</h2><ul>'
           + "".join(toc_rows) + "</ul></div>")

    cover = (COVER_TEMPLATE
             .replace("__KICKER__", "A Companion Essay &nbsp;·&nbsp; Nairobi &nbsp;·&nbsp; 2026")
             .replace("__TITLE__", entry["main_title"])
             .replace("__DEK__", entry["dek"])
             .replace("__DATE__", entry["date_human"].upper())
             .replace("__ABSTRACT__", entry["summary"])
             .replace("__NUM__", str(entry["num"]))
             .replace("__READTIME__", entry["read_time"]))

    css = CSS_TEMPLATE.replace("__RUNNING_HEAD__", RUNNING_HEAD)

    html = f"""<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8">
<title>{entry['main_title']} — The Kenya Institute for Clinical Artificial Intelligence</title>
<style>{css}</style>
</head><body>
{cover}
{toc}
<div class="doc">
{body}
</div>
</body></html>"""

    html_path = os.path.join(tempfile.gettempdir(), f"_companion_{entry['num']}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    from weasyprint import HTML as WHTML
    out_path = os.path.join(OUT, entry["outfile"])
    WHTML(filename=html_path, base_url=SITE).write_pdf(out_path)
    size = os.path.getsize(out_path)
    print(f"built {out_path}  ({size/1024:.0f} KB)")


def main():
    os.makedirs(OUT, exist_ok=True)
    for entry in ENTRIES:
        build_one(entry)


if __name__ == "__main__":
    main()
