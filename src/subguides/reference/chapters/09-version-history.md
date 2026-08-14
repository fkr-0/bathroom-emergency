---
title: "Version History"
chapter: 9
revision: "5.1.2"
last_updated: "2026-08-14"
dependencies: []
---

# Version History

## 5.1.2 — 14 August 2026

The online edition now distinguishes the **product mark** from the **stable
reference namespace**. Reader chrome says **BE**, matching `be.fkr.dev`, and its
accessible name continues to say “Bathroom Emergency Guide”. Existing
`[BEG:...]` references are not renamed: they are public addresses and changing
their prefix would make a cosmetic improvement by breaking citations.

The visible address is live. The complete reader starts at `BE / Shelf`, a
detached Green book at `BE / O`, and scrolling into a section changes the
address to its compact reader code such as `BE / dis.5` or `BE / ref.12`. Browser
tests exercise those transitions directly instead of merely checking that the
right JavaScript exists.

Stable references are now literal web hardlinks too. Every active reference has
one canonical `#BEG:...` target in the complete online guide and at least one
permalink to it; the Pages validator walks all rendered HTML reference links and
proves that their target document and fragment exist. The older lowercase
`#beg-*` IDs stay as compatibility aliases.

The website and reader headers also carry permanent release provenance: a link
to the tagged version, the exact build commit, and the build metadata/date. The
GitHub repository is promoted beyond that quiet metadata row into its own
high-contrast header control, so both “what am I reading?” and “where is the
source?” are answerable without scrolling or opening developer tools.

Dark mode receives its own browser contrast gate over reader chrome, contents,
and book content. That pass removed remaining light-only quantitative-figure
surfaces and now fails the release when normal text falls below the WCAG AA
contrast threshold used by the verifier.

Diagram QA became stricter at the same time. The text-fit audit now rejects
independently positioned labels that overlap one another, not only labels that
escape a drawn box. It caught the Orange `WARN` collision that motivated the
pass, five Recovery Position footer overflows, and additional overview-label
collisions. Ten text-bearing generator families run through the same audit, and
an independent verifier proves the detector against an intentionally broken
synthetic figure before rerendering the current diagrams.

The physical release package is hardened too: qpdf checks the booklet PDF
structure, CI keeps the full booklet matrix, and the individually imposed Shelf
and eleven colour/mono booklets are published beside their books instead of
being hidden behind only the combined print bundles.

## 5.1.1 — 12 August 2026

The web edition becomes a first-class reader rather than a generated document
behind a project landing page. The complete guide again carries a persistent
contents rail on the left at desktop widths. The Shelf and eleven colour books
are its top-level groups; stable guide sections sit beneath them. Scroll state
marks both the current section and its parent book and keeps the active entry in
view during long reads. On narrow screens the same structure remains an
Escape-closeable contents drawer.

The public website and generic book covers are intentionally less prescriptive
about emergency routing than the context-specific service pages. They now say
to use the **local emergency number**, naming **112 only for the EU**, rather
than placing Germany's 110 police shortcut on a general emergency surface. If a
call itself is unsafe, the generic surface points first to a safer place or a
trusted person who can call. Context-specific German service information can
still appear where its purpose, scope, and limits travel with the number.

The eleven-book overview also uses one identity language end to end. The former
graph circles used generic hatch marks that did not match the strong pattern
tiles below them. The graph now uses larger rounded rectangles carrying the
same pulse, diamond, wave, cross, shield, zigzag, crosshatch, dot, speech,
form-grid, and rule motifs as the book directory. Equal-axis rendering prevents
the network from stretching those nodes, and the top title/subtitle no longer
occupy the Green node's space. Local handoff graphs use the same treatment.

Repository publication instructions are no longer displayed on the public
deployment page. GitHub Pages remains an implementation detail documented in
the repository rather than a task a guide deployer needs to see on the site.

This release also records the next deployment target: a static, strictly
client-side wizard that lets a deployer fill canonical local forms, review the
privacy class and visibility of each value, and render a printable local packet
without transmitting entered data. More generally, operational knowledge such
as deployment instructions, maintenance rules, and changelog history should
converge into the deployed guide — usually Grey or Copper, or a future dedicated
deployment/maintenance book when the material becomes a coherent task of its
own.

## 5.0.2 — 11 August 2026

The first stable patch sharpens the visual identity of the eleven standalone
books. Running headers now work like field-manual tabs rather than quiet page
furniture: each book carries its glyph, route code, terse colour-book label,
larger pattern marker, heavy type, and a stronger accent rule. The canonical
`be.fkr.dev` address remains part of the header.

