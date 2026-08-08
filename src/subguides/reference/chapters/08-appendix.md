---
title: "The Copper Book — Reference"
chapter: 8
revision: "5.0.0-rc.1"
last_updated: "2026-08-08"
dependencies:
  - build/diagrams/two_pass_route_map.png
  - build/diagrams/evidence_classes.png
  - build/diagrams/hazard_override_matrix.png
  - build/diagrams/dependency_continuity_map.png
  - build/diagrams/safe_place_route_map.png
  - build/diagrams/communication_access_card.png
---

# The Copper Book — Reference and Useful Loose Ends

Use **R — Reference** when you need an address, a map, a formula, a figure, a
form, a service, a field, a source, or a complete text route. It exists to
shorten a search, not to become a corridor you have to walk down before doing
anything. In an emergency use the owning route or service first, and come back
here when you need to find, compare, cite, or check something.

## Stable references — addresses that survive editing

Canonical references use the form **`[BEG:<guide>:<kind>:<sequence>]`**. For
example, `[BEG:C:S:004]` names a Body and First Aid section,
`[BEG:T:F:003]` names a detachable Grey Book template, and `[BEG:T:G:006]`
names the deployer-completed Location and access figure. The corresponding HTML
anchors are `#beg-c-s-004`, `#beg-t-f-003`, and `#beg-t-g-006`.

Page numbers and labels such as “calm 1.1.3” remain useful navigation aids, but
they are not canonical addresses: inserting a section would silently rename
everything after it. Stable IDs stay attached to the resource; retired IDs are
kept in the registry rather than recycled for a different thing.

| Kind | Resource |
|---|---|
| S | section |
| F | template: reusable writable page |
| G | figure: read-only depiction or deployer-completed local reference |
| C | professional contact or service |
| D | deployment field |
| W | glossary word or term |

The source of truth is `src/data/reference_ids.json`; the generated complete
view is `src/data/content_index.json`.

{{route-identity-index}}

{{writable-template-index}}

{{deployment-field-index}}

{{professional-contact-index}}

{{diagram-index-generated}}

{{glossary-index}}

{{global-content-index}}

{{coverage-matrix}}

## Master cross-reference — where problems, routes, forms, and support meet

| Starting problem | Owning book | Useful Grey Book resource | Professional handoff |
|---|---|---|---|
| red flag / life danger | **C — The Red Book — Self Ambulance** | emergency call; location and access | 112 / dispatcher |
| body signal, faintness, ordinary inputs, medication context, or "what changed?" | **O — The Green Book — Body Owner's Manual** | observation log; comfort inventory | practice / pharmacy / 116 117 / Red as needed |
| pain / illness / injury | **C — The Red Book — Self Ambulance** | observation log; emergency call | practice / 116 117 / 112 according to urgency |
| caused harm / responsibility / dependency | **A — The Amber Book — Responsibility** | five-minute values; remarks and handoff | medical, legal, or social route via Indigo |
| anxiety / panic / overload | **B — The Teal Book — Calm Guide** | comfort inventory; observation log; nice-place map | trusted person / 116 117 / crisis service as needed |
| social absence, communication, boundary, re-entry, or graceful exit | **S — The Purple Book — Social Field Guide** | five-minute values; nice-place map; remarks | named social or professional route when needed |
| danger / coercion / nowhere safe | **D — The Blue Book — Safety & No Place** | safe-place map; location and access; local contacts | 110 / 112 / specialist service |
| smoke, gas, chemicals, electricity, unsafe air, smell, or a natural or technical hazard | **H — The Orange Book — Hazards & Disasters** | emergency call; location and access; care continuity | 112 / warning authority / gas service / poison centre |
| outage or long disruption once immediate hazards are handled | **Z — The Olive Book — Zombie Guide** | care continuity; household board | BBK / local authority / clinician / 112 as appropriate |
| need a number, appointment, bed, document, or handoff | **P — The Indigo Book — Professional Support** | local contacts; emergency call; location and access | named service plus backup |
| need a writable packet | **T — The Grey Book — Templates & Forms** | choose by use mode and privacy class | receiving service named on the resource |
| need a stable address, figure, formula, source, or audit trail | **R — The Copper Book — Reference** | feedback or review form when correcting | owning route remains primary |

