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
RELEASE_DATE = "2026-08-06"
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


def _css_string(value: str) -> str:
    """Quote a value for use in a CSS ``content`` declaration."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def revision_footer_css(
    *, title: str, layout: str, mode: str, glyph: str = "", accent: str = "#0d7355"
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

    heading = f"{glyph}  {title}" if glyph else title
    stamp = f"Bathroom Emergency {VERSION} · {git_revision()}"
    trailer = f"{build_date()} · be.fkr.dev"
    # Always carry the mode so two printouts of the same book can be told
    # apart. verify_density normalizes this one token before comparing colour
    # and monochrome text, because it is meant to differ.
    edition = f"{layout_label} / {mode}"

    return "\n".join(
        (
            "/* Generated running furniture. Literal strings only: Chromium",
            "   drops string() in paged media. */",
            "@page {",
            "  @top-left {",
            f"    content: {_css_string(heading)};",
            f"    color: {accent};",
            "    font-family: sans-serif;",
            "    font-size: 7.5pt;",
            "    letter-spacing: .06em;",
            "  }",
            "  @top-right {",
            f"    content: {_css_string(edition)};",
            f"    color: {muted};",
            "    font-family: sans-serif;",
            "    font-size: 7pt;",
            "    letter-spacing: .08em;",
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
            "  @top-left { content: none; }",
            "  @top-right { content: none; }",
            "  @bottom-left { content: none; }",
            "  @bottom-right { content: none; }",
            "}",
            "",
            "@media print {",
            "  .revision-footer { display: none !important; }",
            "}",
        )
    )
