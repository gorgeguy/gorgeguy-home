
# A Prompt to Generate a Prompt from a Generic Prompt Template

This instruction must be executed from inside a project. Examine this
project for languages, tech stack, tooling, and architecture.  Adapt the
following generic prompt template to this project according to what
you find.  Research and identify best practices that apply here. Add
an evaluation against these best practices as part of this output. The
prompt you generate should be written out as a markdown file in docs/
as it will be used frequently throughout the life of this project to
maintain the highest quality standards.

# The actual Generic Prompt Template:

The Generalized Architecture Review Prompt
Context: I need a deep architectural evaluation of the {{PROJECT_NAME}} project. This is a {{PROJECT_TYPE}} (e.g., CLI tool, React SPA, Microservice, Python Library) built using {{TECH_STACK}} (e.g., Node/Express, Rust/Clap, Django, Vue).

GOALS:

Structure & Flow: Understand the directory structure, data flow, and responsibilities across the {{MAJOR_LAYERS}} (e.g., generic UI components vs. business logic, or CLI commands vs. internal API).

Coupling & Cohesion: Assess whether interfaces, logic, and data storage are properly separated and whether domain logic is leaking across layers.

Domain Logic: Evaluate the implementation of {{CORE_COMPLEX_LOGIC}} (e.g., the scheduling engine, parsing algorithm, authentication flow).

Lifecycle & State: Review how {{KEY_ENTITIES}} transition through their lifecycles/states.

Standardization: Review {{CROSS_CUTTING_CONCERNS}} (e.g., error handling, logging, datetime/timezone, currency, security) for consistency.

Scalability: Identify technical debt or patterns that may limit future goals, specifically: {{FUTURE_SCALING_GOALS}}.

TASKS:

1. Repo Scan & Component Analysis

Walk the directory structure to establish a mental map of the project.

Summarize the major modules/components and their distinct responsibilities.

Identify areas with unclear ownership, circular dependencies, or "god objects" (files doing too much).

2. Key Entity & State Lifecycle Evaluation

Focus on the lifecycle of {{KEY_ENTITIES}} (e.g., a "Match," a "User Session," a "File Stream").

Trace how state transitions occur (e.g., Pending -> Active -> Completed/Failed).

Identify inconsistencies, race conditions, or redundant state logic.

If applicable: Suggest a cleaner state machine or domain model.

3. Critical Logic & Subsystem Audit

Locate the code responsible for {{CORE_COMPLEX_LOGIC}} (e.g., the specific algorithm, the pricing engine, the compiler).

Evaluate if this logic is pure, cohesive, and easily testable.

Identify edge cases that may be missing (race conditions, invariants, null states).

4. Interface Layer Review

Review the entry points: {{ENTRY_POINTS}} (e.g., API Routes, CLI Arguments, UI Views/Forms).

Check if the interface layer contains too much business logic ("Fat Controllers" or "Logic in UI").

Recommend a proper layering approach (e.g., Interface → Service/Use-Case → Domain → Persistence).

5. Data Persistence & Model Review

Review how data is defined and stored (e.g., SQL Models, Redux Store, File Schema).

Check for correct relationship definitions and session/connection management.

{{SPECIFIC_DATA_CONCERN}} (e.g., Check for N+1 query issues, or proper immutability in state updates).

6. Cross-Cutting Concerns (Consistency Check)

Review how {{SPECIFIC_STANDARD}} (e.g., Datetimes, Internationalization, Error Codes) are handled globally.

Check for mixing of standards (e.g., naive vs. aware dates, different error formats).

Suggest how to centralize these utilities.

7. Resilience & Validation

Identify brittle failure paths where the application crashes or behaves unpredictably.

Review input validation: Is it happening at the boundary (API/UI) or deep in the core?

Suggest where types or schema validation (e.g., Pydantic, TypeScript interfaces, Zod) should enforce invariants.

8. Refactor & Roadmap

Propose an ideal folder structure for long-term maintenance.

Create a "Refactor Roadmap": What should be fixed now vs. later.

Suggest specific architectural changes to support {{FUTURE_GOAL}} (e.g., migrating database, adding mobile support, switching to async I/O).

PLEASE PRODUCE:

A detailed architecture report.

A dependency/data-flow map (text or diagram).

A state diagram for {{KEY_ENTITY}}.

A prioritized refactor roadmap.

Actionable code quality recommendations.

Begin by scanning the directory and summarizing the project at a high level.

How to use this template
Here is a guide on how to fill the placeholders for different types of projects:

Example 1: A Frontend React App (Dashboard)
{{KEY_ENTITIES}}: User Reports, Authentication State.

{{CORE_COMPLEX_LOGIC}}: Data visualization rendering, Redux/Context state reducers.

{{ENTRY_POINTS}}: React Router definitions, Page components.

{{SPECIFIC_DATA_CONCERN}}: React Query caching strategies, unnecessary re-renders.

{{CROSS_CUTTING_CONCERNS}}: CSS/Theming consistency, Mobile responsiveness.

Example 2: A CLI Tool (Image Processor)
{{KEY_ENTITIES}}: The Image Buffer, The Configuration Object.

{{CORE_COMPLEX_LOGIC}}: The compression algorithm, multithreading logic.

{{ENTRY_POINTS}}: main() function, Argument Parser setup.

{{SPECIFIC_DATA_CONCERN}}: File I/O safety, Memory management (buffer overflows).

{{CROSS_CUTTING_CONCERNS}}: Logging verbosity levels, Exit codes.
