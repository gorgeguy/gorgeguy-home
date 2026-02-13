# Ticket Generation

## Instructions for Claude

Execute this prompt. Follow these steps:

### Step 1: Get Input
Ask the user for:
1. The project directory path (where `implementation-plan.md` is located)
2. Their ticketing system: GitHub Issues / Jira / Linear / Trello / Plain Markdown / Other

Check if `implementation-plan.md` exists in the directory:
- If it exists, read it
- If not, ask for the path to the implementation plan

### Step 2: Generate Initial Tickets
Convert each implementation item into a ticket formatted for the user's system.

**Every ticket must include:**
- **Title**: Action-oriented (e.g., "Implement navigation bar")
- **Description**: What this accomplishes, with context
- **Acceptance Criteria**: The "Done when" from the implementation plan, as checkboxes
- **Dependencies**: What must be complete first
- **Metadata**: Labels/tags for complexity, phase, type as appropriate for the system

**Critical: Preserve "Done when" exactly as acceptance criteria.** These are the contract for completion. Do not summarize or omit them.

### Step 3: Save and Report
Save as `tickets.md` (or format-appropriate filename like `tickets.csv` for Jira import) in the project directory. Tell the user the full path.

### Step 4: Identify Issues and Iterate
Review your output for issues:
- Do all tickets have complete acceptance criteria from the implementation plan?
- Is the format correct for the specified ticketing system?
- Are dependencies properly represented?
- Are there any tickets that seem too large or unclear?

Present the most important issue and ask the user how to resolve it.

Then wait for the user's response. They may:
- **Answer your question** → Incorporate their answer, save the updated file, and continue to the next issue
- **Say "skip"** → Leave this issue unresolved and continue to the next issue
- **Give an unrelated comment or correction** → Address it, save the updated file, then re-ask the original question
- **Declare the document complete** (e.g., "done", "looks good", "ready to import") → Finalize the document and confirm completion

Repeat until the user declares the document complete or there are no more issues.

---

## Output Formats by System

### GitHub Issues (Markdown)

```markdown
## IMPL-001: Set up project repository

**Labels**: `phase:1`, `size:small`, `type:chore`
**Milestone**: MVP
**Blocked by**: None
**Traces to**: Design Spec § Technology Stack, CON-001

### Description
Initialize the project repository with the chosen tech stack. Set up folder structure, configuration files, and development environment.

### Acceptance Criteria
- [ ] Repository created with README containing project overview
- [ ] Package manager initialized with dependencies from Design Spec
- [ ] Folder structure matches Design Spec § Architecture
- [ ] Development server starts without errors
- [ ] .gitignore properly configured

---
```

### Jira (CSV)

```csv
Summary,Description,Story Points,Epic,Labels,Acceptance Criteria,Blocked By
"Set up project repository","Initialize repo with tech stack and folder structure per Design Spec.",1,MVP-Setup,"phase-1,chore","Repo created; packages init; structure matches spec; server runs; gitignore set",
"Implement navigation bar","Create nav with logo and section links per Design Spec.",3,MVP-Core,"phase-1,feature","Logo + 5 links; fixed on scroll; hamburger <768px; links work",IMPL-001
```

### Linear (YAML)

```yaml
tickets:
  - id: IMPL-001
    title: "Set up project repository"
    description: "Initialize repo with tech stack and folder structure."
    priority: high
    project: "Phase 1"
    labels: [size:small, type:chore]
    acceptance_criteria:
      - Repository created with README
      - Package manager initialized
      - Folder structure matches spec
      - Dev server runs
    blocked_by: []
```

### Plain Markdown (Task List)

```markdown
# Project Tickets

## Ready to Start (No Dependencies)
- [ ] **IMPL-001**: Set up project repository (Small)
  - [ ] Repo created with README
  - [ ] Packages initialized
  - [ ] Structure matches spec
  - [ ] Server runs

## Phase 1: Foundation
- [ ] **IMPL-002**: Implement navigation bar (Medium) — needs IMPL-001
  - [ ] Logo + 5 links displayed
  - [ ] Fixed on scroll
  - [ ] Hamburger menu <768px
  - [ ] All links work
```

---

## Done Criteria

Ticket generation is complete when:
- [ ] Every implementation item has a corresponding ticket
- [ ] Every ticket has acceptance criteria matching "Done when" exactly
- [ ] Format is correct for the target ticketing system
- [ ] Dependencies are properly represented
- [ ] The user has declared the document complete
