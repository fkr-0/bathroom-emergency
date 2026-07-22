# Bathroom Emergency Guide — Source Register

The canonical annotated source register is
[src/chapters/10-sources.md](src/chapters/10-sources.md).

## Release policy

For each release:

1. Verify German service numbers against gesund.bund.de and the named service.
2. Check whether ERC, DRK, WHO, BBK, or other cited authorities issued newer
   guidance.
3. Record exactly which claim each source supports.
4. Store plotted numeric inputs in `src/data/evidence_facts.json` with evidence
   class, denominator, scope, uncertainty, and practical limit.
5. Remove claims that exceed the source, even when they sound usefully
   scientific.
6. Keep emergency instructions short enough to execute.
7. Rebuild and validate color and monochrome A4 and A4/2 outputs.

## Operational route sources

Version 4.2.0 separates operational routing from explanatory evidence:

- `src/data/route_catalog.json` stores pass-1 overrides, pass-2 needs,
  dependency modifiers, destinations, and reviewed source IDs;
- `src/data/locales/de-DE.json` stores national service scopes, poison centres,
  warning channels, and values that must be supplied locally;
- `bin/validate_routes.py` rejects missing destinations, missing or outdated source records,
  unsafe wording regressions, incomplete poison-centre coverage, and diagrams
  without chapter routes.

Operational source order is: current public authority or emergency service;
current technical safety authority; product- or substance-specific professional
advice; explanatory literature. A study never outranks a fire brigade, poison
centre, dispatcher, warning authority, or approved device emergency plan.

## Evidence order

The source choice depends on the question:

1. current public authority or guideline body for operational protocols;
2. systematic review or guideline synthesis for broad effect or accuracy claims;
3. primary peer-reviewed study when the design itself is the notable finding;
4. high-quality public medical information for accessible explanation;
5. secondary explanation only when clearly labelled.

A newer synthesis may legitimately differ from a famous development study. Both
may be shown when the difference teaches calibration rather than confusion.

Access and core emergency-route review date: **2026-07-22**.