The identity deliberately does not depend on colour alone, so monochrome
printing preserves the same book-to-book recognition. The A4/2 treatment also
keeps the stronger geometry inside the printable region; an experimental
outer-edge border was rejected because it violated trim-safety checks.

## 5.0.1 — 11 August 2026

This is the first stable 5.x release. It promotes the reviewed 5.0 release
candidate and closes the last physical-packaging gap: the Shelf introduction is
now a booklet too, rather than a loose front-matter artifact.

The complete booklet print run contains twelve independent signatures in shelf
order: the Shelf intro followed by the eleven colour books. Colour and
monochrome bundles are both already imposed for portrait A4 duplex printing at
100%, flip on the long edge. Each booklet begins on its own physical sheet and
is folded and bound separately after printing.

Release engineering also synchronizes package and lockfile SemVer, exposes the
combined booklet downloads and print instructions through the Pages package,
puts `be.fkr.dev` into the running print header, and makes CI install and retain
the booklet toolchain/artifacts.

## 5.0.0-rc.1 — 8 August 2026

### Why this is 5.0.0 and not 4.14.0-alt.4

The `-alt` suffix existed to mark an experimental editorial line running beside
the mature 4.13 release machinery. That line is finished. The two have been one
tree since the synthesis, all eleven books have now been read by outside
reviewers and revised, and continuing to ship a "4.x alternate" would describe a
fork that no longer exists.

What actually changed at the major-version boundary: the shelf is eleven
colour-titled books rather than eight situation doors; the A–H doors survive
only as a compatibility map; reader references replaced machine identifiers on
the page; every book carries sourced citations attached to individual claims;
and the indexes are generated from registries rather than maintained by hand.
Old stable references still resolve — `[BEG:...]` addresses and retired IDs were
never recycled — so this is a major version by scope, not by breakage.

It is a release *candidate* because nothing here has been deployed, installed in
an actual bathroom, or drilled with a reader who did not write it. The
installation and route-drill sheets in Grey exist precisely to produce the
evidence that would justify dropping the `-rc`.

### The revision campaign

Six books were revised against reader critiques. The pattern across all of them
was the same: a rule stated carefully in one place and carelessly in another,
with nothing in the build noticing the disagreement.

### Safety corrections

- **Amber** had no carve-out for a shaken or head-injured baby: "After losing
  your temper" ran straight to apologize. An urgent-medical override now
  precedes the apology sequence.
- **Blue** routed "a child without safe care" to 112 while its own children's
  section, three pages later, had the correct tiering. That tiering now governs:
  110/112 for danger or unsafe abandonment, Jugendamt or Jugendnotdienst when
  there is no safe adult but no acute danger, 116 111 for counselling — which is
  stated to be counselling, not dispatch and not placement.
- **Blue** also treated any failure to maintain essential medication as a 112
  criterion. It now requires that the interruption is causing or imminently
  risks serious harm, with 116 117 for urgent but not life-threatening, and says
  outright that a missed routine dose is not an ambulance criterion.
- **Olive** told readers to warm a hypothermic person slowly. DRK describes two
  stages, routes both to 112, and says of the second: no further warming
  attempts. The section now splits the stages and keeps the one rule that never
  changes — no rubbing, no direct heat.
- **Olive**'s blanket ban on indoor combustion heaters was too broad, and its
  ban on camping stoves contradicted BBK, which suggests a Campingkocher for
  small meals while forbidding grills indoors. The test is now approval rather
  than fuel: anything not specifically intended and installed for indoor use is
  outdoor-only.
- The **hub**'s threat section advised changing passwords from a trusted device.
  Blue's own modifier already explained that a conspicuous account change can
  itself be the thing that gets noticed. The hub now carries the careful
  version, which also fixes it for the master guide.
- **Purple**'s locked-bathroom instruction became conditional: keep the barrier
  while it is the safer side, leave for fire, smoke, hazardous air, forced
  entry, or a responder's instruction.

### Fabricated precision removed

- **Purple** replaced minute-keyed cover stories with a Level 0–4 disclosure
  ladder, and dropped invented "acceptable absence" and "risk level" columns.
- **Olive** dropped group-size thresholds that presented design intuitions as
  consequences of $C(n)=n(n-1)/2$. The transitions are now qualitative.
- **Grey**'s route-drill timings are labelled provisional interface targets, not
  reader performance standards. A slow stage indicts the installation.
- Household water: BBK publishes at least **1.5 L of fluids per day** plus about
  **0.5 L for cooking**, never "2 litres". $W_{plan}=2nd$ is now labelled Olive's
  own planning convention in Olive, Copper's formula index, and the source notes.

### Architecture

