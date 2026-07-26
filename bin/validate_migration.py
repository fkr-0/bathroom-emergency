#!/usr/bin/env python3
"""Validate v4.5 ownership, source registry, hub, and B/H standalone editions."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data"
BUILD = ROOT / "build" / "subguides"
VERSION = "4.5.0"
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def run_check(script: str) -> None:
    result = subprocess.run(
        ["python3", str(ROOT / "bin" / script), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    check(
        result.returncode == 0,
        (result.stderr or result.stdout).strip() or f"{script} --check failed",
    )


class MainText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_main = False
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "main":
            self.in_main = True
        if self.in_main and tag in {"script", "style", "nav"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if self.in_main and tag in {"script", "style", "nav"} and self.skip:
            self.skip -= 1
        if tag == "main":
            self.in_main = False

    def handle_data(self, data: str) -> None:
        if self.in_main and not self.skip:
            self.parts.append(data)


def semantic_text(path: Path) -> str:
    parser = MainText()
    parser.feed(path.read_text(encoding="utf-8"))
    text = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
    return re.sub(
        r"standalone (?:a4half|largeprint|a4)",
        "standalone layout",
        text,
        flags=re.IGNORECASE,
    )


def pdf_info(path: Path) -> dict[str, str]:
    result = subprocess.run(
        ["pdfinfo", str(path)], cwd=ROOT, text=True, capture_output=True
    )
    if result.returncode:
        return {}
    info = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()
    return info


run_check("build_inventories.py")
run_check("build_source_inventory.py")

section_path = DATA / "section_ownership.json"
figure_path = DATA / "figure_inventory.json"
source_path = DATA / "source_inventory.json"
for path in (section_path, figure_path, source_path):
    check(path.exists(), f"missing {path.relative_to(ROOT)}")

if section_path.exists():
    sections = json.loads(section_path.read_text(encoding="utf-8"))
    records = sections.get("sections", [])
    keys = [item.get("key") for item in records]
    check(sections.get("release") == VERSION, "section inventory version drifted")
    check(len(records) >= 180, f"section inventory unexpectedly small: {len(records)}")
    check(len(keys) == len(set(keys)), "duplicate section inventory keys")
    check(
        all(
            item.get("owner") in {"O", "A", "B", "C", "D", "H", "Z", "P", "R"}
            for item in records
        ),
        "unknown section owner",
    )

if figure_path.exists():
    figures = json.loads(figure_path.read_text(encoding="utf-8"))
    records = figures.get("figures", [])
    ids = [item.get("id") for item in records]
    check(figures.get("release") == VERSION, "figure inventory version drifted")
    check(len(records) >= 26, f"figure inventory unexpectedly small: {len(records)}")
    check(len(ids) == len(set(ids)), "duplicate figure inventory IDs")
    h_reader = [
        item
        for item in records
        if item.get("owner") == "H" and item.get("reader_facing", True)
    ]
    check(
        len(h_reader) >= 4,
        f"H pilot needs four useful canonical visuals, found {len(h_reader)}",
    )
    for item in records:
        check(
            item.get("owner") in {"O", "A", "B", "C", "D", "H", "Z", "P", "R"},
            f"{item.get('id')}: missing exact owner",
        )
        check(bool(item.get("question")), f"{item.get('id')}: missing question")
        check(bool(item.get("source_basis")), f"{item.get('id')}: missing source basis")
        if item.get("reader_facing", True):
            check(
                (ROOT / item.get("file", "missing")).exists(),
                f"{item.get('id')}: output missing",
            )

if source_path.exists():
    sources = json.loads(source_path.read_text(encoding="utf-8"))
    records = sources.get("footnote_sources", [])
    ids = [item.get("id") for item in records]
    check(sources.get("release") == VERSION, "source registry version drifted")
    check(
        sources.get("status") == "canonical-source-registry",
        "canonical source-registry status missing",
    )
    check(not sources.get("unresolved_references"), "unresolved chapter citations remain")
    check(len(records) >= 50, f"source registry unexpectedly small: {len(records)}")
    check(len(ids) == len(set(ids)), "duplicate source IDs")
    check(any("B" in item.get("subguides", []) for item in records), "B has no sources")
    check(any("H" in item.get("subguides", []) for item in records), "H has no sources")

layout_geometry = {
    "a4": ("594", "841"),
    # Chromium reports the standards-defined 105 mm width as 298.08 pt.
    "a4half": ("298", "841"),
    "largeprint": ("594", "841"),
}
for node, slug, min_sources, min_visuals, required, forbidden in (
    (
        "B",
        "alarm-calm",
        6,
        4,
        ("B — I feel anxious", "E — Overload", "Calm Guide", "Sources and limits"),
        ("C — Pain", "D — Threat", "F — Smell"),
    ),
    (
        "H",
        "air-smell-environment",
        8,
        4,
        (
            "F — Smell",
            "Situation H — The Environment May Be Unsafe",
            "Source-location decision map",
            "Five-field hazard handoff card",
            "Sources and limits",
        ),
        ("B — I feel anxious", "C — Pain", "D — Threat", "E — Overload"),
    ),
):
    out = BUILD / node
    manifest_path = out / "manifest.json"
    check(manifest_path.exists(), f"{node}: standalone manifest missing")
    if not manifest_path.exists():
        continue
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    check(manifest.get("release") == VERSION, f"{node}: standalone version drifted")
    check(
        manifest.get("source_count", 0) >= min_sources,
        f"{node}: local source block too small",
    )
    check(
        manifest.get("canonical_visual_count", 0) >= min_visuals,
        f"{node}: visual set below release minimum",
    )
    check(
        len(manifest.get("source_ids", []))
        == len(set(manifest.get("source_ids", []))),
        f"{node}: duplicate local source IDs",
    )
    outputs = manifest.get("outputs", {})
    check(set(outputs) == {"a4", "a4half", "largeprint"}, f"{node}: layout set drifted")

    reference_text: str | None = None
    for layout in ("a4", "a4half", "largeprint"):
        modes = outputs.get(layout, {})
        check(set(modes) == {"color", "mono"}, f"{node}/{layout}: color/mono set drifted")
        page_counts = []
        for monochrome in (False, True):
            mode = "mono" if monochrome else "color"
            stem_parts = [slug]
            if layout != "a4":
                stem_parts.append(layout)
            if monochrome:
                stem_parts.append("mono")
            stem = "_".join(stem_parts)
            md = out / f"{stem}.md"
            html = out / f"{stem}.html"
            pdf = out / f"{stem}.pdf"
            for path in (md, html, pdf):
                check(path.exists(), f"{node}: missing {path.name}")
            if md.exists():
                text = md.read_text(encoding="utf-8")
                content_region = text.split("# Handoff", 1)[0]
                for marker in required:
                    check(marker in text, f"{node}: canonical marker missing: {marker}")
                for marker in forbidden:
                    check(
                        f"\n## {marker}" not in content_region,
                        f"{node}: foreign owned section leaked: {marker}",
                    )
                check(
                    text.count("::: {.emergency-gate}") == 1,
                    f"{node}/{stem}: emergency gate count is not one",
                )
                for source_id in manifest.get("source_ids", []):
                    check(
                        f"### `{source_id}`" in text,
                        f"{node}: source {source_id} missing from local end matter",
                    )
            if html.exists():
                html_text = html.read_text(encoding="utf-8")
                check(
                    html_text.count('class="emergency-gate"') == 1,
                    f"{node}/{stem}: HTML emergency gate count is not one",
                )
                check(
                    'class="sources-and-limits"' in html_text,
                    f"{node}/{stem}: local source block missing",
                )
                check(
                    f'data-print-layout="{layout}"' in html_text,
                    f"{node}/{stem}: layout metadata missing",
                )
                check(
                    f'data-subguide="{node}"' in html_text,
                    f"{node}/{stem}: identity wrapper missing",
                )
                current_text = semantic_text(html)
                if reference_text is None:
                    reference_text = current_text
                else:
                    check(
                        current_text == reference_text,
                        f"{node}/{stem}: semantic text differs across editions",
                    )
            if pdf.exists():
                info = pdf_info(pdf)
                page_counts.append(int(info.get("Pages", "0") or 0))
                check(info.get("Tagged") == "yes", f"{node}/{stem}: PDF is not tagged")
                size = info.get("Page size", "")
                width, height = layout_geometry[layout]
                check(
                    width in size and height in size,
                    f"{node}/{stem}: wrong page geometry: {size}",
                )
                output_meta = modes.get(mode, {})
                check(
                    output_meta.get("pdf_sha256") == hashlib.sha256(pdf.read_bytes()).hexdigest(),
                    f"{node}/{stem}: PDF hash drifted",
                )
        if len(page_counts) == 2:
            check(
                page_counts[0] == page_counts[1],
                f"{node}/{layout}: color/mono page counts differ {page_counts}",
            )

hub_path = BUILD / "index.html"
hub_manifest_path = BUILD / "manifest.json"
check(hub_path.exists(), "graph hub HTML missing")
check(hub_manifest_path.exists(), "graph hub manifest missing")
if hub_manifest_path.exists():
    hub = json.loads(hub_manifest_path.read_text(encoding="utf-8"))
    check(hub.get("release") == VERSION, "hub release drifted")
    check(set(hub.get("standalone_nodes", [])) == {"B", "H"}, "hub standalone set drifted")
    check(len(hub.get("master_only_nodes", [])) == 7, "hub master-only set drifted")

if errors:
    raise SystemExit("Migration validation failed:\n- " + "\n- ".join(errors))

print(
    "Migration validation passed: canonical section/figure/source ownership, "
    "four-plus B/H visuals, graph hub, and 12 tagged standalone PDF editions "
    "with A4/A4/2/large-print color-mono parity."
)
