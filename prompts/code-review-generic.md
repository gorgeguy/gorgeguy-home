
# Architecture Review Prompt Generator

This instruction must be executed from inside a project. It generates a
**project-specific architecture review prompt** tailored to the codebase.

## What This Does

1. Examine the project for languages, tech stack, tooling, and architecture
2. Research and identify best practices that apply
3. Adapt the generic template below to this project
4. Add an evaluation against discovered best practices
5. Write the result as a markdown file in `docs/architecture-review-prompt.md`

## Scan Strategy

To fill the template accurately:

- **Directory scan:** Walk top-level and one level deep under `src/` (or
  equivalent) to map packages/modules
- **Config files:** Read build configs (pyproject.toml, package.json,
  Cargo.toml, etc.) for dependencies, entry points, and tooling
- **Key modules:** Read the 3-5 largest or most-imported files to understand
  core domain logic
- **Entry points:** Identify all ways the code is invoked (CLI, HTTP, Lambda,
  queue consumer, etc.)
- **Tests:** Scan the test directory structure and read 2-3 representative
  test files for patterns
- **CI/CD:** Check for workflow files (.github/workflows/, .gitlab-ci.yml,
  Jenkinsfile, etc.)

Do NOT read every file. Sample strategically to understand patterns, then
generalize.

---
<!-- BEGIN TEMPLATE -->

# {{PROJECT_NAME}} — Architecture Review Prompt

> **Usage:** Run this prompt against the codebase periodically (e.g., after
> each milestone or before a major refactor) to get a structured architectural
> evaluation. Paste it into a new AI coding session from this project root.

---

## Context

I need a deep architectural evaluation of the **{{PROJECT_NAME}}** project.
This is a {{PROJECT_TYPE}} (e.g., CLI tool, React SPA, microservice, Python
library, multi-package monorepo) built using {{TECH_STACK}} (e.g.,
Node/Express, Rust/Clap, Django, Python/Pydantic).

{{ADDITIONAL_CONTEXT — brief description of what the project does, any
deployment targets, and critical constraints like security boundaries}}

## Goals

### 1. Structure & Flow

Understand the directory structure, data flow, and responsibilities across
{{MAJOR_LAYERS}} (e.g., UI components vs. business logic, CLI commands vs.
internal API, package boundaries in a monorepo).

{{If the project has an intended dependency graph, include it here as a text
diagram and ask the reviewer to verify it.}}

### 2. Coupling & Cohesion

Assess whether interfaces, logic, and data storage are properly separated.
Check whether domain logic is leaking across layers. Specifically:

{{COUPLING_CONCERNS — e.g., cross-provider contamination, OPSEC boundary
violations, fat controllers, shared mutable state}}

### 3. Core Complex Logic

Evaluate the implementation of the project's most critical subsystems:

{{CORE_COMPLEX_LOGIC — list 3-5 subsystems with file paths. e.g., "the
scheduling engine (src/scheduler/)", "the extraction pipeline
(src/extract/)", "the convergence detector (src/runtime/convergence.py)"}}

### 4. Entity Lifecycle & State

Review how {{KEY_ENTITIES}} (e.g., a User Session, a Discovery Pipeline Run,
a File Stream, an Order) transition through their lifecycles.

{{STATE_MACHINES — list each entity and its known states. e.g.:
- Processing mode: bootstrap → steady_state
- Order: draft → submitted → fulfilled → cancelled
}}

Identify inconsistencies, race conditions, or redundant state logic. If
applicable, suggest a cleaner state machine or domain model.

### 5. Cross-Cutting Concerns

Review {{CROSS_CUTTING_CONCERNS}} for consistency across the codebase:

{{List specific concerns. e.g.:
- Error handling: Are exceptions caught at appropriate levels?
- Logging: Is structured logging used consistently?
- Datetime/timezone: Are all datetimes timezone-aware?
- Entity naming: Are naming conventions consistent across modules?
}}

### 6. Scalability & Technical Debt

Identify technical debt or patterns that may limit future goals:

{{SCALING_GOALS — e.g., "adding new cloud providers", "supporting 10x more
concurrent users", "migrating to async I/O", "adding a mobile client"}}

## Tasks

### 1. Repo Scan & Component Analysis

Walk the directory structure to establish a mental map of the project.
Summarize the major modules/components and their distinct responsibilities.
Identify:

- Files with unclear ownership or "god object" tendencies (doing too much)
- Circular or unexpected import/dependency paths
- Dead code (unused modules, legacy shims from completed migrations)

### 2. Key Entity & State Lifecycle Evaluation

Focus on the lifecycle of {{KEY_ENTITIES}}.

{{LIFECYCLE_TRACE — describe specific scenarios to trace. e.g., "Trace how
a CloudTrail AssumeRole event flows through the full pipeline" or "Trace
how an Order transitions from draft to fulfilled"}}

Identify inconsistencies, missing edge cases, or redundant processing.

### 3. Critical Logic & Subsystem Audit

For each subsystem listed in Goal 3:

- Is the logic pure, cohesive, and easily testable?
- Are edge cases covered (race conditions, invariants, null/empty states)?
- Identify specific bugs or correctness concerns with file:line references.

### 4. Interface Layer Review

Review the entry points: {{ENTRY_POINTS}} (e.g., API routes, CLI arguments,
Lambda handler, UI views/forms, queue consumers).

- Is the interface layer thin, delegating to domain logic?
- Is there logic duplication between entry points?
- Recommend proper layering if needed (Interface -> Service/Use-Case ->
  Domain -> Persistence).

### 5. Data Persistence & Model Review

Review how data is defined and stored (e.g., SQL models, artifact files,
Redux store, file schemas).

- Check for correct relationship definitions and connection management.
- {{SPECIFIC_DATA_CONCERN — e.g., "Check for N+1 query issues", "Is the
  wire format forwards-compatible?", "Can state corruption cause data
  loss?", "Memory footprint at scale?"}}

### 6. Cross-Cutting Consistency Check

For each concern in Goal 5, scan the codebase for inconsistencies. Pay
special attention to:

- {{SPECIFIC_STANDARD — e.g., "Mixed datetime handling (naive vs. aware)",
  "Inconsistent error propagation between packages", "Logging extra fields
  that differ between code paths"}}

### 7. Resilience & Validation

Identify brittle failure paths where the application crashes or behaves
unpredictably.

- Review input validation: Is it happening at the boundary (API/UI/event
  parsing) or deep in the core?
- Suggest where types or schema validation (e.g., Pydantic, Zod, TypeScript
  interfaces) should enforce invariants.
- {{RESILIENCE_SCENARIOS — e.g., "What happens when a log file is corrupt?",
  "What happens when two instances race on the distributed lock?"}}

### 8. Test Architecture Review

Evaluate the test suite as an architectural artifact:

- **Organization:** How are tests structured? Do they mirror the source
  layout?
- **Fixture patterns:** Are fixtures deterministic and reproducible? Is test
  data realistic?
- **Guard tests:** Are there tests that enforce architectural invariants
  (import boundaries, naming conventions, security constraints)?
- **Contract tests:** If the project has multiple providers or adapters, do
  they pass identical behavioral assertions?
- **Coverage strategy:** Is the test-to-code ratio meaningful, or inflated
  by trivial tests? Are error paths covered?
- **E2E scenarios:** Do end-to-end tests map to documented requirements?

### 9. Security & Compliance Audit

Review the codebase for security concerns:

{{SECURITY_CONCERNS — e.g.:
- No forbidden terms in deployed packages (OPSEC scan)
- No hardcoded credentials or secrets
- Input sanitization at system boundaries
- Dependency vulnerability exposure
- Authentication/authorization correctness
- Logging sensitive data (PII, tokens, keys)
}}

### 10. CI/CD & Deployment Review

Review the build, test, and deployment pipeline:

- Is there automated CI (GitHub Actions, GitLab CI, etc.)?
- Are tests run before merge? Are there required status checks?
- Is the build reproducible (lock files, pinned dependencies)?
- Are deployment artifacts built correctly for target environments?
- {{DEPLOYMENT_CONCERNS — e.g., "Lambda packaging for arm64", "Docker
  multi-stage builds", "CDN cache invalidation"}}

### 11. Performance & Memory Review

Identify performance bottlenecks and memory concerns:

- Are hot-path objects optimized (slots, frozen, interning)?
- Are there unbounded data structures that grow with input size?
- Is I/O properly streaming or batched (not loading everything into memory)?
- {{PERFORMANCE_CONCERNS — e.g., "CatalogBuilder memory at 100K+ entities",
  "N+1 queries in the API layer", "Unnecessary re-renders in React"}}

### 12. Refactor & Roadmap

Based on all findings:

- Propose structural improvements (package splits, module reorganization).
- Create a prioritized refactor roadmap: fix-now vs. fix-later, with
  estimated complexity (S/M/L).
- Recommend changes to support {{SCALING_GOALS}} with minimal friction.
- Identify dead code from completed migrations that can be removed.

---

## Best Practices Evaluation

Evaluate the codebase against best practices relevant to its tech stack. The
generator should research and populate this section based on the project's
languages, frameworks, and deployment targets.

{{BEST_PRACTICES_TABLE — Generate a table per category (language, framework,
testing, cloud/ops, security) with columns: Practice | Check | Pass/Fail.
Tailor to the actual tech stack — don't include React practices for a CLI
tool or Lambda practices for a desktop app.}}

---

## Expected Output

Produce:

1. **Architecture report** — findings organized by the tasks above
2. **Dependency map** — actual import/dependency graph vs. intended graph,
   with violations highlighted
3. **Entity lifecycle diagrams** — annotated flows for each key entity,
   showing where transformations occur *(if the project has meaningful
   entity lifecycles)*
4. **State machine diagrams** — for each stateful subsystem identified in
   Goal 4 *(if applicable)*
5. **Best practices scorecard** — table with pass/fail/partial for each
   practice, with file:line references for failures
6. **Prioritized refactor roadmap** — fix-now vs. fix-later with complexity
   estimates
7. **Actionable recommendations** — specific, implementable suggestions with
   file paths and line references

Begin by scanning the directory and summarizing the project at a high level,
then proceed through each task systematically.

<!-- END TEMPLATE -->

---

## How to Fill the Placeholders

When adapting this template, replace each `{{PLACEHOLDER}}` with
project-specific details. Placeholders in `{{ALL_CAPS}}` are required;
placeholders with lowercase descriptions are guidance for the generator.

### Example 1: A Frontend React App (Dashboard)

| Placeholder | Value |
|-------------|-------|
| `{{PROJECT_TYPE}}` | React SPA with REST API backend |
| `{{TECH_STACK}}` | React 18, TypeScript, Redux Toolkit, TanStack Query |
| `{{MAJOR_LAYERS}}` | UI components, pages, Redux slices, API client, shared hooks |
| `{{KEY_ENTITIES}}` | User Session, Report, Dashboard Widget |
| `{{CORE_COMPLEX_LOGIC}}` | Data visualization rendering, Redux state reducers, real-time WebSocket sync |
| `{{ENTRY_POINTS}}` | React Router definitions, page components |
| `{{SPECIFIC_DATA_CONCERN}}` | TanStack Query caching strategies, unnecessary re-renders, optimistic updates |
| `{{CROSS_CUTTING_CONCERNS}}` | CSS/theming consistency, mobile responsiveness, i18n |
| `{{SCALING_GOALS}}` | Adding mobile app, supporting 50+ dashboard widgets, SSR migration |
| `{{SECURITY_CONCERNS}}` | XSS in user-generated content, CSRF tokens, JWT storage |
| `{{PERFORMANCE_CONCERNS}}` | Bundle size, unnecessary re-renders, image lazy loading |

### Example 2: A CLI Tool (Image Processor)

| Placeholder | Value |
|-------------|-------|
| `{{PROJECT_TYPE}}` | CLI tool for batch image processing |
| `{{TECH_STACK}}` | Rust, Clap, image-rs, rayon |
| `{{MAJOR_LAYERS}}` | CLI argument parsing, processing pipeline, codec layer, filesystem I/O |
| `{{KEY_ENTITIES}}` | Image Buffer, Configuration Object, Processing Job |
| `{{CORE_COMPLEX_LOGIC}}` | Compression algorithm, multithreading pipeline, color space conversion |
| `{{ENTRY_POINTS}}` | `main()` function, argument parser setup |
| `{{SPECIFIC_DATA_CONCERN}}` | File I/O safety, memory management (buffer overflows), temp file cleanup |
| `{{CROSS_CUTTING_CONCERNS}}` | Logging verbosity levels, exit codes, progress reporting |
| `{{SCALING_GOALS}}` | Supporting video formats, GPU acceleration, WASM compilation |
| `{{SECURITY_CONCERNS}}` | Path traversal in output paths, malicious image payloads (decompression bombs) |
| `{{PERFORMANCE_CONCERNS}}` | Memory usage for large images, thread pool sizing, codec benchmarks |

### Example 3: A Multi-Package Monorepo (Cloud Service)

| Placeholder | Value |
|-------------|-------|
| `{{PROJECT_TYPE}}` | Multi-package Python monorepo with cloud deployments |
| `{{TECH_STACK}}` | Python 3.13, Pydantic 2, Typer, boto3, google-cloud-storage |
| `{{MAJOR_LAYERS}}` | Core library, AWS provider, GCP provider, Lambda host, CF host, CLI |
| `{{KEY_ENTITIES}}` | ExtractedEntity, CanonicalEntity, EntityCatalog, SessionRegistry |
| `{{CORE_COMPLEX_LOGIC}}` | Extraction pipeline, catalog builder, convergence engine, session resolution, sampling |
| `{{ENTRY_POINTS}}` | Typer CLI, AWS Lambda handler, GCP Cloud Functions handler |
| `{{SPECIFIC_DATA_CONCERN}}` | JSONL artifact forwards-compatibility, state corruption resilience, cumulative index memory |
| `{{CROSS_CUTTING_CONCERNS}}` | OPSEC log isolation, datetime timezone awareness, entity naming conventions |
| `{{SCALING_GOALS}}` | Adding Azure/OCI providers, 10x log volume, GCP extractor parity with AWS |
| `{{SECURITY_CONCERNS}}` | OPSEC boundary (no deception terms in deployed code), no hardcoded credentials, import isolation |
| `{{PERFORMANCE_CONCERNS}}` | CatalogBuilder memory at 100K+ entities, string interning, orjson vs stdlib json |
