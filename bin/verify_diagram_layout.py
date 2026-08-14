"""Independently verify reader-facing diagram layout and audit coverage."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "src" / "diagrams"
CATALOG = ROOT / "src" / "data" / "illustration_catalog.json"
QA = ROOT / "build" / "qa" / "diagram-layout"
sys.path.insert(0, str(DIAGRAMS))
from textfit import TextOverflow, audit_figure

TEXT_GENERATORS = (
    "generate_flowgraph.py",
    "generate_routes.py",
    "generate_continuity.py",
    "generate_observation.py",
    "generate_responsibility.py",
    "generate_accessibility.py",
    "generate_scientific.py",
    "generate_first_aid.py",
    "generate_professional_support.py",
    "generate_subguides.py",
)


def fail(message: str) -> None:
    raise SystemExit(f"Diagram-layout verification failed: {message}")


def verify_collision_detector() -> None:
    """The gate must reject text-on-text overlap, not merely box overflow."""
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(.5, .5, "WARN", ha="center", va="center", fontsize=18, fontweight="bold")
    ax.text(.5, .5, "Read the current warning", ha="center", va="center", fontsize=12)
    try:
        audit_figure(fig, "synthetic-overlap-regression")
    except TextOverflow as exc:
        if "text collision" not in str(exc):
            fail(f"synthetic collision failed for the wrong reason: {exc}")
    else:
        fail("synthetic WARN/title collision was not rejected")
    finally:
        plt.close(fig)


def verify_generator_contract() -> None:
    for name in TEXT_GENERATORS:
        path = DIAGRAMS / name
        if not path.exists():
            fail(f"missing text-bearing generator: {name}")
        source = path.read_text(encoding="utf-8")
        for marker in ("fit_labels", "audit_figure"):
            if marker not in source:
                fail(f"{name} bypasses {marker}")


def rerender_strictly() -> None:
    environment = os.environ.copy()
    environment.pop("DIAGRAM_TEXT_AUDIT", None)
    with tempfile.TemporaryDirectory(prefix="beg-diagram-layout-") as directory:
        output = Path(directory)
        for name in TEXT_GENERATORS:
            result = subprocess.run(
                [sys.executable, str(DIAGRAMS / name), str(output)],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
            )
            if result.returncode:
                detail = (result.stderr or result.stdout).strip()
                fail(f"strict rerender failed in {name}:\n{detail}")
        # Concrete regression target from the Orange Book report.
        orange = output / "hazard_source_location_map.png"
        if not orange.exists() or orange.stat().st_size < 10_000:
            fail("Orange hazard source-location map was not independently rendered")


def contact_sheets() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    current = [
        item for item in catalog.get("illustrations", [])
        if item.get("reader_facing", True)
    ]
    missing = [item["file"] for item in current if not (ROOT / item["file"]).exists()]
    if missing:
        fail(f"reader-facing illustration files are missing: {missing}")

    QA.mkdir(parents=True, exist_ok=True)
    for old in QA.glob("contact-sheet-*.png"):
        old.unlink()
    columns, rows = 3, 3
    cell_w, cell_h = 520, 390
    per_sheet = columns * rows
    sheets = 0
    for page_start in range(0, len(current), per_sheet):
        page = current[page_start:page_start + per_sheet]
        sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "white")
        draw = ImageDraw.Draw(sheet)
        for index, item in enumerate(page):
            row, col = divmod(index, columns)
            left, top = col * cell_w, row * cell_h
            source = Image.open(ROOT / item["file"]).convert("RGB")
            image = ImageOps.contain(source, (cell_w - 30, cell_h - 72))
            x = left + (cell_w - image.width) // 2
            y = top + 12
            sheet.paste(image, (x, y))
            label = f"{item['id']} · {Path(item['file']).name}"
            draw.text((left + 15, top + cell_h - 44), label, fill="black")
            draw.rectangle((left, top, left + cell_w - 1, top + cell_h - 1), outline="black", width=1)
        sheets += 1
        sheet.save(QA / f"contact-sheet-{sheets}.png", optimize=True)
    return sheets


verify_collision_detector()
verify_generator_contract()
rerender_strictly()
sheet_count = contact_sheets()
print(
    "Diagram-layout verification passed: collision regression, strict audit coverage for "
    f"{len(TEXT_GENERATORS)} text-bearing generator families, independent Orange rerender, "
    f"and {sheet_count} reader-illustration contact sheets."
)
