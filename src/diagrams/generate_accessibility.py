#!/usr/bin/env python3
"""Generate safe-place and communication-access figures from structured data."""
from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)
ROUTES = json.loads((ROOT / "src" / "data" / "route_catalog.json").read_text(encoding="utf-8"))
ACCESS = json.loads((ROOT / "src" / "data" / "accessibility_profiles.json").read_text(encoding="utf-8"))

INK = "#14201d"
MUTED = "#52645e"
PAPER = "#fbfaf4"
WHITE = "#ffffff"
GREEN = "#0d7355"
RED = "#b42318"
BLUE = "#175cd3"
PURPLE = "#6f3ab2"
AMBER = "#9b5b00"
PALE = "#e9f2ed"


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def canvas(figsize: tuple[float, float], xlim=(0, 12), ylim=(0, 10)):
    fig, ax = plt.subplots(figsize=figsize, dpi=180)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def card(ax, x, y, w, h, title, body, color, *, body_size=6.8):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=.04,rounding_size=.08",
        facecolor=WHITE, edgecolor=color, linewidth=2,
    ))
    ax.add_patch(FancyBboxPatch(
        (x, y + h - .44), w, .44,
        boxstyle="round,pad=.04,rounding_size=.08",
        facecolor=color, edgecolor=color, linewidth=0,
    ))
    ax.text(x + w / 2, y + h - .22, title, ha="center", va="center",
            color=WHITE, fontsize=9.2, fontweight="bold")
    ax.text(x + .18, y + h - .62, body, ha="left", va="top",
            color=INK, fontsize=body_size, linespacing=1.25)


def save(fig, name: str):
    path = OUT / name
    fig.savefig(path, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)
    print(f"  [OK] {path}")


# Four-way safe-place route map.
fig, ax = canvas((10.5, 8.6), (0, 12), (0, 9.5))
ax.text(6, 9.05, "SITUATION G / NO SAFE PLACE", ha="center", color=INK,
        fontsize=22, fontweight="bold")
ax.text(6, 8.62, "Secure the next safe hour. Then solve the larger problem.",
        ha="center", color=MUTED, fontsize=9, style="italic")
ax.add_patch(FancyBboxPatch((2.4, 7.65), 7.2, .58, boxstyle="round,pad=.03",
                            facecolor=RED, edgecolor=RED))
ax.text(6, 7.94, "OVERRIDE: 112 life/medical · 110 active threat · Situation H environment",
        ha="center", va="center", color=WHITE, fontsize=8.2, fontweight="bold")

routes = ROUTES["safe_place_routes"]
colors = [PURPLE, AMBER, BLUE, GREEN]
titles = {
    "violence-coercion": "1 / PERSON OR THREAT",
    "no-roof-tonight": "2 / NO ROOF TONIGHT",
    "access-care-failure": "3 / PLACE FAILS ACCESS OR CARE",
    "social-internal-crisis": "4 / SOCIAL OR INTERNAL CRISIS",
}
for idx, (route, color) in enumerate(zip(routes, colors)):
    col, row = idx % 2, idx // 2
    x = .45 + col * 5.8
    y = 4.55 - row * 3.0
    body = (
        "ACTION  " + wrap(route["action"], 49) + "\n\n"
        "BACKUP  " + wrap(route["backup"], 49) + "\n\n"
        "ESCALATE  " + wrap(route["escalation"], 49)
    )
    card(ax, x, y, 5.3, 2.62, titles[route["id"]], body, color, body_size=5.9)

ax.text(6, .3,
        "Every branch ends with a confirmed destination, access method, backup, and escalation condition.",
        ha="center", color=MUTED, fontsize=7.7)
save(fig, "safe_place_route_map.png")


# Communication access card.
fig, ax = canvas((10.5, 9.2), (0, 12), (0, 10.2))
ax.text(6, 9.75, "COMMUNICATION IS PART OF THE ROUTE", ha="center", color=INK,
        fontsize=21, fontweight="bold")
ax.text(6, 9.3, "Ask what works. Adapt the channel; do not lower the urgency threshold.",
        ha="center", color=MUTED, fontsize=9)
profiles = ACCESS["profiles"]
short = {
    "blind-low-vision": "BLIND / LOW VISION",
    "deaf-hard-of-hearing": "DEAF / HARD OF HEARING",
    "speech-language": "SPEECH / LANGUAGE",
    "cognitive-overload": "COGNITIVE OVERLOAD",
    "mobility-fatigue-pain": "MOBILITY / FATIGUE / PAIN",
    "sensory-panic-neurodivergent": "SENSORY / PANIC / NEURODIVERGENCE",
}
colors = [BLUE, PURPLE, GREEN, AMBER, BLUE, PURPLE]
for idx, (profile, color) in enumerate(zip(profiles, colors)):
    col, row = idx % 2, idx // 2
    x = .45 + col * 5.8
    y = 6.65 - row * 2.25
    body = wrap(profile["adaptation"], 53) + "\n\nHANDOFF  " + wrap(profile["handoff"], 48)
    card(ax, x, y, 5.3, 1.9, short[profile["id"]], body, color, body_size=6.1)

ax.add_patch(FancyBboxPatch((1.0, .34), 10.0, .78, boxstyle="round,pad=.04",
                            facecolor=PALE, edgecolor=GREEN, linewidth=1.5))
ax.text(6, .73,
        "ONE SPEAKER · ONE SENTENCE · ONE QUESTION · ONE NEXT ACTION · WRITE IT DOWN",
        ha="center", va="center", color=INK, fontsize=8.5, fontweight="bold")
save(fig, "communication_access_card.png")
