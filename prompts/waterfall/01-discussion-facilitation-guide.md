# Discussion Facilitation Guide
## Requirements & Design Meeting

### Purpose

This guide helps facilitators lead a comprehensive discussion covering both requirements and design. The conversation flows naturally—no need to strictly separate concerns. The transcript will be processed later to extract requirements and design separately.

### Before the Meeting

- Set up recording/transcription
- Share this document with participants so they know what topics to think about
- Have examples ready if discussing visual direction (websites you like, etc.)

---

## Opening (2-3 minutes)

Frame the discussion:

> "We're going to talk through what we're building—what it needs to do, who it's for, and how we want it to work and look. Don't worry about keeping requirements separate from design ideas. Say whatever comes to mind. We'll sort it out later when we process the transcript."

---

## Discussion Areas

Work through these areas. You don't need to ask every question—use them as prompts to ensure comprehensive coverage. Let conversation flow naturally between topics.

### The Problem & Purpose

- What problem are we solving? Why does this need to exist?
- What's the goal? If this is successful, what's different?
- Who asked for this / where did this idea come from?
- What happens if we don't build it?

### Users & Audience

- Who uses this? List all the different types of people.
- For each user type: What are they trying to accomplish? What do they need?
- What do users already know? What's their context?
- How tech-savvy are they?
- Are there different permission levels or roles?

### Core Functionality

- What must this do? What's non-negotiable?
- Walk me through a typical user journey—what happens step by step?
- What actions can users take?
- What information must be displayed?
- What information do we need to collect from users?
- Are there any calculations, transformations, or business logic?

### Content & Data

- What content needs to exist?
- Where does the data come from?
- What's static vs. dynamic?
- How often does content change? Who updates it?
- Any integrations with other systems or data sources?

### Constraints & Boundaries

- What's the timeline?
- What's the budget (if any)?
- Who maintains this after it's built? How technical are they?
- Are there any technical constraints we must work within?
- Any compliance, accessibility, or security requirements?
- What's explicitly out of scope?

### User Experience & Interaction

- What should users feel when they use this?
- What's the most important thing they should notice first?
- How do they navigate? What's the flow?
- What devices will they use? Mobile? Desktop? Both?
- Any interactions that need to feel a particular way? (Fast, careful, playful, etc.)

### Visual Direction

- What's the personality? (Professional, casual, playful, minimal, bold, etc.)
- Any existing brand elements to work with? (Logo, colors, fonts)
- Any examples of things you like? What specifically appeals to you?
- Any examples of things you hate? What should we avoid?
- What feeling should the visual design evoke?

### Technology Preferences

- Any required technologies? (Existing systems to integrate with, platforms to deploy to)
- Any preferred technologies? Any to avoid?
- How important is performance?
- Any preferences on build vs. buy for components?
- What's the maintenance model—who touches the code after launch?

### Scope & Priority

- If we can only do one thing well, what should it be?
- What's the minimum viable version?
- What's nice-to-have vs. must-have?
- What would make this a failure?
- What's Phase 1 vs. later phases?

---

## Closing (2-3 minutes)

Wrap up with:

- "What haven't we talked about that we should?"
- "Any concerns or risks we should note?"
- "Anything you want to make sure doesn't get lost in translation?"

---

## What "Done" Looks Like

The discussion phase is complete when:

- [ ] All discussion areas have been covered (even if briefly)
- [ ] Every participant has had a chance to contribute
- [ ] Major concerns and risks have been voiced
- [ ] The transcript captures enough context for someone who wasn't present to understand the project
- [ ] Recording/transcription is saved and accessible

---

## Facilitator Tips

**Let it flow.** If someone answers a "requirements" question with design ideas, that's fine. Capture it all.

**Probe vague statements.** "User-friendly" means nothing. Ask: "What would make it user-friendly? Give me an example."

**Get specifics.** "It should be fast" → "How fast? What's acceptable? What's too slow?"

**Capture disagreements.** If people disagree, note both positions. Don't resolve in the moment unless necessary.

**Mind the quiet voices.** Actively invite input from people who haven't spoken.

**Watch the clock.** Don't let any single area consume all the time. It's better to cover everything lightly than one thing deeply.

---

## After the Meeting

1. Create a project directory for all artifacts
2. Save the transcript as a text file in that directory (e.g., `transcript.txt`)
3. Proceed to **Transcript Review** (recommended) — surfaces gaps and contradictions while memory is fresh
4. Then **Requirements Extraction** → generates `requirements-spec.md`
5. Then **Design Extraction** → generates `design-spec.md`
6. Then **Implementation Planning** → generates `implementation-plan.md`
7. Then **Ticket Generation** → generates `tickets.md`
