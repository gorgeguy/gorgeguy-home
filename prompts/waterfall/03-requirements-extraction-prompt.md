# Requirements Extraction

## Instructions for Claude

Execute this prompt. Follow these steps:

### Step 1: Get Input
Ask the user for the path to the transcript file, then read it.

Check if `transcript-review.md` exists in the same directory. If it does, read it as additional context. If not, proceed without it.

### Step 2: Generate Initial Requirements Spec
Extract ONLY requirements from the transcript. 

**Include:**
- **Functional Requirements** — What the system must do, actions users can take, behaviors, business rules
- **User Requirements** — Who the users are, what each user type needs to accomplish
- **Content Requirements** — What information must be present, data to capture or display
- **Constraints** — Technical, timeline, budget, maintenance, compliance, security, accessibility limitations
- **Open Questions** — Ambiguities needing resolution, missing information

**Exclude (these belong in Design Spec):**
- Visual design (colors, fonts, layouts)
- Specific UI patterns or components
- Technology choices (frameworks, platforms, languages)
- Implementation details

**Critical: Every requirement must have a "Done when" statement** — a testable condition that proves the requirement is satisfied.

Example:
```
**REQ-001: Password Reset**
Users can reset their password via email.
- **Done when**: User requests reset, receives email with link, can set new password, new password works on next login
```

### Step 3: Save and Report
Save as `requirements-spec.md` in the same directory as the transcript. Tell the user the full path.

### Step 4: Identify Issues and Iterate
Review your output for issues:
- Are any requirements vague or untestable?
- Are any "Done when" criteria ambiguous?
- Did design decisions creep in that should be excluded?
- Are there gaps in user coverage?
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
# Requirements Specification: [Project Name]

## Summary
[2-3 sentences describing the project and its purpose]

## Users
- **[User Type 1]**: [What they need to accomplish]
- **[User Type 2]**: [What they need to accomplish]

## Functional Requirements

### [Category 1]

**REQ-001: [Title]**
[Description of the requirement]
- **Done when**: [Specific, testable condition]

**REQ-002: [Title]**
[Description]
- **Done when**: [Specific, testable condition]

### [Category 2]

**REQ-003: [Title]**
[Description]
- **Done when**: [Specific, testable condition]

## Content Requirements

**REQ-010: [Title]**
[Description]
- **Done when**: [Specific, testable condition]

## Constraints

**CON-001: [Title]**
[Description]
- **Validated when**: [How to confirm constraint is respected]

## Out of Scope
- [Item]
- [Item]

## Open Questions
- [Question needing resolution]
```

---

## Done Criteria

Requirements extraction is complete when:
- [ ] Every functional need from the transcript is captured
- [ ] Every requirement has a unique ID
- [ ] Every requirement has a specific, testable "Done when"
- [ ] No design decisions are included
- [ ] User types are identified with their core needs
- [ ] The user has declared the document complete
