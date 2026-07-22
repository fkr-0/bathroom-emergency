#!/usr/bin/env python3
"""Validate structured route and locale foundations for Bathroom Guide 4.2.x."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
VERSION = PACKAGE["version"]
ROUTES_PATH = ROOT / "src" / "data" / "route_catalog.json"
LOCALE_PATH = ROOT / "src" / "data" / "locales" / "de-DE.json"
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing data file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return {}


routes = load(ROUTES_PATH)
locale = load(LOCALE_PATH)
check(routes.get("release") == VERSION, "route catalog release does not match package version")
check(locale.get("release") == VERSION, "locale release does not match package version")
check(routes.get("reviewed_on") == "2026-07-22", "route catalog review date drifted")
check(locale.get("reviewed_on") == "2026-07-22", "locale review date drifted")
check(routes.get("policy", {}).get("queue") == ["action", "backup", "escalation", "destination"], "route queue invariant missing")

destinations = routes.get("destinations", {})
sources = routes.get("source_registry", {})
overrides = routes.get("overrides", [])
needs = routes.get("needs", [])
modifiers = routes.get("modifiers", [])
required_override_ids = {
    "life-medical", "violence-crime", "fire-smoke", "carbon-monoxide",
    "gas-release", "chemical-exposure", "electrical-danger",
}
required_modifier_ids = {
    "alone", "infant-child", "pregnancy-postpartum", "mobility-sensory",
    "medication", "powered-device", "animal", "language-communication", "no-transport",
}
required_destinations = {"112", "110", "116117", "poison-centre", "gas-network", "chapter-hazard", "chapter-outage"}
check(required_destinations <= set(destinations), "route catalog is missing required destinations")
check(required_override_ids == {item.get("id") for item in overrides}, "override route set is incomplete or unexpected")
check(required_modifier_ids == {item.get("id") for item in modifiers}, "modifier set is incomplete or unexpected")
check(routes.get("override_order") == [item.get("id") for item in overrides], "override order and override records differ")

for collection_name, collection in (("override", overrides), ("need", needs)):
    for item in collection:
        rid = item.get("id", "<missing>")
        for field in ("action", "backup", "escalation", "destination"):
            check(bool(item.get(field)), f"{collection_name} route {rid} lacks {field}")
        check(item.get("destination") in destinations, f"{collection_name} route {rid} has unknown destination")
        emergency = item.get("emergency_destination")
        check(not emergency or emergency in destinations, f"{collection_name} route {rid} has unknown emergency destination")
        if collection_name == "override":
            check(item.get("pass") == 1, f"override route {rid} is not pass 1")
            check(bool(item.get("trigger")), f"override route {rid} lacks trigger")
            for source_id in item.get("source_ids", []):
                check(source_id in sources, f"override route {rid} has unknown source {source_id}")
        else:
            check(item.get("pass") == 2, f"need route {rid} is not pass 2")

for modifier in modifiers:
    mid = modifier.get("id", "<missing>")
    check(bool(modifier.get("preparation")), f"modifier {mid} lacks preparation")
    check(bool(modifier.get("failure_escalation")), f"modifier {mid} lacks failure escalation")

for source_id, source in sources.items():
    check(str(source.get("url", "")).startswith("https://"), f"source {source_id} lacks HTTPS URL")
    check(source.get("reviewed_on") == "2026-07-22", f"source {source_id} review date drifted")

serialized = json.dumps(routes, ensure_ascii=False).lower()
for forbidden in ("light a match to diagnose", "use a flame to test", "make yourself vomit", "neutralize with another chemical"):
    check(forbidden not in serialized, f"unsafe route wording present: {forbidden}")
check("no flame, switch, plug, bell, fan, or phone inside" in serialized, "gas no-spark rule missing")
check("do not enter it" in serialized, "smoky escape-route guard missing")
check("do not induce vomiting" in serialized, "chemical no-vomiting rule missing")

services = locale.get("services", {})
for key, number in {"112": "112", "110": "110", "116117": "116 117", "116123": "116 123"}.items():
    check(services.get(key, {}).get("number") == number, f"locale service {key} has wrong number")
check(services.get("gas_network", {}).get("local_value_required") is True, "gas-network local field is not required")
poison_centres = locale.get("poison_centres", [])
check(len(poison_centres) == 7, f"expected seven German poison centres, found {len(poison_centres)}")
check({item.get("city") for item in poison_centres} == {"Berlin", "Bonn", "Erfurt", "Freiburg", "Göttingen", "Mainz", "München"}, "poison-centre city set drifted")

chapter = ROOT / "src" / "chapters" / "03h-environmental-hazards.md"
check(chapter.exists(), "Situation H chapter is missing")
if chapter.exists():
    text = chapter.read_text(encoding="utf-8")
    for marker in ("Fire or smoke", "Carbon monoxide", "Gas smell or hissing", "Chemical fumes", "Electrical danger", "hazard handoff"):
        check(marker.lower() in text.lower(), f"Situation H marker missing: {marker}")

for name in ("two_pass_route_map.png", "hazard_override_matrix.png", "dependency_continuity_map.png"):
    check((ROOT / "build" / "diagrams" / name).exists(), f"route diagram missing: {name}")

if errors:
    print("Route validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)
print(f"Route validation passed: {len(overrides)} pass-1 overrides, {len(needs)} pass-2 needs, {len(modifiers)} modifiers, {len(poison_centres)} poison centres at {VERSION}.")