- **Amber** leads with an eight-question entity check — welfare, agency,
  development, dependency, transfer, reversibility, hazard, authority — with
  substrate demoted to metadata. The reversibility rule ships with its limit in
  the same section: it constrains your own actions and never manufactures
  authority over another person's body or decision.
- **Olive** promotes the continuity invariant (status, reserve, owner, backup,
  next action, review, failure route) to the front; Dunbar, the survival
  function, the heat balance, Pareto, the pairwise-channel formula, and the
  book-architecture audit move intact to optional reading.
- **Blue** puts First minute ahead of the confirmed-destination model, pulls the
  three threat clocks from the hub after G1 rather than before the routing
  model, and gives G4 an admission criterion so it stops absorbing Teal.
- Section letters A0–A9 are gone from Amber rather than renumbered; they
  collided with the reader references printed beside them.
- **nora** is named in Blue and Purple as a prepared, registered-in-advance
  non-voice route to 110/112 — never an install task during an emergency.

### Grey stops owning rules it should only record

- Grey states explicitly that it does not decide escalation: a form copies the
  route, backup, destination, or threshold owned by the relevant book, service,
  clinical plan, product instruction, or official warning.
- Local operational facts now carry source, checked date, review-by date, and
  backup source. A number is not the fact; scope, access channel, and hours are
  part of it, and they do not always match for the same service.
- "Fresh-air route" becomes "cleaner-air place or safe-air route", because an
  area-scale smoke or chemical warning can make staying inside correct.
- The contacts table and safe-place map now carry Blue's revised escalation
  wording instead of an older copy of it.

### Copper catches up with the shelf it indexes

- The architecture line said **ten** route identities while listing eleven, and
  the sentence naming non-door identities omitted Purple. Both corrected, with a
  release invariant stating that the generated index is authoritative and this
  page must not be patched to agree with a wrong registry.
- The master cross-reference used legacy names as though they were current
  titles, and had no row for Green or Purple. Current public titles now appear;
  aliases are labelled as aliases.
- The master flowchart still routed artificial entities to "isolate, preserve
  logs, notify owner" — the exact architecture Amber was recovered from — and
  had no Purple, no Green, and no continuity invariant. Rewritten against the
  current books, and marked as the one hand-maintained page in Copper.
- Added a reference release gate covering content, service freshness, rendering
  and accessibility, and privacy.

### Evidence gains a status axis

- Source status — current operational, current optional, contested or
  approximate, historical, superseded — now sits alongside evidence class.
  Evidence class asks what kind of claim this is; status asks what job it is
  allowed to do.
- Dunbar, Ostrom, Yerkes–Dodson, polyvagal language, the philosophical material,
  and game theory carry explicit status lines.
- Collective-resilience research replaces the Prisoner's Dilemma as Olive's main
  cooperation frame, citing Drury, Cocking and Reicher (2009) and Ntontis et al.
  (2021). The **"Player B"** battery warning stays in Olive's mainline, beside
  the cooperation rules, because it is a rule about how to treat your neighbour.
- Vague "later rupture-and-repair research" is replaced by a named interaction
  study with a DOI; Bowlby and Ainsworth are relabelled historical foundations.
  The same swap removed two trade paperbacks from Purple, where the Danger
  Assessment now supports the danger list.
- Purple, Blue, Olive, and Amber added sourced citations where the text
  previously asserted. Cited sources went from 72 to 95 across the campaign.
- The IASP pain definition now cites Raja et al. (2020) in *Pain*, the paper
  that states and explains it, with the IASP term list as the secondary link.
  The IASP host refuses automated requests, so the previous citation could never
  be machine-checked; the page was read by hand on 8 August 2026 and that
  confirmation is now recorded in the source checker rather than reported
  forever as an outstanding task.

### Verification

- New validator: retired guidance cannot reappear. Nine superseded phrases —
  including the silicon-entity branch, "ten route identities", "care bridge
  fails", and "fresh-air route" — now fail the build if they return to any
  chapter except the version history and source notes, which exist to record
  what older releases said. Verified against the pre-revision files.
- Field Note headings orphaned their own kickers across the whole shelf.
  `break-after: avoid-page` was set but not `break-inside`, and the "FIELD NOTE
  nn" label is a block in `::before`, so Chromium parked the label at one page
  foot and began the next page with an unlabelled heading.
- `verify_layout` now matches markers across hyphenated line wraps: the A4/2
  column breaks "powered-device" at its own hyphen, and collapsing whitespace
  turned a present, legible heading into a missing marker.
- `verify_sources` retries once on curl code 000. Several cited authorities
  rate-limit, and a checker that reports a slow ministry as a dead link is one
  nobody runs before a release.