The titles above are the current public ones. Older route names survive as
aliases so old links and archived text keep working; an alias is allowed to
remain findable, and is not allowed to appear here as though it were current.


## Mathematical notation legend

| Mark | Meaning | Use here |
|---|---|---|
| $\lor$ | logical OR | one true danger condition can change the route |
| $\Rightarrow$ | implies | a stated condition leads to an action inside the model |
| $\Delta$ | change between observations | sensation after minus sensation before |
| $n$ | number of people or items | group size, supplies, contacts |
| $t$ | time | minutes, hours, or days as stated |
| **Protocol** | authoritative action rule | first aid or public warning instruction |
| **Study result** | observation from a named design and population | anxiety and time-perception experiment |
| **Model** | calculation or thinking aid | communication channels in a group |
| **Mnemonic** | memorable compression | observe, change, compare |

## Eight legacy doors inside eleven route identities

| Door | Loudest problem | Current owning route | Legacy names retained |
|---|---|---|---|
| A | responsibility, dependency, or harm | **A — The Amber Book — Responsibility** | Situation A, Responsibility and Care, Ch.2 |
| B | anxiety, panic, or unreality | **B — The Teal Book — Calm Guide** | Situation B, Alarm and Calm, Ch.4 |
| C | pain or physical illness | **C — The Red Book — Self Ambulance** | Situation C, Body and First Aid, Ch.5 |
| D | danger, coercion, or violence | **D — The Blue Book — Safety & No Place** | Situation D, Threat and Safe Place |
| E | overload and task congestion | **B — The Teal Book — Calm Guide** | Situation E, Alarm and Calm |
| F | bad or unknown smell | **H — The Orange Book — Hazards & Disasters** | Situation F after the environmental gate |
| G | no safe or workable place | **D — The Blue Book — Safety & No Place** | Situation G |
| H | smoke, gas, chemicals, electricity, or unsafe air | **H — The Orange Book — Hazards & Disasters** | Situation H, Air, Smell, and Environment |

The maintained route identities are **O, A, B, C, D, H, Z, P, S, T, and R** —
eleven of them. The A–H door scheme is a compatibility map kept for older links
and printed copies; it is not the shelf.

**O, Z, P, S, T, and R** are route identities rather than additional legacy
doors: they orient bodily observation, preserve continuity, connect professional
systems, handle social navigation, carry writable facts, and make the whole
graph inspectable.

**Release invariant.** The generated route index above must list exactly those
eleven identities under their current public titles. If it ever says ten, omits
Purple, or shows a legacy alias as the current title, the registry is wrong and
this page must not be patched to agree with it.

## Guide topology

The chapters form a directed graph: observations lead to actions, actions lead
to reassessment or another chapter, and every route should end somewhere a
person can actually continue. This is useful mathematics only because dead ends
are bad writing.

![Two-pass guide topology with dependency modifiers](build/diagrams/two_pass_route_map.png)

## Flowchart legend

| Shape or style | Meaning |
|---|---|
| heavy emergency block | immediate action rather than further reading |
| diamond | choose the closest true answer |
| rectangle | do the stated action |
| rounded destination | continue in the named chapter or service |
| dashed line | optional explanation |
| loop | compare better, same, worse, or new information |

## How to read the evidence figures

![Evidence labels used throughout the guide](build/diagrams/evidence_classes.png)

A number is only as useful as its denominator, population, time frame, and
limit. Protocols tell you what to do. Studies tell you what happened under a
particular design. Associations describe variables travelling together. Models
show what follows from assumptions. None of them becomes a personal prophecy by
being printed in a confident font.

## Figure and template grammar

The generated figure catalogue above is canonical. Every figure is presented
as **Figure · Read only** with a stable `[BEG:...:G:...]` address, title, and
short description. A figure may be an authored depiction or a local reference
sheet completed and dated by the deployer before installation. Readers do not
edit the installed figure; it is replaced when the local truth changes.

