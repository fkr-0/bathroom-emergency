#!/usr/bin/env python3
"""Shared release/build metadata for deterministic guide tooling."""
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
VERSION: str = PACKAGE["version"]
RELEASE_DATE = "2026-08-08"
SOURCE_REVIEW_DATE = "2026-08-06"


def git_revision() -> str:
    override = os.environ.get("GUIDE_REVISION")
    if override:
        return override
    result = subprocess.run(
        ["git", "rev-parse", "--short=12", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"


def build_date() -> str:
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(int(epoch), timezone.utc).date().isoformat()
    return datetime.now(timezone.utc).date().isoformat()


LAYOUT_LABELS = {"a4": "A4", "a4half": "A4/2", "largeprint": "LARGE PRINT"}

# The running edition token in the @page margin is deliberately different
# between the colour and monochrome editions of the same book — telling two
# printouts apart is the whole point of it. Everything a reader can act on must
# still match, so parity checks compare text with only this token normalized.
EDITION_TOKEN = re.compile(r"\b(A4/2|A4|LARGE ?PRINT) ?/ ?(?:color|mono)\b")


def content_text(text: str) -> str:
    """Extracted PDF text with per-edition page furniture neutralized."""
    return EDITION_TOKEN.sub(r"\1", text)



# Identity swatch per book pattern, drawn as a gradient in the top margin box.
# Exactly one gradient each: Chromium's printToPDF fails outright when a @page
# margin box carries two background images, so the layered screen patterns are
# reduced to a single stroke here. Angle and spacing carry the difference, which
# keeps them apart in monochrome as well as colour.
PATTERN_SWATCHES = {
    "pulse":      "repeating-linear-gradient(60deg,{c} 0 1.3px,transparent 1.3px 5px)",
    "diamond":    "repeating-linear-gradient(45deg,{c} 0 1.4px,transparent 1.4px 6px)",
    "wave":       "repeating-radial-gradient(ellipse at 50% 130%,transparent 0 2px,{c} 2px 3.2px,transparent 3.2px 6px)",
    "cross":      "repeating-linear-gradient(90deg,{c} 0 1.5px,transparent 1.5px 5px)",
    "shield":     "repeating-linear-gradient(0deg,{c} 0 1.5px,transparent 1.5px 5px)",
    "zigzag":     "repeating-linear-gradient(135deg,{c} 0 1.4px,transparent 1.4px 5px)",
    "crosshatch": "repeating-linear-gradient(45deg,{c} 0 1px,transparent 1px 3px)",
    "dots":       "repeating-radial-gradient(circle at 1.6px 1.6px,{c} 0 .9px,transparent 1.1px 3.2px)",
    "speech":     "repeating-radial-gradient(circle at 40% 60%,transparent 0 1.5px,{c} 1.5px 2.4px,transparent 2.4px 5px)",
    "form-grid":  "repeating-linear-gradient(90deg,{c} 0 1px,transparent 1px 3px)",
    "solid":      "repeating-linear-gradient(0deg,{c} 0 2.2px,transparent 2.2px 5.5px)",
}


def swatch_css(pattern: str, colour: str) -> str:
    """Background gradient for a book's identity swatch."""
    return PATTERN_SWATCHES.get(pattern, PATTERN_SWATCHES["solid"]).format(c=colour)


def _css_string(value: str) -> str:
    """Quote a value for use in a CSS ``content`` declaration."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def revision_footer_css(
    *, title: str, layout: str, mode: str, glyph: str = "", accent: str = "#0d7355",
    pattern: str = "solid", page_name: str | None = None,
) -> str:
    """Return print furniture as ``@page`` margin boxes.

    Chromium honours literal strings and counters inside ``@page`` margin boxes
    but silently drops ``string-set``/``string()``, so the running line has to be
    generated per edition rather than pulled from the document.

    The earlier approach put this line in a fixed-position DOM element. That had
    two defects: Chromium resolved the offset outside the page box and repainted
    the strip inside the content area over headings and table headers, and a
    fixed textual footer interleaves itself into PDF text extraction order. A
    raster background fixed the second problem but not the first. Margin boxes
    are generated content placed in reserved margin space, so they avoid both.

    The element itself stays in the HTML, where it still carries provenance on
    screen; it is simply hidden for print.
    """
    layout_label = LAYOUT_LABELS[layout]
    if mode == "mono":
        accent = "#111111"
    muted = "#111111" if mode == "mono" else "#52645e"

    narrow = layout == "a4half"
    swatch_w, swatch_h = (8, 2.6) if narrow else (12, 3.2)
    heading = f"{glyph}  {title}" if glyph else title
    # The A4/2 page is 105mm wide and gives the running line about 91mm. The
    # full strings wrapped onto a second line there, including the page number.
    # That edition is the primary print target, so it gets compact furniture.
    if layout == "a4half":
        stamp = f"BE {VERSION}"
        trailer = "be.fkr.dev"
    else:
        stamp = f"Bathroom Emergency {VERSION} · {git_revision()[:7]}"
        trailer = f"{build_date()} · be.fkr.dev"
    # Always carry the mode so two printouts of the same book can be told
    # apart. verify_density normalizes this one token before comparing colour
    # and monochrome text, because it is meant to differ.
    edition = f"{layout_label} / {mode}"
    page_selector = f"@page {page_name}" if page_name else "@page"

    return "\n".join(
        (
            "/* Generated running furniture. Literal strings only: Chromium",
            "   drops string() in paged media. */",
            f"{page_selector} {{",
            # The identity band. Chromium honours border and background on a
            # margin box, so the rule and the pattern swatch live in the top
            # margin where they cannot collide with body text -- which is what
            # went wrong when this was a fixed-position element in the flow.
            "  @top-left {",
            f"    content: {_css_string(heading)};",
            f"    color: {accent};",
            "    font-family: sans-serif;",
            f"    font-size: {7 if narrow else 7.5}pt;",
            "    letter-spacing: .06em;",
            "    vertical-align: bottom;",
            f"    padding-left: {swatch_w + 3}mm;",
            "    padding-bottom: 1.2mm;",
            f"    background-image: {swatch_css(pattern, accent)};",
            "    background-repeat: no-repeat;",
            "    background-position: left bottom 1.5mm;",
            f"    background-size: {swatch_w}mm {swatch_h}mm;",
            f"    border-bottom: 1.1pt solid {accent};",
            "  }",
            "  @top-right {",
            f"    content: {_css_string(edition)};",
            f"    color: {muted};",
            "    font-family: sans-serif;",
            "    font-size: 7pt;",
            "    letter-spacing: .08em;",
            "    vertical-align: bottom;",
            "    padding-bottom: 1.2mm;",
            f"    border-bottom: 1.1pt solid {accent};",
            "  }",
            "  @bottom-center {",
            "    content: counter(page) \" / \" counter(pages);",
            f"    color: {muted};",
            "    font-family: sans-serif;",
            "    font-size: 8pt;",
            "  }",
            "  @bottom-left {",
            f"    content: {_css_string(stamp)};",
            f"    color: {muted};",
            "    font-family: sans-serif;",
            "    font-size: 6pt;",
            "  }",
            "  @bottom-right {",
            f"    content: {_css_string(trailer)};",
            f"    color: {muted};",
            "    font-family: sans-serif;",
            "    font-size: 6pt;",
            "  }",
            "}",
            "",
            "@page :first {",
            "  @top-left { content: none; background-image: none; border-bottom: 0; padding: 0; }",
            "  @top-right { border-bottom: 0; }",
            "  @top-right { content: none; }",
            "  @bottom-center { content: none; }",
            "  @bottom-left { content: none; }",
            "  @bottom-right { content: none; }",
            "}",
            "",
            "@media print {",
            "  .revision-footer { display: none !important; }",
            "}",
        )
    )
