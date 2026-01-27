# Design Extraction

## Instructions for Claude

Execute this prompt. Follow these steps:

### Step 1: Get Input
Ask the user for the path to the transcript file, then read it.

Check if `requirements-spec.md` exists in the same directory:
- If it exists, read it (required input)
- If it does not exist, ask the user for the path to the requirements specification

You need both the transcript and the requirements spec before proceeding.

### Step 2: Generate Initial Design Spec
Extract design decisions from the transcript, ensuring every requirement has a corresponding design approach.

**Include:**
- **Visual Direction** — Style, personality, colors, typography, imagery direction
- **User Experience & Layout** — Page structure, navigation, user flows, responsive behavior
- **Content Structure** — Information hierarchy, what's prominent vs. secondary
- **Technology Stack** — Recommended technologies with rationale tied to requirements/constraints
- **Scope Definition** — MVP vs. future phases

**Critical: Every design element must have a "Done when" statement** — a way to verify the design has been correctly implemented.

Example:
```
**Navigation Bar**
Horizontal bar fixed to top of viewport with logo and main section links.
- **Serves**: REQ-003 (users must access all sections from any page)
- **Done when**: Nav displays logo + 5 links, remains fixed during scroll, collapses to hamburger below 768px
```

**Traceability**: Every design decision should reference which requirement(s) it serves.

### Step 3: Save and Report
Save as `design-spec.md` in the same directory as the transcript. Tell the user the full path.

### Step 4: Identify Issues and Iterate
Review your output for issues:
- Are there requirements without a design approach?
- Are any "Done when" criteria too vague to verify?
- Is the tech stack justified by requirements/constraints?
- Is the visual direction specific enough to implement?
- Did you make assumptions that need verification?

Present the most important issue and ask the user how to resolve it.

Then wait for the user's response. They may:
- **Answer your question** → Incorporate their answer, save the updated file, and continue to the next issue
- **Say "skip"** → Leave this issue unresolved and continue to the next issue
- **Give an unrelated comment or correction** → Address it, save the updated file, then re-ask the original question
- **Declare the document complete** (e.g., "done", "looks good", "approved") → Finalize the document and confirm completion

Repeat until the user declares the document complete or there are no more issues.

---

## Output Format

```markdown
# Design Specification: [Project Name]

## Summary
[Brief description of the design approach and how it serves the requirements]

## Visual Direction

**Style**: [Description]
- **Done when**: [Specific, verifiable criteria]

**Colors**: [Palette]
- **Done when**: [Specific color values or rules]

**Typography**: [Font approach]
- **Done when**: [Specific fonts, sizes, weights]

## Layout & Structure

### [Page/Screen 1]
**Purpose**: [What this accomplishes]
- **Serves**: REQ-###

**Layout**: [Structure description]
- **Done when**: [Specific layout criteria]

**Key Elements**: [What's present]
- **Done when**: [Element-specific criteria]

**Interactions**: [What users can do]
- **Done when**: [Interaction-specific criteria]

## User Flows

### [Flow Name]
**Serves**: REQ-###

1. User does X
2. System responds with Y
3. User does Z

- **Done when**: Flow can be executed as described

## Technology Stack

| Layer | Choice | Rationale | Done When |
|-------|--------|-----------|-----------|
| Frontend | [Tech] | Serves REQ/CON-### | [Verification] |
| Backend | [Tech] | [Why] | [Verification] |
| Hosting | [Tech] | [Why] | [Verification] |

## Scope

### MVP (Initial Build)
- [Feature]
- [Feature]

### Phase 2 / Future
- [Feature]
- [Feature]

## Requirements Traceability

| Requirement | Design Approach | Done When |
|-------------|-----------------|-----------|
| REQ-001 | [How addressed] | [Reference] |
| REQ-002 | [How addressed] | [Reference] |
```

---

## Done Criteria

Design extraction is complete when:
- [ ] Every requirement has a corresponding design approach
- [ ] Every design element has a verifiable "Done when"
- [ ] Visual direction is specific enough to implement
- [ ] Tech stack is selected with rationale tied to requirements
- [ ] Traceability table is complete
- [ ] The user has declared the document complete