Grey Book templates use the parallel label **Template · Write** with a stable
`[BEG:...:F:...]` address, title, and short description. Use a fresh copy for
each incident, observation, review, drill, or handoff.

Generated images remain explanatory aids. The adjacent prose remains the
complete route for monochrome print, screen readers, low light, failed images,
and coffee-related diagram loss.


## Evidence labels

The guide distinguishes the role of each statement:

| Label | Meaning | Example |
|---|---|---|
| **Protocol** | Action aligned with an authoritative guideline | call 112 for unresponsive abnormal breathing |
| **Population estimate** | Frequency in a named population and time frame | lifetime infertility prevalence |
| **Diagnostic-accuracy study** | Performance of a screen against a reference standard | GAD-7 sensitivity/specificity |
| **Randomized study** | Comparison created by allocation to interventions | 28-day breathwork trial |
| **Observational association** | Variables travelled together after adjustment; causation remains limited | social isolation and mortality odds |
| **Descriptive equation** | Exact relation once inputs are known | $C(n)=n(n-1)/2$ |
| **Mathematical model** | Calculation from assumptions inside a stated scope | stroke tissue-loss estimate |
| **Conceptual model** | A thinking aid, not a measured prediction | $A_{k+1}=A_k-\delta_k+\varepsilon_k$ |
| **Mnemonic** | Memorable compression | one action, one backup, one escalation |

A metaphor wearing a lab coat still needs identification, a denominator,
and visiting hours.

## Formula and theorem index

### 1. Red-flag dominance — routing protocol

$$R = \bigvee_i r_i, \qquad R=1 \Rightarrow 112$$

A positive red flag overrides scores and self-reassurance.

### 2. Tiny action queue — design theorem

$$Q=[\text{action},\text{backup},\text{escalation}]$$

Acute instructions should fit in a small working-memory budget.

### 3. Accountability tuple — procedural mnemonic

$$A=(\text{stop},\text{stabilize},\text{tell},\text{repair},\text{follow up})$$

Turns guilt into observable repair work.

### 4. Pain change — descriptive communication

$$\Delta P=P_{now}-P_{earlier}$$

Useful for reporting change; not a measure of injury or urgency.

### 5. Cognitive load — conceptual model

$$L=I+E+S$$

Intrinsic difficulty, avoidable clutter, and stress load are separated so at
least one term can be reduced. The equation is not a validated diagnostic
instrument.

### 6. Breath pacing — descriptive equation

$$T=t_i+t_e, \qquad f=\frac{60}{T}$$

Describes a chosen pattern. Comfort and safety set the pattern.

### 7. Stepwise arousal — conceptual model

$$A_{k+1}=A_k-\delta_k+\varepsilon_k$$

Small useful actions can reduce arousal while new events add load. This replaces
the fictional universal cortisol-decay curve.

### 8. Household emergency water — planning convention

$$W_{plan}=2nd\;\text{litres}$$

An **Olive planning convention**, not a BBK figure and not a medical
prescription. BBK's current wording is at least **1.5 L of fluids per day** for
an adult, plus about **0.5 L of water per day when cooking is planned**; the sum
is what this equation carries for $n$ people over $d$ days. Individual needs and
incident conditions vary, and an official water-quality instruction outranks the
arithmetic.

### 9. Communication channels — graph theorem

$$C(n)=\frac{n(n-1)}{2}$$

Explains why groups need roles and broadcast channels.

### 10. Survival function — mathematical model

$$S(t)=\exp\left(-\int_0^t h(u)\,du\right)$$

Valid mathematics, useless as a personal forecast without measured hazard data.

### 11. Heat balance — conceptual physical model

$$\Delta H=M-(C+K+R+E)$$

Represents heat production minus convective, conductive, radiative, and
evaporative losses. The guide uses it to organize prevention, not calculate a
person’s core temperature.

### 12. Listen–reflect–respond — conversation mnemonic

$$\text{listen}\rightarrow\text{reflect}\rightarrow\text{respond}$$

A compact alternative to composing a rebuttal while the other person is still
talking.

### 13. Stroke time model — literature-derived model

