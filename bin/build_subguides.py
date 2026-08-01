#!/usr/bin/env python3
"""Build the graph hub and released standalone vertical slices.

Canonical prose remains in src/chapters. This builder extracts owned sections,
adds generated orientation/source wrappers, and renders the same content into
A4, A4/2, and large-print colour/monochrome editions.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from build_reference_index import decorate_figure_references, inject_heading_ids, mini_toc
from project_meta import (
    SOURCE_REVIEW_DATE,
    VERSION,
    build_date,
    git_revision,
    revision_footer_css,
)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
CHAPTER_DIR = SRC / "chapters"
DATA_DIR = SRC / "data"
BUILD = ROOT / "build" / "subguides"
REVIEWED_ON = SOURCE_REVIEW_DATE
REF_RE = re.compile(r"\[\^([A-Za-z0-9_-]+)\]")
DEF_RE = re.compile(r"^\[\^([A-Za-z0-9_-]+)\]:")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\((build/diagrams/[^)]+)\)")
LAYOUTS = {
    "a4": None,
    "a4half": SRC / "style-a4-half.css",
    "largeprint": SRC / "style-large-print.css",
}


def load_guide_module():
    path = ROOT / "bin" / "build_guide.py"
    spec = importlib.util.spec_from_file_location("build_guide", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load build_guide.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BG = load_guide_module()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout).strip())
    return result


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_pages(path: Path) -> int:
    result = run(["pdfinfo", str(path)])
    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError(f"could not read page count for {path}")
    return int(match.group(1))


def remove_footnote_definitions(text: str) -> str:
    lines = text.splitlines()
    kept: list[str] = []
    index = 0
    while index < len(lines):
        if DEF_RE.match(lines[index]):
            index += 1
            while index < len(lines) and (
                lines[index].startswith("    ") or lines[index].startswith("\t")
            ):
                index += 1
            continue
        kept.append(lines[index])
        index += 1
    return "\n".join(kept).rstrip()


def mixed_sections(owner: str) -> str:
    path = CHAPTER_DIR / "03-situations-b-g.md"
    body = BG.strip_frontmatter(path.read_text(encoding="utf-8"))
    lines = body.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if line.startswith("## "):
            starts.append((index, line[3:].strip()))
    ownership = json.loads(
        (DATA_DIR / "section_ownership.json").read_text(encoding="utf-8")
    )["sections"]
    owner_by_heading = {
        item["heading"]: item["owner"]
        for item in ownership
        if item["chapter"] == path.name and item["level"] == 2
    }
    chunks: list[str] = []
    for pos, (start, heading) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        if owner_by_heading.get(heading) == owner:
            chunks.append("\n".join(lines[start:end]).strip())
    if not chunks:
        raise RuntimeError(f"no mixed sections for owner {owner}")
    return "\n\n".join(chunks)


def chapter_without_definitions(filename: str) -> str:
    text = remove_footnote_definitions(
        BG.strip_frontmatter((CHAPTER_DIR / filename).read_text(encoding="utf-8"))
    )
    return re.sub(r"\{\{subguide-sources:[A-Z]\}\}", "", text).rstrip()


def replace_refs(
    text: str,
    chapter: str,
    source_lookup: dict[tuple[str, str], dict],
    ordered_sources: list[dict],
) -> str:
    seen = {item["id"] for item in ordered_sources}

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        source = source_lookup.get((chapter, key))
        if source is None:
            raise RuntimeError(f"unresolved source {chapter}:{key}")
        if source["id"] not in seen:
            ordered_sources.append(source)
            seen.add(source["id"])
        return f"[^{source['id']}]"

    return REF_RE.sub(repl, text)


def source_endmatter(sources: list[dict]) -> str:
    groups = [
        ("Operational routes", "operational"),
        ("Research and evidence", "research"),
        ("Models and explanatory sources", "explanatory"),
    ]
    parts = [
        "# Sources and limits",
        "",
        "Generated from the canonical source registry. Every entry stays attached "
        "to the subguide that uses it; scope and operational limits remain part "
        "of the entry.",
        "",
    ]
    for title, kind in groups:
        subset = [item for item in sources if item["kind"] == kind]
        if not subset:
            continue
        parts.extend([f"## {title}", ""])
        for item in subset:
            parts.extend(
                [
                    f"### `{item['id']}`",
                    "",
                    item["text"],
                    "",
                    f"**Used in:** {item['chapter']} · **Subguide ownership:** "
                    f"{', '.join(item['subguides']) or 'unassigned'}",
                    "",
                ]
            )
    parts.extend(["## Citation links", ""])
    for item in sources:
        parts.append(
            f"[^{item['id']}]: See source `{item['id']}` in "
            "**Sources and limits** above."
        )
    return "\n".join(parts).rstrip()


def variant_stem(slug: str, layout: str, monochrome: bool) -> str:
    parts = [slug]
    if layout != "a4":
        parts.append(layout)
    if monochrome:
        parts.append("mono")
    return "_".join(parts)


def identity_css(node: dict, *, layout: str, monochrome: bool) -> str:
    parts = [
        (SRC / "style.css").read_text(encoding="utf-8"),
        (SRC / "style-subguides.css").read_text(encoding="utf-8"),
    ]
    if LAYOUTS[layout] is not None:
        parts.append(LAYOUTS[layout].read_text(encoding="utf-8"))
    if monochrome:
        parts.append((SRC / "style-mono.css").read_text(encoding="utf-8"))
    parts.append(
        revision_footer_css(
            title=f'{node["id"]} — {node["title"]}',
            layout=layout,
            mode="mono" if monochrome else "color",
        )
    )
    layout_label = {"a4": "A4", "a4half": "A4/2", "largeprint": "LARGE PRINT"}[layout]
    parts.append(
        "\n".join(
            (
                "/* Generated standalone page furniture. */",
                f'@page {{ @top-left {{ content: "{node["id"]} / {node["title"]}"; }} '
                f'@top-right {{ content: "{layout_label}"; }} }}',
                f':root {{ --subguide-accent: {node["colour"]}; }}',
            )
        )
    )
    return "\n\n".join(parts) + "\n"


def meta_grid(node: dict, layout: str) -> str:
    values = [
        ("Guide version", VERSION),
        ("Subguide revision", VERSION),
        ("Locale", "de-DE / English text"),
        ("Source review", REVIEWED_ON),
        ("Edition", f"standalone {layout}"),
        ("Identity", f'{node["id"]} · {node["pattern"]} · {node["glyph"]}'),
    ]
    blocks = "\n".join(
        f'<div><strong>{label}</strong>{value}</div>' for label, value in values
    )
    return f'<div class="subguide-meta">{blocks}</div>'


def neighbour_grid(node: dict, titles: dict[str, str]) -> str:
    blocks = "\n".join(
        f'<div><strong>{edge} — {titles[edge]}</strong><br>'
        "Move here when that problem becomes primary.</div>"
        for edge in node["outgoing"]
    )
    return f'<div class="subguide-neighbours">{blocks}</div>'


def route_chip(route: str, nodes: dict[str, dict]) -> str:
    node = nodes[route]
    return (
        f'<span class="route-chip" data-subguide="{route}">'
        f'<strong>{route}</strong><span>{node["title"]}</span>'
        f'<small>{node["pattern"].replace("-", " ")}</small></span>'
    )


def edition_resource_map(node: dict, visual_files: list[str]) -> tuple[str, dict]:
    index = json.loads((DATA_DIR / "content_index.json").read_text(encoding="utf-8"))
    records = index["records"]
    nodes = {
        item["id"]: item
        for item in json.loads((DATA_DIR / "subguides.json").read_text(encoding="utf-8"))["nodes"]
    }
    visual_records = [
        item for item in records
        if item.get("kind") == "G" and item.get("file") in visual_files
    ]
    form_records = [
        item for item in records
        if item.get("kind") == "F"
        and (node["id"] == "T" or node["id"] in item.get("routes", []))
    ]
    support_keys = {
        key for form in form_records for key in form.get("support_keys", [])
    }
    support_records = [
        item for item in records
        if item.get("kind") == "C" and item.get("service_key") in support_keys
    ]

    if visual_records:
        figures = "".join(
            f'<li><strong>{item["public_ref"]}</strong> {item["title"]}<br>'
            f'<span>{item.get("question", "")}</span></li>'
            for item in visual_records
        )
    else:
        figures = "<li>No figure is required to use the text route.</li>"

    if node["id"] == "T":
        forms = (
            f'<p><strong>{len(form_records)} canonical forms.</strong> Each heading below '
            'carries its stable form address, privacy class, route chips, paired figures, '
            'and support links.</p>'
        )
    elif form_records:
        forms = "<ul>" + "".join(
            f'<li><strong>{item["public_ref"]}</strong> {item["title"]} '
            f'<span class="resource-privacy">{item.get("privacy", "review locally")}</span></li>'
            for item in form_records
        ) + "</ul>"
    else:
        forms = "<p>No dedicated Blue Book form is required.</p>"

    if support_records:
        support = "<ul>" + "".join(
            f'<li><strong>{item["public_ref"]}</strong> {item["title"]} — '
            f'{item.get("scope", "verify locally")}</li>'
            for item in support_records
        ) + "</ul>"
    else:
        support = "<p>Use the named local or emergency route when the text calls for it.</p>"

    related_routes = [node["id"]]
    for form in form_records:
        related_routes.extend(form.get("routes", []))
    related_routes.extend(item["owner"] for item in visual_records)
    related_routes = list(dict.fromkeys(related_routes))
    route_chips = "".join(route_chip(route, nodes) for route in related_routes)
    html = f'''<div class="edition-resource-map">
<section><h3>Figures inside this edition</h3><ul>{figures}</ul></section>
<section><h3>Blue Book forms paired with this route</h3>{forms}</section>
<section><h3>Support routes named by those forms</h3>{support}</section>
<section class="edition-route-key"><h3>Route key</h3><div class="route-chip-row">{route_chips}</div></section>
</div>'''
    metadata = {
        "figure_refs": [item["public_ref"] for item in visual_records],
        "form_refs": [item["public_ref"] for item in form_records],
        "support_refs": [item["public_ref"] for item in support_records],
    }
    return html, metadata


def build_markdown(
    node: dict,
    canonical_content: str,
    ordered_sources: list[dict],
    *,
    layout: str,
    contents: str,
    resource_map: str,
) -> str:
    node_id = node["id"]
    titles = {
        item["id"]: item["title"]
        for item in json.loads(
            (DATA_DIR / "subguides.json").read_text(encoding="utf-8")
        )["nodes"]
    }
    questions = "\n".join(f"- {question}" for question in node["questions"])
    handoffs = "\n".join(
        f"- **{edge} — {titles[edge]}** — move here when that problem becomes primary."
        for edge in node["outgoing"]
    )
    cover = f'''::: {{#top .standalone-subguide data-subguide="{node_id}" data-pattern="{node["pattern"]}"}}

::: {{.subguide-cover}}

<div class="subguide-family-mark">Bathroom Emergency Guide / graph field guide</div>
<div class="subguide-code">{node_id}</div>

# {node["title"]}

<div class="subguide-promise">{node["promise"]}</div>

:::

::: {{.subguide-position data-subguide="{node_id}"}}

# Page 0 — Position in the graph

![Subguide graph for {node_id} — {node["title"]}](build/diagrams/subguide_graph_{node_id}.png)

{meta_grid(node, layout)}

<div class="subguide-identity-key"><span class="subguide-pattern-swatch" aria-hidden="true"></span><span><strong>{node_id}</strong> uses the <strong>{node["pattern"].replace("-", " ")}</strong> pattern and the written glyph name <strong>{node["glyph"].replace("-", " ")}</strong>.</span></div>

## Arrive here when

{questions}

## Edition contract

<div class="subguide-scope-grid">
<section><strong>Inside</strong><p>{node["scope"]}</p></section>
<section><strong>Deliberate boundary</strong><p>{node["outside_scope"]}</p></section>
<section><strong>Canonical names</strong><p>{" · ".join(node["aliases"])}</p></section>
<section><strong>Exit rule</strong><p>Move to a named neighbouring route when its problem becomes primary; immediate danger bypasses the graph.</p></section>
</div>

## Neighbouring routes

{neighbour_grid(node, titles)}

::: {{.emergency-gate}}

**Immediate emergency gate**

Call **112** now for immediate danger to life, severe breathing difficulty,
unconsciousness, fire, smoke, suspected carbon monoxide, major bleeding, or
another rapidly escalating emergency. Move to safety first when the environment
itself is dangerous.

:::

:::

::: {{.subguide-intro}}

# Introduction and contents

**Begin with the loudest useful question, not a complete theory of your life.**
This edition collects the canonical sections owned by node **{node_id}** and
keeps their original order.

Questions in this edition:

{questions}

## Mini contents

{contents or '- The canonical content follows on the next page.'}

## Edition resource map

{resource_map}

The HTML navigation and PDF outline contain the same route. The graph above and
the handoff page below remain complete in text.

:::
'''
    handoff = f'''::: {{.subguide-handoff data-subguide="{node_id}"}}

# Handoff — What changed while reading?

- **Better:** write the action that helped and the condition that would change the route.
- **Same:** use the backup action or choose the closest neighbouring guide.
- **Worse:** use the chapter escalation condition; immediate danger goes directly to **112**.
- **Different problem:** follow the named graph edge below.

{handoffs}

**Notes:** ________________________________________________________________

**Next check / time:** ____________________________________________________

:::
'''
    endmatter = (
        f'::: {{.sources-and-limits data-subguide="{node_id}"}}\n\n'
        + source_endmatter(ordered_sources)
        + "\n\n:::"
    )
    return "\n\n".join((cover, canonical_content, handoff, endmatter, ":::")) + "\n"


def canonical_blocks(node_id: str) -> list[tuple[str, str]]:
    if node_id == "O":
        return [
            ("01-how-to-use.md", chapter_without_definitions("01-how-to-use.md")),
        ]
    if node_id == "D":
        return [
            ("03-situations-b-g.md", mixed_sections("D")),
            (
                "03g-safe-place-routing.md",
                chapter_without_definitions("03g-safe-place-routing.md"),
            ),
        ]
    if node_id == "B":
        return [
            ("03-situations-b-g.md", mixed_sections("B")),
            ("04-calm-guide.md", chapter_without_definitions("04-calm-guide.md")),
        ]
    if node_id == "P":
        return [
            ("07-professional-support.md", chapter_without_definitions("07-professional-support.md")),
        ]
    if node_id == "C":
        return [
            ("03-situations-b-g.md", mixed_sections("C")),
            ("05-self-ambulance.md", chapter_without_definitions("05-self-ambulance.md")),
        ]
    if node_id == "H":
        return [
            ("03-situations-b-g.md", mixed_sections("H")),
            (
                "03h-environmental-hazards.md",
                chapter_without_definitions("03h-environmental-hazards.md"),
            ),
        ]
    if node_id == "Z":
        return [
            ("06-zombie-guide.md", chapter_without_definitions("06-zombie-guide.md")),
        ]
    if node_id == "T":
        return [
            ("07a-templates.md", chapter_without_definitions("07a-templates.md")),
        ]
    if node_id == "R":
        return [
            ("08-appendix.md", chapter_without_definitions("08-appendix.md")),
            ("09-version-history.md", chapter_without_definitions("09-version-history.md")),
            ("10-sources.md", chapter_without_definitions("10-sources.md")),
        ]
    raise RuntimeError(f"node {node_id} is not a released standalone edition")


def build_node(node_id: str) -> dict:
    manifest = json.loads(
        (DATA_DIR / "subguides.json").read_text(encoding="utf-8")
    )
    node = next(item for item in manifest["nodes"] if item["id"] == node_id)
    inventory = json.loads(
        (DATA_DIR / "source_inventory.json").read_text(encoding="utf-8")
    )
    if inventory.get("status") != "canonical-source-registry":
        raise RuntimeError("source registry is not canonical")
    source_lookup = {
        (item["chapter"], item["footnote_key"]): item
        for item in inventory["footnote_sources"]
    }
    ordered_sources: list[dict] = []
    content_parts: list[str] = []
    for chapter, block in canonical_blocks(node_id):
        block = BG.expand_reference_macros(block)
        block = inject_heading_ids(block, chapter)
        content_parts.append(
            replace_refs(
                remove_footnote_definitions(block),
                chapter,
                source_lookup,
                ordered_sources,
            )
        )
    canonical_content = "\n\n".join(content_parts).strip()
    canonical_content = BG.expand_visualization_macros(
        canonical_content, BG.visualization_lookup()
    )
    canonical_content = decorate_figure_references(canonical_content, set())
    contents = mini_toc(canonical_content)
    visual_files = sorted(set(IMAGE_RE.findall(canonical_content)))
    resource_map, resource_metadata = edition_resource_map(node, visual_files)

    out_dir = BUILD / node_id
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, dict] = {}
    for layout in LAYOUTS:
        outputs[layout] = {}
        for monochrome in (False, True):
            mode = "mono" if monochrome else "color"
            stem = variant_stem(node["slug"], layout, monochrome)
            markdown = build_markdown(
                node,
                canonical_content,
                ordered_sources,
                layout=layout,
                contents=contents,
                resource_map=resource_map,
            )
            markdown = BG.expand_visualization_macros(
                markdown, BG.visualization_lookup()
            )
            md_path = out_dir / f"{stem}.md"
            md_path.write_text(
                "---\n"
                f'title: "{node["id"]} — {node["title"]}"\n'
                f'version: "{VERSION}"\n'
                'lang: "en"\n'
                "---\n\n"
                + markdown,
                encoding="utf-8",
            )
            css_path = out_dir / f"{stem}.css"
            css_path.write_text(
                identity_css(node, layout=layout, monochrome=monochrome),
                encoding="utf-8",
            )
            html_path = out_dir / f"{stem}.html"
            run(
                [
                    shutil.which("pandoc") or "pandoc",
                    str(md_path),
                    "--from=markdown+yaml_metadata_block+tex_math_dollars+footnotes+fenced_divs+link_attributes",
                    "--to=html5",
                    "--standalone",
                    "--template",
                    str(SRC / "template.html"),
                    "--toc",
                    "--toc-depth=2",
                    "--mathml",
                    "--embed-resources",
                    f"--css={css_path.name}",
                    "--resource-path",
                    os.pathsep.join(
                        (str(out_dir), str(ROOT / "build"), str(SRC), str(ROOT))
                    ),
                    "--metadata",
                    f"guide-version={VERSION}",
                    "--metadata",
                    f"print-mode={mode}",
                    "--metadata",
                    f"print-layout={layout}",
                    "--metadata",
                    "home-anchor=top",
                    "--metadata",
                    f"build-revision={git_revision()}",
                    "--metadata",
                    f"build-date={build_date()}",
                    "--metadata",
                    f'subguide-title={node["id"]} — {node["title"]}',
                    "--metadata",
                    "canonical-url=https://be.fkr.dev",
                    "--output",
                    str(html_path),
                ]
            )
            pdf_path = out_dir / f"{stem}.pdf"
            run(
                [
                    "node",
                    str(ROOT / "bin" / "chrome_pdf.mjs"),
                    str(html_path),
                    str(pdf_path),
                    VERSION,
                ]
            )
            outputs[layout][mode] = {
                "html": str(html_path.relative_to(ROOT)),
                "pdf": str(pdf_path.relative_to(ROOT)),
                "pdf_pages": pdf_pages(pdf_path),
                "html_sha256": file_sha256(html_path),
                "pdf_sha256": file_sha256(pdf_path),
            }

    result = {
        "release": VERSION,
        "node": node_id,
        "slug": node["slug"],
        "canonical_content_sha256": hashlib.sha256(
            canonical_content.encode()
        ).hexdigest(),
        "source_ids": [item["id"] for item in ordered_sources],
        "source_count": len(ordered_sources),
        "canonical_visuals": visual_files,
        "canonical_visual_count": len(visual_files),
        "encapsulation": {
            "scope": node["scope"],
            "outside_scope": node["outside_scope"],
            "aliases": node["aliases"],
            **resource_metadata,
        },
        "outputs": outputs,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"  [OK] {node_id} standalone: {len(ordered_sources)} local sources, "
        f"{len(visual_files)} canonical visuals, 6 editions"
    )
    return result


def build_hub(results: dict[str, dict]) -> None:
    manifest = json.loads(
        (DATA_DIR / "subguides.json").read_text(encoding="utf-8")
    )
    cards = []
    for node in manifest["nodes"]:
        pattern_path = f'assets/patterns/{node["id"]}-{node["pattern"]}.svg'
        if node["id"] in results:
            action = (
                f'<a class="hub-open" href="{node["id"]}/{node["slug"]}.html">'
                f'Open standalone {node["id"]} →</a>'
            )
            status = "Standalone release"
        else:
            action = '<span class="hub-master">Read in the complete master guide</span>'
            status = "Master-guide node"
        cards.append(
            f'''<article class="hub-node" data-subguide="{node["id"]}">
<img class="hub-node-pattern" src="{pattern_path}" alt="{node["id"]} {node["pattern"].replace("-", " ")} identity pattern">
<div class="hub-node-heading"><span>{node["id"]}</span><h2>{node["title"]}</h2></div>
<p>{node["promise"]}</p>
<dl><div><dt>Pattern</dt><dd>{node["pattern"].replace("-", " ")}</dd></div><div><dt>Glyph</dt><dd>{node["glyph"].replace("-", " ")}</dd></div><div><dt>Status</dt><dd>{status}</dd></div></dl>
{action}
</article>'''
        )
    markdown = f'''---
title: "Bathroom Emergency Guide — Graph Hub"
version: "{VERSION}"
lang: "en"
---

::: {{#top .standalone-subguide data-subguide="O" data-pattern="dot-field"}}

::: {{.subguide-cover}}

<div class="subguide-family-mark">Bathroom Emergency Guide / v{VERSION}</div>
<div class="subguide-code">O</div>

# Graph Hub

<div class="subguide-promise">Choose one region, keep one next action, and move when the primary problem changes.</div>

:::

::: {{.emergency-gate}}

**Immediate emergency gate**

Immediate danger to life, fire, smoke, suspected carbon monoxide, severe
breathing difficulty, unconsciousness, or major bleeding goes directly to
**112**. Active violence or crime goes to a safer place and **110 / 112**.

:::

# The graph

![Bathroom Emergency Guide subguide graph overview](build/diagrams/subguide_graph_overview.png)

The image shows the orientation spine. The directory below is the complete text
fallback; each released standalone page lists all of its neighbours.

<div class="hub-directory" aria-label="Ten subguide routes">
{chr(10).join(cards)}
</div>

## Why nine nodes are detached in this release

The standalone set now covers orientation (**O**), alarm and calm (**B**), body
and first aid (**C**), threat and safe place (**D**), environmental hazards
(**H**), outage and continuity (**Z**), professional systems (**P**), writable
templates (**T**), and reference material (**R**). The set deliberately mixes
research, operational protocols, action sequences, forms, and indexes so the
build cannot quietly optimize for one content type.

Responsibility and care (**A**) continues to work inside the complete master
guide until its visual set and standalone page grammar pass the same gates.

:::
'''
    out = BUILD
    out.mkdir(parents=True, exist_ok=True)
    md_path = out / "index.md"
    md_path.write_text(markdown, encoding="utf-8")
    css_path = out / "index.css"
    css_path.write_text(
        identity_css(manifest["nodes"][0], layout="a4", monochrome=False),
        encoding="utf-8",
    )
    html_path = out / "index.html"
    run(
        [
            shutil.which("pandoc") or "pandoc",
            str(md_path),
            "--from=markdown+yaml_metadata_block+fenced_divs+link_attributes",
            "--to=html5",
            "--standalone",
            "--template",
            str(SRC / "template.html"),
            "--toc",
            "--toc-depth=2",
            "--embed-resources",
            f"--css={css_path.name}",
            "--resource-path",
            os.pathsep.join((str(out), str(ROOT / "build"), str(SRC), str(ROOT))),
            "--metadata",
            f"guide-version={VERSION}",
            "--metadata",
            "print-mode=color",
            "--metadata",
            "print-layout=a4",
            "--metadata",
            "home-anchor=top",
            "--output",
            str(html_path),
        ]
    )
    hub_manifest = {
        "release": VERSION,
        "standalone_nodes": sorted(results),
        "master_only_nodes": [
            node["id"] for node in manifest["nodes"] if node["id"] not in results
        ],
        "html": str(html_path.relative_to(ROOT)),
        "html_sha256": file_sha256(html_path),
    }
    (out / "manifest.json").write_text(
        json.dumps(hub_manifest, indent=2) + "\n", encoding="utf-8"
    )
    print("  [OK] graph hub → build/subguides/index.html")


def main() -> int:
    parser = argparse.ArgumentParser()
    manifest = json.loads((DATA_DIR / "subguides.json").read_text(encoding="utf-8"))
    released = manifest["standalone_nodes"]
    parser.add_argument("--node", choices=[*released, "all"], default="all")
    args = parser.parse_args()
    node_ids = released if args.node == "all" else [args.node]
    results = {node_id: build_node(node_id) for node_id in node_ids}
    if args.node == "all":
        build_hub(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
