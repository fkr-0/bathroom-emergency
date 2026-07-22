---
title: "Start Here"
chapter: 1
revision: "4.2.0"
last_updated: "2026-07-22"
dependencies:
  - build/diagrams/emergency_flowgraph.png
  - build/diagrams/two_pass_route_map.png
  - build/diagrams/hazard_override_matrix.png
  - build/diagrams/evidence_classes.png
---

# Start Here — One Question at a Time

This guide is intentionally larger than a pocket card and intentionally simpler
than a medical degree. It contains quick routes for the first minute and deeper
explanations for the ten minutes after that, when the room has stopped spinning
quite so theatrically.

## The override

Run three short checks before choosing a topic:

1. **Life or medical danger?** Possible death, abnormal breathing,
   unconsciousness, severe bleeding, stroke sign, major injury, or lasting harm
   means **112**. “Maybe” and “cannot tell” count.
2. **Active violence or crime?** Move toward safety and call **110**. Use
   **112** when medical rescue or life protection is also needed.
3. **Environmental danger?** Fire, smoke, a CO alarm, gas, unknown fumes,
   chemical exposure, live electricity, or sparking means leave or isolate the
   source first and use **Situation H**. Call from a safer place.

You do not have to diagnose the person or the room before asking for help. “I am
not sure, but this looks serious” is a complete reason to call.

![Red-flag-first emergency decision flowgraph](build/diagrams/emergency_flowgraph.png)

![Two-pass routing architecture with dependency modifiers](build/diagrams/two_pass_route_map.png)

## Purpose

The guide helps with eight observable situations:

1. you caused trouble or someone depends on you;
2. anxiety, panic, overload, or dissociation;
3. pain or physical illness;
4. danger, coercion, or violence;
5. too many tasks and too little working memory;
6. a suspicious smell or household hazard;
7. no safe place, no plan, or disrupted infrastructure;
8. fire, smoke, gas, chemicals, electricity, or unsafe air.

Its job is to produce a **safe next action**, a **backup action**, and a clear
**escalation rule**. It is not a diagnosis engine, courtroom, therapist, poison
centre, obstetric ward, or tiny laminated government.

## Target audience

This is written for a stressed lay reader in Germany, including:

- the person having the problem;
- a friend trying to help without becoming an improvised professional;
- a host who wants a useful guide in a bathroom, hallway, shelter, or shared
  flat;
- a household preparing for outages and ordinary disasters;
- anyone whose brain currently has the processing power of a warm toaster.

Children should use it with a trusted adult when possible. Anyone with a known
medical condition should follow their individual emergency plan first.

## Quick-start procedure

Use two passes before reading deeply:

1. **Pass 1 — override.** Check life/medical danger, active violence/crime, and
   environmental danger in that order.
2. **Move first when the environment is unsafe.** Do not troubleshoot gas,
   smoke, electricity, or fumes from inside the exposure area.
3. **Pass 2 — choose the need.** Responsibility, alarm, body, threat/no place,
   household hazard, or outage.
4. **Apply modifiers.** Alone, child, pregnancy/postpartum, mobility or sensory
   access, medication, powered device, animal, language, and transport change
   logistics—not urgency.
5. **Do one action.** Keep the backup, escalation condition, and destination
   visible.
6. **Reassess.** Better, same, worse, or new red flag?

## Your current status

Before continuing, fill this line mentally or on paper:

> I am at **[location]**. I am **[alone / with someone]**. The immediate problem
> is **[one sentence]**. It began **[time]**. The next safe action is **[action]**.

If you cannot fill the line because someone is unresponsive, breathing
abnormally, bleeding heavily, or in immediate danger, the missing word is
**112**.

## Mathematical notation legend

This edition retains v3.3’s formulas, but every formula now wears a label so a
metaphor cannot sneak into the building dressed as physiology.