- Breadth and continuity markers in the validators were pinning headings when
  their job is to guarantee subjects stay covered; they now say so, and hold no
  apostrophes, since pandoc smart-quotes the output.

## 4.14.0-alt.2 — 6 August 2026

### Figures and templates become different objects

- Every reader-facing resource now declares one of two public types:
  **Figure · Read only** or **Template · Write**.
- The eight local-information sheets completed by deployers are figures because
  readers use the installed copies as reference; they are replaced rather than
  edited when facts, privacy, condition, or review dates change.
- Every one of the 49 figures and 10 templates carries a title, stable
  reference, and short description.
- Former form references for migrated local figures remain available as legacy
  anchors rather than being reused for another meaning.

### Rendering and public documentation follow the source of truth

- Figure and template wrappers now group type, title, stable reference, short
  description, content, and related-resource links as one visual object.
- The Grey Book separates local reference figures from reusable templates; the
  Copper Book generates the corresponding catalogues.
- README, deployment instructions, roadmap, landing metrics, downloads, and the
  feedback path now use the same two-type vocabulary.
- Clean standalone builds remove stale pre-Grey-Book output names before
  rendering, while selected guide builds refresh diagrams and inventories first.

### Verification

- Validators require title, stable reference, short description, and use mode
  for every indexed figure and template, exactly ten writable templates, exactly
  eight deployer-completed local figures, and read-only semantics for every
  figure.
- Six master editions, 66 standalone PDF editions, and the complete responsive
  site pass reference, migration, layout, density, accessibility, overflow,
  browser, and release-matrix checks.

## 4.14.0-alt.1 — 6 August 2026

Experimental full synthesis of the mature 4.13 release machinery with the
4.x-alt editorial line. The guide becomes an eleven-book shelf with colour
titles, adult humour, the Green Body Owner’s Manual, Purple Social Field Guide,
and Orange Natural Disasters book as canonical members. Standalone editions
begin with reader questions rather than graph governance. Safety remains
decisive at real red flags but no longer supplies the tone of every page.

## 4.13.1 — 2 August 2026

### The render environment is explicit

- Offline Vega-Lite charts now use a tracked Fontconfig profile rather than
  inheriting unrelated host desktop configuration fragments.
- Diagram labels request the available bold weight instead of an unavailable
  black weight that caused fallback messages.

### Renderer warnings become release failures

- Successful SVG rasterization now forwards stderr instead of discarding it.
- A new smoke validator renders all eight quantitative figures in a temporary
  directory, checks the exact SVG/PNG set, and requires zero stderr.
- Reader routes, claims, forms, sources, graph identities, and the 60 standalone
  PDF editions remain otherwise unchanged.

## 4.13.0 — 2 August 2026

### Responsibility and Care becomes a detachable route

- A now builds from the canonical responsibility and care chapter in A4, A4/2,
  and large-print colour/monochrome editions without copying reader prose.
- Five local sources, five owned reader visuals, seven linked Blue Book forms,
  graph handoffs, and generated Sources and limits remain attached.

### Safety comes before the verdict

- A four-clock route separates live harm, continuing effects, repair, and
  ongoing care before blame or explanation.
- New figures cover the responsibility clocks, the five-step repair sequence,
  consent/capacity/authority boundaries, and care continuity.
- Apology, acceptance, forgiveness, legal liability, and completed repair remain
  distinct claims.

### All ten graph identities are now standalone families

- The released set is O, A, B, C, D, H, Z, P, T, and R, totalling 60 standalone
  PDF editions.
- Build evidence does not decide liability, capacity, consent, forgiveness, or
  whether a real repair or care handoff succeeded.

## 4.12.0 — 2 August 2026

### Every detached route states its contract

- Each released standalone family now states its inside scope, deliberate
  boundary, canonical aliases, exit rule, and local resource map.
- Standalone manifests record linked figure, form, support, and route references
  so completeness is checked across A4, A4/2, large print, colour, and mono.

### Figures and forms carry their context

- Figure cards now carry stable addresses, owning route identity, pattern,
  glyph, reader question, and paired Blue Book forms.
- All eighteen canonical forms carry a generated route band with privacy class,
  route chips, related figures, and support-service references.
- Reference and Professional Support expose generated relationship maps instead
  of maintaining duplicate contact, diagram, and fillable-field tables.

### Clearer language keeps the same address

- Professional Support now distinguishes reaching a service from confirming a
  usable outcome, backup, owner, and review time.
- The appendix maps eight legacy situation doors into ten maintained route
  identities and keeps writable facts in T — Templates.
- Five rewritten headings retain their previous stable public references; a
  wording improvement does not retire a resource that still exists.

