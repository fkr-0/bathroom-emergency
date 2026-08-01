#!/usr/bin/env python3
"""Build stable public references and generated appendix/index fragments."""
from __future__ import annotations

import argparse
import html
import json
import re
from collections import defaultdict
from pathlib import Path

from project_meta import VERSION

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data"
GENERATED = ROOT / "build" / "generated"
REGISTRY_PATH = DATA / "reference_ids.json"
INDEX_PATH = DATA / "content_index.json"
REF_RE = re.compile(r"^\[BEG:([A-Z]):([A-Z]):(\d{3})\]$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+\{#[-a-z0-9]+\})?\s*$")

# Public references name resources, not wording. When an existing section gets
# a clearer heading, retain its original resource key so the stable address and
# inbound links survive the edit.
SECTION_RESOURCE_KEY_ALIASES = {
    ("07-professional-support.md", "Pair support with a maintained Blue Book page"):
        "section:07-professional-support:fill-these-before-deployment",
    ("08-appendix.md", "Master cross-reference — where problems, routes, forms, and support meet"):
        "section:08-appendix:master-cross-reference-where-everything-points",
    ("08-appendix.md", "Eight situation doors inside ten route identities"):
        "section:08-appendix:the-eight-entry-points",
    ("08-appendix.md", "Illustration cross-reference — what travels with a figure"):
        "section:08-appendix:diagram-index",
    ("08-appendix.md", "Fillable fields live in T — Templates"):
        "section:08-appendix:fillable-fields",
}


