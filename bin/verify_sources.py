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
import time
import urllib.parse
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src_layout import all_chapter_paths  # noqa: E402

DEFINITION = re.compile(r"^\[\^([a-z0-9-]+)\]:(.*)$", re.MULTILINE)
URL = re.compile(r"https?://[^\s)\]]+")
AGENT = "Mozilla/5.0 (bathroom-emergency-guide source review)"

# Hosts that refuse automated requests outright, including for their own front
# page. A 403 from these says nothing about whether the cited page exists, so
# they are reported for manual checking rather than counted as failures -- a
# check that can never pass is a check people learn to ignore.
BOT_BLOCKED = {"www.iasp-pain.org"}

# URLs a human has opened and read. Recording the date turns a permanent
# "someone should check this" into provenance: the reviewer confirmed the page
# served the expected content, and the entry ages like any other source.
CONFIRMED_BY_HAND = {
    "https://www.iasp-pain.org/resources/terminology/":
        "2026-08-08 (IASP Terminology, Loeser preamble and term list)",
}


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
    """Fetch the URL, retrying once when nothing came back at all.

    curl reports a timeout or dropped connection as code 000. Several of the
    cited authorities rate-limit, so a single 000 says "try again", not "the
    guidance is gone" -- and a checker that cries wolf on a slow ministry is a
    checker nobody runs before a release.
    """
    for attempt in range(2):
        result = subprocess.run(
            ["curl", "-sSL", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", "25", "-A", AGENT, url],
            capture_output=True, text=True,
        )
        code = result.stdout.strip() or "000"
        if code != "000":
            break
        if attempt == 0:
            time.sleep(3)
    return code.startswith(("2", "3")), f"HTTP {code}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true", help="only report failures")
    args = parser.parse_args()

    urls = cited_urls()
    failures: list[tuple[str, str, list[str]]] = []
    manual: list[tuple[str, str]] = []
    for url, uses in sorted(urls.items()):
        ok, detail = check_doi(url) if "doi.org/" in url else check_http(url)
        host = urllib.parse.urlparse(url).netloc
        if not ok and host in BOT_BLOCKED:
            manual.append((url, detail))
        elif not ok:
            failures.append((url, detail, uses))
        elif not args.quiet:
            print(f"  ok    {detail:<24} {url}")

    for url, detail in manual:
        seen = CONFIRMED_BY_HAND.get(url)
        label = "SEEN  " if seen else "MANUAL"
        print(f"  {label} {detail:<23} {url}")
        print(f"        blocks automated requests; read by hand {seen}" if seen
              else "        this host blocks automated requests; confirm by hand")

    for url, detail, uses in failures:
        print(f"  FAIL  {detail:<24} {url}")
        print(f"        cited by: {', '.join(sorted(set(uses)))}")

    unseen = [url for url, _ in manual if url not in CONFIRMED_BY_HAND]
    print(f"\n{len(urls) - len(failures) - len(manual)}/{len(urls)} cited sources resolve"
          f"{f', {len(manual) - len(unseen)} confirmed by hand' if len(manual) != len(unseen) else ''}"
          f"{f', {len(unseen)} still need a manual check' if unseen else ''}.")
    if failures:
        print("Check whether the authority moved the page or withdrew the guidance;")
        print("a moved page needs a new URL, withdrawn guidance needs a new claim.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