## 4.11.0 — 2 August 2026

### Outage and continuity becomes a detachable route

- Z now builds from the canonical outage, disaster, and continuity chapter in
  six layout/mode editions without copying reader prose into a second source.
- The standalone family carries four local sources, seven owned reader visuals,
  complete graph handoffs, and generated Sources and limits.

### Warning channels gain a local operational source

- The initial verification route now cites current BBK information for NINA and
  Cell Broadcast.
- Short direct warnings remain paired with fuller official information channels
  rather than being treated as complete incident instructions.

### Nine standalone families share one canonical source tree

- The released set is O, B, C, D, H, Z, P, T, and R, totalling 54 standalone
  PDF editions.
- A remains master-only. Build evidence does not claim that a real outage,
  evacuation, supply route, or household continuity plan was field-tested.

## 4.10.0 — 1 August 2026

### Orientation becomes a detachable route

- O now builds from the canonical Small-Room Observatory chapter in six
  layout/mode editions without copying the master cover or duplicating its
  emergency gate.
- The standalone family carries eleven local sources, four owned visuals,
  complete graph handoffs, and generated Sources and limits.

### Threat and safe place becomes a detachable route

- D now builds from its owned threat-clock section and the complete safe-place
  chapter in A4, A4/2, and large-print colour/monochrome editions.
- Eight operational sources and four reader visuals remain attached to the
  route, including destination confirmation, communication access, and the
  remaining-reserve model.

### Eight standalone families share one canonical source tree

- The released set is O, B, C, D, H, P, T, and R, totalling 48 standalone PDF
  editions.
- A and Z remain master-only. Build evidence does not claim that a local bed,
  service, safe place, or real-crisis route was available or successfully used.

## 4.9.0 — 1 August 2026

### Observation gets a visible first route

- Added a first-90-seconds body/room/attention scan before the explanatory
  material in the Small-Room Observatory.
- Added four diagrams for the scan, interoception loop, signal/story/question
  sequence, and bounded three-minute observation.
- Made the stop condition and “no improvement is a result” boundary explicit so
  observation does not silently become delay.

### A suggested safe place must become an operational destination

- Reworked the four-way route map and communication card into shorter,
  large-label operational graphics.
- Added a confirmation packet for destination, availability, access, arrival,
  backup, and escalation.
- Added a reserve-clock route that calls and moves before access or essential
  care fails, while refusing unsupported generic runtime promises.

### Candidate coverage is not a release claim

- O and D now each own four source-backed reader visuals and cross the numerical
  standalone-candidate screen.
- Both remain inside the complete guide until standalone extraction, layout,
  accessibility, and usability review are completed.

## 4.8.0 — 27 July 2026

### The project becomes a usable web surface

- Replaced the single landing document with responsive project, deployment,
  download, and 404 pages built entirely from local assets.
- Added route-aware navigation, release metrics, evidence boundaries, themes,
  mobile navigation, and a self-contained guide/route package.

### Deployment becomes interactive without becoming a database

- Added a local-only six-step checklist, progress display, reset, and copied
  summary beside privacy, format, mounting, maintenance, and operator guidance.
- Stored only generic completion keys and explicitly prohibited sensitive local
  facts in the browser interface.

### Publication remains an explicit operation

- Added browser QA for desktop/mobile layout, overflow, console errors, remote
  requests, theme changes, planner persistence, and download filtering.
- Added a GitHub Pages workflow and optional reviewed custom-domain variable;
  ordinary builds and local releases still do not publish or deploy anything.

## 4.7.0 — 26 July 2026

### First aid becomes a detachable field guide

- C now builds from its owned pain route and the canonical first-aid chapter in
  six standalone layout/mode editions.
- The release gate requires seven local sources, five owned reader visuals,
  local end matter, graph handoffs, tagging, geometry, and semantic parity.

### Professional support gains an operational visual set

- Added a six-field call packet, layered-support map, and professional-route
  selector beside complete text and table fallbacks.
- P now builds independently with five operational sources and four reader
  visuals across A4, A4/2, and large-print color/mono editions.

### Six standalone families share one source tree

- The graph hub and release matrix now cover B, C, H, P, T, and R.
- The remaining O, A, D, and Z nodes stay in the complete guide until they pass
  equivalent source, visual, layout, accessibility, and usability review.

## 4.6.1 — 26 July 2026

### The installation becomes testable

- Added wet-room installation, route-drill, first-aid-figure-review, and
  maintenance sheets to the Blue Book.
- Made glare, reach, one-handed page turning, moisture, privacy, and physical
  replacement observable deployment checks rather than prose reminders.

### Coverage becomes generated evidence

