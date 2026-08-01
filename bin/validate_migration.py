#!/usr/bin/env python3
"""Validate ownership, source registry, hub, and released standalone editions."""
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
from project_meta import VERSION
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
            item.get("owner") in {"O", "A", "B", "C", "D", "H", "Z", "P", "T", "R"}
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
    for node_id, minimum in (("O", 4), ("C", 5), ("D", 4), ("Z", 7), ("P", 4)):
        reader = [
            item
            for item in records
            if item.get("owner") == node_id and item.get("reader_facing", True)
        ]
        check(
            len(reader) >= minimum,
            f"{node_id} standalone needs {minimum} useful canonical visuals, found {len(reader)}",
        )
    for item in records:
        check(
            item.get("owner") in {"O", "A", "B", "C", "D", "H", "Z", "P", "T", "R"},
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
    check(any("C" in item.get("subguides", []) for item in records), "C has no sources")
    check(any("D" in item.get("subguides", []) for item in records), "D has no sources")
    check(any("H" in item.get("subguides", []) for item in records), "H has no sources")
    check(any("O" in item.get("subguides", []) for item in records), "O has no sources")
    check(any("P" in item.get("subguides", []) for item in records), "P has no sources")
    check(sum("Z" in item.get("subguides", []) for item in records) >= 4, "Z has fewer than four sources")

layout_geometry = {
    "a4": ("594", "841"),
    # Chromium reports the standards-defined 105 mm width as 298.08 pt.
    "a4half": ("298", "841"),
    "largeprint": ("594", "841"),
}
for node, slug, min_sources, min_visuals, required, forbidden in (
    (
        "O",
        "small-room-observatory",
        11,
        4,
        (
            "The Small-Room Observatory",
            "Which guide should I pick?",
            "First 90 seconds — scan body, room, and attention",
            "When the outside gets quiet, the inside gets loud",
            "The three-minute bathroom experiment",
            "Sources and limits",
        ),
        (
            "B — I feel anxious",
            "C — Pain",
            "D — Threat",
            "F — Smell",
            "Situation G — No Safe Place",
        ),
    ),
    (
        "B",
        "alarm-calm",
        6,
        4,
        ("B — I feel anxious", "E — Overload", "Calm Guide", "Sources and limits"),
        ("C — Pain", "D — Threat", "F — Smell"),
    ),
    (
        "P",
        "professional-support",
        5,
        4,
        (
            "Professional Support — When the Bathroom Is Too Small",
            "Germany quick reference",
            "The call script — location before autobiography",
            "Make the contact operational — ask, confirm, record",
            "Support handoff map — service, form, figure, and route",
            "IASC support pyramid — start with foundations",
            "Support-selection matrix",
            "Sources and limits",
        ),
        (),
    ),
    (
        "C",
        "body-first-aid",
        7,
        5,
        (
            "C — Pain",
            "First Aid — You Are the First Link, Not the Whole Ambulance",
            "112 — one action box",
            "Unresponsive and not breathing normally",
            "AED — what it actually does",
            "Vital signs — observe, record, never self-clear",
            "Sources and limits",
        ),
        ("B — I feel anxious", "D — Threat", "E — Overload", "F — Smell"),
    ),
    (
        "D",
        "threat-safe-place",
        8,
        4,
        (
            "D — Threat has three clocks",
            "Situation G — No Safe Place",
            "A safe place is confirmed, not merely named",
            "G1 — A person or active threat makes the place unsafe",
            "G3 — A place exists, but it cannot safely support the person",
            "Communication and access card",
            "The safe-place handoff",
            "Sources and limits",
        ),
        ("B — I feel anxious", "C — Pain", "E — Overload", "F — Smell"),
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
    (
        "Z",
        "outage-continuity",
        4,
        7,
        (
            "Zombie Guide — Mostly for Non-Zombie Disasters",
            "Verify before optimizing",
            "Household continuity board",
            "Water — priority zero after air and immediate safety",
            "Essential medication and powered-device failure",
            "Group communication channels",
            "Five functions for the first meeting",
            "Evacuation pocket list",
            "Preparedness checklist before anything happens",
            "Sources and limits",
        ),
        (),
    ),
    (
        "T",
        "templates-blue-book",
        0,
        0,
        (
            "Templates — The Blue Book",
            "How to read the route band",
            "Use, update, replace",
            "Deployment cover and ownership card",
            "Observation and vital-sign log",
            "Feedback and field-note sheet",
            "Installation and wet-room audit",
            "First-aid figure usability review",
            "Sources and limits",
        ),
        (),
    ),
    (
        "R",
        "reference",
        0,
        2,
        (
            "Reference and Appendix — The Useful Loose Ends",
            "Stable references — addresses that survive editing",
            "Route identity key — code, colour, pattern, and glyph",
            "Professional contact and service index",
            "Illustration cross-reference — figures, routes, and forms",
            "Fillable fields live in T — Templates",
            "Glossary",
            "Global content index",
            "Source, visual, and standalone coverage matrix",
            "Version History",
            "Sources and Evidence Notes",
        ),
        (),
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
    encapsulation = manifest.get("encapsulation", {})
    for field in ("scope", "outside_scope", "aliases", "figure_refs", "form_refs", "support_refs"):
        check(field in encapsulation, f"{node}: encapsulation lacks {field}")
    check(bool(encapsulation.get("scope")), f"{node}: empty standalone scope")
    check(bool(encapsulation.get("outside_scope")), f"{node}: empty standalone boundary")
    check(bool(encapsulation.get("aliases")), f"{node}: no canonical aliases")
    check(
        len(encapsulation.get("figure_refs", [])) == manifest.get("canonical_visual_count", 0),
        f"{node}: figure reference set differs from canonical visual count",
    )
    if node == "P":
        check(bool(encapsulation.get("form_refs")), "P: no linked Blue Book forms")
        check(bool(encapsulation.get("support_refs")), "P: no linked support services")
    if node == "T":
        check(len(encapsulation.get("form_refs", [])) == 18, "T: not all canonical forms are indexed")
    if node == "R":
        check(bool(encapsulation.get("form_refs")), "R: no linked review/reference forms")

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
                for marker in ("Edition contract", "Edition resource map", "Deliberate boundary", "Canonical names"):
                    check(marker in text, f"{node}: encapsulation marker missing: {marker}")
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
                check(
                    'class="subguide-scope-grid"' in html_text,
                    f"{node}/{stem}: edition contract grid missing",
                )
                check(
                    'class="edition-resource-map"' in html_text,
                    f"{node}/{stem}: edition resource map missing",
                )
                if manifest.get("canonical_visual_count", 0):
                    check(
                        'class="figure-reference"' in html_text,
                        f"{node}/{stem}: figure cross-reference cards missing",
                    )
                if node == "T":
                    check(
                        html_text.count('class="template-route-band"') >= 18,
                        f"{node}/{stem}: canonical template route bands incomplete",
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
    check(
        set(hub.get("standalone_nodes", [])) == {"O", "B", "C", "D", "H", "Z", "P", "T", "R"},
        "hub standalone set drifted",
    )
    check(set(hub.get("master_only_nodes", [])) == {"A"}, "hub master-only set drifted")

if errors:
    raise SystemExit("Migration validation failed:\n- " + "\n- ".join(errors))

print(
    "Migration validation passed: canonical section/figure/source ownership, "
    "released visual minimums, graph hub, and 54 tagged standalone PDF editions "
    "with A4/A4/2/large-print color-mono parity."
)
