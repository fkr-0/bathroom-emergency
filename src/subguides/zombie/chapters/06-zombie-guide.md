---
title: "The Olive Book — Zombie Guide"
chapter: 6
revision: "5.1.2"
last_updated: "2026-08-14"
dependencies:
  - build/diagrams/dependency_continuity_map.png
  - build/diagrams/survival_pyramid.png
  - build/diagrams/scaling_chart.png
  - build/diagrams/vega_household_water_stock.png
  - build/diagrams/vega_communication_channels.png
  - build/diagrams/vega_continuity_dependencies.png
  - build/diagrams/household_continuity_board.png
  - build/diagrams/first_meeting_roles.png
---

# The Olive Book — Zombie Guide

No confirmed zombie outbreak is known. Power cuts, floods, heat, cold,
contaminated water, smoke, communication failures, and groups improvising a
constitution before locating the first-aid kit are real enough.

Infrastructure is invisible right up until it stops. Then everything you never
had to think about — water, warmth, medication, charging, sewage, transport,
and knowing what is actually true — arrives at once, as a queue, and wants
handling in order.

Which is the real work. Not wilderness theatre: **continuity engineering and
queue management, with worse lighting.**

This book is for disruptions where ordinary infrastructure still exists in some
form but one or more essential household functions are limited, failing, or
uncertain. It keeps those functions visible, assigned, backed up, and reviewed.
It does not replace live warnings, evacuation instructions, clinical device
plans, or emergency services.

## Verify before optimizing

Before rationing toothpaste or founding a perimeter committee, verify that the
crisis exists and identify what kind of failure is actually occurring.

1. Check official warnings: **NINA**, Cell Broadcast, local radio, municipality,
   police, fire service, or BBK.[^bbk-warning]
2. Identify the hazard: fire, flood, chemical release, outage, heat, cold,
   violence, or ordinary rumour wearing tactical trousers.
3. Decide whether authorities say **shelter** or **evacuate**.
4. Tell one other person what you know and where you are.
5. Recheck the source before forwarding it.

> **Live official instructions outrank this static book.**

Cell Broadcast is deliberately short. Use a fuller official channel — NINA,
local radio, the federal warning portal — for detail and updates when you
can.[^bbk-warning]

Do not leave a safe building merely because a group chat has cinematic energy.

## The continuity invariant

A disrupted household is easier to reason about as functions than as a pile of
objects. For every essential function that is active, limited, failed, or
uncertain, record:

1. **status** — what works right now?
2. **reserve** — how much safe time, stock, charge, treatment, or support
   remains?
3. **owner** — who is actually checking it?
4. **backup** — who or what takes over?
5. **next action** — what visible physical action happens next?
6. **review** — when will this be checked again?
7. **failure route** — what condition changes the plan or calls in outside help?

“Someone is handling water” is not continuity. “Mara checks the sealed-water
count at 18:00; Deniz is backup; below twelve litres we call the distribution
point” is.

![Household continuity systems and ownership fields](build/diagrams/household_continuity_board.png)

| Function | Status question | Record now |
|---|---|---|
| information | what is confirmed and when is the next update? | source, owner, next check |
| air and hazard | is the place safe to occupy? | safe area, re-entry authority |
| care and power | what treatment, device, medicine, or caregiver cannot pause? | runtime, approved backup, destination |
| water | what is safe and how much remains? | stock, rate of use, refill route |
| temperature and shelter | can everyone stay dry, ventilated, warm or cool enough? | vulnerable people, room status, move trigger |
| food and cooking | what can be prepared safely with current water and power? | refrigeration, allergies, next meal |
| sanitation | how are hands, toilets, waste, and clean zones separated? | toilet status, waste route, supplies |
| access and transport | who cannot receive a warning, leave, enter, or travel without help? | person, helper, route, keys, communication |

## First minutes — protect what fails fastest

The exact order depends on the hazard. A useful default:

