#!/usr/bin/env python3
"""Fail the build when superseded guidance reappears in the source tree.

Copper's master flowchart is hand-maintained: no generator watches it, so it
drifted several releases behind the books it claims to index. The specific way
it drifted is worth catching mechanically -- an old routing rule survives in an
index page long after the owning book has replaced it, and nothing in the build
disagrees, because both files are internally consistent.

Each entry below is a phrase that was deliberately retired, together with what
replaced it. Matching is done on normalised text so a line wrap cannot hide a
phrase. Version history is exempt: describing what an old release said is that
chapter's entire job.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src_layout import all_chapter_paths  # noqa: E402

# phrase -> why it is retired and what to use instead
SUPERSEDED: dict[str, str] = {
    "isolate, preserve logs, notify owner":
        "Amber's artificial-entity branch now runs through the eight-question "
        "entity check; containment is described as the reversible option",
    "ten route identities":
        "the shelf has eleven maintained identities: O A B C D H Z P S T R",
    "ten maintained route identities":
        "the shelf has eleven maintained identities: O A B C D H Z P S T R",
    "care bridge fails":
        "Blue distinguishes urgent-but-not-life-threatening (116 117) from a "
        "life-supporting failure or imminent serious harm (112)",
    "essential medication cannot be maintained":
        "same Blue distinction: interruption must be causing or imminently "
        "risking serious harm before it is a 112 criterion",
    "a child without safe care":
        "the child route is tiered: 110/112 for danger, Jugendamt for no safe "
        "adult, 116 111 for counselling",
    "lawful shelter":
        "Blue asks whether you have a weather-safe place you can use tonight, "
        "not whether your occupancy was enforceable",
    "fresh-air route":
        "outdoors is not automatically safe air; use cleaner-air or safe-air "
        "route, which an official warning can override",
    "change passwords and device access from a trusted device":
        "a conspicuous account change can itself be noticed; the careful "
        "wording lives in Blue's digital-safety modifier",
}

# Recording what an earlier release said is the point of these chapters.
EXEMPT = {"09-version-history.md", "10-sources.md"}


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def main() -> int:
    failures: list[str] = []
    for path in all_chapter_paths():
        if path.name in EXEMPT:
            continue
        text = normalise(path.read_text(encoding="utf-8"))
        for phrase, replacement in SUPERSEDED.items():
            if phrase in text:
                failures.append(f"  {path.name}: superseded phrase {phrase!r}\n"
                                f"        {replacement}")
    if failures:
        print("Superseded-guidance validation failed:")
        print("\n".join(failures))
        return 1
    print(f"Superseded-guidance validation passed: {len(SUPERSEDED)} retired "
          f"rules absent from every current chapter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
