#!/usr/bin/env python3
"""Resolve chapter files across the hub + subguide directory topology.

Canonical prose used to live in one flat ``src/chapters`` directory and books
were assembled by slicing that directory. Prose now lives where it belongs:

    src/hub/                       orientation and the shared door chapter
    src/subguides/<key>/chapters/  the prose one book owns

Chapter *filenames* stay stable and unique across the tree, because
``section_ownership.json``, ``source_inventory.json``, ``content_index.json``,
and the validators all key on the bare filename. This module is the only place
that knows where a given filename physically sits.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HUB_DIR = SRC / "hub"
SUBGUIDE_DIR = SRC / "subguides"

# Directory name per released book. Node ids stay canonical for data and
# routing; these readable keys only name directories.
BOOK_DIRS: dict[str, str] = {
    "O": "body",
    "A": "responsibility",
    "B": "calm",
    "C": "ambulance",
    "D": "safety",
    "H": "disaster",
    "Z": "zombie",
    "P": "support",
    "S": "social",
    "T": "templates",
    "R": "reference",
}

# Hub prose: the cover, the how-to-use orientation, and the door chapter whose
# sections four books draw from via section_ownership.json.
HUB_CHAPTERS: tuple[str, ...] = (
    "00-cover.md",
    "01-how-to-use.md",
    "03-situations-b-g.md",
)

# Which book directory owns each remaining chapter file.
BOOK_CHAPTERS: dict[str, str] = {
    "01b-body-owner-manual.md": "O",
    "02-situation-a.md": "A",
    "03g-safe-place-routing.md": "D",
    "03h-environmental-hazards.md": "H",
    "04-calm-guide.md": "B",
    "04b-social-field-guide.md": "S",
    "05-self-ambulance.md": "C",
    "06-zombie-guide.md": "Z",
    "06b-natural-disasters.md": "H",
    "07-professional-support.md": "P",
    "07a-templates.md": "T",
    "08-appendix.md": "R",
    "09-version-history.md": "R",
    "10-sources.md": "R",
}


def book_dir(node_id: str) -> Path:
    """Directory holding one book's own material."""
    return SUBGUIDE_DIR / BOOK_DIRS[node_id]


def chapter_dir(node_id: str) -> Path:
    return book_dir(node_id) / "chapters"


def expected_path(name: str) -> Path:
    """Where a chapter filename belongs under the current topology."""
    if name in HUB_CHAPTERS:
        return HUB_DIR / name
    node_id = BOOK_CHAPTERS.get(name)
    if node_id is None:
        raise KeyError(f"chapter {name!r} has no place in the source layout")
    return chapter_dir(node_id) / name


def chapter_path(name: str) -> Path:
    """Resolve a chapter filename to its file, raising if it is missing."""
    path = expected_path(name)
    if not path.exists():
        raise FileNotFoundError(f"missing chapter: {path}")
    return path


def find_chapter(name: str) -> Path | None:
    """Resolve a chapter filename, or None if it is unknown or absent.

    For validators that need to report a missing or misnamed chapter with their
    own message rather than raise.
    """
    try:
        path = expected_path(name)
    except KeyError:
        return None
    return path if path.exists() else None


def owning_book(name: str) -> str | None:
    """Node id of the book that owns this chapter, or None for hub prose."""
    return BOOK_CHAPTERS.get(name)


def chapter_names() -> list[str]:
    """Every chapter filename, sorted the way the flat directory used to be."""
    return sorted((*HUB_CHAPTERS, *BOOK_CHAPTERS))


def all_chapter_paths() -> list[Path]:
    """Every chapter file, in stable filename order.

    Replaces ``sorted(CHAPTER_DIR.glob("*.md"))`` so generated inventories keep
    byte-identical ordering across the migration.
    """
    return [chapter_path(name) for name in chapter_names()]