- Added a ten-node source, section, visual, provenance, and standalone-readiness
  matrix generated from canonical registries.
- Embedded the report in Reference and made stale coverage fail local builds and
  CI.
- Added four stable form references while preserving the retired-ID boundary.

## 4.6.0 — 26 July 2026

### The Blue Book externalizes useful facts

- Added T — Templates as a standalone family with detachable location, call,
  contact, comfort, observation, safe-place, continuity, feedback, remarks, and
  activity sheets.
- Split author, deployer, reader, and helper responsibilities so the person
  using the guide is not silently assigned maintenance of the installation.
- Added privacy-aware deployment fields and a full installation/maintenance
  manual.

### Reference becomes an addressable system

- Added stable typed IDs for sections, forms, figures, contacts, deployment
  fields, and glossary terms.
- Added a generated global index, diagram index, contact collection,
  deployment-field index, glossary, and form index to R — Reference.
- Released R as a standalone A4, A4/2, and large-print color/mono family.
- Expanded the graph to ten identities while keeping page and hierarchical
  numbers as non-canonical navigation aids.

### First aid explains the mechanism without inventing one

- Separated the 112 call from later actions in the first-minute flowgraph.
- Added chest-location, AED-action, and recovery-position diagrams and wrote out
  CPR and AED.
- Replaced the “reboot” metaphor with the accurate rhythm-analysis/shock model,
  explained rescuer switching and 30:2, and added short reasons beside wound,
  shock, burn, fracture, and spine actions.
- Made effective coughing the first choking principle and declined to publish
  unreviewed self-manoeuvres.

### Project and release packaging become complete

- Added a project landing page, deployment instructions, stable revision
  footers, reproducible build metadata, and a hashed release manifest.
- Added CI for every master and B/H/T/R layout/mode/format combination.
- Added validators for the stable reference registry, landing package, complete
  build matrix, and false publication/deployment claims.

## 4.5.0 — 26 July 2026

### Graph-linked subguides become real objects

- Froze nine graph identities with unique code, pattern, glyph, title, and colour
  channels, plus reciprocal edge validation and a complete text directory.
- Added a responsive graph hub and local “you are here” maps that preserve direct
  emergency routes instead of making the graph a queue before help.
- Built B — Alarm and Calm and H — Air, Smell, and Environment as standalone
  A4, A4/2, and large-print color/monochrome families from the same canonical
  prose used by the master.
- Added per-subguide covers, position/version metadata, introductions, handoffs,
  and source-complete local end matter generated from the canonical registry.

### Better models and operational pictures

- Added B’s four-channel alarm map and conceptual load/headroom model, with
  explicit limits against treating either as a diagnostic score.
- Added H’s indoor/outdoor/uncertain source-location map and five-field hazard
  handoff card.
- B and H now each carry four canonical visuals with adjacent text fallbacks and
  non-colour encodings.
- Added identity/grouping contact sheets and selected the quieter nine-node core
  over a noisier split-route prototype.

### Release engineering

- Added validators for source/section/figure ownership, graph reciprocity,
  identity uniqueness, A4/A4/2/large-print parity, PDF tagging and geometry,
  source blocks, semantic text, and reproducible hashes.
- Fixed the screen shell so standalone pages without a contents rail use the
  full reading measure rather than reserving an empty navigation column.

## 4.4.1 — 22 July 2026

### Common continuity synthesis

- Preserved the 4.3.1 observatory, safety routing, evidence limits, accessibility,
  source freshness, and six-edition print architecture while reviewing the
  alternate source tree section by section.
- Accepted compatible ownership, handoff, access, and human-factors material;
  rejected unsupported medical, survival, legal, and developmental claims.
- Added eight structured household-continuity systems, five first-meeting roles,
  two generated figures, and validation for dependencies, sources, owners,
  backups, text equivalents, and denied claims.
- Expanded the outage guide with capability inventory, visible task ownership,
  review times, failure routes, and a route for dissent.

## 4.3.1 — 22 July 2026

### Navigation and release hygiene

- Corrected the mixed situations identity to B–F while preserving a named
  handoff to the dedicated Situation G guide.
- Restored executable validator modes and made script permissions part of the
  release contract.
- Aligned source, renderer, registry, and cover metadata at 4.3.1.

### Reviewed space instead of merely filling it

- Reviewed the seven sparsest A4 pages and retained each as writable space,
  safety buffer, chapter opener, handoff, or reference boundary.
- Preserved the 88-page A4, 87-page A4/2, and 139-page large-print envelope.
- Added plans for graph-linked subguides, 48–60 reviewed visuals, and generated
  Sources and limits at the end of each future subguide.

## 4.3.0 — 22 July 2026