For the scope and assumptions used by Saver (2006), cumulative modelled neuronal
loss over $t$ untreated minutes is:

$$N(t)=1.9t\;\text{million neurons}$$

This is an order-of-magnitude urgency model for a typical large-vessel
supratentorial ischemic stroke, not a measurement in one patient. FAST and 112
remain the action.

### 14. Odds ratio — descriptive study statistic

For odds $o_1$ in one group and $o_0$ in a reference group:

$$OR=\frac{o_1}{o_0}$$

An odds ratio is not the same as a probability ratio, absolute risk, or proof of
causation. It requires the study population, adjustment set, and follow-up to
mean anything useful.



## Fillable fields live in T — Templates

R indexes writable resources; it does not maintain a second blank-form system.
Use the generated figure and template catalogues above to choose the canonical
Grey Book page. The resource band identifies its type, stable reference, and
short description; the privacy class controls placement, and related references
show what should travel with it.

The most commonly paired set is:

- **[BEG:T:G:006] Location and access card**;
- **[BEG:T:F:003] Emergency call card**;
- **[BEG:T:G:005] Local professional contacts**;
- **[BEG:T:G:008] Safe-place and exit map**;
- **[BEG:T:G:003] Medication, power, and care continuity card**;
- **[BEG:T:G:004] Household continuity board**.

Complete only relevant fields, store or photograph them safely, and replace
them when the route, local fact, privacy boundary, or review date changes.

### Do not put these on a shared printout

- passwords;
- PINs;
- alarm codes;
- safe combinations;
- private-key material;
- exact hidden spare-key location;
- information that would endanger someone fleeing violence.

A shared bathroom is not a secure credential vault, however trustworthy the
toothbrushes appear.

## Master flowchart — complete text version

This tree is maintained by hand against the eleven books, and it is the one page
in Copper that can drift without a generator noticing. If it disagrees with an
owning book, the book is right.

