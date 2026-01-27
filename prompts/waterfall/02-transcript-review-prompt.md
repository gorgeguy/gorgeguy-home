# Transcript Review

## Instructions for Claude

Execute this prompt. Follow these steps:

### Step 1: Get Input
Ask the user for the path to the transcript file, then read it.

### Step 2: Generate Initial Review
Analyze the transcript and identify:

1. **Key Decisions Made** — Clear decisions the group made that were discussed and resolved
2. **Ambiguities** — Things that are unclear or could be interpreted multiple ways
3. **Contradictions** — Conflicting statements that weren't resolved
4. **Topics Not Fully Discussed** — Things mentioned but not resolved
5. **Implied Assumptions** — Things the group assumed but didn't state explicitly
6. **Open Questions** — Questions raised but not answered, or questions that should have been asked

### Step 3: Save and Report
Save the review as `transcript-review.md` in the same directory as the transcript. Tell the user the full path where you saved it.

### Step 4: Identify Issues and Iterate
Review your output and identify any issues:
- Are there ambiguities you're uncertain how to categorize?
- Are there sections that seem incomplete?
- Did you make assumptions you should verify?

Present the most important issue and ask the user how to resolve it.

Then wait for the user's response. They may:
- **Answer your question** → Incorporate their answer, save the updated file, and continue to the next issue
- **Say "skip"** → Leave this issue unresolved and continue to the next issue
- **Give an unrelated comment or correction** → Address it, save the updated file, then re-ask the original question
- **Declare the document complete** (e.g., "done", "looks good", "that's fine") → Finalize the document and confirm completion

Repeat until the user declares the document complete or there are no more issues.

---

## Output Format

```markdown
# Transcript Review: [Project Name or Date]

## Key Decisions Made
1. [Decision]: [Brief description]
2. [Decision]: [Brief description]

## Ambiguities
1. **[Topic]**: [What's unclear]
   - Possible interpretation A: [description]
   - Possible interpretation B: [description]

## Contradictions
1. **[Topic]**: [Statement A] vs. [Statement B]
   - Needs resolution: [What must be decided]

## Topics Not Fully Discussed
1. **[Topic]**: Mentioned but not resolved
   - Questions to answer: [list]

## Implied Assumptions
1. The group assumes [X]
2. The group assumes [Y]

## Open Questions
1. [Question]
2. [Question]

## Recommended Follow-up
Before proceeding to requirements extraction:
- [ ] Resolve: [item]
- [ ] Clarify: [item]
- [ ] Confirm assumption: [item]
```

---

## Done Criteria

This review is complete when:
- [ ] All significant ambiguities have been identified
- [ ] Contradictions are surfaced with what needs resolution
- [ ] Gaps are documented with follow-up questions
- [ ] The user has declared the document complete
