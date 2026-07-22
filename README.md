# Bathroom Emergency Guide

> “You are in a room with a door, water, and one next action.”

A sourced, rebuildable decision guide for panic, pain, responsibility, danger,
overload, bad smells, missing places, and infrastructure failure. Version 4.1.2
combines the red-flag-first v4 safety architecture with the extensive subject
breadth of v3.3, bounded quantitative evidence, native MathML, and deterministic
one-column A4 plus A4/2 field-strip printing.

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
    python3 bin/validate_guide.py
    python3 bin/verify_layout.py

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

    src/chapters/          canonical content, 00–10
    src/diagrams/          orientation, safety, and evidence figures
    src/data/              reviewed numeric inputs and evidence limits
    src/template.html      semantic screen shell and small UI controls
    src/style.css          screen + single-column print system
    src/style-a4-half.css  105 × 297 mm field-strip print adaptations
    src/style-mono.css     monochrome overrides only
    bin/build_guide.py     deterministic document builder
    bin/validate_guide.py  safety, evidence, and rendering invariants
    bin/verify_layout.py   rendered A4/2 geometry and collision checks
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
| Markdown | build/md/guide.md | assembled, frontmatter-clean |
| DOCX | build/docx/guide.docx | editable |
| LaTeX | build/latex/guide.tex | intermediate |

## Print invariant

The guide is single column in print even though the screen UI has a navigation
rail and some two-up route cards. The Chrome exporter verifies computed
column-count before producing a PDF. The validator also checks:

- 11 source chapters at revision 4.1.2;
- restored v3.3 breadth markers and a minimum canonical-content size;
- native MathML and no remote MathJax;
- no known unsafe legacy wording or deprecated scientific chart;
- a valid 4.1.2 evidence registry with source and limit for every plotted fact;
- every referenced image and required evidence figure exists;
- roadmap coverage for the next routing, locale, and continuity releases;
- readable A4 and 105 × 297 mm PDFs with plausible page counts;
- renderer-based A4/2 checks for blank pages, physical-edge collisions, required
  content markers, and representative-page contact sheets.

## Evidence policy

Statements are labelled by function: protocol, population estimate,
diagnostic-accuracy study, randomized study, observational association,
descriptive equation, mathematical or conceptual model, and mnemonic.

Plotted values live in `src/data/evidence_facts.json`. Each record names its
population or model scope, denominator, source, uncertainty where available,
and practical limit. The source chapter records the supporting literature and
what it does **not** establish.
Core emergency routes and newly restored source material were reviewed on
22 July 2026.

## Safety scope

This guide supports decisions. It does not diagnose, replace first-aid
training, or overrule emergency dispatchers. In Germany, call **112** when life
may be in danger or lasting harm cannot be excluded.
