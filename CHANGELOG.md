# Changelog

## 4.2.0 — 2026-07-22

### Added a real environmental-hazard branch

- Added **Situation H** for fire, smoke, carbon monoxide, gas release, chemical
  exposure, electrical danger, outdoor warning instructions, and safe handoff.
- Changed the main guide from seven to eight entry doors and implemented the
  planned two-pass architecture: danger overrides first, need-based routing
  second, dependency modifiers after the route.
- Made the existing smell branch explicitly post-override so drain and mould
  troubleshooting cannot sit above fire, gas, electricity, or fumes.

### Strengthened continuity guidance

- Added an essential-medication and powered-device failure route with action,
  approved backup, early escalation, powered destination, and handoff fields.
- Added dependency modifiers for children, pregnancy/postpartum, mobility and
  sensory access, medication, powered devices, animals, language, being alone,
  and transport.

### Added structured foundations and visualizations

- Added `src/data/route_catalog.json` as the canonical action/backup/escalation/
  destination registry and `src/data/locales/de-DE.json` for reviewed German
  services, poison centres, warning channels, and local fields.
- Added data-driven two-pass routing, environmental-hazard, and essential-care
  continuity diagrams.
- Added route and locale validation covering graph destinations, source IDs,
  unsafe wording regressions, official service numbers, all seven German poison
  centres, chapter coverage, and generated figures.

## 4.1.2 — 2026-07-22

### Added the A4/2 field-strip edition

- Added color and monochrome **105 × 297 mm** outputs, equivalent to cutting an
  A4 sheet lengthwise into two tall one-column pages.
- Added a dedicated narrow-layout stylesheet instead of shrinking the A4 design.
- Reworked headings, emergency-number blocks, figures, tables, formulas,
  footnotes, code blocks, and cover proportions for the narrow page.
- Added curiosity-oriented “FIELD NOTE” and “LOOK CLOSER” visual labels while
  keeping emergency actions visually dominant.

### Verified the rendered result

- Added renderer-based checks for exact page geometry, tagging, missing or blank
  pages, physical-edge collisions, required content markers, and representative
  contact sheets.
- Made the full build produce and validate standard A4 plus A4/2 color and
  monochrome editions from the same canonical chapters.

### Prepared 4.2.0

- Added a two-track content plan: an **improvement track** for clearer existing
  routes and a distinct **extension track** for new environmental-hazard,
  dependency, and “no safe place” branches.
- Converted the broad roadmap into reviewable content packets with acceptance
  criteria, source requirements, and flowgraph effects.

## 4.1.1 — 2026-07-22

### Restored carefully

- Reintroduced useful quantitative context removed with the unsafe v3.3 claims,
  but only with named evidence class, denominator, scope, source, uncertainty,
  and practical limit.
- Added bounded findings on GAD-7 diagnostic accuracy, a 28-day breathwork
  trial, lifetime infertility prevalence, postpartum-psychosis incidence,
  stroke urgency modelling, household water planning, repeated sleep
  restriction, and social-connection associations.
- Kept emergency protocols dominant over every screen, estimate, association,
  and model.

### Visualized

- Added eight reproducible evidence diagrams: evidence labels, GAD-7 validation,
  breathwork design, reproductive-health denominators, stroke time model,
  household water planner, sleep-restriction design, and social-connection odds.
- Added `src/data/evidence_facts.json` as the reviewable source of plotted values
  and figure caveats.
- Replaced the legacy monolithic diagram generator; deprecated fictional or
  unsafe charts are removed during the canonical build.

### Extended

- Expanded scientific notation with a bounded stroke model and odds-ratio
  definition.
- Added `ROADMAP.md` covering main-flowgraph hazard gates, vulnerability
  modifiers, chapter extensions, locale/accessibility work, evidence candidates,
  and release sequencing through 4.4.0.
- Updated source policy, annotated bibliography, appendix diagram index, and
  release validation expectations.

## 4.0.1 — 2026-07-22

### Restored

- Brought the canonical v4 guide to full subject-matter parity with the
  extensive v3.3 edition while retaining v4's safer red-flag-first routing.
- Restored detailed navigation, responsibility and life-form branches, anxiety
  and pain context, comfort and exit scripts, first-aid reference material,
  disaster preparedness, group governance, professional support, legal and
  social navigation, fillable worksheets, complete text routing, and notes.
- Expanded the annotated source chapter across every major v3.3 topic area.

### Rewritten

- Reworked the restored material in the established concise, humane, mildly
  suspicious-of-nonsense voice.
- Separated urgent “do now” instructions from deeper “understand later”
  material so the long edition remains usable under stress.

### Kept safe

- Did not restore match flames, generic bleach dosing, unsafe foraging,
  fictional cortisol decay, pain/vital-sign self-clearance, tactical violence,
  deterministic attachment or development claims, therapy outcome promises,
  or personal survival percentages.
- Updated burns, fractures, hypothermia, postpartum support, legal aid, and BBK
  preparedness references against current authoritative material.

### Verified

- Added content-parity regression markers, source-volume checks, and dynamic
  revision validation tied to the package version.
- Rebuilt and validated the complete color and monochrome document pipeline.
- Removed the redundant blank page between the full-page cover and Chapter 1.

## 4.0.0 — 2026-07-17

### Rebuilt

- Unified cover, chapters, navigation, screen UI, and print output in one
  semantic document pipeline.
- Replaced remote MathJax and timed browser waits with Pandoc-native MathML.
- Added a responsive contents rail, mobile drawer, theme toggle, reading
  progress, print control, and a restrained bathroom-tile visual system.
- Enforced A4 single-column printing for both color and monochrome editions.
- Added Chrome and WeasyPrint PDF paths that consume the same HTML.
- Added build validation for structure, known safety regressions, MathML,
  image references, A4 geometry, and plausible page count.

### Reoriented

- Replaced the old broad fan-out with a portrait red-flag-first flowgraph.
- Added a four-route overview and explicit act/check/escalate loop.
- Established the red-flag dominance invariant: scoring and formulas cannot
  cancel emergency routing.

### Corrected

- Medical and unexpected-birth emergencies now route to 112, not police 110.
- Removed match-based smell advice, concentration-free bleach dosing, unsafe
  emergency foraging, pain “physiological correlates,” and a fictional
  cortisol-decay curve.
- Reframed GAD-7 and numerical pain scores as screening/communication tools.
- Updated CPR, bleeding, burns, stroke, anaphylaxis, poisoning, crisis,
  violence, pregnancy, water, outage, and caregiver guidance.
- Reworked every formula as a protocol, exact relation, conceptual model, or
  mnemonic and documented its limit.

### Sourced

- Updated to ERC Guidelines 2025 and the current 2025 BBK preparedness guide.
- Verified German 112, 110, 116 117, 116 123, 116 016, and 116 111 routes.
- Added direct authoritative and primary references with claim-specific notes.

## 3.4.0 — 2026-06-10

Experimental multi-backend PDF and two-column layout work.

## 3.2.0 — 2026-05-03

Scientific-diagram and formula expansion.

## 3.0.0 — 2026-05-01

Modular content and source chapter.

## 2.0.0 — 2026-04-29

Pixel assets and themed output.

## 1.0.0 — 2026-04-29

Initial guide.
