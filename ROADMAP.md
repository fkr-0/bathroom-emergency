# Bathroom Emergency Guide — Roadmap

The guide is now broad enough that “add more chapters” is not a strategy. Future
work should improve **routing coverage**, **local usefulness**, and **evidence
quality** without turning the first minute into a literature review.

## Design invariants

Every extension must preserve these rules:

1. **Red flags dominate.** No score, chart, home measurement, or reassuring
   percentage may cancel emergency routing.
2. **One route, one action.** The first screen/page supplies one next action, one
   backup, one escalation condition, and one destination.
3. **Scope travels with the number.** Numeric claims need evidence class,
   population or model scope, denominator, uncertainty where available, source,
   and practical limit.
4. **Text remains complete.** Diagrams help; they never become the only usable
   route.
5. **Local details are data.** Service numbers, language, legal routes, and
   regional hazards should be configurable rather than buried in prose.
6. **Humour follows safety.** A joke may sit beside explanation, never between a
   danger sign and the action.

## Review findings from 4.1.1–4.1.2

### Strong foundations

- The red-flag override and four destination guides remain a sound top-level
  architecture.
- The A–G entry doors cover emotional, bodily, responsibility, danger,
  congestion, household-hazard, and no-place states in plain language.
- The long text tree provides a robust non-visual fallback.
- Evidence labels and the new fact registry make bounded quantitative material
  reviewable and reproducible.
- The color and monochrome A4 and A4/2 pipelines support offline use and two
  distinct reading rhythms without duplicating content.

### Remaining structural gaps

- Environmental hazards are distributed across smell, first aid, and disaster
  chapters rather than represented by one explicit hazard gate.
- Vulnerability modifiers—infant, pregnancy, disability, medication dependence,
  language/access needs, animal care—appear in chapters but do not yet alter the
  main route visibly.
- “No safe place” combines housing loss, violence, exposure, social overload,
  and internal crisis; these need a clearer second-level split.
- Local services are fillable prose, not validated locale data.
- The guide handles outages better than short evacuations, floods, heat waves,
  smoke/CO, and loss of essential medical equipment.
- The evidence registry validates shape and values but not automatic source
  freshness or claim-to-figure consistency.

## Main flowgraph evolution

### Proposed two-pass topology

Keep the first pass short:

```text
PASS 1 — OVERRIDE
  life/medical danger?              -> 112
  active violence/crime?            -> safer place -> 110 / 112
  fire/smoke/gas/chemical/electric? -> leave/isolate if safe -> 112/utility

PASS 2 — NEED
  body / alarm / threat-duty / outage-place
      -> apply modifiers
      -> one action + backup + escalation + destination
```

Then apply visible modifiers without creating dozens of top-level doors:

```text
M = {alone, child/infant, pregnancy/postpartum, disability,
     medication/power dependence, language/access need, animal,
     unsafe home/device, no transport}
```

A modifier changes instructions, not urgency. For example, a power-dependent
medical device adds an early backup-power/service route; it does not invent a
new diagnosis.

### Flowgraph extensions by priority

| Priority | Extension | Why it belongs in the main graph | Definition of done |
|---|---|---|---|
| P0 | fire, smoke, carbon monoxide, gas, chemical, electrical hazard gate | these hazards require leaving before ordinary troubleshooting | one compact override branch, official actions, text fallback, no switch/flame errors |
| P0 | vulnerable-person modifier strip | current route may change when an infant, pregnant/postpartum person, dependent adult, disabled person, or animal is present | modifiers appear after override and point to chapter-specific adaptations |
| P0 | essential medication / powered-device failure | outages can become medical emergencies quickly | route covers backup power, supplier, 116 117/112 escalation, and written device plan |
| P1 | “no place” second-level split | housing, violence, exposure, and internal crisis require different services | four explicit subroutes with one-hour action and local destination |
| P1 | evacuate versus shelter decision | current disaster chapter explains both but the main graph does not choose | official-warning dominance, immediate-hazard exception, go-bag and accessibility branch |
| P1 | poisoning/substance exposure route | currently divided between smells and first aid | product/substance identification, fresh-air/rinse limits, poison centre versus 112 |
| P2 | information reliability gate | outages and conflict invite rumours and malicious instructions | verify source/time/location, two-channel confirmation, no delay of immediate safety action |
| P2 | recovery/aftercare loop | the current loop ends after escalation or improvement | documentation, follow-up, restocking, repair, and delayed-symptom route |