1. immediate safety and breathable air;
2. urgent medical needs;
3. protection from heat, cold, wind, and rain;
4. reliable water;
5. communication and location;
6. medication, essential care, and food continuity;
7. sanitation and longer-term organization.

Food is important. It is rarely the first ten-minute problem unless someone has
a condition requiring immediate intake.

![Priority pyramid for disrupted infrastructure](build/diagrams/survival_pyramid.png)

Orange owns the live environmental hazard. Red owns immediate first aid. Blue
owns relocation when the current place cannot support a person. Indigo owns the
professional system. Olive owns the continuity queue once the next safe action
is known.

## Water — priority zero after air and immediate safety

Current BBK guidance is that an adult needs at least **1.5 litres of fluids per
day**, and that if you plan to cook you should allow about **0.5 litres of water
per day on top**.[^bbk-stock] Adding those gives this guide its deliberately
simple planning estimate:

$$W_{plan} = 2nd\;\text{litres}$$

for $n$ people over $d$ days. That is a stock-planning convention of ours, not a
physiological law, and not a number BBK publishes.

{{visualization:vega-household-water-stock}}

BBK suggests managing for **ten days** where practical, while saying plainly
that a stock for **at least three days already helps a great deal** and can be
built up gradually.[^bbk-stock] At the two-litre planning value, one person has
6 L for three days or 20 L for ten; a four-person household, 24 L or 80 L.
Containers, weight, storage space, and rotation are part of the equation even
when algebra would prefer not to carry bottles upstairs.

Add pet needs. Heat, illness, pregnancy, breastfeeding, medication, and physical
work can all increase requirements.

- Store potable water in clean food-safe containers.
- Rotate stock according to product and container guidance.
- Follow local boil-water or **do-not-use** notices exactly.
- Filtering cloudy water through cloth removes particles, not dissolved
  chemicals or all microorganisms.
- Boiling does not remove fuel, solvents, pesticides, salt, or radioactive
  contamination.
- Do not use generic bleach-drop recipes: products and concentrations differ.
- Separate drinking-water containers from washing and waste containers.

### Finding and evaluating water

In a genuine emergency, official distribution points and sealed household
supplies beat improvised natural sources. Surface water can carry
microorganisms, sewage, agricultural runoff, or chemicals even when it looks
clear.

If no safe source exists, contact the responsible local authority for current
instructions, and emergency services when there is an actual emergency. A
four-line universal purification recipe would be comforting, compact, and
dishonest.

## Essential medication and powered-device continuity

![Essential treatment and powered-device continuity map](build/diagrams/dependency_continuity_map.png)

An outage becomes a medical route when a treatment, device, storage condition,
caregiver, or accessible transport cannot be safely bridged. Do not wait for the
last battery bar to become emotionally persuasive.

1. **Identify the function.** Which treatment or device is essential? What
   failed? How much approved battery runtime, medication, oxygen, cooling, or
   caregiver coverage remains?
2. **Use the approved bridge.** Switch only to a battery, reserve, alternate
   administration method, backup caregiver, or powered destination already
   specified by the care team or manufacturer.
3. **Call early.** Contact the supplier, pharmacy, prescriber, care service, or
   **116 117** while a safe bridge still exists. The medical on-call service is
   reachable around the clock for urgent problems that are not life-threatening;
   life-threatening emergencies belong to **112**.[^medical-route]
4. **Move before exhaustion.** Go to a known staffed, powered, accessible place.
   Tell them the device, treatment, remaining runtime, power need, mobility and
   communication needs, and transport constraints.

Call **112** when a life-supporting function is interrupted, breathing or
consciousness changes, or serious harm is imminent because the bridge or
transfer will fail before help arrives.

Do not improvise voltage, connectors, oxygen flow, refrigeration temperature,
medication dose, or fuel use. A technically creative adapter is not improved by
being attached to someone's breathing.

Record these before an outage:

| Field | Household value |
|---|---|
| essential device or treatment | |
| power draw / battery runtime / storage range | |
| approved backup and where it is | |
| supplier, pharmacy, prescriber, care service | |
| accessible powered destination | |
| transport and who can help | |
| 112 escalation condition | |

## Shelter and temperature

Exposure can become urgent long before hunger.

Use the available building or location only if it is safer than the hazard.
Hazard-specific movement belongs to Orange and to current official instructions:

- **flood:** move away from flowing water; follow evacuation or shelter orders;
- **fire/smoke:** leave by a safe route; never choose smoke as shelter;
- **chemical release:** follow official indoor-shelter or evacuation guidance;
- **cold/wind/rain:** stay dry, block wind, insulate from the ground, add layers;
- **heat:** seek shade or a cooler space, reduce exertion, drink normally when
  safe, check vulnerable people;
- **storm:** avoid windows, loose objects, trees, and exposed structures.

For outdoor temporary shelter, insulation below the body matters as much as
material above it. Use dry clothing, mats, cardboard, blankets, or vegetation
only when safe and permitted. Do not choose flood channels, unstable slopes,
rockfall zones, dead trees, or a charming patch directly beneath lightning.

### Cold

If you suspect **hypothermia** rather than ordinary cold, call **112**. Current
DRK first-aid guidance routes hypothermia to emergency services at both stages
it describes — this is not a judgement call about whether it has become
“significant” yet.[^drk-cold]

While waiting, and while the person is still shivering and fully awake:

- get them out of wind and wet, into a warm place;
- remove wet clothing and wrap them in dry blankets;
- warm them **slowly**;
- if they are fully conscious, warm sweet drinks such as tea are fine — never
  alcohol;
- **no rubbing, no hot water bottle, no intense direct heat.**

If shivering stops and they become drowsy, stiff, or hard to rouse, that is the
more serious stage: **stop trying to warm them**, keep them covered and still,
and wait for the ambulance. If they are unconscious but breathing normally, use
the recovery position. If they are not breathing normally, start CPR.

Note that one instruction does not change between the stages: no rubbing and no
direct heat, ever. Cover, do not scrub.

### Heat

- move to shade or a cooler place;
- reduce exertion and excess clothing;
- drink normally when safe;
- cool the skin with water and airflow;
- check infants, older adults, chronically ill people, pregnant people, and
  anyone unable to communicate or move independently;
- call **112** for confusion, collapse, seizure, markedly altered consciousness,
  or another severe heat illness.[^bbk-heat]

## Air, fire, and carbon monoxide

Never operate a **generator, charcoal grill, or any other appliance meant for
outdoor use** inside a home, garage, cellar, tent, or bathroom. BBK's own outage
guidance is blunt about the grill: not in the flat, not in the house, because of
the suffocation risk.[^bbk-power] Fire-service guidance is the same for
generators and charcoal, and notes that an open door or window does not make an
enclosed space safe.[^dfv-co]

The test is not the fuel, it is the approval. If an appliance is not
specifically intended and installed for indoor use, treat it as outdoor-only.
For equipment that *is* intended for indoors — an installed gas heater, for
instance — follow its ventilation and manufacturer requirements exactly; BBK
recommends professional advice for alternative heating, safety devices such as
oxygen-deficiency and flame-failure cut-offs, and a carbon-monoxide
detector.[^bbk-power]

Carbon monoxide is colourless and odourless. Move to fresh air and call **112**
if poisoning is suspected.

An unknown gas or chemical smell means no matches and no electrical switches.
Follow Orange's source-location rule and current official instructions; for a
suspected gas release, leave by a safe route and call from outside.

## Food

- Use refrigerated perishables first while they remain safe.
- Keep fridge and freezer doors closed during outages.
- Follow official discard guidance after prolonged outages or flooding.
- Smell and appearance cannot detect every pathogen or toxin.
- Store familiar foods household members can actually eat and prepare with the
  water and energy available.
- Include infant, allergy, disability, cultural, and pet needs.
- Do not forage from a bathroom guide. Plant identification by vibes has a poor
  safety record.