```text
BATHROOM EMERGENCY GUIDE — MASTER FLOWCHART
============================================================

0. OVERRIDE
   |
   +-- life danger, abnormal breathing, unresponsive,
   |   severe bleeding, stroke sign, seizure, collapse,
   |   major burn, acute self/other danger?
   |       +-- YES / MAYBE / UNSURE --> 112
   |       |                           unlock if safe
   |       |                           speakerphone
   |       |                           follow dispatcher
   |       +-- NO --> continue
   |
   +-- active crime or immediate violent threat?
   |       +-- YES --> safer place --> 110
   |       |          injury / life danger --> 112
   |       +-- NO --> continue
   |
   +-- fire / smoke / CO / gas / chemical / electrical danger,
   |   or an official hazard warning?
           +-- YES / MAYBE --> H — ORANGE
           |                  leave, shelter, or isolate only as safely
           |                  instructed; live official instructions win
           |                  112 / poison centre / gas service / warning authority
           +-- NO --> choose the loudest remaining problem

A. RESPONSIBILITY / DEPENDENCY / HARM --> A — AMBER
   |
   +-- WHICH CLOCK?  live harm / continuing effects / repair / ongoing care
   +-- live injury, birth, or immediate danger --> C — RED / 112 / 110
   +-- WHAT KIND OF STAKE?   (substrate is metadata, not a verdict)
   |      welfare       can it presently be harmed?
   |      agency        can it choose, consent, refuse, act?
   |      development   are important capacities still emerging?
   |      dependency    what fails if care stops, and is that on me?
   |      transfer      can a competent person or system take over?
   |      reversibility can today's decision be undone?
   |      hazard        can it harm other entities?
   |      authority     what am I entitled or required to decide?
   |         limit: uncertainty + irreversibility raise the burden of care
   |                on MY actions; they never manufacture authority over
   |                another person's body or decision
   +-- then the domain module: pregnancy / birth / newborn / child /
   |   adult / animal / technical system
   +-- caused harm --> stop + stabilize + tell + repair + follow up
   +-- technical system --> contain first (isolate, pause, preserve,
   |                       snapshot, notify) -- every step reversible
   |                       uncertain moral status is not zero moral status,
   |                       and never a reason to leave a harmful system running
   +-- unresolved duty --> today / legal / transfer / long-term care

B. ANXIETY / PANIC / OVERLOAD --> B — TEAL
   |
   +-- bodily symptom new, severe, or unclear --> O — GREEN / C — RED
   +-- otherwise --> orient outward + reduce one avoidable load
   |                 + one safe action + one person
   +-- recurring, or shrinking ordinary life --> P — INDIGO
   +-- acute self / other danger --> 112

C. BODY SIGNAL / PAIN / ILLNESS / INJURY --> O — GREEN + C — RED
   |
   +-- describe what changed; OPQRST or the observation log when useful
   +-- severe / sudden / chest / neuro / collapse / pregnancy red flag --> 112
   +-- urgent but not life-threatening --> practice / 116 117
   +-- stable minor problem --> appropriate first aid + reassess
   +-- device readings inform the handoff; they never cancel a red flag

D. DANGER / COERCION / NOWHERE SAFE --> D — BLUE
   |
   +-- FIRST MINUTE: 112 / 110 / Orange overrides
   +-- G1 person or active threat --> exit or safer place --> 110
   |      a lock is a barrier, not a plan: leave anyway for fire, smoke,
   |      bad air, forced entry, or a responder's instruction
   |      prepared non-voice route: nora, registered in advance
   +-- G2 no weather-safe place tonight --> municipal accommodation route
   |      child: danger --> 110/112; no safe adult --> Jugendamt;
   |      someone to talk to --> 116 111 (counselling, not placement)
   +-- G3 access or essential care fails --> name the failing function
   |      and the remaining reserve
   |      urgent but not life-threatening --> 116 117 / clinician
   |      life-supporting failure or imminent serious harm --> 112
   +-- G4 physically safe, cannot remain here for the next hour
   |      --> one-hour container + hand off the primary problem
   |      merely distressed but able to stay --> B — TEAL / S — PURPLE
   +-- CONFIRM before travelling: destination, availability, access,
   |   arrival, backup, escalation
   +-- after-effects or service need --> P — INDIGO

E. OVERLOAD / TASK CONGESTION --> B — TEAL
   |
   +-- write: prevent harm / soon / can be ugly
   +-- choose one physical action under five minutes
   +-- delegate or hand off repeated essential failures
   +-- if the real problem is social navigation --> S — PURPLE

F. BAD OR UNKNOWN SMELL --> H — ORANGE
   |
   +-- fire / smoke / CO / gas / chemical / electrical / symptoms --> hazard route
   +-- sewage or drain, only after a negative hazard gate --> repair route
   +-- damp or mould, only after a negative hazard gate --> moisture repair
   +-- do not assume outdoors is safer; current warning instructions decide

G. NO SAFE OR WORKABLE PLACE --> D — BLUE + P — INDIGO
   |
   +-- see the D branch above; G is its legacy door

H. ENVIRONMENT / HAZARD / DISASTER --> H — ORANGE
   |
   +-- fire / smoke --> smoke-free exit; unsafe route --> close door + 112
   +-- CO or combustion exposure --> leave the exposure when safe + 112
   +-- gas --> no flame, switch, bell, or phone; knock, leave, call outside
   +-- chemical --> stop exposure; rinse when appropriate; keep the label;
   |               poison centre / 112
   +-- electrical --> do not touch a live source; isolate only if safe; 112
   +-- area-scale warning --> shelter, stop ventilation, or evacuate exactly
                             as instructed

OUTAGE / LONG DISRUPTION --> Z — OLIVE
   |
   +-- first: clear Orange's hazard overrides and verify the official warning
   +-- THE CONTINUITY INVARIANT, per function:
   |      status / reserve / owner / backup / next action / review /
   |      failure route
   +-- first minutes --> air + urgent medical + temperature + water
   |                     + communication
   +-- first days --> food + medication + sanitation + dependants + animals
   +-- several households --> named roles + shared log + explicit handoffs
   +-- longer shared-resource problem --> allocation, rotation, accountability
                                          (and it never overrides an
                                           evacuation order)

SOCIAL NAVIGATION --> S — PURPLE
   |
   +-- am I safe?  no, or cannot tell --> D — BLUE / 110 / 112
   +-- clinical crisis --> C — RED / P — INDIGO
   +-- otherwise --> disclose at the level you choose (Level 0-4)
                     + boundary + re-entry + graceful exit + one next move

PROFESSIONAL ROUTE --> P — INDIGO
   |
   +-- name the problem
   +-- choose the service able to change it
   +-- prepare a usable handoff
   +-- confirm outcome, backup, owner, review time
       (contact is not handoff)

WRITABLE FACTS --> T — GREY
REFERENCE / SOURCE / STABLE ID --> R — COPPER

EVERY NON-EMERGENCY ROUTE
   |
   +-- do one action
   +-- check better / same / worse / different problem
   +-- use the backup
   +-- escalate on worsening, uncertainty, or a red flag
   +-- end at a named destination
```