## Chapter extension candidates

### Ch.1 — Start Here

- Add the two-pass flowgraph and modifier strip.
- Add a one-page “what this guide cannot decide” boundary map.
- Add accessibility instructions for low vision, screen readers, cognitive
  overload, and limited German.
- Future visualization: route-coverage matrix showing that every entry reaches
  action, backup, escalation, and destination.

### Ch.2 — Responsibility and dependants

- Expand medication-dependent, mobility-dependent, and communication-dependent
  care plans.
- Add a brief safeguarding route for children and dependent adults without
  encouraging amateur investigation.
- Add pet evacuation, transport, heat, and medication planning.
- Add grief and ambiguous-loss support without stage models or mandatory
  emotional sequences.
- Candidate evidence: respite-care access, medication reconciliation, and
  continuity-plan research—only where denominators and intervention scope are
  clear.

### Ch.3 — Situations B–F and the Situation G handoff

- Separate panic, dissociation, intoxication/withdrawal, delirium, and psychosis
  by observable red flags rather than self-diagnosis.
- Add heat, cold, dehydration, and sleep-loss modifiers to overload.
- Expand smell into a compact household-hazard classifier: gas, CO/smoke,
  electrical, chemical, sewage, damp/mould, ordinary hygiene.
- Expand “no place” into physical shelter, violence escape, social overload,
  and internal crisis.
- Candidate visualizations: symptom-overlap caution map; source-to-action hazard
  matrix; decision-quality versus repeated sleep restriction only when primary
  data can be plotted faithfully.

### Ch.4 — Calm Guide

- Add sensory-access alternatives for readers who cannot use visual grounding,
  breath focus, or body scans.
- Add co-regulation scripts for children, dementia, autism, and acute grief,
  reviewed for respectful language and evidence limits.
- Add a short section on when breathing focus worsens panic and how to switch to
  external orientation.
- Candidate evidence: systematic reviews of brief grounding and paced breathing;
  avoid device-derived HRV promises and universal vagal explanations.

### Ch.5 — First Aid

- Add official carbon-monoxide/smoke inhalation, heat illness, cold injury,
  drowning/near-drowning, and chemical-eye exposure routes.
- Add medication error and overdose routing with poison-centre boundaries.
- Add “waiting for help with accessibility needs” instructions: door access,
  communication cards, service animals, mobility equipment.
- Add delayed-symptom and follow-up prompts after head injury, burns, electrical
  injury, and inhalation exposure, based on current official guidance.
- Candidate visualizations: FAST timeline model already present; next figures
  should favour protocol sequences over unsupported severity scales.

### Ch.6 — Outage and disaster

- Add heat wave, winter outage, flood, wildfire/smoke, contaminated water,
  evacuation, and shelter-in-place modules.
- Add refrigeration and temperature-sensitive medication planning.
- Add sanitation/WASH for apartments and short disruptions without importing
  humanitarian-camp quantities into household advice.
- Add analogue information and neighbourhood check-in plans.
- Candidate visualizations: battery/runtime budget, food-refrigeration decision
  tree, evacuation load by mobility constraint, and communication-network
  resilience under node failure.

### Ch.7 — Professional support

- Convert German service information into a locale registry with reviewed date,
  language availability, opening hours, and escalation boundary.
- Add routes for disability advice, migration/language support, debt, tenant
  emergencies, addiction, sexual violence, LGBTQIA+ crisis support, and animal
  emergencies.
