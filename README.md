# Bathroom Emergency Guide

> “Most bathroom crises are not catastrophes. They are short intervals in which the body becomes unusually noticeable and the world unusually small.”

A sourced, rebuildable field guide for panic, pain, responsibility, strange body
signals, danger, overload, environmental hazards, missing places, and
infrastructure failure. The opening is a curiosity-first small-room observatory,
not a routing manual: interoception, gut–brain effects, bathroom acoustics, time
perception, working memory, affect labeling, cold-water physiology, fainting,
and smell are introduced before the first topic branch.

## Quick build

    ./bin/build_all.sh

Individual targets:

    ./bin/build_guide.sh html
    ./bin/build_guide.sh pdf
    ./bin/build_guide.sh mono
    ./bin/build_guide.sh chrome
    ./bin/build_guide.sh weasyprint
    ./bin/build_guide.sh docx
    ./bin/build_guide.sh latex
    ./bin/build_guide.sh a4half
    ./bin/build_guide.sh largeprint
    python3 bin/validate_routes.py
    python3 bin/validate_guide.py
    python3 bin/verify_layout.py
    python3 bin/verify_density.py
    python3 bin/verify_accessibility.py
    node bin/verify_overflow.mjs

Or with npm:

    npm run build
    npm test

## Requirements

| Tool | Purpose |
|---|---|
| Python 3.10+ | build orchestration and validation |
| Pandoc 3+ | Markdown to semantic HTML, LaTeX, and DOCX |
| matplotlib + Pillow | diagrams and pixel sprites |
| Node.js + Playwright | preferred tagged Chrome PDF |
| WeasyPrint | fallback PDF backend |
| Poppler tools | PDF validation and preview rendering |

The HTML route uses native MathML and system fonts. It has no CDN or runtime
network dependency.

## Source layout

    src/chapters/          13 canonical chapters, including Situations G and H
    src/diagrams/          custom routing, hazard, continuity, and evidence figures
    src/visualizations/     reviewed data, Vega-Lite specifications, and shared chart theme
    src/data/              evidence, route, locale, accessibility, continuity, subguide, visualization, and illustration registries
    src/data/locales/      reviewed locale-specific service foundations
    src/template.html      semantic screen shell and small UI controls
    src/style.css          screen + single-column print system
    src/style-subguides.css graph identities, hub cards, and standalone page grammar
    src/style-a4-half.css  105 × 297 mm field-strip print adaptations
    src/style-large-print.css A4 large-print adaptations
    src/style-mono.css     monochrome overrides only
    bin/build_guide.py     deterministic document builder
    bin/validate_routes.py routing, destination, locale, and source invariants
    bin/validate_continuity.py household systems, roles, dependencies, and figures
    bin/validate_subguides.py graph nodes, chapter coverage, identities, and gate policy
    bin/validate_visualizations.py chart provenance, fallbacks, outputs, and mono encodings
    bin/validate_illustrations.py figure-family coverage and redesign-priority audit
    bin/build_visualizations.mjs offline Vega-Lite SVG/PNG renderer
    bin/validate_guide.py  safety, evidence, and rendering invariants
    bin/verify_layout.py   rendered A4/2 geometry and collision checks
    bin/verify_density.py  standard-A4 blank, edge, density, and parity checks
    bin/verify_accessibility.py structured access and large-print checks
    bin/verify_overflow.mjs boxed/table overflow checks in all HTML editions
    docs/plans/4.4.1-common-synthesis.md canonical/alternate synthesis record
    docs/plans/4.4.2-alt-spec-feasibility-and-vega.md implementation decisions
    docs/plans/4.5.0-roadmap-milestones.md gated 4.5 delivery sequence
    docs/plans/4.5.0-graph-subguide-architecture.md implemented B/H graph/subguide architecture
    docs/plans/visualization-program.md 48–60-figure visual evidence program
    docs/plans/visual-design-system.md chart, illustration, and page-composition rules
    docs/plans/subguide-source-localization.md local Sources and limits migration
    docs/qa/4.3.1-sparse-page-review.md reviewed intentional whitespace decisions
    docs/qa/4.5.0-prototype-review.md graph, identity, hub, and B/H print review
    ROADMAP.md             flowgraph, chapter, research, and release backlog
    build/                 generated deliverables

## Output matrix

