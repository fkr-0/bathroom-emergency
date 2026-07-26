#!/usr/bin/env python3
"""Validate the generated landing page and deployment-document contract."""
from __future__ import annotations

from pathlib import Path

from project_meta import VERSION

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "build/site/index.html"
DEPLOYMENT = ROOT / "DEPLOYMENT.md"
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


check(SITE.exists(), "landing page missing")
check(DEPLOYMENT.exists(), "deployment instructions missing")
if SITE.exists():
    text = SITE.read_text(encoding="utf-8")
    for marker in (
        f"release {VERSION}",
        "Purpose and design ideas",
        "Participation and feedback",
        "Deployment in one screen",
        "Build and development",
        "Sources and disclaimers",
        "../html/guide.html",
        "../subguides/index.html",
        "href=\"DEPLOYMENT.md\"",
        "href=\"README.md\"",
        "href=\"CHANGELOG.md\"",
        "bathroom_emergency@fkr.dev",
        "bathroom-emergency.fkr.dev",
        "be.fkr.dev",
        "does not claim that hosting has already occurred",
    ):
        check(marker in text, f"landing page marker missing: {marker}")
if DEPLOYMENT.exists():
    text = DEPLOYMENT.read_text(encoding="utf-8")
    for marker in (
        "Minimum viable deployment",
        "Canonical deployment-field index",
        "Object- and person-specific safe places",
        "Physical installation concepts",
        "Additional deployables",
        "Build from source",
        "Maintenance cycle",
        "Privacy",
        "bathroom_emergency@fkr.dev",
    ):
        check(marker.lower() in text.lower(), f"deployment marker missing: {marker}")
for name in ("README.md", "DEPLOYMENT.md", "CHANGELOG.md"):
    copied = ROOT / "build/site" / name
    check(copied.exists() and copied.stat().st_size > 0, f"landing package document missing: {name}")

if errors:
    raise SystemExit("Landing/deployment validation failed:\n- " + "\n- ".join(errors))
print("Landing/deployment validation passed: project purpose, participation, build, deployment, sources, disclaimers, and guide links are present.")