- Add “how to prepare for a first appointment” templates without collecting
  secrets in shared printouts.
- Candidate evidence: access barriers and service-navigation studies; avoid
  generic therapy success percentages.

### Ch.8 — Appendix

- Add a claim ledger mapping each numeric sentence to registry key, source, figure,
  and chapter.
- Add printable household profiles as optional separate pages, not part of a
  shared default print.
- Add change-log tables for revised estimates and withdrawn claims.
- Add machine-readable JSON schema for evidence and locale data.

## Research and visualization backlog

A candidate only graduates into the guide when the exact figure can be defended.

| Candidate | Useful question | Preferred evidence | Main trap |
|---|---|---|---|
| carbon-monoxide exposure | which observable signs and actions require immediate exit/112? | fire service/public-health protocol | symptom concentration thresholds used for self-clearance |
| heat illness | what separates cooling/monitoring from emergency signs? | current guideline/systematic review | universal temperature cut-offs without measurement context |
| household refrigeration | when should food be discarded during outage? | public food-safety authority | one time limit applied to every appliance/food |
| medication continuity | how long can specific products tolerate temperature excursion? | product/authority data | generic medication rules |
| evacuation mobility | how do time and load change with stairs, aids, children, animals? | civil-protection guidance and measured drills | invented speed constants |
| crisis communication | which message structures improve handoff accuracy? | dispatch/human-factors studies | turning mnemonics into outcome guarantees |
| bystander support | what forms of contact improve engagement or help-seeking? | randomized/systematic evidence | mortality associations presented as intervention effects |
| flood and sewage | which contact and contamination actions are safe? | public-health/civil-protection protocols | household bleach recipes without concentration authority |
| misinformation | which verification steps reduce forwarding of false alerts? | behavioural experiments/systematic reviews | assuming one literacy trick works in acute danger |

## Engineering roadmap

### 4.2.0 — Routing and hazard architecture — released

- [x] execute the core of the two-track content plan;
- [x] implement the two-pass flowgraph and structured route registry;
- [x] add fire/smoke/CO/gas/chemical/electrical Situation H override;
- [x] add modifier strip and essential medication/powered-device route;
- [x] make the existing smell route subordinate to the hazard gate;
- [x] add data-driven route, hazard, and continuity visualizations;
- [x] preserve complete text and A4/A4/2 monochrome parity;
- [ ] split “no place” into four fully localized service subroutes—carried into
  4.3.0 because the destinations depend on locale data and accessibility.

### 4.3.0 — Locale, accessibility, and safe-place routing — implemented candidate

- [x] split Situation G into four service-specific routes;
- [x] extend `src/data/locales/de-DE.json` with scoped national services,
  access channels, and explicit local-only destinations;
- [x] add source freshness windows, warnings, failures, and deterministic
  `GUIDE_AS_OF` validation;
- [x] add six communication/access profiles, minimal written cards, and
  alternate non-breath-focused adaptations;
- [x] add safe-place and communication-access visualizations;
- [x] add color and monochrome A4 large-print editions;
- [x] test image alternatives, heading order, tagging, blank pages, geometry,
  page growth, and color/mono text parity;
- [ ] add further locales only with a local reviewer and authoritative service
  sources; translation without route ownership remains out of scope.

### 4.3.1 — Navigation and release polish — candidate complete

Tracked in `docs/plans/4.3.1-polish-plan.md`.

- [x] correct the B–F identity and preserve a named Situation G handoff;
- [x] restore and validate executable command-line script modes;
- [x] align standalone cover language and validation output with the reader voice;
- [x] bump current source, registry, and renderer metadata to 4.3.1;
- [x] review the seven sparsest A4 pages and retain each as functional writable
  space, safety buffer, opener, handoff, or reference boundary;
- [x] document the decisions in `docs/qa/4.3.1-sparse-page-review.md`;
- [x] rerender and approve the six-edition 88/87/139 page-count and density
  matrix;
