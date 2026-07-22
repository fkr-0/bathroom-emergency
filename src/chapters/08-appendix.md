---
title: "Appendix: Formulas, Theorems, Cross-References, and Print Card"
chapter: 8
revision: "4.1.1"
last_updated: "2026-07-22"
dependencies: []
---

# Appendix — The Useful Loose Ends

The v3.3 appendix tried to be index, legend, workbook, decision tree, notes page,
and emergency wallet card simultaneously. Version 4.1.1 accepts the assignment,
but labels the parts so the notes page does not accidentally become a theorem.

## Master cross-reference — where everything points

| Starting problem | Immediate destination | Deeper material | Professional route |
|---|---|---|---|
| red flag / life danger | 112, Ch.5 | first-aid sections | emergency dispatcher |
| caused harm / responsibility | Ch.2 | repair, care, postpartum, dependants | Ch.7 medical/legal/social |
| anxiety / panic | Ch.4 | Ch.3B screening and stress context | 116 123 / 116 117 / local service |
| pain / illness | Ch.5 | Ch.3C pain description | practice / 116 117 / 112 |
| danger / coercion | Ch.3D | safety plan | 110 / 112 / 116 016 |
| task overload | Ch.3E, Ch.4 | congestion board | appropriate care/support |
| unknown smell | Ch.3F | source troubleshooting | 112 / utility / poison centre |
| nowhere safe | Ch.3G | one-hour plan | municipal/social/shelter service |
| outage / disaster | Ch.6 | household and community planning | BBK/local authority/112 |
| need a number or script | Ch.7 | support-selection matrix | named service |

## Diagram index

| Diagram | Location | Purpose |
|---|---|---|
| emergency flowgraph | Ch.1 | red-flag-first routing |
| breathing techniques | Ch.4 | optional pacing patterns |
| first-aid triage | Ch.5 | response and escalation overview |
| survival priority pyramid | Ch.6 | infrastructure-failure priorities |
| group scaling chart | Ch.6 | coordination from one to 100+ |
| evidence classes | Ch.1 | what protocols, studies, associations, and models may claim |
| reproductive-health denominators | Ch.2 | lifetime prevalence versus rare-event incidence without denominator tricks |
| GAD-7 validation comparison | Ch.3 | original study versus pooled diagnostic accuracy |
| sleep-restriction study | Ch.3 | repeated sleep opportunity and cumulative impairment |
| breathwork trial map | Ch.4 | trial arms, dose, outcomes, and limits |
| stroke time model | Ch.5 | order-of-magnitude urgency model |
| household water planner | Ch.6 | three- and ten-day storage by household size |
| social-connection associations | Ch.7 | adjusted observational odds ratios with causal limits |

Generated images are explanatory aids. The text route remains complete for
monochrome print, screen readers, low light, and coffee-related diagram loss.

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

The old edition sometimes dressed a metaphor in a lab coat. Version 4.1.1 asks
the coat for identification, denominator, and visiting hours.

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

### 8. Household emergency water — planning equation

$$W=2nd\;\text{litres}$$

BBK planning value for $n$ people and $d$ days; individual needs vary.

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

## Reproducible evidence registry

The numeric inputs for v4.1.1 figures live in
`src/data/evidence_facts.json`. Each entry records evidence class, population or
scope, value and unit, source, and practical limit. Diagram code reads that file
rather than hiding facts inside plotting coordinates.

A future number change should therefore modify the registry, source annotation,
chapter prose, and generated figure in one reviewable change. Four copies of a
number drifting independently is how folklore acquires error bars.

## Flowchart symbol legend — extended

| Symbol/style | Meaning | Monochrome equivalent |
|---|---|---|
| red emergency block | call now | EMERGENCY label and heavy border |
| diamond | question/decision | question mark and branching text |
| rectangle | action | numbered imperative |
| rounded box | destination | “Go to…” label |
| dashed connector | optional explanation | “Understand later” text |
| loop arrow | reassessment | “better / same / worse?” |
| table | comparison or fillable plan | row and column headings |
| formula block | labelled mathematical content | surrounding explanation |

## Fillable fields

Fill these once, photograph or securely store the page, and update it when
anything changes.

| Field | Your value |
|---|---|
| Home address, floor, access note | |
| Emergency contact #1 | |
| Emergency contact #2 | |
| Trusted nearby person | |
| GP / practice | |
| Pharmacy / night service | |
| Local hospital / emergency department | |
| Psychiatric emergency / crisis service | |
| Sozialpsychiatrischer Dienst | |
| Poison centre | |
| Maternity / gynecology | |
| Pediatric emergency | |
| Veterinary emergency | |
| Emergency housing / shelter | |
| Building utility emergency | |
| Medication list location | |
| First-aid kit location | |
| Power bank / radio location | |
| Evacuation meeting point | |
| Backup caregiver | |

### Do not put these on a shared printout

