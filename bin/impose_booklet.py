#!/usr/bin/env python3
"""Impose every standalone A4/2 subguide as its own folded A4 booklet.

Each source page is 105 x 297 mm. Two logical pages therefore fit side by side
on one portrait A4 side at 1:1. Each physical A4 sheet carries four logical
pages across front/back and is folded on the vertical centre line.

Every subguide is a separate booklet/signature. Its logical page count is
padded only to the next multiple of four, so short books do not acquire the
extra blanks that a fixed 24-page signature would introduce.

By default both color and monochrome A4/2 editions of the Shelf introduction
and every released standalone subguide are imposed under
build/booklet/subguides/<node>/.

Print the output duplex on portrait A4 with LONG-EDGE flipping, fold on the
vertical centre, then staple/bind each guide separately.

Usage:
    impose_booklet.py [--outdir build/booklet/subguides]
    impose_booklet.py path/to/one_a4half.pdf [more PDFs ...]
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
SUBGUIDE_MANIFEST = ROOT / "src" / "data" / "subguides.json"

A4_W_PT = 595.276
A4_H_PT = 841.890
TOLERANCE_PT = 6.0


class BookletError(RuntimeError):
    pass


def require(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise BookletError(f"required command not found: {binary}")
    return path


def page_geometry(pdf: Path) -> tuple[float, float, int]:
    result = subprocess.run(
        [require("pdfinfo"), str(pdf)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise BookletError((result.stderr or result.stdout).strip())
    size_line = next((line for line in result.stdout.splitlines() if line.startswith("Page size:")), None)
    pages_line = next((line for line in result.stdout.splitlines() if line.startswith("Pages:")), None)
    if not size_line or not pages_line:
        raise BookletError(f"could not read PDF geometry: {pdf}")
    width, height = (
        float(value)
        for value in size_line.split(":", 1)[1].split("pts", 1)[0].split(" x ")
    )
    return width, height, int(pages_line.split(":", 1)[1])


def default_inputs() -> list[tuple[str, Path]]:
    if not SUBGUIDE_MANIFEST.exists():
        raise BookletError(f"subguide manifest missing: {SUBGUIDE_MANIFEST}")
    manifest = json.loads(SUBGUIDE_MANIFEST.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in manifest.get("nodes", [])}
    inputs: list[tuple[str, Path]] = [
        ("SHELF", BUILD / "subguides" / "SHELF" / "shelf-how-to-use_a4half.pdf"),
        ("SHELF", BUILD / "subguides" / "SHELF" / "shelf-how-to-use_a4half_mono.pdf"),
    ]
    for node_id in manifest.get("standalone_nodes", []):
        node = by_id.get(node_id)
        if not node:
            raise BookletError(f"standalone node {node_id!r} is absent from subguide manifest")
        stem = f"{node['slug']}_a4half"
        inputs.append((node_id, BUILD / "subguides" / node_id / f"{stem}.pdf"))
        inputs.append((node_id, BUILD / "subguides" / node_id / f"{stem}_mono.pdf"))
    return inputs


def infer_node(pdf: Path) -> str:
    parent = pdf.parent.name
    return parent if parent else "manual"


def booklet_pairs(padded_pages: int) -> list[tuple[int, int]]:
    """Return logical left/right page numbers for one folded signature."""
    pairs: list[tuple[int, int]] = []
    for sheet in range(padded_pages // 4):
        pairs.append((padded_pages - 2 * sheet, 1 + 2 * sheet))
        pairs.append((2 + 2 * sheet, padded_pages - 2 * sheet - 1))
    return pairs


def make_blank_half_page(path: Path) -> None:
    """Create one truly blank A4/2 page for signature padding."""
    html = path.with_suffix(".html")
    html.write_text(
        "<!doctype html><style>@page { size: 105mm 297mm; margin: 0 } "
        "html, body { margin: 0; padding: 0 }</style>",
        encoding="utf-8",
    )
    result = subprocess.run(
        [require("weasyprint"), str(html), str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise BookletError((result.stderr or result.stdout).strip())
    width, height, pages = page_geometry(path)
    if pages != 1 or abs(width * 2 - A4_W_PT) > TOLERANCE_PT or abs(height - A4_H_PT) > TOLERANCE_PT:
        raise BookletError(
            f"generated blank page has wrong geometry: {width:.2f}x{height:.2f}pt, {pages} pages"
        )


def impose(pdf: Path, out: Path) -> dict[str, int]:
    width, height, source_pages = page_geometry(pdf)
    if abs(width * 2 - A4_W_PT) > TOLERANCE_PT or abs(height - A4_H_PT) > TOLERANCE_PT:
        raise BookletError(
            f"{pdf.name}: {width:.2f}x{height:.2f}pt is not the 105x297mm A4/2 layout"
        )

    # One booklet = one signature. Booklet imposition only needs a multiple of
    # four logical pages, so pad minimally rather than to a fixed signature size.
    padded_pages = math.ceil(source_pages / 4) * 4
    physical_sides = padded_pages // 2
    physical_sheets = padded_pages // 4

    out.parent.mkdir(parents=True, exist_ok=True)

    # Do not use pdfjam's --signature implementation here. pdfjam 3.10 (the
    # Ubuntu 24.04 package) and 4.2 disagree about how --signature composes with
    # --nup 2x1: 3.10 can split one logical A4/2 page across both physical
    # halves, which destroys the padded blank and the folding order. Compute the
    # signature order ourselves, then ask pdfjam only to place already-ordered
    # half-pages side by side. Plain --nup 2x1 is stable across both versions.
    with tempfile.TemporaryDirectory(prefix="beg-booklet-impose-") as directory:
        tmp = Path(directory)
        page_pattern = tmp / "page-%d.pdf"
        result = subprocess.run(
            [require("pdfseparate"), str(pdf), str(page_pattern)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise BookletError((result.stderr or result.stdout).strip())

        blank: Path | None = None
        if padded_pages > source_pages:
            blank = tmp / "blank.pdf"
            make_blank_half_page(blank)

        ordered_pages: list[Path] = []
        for left, right in booklet_pairs(padded_pages):
            for logical in (left, right):
                if logical <= source_pages:
                    ordered_pages.append(tmp / f"page-{logical}.pdf")
                elif blank is not None:
                    ordered_pages.append(blank)
                else:
                    raise BookletError(f"missing padding page {logical} for {pdf.name}")

        ordered = tmp / "ordered.pdf"
        result = subprocess.run(
            [require("pdfunite"), *(str(page) for page in ordered_pages), str(ordered)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise BookletError((result.stderr or result.stdout).strip())

        result = subprocess.run(
            [
                require("pdfjam"),
                "--nup", "2x1",
                "--paper", "a4paper",
                "--no-landscape",
                "--scale", "1.0",
                "--delta", "0 0",
                "--offset", "0 0",
                "--quiet",
                "--outfile", str(out),
                str(ordered),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise BookletError((result.stderr or result.stdout).strip())

    out_width, out_height, out_pages = page_geometry(out)
    if abs(out_width - A4_W_PT) > TOLERANCE_PT or abs(out_height - A4_H_PT) > TOLERANCE_PT:
        raise BookletError(
            f"{out.name}: imposed output is not portrait A4: {out_width:.2f}x{out_height:.2f}pt"
        )
    if out_pages != physical_sides:
        raise BookletError(
            f"{out.name}: expected {physical_sides} printable sides, got {out_pages}"
        )

    return {
        "source_pages": source_pages,
        "padded_pages": padded_pages,
        "physical_sheets": physical_sheets,
        "physical_sides": physical_sides,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="build/booklet/subguides")
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="optional A4/2 PDFs; defaults to color+mono editions of all standalone subguides",
    )
    args = parser.parse_args()

    outdir = ROOT / args.outdir
    if args.inputs:
        inputs = [
            (infer_node(path), path if path.is_absolute() else ROOT / path)
            for path in args.inputs
        ]
    else:
        inputs = default_inputs()

    missing = [path for _, path in inputs if not path.exists()]
    if missing:
        raise BookletError("missing input PDF(s): " + ", ".join(str(path) for path in missing))

    for node_id, pdf in inputs:
        out = outdir / node_id / f"{pdf.stem}_booklet.pdf"
        stats = impose(pdf, out)
        blank_pages = stats["padded_pages"] - stats["source_pages"]
        print(
            f"  [OK] {out.relative_to(ROOT)}: "
            f"{stats['source_pages']} logical pages + {blank_pages} blank -> "
            f"{stats['padded_pages']} pages = {stats['physical_sheets']} A4 sheets / "
            f"{stats['physical_sides']} printable sides"
        )

    print(f"\nBuilt {len(inputs)} booklet editions: Shelf intro + eleven standalone books, color and mono.")
    print("Booklet imposition: 2 x A4/2 pages per A4 side at 1:1; one signature per guide.")
    print("Print duplex, portrait A4, flip on LONG edge; fold each guide on the vertical centre.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BookletError as exc:
        print(f"BOOKLET IMPOSITION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
