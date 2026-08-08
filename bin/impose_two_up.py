#!/usr/bin/env python3
"""Impose the A4/2 editions two-to-a-sheet on A4.

The A4/2 page is 105 x 297 mm, which is exactly half an A4 sheet cut down the
long side. Two of them side by side are an A4 sheet at 1:1 -- no scaling, no
resampling, no "fit to page" softening the type. Print duplex, cut once down
the middle, and the stack is the field guide.

Ordinary reading order is preserved: pages 1 and 2 land on sheet 1, 3 and 4 on
sheet 2. That is the layout you want for a guide that will be cut and stacked,
not for a saddle-stitched booklet, which would need the pages shuffled.

Usage:
    impose_two_up.py [--pattern GLOB] [--outdir DIR]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"

A4_W_PT = 595.276
A4_H_PT = 841.890
TOLERANCE_PT = 6.0


def page_geometry(pdf: Path) -> tuple[float, float, int]:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    size = next(line for line in out.splitlines() if line.startswith("Page size:"))
    pages = next(line for line in out.splitlines() if line.startswith("Pages:"))
    width, height = (float(v) for v in size.split(":")[1].split("pts")[0].split(" x "))
    return width, height, int(pages.split(":")[1])


def impose(pdf: Path, out: Path) -> tuple[int, int]:
    width, height, pages = page_geometry(pdf)
    if abs(width * 2 - A4_W_PT) > TOLERANCE_PT or abs(height - A4_H_PT) > TOLERANCE_PT:
        raise SystemExit(
            f"{pdf.name}: {width:.0f}x{height:.0f}pt is not half an A4 sheet; "
            "this tool only imposes the A4/2 editions"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["pdfjam", "--nup", "2x1", "--paper", "a4paper", "--no-landscape",
         "--scale", "1.0", "--delta", "0 0", "--offset", "0 0",
         "--quiet", "--outfile", str(out), str(pdf)],
        check=True, capture_output=True, text=True,
    )
    _, _, sheets = page_geometry(out)
    return pages, sheets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", default="subguides/*/*_a4half.pdf",
                        help="glob under build/ selecting A4/2 PDFs")
    parser.add_argument("--outdir", default="build/twoup")
    args = parser.parse_args()

    targets = sorted(BUILD.glob(args.pattern))
    if not targets:
        raise SystemExit(f"no A4/2 editions matched {args.pattern}")
    outdir = ROOT / args.outdir
    total = 0
    for pdf in targets:
        out = outdir / f"{pdf.stem}_2up.pdf"
        pages, sheets = impose(pdf, out)
        print(f"  [OK] {out.relative_to(ROOT)}: {pages} pages → {sheets} A4 sheets")
        total += 1
    print(f"\n{total} editions imposed two-up at 1:1 → {outdir.relative_to(ROOT)}")
    print("Print duplex on A4, then cut down the middle of the long side.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