### Situation G becomes a router, not a shrug

- Split “no safe place” into violence/coercion, no roof tonight, access or
  essential-care failure, and social/internal crisis.
- Added national service routes where they genuinely exist and explicit local
  fields where municipalities, shelters, transport, and after-hours services
  differ.
- Added a safe-place handoff that asks for a confirmed destination, access
  method, backup, and escalation condition rather than accepting “try elsewhere.”

### Communication is part of safety

- Added six structured communication/access profiles and a minimal written
  emergency card.
- Added sign-language, text, easy-language, and online access metadata where the
  relevant German service publishes it.
- Added generated safe-place and communication-access maps while keeping the
  prose complete without colour or diagrams.

### Large print and freshness

- Added color and monochrome A4 large-print editions with materially larger
  typography rather than a browser zoom instruction disguised as a format.
- Added image-alt, heading-order, tagging, blank-page, geometry, page-growth,
  and color/mono parity checks.
- Added dated operational-source windows and deterministic stale-source tests so
  a once-correct telephone route cannot age invisibly inside the guide.

## 4.2.0 — 22 July 2026

### Eighth door: environmental danger

- Added Situation H for fire, smoke, CO, gas, chemicals, electricity, and the
  important distinction between an indoor source and an outdoor official
  shelter warning.
- Implemented the two-pass route promised in the roadmap: life/medical,
  violence/crime, and environment overrides first; observable need second;
  dependency modifiers after the route.
- Reworked Situation F so ordinary smell troubleshooting begins only after the
  hazard gate is negative.

### Existing-guide enhancements

- Added a complete essential-medication and powered-device interruption route to
  the outage guide, including approved backup, early calls, powered destination,
  transport, access, and a fillable handoff.
- Added a concise hazard handoff and after-action recovery steps rather than
  ending the route at “leave.”

### Data and visualization foundations

- Added structured route and de-DE locale registries with reviewed source IDs,
  destination types, service scopes, seven current poison centres, warning
  channels, and fields that must be supplied locally.
- Added three generated views of the data: two-pass architecture, hazard
  override matrix, and essential-care continuity map.
- Added route-specific validation so diagrams and chapters cannot quietly drift
  away from the registry.

## 4.1.2 — 22 July 2026

### A4/2 vertical field guide

- Added a true 105 × 297 mm color and monochrome edition rather than scaling an
  A4 page until the type surrendered.
- Preserved one-column reading while adapting wide tables, equations, evidence
  figures, emergency cards, footnotes, code blocks, and cover geometry.
- Added numbered “FIELD NOTE” headings and “LOOK CLOSER” figure bands to make
  the long narrow pages feel like a browsable field manual rather than a receipt
  from a very anxious pharmacy.

### Layout verification

- Added full-PDF render checks for geometry, tagging, blank pages, edge
  collisions, extracted-text markers, and color/mono contact sheets.
- Kept the standard A4 editions and made both page families part of the same
  validated build.

### Next-minor preparation

- Prepared separate 4.2.0 improvement and extension tracks with content packets,
  source gates, flowgraph changes, and definitions of done.

## 4.1.1 — 22 July 2026

### Bounded facts return

- Added a structured evidence registry containing the values, evidence class,
  denominator, source, and practical limit for every new quantitative figure.
- Added eight diagrams covering evidence roles, GAD-7 external validation,
  breathwork trial design, reproductive-health denominators, the stroke urgency
  model, household water planning, repeated sleep restriction, and social
  connection associations.
- Restored notable numbers only where the source supports their exact wording;
  emergency protocols remain dominant over all estimates and models.

### Research and writing

- Compared the famous original GAD-7 accuracy estimates with a later pooled
  diagnostic-accuracy review instead of treating one study as permanent
  calibration.
- Distinguished lifetime prevalence, rare-event incidence, randomized results,
  observational odds ratios, and literature-derived models in both prose and
  diagrams.
- Maintained the warm, slightly dry Flo voice while keeping humour outside the
  red-flag-to-action interval.

### Engineering and roadmap

- Replaced the legacy monolithic scientific generator and removed deprecated
  generated figures during the canonical build.
- Added registry and diagram expectations to validation and source policy.
- Added a roadmap for hazard overrides, vulnerability modifiers, locale data,
  accessibility, household continuity, and future evidence visualizations.

## 4.0.1 — 22 July 2026

### Full v3.3 content parity on the v4 safety core

- Restored the complete seven-door guide topology, target audience, notation
  legend, flowchart legend, current-status prompt, quick routes, and safe text
  master tree.
- Reintroduced all Situation A branches: pregnancy before birth, unexpected
  birth, postpartum period, child and adult dependants, ambiguous duties,
  harm, ongoing care, animals, and the escaped silicon life form.
