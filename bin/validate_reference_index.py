#!/usr/bin/env python3
"""Validate stable reference immutability, coverage, and generated fragments."""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from project_meta import VERSION

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data"
REGISTRY = DATA / "reference_ids.json"
INDEX = DATA / "content_index.json"
REF_RE = re.compile(r"^\[BEG:([OABCDHZPTR]):([SFGCDW]):(\d{3})\]$")
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


result = subprocess.run(
    ["python3", str(ROOT / "bin/build_reference_index.py"), "--check"],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
check(result.returncode == 0, (result.stderr or result.stdout).strip() or "reference generation check failed")
check(REGISTRY.exists(), "stable reference registry missing")
check(INDEX.exists(), "global content index missing")

if REGISTRY.exists() and INDEX.exists():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    ids = registry.get("ids", {})
    records = index.get("records", [])
    active = {item.get("resource_key"): item.get("public_ref") for item in records}
    check(registry.get("release") == VERSION, "reference registry release drifted")
    check(index.get("release") == VERSION, "content index release drifted")
    check(len(records) >= 290, f"content index unexpectedly small: {len(records)}")
    check(len(active) == len(records), "duplicate active resource keys")
    check(len(set(ids.values())) == len(ids), "public reference IDs are not unique")
    for key, ref in ids.items():
        check(bool(REF_RE.match(ref)), f"{key}: malformed public reference {ref}")
    for key, ref in active.items():
        check(ids.get(key) == ref, f"{key}: active index and registry disagree")
    retired = set(registry.get("retired_resource_keys", []))
    check(retired == set(ids) - set(active), "retired reference-key set drifted")
    check(not (set(active) & retired), "retired reference key is active")
    check(
        retired == {"section:09-version-history:4-5-0-23-july-2026-release-candidate"},
        f"unexpected stable references retired during wording edits: {sorted(retired)}",
    )
    counts = Counter(item.get("kind") for item in records)
    for kind in ("S", "F", "G", "C", "D", "W"):
        check(counts[kind] > 0, f"reference kind {kind} has no records")
    html_ids = [item.get("html_id") for item in records]
    check(len(html_ids) == len(set(html_ids)), "generated HTML reference anchors collide")

    route_ids = {
        item["id"]
        for item in json.loads((DATA / "subguides.json").read_text(encoding="utf-8"))["nodes"]
    }
    figure_ids = {
        item["resource_key"].split(":", 1)[1]
        for item in records if item.get("kind") == "G"
    }
    service_keys = {
        item.get("service_key")
        for item in records if item.get("kind") == "C" and item.get("service_key")
    }
    forms = [item for item in records if item.get("kind") == "F"]
    check(len(forms) == 18, f"expected 18 canonical forms, found {len(forms)}")
    for form in forms:
        check(bool(form.get("routes")), f"{form['title']}: no related route identities")
        check(
            set(form.get("routes", [])) <= route_ids,
            f"{form['title']}: unknown route identity",
        )
        check(
            set(form.get("figure_ids", [])) <= figure_ids,
            f"{form['title']}: unknown related figure",
        )
        check(
            set(form.get("support_keys", [])) <= service_keys,
            f"{form['title']}: unknown support service",
        )
        for field in ("purpose", "responsibility", "privacy"):
            check(bool(form.get(field)), f"{form['title']}: missing {field}")

for name in (
    "global-content-index.md",
    "diagram-index.md",
    "contact-index.md",
    "deployment-index.md",
    "glossary-index.md",
    "form-index.md",
    "route-identity-index.md",
    "support-form-map.md",
):
    path = ROOT / "build/generated" / name
    check(path.exists(), f"generated reference fragment missing: {name}")
    if path.exists():
        if name != "route-identity-index.md":
            check("[BEG:" in path.read_text(encoding="utf-8"), f"{name}: no stable references")

for name, markers in {
    "diagram-index.md": ("Illustration cross-reference", "Paired forms", "Route identity"),
    "form-index.md": ("Route identities", "Related figures", "Support routes", "Privacy"),
    "route-identity-index.md": ("code, colour, pattern, and glyph", "Deliberate boundary"),
    "support-form-map.md": ("Support handoff map", "Use these forms", "Related figures"),
}.items():
    path = ROOT / "build/generated" / name
    if path.exists():
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            check(marker in text, f"{name}: missing cross-reference marker {marker}")

check(
    (ROOT / "build/generated/coverage-matrix.md").exists(),
    "generated coverage fragment missing: coverage-matrix.md",
)

if errors:
    raise SystemExit("Reference-index validation failed:\n- " + "\n- ".join(errors))

print(f"Reference-index validation passed: {len(records)} stable active resources across six typed kinds.")
