#!/usr/bin/env python3
"""Generate simple first-aid orientation diagrams with complete text fallbacks."""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#16201d"
MUTED = "#52645e"
PAPER = "#fbfaf4"
RED = "#b42318"
BLUE = "#2457a6"
GREEN = "#0d7355"
LINE = "#9baca5"


def finish(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight", facecolor=PAPER)
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)
    print(f"  [OK] {OUT / (name + '.png')}")


# Adult CPR location: deliberately schematic, with head/hips/feet landmarks.
fig, ax = plt.subplots(figsize=(8.2, 10.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis("off")
ax.set_title("Adult chest-compression orientation", fontsize=20, fontweight="bold", color=INK, pad=18)
ax.text(5, 13.35, "Person flat on a firm surface · kneel beside the chest", ha="center", color=MUTED, fontsize=10)
ax.add_patch(Circle((5, 11.9), .72, facecolor="white", edgecolor=INK, linewidth=2))
# Torso, drawn as chest and abdomen rather than one box. With a single
# shoulders-to-hips rectangle, "centre of the chest" reads as centre of the
# rectangle, which is the upper abdomen -- the wrong place to compress.
ax.add_patch(FancyBboxPatch((3.25, 7.1), 3.5, 4.25, boxstyle="round,pad=.18,rounding_size=.8", facecolor="white", edgecolor=INK, linewidth=2))
ax.add_patch(Rectangle((3.32, 9.35), 3.36, 2.0, facecolor="#eef4f2", edgecolor="none", zorder=1))
ax.plot([3.32, 6.68], [9.35, 9.35], color=LINE, linewidth=1.6, linestyle=(0, (5, 3)), zorder=2)
ax.text(7.15, 9.35, "ribs end here", va="center", color=MUTED, fontsize=8.5)
ax.text(5, 11.02, "CHEST", ha="center", color=MUTED, fontsize=9, fontweight="bold", zorder=3)
ax.add_patch(Polygon([[3.55,7.2],[2.95,4.7],[3.75,4.55],[4.45,7.2]], closed=True, facecolor="white", edgecolor=INK, linewidth=2))
ax.add_patch(Polygon([[6.45,7.2],[5.55,7.2],[6.25,4.55],[7.05,4.7]], closed=True, facecolor="white", edgecolor=INK, linewidth=2))
ax.add_patch(Rectangle((3.95, 1.2), .9, 3.5, facecolor="white", edgecolor=INK, linewidth=2))
ax.add_patch(Rectangle((5.15, 1.2), .9, 3.5, facecolor="white", edgecolor=INK, linewidth=2))
ax.add_patch(Rectangle((3.55, .75), 1.3, .55, facecolor="white", edgecolor=INK, linewidth=2))
ax.add_patch(Rectangle((5.15, .75), 1.3, .55, facecolor="white", edgecolor=INK, linewidth=2))
# Target: lower half of the breastbone, which is the upper-middle of the torso.
ax.add_patch(Circle((5, 9.95), .42, facecolor="#fde7e5", edgecolor=RED, linewidth=3, zorder=4))
ax.plot([4.72, 5.28], [9.95, 9.95], color=RED, linewidth=2.4, zorder=5)
ax.plot([5, 5], [9.67, 10.23], color=RED, linewidth=2.4, zorder=5)
# Label sits clear of the figure; the leader ends at the circle and crosses nothing.
ax.text(9.7, 10.95, "HANDS HERE", ha="right", color=RED, fontsize=13, fontweight="bold")
ax.text(9.7, 10.55, "lower half of the breastbone", ha="right", color=INK, fontsize=10)
ax.add_patch(FancyArrowPatch((7.5, 10.45), (5.5, 10.05), arrowstyle="-|>", mutation_scale=16, color=RED, linewidth=2))
ax.text(9.7, 8.9, "not on the soft part", ha="right", color=MUTED, fontsize=9)
ax.text(9.7, 8.55, "below the ribs", ha="right", color=MUTED, fontsize=9)
ax.text(1.05, 11.9, "HEAD", color=BLUE, fontsize=11, fontweight="bold")
ax.add_patch(FancyArrowPatch((2.1, 11.9), (4.2, 11.9), arrowstyle="-|>", mutation_scale=12, color=BLUE))
ax.text(1.05, 6.25, "HIPS", color=BLUE, fontsize=11, fontweight="bold")
ax.add_patch(FancyArrowPatch((2.1, 6.25), (3.6, 6.25), arrowstyle="-|>", mutation_scale=12, color=BLUE))
ax.text(1.05, 1.0, "FEET", color=BLUE, fontsize=11, fontweight="bold")
ax.add_patch(FancyArrowPatch((2.1, 1.0), (3.5, 1.0), arrowstyle="-|>", mutation_scale=12, color=BLUE))
ax.text(5, .05, "Hands together · shoulders above hands · push hard and fast · allow full recoil", ha="center", color=GREEN, fontsize=9.5, fontweight="bold")
finish(fig, "cpr_body_orientation")


# Recovery position: five spatial steps, matching the adjacent text route.
# Laid out 2x3 rather than 1x5. One row of five made each panel about 25mm wide
# on the A4/2 edition, which is the primary print target -- readable only if you
# stopped and studied it, which is the opposite of what this figure is for.
fig, axes = plt.subplots(3, 2, figsize=(9.0, 10.6))
axes = list(axes.flat)  # a bare .flat iterator loses the spare cell to zip
fig.suptitle("Recovery position — unresponsive and breathing normally", fontsize=19, fontweight="bold", color=INK)
steps = [
    ("1", "Near arm up", "Kneel beside them.\nStraighten legs."),
    ("2", "Far hand to cheek", "Hold the hand\nagainst the near cheek."),
    ("3", "Far knee up", "Bend the far leg\nwithout lifting the body."),
    ("4", "Roll toward you", "Use the bent knee\nas a lever."),
    ("5", "Airway and drain", "Top leg at a right angle.\nTilt head back; mouth down."),
]
for ax, (number, title, note) in zip(axes[:5], steps):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((.03,.05),.94,.88,boxstyle="round,pad=.02",facecolor="white",edgecolor=LINE,linewidth=1.5))
    ax.add_patch(Circle((.16,.82),.09,facecolor=GREEN,edgecolor=GREEN))
    ax.text(.16,.82,number,color="white",fontweight="bold",ha="center",va="center")
    ax.add_patch(Circle((.28,.55),.09,facecolor="white",edgecolor=INK,linewidth=1.5))
    if number in {"1","2","3"}:
        ax.plot([.36,.72],[.55,.55],color=INK,linewidth=5,solid_capstyle="round")
        ax.plot([.48,.38],[.55,.34],color=BLUE,linewidth=3)
        ax.plot([.63,.78],[.55,.33 if number=="3" else .55],color=BLUE,linewidth=3)
    else:
        ax.plot([.34,.66],[.55,.43],color=INK,linewidth=5,solid_capstyle="round")
        ax.plot([.52,.73],[.48,.27],color=BLUE,linewidth=3)
        ax.plot([.52,.35],[.48,.26],color=BLUE,linewidth=3)
        ax.add_patch(FancyArrowPatch((.75,.66),(.60,.52),arrowstyle="-|>",mutation_scale=12,color=GREEN))
    ax.text(.5,.18,title,ha="center",fontweight="bold",color=INK,fontsize=10)
    ax.text(.5,.075,note,ha="center",va="top",color=MUTED,fontsize=7.8)
spare = axes[5]                   # the sixth cell carries the standing instruction
spare.set_xlim(0, 1); spare.set_ylim(0, 1); spare.axis("off")
spare.add_patch(FancyBboxPatch((.03,.05),.94,.88,boxstyle="round,pad=.02",
                               facecolor="#fdf1ef",edgecolor=RED,linewidth=1.8))
spare.text(.5,.62,"Keep checking\nnormal breathing.",ha="center",va="center",
           color=INK,fontweight="bold",fontsize=12)
spare.text(.5,.34,"Abnormal breathing\nmeans CPR.",ha="center",va="center",
           color=RED,fontweight="bold",fontsize=12)
fig.text(.5,.015,"Call 112 · do not give food or drink",ha="center",color=RED,fontweight="bold",fontsize=10)
fig.tight_layout(rect=(0,.03,1,.94))
finish(fig, "recovery_position_steps")


# AED action sequence: no reboot metaphor; the device decides whether shock is indicated.
fig, ax = plt.subplots(figsize=(12.6, 5.2))
ax.set_xlim(0, 12.6)
ax.set_ylim(0, 5.2)
ax.axis("off")
ax.set_title("AED — attach, listen, clear, continue CPR", fontsize=20, fontweight="bold", color=INK, pad=14)
# Notes are wrapped to the panel rather than hand-broken: "Device shocks only
# if indicated." was one character run too long and printed through the box.
NOTE_WRAP = 19
steps = [
    ("1", "TURN ON", "Open or power on. Follow the voice."),
    ("2", "BARE + DRY CHEST", "Attach pads exactly as pictured."),
    ("3", "ANALYSE", "Nobody touches the person."),
    ("4", "SHOCK IF TOLD", "Say CLEAR. Device shocks only if indicated."),
    ("5", "CPR AGAIN", "Resume immediately. Follow the next prompt."),
]
steps = [(n, title, textwrap.fill(note, NOTE_WRAP)) for n, title, note in steps]
for index,(number,title,note) in enumerate(steps):
    x=.25+index*2.46
    ax.add_patch(FancyBboxPatch((x,.9),2.12,3.2,boxstyle="round,pad=.08",facecolor="white",edgecolor=BLUE if index<3 else RED if index==3 else GREEN,linewidth=2))
    ax.add_patch(Circle((x+.27,3.76),.17,facecolor=INK,edgecolor=INK))
    ax.text(x+.27,3.76,number,color="white",ha="center",va="center",fontweight="bold")
    ax.text(x+1.06,3.14,title,ha="center",color=INK,fontweight="bold",fontsize=10)
    ax.text(x+1.06,2.25,note,ha="center",va="center",color=MUTED,fontsize=8.8)
    if index<4:
        ax.add_patch(FancyArrowPatch((x+2.14,2.5),(x+2.38,2.5),arrowstyle="-|>",mutation_scale=12,color=LINE))
ax.text(6.3,.35,"An AED analyzes the rhythm. It does not shock every cardiac arrest and it does not replace compressions.",ha="center",color=INK,fontweight="bold",fontsize=9.4)
finish(fig, "aed_action_sequence")
