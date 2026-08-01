# Bathroom Emergency Guide

> Most bathroom crises are short intervals in which the body becomes unusually
> noticeable and the world unusually small.

A sourced, rebuildable, print-first field guide for panic, pain, responsibility,
strange body signals, immediate danger, overload, environmental hazards, loss of
safe place, and infrastructure failure.

The project is not one long emergency leaflet. It is a maintained family of:

- one complete master guide;
- ten graph-linked content identities;
- six released standalone subguide families;
- detachable forms and deployment fields;
- a stable global reference registry;
- a modern project landing page, deployment planner, download catalogue, route
  hub, and enhanced HTML guide;
- A4, A4/2, large-print, color, monochrome, Markdown, DOCX, and LaTeX outputs;
- source, route, figure, accessibility, layout, density, and release validators.

## Roles

| Role | Responsibility |
|---|---|
| **Authors** | maintain generic content, evidence, references, rendering, and release history |
| **Deployer** | adapt one copy to one place, verify local routes, install supplies, protect private data, and maintain the installation |
| **Reader** | use the guide in the moment; the reader is not silently made responsible for maintaining the project |
| **Helper** | support calls, writing, observation, transport, or handoff without replacing the affected person’s agency where they can decide |

## Safety scope

The guide supports observation, routing, first actions, preparation, and
handoff. It does not diagnose, replace first-aid training, guarantee service
availability, or overrule emergency dispatchers and qualified professionals.

In Germany, use **112** for acute or potentially life-threatening emergencies,
fire, smoke, severe breathing difficulty, unresponsiveness, major bleeding, or
another rapidly escalating danger. Use **116 117** for an urgent medical problem
that cannot wait for ordinary practice hours but is not life-threatening.

## Quick start

### Local build

    npm ci
    npx playwright install chromium
    npm run build
    npm test

`npm run build` regenerates diagrams, inventories, stable references, every
master edition, every released standalone edition, the landing page, the release
manifest, and all release gates.

### Reproducible metadata

    export SOURCE_DATE_EPOCH="$(git show -s --format=%ct HEAD)"
    export GUIDE_REVISION="$(git rev-parse --short=12 HEAD)"
    npm run build

`SOURCE_DATE_EPOCH` controls the recorded build date. `GUIDE_REVISION` controls
the revision displayed in metadata and footers. Build outputs remain ignored by
Git and are reproducible from tracked sources.

### Selected targets

    ./bin/build_guide.sh html
    ./bin/build_guide.sh pdf
    ./bin/build_guide.sh mono
    ./bin/build_guide.sh docx
    ./bin/build_guide.sh latex
    ./bin/build_guide.sh a4half
    ./bin/build_guide.sh largeprint
    python3 bin/build_subguides.py --node all
    python3 bin/build_site.py
    node bin/verify_site.mjs
    python3 bin/build_release_manifest.py

## Requirements

| Tool | Purpose |
|---|---|
| Python 3.10+ | deterministic orchestration, data derivation, diagrams, and validation |
| Pandoc 3+ | semantic HTML, Markdown assembly, DOCX, and LaTeX |
| matplotlib + Pillow | generated operational and educational figures |
| Node.js 24+ + npm | locked frontend/rendering dependencies and build scripts |
| Playwright Chromium | preferred tagged PDF renderer and browser layout checks |
| WeasyPrint | fallback PDF backend |
| Poppler tools | PDF metadata, text, geometry, and page-render validation |

The HTML guide uses native MathML and system fonts. It has no CDN or runtime
network dependency.

## Information architecture

### Ten graph identities

| Code | Title | Current packaging |
|---|---|---|
| O | Orientation | master guide |
| A | Reproductive Health and Responsibility | master guide |
| B | Alarm and Calm | master + standalone |
| C | Body and First Aid | master + standalone |
| D | Threat and Safe Place | master guide |
| H | Air, Smell, and Environment | master + standalone |
| Z | Disruption and Continuity | master guide |
| P | Professional Support | master + standalone |
| T | Templates — The Blue Book | master + standalone |
| R | Reference and Appendix | master + standalone |

Detaching a node is not a copy operation. A standalone node must pass source,
visual, color/mono, geometry, tagged-PDF, semantic-text, handoff, and
accessibility gates. B, C, H, P, T, and R currently meet that release contract.
O and D now cross the numerical source/visual candidate screen, but remain in
the master guide until their extracted layouts, accessibility behaviour, route
handoffs, and real-reader usability have been reviewed to the same standard.

### Stable public references

Canonical references use:

    [BEG:<owner>:<kind>:<sequence>]

Examples:

    [BEG:C:S:004]   section in Body and First Aid
    [BEG:T:F:003]   detachable Blue Book form
    [BEG:R:W:005]   glossary term

Kinds:

