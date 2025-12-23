# PB Tourney

**Full-Stack Tournament Management System for Pickleball**

A production-ready web application for organizing and managing round-robin pickleball tournaments with support for fixed and rotating partner formats, league management, and role-based access control.

---

## Project Metrics

| Metric | Value |
|--------|-------|
| **Development Period** | November 1 – December 21, 2025 (51 days) |
| **Total Commits** | 262 |
| **Lines of Code** | ~32,300 (16,200 Python + 16,100 TypeScript) |
| **Test Coverage** | 382 automated tests across 13,200 lines of test code |
| **Manual Code Written** | 0 lines — entirely AI-assisted implementation |
| **AI Tool** | Claude Code (Anthropic) |

---

## Development Approach

This project was built using **entirely AI-assisted implementation** through Claude Code. Every line of code—backend, frontend, tests, configuration, and documentation—was generated through AI pair programming. The developer provided requirements, architectural direction, and review; Claude Code handled all implementation.

This approach demonstrated:
- **Rapid iteration**: Full-stack application built in 51 days
- **Comprehensive testing**: 382 tests written alongside features
- **Consistent quality**: Automated linting, type checking, and formatting from day one
- **Production-ready architecture**: Repository pattern, dependency injection, and domain-driven design

---

## Features

### Tournament Management
- Round-robin tournament generation with automatic scheduling
- Fixed partners and rotating partners formats
- Skill-based team seeding algorithms
- Court assignment with variety optimization
- Multi-level tiebreaker standings calculation

### Score Reporting
- Player-reported scores with confirmation workflow
- Director override capabilities
- Score dispute resolution
- Single-game and best-of-three scoring formats

### User Management
- JWT-based authentication
- Role-based access control (League Owner, Tournament Director, Participant)
- Fine-grained permission system

### League Organization
- Multi-league support
- Tournament grouping by league
- Director and participant management

---

## Technology Stack

### Backend (Python)

| Category | Technologies |
|----------|-------------|
| **Framework** | FastAPI, Uvicorn (ASGI) |
| **Database** | SQLAlchemy 2.0, PostgreSQL (prod), SQLite (dev) |
| **Validation** | Pydantic v2 |
| **Authentication** | JWT (python-jose), bcrypt, passlib |
| **CLI** | Typer, Rich |
| **HTTP Client** | httpx |
| **Rate Limiting** | SlowAPI |
| **Integrations** | Slack API, iCalendar (ics) |

### Frontend (TypeScript)

| Category | Technologies |
|----------|-------------|
| **Framework** | React 19 |
| **Routing** | React Router DOM |
| **State Management** | TanStack React Query |
| **Forms** | React Hook Form, Zod |
| **HTTP Client** | Axios |
| **Styling** | Tailwind CSS, Headless UI, Heroicons |
| **Build Tool** | Vite |
| **Date Handling** | date-fns |

### DevOps & Infrastructure

| Category | Technologies |
|----------|-------------|
| **Containerization** | Docker (multi-stage builds) |
| **CI/CD** | GitHub Actions |
| **Deployment** | Fly.io |
| **Web Server** | Caddy (reverse proxy) |
| **Pre-commit** | pre-commit hooks |

### Testing & Quality

| Category | Technologies |
|----------|-------------|
| **Test Framework** | pytest, pytest-asyncio |
| **Coverage** | pytest-cov |
| **Python Linting** | Ruff |
| **Python Types** | Pyright |
| **JS/TS Linting** | ESLint |
| **Formatting** | Ruff (Python), Prettier (JS/TS) |

---

## Architecture

### Project Structure

```
src/pbtourney/
├── api/                    # FastAPI application layer
│   ├── app.py             # App initialization, middleware
│   ├── dependencies.py    # Dependency injection
│   ├── schemas.py         # Pydantic models
│   └── routes/            # REST endpoints
├── domain/                 # Business logic (framework-agnostic)
│   ├── auth.py            # Authentication
│   ├── permissions.py     # Authorization
│   ├── tournament_engine.py
│   ├── scheduling/        # Round-robin algorithms
│   ├── seeding.py
│   ├── standings.py
│   └── scoring.py
├── persistence/db/        # Database layer
│   ├── models.py          # SQLAlchemy ORM
│   └── repositories.py    # Data access
├── cli/                   # Command-line interface
└── infra/                 # Logging, notifications, utilities

web/src/
├── components/            # React components
├── context/               # Auth, Toast, Error contexts
├── types/                 # TypeScript definitions
└── utils/                 # Helpers
```

### Design Patterns

- **Repository Pattern** — Abstracts data access from business logic
- **Dependency Injection** — FastAPI's `Depends()` for loose coupling
- **Service Layer** — Domain logic separated from API and persistence
- **State Machine** — Match lifecycle (scheduled → in_progress → pending_confirmation → completed)
- **Domain-Driven Design** — Clear boundaries between API, domain, and persistence layers

### Data Model

```
League (owners)
  └── Tournament (directors)
        ├── Participants (users)
        ├── Teams
        └── Matches
```

---

## Key Algorithms

### Round-Robin Scheduling
Circle method for fixed partners; rotation algorithm for rotating partners format. Generates complete tournament schedule at start.

### Team Seeding
Skill-based pairing: highest-rated with lowest-rated to create balanced teams.

### Court Assignment
Maximizes court variety per player by tracking assignment history and optimizing distribution.

### Standings Calculation
5-level tiebreaker system:
1. Wins
2. Point differential
3. Head-to-head record
4. Points scored
5. Alphabetical (deterministic fallback)

---

## CI/CD Pipeline

### Continuous Integration (GitHub Actions)
- **Backend**: Python 3.12, uv sync, Pyright type checking, Ruff linting, pytest
- **Frontend**: Node.js 22, npm ci, TypeScript compilation, ESLint, Vite build

### Continuous Deployment
- Automatic deployment to Fly.io on push to main
- Multi-stage Docker build for optimized images
- Git version tracking in builds

### Pre-commit Hooks
- Ruff format and lint
- Trailing whitespace, EOF fixes
- YAML/JSON/TOML validation
- pytest execution

---

## API Documentation

Interactive API documentation available at `/docs` (Swagger UI) when running locally.

### Key Endpoints
- `POST /auth/register`, `POST /auth/login` — Authentication
- `GET/POST /leagues` — League management
- `GET/POST /tournaments` — Tournament CRUD
- `POST /tournaments/{id}/start` — Begin tournament
- `PATCH /matches/{id}/score` — Report score
- `POST /matches/{id}/confirm` — Confirm score
- `GET /tournaments/{id}/standings` — View standings

---

## What This Project Demonstrates

1. **AI-Accelerated Development** — Complete application built through AI pair programming
2. **Modern Python Backend** — FastAPI, SQLAlchemy 2.0, Pydantic v2, type hints throughout
3. **Modern React Frontend** — React 19, TypeScript, TanStack Query, Tailwind CSS
4. **Production-Ready Infrastructure** — Docker, CI/CD, automated testing, deployment
5. **Clean Architecture** — Separation of concerns, testability, maintainability
6. **Comprehensive Testing** — Unit and integration tests with high coverage
7. **Algorithm Implementation** — Scheduling, seeding, standings calculation

---

## Links

- **Resume**: [Jon Richards](https://github.com/gorgeguy/gorgeguy-home/blob/main/RESUME.md)
