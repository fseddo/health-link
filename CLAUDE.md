# CLAUDE.md

This file gives Claude Code the context it needs to be productive on this project. Read this first before any task.

## What this project is

A fitness/strength-training app whose **primary purpose is to teach the developer applied AI/ML engineering**. The product itself is a real, useful workout tracker with health/recovery features, but every architectural decision should also serve the learning goal. If a choice between "ship faster" and "learn deeper" appears, ask before optimizing for the former.

Long-term: native iOS (Swift/SwiftUI) app with HealthKit integration. Short-term: Python/FastAPI backend with a minimal React frontend used only for development. The iOS app is the real client; the web frontend is throwaway.

## Core product features (target state)

- Strength workout logging (exercises, sets, reps, weight, RPE)
- Progressive overload suggestions (when to add weight or reps)
- Per-muscle, per-side soreness/recovery tracking with asymmetry detection
- LLM-powered coaching layer with personalized recommendations
- Food-photo → macros via vision LLM
- Diet tracking with reminders
- HealthKit integration: HRV, sleep, resting HR, training load, body weight, workout effort scores

## AI/ML scope (the actual learning target)

The ML work spans three tracks. The project is structured so each phase teaches a distinct skill:

1. **Classical ML** — progression suggestions, recovery curve modeling, asymmetry anomaly detection. scikit-learn, pandas, evaluation metrics, train/serve loop.
2. **Applied LLM engineering** — coaching agent with retrieval over user history. Prompts, evals, structured output, RAG using pgvector.
3. **Vision** — food photo parsing via Claude or GPT-4V. Multimodal prompting, structured output, confidence handling.

The evaluation discipline matters more than the models. Every ML feature must ship with an eval suite.

## Tech stack (locked)

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2
- **Database**: Postgres 16 with pgvector extension (use `pgvector/pgvector:pg16` image)
- **Auth**: Email + password, bcrypt or argon2, JWT access tokens + refresh tokens (persisted, hashed)
- **ML libraries**: scikit-learn, pandas, numpy. PyTorch later if needed.
- **LLM**: Anthropic SDK directly. No LangChain — it obscures what's happening and that's the opposite of the learning goal.
- **Frontend (dev only)**: Vite + React + TypeScript + Tailwind + shadcn/ui + TanStack Query
- **Type sharing**: Generate TS types from FastAPI's OpenAPI schema (`openapi-typescript`)
- **Containers**: Docker Compose for local Postgres + any future services
- **Deployment**: Railway or Fly.io (decide when needed)
- **Eventual iOS**: Swift/SwiftUI, talks to same backend, reads HealthKit, writes summarized data back

## Conventions

### Units (critical — don't get this wrong)
- **Internal storage is canonical SI**: kg for weight, meters for distance, seconds for time, cm for measurements.
- **Display is per-user preference**: `users.weight_unit_preference` (`'lbs'` default).
- Conversion happens in API serializers. Database, ML pipelines, and internal code never see lbs/miles.
- Never store derived "display values" alongside canonical values.

### Soft delete
- Soft delete applies to **user-generated journal/event data**: users, workouts, soreness_reports, nutrition_entries, body_measurements.
- Children of those parents filter via JOIN to parent's `deleted_at`.
- Default queries exclude soft-deleted rows.
- **Reference data uses hard delete with FK-restrict**, not soft delete. This includes `muscle_groups` (seeded, effectively immutable) and `exercises` (both built-in and user-customised). A custom exercise that has been used in any workout cannot be deleted — the FK constraint blocks it and the API returns 409. See ADR-002 and `docs/SCHEMA.md` `exercises` "Deletion" for full rationale.

### IDs
- All primary keys are UUIDs.
- Sync-sensitive tables (workouts) accept a client-generated `client_id` for idempotency. Server rejects duplicates per-user with 409.

### API design
- REST, JSON in/out, ISO 8601 UTC timestamps.
- Versioned routes under `/api/v1/`.
- Every list endpoint paginated with cursors (even when data is small — design once).
- Endpoints designed assuming a mobile client will consume them. Never assume web-only.
- OpenAPI schema is the contract. Keep Pydantic models clean and well-documented.

### Source tracking
- Every imported/synced piece of data has a `source` column: `'manual'`, `'healthkit'`, `'photo'`, `'mock'`, `'estimated'`. ML code uses this for data quality decisions.

### Asymmetry signal
- Per-side data lives in `soreness_reports`, `body_measurements`, and `sets` (when exercise is unilateral).
- Bilateral exercises do **not** expose left/right at the set level. Don't try to split squat-set data per side.