def slugify(value: str) -> str:
    value = value.lower().replace("–", "-").replace("—", "-")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def load_json(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def resources() -> list[dict]:
    sections = load_json("section_ownership.json")["sections"]
    figures = load_json("figure_inventory.json")["figures"]
    forms = load_json("forms.json")["forms"]
    deployment = load_json("deployment_fields.json")["fields"]
    glossary = load_json("glossary.json")["terms"]
    locale = load_json("locales/de-DE.json")
    form_by_title = {item["title"]: item for item in forms}
    related_forms_by_figure: dict[str, list[str]] = defaultdict(list)
    for form in forms:
        for figure_id in form.get("figure_ids", []):
            related_forms_by_figure[figure_id].append(form["key"])
    records: list[dict] = []
    matched_forms: set[str] = set()

    for section in sections:
        form = form_by_title.get(section["heading"])
        if section["chapter"] == "07a-templates.md" and form:
            resource_key = f"form:{form['key']}"
            kind = "F"
            matched_forms.add(form["key"])
        else:
            resource_key = SECTION_RESOURCE_KEY_ALIASES.get(
                (section["chapter"], section["heading"]),
                f"section:{section['key']}",
            )
            kind = "S"
        records.append({
            "resource_key": resource_key,
            "owner": section["owner"],
            "kind": kind,
            "title": section["heading"],
            "chapter": section["chapter"],
            "line": section["line"],
            "level": section["level"],
            **({
                "purpose": form["purpose"],
                "responsibility": form["responsibility"],
                "privacy": form["privacy"],
                "routes": form.get("routes", ["T"]),
                "figure_ids": form.get("figure_ids", []),
                "support_keys": form.get("support_keys", []),
            } if form else {}),
        })

    for form in forms:
        if form["key"] in matched_forms:
            continue
        records.append({
            "resource_key": f"form:{form['key']}",
            "owner": "T",
            "kind": "F",
            "title": form["title"],
            "purpose": form["purpose"],
            "responsibility": form["responsibility"],
            "privacy": form["privacy"],
            "routes": form.get("routes", ["T"]),
            "figure_ids": form.get("figure_ids", []),
            "support_keys": form.get("support_keys", []),
        })

    for figure in figures:
        if not figure.get("reader_facing", True):
            continue
        records.append({
            "resource_key": f"figure:{figure['id']}",
            "owner": figure["owner"],
            "kind": "G",
            "title": figure["id"].replace("_", " "),
            "file": figure["file"],
            "question": figure["question"],
            "source_basis": figure["source_basis"],
            "chapters": figure.get("chapters", []),
            "secondary_subguides": figure.get("secondary_subguides", []),
            "related_form_keys": sorted(related_forms_by_figure.get(figure["id"], [])),
        })

    for field in deployment:
        records.append({
            "resource_key": f"deployment:{field['key']}",
            "owner": "T",
            "kind": "D",
            "title": field["label"],
            "group": field["group"],
            "required": field["required"],
            "privacy": field["privacy"],
            "example": field["example"],
        })

    for term in glossary:
        records.append({
            "resource_key": f"glossary:{term['key']}",
            "owner": "R",
            "kind": "W",
            "title": term["term"],
            "definition": term["definition"],
        })

    for key, service in locale["services"].items():
        records.append({
            "resource_key": f"contact:service:{key}",
            "owner": "P",
            "kind": "C",
            "title": service["label"],
            "service_key": key,
            "number": service.get("number") or "local value required",
            "scope": service["scope"],
            "availability": "24/7" if service.get("always_available") else service.get("availability", "verify locally"),
        })
    for centre in locale["poison_centres"]:
        records.append({
            "resource_key": f"contact:poison:{slugify(centre['city'])}",
            "owner": "P",
            "kind": "C",
            "title": f"Poison information centre — {centre['city']}",
            "number": centre["number"],
            "scope": "Poisoning advice; severe symptoms or immediate danger remain 112.",
            "availability": "verify current service details",
        })

    seen: set[str] = set()
    for record in records:
        key = record["resource_key"]
        if key in seen:
            raise ValueError(f"duplicate reference resource key: {key}")
        seen.add(key)
    return records


def assign(records: list[dict]) -> tuple[dict, list[dict]]:
    old = {}
    if REGISTRY_PATH.exists():
        old = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")).get("ids", {})
    counters: dict[tuple[str, str], int] = defaultdict(int)
    for ref in old.values():
        match = REF_RE.match(ref)
        if match:
            counters[(match.group(1), match.group(2))] = max(
                counters[(match.group(1), match.group(2))], int(match.group(3))
            )
    ids = dict(old)
    for record in sorted(records, key=lambda item: (item["owner"], item["kind"], item["resource_key"])):
        key = record["resource_key"]
        if key not in ids:
            pair = (record["owner"], record["kind"])
            counters[pair] += 1
            ids[key] = f"[BEG:{pair[0]}:{pair[1]}:{counters[pair]:03d}]"
    current_keys = {item["resource_key"] for item in records}
    retired = sorted(set(ids) - current_keys)
    enriched = []
    for record in records:
        item = dict(record)
        item["public_ref"] = ids[record["resource_key"]]
        match = REF_RE.match(item["public_ref"])
        assert match
        item["html_id"] = f"beg-{match.group(1).lower()}-{match.group(2).lower()}-{match.group(3)}"
        enriched.append(item)
    registry = {
        "schema_version": 1,
        "release": VERSION,
        "status": "stable-public-reference-registry",
        "format": "[BEG:<owner>:<kind>:<sequence>]",
        "kind_legend": {
            "S": "section",
            "F": "form or detachable template",
            "G": "figure, chart, map, or diagram",
            "C": "professional contact or service",
            "D": "deployment field",
            "W": "glossary word or term",
        },
        "ids": dict(sorted(ids.items())),
        "retired_resource_keys": retired,
    }
    return registry, enriched


def table(headers: list[str], rows: list[list[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    rule = "|" + "|".join("---" for _ in headers) + "|"
    body = ["| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |" for row in rows]
    return "\n".join([head, rule, *body])


def generated_fragments(records: list[dict]) -> dict[str, str]:
    records = sorted(records, key=lambda item: item["public_ref"])
    nodes = {
        item["id"]: item for item in load_json("subguides.json")["nodes"]
    }
    by_key = {item["resource_key"]: item for item in records}

    def route_identity(route: str) -> str:
        node = nodes[route]
        return (
            f"**{route} — {node['title']}** · {node['pattern'].replace('-', ' ')} · "
            f"{node['glyph'].replace('-', ' ')}"
        )

    def route_list(routes: list[str]) -> str:
        return "<br>".join(route_identity(route) for route in routes) or "—"

    def related_figure_list(figure_ids: list[str]) -> str:
        values = []
        for figure_id in figure_ids:
            item = by_key.get(f"figure:{figure_id}")
            if item:
                values.append(f"{item['public_ref']} {item['title']}")
        return "<br>".join(values) or "—"

    def related_form_list(form_keys: list[str]) -> str:
        values = []
        for form_key in form_keys:
            item = by_key.get(f"form:{form_key}")
            if item:
                values.append(f"{item['public_ref']} {item['title']}")
        return "<br>".join(values) or "—"

    def related_support_list(support_keys: list[str]) -> str:
        values = []
        for support_key in support_keys:
            item = by_key.get(f"contact:service:{support_key}")
            if item:
                values.append(f"{item['public_ref']} {item['title']}")
        return "<br>".join(values) or "—"

    content_rows = [
        [item["public_ref"], item["kind"], item["owner"], item["title"], item.get("chapter", "—")]
        for item in records
    ]
    diagrams = [item for item in records if item["kind"] == "G"]
    contacts = [item for item in records if item["kind"] == "C"]
    fields = [item for item in records if item["kind"] == "D"]
    words = [item for item in records if item["kind"] == "W"]
    forms = [item for item in records if item["kind"] == "F"]
    return {
        "global-content-index.md": "## Global content index\n\n" + table(
            ["Stable reference", "Kind", "Guide", "Resource", "Canonical source"], content_rows
        ) + "\n",
        "diagram-index.md": "## Illustration cross-reference — figures, routes, and forms\n\n"
        "Every figure keeps a stable address. Colour is supplementary: the route code, "
        "pattern name, and glyph name identify the same family in monochrome, speech, and "
        "low-colour printing.\n\n" + table(
            ["Stable reference", "Route identity", "Resource", "Reader question", "Paired forms"],
            [[
                i["public_ref"],
                route_identity(i["owner"]),
                i["title"],
                i.get("question", "—"),
                related_form_list(i.get("related_form_keys", [])),
            ] for i in diagrams],
        ) + "\n",
        "contact-index.md": "## Professional contact and service index\n\n" + table(
            ["Stable reference", "Service", "Number / local field", "Purpose", "Availability"],
            [[i["public_ref"], i["title"], i.get("number", "—"), i.get("scope", "—"), i.get("availability", "—")] for i in contacts],
        ) + "\n",
        "deployment-index.md": "## Deployment customization index\n\n" + table(
            ["Stable reference", "Group", "Field", "Required", "Privacy", "Example"],
            [[i["public_ref"], i.get("group", "—"), i["title"], "yes" if i.get("required") else "when relevant", i.get("privacy", "—"), i.get("example", "—")] for i in fields],
        ) + "\n",
        "glossary-index.md": "## Glossary\n\n" + "\n\n".join(
            f"### {i['title']} {{#{i['html_id']}}}\n\n**{i['public_ref']}** — {i['definition']}" for i in words
        ) + "\n",
        "form-index.md": "## Detachable form index\n\n" + table(
            ["Stable reference", "Template", "Route identities", "Related figures", "Support routes", "Privacy"],
            [[
                i["public_ref"],
                i["title"],
                route_list(i.get("routes", ["T"])),
                related_figure_list(i.get("figure_ids", [])),
                related_support_list(i.get("support_keys", [])),
                i.get("privacy", "—"),
            ] for i in forms],
        ) + "\n",
        "route-identity-index.md": "## Route identity key — code, colour, pattern, and glyph\n\n"
        "Use the code and title first. Colour accelerates scanning; the printed pattern and "
        "written glyph name carry the identity when colour is unavailable.\n\n" + table(
            ["Route", "Pattern", "Glyph", "Scope", "Deliberate boundary"],
            [[
                f"**{node_id} — {node['title']}**",
                node["pattern"].replace("-", " "),
                node["glyph"].replace("-", " "),
                node["scope"],
                node["outside_scope"],
            ] for node_id, node in nodes.items()],
        ) + "\n",
        "support-form-map.md": "## Support handoff map — service, form, figure, and route\n\n"
        "A telephone number or directory result is not yet a handoff. Pair the service with "
        "the form that carries location, access, current state, requested outcome, backup, "
        "and review time.\n\n" + table(
            ["Support or service", "Use these forms", "Related figures", "Route identities"],
            [[
                related_support_list(form.get("support_keys", [])),
                f"{form['public_ref']} {form['title']}",
                related_figure_list(form.get("figure_ids", [])),
                route_list(form.get("routes", ["P", "T"])),
            ] for form in forms if form.get("support_keys")],
        ) + "\n",
    }


def render(check: bool = False) -> None:
    registry, records = assign(resources())
    index = {
        "schema_version": 1,
        "release": VERSION,
        "status": "global-content-index",
        "reference_scheme": "stable typed IDs; page and hierarchical numbers are non-canonical navigation aids",
        "records": sorted(records, key=lambda item: item["public_ref"]),
    }
    outputs: dict[Path, str] = {
        REGISTRY_PATH: json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        INDEX_PATH: json.dumps(index, indent=2, ensure_ascii=False) + "\n",
    }
    GENERATED.mkdir(parents=True, exist_ok=True)
    for name, content in generated_fragments(records).items():
        outputs[GENERATED / name] = content
    stale = []
    for path, content in outputs.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Reference outputs are stale:\n- " + "\n- ".join(stale))
    if not check:
        print(f"  [OK] stable reference index: {len(records)} active resources, {len(registry['retired_resource_keys'])} retired keys")


def load_index() -> dict:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def inject_heading_ids(text: str, chapter: str) -> str:
    if not INDEX_PATH.exists():
        return text
    index_records = load_index()["records"]
    lookup = {
        item["title"]: item
        for item in index_records
        if item.get("chapter") == chapter and item["kind"] in {"S", "F"}
    }
    nodes = {
        item["id"]: item for item in load_json("subguides.json")["nodes"]
    }

    def route_chip(route: str) -> str:
        node = nodes[route]
        return (
            f'<span class="route-chip" data-subguide="{route}">'
            f'<strong>{route}</strong><span>{html.escape(node["title"])}</span>'
            f'<small>{html.escape(node["pattern"].replace("-", " "))}</small></span>'
        )

    by_resource = {item["resource_key"]: item for item in index_records}
    form_records = {
        item["resource_key"].split(":", 1)[1]: item
        for item in index_records if item.get("kind") == "F"
    }
    form_by_heading = (
        {
            form.get("heading", form["title"]): form_records.get(form["key"])
            for form in load_json("forms.json")["forms"]
        }
        if chapter == "07a-templates.md"
        else {}
    )

    def form_band(item: dict) -> str:
        routes = "".join(route_chip(route) for route in item.get("routes", ["T"]))
        figures = [
            by_resource.get(f"figure:{figure_id}")
            for figure_id in item.get("figure_ids", [])
        ]
        supports = [
            by_resource.get(f"contact:service:{support_key}")
            for support_key in item.get("support_keys", [])
        ]
        figure_text = ", ".join(
            f"{figure['public_ref']} {figure['title']}" for figure in figures if figure
        ) or "none required"
        support_text = ", ".join(
            f"{support['public_ref']} {support['title']}" for support in supports if support
        ) or "local route as applicable"
        return "\n".join((
            f'<div class="template-route-band" data-template-ref="{item["public_ref"]}">',
            '<div class="template-route-head">'
            f'<strong>{item["public_ref"]}</strong>'
            f'<span>{html.escape(item.get("privacy", "review locally"))}</span></div>',
            f'<div class="route-chip-row" aria-label="Routes using this form">{routes}</div>',
            '<div class="template-crossrefs">'
            f'<span><strong>Figures:</strong> {html.escape(figure_text)}</span>'
            f'<span><strong>Support:</strong> {html.escape(support_text)}</span></div>',
            '</div>',
        ))

    lines = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        item = lookup.get(match.group(2)) if match else None
        form_item = form_by_heading.get(match.group(2)) if match else None
        if item and "{#" not in line:
            line = f"{match.group(1)} {match.group(2)} {{#{item['html_id']}}}"
        lines.append(line)
        if form_item:
            lines.extend(("", form_band(form_item), ""))
    return "\n".join(lines)


def decorate_figure_references(text: str, seen: set[str] | None = None) -> str:
    """Add stable route/form metadata after canonical figure occurrences."""
    seen = seen if seen is not None else set()
    records = load_index()["records"] if INDEX_PATH.exists() else []
    figures = {
        item.get("file"): item for item in records if item.get("kind") == "G"
    }
    forms = [item for item in records if item.get("kind") == "F"]
    nodes = {
        item["id"]: item for item in load_json("subguides.json")["nodes"]
    }
    pattern = re.compile(r"^!\[([^\]]*)\]\((build/diagrams/[^)]+)\)\s*$", re.MULTILINE)

    def replace(match: re.Match[str]) -> str:
        item = figures.get(match.group(2))
        if not item:
            return match.group(0)
        figure_id = item["resource_key"].split(":", 1)[1]
        paired = [form for form in forms if figure_id in form.get("figure_ids", [])]
        paired_text = ", ".join(
            f"{form['public_ref']} {form['title']}" for form in paired
        ) or "no dedicated form"
        node = nodes[item["owner"]]
        anchor = ""
        if item["public_ref"] not in seen:
            anchor = f' id="{item["html_id"]}"'
            seen.add(item["public_ref"])
        card = (
            f'<div{anchor} class="figure-reference" data-subguide="{item["owner"]}">'
            f'<span class="figure-reference-code">{item["public_ref"]}</span>'
            f'<span><strong>{item["owner"]} — {html.escape(node["title"])}</strong> · '
            f'{html.escape(node["pattern"].replace("-", " "))} · '
            f'{html.escape(node["glyph"].replace("-", " "))}</span>'
            f'<span><strong>Reader question:</strong> {html.escape(item.get("question", "—"))}</span>'
            f'<span><strong>Paired forms:</strong> {html.escape(paired_text)}</span>'
            '</div>'
        )
        return match.group(0) + "\n\n" + card

    return pattern.sub(replace, text)


def mini_toc(text: str, max_level: int = 2) -> str:
    rows = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match or len(match.group(1)) > max_level:
            continue
        id_match = re.search(r"\{#([-a-z0-9]+)\}\s*$", line)
        if not id_match:
            continue
        title = re.sub(r"\s+\{#[-a-z0-9]+\}\s*$", "", match.group(2))
        indent = "  " * (len(match.group(1)) - 1)
        rows.append(f"{indent}- [{title}](#{id_match.group(1)})")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    render(check=args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
