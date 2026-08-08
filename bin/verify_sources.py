#!/usr/bin/env python3
"""Check that every cited source still resolves.

Step 7 of the release policy in SOURCES.md. Run it before a release, or when a
reader review adds citations: a source list is only worth having if the links
are real, and the point of the exercise is that a future audit can follow the
links and check whether the action cards changed.

Not part of `npm test`, because it needs the network and a validator that fails
when a ministry reorganises its website is a validator people learn to ignore.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src_layout import all_chapter_paths  # noqa: E402

DEFINITION = re.compile(r"^\[\^([a-z0-9-]+)\]:(.*)$", re.MULTILINE)
URL = re.compile(r"https?://[^\s)\]]+")
AGENT = "Mozilla/5.0 (bathroom-emergency-guide source review)"


def cited_urls() -> dict[str, list[str]]:
    found: dict[str, list[str]] = defaultdict(list)
    for path in all_chapter_paths():
        for match in DEFINITION.finditer(path.read_text(encoding="utf-8")):
            for url in URL.findall(match.group(2)):
                found[url.rstrip(".,;")].append(f"{path.name}:{match.group(1)}")
    return found


def check_doi(url: str) -> tuple[bool, str]:
    """A DOI is sound when it is registered, not when its landing page loads.

    Publishers routinely answer a non-browser request with 403, which says
    nothing about whether the reference is good.
    """
    doi = urllib.parse.urlparse(url).path.lstrip("/")
    result = subprocess.run(
        ["curl", "-sS", "--max-time", "20", f"https://doi.org/api/handles/{doi}"],
        capture_output=True, text=True,
    )
    try:
        code = json.loads(result.stdout).get("responseCode")
    except json.JSONDecodeError:
        return False, "handle lookup returned no JSON"
    return code == 1, f"handle responseCode={code}"


def check_http(url: str) -> tuple[bool, str]:
    result = subprocess.run(
        ["curl", "-sSL", "-o", "/dev/null", "-w", "%{http_code}",
         "--max-time", "25", "-A", AGENT, url],
        capture_output=True, text=True,
    )
    code = result.stdout.strip() or "no response"
    return code.startswith(("2", "3")), f"HTTP {code}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true", help="only report failures")
    args = parser.parse_args()

    urls = cited_urls()
    failures: list[tuple[str, str, list[str]]] = []
    for url, uses in sorted(urls.items()):
        ok, detail = check_doi(url) if "doi.org/" in url else check_http(url)
        if not ok:
            failures.append((url, detail, uses))
        elif not args.quiet:
            print(f"  ok    {detail:<24} {url}")

    for url, detail, uses in failures:
        print(f"  FAIL  {detail:<24} {url}")
        print(f"        cited by: {', '.join(sorted(set(uses)))}")

    print(f"\n{len(urls) - len(failures)}/{len(urls)} cited sources resolve.")
    if failures:
        print("Check whether the authority moved the page or withdrew the guidance;")
        print("a moved page needs a new URL, withdrawn guidance needs a new claim.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
