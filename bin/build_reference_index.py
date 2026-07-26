#!/usr/bin/env python3
"""Build stable public references and generated appendix/index fragments."""
from __future__ import annotations

import argparse
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
    records: list[dict] = []
    matched_forms: set[str] = set()

    for section in sections:
        form = form_by_title.get(section["heading"])
        if section["chapter"] == "07a-templates.md" and form:
            resource_key = f"form:{form['key']}"
            kind = "F"
            matched_forms.add(form["key"])
        else:
            resource_key = f"section:{section['key']}"
            kind = "S"
        records.append({
            "resource_key": resource_key,
            "owner": section["owner"],
            "kind": kind,
            "title": section["heading"],
            "chapter": section["chapter"],
            "line": section["line"],
            "level": section["level"],
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
        "diagram-index.md": "## Diagram, chart, map, and figure index\n\n" + table(
            ["Stable reference", "Guide", "Resource", "Reader question", "File"],
            [[i["public_ref"], i["owner"], i["title"], i.get("question", "—"), i.get("file", "—")] for i in diagrams],
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
            ["Stable reference", "Template", "Canonical chapter"],
            [[i["public_ref"], i["title"], i.get("chapter", "07a-templates.md")] for i in forms],
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
    lookup = {
        item["title"]: item["html_id"]
        for item in load_index()["records"]
        if item.get("chapter") == chapter and item["kind"] in {"S", "F"}
    }
    lines = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match and match.group(2) in lookup and "{#" not in line:
            line = f"{match.group(1)} {match.group(2)} {{#{lookup[match.group(2)]}}}"
        lines.append(line)
    return "\n".join(lines)


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
