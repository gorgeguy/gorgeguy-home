# PB Tourney — Reviewer Introduction

## Executive Summary (For Busy Reviewers)
PB Tourney is an attempt to make **small, local pickleball tournaments easier to run and easier to play**.

If you’ve been part of local tournaments, you’ve probably seen the same challenges: a director overloaded with questions, players waiting to report scores or find their next match, and limited visibility into standings until everything is over. PB Tourney aims to reduce that friction by making score reporting, match discovery, and tournament status **self-service and always up to date**.

The goal is simple: take routine load off the director and give players clearer, faster answers.

## How to Review This
As you review PB Tourney, think about it from the perspective of someone *running* or *playing* in a real tournament. Consider whether the problems described here match what you’ve seen in practice, whether the objectives align with what actually matters during live play, and whether this approach would make tournaments feel more fluid for players and directors.

Feedback of all kinds is welcome — including ideas about features, usability, and polish — especially when tied back to how they would improve the real tournament experience. Even quick, instinctive reactions are valuable.

---

## Purpose of This Document
This document is intended for **experienced pickleball players and tournament directors** who are reviewing PB Tourney. A technical background is *not* required.

The purpose of this document is to ask a very specific kind of feedback:

- Does this accurately describe the problems you experience running or playing in local tournaments?
- Are the objectives the *right* ones?
- Does the application, as designed so far, meaningfully improve the experience for both players and directors?

Rather than focusing on software details, this document frames PB Tourney in terms of **real tournament workflows**, **human bottlenecks**, and **information flow during live play**.

---

## The Environment PB Tourney Is Built For
PB Tourney is designed primarily for **small, local pickleball tournaments** — often run by clubs or volunteers — where:

- Tournaments are informal or semi-formal
- Directors often juggle many responsibilities alone
- Players are accustomed to asking questions in person
- Pen-and-paper systems (clipboards, printed sheets, pencil scores) are still common

The continued use of manual systems is taken as a signal that existing software solutions may be:
- Too expensive
- Too complex
- Or poorly matched to how these tournaments actually run

PB Tourney intentionally targets this lower end of the spectrum.

---

## The Two Primary Roles
PB Tourney is designed around two roles:

- **Players** — participants focused on playing matches with minimal administrative friction
- **Tournament Directors** — organizers responsible for setup, scheduling, scoring, and flow

Each role has distinct needs, especially during *live tournament play*.

---

## Player Needs During a Tournament
From a player’s perspective, a tournament system should reliably answer three questions at all times:

1. **How do I report my score?**
   - Players need a fast, unambiguous way to submit match results
   - Reporting should not require tracking down the director

2. **What is my next match?**
   - Who am I playing?
   - When is the match ready to start?
   - Which court should I go to?

3. **Where do I stand in the tournament?**
   - Current rankings or standings
   - Tournament progress
   - Elimination status (when applicable)

In many local tournaments today, players satisfy these needs by repeatedly visiting the director — reporting scores, asking questions, and returning later when matches are not yet ready. PB Tourney aims to reduce this uncertainty and waiting.

---

## Tournament Director Needs
Tournament directors typically want to:

- Get players signed up prior to the tournament
- Define the tournament format (number of rounds, number of courts)
- Schedule matches
- Assign matches to courts
- Record scores accurately
- Keep the tournament moving smoothly

In small tournaments, all of this often happens with a clipboard as the single source of truth. Directors are frequently interrupted by players asking questions, which increases cognitive load and slows overall flow.

PB Tourney is designed to offload routine questions and score reporting to the system, allowing directors to focus on oversight and exceptions rather than constant manual updates.

---

## What Is PB Tourney?
PB Tourney is a **web-based pickleball tournament management application** designed to support *live tournament execution*.

Key characteristics:
- Mobile-friendly web application (with native mobile apps planned, especially for players)
- Real-time updates so information reflects the current state of play
- Player self-service for score reporting and match discovery
- Designed to improve clarity and flow during live tournaments

Although the domain is pickleball, many of the challenges PB Tourney addresses — coordination, state changes, and reducing human bottlenecks — are broadly applicable.

---

## Core Objectives
PB Tourney is built around a small set of explicit objectives:

- Reduce the operational load on tournament directors
- Give players self-service access to the information they need
- Make the current state of the tournament obvious and trustworthy
- Improve flow by reducing waiting, ambiguity, and repeated interruptions

Design decisions should be evaluated against how well they support these goals.

---

## What Feedback Is Most Valuable
As a reviewer, feedback is especially valuable on:

- Whether the problem statement reflects your real experience
- Whether the objectives match what *actually* matters during tournaments
- Where the application succeeds or falls short in meeting those objectives
- What feels unnecessary, missing, or mismatched to local tournament reality

Feedback does *not* need to be technical to be useful.

---

## Where This Could Go
PB Tourney is an evolving project. There is an intent to eventually **monetize** the application, but the specific model is intentionally undecided.

No formal market or competitive analysis has been done yet. This is deliberate. The current focus is on:

- Understanding the problem deeply
- Exploring solutions creatively
- Building something that genuinely improves local tournaments

The belief motivating this work is that modern AI-assisted development can enable a small effort to compete on **cost, iteration speed, and focus**, especially at the lower end of the market where existing solutions may not fit well.

Reviewer perspective on whether this direction makes sense — or misses something important — is especially welcome.

---

## Thank You
Thank you for taking the time to review PB Tourney. Your perspective as a player or director is essential to shaping whether this project is solving the *right* problems in the *right* way.