## Pocket print card

<div class="safety-card">
  <h3>RED FLAG?</h3>
  <p><strong>112 · unlock if safe · speakerphone · follow dispatcher</strong></p>
  <p>Unresponsive · abnormal breathing · severe bleeding · stroke sign · chest
  pressure · severe breathlessness · seizure · major burn · collapse · acute
  self/other danger</p>
</div>

<div class="route-grid">
  <section class="route-card" data-route="medical">
    <h3>BODY</h3><p>Ch.5 · first aid · 116 117 if urgent but non-life-threatening</p>
  </section>
  <section class="route-card" data-route="calm">
    <h3>ALARM</h3><p>Feet · five objects · gentle exhale · one person</p>
  </section>
  <section class="route-card" data-route="support">
    <h3>THREAT</h3><p>Exit / safer place · 110 · 116 016 · do not confront</p>
  </section>
  <section class="route-card" data-route="support">
    <h3>NO SAFE PLACE</h3><p>Situation G · threat / no roof / access-care / internal crisis</p>
  </section>
  <section class="route-card" data-route="survival">
    <h3>ENVIRONMENT</h3><p>Leave source · Situation H · call from safety</p>
  </section>
  <section class="route-card" data-route="survival">
    <h3>OUTAGE</h3><p>Official warning · essential care · water · temperature · roles</p>
  </section>
</div>

## Offline deployment checklist

- Print the monochrome PDF single-sided or duplex.
- Complete the relevant Grey Book resources and keep their resource bands attached.
- Keep the guide near a charged light source.
- Add a simple first-aid poster from an official provider.
- Store current medication and emergency plans nearby but privately.
- Refresh service numbers and medical guidance before relying on an older printout.
- Test that QR codes or links are not the only access path.
- Ensure the print remains readable without colour.
- Replace the guide after water damage. It is not itself waterproof, despite
  strong thematic alignment.


## Navigation invariant

Every non-emergency route must provide:

1. a next action;
2. a backup;
3. a reason to escalate;
4. a named destination.

A dead end in prose is still a dead end.

## Reference release gate

Before a print or public build is called current, check the compiled system, not
only the chapter you happen to have edited.

### Content gate

- current public title and owning route agree with the generated route index;
- the emergency override and escalation rule agree with the owning book, not
  with an older copy of it;
- models, estimates, mnemonics, and optional theory are visibly labelled;
- legacy aliases remain searchable without being presented as current titles.

### Service and freshness gate

- operational numbers, hours, access modes, and scopes carry a checked date;
- a review-by date or maximum review interval exists;
- a backup or failure route exists wherever availability matters;
- a directory entry is not described as a confirmed bed, appointment, responder,
  or live destination unless that outcome was actually confirmed.

### Render and accessibility gate

- no orphan **FIELD NOTE** heading, and no identity band without its payload;
- no accidental blank-page or severe whitespace regression;
- monochrome and large-print routes remain usable;
- image alternatives and adjacent text carry the complete action route;
- detached Grey pages keep identity, privacy class, version, and review data.

### Privacy gate

- no password, PIN, private key, alarm code, hidden-key location, or protected
  refuge address is exposed;
- no private medical or identifying data is published without a lawful and
  appropriate reason;
- photographs of installations reveal no access or security detail.
