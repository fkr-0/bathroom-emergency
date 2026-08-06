# Threading the door sections into the Calm Guide

## Problem

The standalone Teal Book opens with two sections sliced out of the shared door
chapter — `B — I feel anxious` and `E — Overload is a queueing failure` — so the
book's own material starts at `calm.2`, and a reader meets the letters `B` and
`E` with nothing on the page explaining what they are.

Deleting them is not an option and never was: together they are 8,004 characters
of genuine content (the four-layer alarm decomposition, panic vs. emergency, the
GAD-7 spectrum, cognitive load, sleep debt, and three practical triage tools)
that exists nowhere else in the book.

## Observation that makes this easy

The Calm Guide's own opening already says:

> Anxiety merges sensation, prediction, memory, and obligation into one enormous
> notification. Separate them. Change one variable.

That is section B, compressed into three sentences. B says the same thing with a
table, a figure, and a worked decomposition. They are not two topics that need
reconciling; they are the same move at two levels of detail. B does it properly,
so B should carry it and the opening should hand off to it.

## Running order

Scope: the **standalone** book only. The master guide keeps `03-situations-b-g.md`
as its routing chapter, where the doors belong and where the letters are
explained by their neighbours.

| # | Source | Section | Role |
|---|---|---|---|
| 1 | `04-calm-guide.md` | opening prose | you made it here |
| 2 | `03-situations-b-g.md` | B: split the experience, panic, GAD-7, stress response | **what is actually happening** |
| 3 | `03-situations-b-g.md` | E: cognitive load, sleep debt | **when it is overload, not anxiety** |
| 4 | `04-calm-guide.md` | a pause needs no legal brief | permission |
| 5 | `04-calm-guide.md` | the 90-second landing | first physical action |
| 6 | `04-calm-guide.md` | breathing exercises | the menu |
| 7 | `04-calm-guide.md` | decay curve, Yerkes–Dodson, polyvagal | why any of this works |
| 8 | `04-calm-guide.md` | control panel, comfort inventory | adjust the room |
| 9 | `03-situations-b-g.md` | E: three-line triage, congestion board, five-minute reboot | **traffic control** |
| 10 | `04-calm-guide.md` | unhook, five-minute values bridge | thought and direction |
| 11 | `04-calm-guide.md` | leaving, nice-place map | exit |
| 12 | `04-calm-guide.md` | when calm is not enough, plan for another person | escalate, then help |

Diagnose → land → understand → adjust → triage → leave → escalate.

Note that E splits in two. Its explanatory half (why the brain is crashing)
belongs with the other explanations at step 3; its three practical tools are
task-management and belong after the room is already calmer, at step 9. Keeping
them together was what forced the whole section to the front.

## Retitling

The letters are routing labels from the hub and mean nothing inside a book:

- `B — I feel anxious` → `What is actually happening`
- `E — Overload is a queueing failure` → `When it is overload, not anxiety`
- E's tool half → `Traffic control`

## Mechanism

`canonical_blocks()` currently returns whole chapters plus one all-or-nothing
`mixed_sections(owner)` slice. It needs section-level granularity: an optional
per-node running order naming `(chapter, heading)` pairs, falling back to
current behaviour for books that do not declare one.