## Medication

- Keep an up-to-date medication and allergy list.
- Maintain a reasonable reserve agreed with prescriber or pharmacy.
- Plan refrigeration, power, administration equipment, and replacement routes.
- Keep medicines dry, labelled, and away from children.
- Do not ration or substitute prescription medicines without professional advice
  unless an emergency plan specifically instructs it.

## Energy

Use energy in this order unless the actual situation changes it:

1. life-supporting medical devices and emergency communication;
2. lighting and information;
3. refrigeration where medically or food-safety critical;
4. cooking and thermal comfort;
5. everything else.

- Charge devices while power exists.
- Use power banks and batteries safely.
- Keep flame-based lighting away from gas, oxygen, children, and combustibles;
  battery lights are preferable.
- Never back-feed household wiring with an improvised generator connection.
- Follow manufacturer guidance for every appliance and fuel source.

Do not spend the first hour colour-coding canned beans while smoke enters the
stairwell.

## Hygiene and toilet failure

Reserve clean water for drinking and essential food preparation. Keep hands
clean after toilet use and before handling food. Separate clean and dirty zones.
If toilets fail, follow municipal sanitation guidance and keep waste away from
food, living areas, and water sources.[^bbk-hygiene]

Useful supplies: soap, sanitizer where appropriate, toilet paper, menstrual
products, nappies, waste bags, gloves, disinfectant used according to label, and
personal care supplies.

## Reading traces and observing the environment

“Reading traces” means situational awareness, not wilderness detective theatre:

- note water level, smoke direction, wind, damaged power lines, unstable walls,
  blocked exits, animal behaviour, traffic, and official markings;
- compare changes over time;
- photograph conditions when safe;
- mark hazards for others when useful;
- never enter a dangerous area merely to obtain better evidence.

Observation serves decisions. It does not make the observer invulnerable.

## Mini collapsing-society guide — or, more often, several bad days with broken infrastructure

The phrase is deliberately dramatic. Most real events are temporary service
failures, local disasters, evacuations, or strained institutions. Behave in a
way that still makes sense when the power returns and everyone remembers your
name.

### Account before acquiring

1. inventory before acquiring more;
2. record owners and shared stock;
3. prioritize water, medication, food safety, warmth and cooling,
   communication, care supplies, and sanitation;
4. avoid dangerous or illegal entry;
5. distribute shared resources by need and agreed rules;
6. keep a visible reserve rather than hiding every uncertainty in one cupboard.

| Resource | Quantity | Daily use | Owner/shared | Reorder/escalation |
|---|---:|---:|---|---|
| water | | | | |
| medication | | | | |
| food | | | | |
| batteries | | | | |
| hygiene | | | | |

### Capability inventory

Supplies are only one kind of capacity. Record the human and infrastructural
capabilities too:

| Capability | Person / place | Available until | Backup |
|---|---|---|---|
| first aid or clinical knowledge | | | |
| medication, device, or care knowledge | | | |
| translation or communication access | | | |
| repair, electrical, plumbing, or building knowledge | | | |
| transport, lifting, or accessible transfer | | | |
| cooking, sanitation, childcare, or animal care | | | |
| radio, printing, mapping, or record keeping | | | |

Do not turn a skilled person into an inexhaustible public utility. Name relief,
backup, and a handoff route for them as well.

### Check people whose continuity may fail sooner

Check people who may have difficulty receiving warnings, evacuating, obtaining
supplies, regulating temperature, or communicating:

- children;
- older adults;
- disabled and chronically ill people;
- pregnant and postpartum people;
- isolated neighbours;
- people dependent on electricity, refrigeration, oxygen, medication, or care;
- people exposed to violence or homelessness;
- animals.

Ask what support is wanted. Do not convert vulnerability into permission to
remove autonomy.

## Several households — coordinating without inventing a tiny dictatorship

