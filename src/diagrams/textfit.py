"""Keep diagram labels inside the boxes drawn around them.

Every generator here draws a box at hardcoded axes coordinates and then centres
a string in it. Nothing measures the string, so a caption that outgrows its
outline simply spills over both edges and still renders "successfully" -- which
is how "AN APOLOGY MAY BE PART OF REPAIR..." ended up straddling its own border
in the released figure.

Two functions, used together from each module's save():

    fit_labels(fig)   shrink any label that overflows its box, down to a floor
    audit_figure(fig) raise if anything still overflows

Shrinking handles the ordinary case without asking anyone to hand-tune axes
fractions. The floor exists because the honest answer to "this text is far too
long for that box" is a wider box, not 4pt type, and that is a decision for a
person.
"""
from __future__ import annotations

import os

from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Text

MIN_FONTSIZE = 6.5
# Boxes are drawn with a stroke; a label touching the inside of its own border
# reads as broken even when it technically fits.
PAD_PX = 3.0


class TextOverflow(RuntimeError):
    pass


def _eligible_patches(fig):
    """Container patches only: not arrows, not the figure/axes backgrounds."""
    patches = []
    for ax in fig.axes:
        for patch in ax.patches:
            if isinstance(patch, FancyArrowPatch):
                continue
            if patch in (ax.patch, fig.patch):
                continue
            patches.append(patch)
    return patches


def _violations(fig, renderer):
    """Labels that overlap at least one box and sit inside none of them."""
    patches = _eligible_patches(fig)
    if not patches:
        return []
    boxes = [(p, p.get_window_extent(renderer)) for p in patches]
    found = []
    for ax in fig.axes:
        for artist in ax.texts:
            if not isinstance(artist, Text) or not artist.get_text().strip():
                continue
            extent = artist.get_window_extent(renderer)
            overlapping = [
                (p, b) for p, b in boxes
                if b.overlaps(extent) or b.contains(extent.x0, extent.y0)
            ]
            if not overlapping:
                continue  # free-floating label; nothing claims to contain it
            contained = any(
                b.x0 + PAD_PX <= extent.x0 and extent.x1 <= b.x1 - PAD_PX
                and b.y0 + PAD_PX <= extent.y0 and extent.y1 <= b.y1 - PAD_PX
                for _, b in overlapping
            )
            if not contained:
                tightest = min(overlapping, key=lambda pb: pb[1].width)[1]
                found.append((artist, extent, tightest))
    return found


def fit_labels(fig) -> None:
    """Shrink overflowing labels until they fit, or until MIN_FONTSIZE."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for _ in range(24):
        pending = _violations(fig, renderer)
        if not pending:
            return
        shrunk = False
        for artist, _, _ in pending:
            size = artist.get_fontsize()
            if size > MIN_FONTSIZE:
                artist.set_fontsize(max(MIN_FONTSIZE, size * 0.94))
                shrunk = True
        if not shrunk:
            return  # everything is already at the floor; audit_figure reports it
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()


def audit_figure(fig, name: str) -> None:
    fig.canvas.draw()
    remaining = _violations(fig, fig.canvas.get_renderer())
    if not remaining:
        return
    lines = [f"{name}: {len(remaining)} label(s) overflow the box drawn around them"]
    for artist, extent, box in remaining:
        label = artist.get_text().replace("\n", " ")[:60]
        lines.append(
            f"    {label!r} is {extent.width:.0f}px wide in a {box.width:.0f}px box"
            f" at {artist.get_fontsize():.1f}pt"
        )
    lines.append("    widen the box or shorten the string; the label is already at the size floor")
    report = "\n".join(lines)
    if os.environ.get("DIAGRAM_TEXT_AUDIT") == "report":
        print("  [OVERFLOW] " + report)
        return
    raise TextOverflow(report)