| Code | Resource |
|---|---|
| S | section |
| F | form or detachable template |
| G | figure, chart, map, or diagram |
| C | professional contact or service |
| D | deployment field |
| W | glossary word or term |

The corresponding HTML anchor is `#beg-c-s-004`. Page numbers and hierarchical
chapter numbers remain useful navigation aids, but they are not canonical IDs:
an insertion must not silently rename every later resource.

Source files:

- `src/data/reference_ids.json` — stable ID allocation and retired keys;
- `src/data/content_index.json` — complete active resource index;
- `bin/build_reference_index.py` — deterministic generator;
- `bin/validate_reference_index.py` — immutability, uniqueness, coverage, and
  fragment validation.
- `src/data/coverage_matrix.json` — per-node section, source, visual, and
  standalone readiness;
- `bin/build_coverage_matrix.py` / `bin/validate_coverage_matrix.py` — generated
  provenance report and drift gate.

### Blue Book forms

`src/chapters/07a-templates.md` and `src/data/forms.json` define detachable,
fillable resources, including:

- deployment ownership and revision card;
- factual location and access card;
- emergency call card;
- local professional contacts;
- comfort inventory;
- five-minute values bridge;
- observation and vital-sign log;
- nice-place and safe-place maps;
- medication, power, and care continuity card;
- household continuity board;
- feedback, installation audit, route-drill, first-aid-figure review,
  maintenance, remarks, and quiet-activity sheets.

`src/data/deployment_fields.json` is the machine-readable index of local facts a
deployer should consider. Each field records whether it is required, its privacy
class, and an example. Shared wall copies must not expose hidden-key locations,
credentials, private medical details, or violence-related safe locations.

## Source layout

```text
.
├── src/
│   ├── chapters/                 14 canonical source chapters
│   ├── data/                     routes, sources, forms, references, locale,
│   │                             accessibility, continuity, and figure catalogs
│   ├── data/locales/             reviewed locale-specific service foundations
│   ├── diagrams/                 generated route, first-aid, continuity,
│   │                             accessibility, scientific, and graph figures
│   ├── visualizations/           Vega-Lite specs, reviewed data, and shared theme
│   ├── template.html             semantic shell and revision furniture
│   ├── style.css                 screen and single-column print system
│   ├── style-subguides.css       graph identities and subguide grammar
│   ├── style-a4-half.css         105 × 297 mm field-strip adaptations
│   ├── style-large-print.css     materially larger A4 typography
│   └── style-mono.css            monochrome overrides
├── bin/
│   ├── build_all.sh              complete build-and-validation pipeline
│   ├── build_guide.py            master document builder
│   ├── build_subguides.py        graph hub and standalone families
│   ├── build_reference_index.py  stable reference/index generator
│   ├── build_site.py             self-contained Pages-ready project site
│   ├── verify_site.mjs           responsive browser and interaction QA
│   ├── build_release_manifest.py artifact hashes and build provenance
│   └── validate_*.py             content and release gates
├── .github/workflows/ci.yml      complete release-matrix CI
├── .github/workflows/pages.yml   explicit GitHub Pages build/deploy workflow
├── DEPLOYMENT.md                 local installation and maintenance manual
├── CHANGELOG.md                  detailed release history
└── ROADMAP.md                    completed and future work
```

## Output matrix

### Master guide

| Output | Path |
|---|---|
| A4 color HTML/PDF | `build/html/guide.html`, `build/pdf/guide.pdf` |
| A4 monochrome HTML/PDF | `build/html/guide_mono.html`, `build/pdf/guide_mono.pdf` |
| A4/2 color HTML/PDF | `build/html/guide_a4half.html`, `build/pdf/guide_a4half.pdf` |
| A4/2 monochrome HTML/PDF | `build/html/guide_a4half_mono.html`, `build/pdf/guide_a4half_mono.pdf` |
| large-print color HTML/PDF | `build/html/guide_largeprint.html`, `build/pdf/guide_largeprint.pdf` |
| large-print mono HTML/PDF | `build/html/guide_largeprint_mono.html`, `build/pdf/guide_largeprint_mono.pdf` |
| assembled Markdown | `build/md/guide.md` |
| editable DOCX | `build/docx/guide.docx` |
| LaTeX intermediate | `build/latex/guide.tex` |

### Standalone and project outputs

| Output | Path | Contract |
|---|---|---|
| graph hub | `build/subguides/index.html` | ten-node directory and handoffs |
| B family | `build/subguides/B/` | six HTML/PDF/Markdown layout-mode editions |
| C family | `build/subguides/C/` | six first-aid layout-mode editions |
| H family | `build/subguides/H/` | six HTML/PDF/Markdown layout-mode editions |
| P family | `build/subguides/P/` | six professional-support editions |
| T family | `build/subguides/T/` | six detachable-template editions |
| R family | `build/subguides/R/` | six reference/index editions |
| project landing page | `build/site/index.html` | modern project representation and route entry points |
| deployment planner | `build/site/deploy/index.html` | local-only checklist, privacy, format, mounting, and operator guidance |
| download catalogue | `build/site/downloads/index.html` | master and standalone release selection |
| Pages guide and routes | `build/site/guide/`, `build/site/routes/` | self-contained online reading package |
| packaged project docs | `build/site/docs/` | README, deployment manual, and changelog |
| site release metadata | `build/site/meta/release.json` | version, revision, metrics, and explicit no-publish/no-deploy flags |
| release manifest | `build/release/manifest.json` | version, revision, toolchain, hashes, no false publish/deploy claim |

