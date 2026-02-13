# Implementation Planning

## Instructions for Claude

Execute this prompt. Follow these steps:

### Step 1: Get Input
Ask the user for the project directory path (where the spec files are located).

Check for these files in that directory:
- `design-spec.md` (required) — if missing, ask for the path to the design specification
- `requirements-spec.md` (optional but helpful) — read if present

### Step 2: Generate Initial Implementation Plan
Break the design into small, discrete work items that:
- Won't stress an LLM context window when implemented
- Have clear boundaries (obvious when "done")
- Can be directly converted to tickets
- Have explicit dependencies

**Each work item must include:**
- **ID**: e.g., IMPL-001
- **Title**: Brief, descriptive name
- **Description**: What this accomplishes (2-4 sentences)
- **Depends on**: List of item IDs required first (or "None")
- **Done when**: Specific, testable criteria (inherited from Design Spec)
- **Complexity**: Simple / Medium / Complex
- **Traces to**: Design Spec sections and requirement IDs

**"Done when" must be testable:**
```
✓ Good: "Nav bar displays 5 links, remains fixed during scroll, collapses to hamburger at <768px"
✗ Bad: "Navigation works correctly"
```

### Step 3: Save and Report
Save as `implementation-plan.md` in the project directory. Tell the user the full path.

### Step 4: Identify Issues and Iterate
Review your output for issues:
- Are any items too large for a single session?
- Are any "Done when" criteria vague?
- Are dependencies correct and complete (no circular dependencies)?
- Is every design element covered?
- Are complexity estimates reasonable?

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
# Implementation Plan: [Project Name]

## Summary
- **Total items**: [N]
- **By complexity**: Simple: [N] | Medium: [N] | Complex: [N]
- **Phases**: [N]
- **Critical path**: [Key items that block the most work]

## Dependency Overview
[Brief description or diagram of major dependencies]

---

## Phase 1: [Name — e.g., Foundation]

### IMPL-001: [Title]
- **Description**: [What this accomplishes]
- **Depends on**: None
- **Done when**:
  - [ ] [Specific criterion]
  - [ ] [Specific criterion]
- **Complexity**: Simple
- **Traces to**: Design Spec § [section], REQ-###

### IMPL-002: [Title]
- **Description**: [What this accomplishes]
- **Depends on**: IMPL-001
- **Done when**:
  - [ ] [Specific criterion]
  - [ ] [Specific criterion]
- **Complexity**: Medium
- **Traces to**: Design Spec § [section], REQ-###

---

## Phase 2: [Name — e.g., Core Features]

### IMPL-003: [Title]
...

---

## Traceability

| Requirement | Design Section | Implementation Items |
|-------------|----------------|---------------------|
| REQ-001 | § [Section] | IMPL-001, IMPL-003 |
| REQ-002 | § [Section] | IMPL-004 |

## Items by Complexity

**Simple** (target: <2 hours)
- IMPL-001, IMPL-004

**Medium** (target: 2-4 hours)
- IMPL-002, IMPL-003

**Complex** (target: 4-8 hours)
- IMPL-005
```

---

## Done Criteria

Implementation planning is complete when:
- [ ] Every design element is covered by at least one item
- [ ] Every item has a unique ID
- [ ] Every item has testable "Done when" traced to Design Spec
- [ ] Dependencies are identified with no circular dependencies
- [ ] Items are small enough for single-session implementation
- [ ] Critical path is identified
- [ ] The user has declared the document complete