| Mark | Meaning | Example |
|---|---|---|
| $\lor$ | logical OR | any red flag activates emergency routing |
| $\Rightarrow$ | implies | red flag implies 112 |
| $\Delta$ | change between two observations | pain now minus pain earlier |
| $n$ | number of people or items | group size |
| $t$ | time | minutes, hours, or days as stated |
| **Protocol** | authoritative action rule | call 112 for abnormal breathing |
| **Descriptive equation** | exact relation once inputs are known | communication channels |
| **Conceptual model** | teaching aid, not a measured prediction | stepwise arousal model |
| **Mnemonic** | compact memory aid | action, backup, escalation |

No equation in this guide can overrule symptoms, a dispatcher, or common sense.
That would be a very ambitious equation.

## How to read the evidence figures

![Evidence labels used by the guide](build/diagrams/evidence_classes.png)

Version 4.2.0 keeps numbers and routes carefully bounded. Every evidence figure states:

- **what kind of evidence it is**—protocol, population estimate, study,
  association, or model;
- **who or what was measured**;
- **the denominator and time frame**;
- **uncertainty**, when the source reports it;
- **what the result does not permit you to conclude**.

A useful number answers a bounded question. A number without a denominator is a
rumour with a decimal point.

## Guide topology — a graph model

The guide can be treated as a directed graph $G=(V,E)$:

- each chapter or action is a node $v\in V$;
- each “go to,” “call,” or “reassess” instruction is an edge $e\in E$;
- **112** is a dominant emergency destination;
- every non-emergency route must eventually reach an action, a named support
  destination, or a safe exit.

A route is defective if it ends with “consider your options” while the reader is
still sitting on cold tiles with no trousers and a rising pulse.

### Navigation invariant

Every route must contain:

1. **one next action**;
2. **one backup** if that action fails;
3. **one escalation condition**;
4. **one destination** where the reader can continue.

## Flowchart legend

| Shape or style | Meaning |
|---|---|
| Red / emergency block | call 112 or 110 now |
| Question / diamond | choose the closest true answer |
| Action / rectangle | do the stated action |
| Rounded destination | continue in the named chapter or service |
| Dashed line | optional deeper explanation |
| Loop arrow | reassess only while no red flag exists |

In monochrome print, labels and wording carry the meaning; colour is never the
only signal.

## Four routes

<div class="route-grid">
  <section class="route-card" data-route="112">
    <h3>Red flag</h3>
    <p>Call 112. Then do only what the dispatcher asks and what is safe.</p>
  </section>
  <section class="route-card" data-route="medical">
    <h3>Body / pain</h3>
    <p>Go to Ch.5. Start with red flags, then simple first aid.</p>
  </section>
  <section class="route-card" data-route="calm">
    <h3>Panic / overload</h3>
    <p>Go to Ch.4. Orient outward, slow down, choose one action.</p>
  </section>
  <section class="route-card" data-route="support">
    <h3>Threat / responsibility</h3>
    <p>Go to Ch.2 or Ch.7. Safety first; repair comes after stabilization.</p>
  </section>
  <section class="route-card" data-route="survival">
    <h3>Environment unsafe</h3>
    <p>Go to Situation H. Leave or isolate the source before symptom sorting.</p>
  </section>
  <section class="route-card" data-route="survival">
    <h3>Outage / collapse</h3>
    <p>Go to Ch.6. Protect essential care, water, temperature, and information.</p>
  </section>
</div>

## The eight entry points

| Door | What is happening | First destination |
|---|---|---|
| A | I caused trouble or someone depends on me | Ch.2 Responsibility |
| B | I feel anxious, panicky, unreal, or flooded | Ch.4 Calm |
| C | I feel pain or physically unwell | Ch.5 First aid |
| D | I feel endangered or controlled | Ch.7 Safety and support |
| E | Everything is congesting | Ch.4 Calm, then one task |
| F | There is a bad or unknown smell | Ch.3F Safety check |
| G | I have no safe place or no workable plan | Ch.7 Practical support |
| H | Fire, smoke, gas, chemical, electrical, or unsafe air | Situation H Environmental hazards |

