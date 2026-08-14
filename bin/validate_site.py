#!/usr/bin/env python3
"""Validate the self-contained landing, deployment, download, and Pages contract."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from project_meta import VERSION

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "build" / "site"
DEPLOYMENT = ROOT / "DEPLOYMENT.md"
SUBGUIDES = ROOT / "src" / "data" / "subguides.json"
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.stable_links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "a" and values.get("data-reference") and values.get("href"):
            self.stable_links.append((values["data-reference"], values["href"]))
        for attr in ("href", "src"):
            value = values.get(attr)
            if value:
                self.references.append((attr, value))


def local_target(page: Path, reference: str) -> Path | None:
    if reference.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    target = (page.parent / path).resolve()
    if path.endswith("/"):
        target = target / "index.html"
    return target


def packaged_target(page: Path, reference: str) -> tuple[Path, str] | None:
    """Resolve local and canonical be.fkr.dev links into the Pages package."""
    if reference.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"http", "https"} or parsed.netloc != "be.fkr.dev":
            return None
        target = (SITE / unquote(parsed.path).lstrip("/")).resolve()
    elif parsed.path:
        target = (page.parent / unquote(parsed.path)).resolve()
    else:
        target = page.resolve()
    if parsed.path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target, unquote(parsed.fragment)


core_pages = {
    "landing": SITE / "index.html",
    "deployment": SITE / "deploy" / "index.html",
    "downloads": SITE / "downloads" / "index.html",
    "not-found": SITE / "404.html",
}
for label, page in core_pages.items():
    check(page.exists() and page.stat().st_size > 0, f"{label} page missing or empty")

for path in (
    SITE / ".nojekyll",
    SITE / "assets" / "site.css",
    SITE / "assets" / "site.js",
    SITE / "assets" / "mark.svg",
    SITE / "site.webmanifest",
    SITE / "robots.txt",
    SITE / "guide" / "index.html",
    SITE / "guide" / "guide.css",
    SITE / "routes" / "index.html",
    SITE / "files" / "guide.pdf",
    SITE / "files" / "guide_mono.pdf",
    SITE / "files" / "guide_a4half.pdf",
    SITE / "files" / "guide_a4half_mono.pdf",
    SITE / "files" / "guide_largeprint.pdf",
    SITE / "files" / "guide_largeprint_mono.pdf",
    SITE / "files" / "all-subguides_booklet-print.pdf",
    SITE / "files" / "all-subguides_booklet-print_mono.pdf",
    SITE / "routes" / "SHELF" / "shelf-how-to-use_a4half_booklet.pdf",
    SITE / "routes" / "SHELF" / "shelf-how-to-use_a4half_mono_booklet.pdf",
    SITE / "docs" / "README.md",
    SITE / "docs" / "DEPLOYMENT.md",
    SITE / "docs" / "PRINTING.md",
    SITE / "docs" / "CHANGELOG.md",
    SITE / "meta" / "release.json",
):
    check(path.exists(), f"Pages package artifact missing: {path.relative_to(ROOT)}")

landing_markers = (
    f"Release {VERSION}",
    "Useful before heroic.",
    "Choose your next move.",
    "A shelf, not a diagnostic maze.",
    "A PDF on a shelf is not resilience.",
    "The source trail stays attached.",
    "data-theme-toggle",
    "No tracking",
    "href=\"guide/\"",
    "href=\"files/guide.pdf\"",
    "Latest A4 PDF",
    "href=\"routes/\"",
    "href=\"downloads/\"",
    "href=\"deploy/\"",
    "bathroom_emergency@fkr.dev",
    "Open feedback template",
    "figures, including local references",
)
deployment_markers = (
    "Minimum viable deployment",
    "data-deployment-planner",
    "Local-only by design",
    "Classify before you print.",
    "data-copy-plan",
    "data-reset-plan",
    "../files/guide.pdf",
    "../docs/DEPLOYMENT.md",
)
download_markers = (
    f"Release {VERSION} download catalogue",
    "Master editions",
    "The eleven individual books",
    "Source, evidence, and maintenance",
    "data-download-filter=\"master\"",
    "../files/guide.pdf",
    "../files/all-subguides_booklet-print.pdf",
    "../files/all-subguides_booklet-print_mono.pdf",
    "../routes/SHELF/shelf-how-to-use_a4half_booklet.pdf",
    "../routes/SHELF/shelf-how-to-use_a4half_mono_booklet.pdf",
    "../docs/PRINTING.md",
    "../routes/O/green-book-body-owners-manual.pdf",
    "../routes/A/amber-book-responsibility.pdf",
    "../routes/B/teal-book-calm-guide.pdf",
    "../routes/C/red-book-self-ambulance.pdf",
    "../routes/D/blue-book-safety-no-place.pdf",
    "../routes/H/orange-book-hazards-disasters.pdf",
    "../routes/Z/olive-book-zombie-guide.pdf",
    "../routes/P/indigo-book-professional-support.pdf",
    "../routes/S/purple-book-social-field-guide.pdf",
    "../routes/T/grey-book-templates-forms.pdf",
    "../routes/R/copper-book-reference.pdf",
    "../routes/T/grey-book-templates-forms.html#beg-t-f-005",
    "Feedback template",
    "../meta/release.json",
)
for page, markers in (
    (core_pages["landing"], landing_markers),
    (core_pages["deployment"], deployment_markers),
    (core_pages["downloads"], download_markers),
):
    if not page.exists():
        continue
    text = page.read_text(encoding="utf-8")
    for marker in markers:
        check(marker in text, f"{page.relative_to(ROOT)} marker missing: {marker}")
    check("<main id=\"main\">" in text, f"{page.relative_to(ROOT)} lacks main landmark")
    check("class=\"skip-link\"" in text, f"{page.relative_to(ROOT)} lacks skip link")
    check("aria-label=\"Primary\"" in text, f"{page.relative_to(ROOT)} lacks primary navigation label")

guide_page = SITE / "guide" / "index.html"
if guide_page.exists():
    guide_text = guide_page.read_text(encoding="utf-8")
    for marker in (
        '<link rel="canonical" href="https://be.fkr.dev/guide/">',
        "Online edition",
        '<span class="brand-guide">BE</span>',
        'class="reader-provenance"',
        'class="repository-link"',
        'class="reader-links"',
        'href="https://be.fkr.dev/"',
        'href="https://be.fkr.dev/files/guide.pdf"',
        "Latest PDF",
        "aria-current",
        'data-reader-toc',
        'is-current-book',
        'requestAnimationFrame(updateActiveToc)',
        '<span class="brand-guide">BE</span>',
        'class="reader-provenance"',
        'https://github.com/fkr-0/bathroom-emergency',
    ):
        check(marker in guide_text, f"guide reader marker missing: {marker}")
    book_ids = re.findall(r'id="(book-[a-z]+)" class="standalone-subguide"', guide_text)
    check(len(book_ids) == 12, f"guide reader expected 12 top-level book anchors, found {len(book_ids)}")
    check(len(set(book_ids)) == 12, "guide reader top-level book anchors are not unique")
    check("book-shelf" in book_ids, "guide reader lacks the Shelf top-level anchor")

landing_text = core_pages["landing"].read_text(encoding="utf-8") if core_pages["landing"].exists() else ""
check('href="tel:112"' in landing_text, "landing emergency strip lacks 112")
check('href="tel:110"' not in landing_text, "landing emergency strip still exposes Germany-only 110")
check("Use the local emergency number" in landing_text, "landing emergency strip lacks local-number-first wording")
check("In the EU, call" in landing_text, "landing emergency strip lacks bounded 112 context")

deployment_text = core_pages["deployment"].read_text(encoding="utf-8") if core_pages["deployment"].exists() else ""
check("GitHub Pages deployment is prepared" not in deployment_text, "deployment page still exposes repository publication instructions")

route_page = SITE / "routes" / "O" / "green-book-body-owners-manual.html"
if route_page.exists():
    route_text = route_page.read_text(encoding="utf-8")
    for marker in (
        '<link rel="canonical" href="https://be.fkr.dev/routes/O/green-book-body-owners-manual.html">',
        'href="https://be.fkr.dev/routes/O/green-book-body-owners-manual.pdf"',
        "Online edition",
    ):
        check(marker in route_text, f"standalone reader marker missing: {marker}")
    check('href="data:text/html' not in route_text, "standalone canonical metadata was embedded as a data URI")

check('href="data:text/html' not in guide_text if guide_page.exists() else True, "guide canonical metadata was embedded as a data URI")

# Core pages must be internally navigable without network assets.
for label, page in core_pages.items():
    if not page.exists():
        continue
    parser = LinkParser()
    parser.feed(page.read_text(encoding="utf-8"))
    for attr, reference in parser.references:
        target = local_target(page, reference)
        if target is None:
            continue
        check(
            target == SITE or SITE in target.parents,
            f"{label} {attr} escapes Pages package: {reference}",
        )
        check(target.exists(), f"{label} broken local {attr}: {reference}")

# Stable hardlinks are a release contract, not a sample check. Every active
# public reference must have exactly one canonical #BEG:... target in the
# complete online guide, at least one permalink, and every rendered stable link
# in every HTML edition must resolve either locally or into that canonical guide.
content_index_path = ROOT / "src" / "data" / "content_index.json"
if guide_page.exists() and content_index_path.exists():
    records = json.loads(content_index_path.read_text(encoding="utf-8"))["records"]
    guide_parser = LinkParser()
    guide_parser.feed(guide_page.read_text(encoding="utf-8"))
    guide_ids = {value: guide_parser.ids.count(value) for value in set(guide_parser.ids)}
    linked_fragments = [urlsplit(href).fragment for _, href in guide_parser.stable_links]
    for item in records:
        fragment = item.get("fragment_id") or item["public_ref"][1:-1]
        check(
            guide_ids.get(fragment, 0) == 1,
            f"{item['public_ref']}: Pages guide expected exactly one #{fragment} target, found {guide_ids.get(fragment, 0)}",
        )
        check(
            fragment in linked_fragments,
            f"{item['public_ref']}: Pages guide has no stable permalink to #{fragment}",
        )

    parsed_cache: dict[Path, set[str]] = {guide_page.resolve(): set(guide_parser.ids)}
    for page in sorted(SITE.rglob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed_cache[page.resolve()] = set(parser.ids)
        for public_ref, href in parser.stable_links:
            resolved = packaged_target(page, href)
            check(resolved is not None, f"{page.relative_to(SITE)} {public_ref}: stable link escapes the canonical site: {href}")
            if resolved is None:
                continue
            target, fragment = resolved
            check(target.exists(), f"{page.relative_to(SITE)} {public_ref}: stable link target missing: {href}")
            if not target.exists() or not fragment or target.suffix.lower() != ".html":
                continue
            if target.resolve() not in parsed_cache:
                target_parser = LinkParser()
                target_parser.feed(target.read_text(encoding="utf-8"))
                parsed_cache[target.resolve()] = set(target_parser.ids)
            check(
                fragment in parsed_cache[target.resolve()],
                f"{page.relative_to(SITE)} {public_ref}: fragment #{fragment} does not resolve in {target.relative_to(SITE)}",
            )

if SUBGUIDES.exists():
    subguides = json.loads(SUBGUIDES.read_text(encoding="utf-8"))
    by_id = {node["id"]: node for node in subguides["nodes"]}
    downloads_text = (
        core_pages["downloads"].read_text(encoding="utf-8")
        if core_pages["downloads"].exists()
        else ""
    )
    for node_id in subguides["standalone_nodes"]:
        node = by_id[node_id]
        base = SITE / "routes" / node_id
        for suffix in (".html", ".pdf", "_a4half.pdf", "_largeprint.pdf"):
            check(
                (base / f'{node["slug"]}{suffix}').exists(),
                f"Pages package missing {node_id} route artifact: {node['slug']}{suffix}",
            )
        for suffix in ("_a4half_booklet.pdf", "_a4half_mono_booklet.pdf"):
            filename = f'{node["slug"]}{suffix}'
            check(
                (base / filename).exists(),
                f"Pages package missing {node_id} booklet artifact: {filename}",
            )
            check(
                f'../routes/{node_id}/{filename}' in downloads_text,
                f"Downloads page missing {node_id} booklet link: {filename}",
            )

meta_path = SITE / "meta" / "release.json"
if meta_path.exists():
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    reference_registry = json.loads(
        (ROOT / "src" / "data" / "reference_ids.json").read_text(encoding="utf-8")
    )
    expected_active_references = len(reference_registry.get("ids", {})) - len(
        reference_registry.get("retired_resource_keys", [])
    )
    check(meta.get("release") == VERSION, "site release metadata version drifted")
    check(meta.get("published_by_this_build") is False, "site metadata falsely claims publication")
    check(meta.get("deployment_performed_by_this_build") is False, "site metadata falsely claims deployment")
    metrics = meta.get("metrics", {})
    check(metrics.get("chapters") == 17, "site chapter metric drifted")
    check(metrics.get("standalone") == 11, "site standalone metric drifted")
    check(
        metrics.get("references") == expected_active_references,
        "site active stable-reference metric drifted",
    )
    check(metrics.get("figures") == 49, "site public figure metric drifted")
    check(metrics.get("authored_visuals") == 41, "site authored-visual metric drifted")
    check(metrics.get("standalone_pdf_editions") == 66, "site standalone PDF metric drifted")
    check(metrics.get("folded_booklet_editions") == 24, "site folded-booklet metric drifted")

check(
    not list((SITE / "routes" / "T").glob("templates-blue-book*")),
    "Pages package retained obsolete templates-blue-book output aliases",
)

css = SITE / "assets" / "site.css"
js = SITE / "assets" / "site.js"
if css.exists():
    text = css.read_text(encoding="utf-8")
    for marker in ("prefers-reduced-motion", "prefers-color-scheme", "@media print", ".route-grid", ".planner-layout", ":focus-visible"):
        check(marker in text, f"site stylesheet marker missing: {marker}")

for label, page in core_pages.items():
    if not page.exists():
        continue
    text = page.read_text(encoding="utf-8")
    for marker in (
        'class="site-provenance"',
        'class="repository-link"',
        f"/tree/v{VERSION}",
        "/commit/",
        "meta/release.json",
        "https://github.com/fkr-0/bathroom-emergency",
    ):
        check(marker in text, f"{label} header provenance marker missing: {marker}")
if js.exists():
    text = js.read_text(encoding="utf-8")
    for marker in ("localStorage", "data-deployment-planner", "data-download-filter", "navigator.clipboard"):
        check(marker in text, f"site script marker missing: {marker}")
    check("fetch(" not in text and "XMLHttpRequest" not in text, "site script introduces a network request")

check(DEPLOYMENT.exists(), "deployment instructions missing")
if DEPLOYMENT.exists():
    text = DEPLOYMENT.read_text(encoding="utf-8").lower()
    for marker in (
        "minimum viable deployment",
        "canonical deployment-field index",
        "object- and person-specific safe places",
        "physical installation concepts",
        "additional deployables",
        "build from source",
        "maintenance cycle",
        "privacy",
        "bathroom_emergency@fkr.dev",
    ):
        check(marker in text, f"deployment marker missing: {marker}")

if errors:
    raise SystemExit("Landing/deployment validation failed:\n- " + "\n- ".join(errors))
print(
    "Landing/deployment validation passed: responsive project, deployment, "
    "downloads, guide, route, offline-asset, privacy, and Pages-package contracts are present."
)
