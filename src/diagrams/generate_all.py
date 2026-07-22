#!/usr/bin/env python3
"""Canonical diagram build entry point.

The former monolithic generator duplicated old v3.x charts, including figures
whose numbers were later withdrawn.  Keep orchestration here and the actual
figure families in focused scripts.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

DEPRECATED = {
    "stress_decay_curve.png",
    "anxiety_severity_spectrum.png",
    "triage_priority_heatmap.png",
    "survival_probability_function.png",
    "group_complexity_scaling.png",
    "pain_nrs_correlates.png",
    "water_requirements_scaling.png",
    "situation_a_tree.png",
}

for name in sorted(DEPRECATED):
    path = OUT / name
    if path.exists():
        path.unlink()
        print(f"  [REMOVED] deprecated generated figure {path}")

scripts = [
    "generate_pixel_art.py",
    "generate_flowgraph.py",
    "generate_routes.py",
    "generate_continuity.py",
    "generate_accessibility.py",
    "generate_scientific.py",
]
for script in scripts:
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name(script)), str(OUT)],
        check=True,
    )

print(f"Diagram build complete: {OUT}")