### ML conventions
- Every ML feature has a corresponding eval suite in `evals/`.
- Models go in `ml/` with a clear interface (train.py, predict.py, eval.py).
- Synthetic data generators live in `ml/data/` for bootstrapping models without real user data.
- Prompts for LLM features live in `prompts/` as plain text files or Python constants, version-controlled.
- Evals run in CI eventually; for now, runnable via `make eval` or equivalent.

### What NOT to do
- Don't use LangChain or similar high-level LLM frameworks. Raw Anthropic SDK calls only.
- Don't add features outside the current phase's scope without asking.
- Don't over-engineer the web frontend. It is throwaway. Minimal styling via shadcn defaults; no design polish.
- Don't write tests for the frontend. Backend and ML get tests; frontend gets manual clicking.
- Don't denormalize derived values (PRs, 1RM estimates, volume). Compute at query time.
- Don't add ORM abstractions on top of SQLAlchemy. SQLAlchemy 2.0 is already the abstraction.
- Don't store anything from HealthKit at sub-daily granularity in Postgres. Daily roll-ups only.

## Phase structure

The project is built in phases. Don't jump ahead. Each phase has a clear "done" state.

Phase order: Foundation → Synthetic HealthKit data → Classical ML (progression) → **iOS port** → LLM coaching → Recovery & asymmetry → Food vision → Diet tracking.

The iOS port lands at Phase 3, before the deeper ML work, because HealthKit data is structurally central to coaching and recovery models. Phases 1 and 2 build the architecture with mocked HealthKit data; Phase 3 swaps in real data via the same endpoints.

See `docs/ROADMAP.md` for the full phase plan.

Current phase: **Phase 1 — Foundation**.

## Literature priors layer

A literature-priors layer — peer-reviewed research encoded as structured
Python priors for the recommendation engine/optimizer — is in active
development in the **untracked `priors-handoff/`** directory. It is Phase 2
work built ahead and is not yet integrated into the repo proper.

If working on it, read the live state docs first:
`priors-handoff/docs/priors/BACKLOG.md` (current state + next steps),
`COVERAGE.md` (coverage + gaps), `SESSION_LOG.md` (history). New papers are
added through the agent pipeline in `.claude/agents/priors-*.md`
(seeker → relevance-checker → entry-maker → auditor; an independent audit is a
mandatory gate). See also the `project-priors-layer` memory.

## Asking for help

When you need clarification:
- For ambiguous schema changes: propose an option and ask before applying.
- For new dependencies: list the reason and the alternative, ask before adding.
- For new tables or columns: pause and propose before creating migration.
- For new endpoints outside the current phase: ask before implementing.

When in doubt: smaller, clearer commits over larger ones.

## File layout (target)

```
.
├── backend/
│   ├── app/
│   │   ├── api/v1/         # FastAPI routers
│   │   ├── core/           # config, security, auth
│   │   ├── db/             # SQLAlchemy models, session
│   │   ├── schemas/        # Pydantic models
│   │   ├── services/       # business logic
│   │   └── main.py
│   ├── alembic/            # migrations
│   ├── ml/                 # training, prediction, eval
│   │   ├── progression/
│   │   ├── recovery/
│   │   └── data/           # synthetic data generators
│   ├── evals/              # LLM eval suites
│   ├── prompts/            # LLM prompts as text
│   ├── tests/
│   ├── pyproject.toml
│   └── docker-compose.yml
├── frontend/               # Vite + React + TS, dev-only
│   ├── src/
│   └── package.json
├── ios/                    # Added in Phase 3; Swift/SwiftUI app
│   └── (Xcode project)
├── docs/
│   ├── ROADMAP.md
│   ├── SCHEMA.md
│   └── DECISIONS.md        # ADRs for non-obvious choices
└── CLAUDE.md
```

The `ios/` directory may be its own Git repo or a subdirectory — decide at Phase 3 start. Either way, it consumes the same backend API.

## When you finish a task

- Run the test suite if one exists for the area you touched.
- Update `docs/DECISIONS.md` if you made a non-obvious architectural choice.
- Update `docs/ROADMAP.md` to check off completed work.
- If you added a model or migration, update `docs/SCHEMA.md`.

## What's already decided (don't re-litigate)

- Postgres over SQLite — committed, simpler than migrating.
- pgvector extension — installed from day one, used in Phase 4.
- UUIDs over bigints.
- Soft delete pattern documented above.
- Web frontend stays minimal and disposable.
- **iOS port happens at Phase 3** — earlier than originally planned — because HealthKit data is central to the deeper ML in Phases 4–5.
- Synthetic HealthKit data (`source='mock'`) is generated in Phase 1.5 to unblock ML development before iOS exists.
- ML code treats `source='mock'` and `source='healthkit'` identically; no special-casing.
- kg internal, lbs display.
- Raw Anthropic SDK, not LangChain.

If you think any of these need revisiting, raise it explicitly with reasoning.
