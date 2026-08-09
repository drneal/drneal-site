#!/usr/bin/env python3
"""Correct the 'The Evidence' box on slide 9 of Clinical_AI_Foundations_Blueprint.pdf.

The original box states that clinicians deferred to erroneous AI output
*because* they consulted the AI before deciding — a causal mechanism the 2025
trial did not establish. It showed deference despite prior AI-literacy training.
The independent-impression rule is a design response to anchoring, not a finding
of the trial.

Method: the deck's pages are single full-bleed raster images with no text layer,
so the box is repainted on the page bitmap and that one page is swapped. Pages
1-8 and 10-13 are copied through untouched by pypdf, so the file structure and
every other page are preserved exactly.
"""
import glob
import os
import subprocess
import tempfile

import img2pdf
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PDF = os.path.join(SITE, "static", "Clinical_AI_Foundations_Blueprint.pdf")
PAGE = 9                                   # 1-based

# measured from the page bitmap, not estimated.
# y1 extends the original 223 down to 278: the corrected wording is longer than
# the original, and a scan of the page confirms the next occupied row below the
# box is y=296, so this uses free space without touching anything else.
BOX = dict(x0=1037, x1=1344, y0=31, y1=278, hdr_end=74)
BORDER = (7, 7, 4)
WHITE = (255, 255, 255)

NEW_TEXT = ("In 2025 trials, clinicians deferred to erroneous AI output "
            "even after 20 hours of AI-literacy training. Writing your "
            "impression first is designed to block that anchoring.")

FONT = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    tmp = tempfile.mkdtemp()

    # 1. render the target page at its native pixel grid (1376x768 = 72 dpi)
    subprocess.run(["pdftoppm", "-png", "-r", "72", "-f", str(PAGE), "-l", str(PAGE),
                    PDF, os.path.join(tmp, "pg")], check=True)
    src = glob.glob(os.path.join(tmp, "pg-*.png"))[0]
    img = Image.open(src).convert("RGB")
    assert img.size == (1376, 768), f"unexpected page raster {img.size}"

    d = ImageDraw.Draw(img)
    b = BOX

    # 2. clear the body of the box, leaving header and border intact
    d.rectangle([b["x0"] + 3, b["hdr_end"], b["x1"] - 3, b["y1"] - 3], fill=WHITE)

    # 3. fit the corrected wording to the existing box
    pad_x, pad_top = 14, 10
    max_w = (b["x1"] - b["x0"]) - 2 * pad_x - 6
    max_h = (b["y1"] - b["hdr_end"]) - pad_top - 8
    for size in range(26, 14, -1):
        font = ImageFont.truetype(FONT, size)
        lines = wrap(d, NEW_TEXT, font, max_w)
        pitch = round(size * 1.22)
        if len(lines) * pitch <= max_h:
            break
    else:
        raise SystemExit("could not fit the text in the box")

    y = b["hdr_end"] + pad_top
    for ln in lines:
        d.text((b["x0"] + pad_x + 3, y), ln, font=font, fill=(17, 17, 17))
        y += pitch

    # redraw the border so the repaint cannot have eaten it
    d.rectangle([b["x0"], b["y0"], b["x1"], b["y1"]], outline=BORDER, width=3)

    patched_png = os.path.join(tmp, "page9_patched.png")
    img.save(patched_png)
    print(f"  text set at {size}px in {len(lines)} lines")

    # 4. that one page as a PDF at exactly the original page size
    page_pdf = os.path.join(tmp, "page9.pdf")
    layout = img2pdf.get_layout_fun((img2pdf.px_to_pt(1376, 72),
                                     img2pdf.px_to_pt(768, 72)))
    with open(page_pdf, "wb") as f:
        f.write(img2pdf.convert(patched_png, layout_fun=layout))

    # 5. rebuild: originals copied through, only page 9 replaced
    reader, new = PdfReader(PDF), PdfReader(page_pdf)
    w = PdfWriter()
    for i, p in enumerate(reader.pages, start=1):
        w.add_page(new.pages[0] if i == PAGE else p)
    if reader.metadata:
        w.add_metadata({k: v for k, v in reader.metadata.items() if isinstance(v, str)})

    out = PDF + ".new"
    with open(out, "wb") as f:
        w.write(f)
    os.replace(out, PDF)
    print(f"  wrote {PDF}")


if __name__ == "__main__":
    main()