When several people share infrastructure, individual continuity becomes a
coordination problem. That does not mean panic and selfishness. Research on real
emergencies repeatedly finds mutual aid, solidarity, and support, particularly
where people experience a sense of common fate or shared
identity.[^collective-emergency][^collective-recovery]

### The first meeting

Keep it short:

1. What happened, and what is confirmed?
2. Is anyone missing, injured, unsafe, or without essential care?
3. Which continuity systems are okay, limited, failed, or unknown?
4. What must happen in the next two hours?
5. Who owns each task, and who is backup?
6. When is the next briefing?
7. How can a person raise an urgent concern or a disagreement?

Minutes should record decisions, owners, backups, and review times — not every
sentence spoken while the biscuits were still available.

### Five functions for the first meeting

![Five operational functions for a short crisis meeting](build/diagrams/first_meeting_roles.png)

| Function | Owns |
|---|---|
| coordination | task board, owners, deadlines, next briefing |
| care | injury, medication, devices, children, dependants, animals |
| supplies | water, food, batteries, hygiene, stock and use rate |
| information | official sources, confirmed facts, uncertainty, update time |
| access and logistics | exits, transport, entry, mobility, communication, destination |

One person may hold two functions in a small household. No function may exist
only in somebody's memory. Every role needs a visible log or handoff another
person can understand.

## The assignment invariant

A task is not assigned until it has:

1. a named owner;
2. a visible next physical action;
3. a deadline or review time;
4. a named backup or failure route.

“Someone check the batteries” is a wish. “Sam counts charged batteries by 19:00;
Lee records the result; no lighting reserve means we move the charging schedule
forward” is an assignment.

Confidence is not a credential. Build a route for dissent: a second check,
written uncertainty, or a person who can stop a plan when they see a hazard.

## Communication as the group grows

Do not derive a constitution from a head count. The practical pattern is
qualitative:

| Group condition | What starts breaking | Add next |
|---|---|---|
| very small, everyone talks directly | unstated assumptions, absent backups | explicit roles and check-ins |
| growing | missed tasks, the same conversation repeated | task board, shared briefing, backups |
| several teams | contradictory updates, information silos | shared log, representatives, handoffs |
| large or long-lived | informal authority, fatigue, lost memory | review, rotation, complaints, onboarding, nested teams |

Every time coordination gets harder, communication and accountability have to
grow with it. Adding people without adding structure is not community scaling;
it is a larger argument.

Useful channels: a bulletin, a radio channel, a shared log, a scheduled
briefing, clearly named coordinators. The aim is not maximum communication. It
is getting the same important fact to the people who need it without making
every person relay every message.

## Cooperation and collective resilience

Groups under threat can show rumour, conformity pressure, conflict, exhaustion,
and in-group/out-group thinking. They also, repeatedly and measurably, show
rapid mutual aid and strong solidarity — crowds in real emergencies are not the
selfish stampede of disaster films.[^collective-emergency] Shared identity and
observed support are associated with collective efficacy and well-being during
recovery, not merely during the dramatic hour.[^collective-recovery]

Treat cooperation as a capacity to support, not a miracle to assume or a myth to
dismiss.

- publish confirmed facts and uncertainty separately;
- correct rumours without humiliating the person;
- begin cooperatively where it is reasonably safe;
- make expectations and resource rules visible;
- respond to exploitation proportionately;
- allow repair after a breach where safety permits;
- record shared-resource decisions;
- avoid humiliating punishment, which only creates future conflict inventory;
- rotate exhausting or powerful roles;
- create complaint and appeal routes;
- include affected minorities and people with access or care needs;
- schedule rest, and keep ordinary rituals such as meals and check-ins.

**Game theory is not permission to call your neighbour “Player B” while taking
his batteries.**

## Water, energy, and hygiene at group scale

At group scale, assign named roles and logs:

| System | Minimum controls |
|---|---|
| water | source, treatment status, storage, allocation, contamination report |
| food | inventory, allergies, refrigeration status, cooking fuel |
| energy | priority loads, charging schedule, fuel safety, shutdown authority |
| sanitation | toilet plan, handwashing, waste route, cleaning responsibility |
| health | medication, first aid, vulnerable-person checks, referral route |
| information | official source, update time, rumour correction, meeting point |

## If the disruption lasts — shared rules without emergency cosplay

Do not invent a government in the first ten minutes. But if several households
are managing shared resources for days or longer, resource rules and
accountability stop being politics and become continuity infrastructure.

> **Improvised group governance does not override evacuation orders, emergency
> services, clinical plans, public-health instructions, or an authority already
> responsible for the incident.**

Nobody needs to hold a participatory vote on whether the fire brigade's
evacuation order has sufficient democratic legitimacy.

### Forms of self-administration

| Model | Strength | Risk | Good use |
|---|---|---|---|
| coordinator | fast | dependency or unchecked power | immediate short crisis |
| majority vote | clear decision | minority needs ignored | bounded choices |
| consensus | broad support | slow or blocked | small trusted group |
| consent | proceed unless reasoned objection | requires facilitation | operational teams |
| delegated teams | expertise and speed | silos | larger, multi-team work |
| rotating roles | distributes power and fatigue | continuity loss | ongoing work |

Use different models for different decisions. Nobody needs consensus on calling
112. Everyone affected should have a meaningful voice in long-term rationing
rules.

### Ostrom's commons principles — useful later, not emergency scripture

Long-lived self-governed commons often include:[^ostrom]

1. clear boundaries around resource and users;
2. rules fitted to local conditions;
3. participation by affected users in changing rules;
4. monitoring accountable to the group;
5. graduated responses to rule violations;
6. accessible conflict resolution;
7. recognition of the group's right to organize;
8. nested layers for larger systems.

The bathroom translation: define the water, define the users, write the rule,
record use, and resolve conflict before somebody declares themselves Hydration
Chancellor.

## Self-defence is not a continuity strategy

Priority order:

1. avoid and leave when it is safely possible;
2. create barriers, distance, light, witnesses, and communication;
3. contact police or emergency services;
4. protect vulnerable people without creating another casualty;
5. if immediate defence becomes unavoidable, use only what is necessary to stop
   the attack that is happening now;
6. obtain medical and qualified legal help afterward.

This guide does not teach weapons, traps, combat, vigilantism, or property
violence. German self-defence law is fact-specific: §32 StGB defines Notwehr as
the defence *necessary* to avert a present unlawful attack on oneself or
another.[^stgb32] Every word in that sentence has done years of litigation. Blue
and Indigo own the safety and legal-routing detail.

## Evacuation pocket list

Take what is immediately useful without delaying an urgent evacuation:

- phone and power bank;
- medication and medication list;
- ID, keys, payment method, essential documents;
- water and simple food;
- weather layer and sturdy shoes;
- small first-aid kit;
- glasses, hearing aids, mobility and communication supplies;
- infant, disability, menstrual, and pet supplies;
- radio or warning access;
- written destination, meeting point, and contact.

Leave weapons, looting fantasies, and twelve kilograms of philosophical
literature unless the authorities have specifically requested an ethics seminar.

## Preparedness checklist — before anything happens

| Area | Ready? | Next action |
|---|---|---|
| official warning apps / radio | ☐ | |
| water and familiar food | ☐ | |
| medication and care supplies | ☐ | |
| lights, batteries, charging | ☐ | |
| documents and contacts | ☐ | |
| household evacuation plan | ☐ | |
| support plan for dependants | ☐ | |
| fire/CO safety | ☐ | |
| hygiene and toilet failure plan | ☐ | |
| neighbour / mutual-aid contact | ☐ | |

BBK maintains the fuller national checklist and keeps it current, which is a
better place for the details than a book printed once.[^bbk-ratgeber]

Preparedness is not a personality or a bunker aesthetic. It is the quiet removal
of tomorrow's stupidest problems.

## Optional reading — models that are not prerequisites for action

