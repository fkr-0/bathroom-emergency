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
# Two separately authored labels should never visibly occupy the same pixels.
# A tiny amount of renderer antialias/bbox rounding is harmless, so require a
# real intersection in both dimensions and a meaningful fraction of the
# smaller label before calling it a collision.
TEXT_COLLISION_PX = 2.0
TEXT_COLLISION_FRACTION = 0.02


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


def _text_artists(fig):
    """Visible authored text whose layout is controlled by the figure code.

    Axis tick labels are deliberately excluded: Matplotlib owns those through
    its axis layout engine.  ``ax.text`` labels and titles are ours, which is
    exactly the class where hand-positioned card labels can silently collide.
    """
    for ax in fig.axes:
        seen: set[int] = set()
        candidates = [
            *ax.texts,
            ax.title,
            getattr(ax, "_left_title", None),
            getattr(ax, "_right_title", None),
        ]
        for artist in candidates:
            if not isinstance(artist, Text):
                continue
            if id(artist) in seen or not artist.get_visible() or not artist.get_text().strip():
                continue
            seen.add(id(artist))
            yield ax, artist


def _text_collisions(fig, renderer):
    """Return independently positioned labels whose rendered bounds overlap."""
    by_axes: dict[object, list[tuple[Text, object]]] = {}
    for ax, artist in _text_artists(fig):
        extent = artist.get_window_extent(renderer)
        if extent.width <= 0.5 or extent.height <= 0.5:
            continue
        by_axes.setdefault(ax, []).append((artist, extent))

    found = []
    for artists in by_axes.values():
        for index, (left, left_box) in enumerate(artists):
            for right, right_box in artists[index + 1:]:
                overlap_w = min(left_box.x1, right_box.x1) - max(left_box.x0, right_box.x0)
                overlap_h = min(left_box.y1, right_box.y1) - max(left_box.y0, right_box.y0)
                if overlap_w <= TEXT_COLLISION_PX or overlap_h <= TEXT_COLLISION_PX:
                    continue
                smaller_area = min(
                    left_box.width * left_box.height,
                    right_box.width * right_box.height,
                )
                if smaller_area <= 0:
                    continue
                overlap_fraction = (overlap_w * overlap_h) / smaller_area
                if overlap_fraction < TEXT_COLLISION_FRACTION:
                    continue
                found.append(
                    (left, right, overlap_w, overlap_h, overlap_fraction)
                )
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
    renderer = fig.canvas.get_renderer()
    remaining = _violations(fig, renderer)
    collisions = _text_collisions(fig, renderer)
    if not remaining and not collisions:
        return
    lines = [
        f"{name}: diagram text-layout audit failed "
        f"({len(remaining)} box overflow(s), {len(collisions)} text collision(s))"
    ]
    if remaining:
        lines.append("  Box overflows:")
        for artist, extent, box in remaining:
            label = artist.get_text().replace("\n", " ")[:60]
            lines.append(
                f"    {label!r} is {extent.width:.0f}px wide in a {box.width:.0f}px box"
                f" at {artist.get_fontsize():.1f}pt"
            )
        lines.append(
            "    widen the box or shorten the string; the label is already at the size floor"
        )
    if collisions:
        lines.append("  Text collisions:")
        for left, right, overlap_w, overlap_h, fraction in collisions:
            left_label = left.get_text().replace("\n", " ")[:52]
            right_label = right.get_text().replace("\n", " ")[:52]
            lines.append(
                f"    {left_label!r} overlaps {right_label!r} by "
                f"{overlap_w:.0f}×{overlap_h:.0f}px ({fraction:.0%} of the smaller label)"
            )
        lines.append("    move or reflow the labels; shrinking both is not a correctness fix")
    report = "\n".join(lines)
    if os.environ.get("DIAGRAM_TEXT_AUDIT") == "report":
        print("  [OVERFLOW] " + report)
        return
    raise TextOverflow(report)
