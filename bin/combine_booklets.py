#!/usr/bin/env python3
"""Concatenate the intro and eleven already-imposed booklets for one print run.

The inputs are the portrait-A4 booklet PDFs produced by impose_booklet.py.
Each component has an even number of physical PDF pages (front/back sides), so
concatenating components cannot pair the end of one booklet with the beginning
of the next when the bundle is printed duplex.

Two bundles are built by default:

  build/booklet/all-subguides_booklet-print.pdf
  build/booklet/all-subguides_booklet-print_mono.pdf

A build-specific build/booklet/PRINTING.md is emitted alongside them with the
exact booklet boundaries and sheet counts.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from project_meta import VERSION

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
BOOKLET_DIR = BUILD / "booklet"
SUBGUIDE_MANIFEST = ROOT / "src" / "data" / "subguides.json"
PRINTING_GUIDE = ROOT / "PRINTING.md"

A4_W_PT = 595.276
A4_H_PT = 841.890
TOLERANCE_PT = 6.0


class BundleError(RuntimeError):
    pass


def require(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise BundleError(f"required command not found: {binary}")
    return path


def page_geometry(pdf: Path) -> tuple[float, float, int]:
    result = subprocess.run(
        [require("pdfinfo"), str(pdf)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise BundleError((result.stderr or result.stdout).strip())
    size_line = next((line for line in result.stdout.splitlines() if line.startswith("Page size:")), None)
    pages_line = next((line for line in result.stdout.splitlines() if line.startswith("Pages:")), None)
    if not size_line or not pages_line:
        raise BundleError(f"could not read PDF geometry: {pdf}")
    width, height = (
        float(value)
        for value in size_line.split(":", 1)[1].split("pts", 1)[0].split(" x ")
    )
    return width, height, int(pages_line.split(":", 1)[1])


def load_manifest() -> tuple[dict, list[dict]]:
    if not SUBGUIDE_MANIFEST.exists():
        raise BundleError(f"subguide manifest missing: {SUBGUIDE_MANIFEST}")
    manifest = json.loads(SUBGUIDE_MANIFEST.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in manifest.get("nodes", [])}
    ordered: list[dict] = [
        {
            "id": "SHELF",
            "slug": "shelf-how-to-use",
            "title": "Shelf Intro — How to Use the Eleven Books",
        }
    ]
    for node_id in manifest.get("shelf_order", []):
        if node_id not in manifest.get("standalone_nodes", []):
            continue
        node = by_id.get(node_id)
        if not node:
            raise BundleError(f"shelf node {node_id!r} is absent from manifest nodes")
        ordered.append(node)
    if len(ordered) != 12:
        raise BundleError(f"expected Shelf intro plus eleven books, found {len(ordered)} components")
    return manifest, ordered


def component_path(node: dict, mode: str) -> Path:
    suffix = "_mono" if mode == "mono" else ""
    stem = f"{node['slug']}_a4half{suffix}_booklet.pdf"
    return BOOKLET_DIR / "subguides" / node["id"] / stem


def inspect_components(nodes: list[dict], mode: str) -> list[dict]:
    components: list[dict] = []
    next_side = 1
    next_sheet = 1
    for node in nodes:
        path = component_path(node, mode)
        if not path.exists():
            raise BundleError(f"missing imposed booklet: {path.relative_to(ROOT)}")
        width, height, sides = page_geometry(path)
        if abs(width - A4_W_PT) > TOLERANCE_PT or abs(height - A4_H_PT) > TOLERANCE_PT:
            raise BundleError(
                f"{path.name}: booklet component is not portrait A4: {width:.2f}x{height:.2f}pt"
            )
        if sides % 2:
            raise BundleError(
                f"{path.name}: booklet component has {sides} physical sides; duplex-safe components must be even"
            )
        sheets = sides // 2
        components.append(
            {
                "node": node["id"],
                "title": node["title"],
                "path": path,
                "sides": sides,
                "sheets": sheets,
                "first_side": next_side,
                "last_side": next_side + sides - 1,
                "first_sheet": next_sheet,
                "last_sheet": next_sheet + sheets - 1,
            }
        )
        next_side += sides
        next_sheet += sheets
    return components


def combine(components: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [require("pdfunite"), *[str(item["path"]) for item in components], str(output)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise BundleError((result.stderr or result.stdout).strip())

    width, height, sides = page_geometry(output)
    expected_sides = sum(item["sides"] for item in components)
    if abs(width - A4_W_PT) > TOLERANCE_PT or abs(height - A4_H_PT) > TOLERANCE_PT:
        raise BundleError(
            f"{output.name}: combined output is not portrait A4: {width:.2f}x{height:.2f}pt"
        )
    if sides != expected_sides:
        raise BundleError(f"{output.name}: expected {expected_sides} sides, got {sides}")


def write_printing_plan(results: dict[str, dict]) -> Path:
    if not PRINTING_GUIDE.exists():
        raise BundleError(f"printing guide missing: {PRINTING_GUIDE}")
    lines = [PRINTING_GUIDE.read_text(encoding="utf-8").rstrip(), "", "## Build-specific sheet plan", ""]
    lines.append(f"Release: `{VERSION}`")
    lines.append("")
    for mode in ("color", "mono"):
        result = results[mode]
        lines.extend(
            [
                f"### {mode.capitalize()} bundle",
                "",
                f"File: `{result['output'].relative_to(ROOT)}`",
                "",
                "| Book | Bundle PDF sides | Physical A4 sheets |",
                "|---|---:|---:|",
            ]
        )
        for item in result["components"]:
            lines.append(
                f"| {item['node']} — {item['title']} | "
                f"{item['first_side']}–{item['last_side']} | "
                f"{item['first_sheet']}–{item['last_sheet']} ({item['sheets']}) |"
            )
        lines.extend(
            [
                "",
                f"Total: **{result['sides']} printed sides / {result['sheets']} A4 sheets**.",
                "",
            ]
        )

    target = BOOKLET_DIR / "PRINTING.md"
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("color", "mono", "all"),
        default="all",
        help="bundle color, mono, or both (default: both)",
    )
    args = parser.parse_args()

    _manifest, nodes = load_manifest()
    modes = ("color", "mono") if args.mode == "all" else (args.mode,)
    results: dict[str, dict] = {}

    for mode in modes:
        components = inspect_components(nodes, mode)
        suffix = "_mono" if mode == "mono" else ""
        output = BOOKLET_DIR / f"all-subguides_booklet-print{suffix}.pdf"
        combine(components, output)
        sides = sum(item["sides"] for item in components)
        sheets = sum(item["sheets"] for item in components)
        results[mode] = {
            "output": output,
            "components": components,
            "sides": sides,
            "sheets": sheets,
        }
        print(
            f"  [OK] {output.relative_to(ROOT)}: {len(components)} booklet signatures, "
            f"{sides} printable sides / {sheets} A4 sheets"
        )

    # A normal build always creates both modes. For a selected one-mode run,
    # emit a plan only when the other existing bundle can also be inspected.
    if len(results) == 1:
        other = "mono" if "color" in results else "color"
        suffix = "_mono" if other == "mono" else ""
        other_output = BOOKLET_DIR / f"all-subguides_booklet-print{suffix}.pdf"
        if other_output.exists():
            components = inspect_components(nodes, other)
            results[other] = {
                "output": other_output,
                "components": components,
                "sides": sum(item["sides"] for item in components),
                "sheets": sum(item["sheets"] for item in components),
            }

    if set(results) == {"color", "mono"}:
        plan = write_printing_plan(results)
        print(f"  [OK] {plan.relative_to(ROOT)}: exact booklet boundaries and print settings")
    else:
        print("  [WARN] build-specific PRINTING.md not regenerated because only one bundle is available")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BundleError as exc:
        print(f"BOOKLET BUNDLE FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
