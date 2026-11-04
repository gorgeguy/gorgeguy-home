## **Jon Richards**
**Software Development Consultant · Agentic Engineering**
Hood River, Oregon • jon@gorgeguy.com • gorgeguy.com • github.com/gorgeguy

---

### **Summary**
I build software, and I help businesses adapt how they build it as AI coding agents take over more of the work. My 33 years span databases, infrastructure automation and multicloud platforms (AWS, GCP, Azure, OCI), at Informix, at Oracle and now with a multicloud SaaS client. Since 2025 I have built nearly everything by directing Claude Code and OpenAI Codex, often several agents at once, along with the reviews, gates and habits that make their output trustworthy. Agents made writing code in any language cheap. What they didn't make cheap is knowing what to build and whether it's right, and that comes from domain depth. This is the most interesting shift of my career, and I share what I learn as I go.

---

### **How I Work With Agents**
- **A shared team agent with written delegation rules: about 1,000 requests in six weeks, 65% from five teammates.** Engineers ask it in Slack for PR reviews, root-cause analysis, fixes and builds. Its rules say who may request a merge, pre-authorize small fixes within six scope limits, attribute every PR to its requester, and re-run CI before any merge.
- **Plan → tickets → autonomous execution → human gates.** Designs become dependency-safe tickets and are audited with fresh eyes. Agents then work them one at a time, claim tickets atomically, and escalate to a person when blocked (319 tickets closed autonomously, 32 escalated).
- **Parallel agents without collisions.** I run 3–9 agent sessions at once in isolated git worktrees. One landing coordinator merges their work, history is merge-only, and quality gates run on the integrated commit.
- **Cross-model review.** Codex reviews Claude's plans and code, and Claude reviews Codex's. Every finding is checked against the code before anyone acts on it. Built agent-review-loop (open source) so two agents can iterate as editor and reviewer.
- **Long-horizon autonomy.** Goal-driven agent runs of up to 64 hours for end-to-end cloud validation, with explicit completion criteria and stop conditions.
- **Context first.** My agents work from the same context I do. Claude Briefcase (below) gathers my email, calendar, meeting notes, Slack, Jira and pull requests into notes and a tracker that any agent session can query.
- **Agent-safe hygiene.**
  - Typed credential descriptors let agents call APIs without secrets reaching command lines, logs or transcripts.
  - Provenance rules keep unverified content out of recorded decisions.
  - Each repo has one `AGENTS.md`, read by Claude Code, Codex and Cursor alike.
- **Teaching it.** Led an agentic-engineering session for a client's engineering team. Packaged the team's review standards as one skill that installs into Codex, Claude Code and Cursor.

---

### **Domains**
- **Cloud platforms: AWS, GCP, Azure, OCI.** Multi-account organizations, IAM, serverless and event-driven services, infrastructure as code.
- **High-volume data pipelines.** Event ingestion and processing across clouds, plus the performance engineering to make it fast.
- **Multicloud SaaS platforms.** Provider-plugin architecture, versioned data contracts, in-place upgrades.
- **Databases.** From RDBMS kernel internals (threading, BLOB storage, transaction logging) to Postgres schema unification and migrations.
- **Infrastructure and provisioning automation.** Cloud region build-out, bare-metal/PXE edge provisioning, rack-scale backup and restore, VM image assembly (2 patents).
- **Release engineering.** CI gating, VM-based release qualification, runtime and dependency patching.
- **Product software.** Mobile and web community apps; small-business bookkeeping automation.

---

### **Experience**

**Multicloud SaaS company (client of GorgeGuy Solutions) — Software Development Consultant**
_Remote | 2026–present_
- **Core services.** Designed and built core services for a multicloud product across AWS, GCP and Azure.
- **Pipeline performance.** Cut a high-volume event pipeline's runtime by 52% and raised its throughput by 87%.
- **Codebase consolidation.** Led the merge of separate per-cloud codebases into one multicloud codebase, using a provider-plugin architecture and versioned data contracts enforced by contract tests.
- **Database.** Unified the Postgres schema across cloud providers and built the numbered, re-runnable migration path for in-place product upgrades.
- **CI and release qualification.**
  - Added CI gating on every pull request.
  - Built an on-demand release-qualification job: it provisions a clean VM, installs the release, verifies services, and always cleans up.
