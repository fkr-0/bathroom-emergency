#!/usr/bin/env python3
"""Merge duplicate footnotes in Pandoc HTML output.

Pandoc emits one note per *reference*, not per source: citing the same source
twice produces two identically-worded entries in the reference list with
different numbers. Readers see the same citation printed twice and cannot tell
whether the second one differs.

This rewrites the note list so identical notes collapse to one entry, every
reference to them points at it, the surviving notes are renumbered
consecutively, and the note carries a back-link per referring passage.
"""
from __future__ import annotations

import re

REF_RE = re.compile(
    r'<a href="#fn(\d+)" class="footnote-ref" id="fnref(\d+)"([^>]*)><sup>\d+</sup></a>'
)
NOTE_RE = re.compile(r'<li id="fn(\d+)">(.*?)</li>', re.S)
BACKLINK_RE = re.compile(
    r'<a href="#fnref\d+(?:-\d+)?" class="footnote-back"[^>]*>.*?</a>', re.S
)


def _note_text(body: str) -> str:
    """Note content with back-links and whitespace normalized away."""
    return " ".join(BACKLINK_RE.sub("", body).split())


def merge_duplicate_footnotes(html: str) -> str:
    notes = NOTE_RE.findall(html)
    if not notes:
        return html

    # First note id for each distinct wording, in document order.
    canonical: dict[str, str] = {}
    replaces: dict[str, str] = {}
    for note_id, body in notes:
        key = _note_text(body)
        if key in canonical:
            replaces[note_id] = canonical[key]
        else:
            canonical[key] = note_id
            replaces[note_id] = note_id

    if all(old == new for old, new in replaces.items()):
        return html

    survivors = [note_id for note_id, _ in notes if replaces[note_id] == note_id]
    number = {note_id: index for index, note_id in enumerate(survivors, start=1)}

    # Referrers per surviving note, so each keeps a working back-link.
    referrers: dict[str, list[str]] = {note_id: [] for note_id in survivors}
    for ref_target, ref_id, _rest in REF_RE.findall(html):
        referrers[replaces[ref_target]].append(ref_id)

    def rewrite_ref(match: re.Match[str]) -> str:
        target = replaces[match.group(1)]
        own_id = match.group(2)
        return (
            f'<a href="#fn{number[target]}" class="footnote-ref" '
            f'id="fnref{own_id}"{match.group(3)}><sup>{number[target]}</sup></a>'
        )

    html = REF_RE.sub(rewrite_ref, html)

    def rewrite_note(match: re.Match[str]) -> str:
        note_id, body = match.group(1), match.group(2)
        if replaces[note_id] != note_id:
            return ""  # duplicate wording; its references now point elsewhere
        body = BACKLINK_RE.sub("", body)
        links = "".join(
            f'<a href="#fnref{ref}" class="footnote-back" role="doc-backlink">↩︎</a>'
            for ref in referrers[note_id]
        )
        if body.rstrip().endswith("</p>"):
            body = body.rstrip()[: -len("</p>")] + links + "</p>"
        else:
            body += links
        return f'<li id="fn{number[note_id]}">{body}</li>'

    return NOTE_RE.sub(rewrite_note, html)
