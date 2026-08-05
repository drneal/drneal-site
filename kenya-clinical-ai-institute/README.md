# Another Arrow in the Quiver — document source

Source for the blueprint *Another Arrow in the Quiver: What I Would Build to Teach
Clinical Artificial Intelligence to Kenya's Doctors, Surgeons and Nurses — and How I
Would Make Sure It Works.*

Published as the blog post `content/posts/2026-08-05-another-arrow-in-the-quiver.md`.

## Contents

| File | What it is |
|---|---|
| `kenya-clinical-ai-institute.md` | The document itself — the single source of truth. Edit this. |
| `figures.py` | Generates all eight figures as SVG, in two palettes. |
| `build_pdf.py` | Markdown → HTML → typeset A4 PDF (cover, contents with page numbers, running heads). |
| `figures/*.svg` | Print-palette figures, consumed by the PDF build. |
| `Kenya-Institute-for-Clinical-AI-Blueprint.pdf` | The built PDF, 44 pages. |

## Rebuilding

```bash
pip install weasyprint cairosvg          # plus pandoc on the system
cd kenya-clinical-ai-institute

python3 figures.py                       # print figures  → ./figures/*.svg
python3 build_pdf.py                     # PDF → here, and copied into ../static/

FIGTHEME=dark python3 figures.py         # web figures → ../static/img/kenya-clinical-ai/fig-01..08.png
```

Both figure sets come from the same source. `figures.py` switches palette on the
`FIGTHEME` environment variable: `light` (default) is the print palette used in the
PDF; `dark` uses the site's own custom properties from `static/css/style.css`
(`--bg #080d16`, `--bg-card #0d1424`, `--cyan`, `--amber`, `--green`, `--red`) so the
figures sit on the page rather than on top of it. The dark run also rasterises to 2x
PNG and cleans up its intermediate SVGs.

`build_pdf.py` writes the PDF twice: once here, once to
`../static/Kenya_Institute_for_Clinical_AI_Blueprint.pdf`, which is the copy the blog
post links to. Rebuild it and the download link is current.

## Notes on the build

A few things in `build_pdf.py` exist to work around specific rendering quirks and
should not be removed casually:

- WeasyPrint ignores `<ol start="n">`, so pandoc's start attributes are rewritten as
  `counter-reset: list-item`. Without this the reference list restarts at 1 in every
  section.
- Pandoc's `<colgroup>` width hints are stripped so tables use automatic layout;
  otherwise column widths follow the markdown source's character widths.
- The four widest diagrams get `class="wide"` and break out of the text measure.
- Part-level headings are detected by text and forced onto a new page; the contents
  list is generated from the same pass, with page numbers resolved by
  `target-counter()`.

## Attribution

The Clinical 4Ds in Part III adapt the AI Fluency Framework by Prof. Rick Dakan
(Ringling College of Art and Design) and Prof. Joseph Feller (Cork University Business
School, University College Cork), elaborated into an open course series with Anthropic
PBC and Ireland's Higher Education Authority.

Two different licences apply, and they are not interchangeable:

- The open **course materials** are CC BY-NC-SA 4.0 — adaptation permitted under
  share-alike terms. Any curriculum derived from them carries that licence forward.
- The authors' **Framework for AI Fluency (Practical Summary Document)**, v1.1, is
  CC BY-NC-ND 4.0 — NoDerivatives. Cite it; do not remix it.

Full reference list — 71 sources with links — is in Part XI of the document.
