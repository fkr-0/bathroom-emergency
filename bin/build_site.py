#!/usr/bin/env python3
"""Build the static project landing page from release metadata."""
from __future__ import annotations

import html
import shutil
from pathlib import Path

from project_meta import VERSION, build_date, git_revision

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "site"


def build() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in ("README.md", "DEPLOYMENT.md", "CHANGELOG.md"):
        shutil.copy2(ROOT / name, OUT / name)
    revision = git_revision()
    date = build_date()
    document = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Bathroom Emergency Guide: a sourced, printable, locally deployable small-room decision guide.">
  <title>Bathroom Emergency Guide — project and deployment</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; --ink:#14201d; --paper:#fbfaf4; --surface:#fff; --line:#b8c9c1; --green:#0d7355; --blue:#2457a6; --red:#b42318; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; color:var(--ink); background:var(--paper); line-height:1.55; }}
    a {{ color:#0b5fb3; }}
    header {{ padding:clamp(2rem,8vw,6rem) max(1rem,calc((100% - 1120px)/2)); color:white; background:#123b31; background-image:linear-gradient(135deg,transparent 0 48%,rgba(255,255,255,.06) 48% 52%,transparent 52%); background-size:28px 28px; }}
    header p {{ max-width:65ch; font-size:1.15rem; }}
    .kicker {{ font:800 .78rem ui-monospace,monospace; letter-spacing:.12em; text-transform:uppercase; }}
    h1 {{ max-width:12ch; margin:.3rem 0 1rem; font-size:clamp(3rem,9vw,6.5rem); line-height:.88; letter-spacing:-.06em; }}
    main {{ width:min(1120px,calc(100% - 2rem)); margin:0 auto; padding:2rem 0 5rem; }}
    h2 {{ margin-top:2.4rem; padding-top:.65rem; border-top:4px solid var(--green); }}
    .actions,.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1rem; }}
    .action,.card {{ padding:1rem; background:var(--surface); border:1px solid var(--line); border-top:5px solid var(--blue); }}
    .action strong {{ display:block; margin-bottom:.35rem; font-size:1.12rem; }}
    .primary {{ border-top-color:var(--green); }}
    .warning {{ border-top-color:var(--red); }}
    code {{ font-family:ui-monospace,monospace; }}
    pre {{ overflow:auto; padding:1rem; background:#eef3f0; border:1px solid var(--line); }}
    footer {{ padding:1rem; color:#52645e; border-top:1px solid var(--line); font: .75rem ui-monospace,monospace; text-align:center; }}
    @media (prefers-color-scheme:dark) {{ :root {{ --ink:#e7f1ed;--paper:#101714;--surface:#18221e;--line:#3b5047; }} pre {{ background:#17231e; }} a {{ color:#8bb6ff; }} }}
  </style>
</head>
<body>
<header>
  <div class="kicker">Bathroom Emergency Guide · release {html.escape(VERSION)}</div>
  <h1>Useful before heroic.</h1>
  <p>A sourced, rebuildable field guide for moments when the room is small, attention is narrower than usual, and the next useful action should not depend on remembering a whole course, website, or phone tree.</p>
  <p><strong>This page represents the project.</strong> The guide supports observation, routing, first actions, preparation, and handoff. It does not diagnose, replace first-aid training, guarantee local services, or overrule emergency dispatchers.</p>
</header>
<main>
  <section class="actions" aria-label="Primary project links">
    <a class="action primary" href="../html/guide.html"><strong>Open the HTML guide</strong>Responsive complete edition, printable and usable offline after download.</a>
    <a class="action" href="../subguides/index.html"><strong>Choose a subguide</strong>Graph hub with released Alarm, Environment, Blue Book, and Reference editions.</a>
    <a class="action" href="DEPLOYMENT.md"><strong>Deploy a local copy</strong>Fields, privacy boundaries, mounting concepts, maintenance, and build instructions.</a>
    <a class="action" href="mailto:bathroom_emergency@fkr.dev"><strong>Send feedback</strong>Corrections, failed routes, local adaptations, accessibility findings, and participation.</a>
  </section>

  <h2>Purpose and design ideas</h2>
  <div class="grid">
    <article class="card"><h3>Mini-why, then action</h3><p>A compact reason reduces resistance and myth-making without turning urgent pages into lectures.</p></article>
    <article class="card"><h3>Externalize the load</h3><p>Forms, maps, logs, local contacts, and handoff cards move facts out of working memory.</p></article>
    <article class="card"><h3>Stable addresses</h3><p>Typed references such as <code>[BEG:T:F:003]</code> survive page and chapter movement.</p></article>
    <article class="card"><h3>Local truth stays local</h3><p>Unknown service numbers, safe places, access barriers, care dependencies, and building facts remain visible deployment fields rather than plausible inventions.</p></article>
    <article class="card"><h3>Print is a first-class interface</h3><p>A4, A4/2, large print, color, and monochrome outputs are built and checked from one source tree.</p></article>
    <article class="card"><h3>Sources include limits</h3><p>Protocols, studies, associations, models, and mnemonics are labelled by what they can honestly establish.</p></article>
  </div>

  <h2>Participation and feedback</h2>
  <p>Useful contributions include factual corrections, official local routes, failed instructions, tested mounting ideas, accessible alternatives, print defects, diagrams that did or did not help, and low-demand activities that have survived contact with an actual bathroom.</p>
  <p>Email <a href="mailto:bathroom_emergency@fkr.dev">bathroom_emergency@fkr.dev</a>. Include the guide version, build revision, layout, and stable reference where possible. Do not send medical records, credentials, hidden safe-place locations, or identifying information about another person without permission.</p>

  <h2>Deployment in one screen</h2>
  <ol>
    <li>Choose the readable physical edition and print mode.</li>
    <li>Fill required local location, access, support, safe-place, building, and continuity fields.</li>
    <li>Verify time-sensitive contacts with the responsible official or service.</li>
    <li>Separate shared-safe pages from private or context-sensitive material.</li>
    <li>Add a pencil, writing surface, light, charger, maintained power bank, and relevant first-aid supplies.</li>
    <li>Test one route and record the next review date.</li>
  </ol>
  <p>The complete procedure, field index, installation concepts, and maintenance cycle are in <a href="DEPLOYMENT.md">DEPLOYMENT.md</a>.</p>

  <h2>Build and development</h2>
  <pre><code>npm ci
npx playwright install chromium
npm run build
npm test</code></pre>
  <p>The build creates the master HTML/PDF families, editable formats, four standalone subguide families, the graph hub, generated indexes, landing page, and release manifest. See <a href="README.md">README.md</a> for the toolchain and <a href="CHANGELOG.md">CHANGELOG.md</a> for release history.</p>

  <h2>Sources and disclaimers</h2>
  <p>Operational and scientific sources are kept in the guide beside claims, in local Sources and limits blocks, and in the Reference edition. Local service availability and procedures can change; a deployed copy needs dated verification.</p>
  <div class="card warning"><strong>Emergency scope:</strong> In Germany, immediate or potentially life-threatening situations, severe breathing difficulty, unresponsiveness, fire, smoke, major bleeding, or another rapidly escalating emergency belong on the 112 route. The guide must never create a reading queue before emergency help.</div>

  <h2>Domain contract</h2>
  <p><code>bathroom-emergency.fkr.dev</code> is intended for this project representation. <code>be.fkr.dev</code> is intended for the enhanced online guide and downloads. These names describe the deployment plan; this local build does not claim that hosting has already occurred.</p>
</main>
<footer>Bathroom Emergency {html.escape(VERSION)} · {html.escape(revision)} · built {html.escape(date)} · source tree remains authoritative</footer>
</body>
</html>
'''
    path = OUT / "index.html"
    path.write_text(document, encoding="utf-8")
    print(f"  [OK] landing page → {path.relative_to(ROOT)}")
    return path


if __name__ == "__main__":
    build()