- Expanded anxiety, panic, GAD-7 context, pain communication, danger and digital
  safety, cognitive overload, smell troubleshooting, and no-place planning.
- Restored the full calm-guide breadth: permission, grounding, optional
  breathing patterns, Yerkes–Dodson context, cautious polyvagal language,
  comfort inventory, leaving scripts, help requests, smalltalk, and low-demand
  activities.
- Restored first-aid triage, wounds, shock, burns, fractures, electrical injury,
  vital observations, kit planning, waiting guidance, and non-physical crisis
  parallels.
- Restored nature/disaster priorities, shelter, thermoregulation, food, energy,
  environmental observation, cooperation, communication scaling, Dunbar
  context, governance models, group psychology, and Ostrom’s principles.
- Restored the IASC support pyramid, therapy-evidence boundaries, friend-support
  guide, legal-navigation section, medical/social directories, housing packet,
  quick-reference card, and comprehensive local fields.
- Restored the appendix cross-reference, diagram index, extended formula index,
  complete safe text tree, fillable fields, deployment/update protocols, and
  notes pages.
- Expanded source coverage to match the subject breadth of v3.3.

### Safety-preserving rewrites

- Kept red-flag dominance and corrected 112/110/116 117 routing from v4.
- Replaced the fictional universal cortisol-decay curve with a labelled
  conceptual step model.
- Replaced pain “physiological correlates” and home vital-sign clearance
  thresholds with observation and escalation guidance.
- Replaced match-based smell treatment, concentration-free bleach dosing,
  unsafe foraging, tactical self-defence, deterministic attachment/development
  claims, therapy-response promises, and personal survival percentages.
- Added explicit limits to Yerkes–Dodson, polyvagal, Dunbar, game-theory,
  survival, heat-balance, and screening content.
- Removed passwords, PINs, key locations, and similar secrets from shared
  fillable-print recommendations.

### Writing and usability

- Reworked the full guide in the concise, warm, technically suspicious-of-
  nonsense voice established by v4.
- Preserved humour without placing jokes between a red flag and the emergency
  action.
- Separated “do now” instructions from “understand later” material so extensive
  content does not obstruct urgent use.

## 4.0.0 — 17 July 2026

### Technical realization

- Replaced CDN MathJax and timed browser waiting with native MathML.
- Removed brittle cover-document CSS merging; chapters and cover share one
  semantic document.
- Added a Pandoc template with table of contents, mobile navigation, theme
  toggle, reading progress, and print action.
- Rebuilt print CSS around an enforced A4 single-column invariant.
- Added an independent monochrome layer without copying the full stylesheet.
- Added Chrome and WeasyPrint PDF backends consuming identical HTML.
- Added structural, safety-wording, MathML, image, A4, and page-count validation.
- Fixed chapter assembly so repeated YAML frontmatter does not leak into output.

### Orientation and UI

- Replaced route-first diagrams with a portrait, red-flag-first flowgraph.
- Added four explicit destinations and a reassessment loop.
- Reduced decorative cards and gradients in favour of a bathroom-tile,
  high-contrast utilitarian system.
- Improved mobile contents navigation and print table/figure behaviour.

### Content and evidence

- Corrected newborn/medical routing from 110 to 112.
- Removed concentration-free bleach dosing, unsafe foraging advice, match-based
  smell advice, pain “physiological correlates,” and fictional cortisol decay.
- Reframed GAD-7 and pain scales as communication/screening tools, not triage.
- Rewrote CPR, bleeding, burn, stroke, poisoning, anaphylaxis, crisis, violence,
  water, outage, pregnancy, and caregiver sections against authoritative
  sources.
- Marked every formula as protocol, descriptive equation, conceptual model, or
  mnemonic.
- Expanded current German help numbers and source annotations.

## Earlier versions

| Version | Date | Summary |
|---|---|---|
| 3.4 | 2026-06-10 | experimental multi-backend and two-column work |
| 3.3 | 2026-05/06 | extensive content/reference edition preserved in archive |
| 3.2 | 2026-05-03 | formula and scientific-diagram expansion |
| 3.0 | 2026-05-01 | modular content and source chapter |
| 2.0 | 2026-04-29 | pixel assets and themed HTML/PDF |
| 1.0 | 2026-04-29 | initial guide |

Version 4.0.0 deliberately removed several “scientific-looking” claims from
3.x. Version 4.0.1 restored the **breadth**, not the mistakes. Version 4.1.1
restores selected **numbers**, but only with visible scope, denominator,
uncertainty, and limit. More content is useful only when its boundaries remain
visible.