- [ ] commit and tag only after the patch candidate is explicitly approved.

### 4.4.0 — Household continuity and data foundations

- heat/cold/flood/smoke modules;
- medication refrigeration and powered-device planning;
- evacuation versus shelter worksheets;
- optional household profile pages generated outside the shared default guide;
- introduce the visualization catalog and accessible chart design tokens;
- begin the first 24-figure visualization expansion, prioritizing O, B, C, H,
  and Z;
- inventory and assign stable IDs to current sources;
- prototype the canonical source registry and claim/figure back-references;
- pilot subguide-local Sources and limits on B and H.

### 4.5.0 — Graph-oriented subguide editions — specified

Tracked in `docs/plans/4.5.0-graph-subguide-architecture.md`.

- [x] define a proposed nine-subguide core family and graph identity;
- [x] define candidate satellite modules for small-room physics, decision
  science, sensors, sleep, medicines, sanitation, human factors, mutual aid,
  evidence literacy, locality, and field experiments;
- [x] specify cover, page-0 position/version, page-1 introduction/contents, and
  final handoff page grammar;
- [x] specify redundant code + pattern + glyph + colour identity;
- [x] distinguish master-guide and standalone emergency-gate behaviour;
- [x] define data, CSS, graph, build, validation, and editorial contracts;
- [x] specify local end-of-subguide Sources and limits with a deduplicated R
  index;
- [x] specify a 48–60-figure visualization program and reproducible chart
  pipeline;
- [ ] prototype the graph and two competing subguide groupings on paper;
- [ ] test monochrome/pattern recognition in A4 and A4/2;
- [ ] freeze codes, patterns, and chapter assignments after visual review;
- [ ] implement registry-driven standalone colour and monochrome outputs;
- [ ] migrate subguides one at a time without duplicating canonical prose;
- [ ] generate each subguide's source-complete end matter from one registry;
- [ ] require orientation, mechanism, evidence, and handoff visuals where the
  material supports them.

### Cross-release visualization program

Tracked in `docs/plans/visualization-program.md`.

- [x] define figure families, chart-selection rules, accessibility standards,
  and a per-subguide candidate inventory;
- [x] set a reviewed target of approximately 48–60 master-guide visuals;
- [ ] add `src/data/visualization_catalog.json`;
- [ ] add SVG/PNG generation from Vega-Lite, Graphviz/generated SVG, and
  matplotlib as appropriate;
- [ ] add alt text, long descriptions, table fallbacks, contrast checks, and
  color/mono information-parity tests;
- [ ] generate figure contact sheets, source coverage, and provenance reports.

### Subguide-local source migration

Tracked in `docs/plans/subguide-source-localization.md`.

- [x] agree on local Sources and limits at the end of every subguide;
- [x] retain citations beside claims and one canonical source registry;
- [x] define master versus standalone behavior and a B/H pilot;
- [ ] inventory current Ch.10 entries and chapter footnotes;
- [ ] add stable source IDs, ownership, claim, route, and figure links;
- [ ] migrate subguides incrementally and replace the monolithic bibliography
  with an R source index only after parity is proven.

### Continuous quality work

- validate that every referenced figure exists and every figure key exists in
  the evidence registry;
- compare numeric prose against registry values where practical;
- fail builds on deprecated figure names or withdrawn claim fragments;
- record source review dates and flag stale operational sources;
- render representative PDF pages and inspect crop, contrast, captions, and
  monochrome legibility;
- add tests that every flowgraph destination has a text equivalent.

## Not planned without stronger evidence

- personal survival percentages;
- universal cortisol or “nervous-system reset” curves;
- therapy response promises detached from condition and comparator;
- home vital-sign thresholds that clear emergency symptoms;
- deterministic attachment, trauma, or developmental predictions;
- improvised chemical dosing;
- tactical violence advice;
- scores that claim to decide whether a person deserves urgent help.

Those topics may be scientifically interesting. They are not automatically good
bathroom furniture.