Several doors may be open. Red flags outrank all of them.

## Master flowchart — text version

Use this when the diagram is unavailable, inaccessible, or has acquired coffee:

```text
START
 |
 +-- Immediate danger, abnormal breathing, severe bleeding,
 |   unconsciousness, major burn, stroke sign, seizure,
 |   collapse, acute self/other danger?
 |       |
 |       +-- yes / maybe / unsure --> 112
 |       |                           speakerphone
 |       |                           unlock if safe
 |       |                           follow dispatcher
 |       |
 |       +-- no --> continue
 |
 +-- Active violence or crime needing police now?
 |       |
 |       +-- yes --> move to safety --> 110
 |       |          injury/life danger too --> 112
 |       +-- no --> continue
 |
 +-- Fire/smoke/CO/gas/chemical/electrical danger?
 |       |
 |       +-- yes / maybe --> leave or isolate safely
 |       |                 --> Situation H
 |       |                 --> 112 / poison centre / gas service
 |       +-- no --> continue
 |
 +-- Closest door:
         A responsibility/harm --> Ch.2 --> Ch.7 as needed
         B anxiety/panic       --> Ch.4
         C pain/body           --> Ch.5
         D danger/coercion     --> Ch.7
         E overload            --> Ch.4 --> one task
         F smell/fumes         --> Ch.3F --> leave/call if hazardous
         G no place            --> Ch.7
         H environment unsafe  --> Situation H
         outage/disaster       --> Ch.6

EVERY NON-EMERGENCY ROUTE:
  act once --> check better/same/worse --> escalate if worse --> repeat
```

## Basic theorem 1 — red-flag dominance

Let each red flag be a Boolean value $r_i \in \{0,1\}$:

$$R = r_1 \lor r_2 \lor \cdots \lor r_n$$

If $R=1$, the route is **112**. No anxiety score, pain score, formula, pulse
reading, or bathroom philosophy may cancel that result. This is a routing rule,
not a medical model.

## Basic theorem 2 — the one-next-action rule

Acute stress reduces the amount of information people can reliably hold and
use. The guide therefore keeps a tiny queue:

$$Q = [\text{one action},\; \text{one backup},\; \text{one escalation rule}]$$

Example: **sit down → call a friend → if chest pain or fainting appears, call
112**. A plan with twelve beautiful steps is decorative. A plan with one
executable step is equipment.[^who-stress]

## Quick-route summary

| Problem | First action | Backup | Escalation |
|---|---|---|---|
| panic / overload | sit, orient, exhale gently | call one person | 112 for red flags or acute danger |
| pain / illness | check red flags | 116 117 / practice | 112 for severe or sudden danger signs |
| responsibility | stop further harm | tell and repair | 112 / 110 when danger is live |
| violence | move to safety | trusted person / specialist service | 110 / 112 now |
| smell / fumes | no flame or switch | leave and warn others | 112 from outside if poisoning/fire possible |
| no place | secure the next hour | municipal/social support | 112 / 110 for exposure or danger |
| outage | verify official warning | conserve and coordinate | 112 for immediate hazard |

## Reassessment loop

1. **Act:** do the smallest safe action.
2. **Check:** better, same, or worse?
3. **Escalate:** if worse, new red flags appear, or uncertainty remains.
4. **Repeat:** only while the situation remains non-emergent.

This is the guide’s only intentional loop. It prevents both frozen inaction
and heroic improvisation.

## How to read the long sections

Each later chapter has two speeds:

- **Do now** material comes first and can be followed under stress.
- **Understand later** material explains why, adds options, and restores the
  breadth of v3.3 without forcing a lecture into the emergency minute.

Reading everything is not a prerequisite for deserving help. The appendix is
also not a boss fight.

[^who-stress]: World Health Organization, *Doing What Matters in Times of Stress* (2020), an evidence-informed and field-tested guide to grounding, unhooking from difficult thoughts, and values-based small actions: https://www.who.int/publications/i/item/9789240003927
