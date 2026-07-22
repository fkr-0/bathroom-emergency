#!/usr/bin/env python3
"""Structural, content-parity, and safety regression checks for the guide."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = sorted((ROOT / "src" / "chapters").glob("*.md"))
STYLE = (ROOT / "src" / "style.css").read_text(encoding="utf-8")
HTML = ROOT / "build" / "html" / "guide.html"
PDF = ROOT / "build" / "pdf" / "guide.pdf"
PACKAGE = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
VERSION = PACKAGE["version"]
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


check(len(CHAPTERS) == 11, f"expected 11 chapters, found {len(CHAPTERS)}")
source = "\n".join(path.read_text(encoding="utf-8") for path in CHAPTERS)
action_source = "\n".join(
    path.read_text(encoding="utf-8")
    for path in CHAPTERS
    if path.name not in {"09-version-history.md", "10-sources.md"}
)

# Safety regressions intentionally removed from the v3.x action material.
# History and evidence notes may quote a removed claim in order to document it.
for forbidden, message in {
    "Call 110. Now.": "medical path still routes to police 110",
    "pain_nrs_correlates": "pain score still claims physiological correlates",
    "2 drops of unscented household bleach": "unsafe concentration-free bleach recipe remains",
    "starvation is preferable to poisoning": "unsafe foraging rhetoric remains",
    "Notdienst (emergency lawyer)": "unverified legacy lawyer hotline remains",
    "fight it — not heroically": "unsafe instruction to fight loss of consciousness remains",
    "Scent candle location": "shared-print secret/unsafe candle field remains",
}.items():
    check(forbidden.lower() not in action_source.lower(), message)

check(
    "C(t) = C_0" not in action_source and "C(t)=C_0" not in action_source,
    "legacy cortisol-decay formula remains",
)
check(
    "112" in source and "116 117" in source and "116 123" in source,
    "core German help numbers missing",
)
check("column-count: 1 !important" in STYLE, "single-column print invariant missing")
check("columns: auto !important" in STYLE, "print column reset missing")

# Version and source-shape checks.
for path in CHAPTERS:
    text = path.read_text(encoding="utf-8")
    check(text.startswith("---\n"), f"{path.name}: missing YAML frontmatter")
    check(
        re.search(rf"revision:\s*[\"']{re.escape(VERSION)}[\"']", text) is not None,
        f"{path.name}: revision is not {VERSION}",
    )
    check(
        re.search(r"last_updated:\s*[\"']2026-07-22[\"']", text) is not None,
        f"{path.name}: release date is not 2026-07-22",
    )

# v3.3 breadth must remain represented even though unsafe claims were rewritten.
parity_markers = [
    "Mathematical notation legend",
    "Guide topology",
    "Flowchart legend",
    "Master flowchart",
    "A1 — A life may be developing",
    "A2 — Birth appears to be happening now",
    "A3 — A baby arrived recently",
    "Attachment",
    "Postpartum",
    "A8 — Ongoing responsibility",
    "silicon-based life form",
    "Panic attack",
    "GAD-7 severity spectrum",
    "NRS pain scale",
    "Cognitive load",
    "Smell decision tree",
    "No place to go",
    "Yerkes–Dodson",
    "Polyvagal",
    "Comfort inventory",
    "Conversation strategies",
    "Smalltalk toolkit",
    "Triage priority heatmap",
    "Suspected fractures",
    "Vital signs",
    "Self ambulance for non-physical emergencies",
    "Thermoregulation",
    "Prisoner’s dilemma",
    "Dunbar numbers",
    "Ostrom’s eight commons principles",
    "Forms of self-administration",
    "Psychology of masses",
    "IASC support pyramid",
    "Friends’ psychological-support guide",
    "Legal support",
    "Housing and “no place tonight”",
    "Master cross-reference",
    "Diagram index",
    "Fillable fields",
    "Complete decision tree",
    "Notes page",
    "Therapy effectiveness",
    "Game theory and cooperation",
]
for marker in parity_markers:
    check(marker.lower() in source.lower(), f"v3.3 parity marker missing: {marker}")

# A content-volume floor catches accidental replacement by the former lean edition.
check(
    len(source) >= 120_000,
    f"canonical chapter source is too small for full-content edition: {len(source):,} chars",
)

if HTML.exists():
    html = HTML.read_text(encoding="utf-8")
    check("<math" in html, "built HTML has no native MathML")
    check(
        "cdn.jsdelivr" not in html
        and re.search(r"<script[^>]+mathjax", html, re.IGNORECASE) is None,
        "built HTML has a remote math dependency",
    )
    check("<main id=\"guide\">" in html, "semantic guide wrapper missing")
    check("class=\"chapter" in html, "chapter wrappers missing")
    check(VERSION in html, f"built HTML does not contain version {VERSION}")
    for marker in ("IASC support pyramid", "Ostrom", "decision tree — safe text version"):
        check(marker.lower() in html.lower(), f"built HTML missing parity content: {marker}")
else:
    errors.append("build/html/guide.html is missing")

if PDF.exists():
    result = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True)
    check(result.returncode == 0, "pdfinfo could not read guide.pdf")
    if result.returncode == 0:
        match = re.search(r"Pages:\s+(\d+)", result.stdout)
        check(bool(match and int(match.group(1)) >= 30), "PDF is suspiciously short for full-content edition")
        check("A4" in result.stdout or "595" in result.stdout, "PDF does not appear to be A4")
else:
    errors.append("build/pdf/guide.pdf is missing")

for markdown_path in re.findall(r"\]\((?:build/)?(diagrams/[^)]+)\)", source):
    image = ROOT / "build" / markdown_path
    check(image.exists(), f"referenced image missing: {image.relative_to(ROOT)}")

if errors:
    print("Guide validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

print(
    "Guide validation passed: "
    f"{len(CHAPTERS)} chapters at {VERSION}, {len(source):,} source chars, "
    "v3.3 breadth markers, native MathML, A4 PDF, one-column print."
)
