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
STYLE_A4_HALF = (ROOT / "src" / "style-a4-half.css").read_text(encoding="utf-8")
STYLE_LARGE_PRINT = (ROOT / "src" / "style-large-print.css").read_text(encoding="utf-8")
HTML = ROOT / "build" / "html" / "guide.html"
PDF = ROOT / "build" / "pdf" / "guide.pdf"
A4_HALF_HTML = ROOT / "build" / "html" / "guide_a4half.html"
A4_HALF_MONO_HTML = ROOT / "build" / "html" / "guide_a4half_mono.html"
A4_HALF_CSS = ROOT / "build" / "html" / "guide-a4half.css"
A4_HALF_MONO_CSS = ROOT / "build" / "html" / "guide-a4half-mono.css"
A4_HALF_PDF = ROOT / "build" / "pdf" / "guide_a4half.pdf"
A4_HALF_MONO_PDF = ROOT / "build" / "pdf" / "guide_a4half_mono.pdf"
PACKAGE = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
VERSION = PACKAGE["version"]
EVIDENCE_PATH = ROOT / "src" / "data" / "evidence_facts.json"
ROADMAP = ROOT / "ROADMAP.md"
NEXT_MINOR_PLAN = ROOT / "docs" / "plans" / "4.3.0-accessibility-plan.md"
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


check(len(CHAPTERS) == 13, f"expected 13 chapters, found {len(CHAPTERS)}")
source = "\n".join(path.read_text(encoding="utf-8") for path in CHAPTERS)
action_source = "\n".join(
    path.read_text(encoding="utf-8")
    for path in CHAPTERS
    if path.name not in {"09-version-history.md", "10-sources.md"}
)
opening_source = "\n".join(
    (ROOT / "src" / "chapters" / name).read_text(encoding="utf-8")
    for name in ("00-cover.md", "01-how-to-use.md")
)

# The reader-facing guide contains subject matter, not release archaeology.
for forbidden in (
    "v3.",
    "Version 3.",
    "Version 4.",
    "old guide",
    "old edition",
    "new chapter",
    "this chapter",
    "this subguide",
    "implemented candidate",
):
    check(forbidden.lower() not in action_source.lower(), f"reader-facing project meta remains: {forbidden}")
check(opening_source.count("112") == 1, "opening must contain exactly one 112 emergency gate")
for marker in (
    "The Small-Room Observatory",
    "When the outside gets quiet, the inside gets loud",
    "The gut votes early",
    "The room is amplifying you",
    "Anxiety bends time",
    "Acute stress makes the mind narrower, not stupider",
    "Naming a feeling changes the task",
    "Cold water is interesting, not magical",
    "Bathroom fainting is a real category",
    "Smell is a fading sensor",
    "The three-minute bathroom experiment",
):
    check(marker.lower() in opening_source.lower(), f"curiosity-first opening marker missing: {marker}")

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
check("font-size: 9.3pt" in STYLE, "standard A4 density typography invariant missing")
check("font-size: 8.35pt" in STYLE_A4_HALF, "A4/2 density typography invariant missing")
check(".emergency-gate" in STYLE, "single opening emergency-gate styling missing")
check("size: 105mm 297mm" in STYLE_A4_HALF, "A4/2 page geometry missing from layout CSS")
check("grid-template-columns: 1fr 1fr" in STYLE_A4_HALF, "A4/2 emergency strip adaptation missing")
check("table-layout: fixed" in STYLE_A4_HALF, "A4/2 narrow-table protection missing")
check("LOOK CLOSER" in STYLE_A4_HALF, "A4/2 curiosity figure label missing")
check("font-size: 13.25pt" in STYLE_LARGE_PRINT, "large-print typography invariant missing")
check("LARGE PRINT / TEXT ROUTE FOLLOWS" in STYLE_LARGE_PRINT, "large-print text-route marker missing")

# Evidence registry and figure checks. A chart may be simple; its provenance may not.
evidence: dict = {}
if EVIDENCE_PATH.exists():
    try:
        evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"evidence registry is invalid JSON: {exc}")
