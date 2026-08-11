#!/usr/bin/env python3
"""Validate one folded A4 booklet per standalone A4/2 subguide.

For every released subguide, both color and mono A4/2 editions must have a
corresponding portrait-A4 booklet artifact. Each guide is one signature padded
only to the next multiple of four logical pages.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
MANIFEST = ROOT / "src" / "data" / "subguides.json"
A4_W_PT = 595.276
A4_H_PT = 841.890
HALF_W_PT = A4_W_PT / 2
TOLERANCE_PT = 6.0
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        errors.append(f"command failed: {' '.join(args)} — {(result.stderr or result.stdout).strip()}")
        return ""
    return result.stdout


def geometry(path: Path) -> tuple[int, float, float]:
    info = run("pdfinfo", str(path))
    page_match = re.search(r"^Pages:\s+(\d+)$", info, re.M)
    size_match = re.search(r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", info, re.M)
    if not page_match or not size_match:
        errors.append(f"cannot parse PDF geometry: {path.relative_to(ROOT)}")
        return 0, 0.0, 0.0
    return int(page_match.group(1)), float(size_match.group(1)), float(size_match.group(2))


def page_text(path: Path, page: int) -> str:
    return run("pdftotext", "-f", str(page), "-l", str(page), "-layout", str(path), "-")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def probe_line(text: str) -> str | None:
    """Pick a long source-page line likely to survive two-up text extraction."""
    candidates: list[str] = []
    for raw in text.splitlines():
        line = normalized(raw)
        if len(line) < 28:
            continue
        if re.search(r"\bA4/2 / (?:color|mono)\b", line):
            continue
        if re.search(r"\b\d+ / \d+\b", line):
            continue
        candidates.append(line)
    return max(candidates, key=len) if candidates else None


def booklet_pairs(padded_pages: int) -> list[tuple[int, int]]:
    """Logical left/right page numbers for one booklet signature."""
    pairs: list[tuple[int, int]] = []
    for sheet in range(padded_pages // 4):
        pairs.append((padded_pages - 2 * sheet, 1 + 2 * sheet))
        pairs.append((2 + 2 * sheet, padded_pages - 2 * sheet - 1))
    return pairs


def verify_blank_half(output: Path, side: int, *, left: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="beg-booklet-blank-") as directory:
        prefix = Path(directory) / "side"
        result = subprocess.run(
            [
                "pdftoppm", "-f", str(side), "-l", str(side), "-singlefile",
                "-png", "-r", "72", str(output), str(prefix),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            errors.append(f"could not rasterize {output.name} side {side}")
            return
        image = Image.open(prefix.with_suffix(".png")).convert("L")
        width, height = image.size
        half = image.crop((0, 0, width // 2, height)) if left else image.crop((width // 2, 0, width, height))
        dark = sum(count for value, count in enumerate(half.histogram()) if value < 245)
        ratio = dark / (half.width * half.height)
        check(ratio < 0.0005, f"{output.name}: padded blank half is not blank (ink ratio {ratio:.5f})")


def expected_pairs() -> list[tuple[str, Path, Path]]:
    if not MANIFEST.exists():
        errors.append("subguide source manifest missing")
        return []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in manifest.get("nodes", [])}
    pairs: list[tuple[str, Path, Path]] = []
    for suffix in ("", "_mono"):
        stem = f"shelf-how-to-use_a4half{suffix}"
        pairs.append(
            (
                "SHELF",
                BUILD / "subguides" / "SHELF" / f"{stem}.pdf",
                BUILD / "booklet" / "subguides" / "SHELF" / f"{stem}_booklet.pdf",
            )
        )
    for node_id in manifest.get("standalone_nodes", []):
        node = by_id.get(node_id)
        if not node:
            errors.append(f"standalone node {node_id} absent from manifest nodes")
            continue
        base = f"{node['slug']}_a4half"
        for suffix in ("", "_mono"):
            stem = f"{base}{suffix}"
            source = BUILD / "subguides" / node_id / f"{stem}.pdf"
            output = BUILD / "booklet" / "subguides" / node_id / f"{stem}_booklet.pdf"
            pairs.append((node_id, source, output))
    return pairs


pairs_to_check = expected_pairs()
check(len(pairs_to_check) == 24, f"expected 24 booklet editions, found {len(pairs_to_check)} targets")

for node_id, source, output in pairs_to_check:
    if not source.exists():
        errors.append(f"source A4/2 PDF missing: {source.relative_to(ROOT)}")
        continue
    if not output.exists():
        errors.append(f"booklet PDF missing: {output.relative_to(ROOT)}")
        continue

    source_pages, source_w, source_h = geometry(source)
    output_sides, output_w, output_h = geometry(output)
    padded = math.ceil(source_pages / 4) * 4
    expected_sides = padded // 2
    expected_sheets = padded // 4

    check(abs(source_w - HALF_W_PT) <= TOLERANCE_PT, f"{source.name}: source width is not A4/2")
    check(abs(source_h - A4_H_PT) <= TOLERANCE_PT, f"{source.name}: source height is not A4")
    check(padded % 4 == 0, f"{source.name}: padded logical page count is not divisible by four")
    check(0 <= padded - source_pages <= 3, f"{source.name}: booklet padding is not minimal")
    check(output_sides == expected_sides, f"{output.name}: expected {expected_sides} sides, got {output_sides}")
    check(
        abs(output_w - A4_W_PT) <= TOLERANCE_PT and abs(output_h - A4_H_PT) <= TOLERANCE_PT,
        f"{output.name}: physical page is not portrait A4",
    )

    logical_pairs = booklet_pairs(padded)
    check(len(logical_pairs) == output_sides, f"{output.name}: imposition pair count mismatch")

    # Exercise outer cover, first inside, middle spread, and final side. This
    # detects reversal/order mistakes without repeatedly extracting every page.
    representatives = sorted({1, 2, max(1, output_sides // 2), output_sides})
    for side in representatives:
        side_text = normalized(page_text(output, side))
        left, right = logical_pairs[side - 1]
        for logical in (left, right):
            if logical > source_pages:
                continue
            probe = probe_line(page_text(source, logical))
            if probe:
                check(probe in side_text, f"{output.name}: side {side} does not contain logical page {logical}")

    padding_pages = list(range(source_pages + 1, padded + 1))
    for logical in padding_pages:
        locations = [
            (index + 1, pair.index(logical) == 0)
            for index, pair in enumerate(logical_pairs)
            if logical in pair
        ]
        check(len(locations) == 1, f"{output.name}: padded page {logical} appears {len(locations)} times")
        if locations:
            side, is_left = locations[0]
            verify_blank_half(output, side, left=is_left)

    print(
        f"Booklet verified [{node_id}]: {output.relative_to(ROOT)} — "
        f"{source_pages} -> {padded} logical pages, {expected_sheets} A4 sheets / {output_sides} sides"
    )

# The two convenience print runs must be exact concatenations of the already
# imposed booklets. An even physical-side count per component is the key duplex
# invariant: it guarantees that no A4 sheet can contain two different books.
manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
by_id = {item["id"]: item for item in manifest.get("nodes", [])}
bundle_nodes = [
    {"id": "SHELF", "slug": "shelf-how-to-use", "title": "Shelf Intro — How to Use the Eleven Books"}
]
bundle_nodes.extend(
    by_id[node_id]
    for node_id in manifest.get("shelf_order", [])
    if node_id in manifest.get("standalone_nodes", []) and node_id in by_id
)
check(len(bundle_nodes) == 12, f"expected Shelf intro plus eleven bundle components, found {len(bundle_nodes)}")
for mode in ("color", "mono"):
    mode_suffix = "_mono" if mode == "mono" else ""
    bundle = BUILD / "booklet" / f"all-subguides_booklet-print{mode_suffix}.pdf"
    if not bundle.exists():
        errors.append(f"combined {mode} booklet print run missing: {bundle.relative_to(ROOT)}")
        continue

    bundle_sides, bundle_w, bundle_h = geometry(bundle)
    check(
        abs(bundle_w - A4_W_PT) <= TOLERANCE_PT and abs(bundle_h - A4_H_PT) <= TOLERANCE_PT,
        f"{bundle.name}: physical page is not portrait A4",
    )

    expected_total = 0
    cursor = 1
    for node in bundle_nodes:
        node_id = node["id"]
        component = (
            BUILD
            / "booklet"
            / "subguides"
            / node_id
            / f"{node['slug']}_a4half{mode_suffix}_booklet.pdf"
        )
        if not component.exists():
            errors.append(f"combined {mode}: component missing: {component.relative_to(ROOT)}")
            continue
        component_sides, _component_w, _component_h = geometry(component)
        check(component_sides % 2 == 0, f"{component.name}: physical side count is not duplex-safe")
        check(cursor % 2 == 1, f"{bundle.name}: {node_id} begins on an even PDF side")

        component_first = probe_line(page_text(component, 1))
        bundle_first = normalized(page_text(bundle, cursor))
        if component_first:
            check(
                component_first in bundle_first,
                f"{bundle.name}: {node_id} does not begin at expected side {cursor}",
            )
        expected_total += component_sides
        cursor += component_sides

    check(bundle_sides == expected_total, f"{bundle.name}: expected {expected_total} sides, got {bundle_sides}")
    print(
        f"Combined booklet verified [{mode}]: {bundle.relative_to(ROOT)} — "
        f"{bundle_sides} sides / {bundle_sides // 2} A4 sheets, twelve duplex-safe booklet boundaries"
    )

printing = BUILD / "booklet" / "PRINTING.md"
if printing.exists():
    printing_text = printing.read_text(encoding="utf-8")
    check("flip on long edge" in printing_text.lower(), "generated booklet instructions omit long-edge duplex setting")
    check("all-subguides_booklet-print.pdf" in printing_text, "generated booklet instructions omit color bundle")
    check("all-subguides_booklet-print_mono.pdf" in printing_text, "generated booklet instructions omit mono bundle")
else:
    errors.append("generated build/booklet/PRINTING.md is missing")

if errors:
    raise SystemExit("Booklet validation failed:\n- " + "\n- ".join(errors))

print("Folded booklet validation passed: 24 editions (Shelf intro + eleven books, color and mono) plus two twelve-signature print bundles, with minimal padding, A4 geometry, order, duplex-safe boundaries, blank padding, and print instructions verified.")