- **Patching.** Kept the runtime and dependencies current: Node and Python patch floors, CA trust-store corrections, dependency audits.
- **Team practice.** One of the primary cross-team code reviewers. Introduced the team's shared agent, agent instructions and review standards (see above).

**GorgeGuy Solutions — Founder & Software Development Consultant**
_Hood River, OR | 2025–present_
- **Consulting.** I build software for clients and for my own products. I also help businesses adapt their development practices to agentic engineering: standards, workflows, review gates, shared team agents and training.
- **Claude Briefcase** (my creation; open source) is a personal work-intelligence system run by Claude Code.
  - It pulls from Gmail, Google Calendar, Google Drive meeting transcripts, Slack channels and DMs, Jira and Bitbucket.
  - It turns that into structured notes, an action and decision tracker, and a daily briefing delivered to me in Slack.
  - In daily use for eight months, it has processed 1,100+ email threads and 600+ Slack threads into 260+ notes, and tracked 160+ Jira issues.
- **Briefcase workboard.** Its personal app is a live workboard: an always-on local web app where I reprioritize, defer and close work.
  - My edits on the board feed into the next briefing.
  - Pull requests and tickets close themselves when their system of record says they're done.
- **Briefcase ad-hoc queries.** Between briefings I ask it questions and it acts on the answers: "What is my client asking of me today?" "Which of my PRs cover the Node 24 upgrade?" and then "Add these two reviewers to both." It answers from the collected context and makes the change.
- **Briefcase architecture.** Subagents fetch issue-tracker and pull-request data, so raw API output never crowds the main context. Mail and documents come through a self-hosted, read-only Google Workspace MCP server.
- **pbmatch:** an iOS, Android and web app for organizing pickup games (Expo/React Native, Supabase/Postgres).
  - Built by three coordinated agents working in separate worktrees and claiming tickets from a shared queue.
  - UI changes are verified across iOS, Android and web at normal and large text sizes: 132 dated verification records and 79 automated UI flows to date.
- **PB Tourney:** a full-stack tournament app (FastAPI, React, Postgres): 262 commits and 382 tests in 51 days. My first all-agent build (Nov 2025).
- **port-manager:** a Rust CLI published on crates.io, shipped without prior Rust experience.

**Oracle Corporation — Principal Software Engineer**
_Hillsboro, OR | 1999–2025_
- **Cloud region build automation:** built and maintained the applications and processes used to construct new OCI data centers worldwide.
- **Edge provisioning:** led design and implementation of PXE-based installation and configuration for OCI Roving Edge Infrastructure devices.
- **Backup and restore:** automated full-rack backup and restore for Oracle Cloud at Customer, cutting iteration time from 5 days to 5 hours.
- **Media performance:** designed a benchmarking framework for OCI Digital Media Services that measures FFmpeg transcode performance across compute shapes.
- **Virtualization:** co-invented patented VM image assembly technology for multi-tier installations.

**Informix Corporation — Software Engineer**
_Portland, OR | 1993–1999_
- **Database kernel:** developed a non-preemptive threading library in assembly for SMP architectures.
- **Query observability:** built a real-time graphical tool for monitoring parallel SQL queries.
- **Storage:** implemented Binary Large Object (BLOB) storage and enhanced the transaction logging subsystems.

---

### **Patents**
- *US 9,690,607* — Automated VM assembly and deployment (2017)
- *US 9,612,803* — Multi-node virtual appliance construction (2017)

---

### **Education**
**B.S. Computer Science** — Portland State University, Portland, OR

---

### **Implementation**

**Agents:** Claude Code, OpenAI Codex, Cursor, MCP servers, Beads

**Languages:** Python, JavaScript and TypeScript (Node.js, React, React Native), SQL (Postgres), Bash, Rust; earlier in my career, Java, C and assembly

**AWS:** Lambda, SQS, SNS, S3, EventBridge, CloudFormation and SAM, CodeBuild, CodeDeploy, CodeArtifact, IAM, Organizations, Systems Manager, Secrets Manager, CloudWatch, EC2

**GCP:** Cloud Functions, Cloud Run, Eventarc, Pub/Sub, Cloud Storage, Secret Manager, Cloud KMS, IAM

**Azure:** Azure Functions, Event Hubs, Blob Storage, Resource Manager, Entra ID

**OCI:** Compute, Container Instances, OCI SDK and CLI

**Delivery and runtime:** Bitbucket Pipelines, GitHub Actions, Docker, Linux/systemd, Postgres, Redis, Express, FastAPI, Supabase