else:
    errors.append("src/data/evidence_facts.json is missing")

facts = evidence.get("facts", {}) if isinstance(evidence, dict) else {}
required_fact_keys = {
    "gad7_original",
    "gad7_cochrane",
    "breathwork_trial",
    "infertility_lifetime",
    "postpartum_psychosis",
    "stroke_time_model",
    "household_water",
    "sleep_restriction",
    "social_connection_mortality",
}
check(evidence.get("release") == VERSION, "evidence registry release does not match package version")
check(required_fact_keys <= set(facts), "evidence registry is missing one or more required fact sets")
for key in sorted(required_fact_keys & set(facts)):
    fact = facts[key]
    check(bool(fact.get("class")), f"evidence fact {key} has no evidence class")
    check(bool(fact.get("source")), f"evidence fact {key} has no source")
    check(bool(fact.get("limit")), f"evidence fact {key} has no practical limit")
    context_keys = {
        "population", "denominator", "scope", "target", "participants",
        "participants_included", "incidence_per_1000_range",
        "litres_per_person_per_day", "associations", "estimate",
    }
    check(any(name in fact for name in context_keys), f"evidence fact {key} has no scope or denominator field")

if required_fact_keys <= set(facts):
    check(facts["gad7_cochrane"].get("sensitivity") == 0.64, "pooled GAD-7 sensitivity drifted from reviewed value")
    check(facts["gad7_cochrane"].get("specificity") == 0.91, "pooled GAD-7 specificity drifted from reviewed value")
    check(facts["infertility_lifetime"].get("estimate") == 0.175, "WHO infertility estimate drifted from reviewed value")
    check(facts["stroke_time_model"].get("neurons_million_per_minute") == 1.9, "stroke model value drifted from reviewed value")
    check(facts["household_water"].get("litres_per_person_per_day") == 2, "BBK household-water value drifted from reviewed value")

required_evidence_figures = {
    "evidence_classes.png",
    "gad7_validation_comparison.png",
    "breathwork_trial_map.png",
    "reproductive_health_denominators.png",
    "stroke_time_model.png",
    "household_water_planner.png",
    "sleep_restriction_study.png",
    "social_connection_associations.png",
}
for name in sorted(required_evidence_figures):
    check((ROOT / "build" / "diagrams" / name).exists(), f"required evidence figure missing: {name}")
    check(name in source, f"required evidence figure is not referenced in chapters: {name}")

required_route_figures = {
    "two_pass_route_map.png",
    "hazard_override_matrix.png",
    "dependency_continuity_map.png",
    "safe_place_route_map.png",
    "communication_access_card.png",
}
for name in sorted(required_route_figures):
    check((ROOT / "build" / "diagrams" / name).exists(), f"required route figure missing: {name}")
    check(name in source, f"required route figure is not referenced in chapters: {name}")

deprecated_figures = {
    "stress_decay_curve.png",
    "anxiety_severity_spectrum.png",
    "survival_probability_function.png",
    "group_complexity_scaling.png",
    "pain_nrs_correlates.png",
    "water_requirements_scaling.png",
    "situation_a_tree.png",
}
for name in sorted(deprecated_figures):
    check(name not in source, f"deprecated figure is still referenced: {name}")
    check(not (ROOT / "build" / "diagrams" / name).exists(), f"deprecated figure was regenerated: {name}")

check(ROADMAP.exists(), "ROADMAP.md is missing")
if ROADMAP.exists():
    roadmap = ROADMAP.read_text(encoding="utf-8")
    for marker in (
        "Proposed two-pass topology",
        "fire, smoke, carbon monoxide",
        "vulnerable-person modifier",
        "4.2.0 — Routing and hazard architecture",
        "4.3.0 — Locale, accessibility, and safe-place routing",
        "4.4.0 — Household continuity modules",
    ):
        check(marker.lower() in roadmap.lower(), f"roadmap marker missing: {marker}")