If air, water, medical care, shelter, or a safe destination is failing, go back
to the operational sections. These are kept because they explain useful ideas,
not because a crisis owes you time to finish the maths.

### Survival probability — valid mathematics, unusable prophecy

A standard survival function can be written as

$$S(t)=\exp\left(-\int_0^t h(u)\,du\right)$$

where $h(u)$ is a hazard rate. Without measured hazards it predicts nothing
whatsoever about your personal future. Its practical lesson is simpler: reduce
known hazards — smoke, unsafe water, cold, heat, isolation, untreated illness —
instead of inventing a percentage for survival.

### Heat balance — explanatory, not a bathroom calculation

A conceptual heat balance:

$$\Delta H = M - (C + K + R + E)$$

where $M$ is metabolic heat and the remaining terms are convection, conduction,
radiation, and evaporation. It explains why wind, wet clothing, ground contact,
shade, airflow, and exertion matter. It is not a home calculator for declaring
somebody safe.

### Architecture audit — which functions are coupled?

{{visualization:vega-continuity-dependencies}}

This is an audit of this guide's own model, not a hazard score. **Depends on**
counts prerequisites named by one system; **supports** counts how many other
systems name it. A high count means “expect handoffs and cascading effects,” not
“this will fail first.”

### Pairwise channels — exact arithmetic, qualitative lesson

A fully connected group of $n$ people has

$$C(n)=\frac{n(n-1)}{2}$$

unique pairs.

{{visualization:vega-communication-channels}}

The arithmetic is exact. Organizational thresholds derived from it are not: no
particular head count makes a shared log necessary. The real lesson is that
“everyone tells everyone” grows expensive and fragile, so shared logs,
briefings, and explicit handoffs replace it when direct conversation stops being
reliable.

### Dunbar numbers — descriptive research, not a crisis zoning code

Research on social network layers describes relationships as roughly nested
circles of different sizes. These are interesting observations about human
social organization, not thresholds for deciding when your block needs a
minister of batteries.

What survives as practical advice:

- nobody can maintain every relationship equally;
- smaller working groups execute; larger groups keep records;
- a community is not failing merely because it contains subgroups.

### Prisoner's dilemma — one model among better ones

Repeated-game models illustrate one reason cooperation can be stable: people
expect to meet again, can observe behaviour, and have ways to respond to
breaches and restore cooperation. It is a tidy story and it is not the main
one. Real disaster cooperation runs on shared identity, common fate, norms,
material conditions, and institutions — which is why the operational advice in
this book cites emergency research rather than
game theory.[^collective-emergency][^collective-recovery]

### Pareto principle — useful attention, not a literal law

The 80/20 rule is a heuristic, not an emergency equation. A few actions often
produce most of the immediate benefit:

- leave the active hazard;
- call for help;
- protect air and temperature;
- secure water, medication, and essential care;
- establish reliable information and roles.

### Scaling chart — architecture sketch, not population law

![Coordination scaling from one person to a community](build/diagrams/scaling_chart.png)

The chart is kept as an architecture sketch. Do **not** read its head-count
bands as empirical cut-offs. The operational text uses the qualitative
transition instead: direct coordination → written assignments → shared logs and
teams → explicit accountability and institutional memory.

[^bbk-warning]: Bundesamt für Bevölkerungsschutz und Katastrophenhilfe (BBK), “Warn-App NINA” and “Cell Broadcast.” NINA carries official civil-protection warnings with weather and flood information; Cell Broadcast pushes short official warnings to compatible mobile devices and is designed to be supplemented by a fuller channel. https://www.bbk.bund.de/DE/Warnung-Vorsorge/Warn-App-NINA/warn-app-nina_node.html and https://www.bbk.bund.de/DE/Warnung-Vorsorge/Warnung-in-Deutschland/So-werden-Sie-gewarnt/Cell-Broadcast/cell-broadcast_node.html