- passwords;
- PINs;
- alarm codes;
- safe combinations;
- private-key material;
- exact hidden spare-key location;
- information that would endanger someone fleeing violence.

The v3.3 fillable page included several of these. It trusted the bathroom more
than security engineering recommends.

## Complete decision tree — safe text version

```text
BATHROOM EMERGENCY GUIDE — MASTER TREE v4.1.1
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
           +-- YES --> safer place --> 110
           |          injury/life danger --> 112
           +-- NO --> choose door

A. I CAUSED TROUBLE / SOMEONE DEPENDS ON ME --> Ch.2
   |
   +-- live injury/birth/danger --> 112 / 110 / Ch.5
   +-- pregnancy before birth --> medical + recognized counselling
   +-- birth happening now --> 112, warmth, dispatcher
   +-- hours/days after birth --> parent/baby care + mental-health check
   +-- child/dependant --> safety, essentials, backup caregiver
   +-- adult dependant/child --> requested help + boundaries
   +-- ambiguous duty --> today / legal / long-term / handoff
   +-- harm --> stop, stabilize, tell, repair, follow up
   +-- silicon entity --> isolate, preserve logs, notify owner

B. I FEEL ANXIOUS --> Ch.3B + Ch.4
   |
   +-- medical red flag/new severe symptoms --> 112
   +-- no red flag --> feet, five objects, gentle exhale, one person
   +-- recurring/impairing --> professional assessment
   +-- acute self-harm danger --> 112

C. I FEEL PAIN --> Ch.3C + Ch.5
   |
   +-- severe/sudden/chest/neuro/collapse/pregnancy red flag --> 112
   +-- urgent non-life-threatening --> 116 117 / practice
   +-- stable minor --> simple first aid + monitor
   +-- describe with OPQRST and change over time

D. I FEEL ENDANGERED --> Ch.3D + Ch.7
   |
   +-- present threat --> exit/safer place --> 110 / 112
   +-- expected/digital/coercive threat --> evidence + trusted person
   +-- violence against women support --> 116 016
   +-- after-effects --> Ch.4 + professional support

E. THINGS ARE CONGESTING --> Ch.3E + Ch.4
   |
   +-- write: prevent harm / soon / can be ugly
   +-- choose one physical action under five minutes
   +-- delegate or obtain care when essentials repeatedly fail

F. BAD SMELL --> Ch.3F
   |
   +-- gas/chemical/burning/symptoms --> no flame/switch --> leave
   |                                    112 from outside if danger
   +-- sewage/drain --> water trap + plumber/building management
   +-- damp/mould --> moisture inspection + professional repair
   +-- ordinary smell --> ventilation and cleaning, no combustion

G. NO PLACE TO GO --> Ch.3G + Ch.7
   |
   +-- no safe physical place --> municipal/social/shelter service
   +-- social overload --> pause, ally, exit, later conversation
   +-- internal crisis --> one person + 116 123 / 116 117
   +-- exposure/violence/self-harm/medical danger --> 112 / 110

OUTAGE / DISASTER --> Ch.6
   |
   +-- verify official warning
   +-- shelter or evacuate as instructed
   +-- air, medical needs, temperature, water, communication
   +-- food, medication, hygiene, roles
   +-- group scale --> logs, roles, meetings, accountability

EVERY NON-EMERGENCY ROUTE
   |
   +-- do one action
   +-- check better / same / worse
   +-- use backup
   +-- escalate on worsening, uncertainty, or red flag
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
  <section class="route-card" data-route="survival">
    <h3>OUTAGE</h3><p>Official warning · air · water · medication · roles</p>
  </section>
</div>

## Offline deployment checklist

- Print the monochrome PDF single-sided or duplex.
- Write local contacts in Ch.7 or the fillable table above.
- Keep the guide near a charged light source.
- Add a simple first-aid poster from an official provider.
- Store current medication and emergency plans nearby but privately.
- Refresh service numbers and medical guidance at each release.
- Test that QR codes or links are not the only access path.
- Ensure the print remains readable without colour.
- Replace the guide after water damage. It is not itself waterproof, despite
  strong thematic alignment.

## Update protocol

At each release:

1. recheck emergency numbers and official URLs;
2. review first-aid and preparedness guideline updates;
3. verify every numeric figure against `src/data/evidence_facts.json` and its primary or authoritative source;
4. run safety-regression and evidence-registry validation;
5. build colour and monochrome outputs;
6. inspect page count, clipped tables, diagrams, and text tree;
7. verify version strings across source, HTML, PDF, package, and changelog;
8. record removed claims, changed estimates, and uncertainty as well as added material.

## Notes page

Use this for local information, personal reminders, the name of a recommended
service, or simply moving thoughts out of your head.

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

## Second notes page — because v3.3 was extensive

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

## Navigation invariant

Every non-emergency route must provide:

1. a next action;
2. a backup;
3. a reason to escalate;
4. a named destination.

A dead end in prose is still a dead end.