check(NEXT_MINOR_PLAN.exists(), "4.3.0 accessibility plan is missing")
if NEXT_MINOR_PLAN.exists():
    next_minor = NEXT_MINOR_PLAN.read_text(encoding="utf-8")
    for marker in (
        "Safe-place route split",
        "Source freshness",
        "Communication access profiles",
        "Large-print edition",
        "Release acceptance",
    ):
        check(marker.lower() in next_minor.lower(), f"4.3.0 plan marker missing: {marker}")

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
    "The eight entry points",
    "Situation G — No Safe Place",
    "G1 — A person or active threat makes the place unsafe",
    "G2 — There is no weather-safe place to sleep tonight",
    "Communication and access card",
    "Minimal written emergency card",
    "Situation H — The Environment May Be Unsafe",
    "Essential medication and powered-device failure",
    "The hazard handoff",
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
    "Master flowchart — complete text version",
    "Navigation invariant",
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
    normalized_html = re.sub(r"\s+", " ", html).lower()
    for marker in (
        "The Small-Room Observatory",
        "The gut votes early",
        "Acute stress makes the mind narrower, not stupider",
        "Bathroom fainting is a real category",
        "The three-minute bathroom experiment",
        "IASC support pyramid",
        "Ostrom",
        "Master flowchart — complete text version",
        "That is not a contradiction requiring a duel between bar charts",
        "Time is brain",
        "Social connection is not decorative trim",
        "Situation G — No Safe Place",
        "G3 — A place exists, but it cannot safely support the person",
        "Minimal written emergency card",
        "Situation H — The Environment May Be Unsafe",
        "Essential medication and powered-device failure",
        "The hazard handoff",
    ):
        check(marker.lower() in normalized_html, f"built HTML missing required content: {marker}")
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


def check_a4_half_pdf(path: Path, label: str) -> None:
    if not path.exists():
        errors.append(f"{label} is missing")
        return
    result = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True)
    check(result.returncode == 0, f"pdfinfo could not read {label}")
    if result.returncode:
        return
    pages_match = re.search(r"Pages:\s+(\d+)", result.stdout)
    size_match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", result.stdout)
    check(bool(pages_match and int(pages_match.group(1)) >= 60), f"{label} is suspiciously short")
    if size_match:
        width = float(size_match.group(1))
        height = float(size_match.group(2))
        check(abs(width - 297.64) <= 1.5, f"{label} width is not 105 mm: {width:.2f} pt")
        check(abs(height - 841.89) <= 1.5, f"{label} height is not 297 mm: {height:.2f} pt")
    else:
        errors.append(f"could not parse page size for {label}")
    check("Tagged:          yes" in result.stdout, f"{label} is not tagged")


for narrow_html, label in (
    (A4_HALF_HTML, "A4/2 color HTML"),
    (A4_HALF_MONO_HTML, "A4/2 mono HTML"),
):
    if narrow_html.exists():
        narrow_text = narrow_html.read_text(encoding="utf-8")
        check(VERSION in narrow_text, f"{label} does not contain version {VERSION}")
        check("guide-a4half" in narrow_text, f"{label} does not link the A4/2 stylesheet")
    else:
        errors.append(f"{label} is missing")

for narrow_css, label in (
    (A4_HALF_CSS, "A4/2 color CSS"),
    (A4_HALF_MONO_CSS, "A4/2 mono CSS"),
):
    if narrow_css.exists():
        css_text = narrow_css.read_text(encoding="utf-8")
        check("size: 105mm 297mm" in css_text, f"{label} lacks A4/2 page geometry")
        check("LOOK CLOSER" in css_text, f"{label} lacks the narrow figure treatment")
    else:
        errors.append(f"{label} is missing")

check_a4_half_pdf(A4_HALF_PDF, "A4/2 color PDF")
check_a4_half_pdf(A4_HALF_MONO_PDF, "A4/2 mono PDF")

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
    f"{len(required_fact_keys)} reviewed fact sets, {len(required_evidence_figures)} evidence figures, "
    f"{len(required_route_figures)} route/access figures, v3.3 breadth markers, "
    "structured routing/locales/accessibility, roadmap coverage, native MathML, "
    "A4, A4/2, and large-print outputs."
)