| Output | Path | Notes |
|---|---|---|
| Color HTML | build/html/guide.html | responsive TOC, theme and print controls |
| Mono HTML | build/html/guide_mono.html | same structure, grayscale design |
| Color PDF | build/pdf/guide.pdf | A4, one column |
| Mono PDF | build/pdf/guide_mono.pdf | A4, one column, ink-conscious |
| A4/2 color PDF | build/pdf/guide_a4half.pdf | 105 × 297 mm vertical field strip |
| A4/2 mono PDF | build/pdf/guide_a4half_mono.pdf | narrow grayscale field strip |
| Large-print color PDF | build/pdf/guide_largeprint.pdf | A4, materially larger typography |
| Large-print mono PDF | build/pdf/guide_largeprint_mono.pdf | A4 large print, grayscale |
| Graph hub | build/subguides/index.html | nine-node identity directory; B/H links |
| B standalone family | build/subguides/B/ | A4, A4/2, and large-print color/mono |
| H standalone family | build/subguides/H/ | A4, A4/2, and large-print color/mono |
| Markdown | build/md/guide.md | assembled, frontmatter-clean |
| DOCX | build/docx/guide.docx | editable |
| LaTeX | build/latex/guide.tex | intermediate |

## Print invariant

The guide is single column in print even though the screen UI has a navigation
rail and some two-up route cards. The Chrome exporter verifies computed
column-count before producing a PDF. The validator also checks:

- 13 source chapters at revision 4.5.0;
- subject-breadth regression markers and a minimum canonical-content size;
- native MathML and no remote MathJax;
- no known unsafe legacy wording or deprecated scientific chart;
- valid 4.5.0 evidence, route, continuity, subguide, illustration, and visualization registries with source and limit fields;
- a structured route catalog with seven pass-1 overrides, six pass-2 needs,
  four safe-place routes, and nine dependency/access modifiers;
- eight household-continuity systems, five first-meeting roles, and two
  data-driven continuity figures;
- a frozen nine-node subguide graph with reciprocal edges, unique code/pattern/glyph/colour identities, a screen hub, and local position maps;
- eight offline Vega-Lite charts with reviewed derived data, canonical SVG, PNG
  fallbacks, one shared theme, catalog-driven captions/limits, SVG metadata,
  text/table equivalents, source scope, and practical limits;
- seventeen current non-Vega figures classified by reader question, visual family,
  renderer, text fallback, monochrome strategy, and redesign priority;
- reviewed de-DE services, all seven poison-information centres, dated source
  windows, access channels, and local-value requirements;
- every referenced image, evidence figure, and route figure exists;
- roadmap coverage for locale, accessibility, and continuity follow-up releases;
- readable standard A4, 105 × 297 mm, and large-print A4 PDFs, including 12 tagged standalone B/H editions with color/mono text and page-count parity;
- renderer-based A4/2 checks for blank pages, physical-edge collisions, required
  content markers, and representative-page contact sheets;
- standard-A4 density checks for blank pages, physical-edge contact, extreme
  packing, color/mono text parity, and sparse/dense review contact sheets;
- computed overflow checks for cards, emergency boxes, tables, preformatted text,
  quotations, and figures across all six HTML editions.

## Evidence policy

Statements are labelled by function: protocol, population estimate,
diagnostic-accuracy study, randomized study, observational association,
descriptive equation, mathematical or conceptual model, and mnemonic.

Plotted values live in `src/data/evidence_facts.json`. Each record names its
population or model scope, denominator, source, uncertainty where available,
and practical limit. The source chapter records the supporting literature and
what it does **not** establish.

Operational routes live in `src/data/route_catalog.json`. Every route carries an
action, backup, escalation condition, destination, and reviewed source IDs.
Locale-dependent services live in `src/data/locales/de-DE.json`; unknown local
values remain explicit fields rather than plausible-looking inventions.
Communication adaptations live in `src/data/accessibility_profiles.json`.
Household functions, ownership, backups, dependencies, and failure routes live
in `src/data/continuity_catalog.json`. Prototype graph ownership lives in
`src/data/subguides.json`; visualization provenance and output contracts live in
`src/data/visualization_catalog.json`. Operational sources carry review windows
checked against `GUIDE_AS_OF`.
Core emergency routes and source material were reviewed on 23 July 2026.

The graph-oriented subguide packaging specified in
`docs/plans/4.5.0-graph-subguide-architecture.md` now has its first
release-candidate vertical slices: distinct covers, page-0 graph position/version information,
introductions, handoffs, local Sources and limits, a nine-node core, and
redundant code + pattern + glyph + colour identities. B and H are detached;
the remaining nodes stay in the master until they pass the same gates.

`docs/plans/visualization-program.md` defines a reproducible, accessible
48–60-figure visual evidence system. `docs/plans/visual-design-system.md`
defines why Vega-Lite is used for quantitative charts, where it should not be
used, and the shared graph, illustration, typography, and page-layout rules.
`docs/plans/subguide-source-localization.md`
defines filtered Sources and limits at the end of each subguide, generated from
one canonical source registry while citations remain beside claims.

## Safety scope

This guide supports decisions. It does not diagnose, replace first-aid
training, or overrule emergency dispatchers. In Germany, call **112** when life
may be in danger or lasting harm cannot be excluded.