## Print and release invariants

The validators enforce, among other things:

- 14 canonical chapters at the package version and release date;
- one-column print output despite the responsive screen navigation;
- six master layout/mode editions and 36 standalone B/C/H/P/T/R editions;
- valid A4, 105 × 297 mm A4/2, and large-print geometry;
- tagged PDFs, semantic text parity, page-count parity, and no blank/colliding
  pages;
- native MathML and no remote MathJax;
- one source-backed route registry with escalation, destination, backup, and
  reviewed-source contracts;
- ten reciprocal graph identities with unique code, pattern, glyph, color, and
  title channels;
- 300+ stable indexed resources across sections, forms, figures, contacts,
  deployment fields, and glossary terms;
- eight offline Vega-Lite figures and twenty-nine current non-Vega illustrations,
  each with reader question, fallback, source basis, and monochrome strategy;
- no known unsafe legacy wording or deprecated scientific chart;
- layout-density, physical-edge, overflow, accessibility, and color/mono checks;
- a self-contained landing/deployment/download package, responsive browser QA,
  and hashed release manifest;
- no claim that a local build was published or deployed.

Run the complete gate with:

    npm run build
    npm test
    git diff --check

## CI

`.github/workflows/ci.yml` runs on pushes to `main`, version tags, pull requests,
and manual dispatch. It:

1. installs the document and browser toolchain;
2. builds the complete release matrix;
3. reruns validation independently;
4. verifies that tracked generated registries are current;
5. uploads the master, standalone, site, and release-manifest artifacts.

CI builds artifacts; it does not deploy either intended domain.

`.github/workflows/pages.yml` is the separate, explicit publication path. It
rebuilds and validates the same source tree, uploads only `build/site`, and then
uses GitHub's Pages deployment action. A local build never invokes that workflow.
Set the optional repository variable `PAGES_CUSTOM_DOMAIN` only after DNS and
the intended public domain are ready.

## Deployment

Read `DEPLOYMENT.md` before placing a copy. A deployer should at minimum:

1. select a readable layout and print mode;
2. fill and verify required local fields;
3. separate shared-safe from private/context-sensitive pages;
4. add a pencil, writing surface, light, charger, maintained power bank, and
   appropriate first-aid supplies;
5. test one emergency/support route;
6. complete the installation audit on the actual wall, folder, sleeve, or box;
7. record the guide version, build commit, local revision, last check, and next
   review date.

Intended domain roles:

- `bathroom-emergency.fkr.dev` — project representation, participation,
  deployment, sources, disclaimers, and release links;
- `be.fkr.dev` — enhanced HTML guide and downloads.

These are deployment contracts, not evidence that hosting has already occurred.
For a local preview of the exact Pages package, run:

    python -m http.server 8080 -d build/site

Then open `http://localhost:8080`. The project UI uses local assets and makes no
runtime analytics, font, CDN, or API request. The deployment checklist persists
only in that browser's local storage and is deliberately unsuitable for storing
sensitive local facts.

## Evidence policy

Statements are labelled by function: protocol, population estimate,
diagnostic-accuracy study, randomized study, observational association,
descriptive equation, mathematical/conceptual model, or mnemonic.

- plotted values: `src/data/evidence_facts.json`;
- operational routes: `src/data/route_catalog.json`;
- local service foundations: `src/data/locales/de-DE.json`;
- communication/access adaptations: `src/data/accessibility_profiles.json`;
- household continuity: `src/data/continuity_catalog.json`;
- graph ownership: `src/data/subguides.json`;
- visualization provenance: `src/data/visualization_catalog.json`;
- illustration provenance: `src/data/illustration_catalog.json`;
- canonical source view: `src/data/source_inventory.json`.
- cross-guide coverage and readiness: `src/data/coverage_matrix.json`.

Operational sources carry review windows checked against `GUIDE_AS_OF`. Unknown
local values stay explicit fields rather than plausible-looking inventions.

## Feedback and participation

Send factual corrections, failed routes, useful local adaptations, accessible
alternatives, print defects, diagrams that helped or failed, and tested
installation ideas to:

    bathroom_emergency@fkr.dev

Include the guide version, build revision, layout, and stable reference where
possible. Do not send private medical records, credentials, hidden safe-place
locations, or identifying information about another person without permission.
