# Requirements-to-Tickets Toolkit
## A Structured Approach to AI-Assisted Project Planning

### What This Is

A set of prompts and guides for turning a project discussion into actionable tickets, using an LLM (like Claude Code) to do the heavy lifting of extraction and organization.

The approach:
1. Have a natural conversation about what you're building
2. Use AI to extract and structure that conversation into formal artifacts
3. End up with tickets ready to implement

Each stage produces a document that feeds into the next, with explicit "Done When" criteria that flow from requirements through to tickets.

---

### The Documents

| # | Document | Purpose |
|---|----------|---------|
| 01 | Discussion Facilitation Guide | Questions to guide a comprehensive project conversation |
| 02 | Transcript Review Prompt | Surface gaps and contradictions before formal extraction |
| 03 | Requirements Extraction Prompt | Extract functional requirements from transcript |
| 04 | Design Extraction Prompt | Extract design decisions using transcript + requirements |
| 05 | Implementation Plan Prompt | Break design into small, dependency-aware work items |
| 06 | Ticket Generation Prompt | Convert implementation items to your ticketing system |

---

### The Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  [Discussion]                                                       │
│       │                                                             │
│       ▼                                                             │
│  transcript.txt (you provide) ──────────────────────┐               │
│       │                                             │               │
│       ▼                                             │               │
│  transcript-review.md ◄── optional but recommended  │               │
│       │                                             │               │
│       ▼                                             │               │
│  requirements-spec.md ◄── reads transcript          │               │
│       │                    (+ review if exists)     │               │
│       │                                             │               │
│       ▼                                             ▼               │
│  design-spec.md ◄─────────── reads transcript + requirements        │
│       │                                                             │
│       ▼                                                             │
│  implementation-plan.md ◄── reads design (+ requirements)           │
│       │                                                             │
│       ▼                                                             │
│  tickets.md ◄────────────── reads implementation plan               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Standard Filenames

Each step generates a file with a predictable name. Subsequent steps look for these files automatically:

| Step | Output Filename |
|------|-----------------|
| Transcript Review | `transcript-review.md` |
| Requirements Extraction | `requirements-spec.md` |
| Design Extraction | `design-spec.md` |
| Implementation Planning | `implementation-plan.md` |
| Ticket Generation | `tickets.md` (or `tickets.csv`, etc.) |

Keep all files in the same project directory. Each prompt checks for the previous step's output and only asks for a file path if it's missing.

---

### How to Use

Each prompt document (02-06) is directly executable. Tell your LLM:

> "Read /path/to/02-transcript-review-prompt.md and execute it"

The LLM will:
1. Ask you for the required input file(s)
2. Generate an initial document and save it
3. Tell you where it saved the file
4. Identify issues and ask you how to resolve them
5. Wait for your response

You can respond in four ways:
- **Answer the question** → LLM incorporates your answer, saves, and continues to next issue
- **Say "skip"** → LLM leaves this issue unresolved and continues to next issue
- **Give a correction or comment** → LLM addresses it, saves, then re-asks the original question
- **Declare done** (e.g., "done", "looks good", "approved") → LLM finalizes and confirms completion

This loop continues until you declare the document complete or there are no more issues.

---

### Quick Start

#### 1. Hold the Discussion (15-45 minutes)

Use **01-discussion-facilitation-guide.md** to run a meeting. Record and transcribe the conversation. Save the transcript in a project directory.

#### 2. Review the Transcript (Optional, 10-15 minutes)

> "Read 02-transcript-review-prompt.md and execute it"

The LLM asks for your transcript path, analyzes it, saves `transcript-review.md`, and guides you through resolving any issues.

#### 3. Extract Requirements (15-30 minutes)

> "Read 03-requirements-extraction-prompt.md and execute it"

The LLM asks for your transcript path, finds the review if it exists, saves `requirements-spec.md`, and guides you through refinement.

**Declare done** only when requirements are solid—design depends on them.

#### 4. Extract Design (15-30 minutes)

> "Read 04-design-extraction-prompt.md and execute it"

The LLM asks for your transcript path, finds the requirements spec, saves `design-spec.md`, and guides you through refinement.

#### 5. Create Implementation Plan (15-30 minutes)

> "Read 05-implementation-plan-prompt.md and execute it"

The LLM asks for your project directory, finds the specs, saves `implementation-plan.md`, and guides you through refinement.

#### 6. Generate Tickets (10-20 minutes)

> "Read 06-ticket-generation-prompt.md and execute it"

The LLM asks for your project directory and ticketing system, finds the implementation plan, saves `tickets.md`, and guides you through refinement.

---

### Key Principles

#### "Done When" Flows Through Everything

Every level has explicit completion criteria:

| Level | "Done When" Example |
|-------|---------------------|
| Requirement | Users can reset password via email link |
| Design | Reset flow: request → email with token → new password form → confirmation message |
| Implementation Item | Password reset endpoint accepts token, validates expiry, updates password hash, returns 200 |
| Ticket | Checkbox: Token validated; Checkbox: Password updated; Checkbox: 200 returned |

This prevents ambiguity and scope creep. If the criteria are met, the work is done.

#### Separation Happens in Processing, Not Discussion

People naturally mix requirements and design when talking. That's fine. Let the conversation flow naturally; the LLM separates concerns during extraction.

This is faster and more natural than forcing people to think in "spec format."

#### Iterate Through the Built-in Loop

Each prompt includes an iteration loop. After generating the initial document, the LLM identifies issues and asks you to resolve them. This is where quality comes from.

Common things to address:
- Vague "Done When" criteria
- Missing requirements coverage
- Over-engineered designs
- Implementation items that are too large
- Unclear dependencies

Don't rush to "done." The conversation is the refinement process.

#### Traceability Matters

Each artifact references the previous:
- Design decisions cite requirements they serve
- Implementation items cite design sections
- Tickets cite implementation items

This lets you trace any piece of work back to the original need, and ensures nothing gets lost.

---

### Time Estimates

| Phase | Minimum | Typical | Maximum |
|-------|---------|---------|---------|
| Discussion | 15 min | 30 min | 60 min |
| Transcript Review | 5 min | 10 min | 20 min |
| Requirements Extraction | 10 min | 20 min | 45 min |
| Design Extraction | 10 min | 20 min | 45 min |
| Implementation Planning | 10 min | 20 min | 30 min |
| Ticket Generation | 5 min | 15 min | 30 min |
| **Total** | **55 min** | **~2 hours** | **~4 hours** |

Smaller projects skew toward minimum. Complex projects with multiple stakeholders skew toward maximum.

---

### Tips for Success

**Before the discussion:**
- Share the facilitation guide so participants know what to think about
- Set up reliable recording/transcription
- Have visual examples ready if discussing design direction

**During extraction:**
- Keep all files in one project directory for automatic detection
- Don't rush to "done"—the iteration loop is where quality comes from
- If the LLM's question doesn't make sense, ask it to clarify
- You can always say "show me the current document" to review progress

**Between phases:**
- Declare "done" only when you're confident in the document
- Changes to requirements after design extraction cause rework
- It's cheaper to spend 10 extra minutes on requirements than to redo design

**For workshops/teaching:**
- Run the same transcript through different LLMs and compare outputs
- Have participants do extraction in parallel and compare results
- Use the "Done When" criteria to evaluate outputs objectively

---

### Customization

#### Adjusting for Project Size

**Small projects** (landing page, simple tool):
- Shorter discussion (15-20 min)
- May skip transcript review
- Requirements and design extraction might take 10 min each
- Fewer implementation items, simpler dependencies

**Large projects** (complex application, multiple user types):
- Longer discussion, possibly multiple sessions
- Transcript review is essential
- Multiple iteration rounds per phase
- Consider breaking into modules and running the process per module

#### Adjusting the Prompts

The prompts are designed to be executed directly but can be customized:
- Edit the Output Format section to match your conventions
- Add domain-specific terminology to the instructions
- Adjust the Done Criteria for your quality bar
- Change what the LLM checks for in Step 4 (iteration issues)

#### Using Different LLMs

The prompts are written for Claude but work with other capable LLMs. You may need to adjust:
- Level of detail in instructions (some models need more explicit guidance)
- Output format expectations
- Iteration strategy (some models respond better to different follow-up styles)

Running the same transcript through multiple models and comparing outputs is a useful exercise.

---

### Troubleshooting

**LLM includes design in requirements**
→ Tell it: "REQ-### is actually a design decision. What's the underlying need?"

**"Done When" criteria are vague**
→ Ask: "How would I test REQ-###? What specific behavior proves it's done?"

**Missing requirements coverage in design**
→ Ask: "Walk through each requirement. Which design element addresses it?"

**Implementation items are too large**
→ Tell it: "IMPL-### is too big. Break it into pieces completable in one session."

**Circular dependencies**
→ Ask: "Walk through the dependency chain. Is there a cycle? How do we break it?"

**Tickets don't match your system's format**
→ Describe your exact format requirements and ask it to regenerate.

**Want to see current state**
→ Say: "Show me the current document" at any point.

---

### File Checklist

After completing the process, your project directory should contain:

- [ ] `transcript.txt` (or similar — your discussion recording)
- [ ] `transcript-review.md` (optional, but recommended)
- [ ] `requirements-spec.md` (approved)
- [ ] `design-spec.md` (approved)
- [ ] `implementation-plan.md` (approved)
- [ ] `tickets.md` (or format-specific file, ready to import)

Keep these artifacts. They're useful for:
- Onboarding new team members
- Resolving disputes about scope
- Post-project retrospectives
- Comparing LLM performance across projects