[^bbk-stock]: BBK, “Essen und Trinken bevorraten.” Current text: an adult needs at least 1.5 litres of fluid per day, with about 0.5 litres of water extra per day if cooking is planned; aim where possible for ten days of self-supply, though a stock for at least three days already helps considerably and can be built up in stages. The combined 2 L/person/day figure used above is this guide's own planning convention. https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/So-koennen-Sie-sich-vorbereiten/Bevorraten/bevorraten.html

[^bbk-power]: BBK, “Vorsorge und Handeln bei Stromausfall.” Covers alternative heating, oxygen-deficiency and flame-failure safety devices for gas appliances, carbon-monoxide detectors, cooking without mains power, and the explicit warning not to use a grill inside the flat or house because of the suffocation risk. https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/Stromausfall/stromausfall_node.html

[^dfv-co]: Deutscher Feuerwehrverband, carbon-monoxide prevention guidance: charcoal grills and generators do not belong in enclosed spaces, and an apparently open door or window does not make them safe. https://www.feuerwehrverband.de/feuerwehrverband-klaert-auf-rechtzeitige-warnung-vor-kohlenmonoxid-vergiftungen-bieten-nur-co-melder/

[^drk-cold]: Deutsches Rotes Kreuz, “Erfrierungen und Unterkühlungen.” DRK routes both described stages of hypothermia to 112. Stage I: warm place, slow warming, remove wet clothing, wrap in blankets, no active heat by rubbing or hot water bottle, warm sweet non-alcoholic drinks if the person is conscious. Stage II (slowed breathing, muscle rigidity, drowsiness or unconsciousness): no further warming attempts, recovery position if unconscious and breathing, CPR if breathing is not normal. https://www.drk.de/hilfe-in-deutschland/erste-hilfe/erfrierungen-und-unterkuehlungen/

[^bbk-heat]: BBK, current heat guidance: cooling, hydration, reduced exertion, checks on vulnerable people, and emergency escalation for severe heat illness. https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/Mit-Naturgefahren-umgehen/Hitze-Duerre/hitze-duerre_node.html

[^bbk-hygiene]: BBK, “Hygiene in Notsituationen,” including water-saving hygiene and preparation for toilet failure. https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/Gesundheit-und-Hygiene/Hygiene-in-Notsituationen/hygiene-in-notsituationen_node.html

[^bbk-ratgeber]: BBK, *Ratgeber und Checkliste für Notfallvorsorge und richtiges Handeln in Notsituationen*, the maintained national preparedness guide. https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/Ratgeber-Checkliste/ratgeber-checkliste_node.html

[^medical-route]: 116117 Patientenservice / ärztlicher Bereitschaftsdienst. The service states it is reachable around the clock, 24 hours a day and seven days a week, for urgent problems that are not life-threatening; life-threatening emergencies belong to 112. https://www.116117.de/de/aerztlicher-bereitschaftsdienst.php

[^collective-emergency]: Drury J, Cocking C, Reicher S, “Everyone for themselves? A comparative study of crowd solidarity among emergency survivors,” *British Journal of Social Psychology* 48 (2009): 487–506. https://doi.org/10.1348/014466608X357893

[^collective-recovery]: Ntontis E, Drury J, Amlôt R, Rubin GJ, Williams R, Saavedra P, “Collective resilience in the disaster recovery period: Emergent social identity and observed social support are associated with collective efficacy, well-being, and the provision of social support,” *British Journal of Social Psychology* 60 (2021): 1075–1095. https://doi.org/10.1111/bjso.12434

[^ostrom]: Elinor Ostrom, “Beyond Markets and States: Polycentric Governance of Complex Economic Systems,” Nobel Prize Lecture (2009). https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/lecture/

[^stgb32]: Strafgesetzbuch §32 Notwehr: “Notwehr ist die Verteidigung, die erforderlich ist, um einen gegenwärtigen rechtswidrigen Angriff von sich oder einem anderen abzuwenden.” https://www.gesetze-im-internet.de/stgb/__32.html
