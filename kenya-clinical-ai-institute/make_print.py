#!/usr/bin/env python3
"""Build wall-printable versions of a figure.

Any figure in ./figures can be turned into a centred, print-ready sheet:

    python3 make_print.py                      # default: fig5-quality-loop
    python3 make_print.py fig2-clinical-4d     # any stem from ./figures

Output goes to ./print — vector PDFs at A4 and A3 landscape, plus a 300 dpi
PNG fallback for print paths that dislike PDF.

Note on size: these figures are drawn for a page in a document, so on A4 the
smallest labels land around 6.5 pt. A3 puts them near 9 pt, which is what you
want for anything read at standing distance.
"""
import os
import sys

import cairosvg
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
FIGURES = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "print")

SHEETS = [("A4 landscape", 14), ("A3 landscape", 18)]


def build(stem: str) -> None:
    src = os.path.join(FIGURES, f"{stem}.svg")
    if not os.path.exists(src):
        available = sorted(f[:-4] for f in os.listdir(FIGURES) if f.endswith(".svg"))
        sys.exit(f"no such figure: {stem}\navailable: " + ", ".join(available))

    os.makedirs(OUT, exist_ok=True)
    short = stem.split("-", 1)[1] if "-" in stem else stem

    for size, margin in SHEETS:
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        @page {{ size: {size}; margin: {margin}mm; }}
        html, body {{ margin: 0; padding: 0; height: 100%; }}
        .wrap {{ display: flex; align-items: center; justify-content: center; height: 100%; }}
        img {{ max-width: 100%; max-height: 100%; width: auto; height: auto; }}
        </style></head><body><div class="wrap"><img src="file://{src}"></div></body></html>"""
        name = f"{short}-{size.split()[0]}-landscape.pdf"
        HTML(string=html, base_url=OUT).write_pdf(os.path.join(OUT, name))
        print("  ", name)

    name = f"{short}-300dpi.png"
    cairosvg.svg2png(url=src, write_to=os.path.join(OUT, name),
                     scale=4.0, background_color="#FFFFFF")
    print("  ", name)


if __name__ == "__main__":
    stem = sys.argv[1] if len(sys.argv) > 1 else "fig5-quality-loop"
    print(f"building print sheets for {stem}:")
    build(stem)
