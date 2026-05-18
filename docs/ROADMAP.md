# Roadmap

Phased build plan. Each phase has a definition of done. Don't start a phase until the previous one is complete.

## Phase overview

| Phase | Focus | Approx. duration |
|---|---|---|
| 0 | Scaffolding: rule docs, schema draft, review tooling | complete |
| 1 | Foundation: backend + minimal web frontend | 1–2 weeks |
| 1.5 | Synthetic HealthKit data generator | ~3 days |
| 2 | Classical ML: progression suggestions | 2 weeks |
| 3 | iOS port (Swift/SwiftUI + real HealthKit) | 3–4 weeks |
| 4 | LLM coaching with RAG | 2 weeks |
| 5 | Recovery modeling + asymmetry detection | 1–2 weeks |
| 6 | Food photo → macros | 1 week |
| 7 | Diet tracking + reminders | TBD |

The iOS port is intentionally placed at Phase 3 rather than later. Rationale: HealthKit data is structurally central to the ML in Phases 4–5, and the developer wants to use the app personally. Phases 1 and 2 establish the ML loop using mocked HealthKit data; Phase 3 swaps the mock for real HealthKit before the coaching and recovery models go deep.

---

## Phase 0 — Scaffolding (complete)

**Goal**: Repository and documentation in shape before any code lands. No source code yet.

- [x] Root `CLAUDE.md` with project-wide rules, conventions, locked decisions
- [x] Per-component `backend/CLAUDE.md` and `frontend/CLAUDE.md` with overarching rules specific to each
- [x] `docs/ROADMAP.md` (this file), `docs/SCHEMA.md` (database schema draft), `docs/DECISIONS.md` (ADR-001 … ADR-007)
- [x] `.gitignore` covering Python (uv, pytest, mypy), Node, OS, IDE, ML artifacts
- [x] `/dual-review` project-local slash command with `code-reviewer` and `code-review-auditor` sub-agents at `.claude/`
- [x] `backend/docs/` and `frontend/docs/` README placeholders describing what each folder will contain

**Definition of done**: A new contributor can clone the repo, read `CLAUDE.md` + the three top-level docs, and understand what the project is, what's already decided, and how Phase 1 will be evaluated — without reading any code. ✅

---

## Phase 1 — Foundation (1–2 weeks)

**Goal**: Working backend + minimal frontend where a user can register, log in, log a workout with sets, view history. No ML yet.

### Backend
- [ ] FastAPI project skeleton
- [ ] Docker Compose with Postgres 16 (pgvector image) and the FastAPI service
- [ ] SQLAlchemy 2.0 models for all tables in SCHEMA.md
- [ ] Alembic initial migration with seed data for muscle_groups and a starter exercise catalog (~50 common lifts)
- [ ] Email + password auth with JWT access + refresh tokens
- [ ] Endpoints:
  - `POST /api/v1/auth/register`
  - `POST /api/v1/auth/login`
  - `POST /api/v1/auth/refresh`
  - `POST /api/v1/auth/logout` (revokes refresh)
  - `GET /api/v1/me`
  - `PATCH /api/v1/me` (update profile, weight_unit_preference, etc.)
  - `GET /api/v1/exercises` (paginated, searchable)
  - `POST /api/v1/exercises` (custom user exercise)
  - `GET /api/v1/workouts` (paginated, by date range)
  - `POST /api/v1/workouts` (create with idempotency via client_id)
  - `GET /api/v1/workouts/{id}` (full nested representation)
  - `PATCH /api/v1/workouts/{id}` (rename, notes)
  - `DELETE /api/v1/workouts/{id}` (soft delete)
  - `POST /api/v1/workouts/{id}/exercises`
  - `POST /api/v1/workout-exercises/{id}/sets`
  - `PATCH /api/v1/sets/{id}`
  - `DELETE /api/v1/sets/{id}` (hard delete; cascade with workout soft-delete)
  - `POST /api/v1/soreness-reports`
  - `GET /api/v1/soreness-reports` (filterable by muscle group, date range)
- [ ] Pydantic schemas with `weight_kg` ↔ display-unit conversion in serializers
- [ ] pytest setup with at least smoke tests for auth and workout CRUD
- [ ] Generate OpenAPI schema; verify `/docs` renders

### Frontend (minimal, throwaway)
- [ ] Vite + React + TypeScript + Tailwind + shadcn/ui scaffold
- [ ] TanStack Query setup
- [ ] Generated types from backend OpenAPI (`openapi-typescript`)
- [ ] Pages: Login, Register, Workout List, Workout Detail (log sets), Soreness Log
- [ ] No design polish. Default shadcn components. Functional only.

### Definition of done
- Developer can: register, log in, create a workout, add exercises and sets, log soreness, view past workouts. Everything persists. All operations work via the web UI and via curl/HTTPie.

---

## Phase 1.5 — Synthetic HealthKit Data Generator (~3 days)

**Goal**: Generate realistic health data and load it into `health_snapshots` with `source='mock'`, so all downstream ML can consume health context before the iOS port lands.

This phase exists because HealthKit data is essential context for the ML in Phases 4–5, and we don't want to defer those phases until iOS is built. Generating synthetic data forces the data pipeline and API design now, and is itself a legitimate AI/ML engineering artifact.

### Tasks
- [ ] `ml/data/generate_health_data.py`:
  - Simulates a single user's HealthKit-equivalent metrics across a configurable date range
  - Produces daily records for: `resting_heart_rate`, `hrv_sdnn_ms`, `sleep_hours`, `sleep_quality_score`, `wrist_temp_deviation_c`, `body_weight_kg`, `body_fat_percent`, `training_load_category`, `active_energy_kcal`
  - Models realistic correlations: poor sleep → elevated resting HR + lower HRV the next day; heavy training day → elevated active energy + temperature deviation; gradual body weight trends
  - Models realistic noise and missing data (some days have partial data, mirroring real HealthKit gaps)
  - Configurable user archetypes (well-recovered athlete, overtrained, beginner, etc.) for generating varied datasets
- [ ] Endpoint: `POST /api/v1/health-snapshots/batch` accepts an array of snapshots (this is also the endpoint the iOS app will use in Phase 3 — design it correctly now)
- [ ] CLI or Make target: `make seed-health-data USER=<email> DAYS=90` populates a user's history
- [ ] All ML code that reads `health_snapshots` treats `source='mock'` and `source='healthkit'` identically — no special-casing
- [ ] Document the generator's assumptions and limitations in `ml/data/README.md` (what's realistic, what's hand-waved)

### Definition of done
Running the seed command for a user produces 90+ days of realistic health snapshots in the database. The `POST /api/v1/health-snapshots/batch` endpoint is the same one the iOS app will call in Phase 3 — no contract changes needed at port time.

---

## Phase 2 — Classical ML: Progression Suggestions (2 weeks)

**Goal**: When the user views an exercise, the app suggests whether to increase weight, add reps, hold, or deload, based on recent performance.

### Approach
Start rules-based to validate the concept, then replace with a trained model. The replacement is the point — comparing rules vs. ML is exactly the kind of empirical thinking the role requires.

### Tasks
- [ ] Rules-based baseline:
  - "Hit top of rep range with RPE ≤ 8 on most recent set across 2 consecutive workouts → suggest +2.5 kg"
  - "Failed to hit bottom of rep range with RPE 9–10 → suggest deload 10%"
  - "Otherwise → hold"
  - Endpoint: `GET /api/v1/exercises/{id}/suggestion?user_id=...`
- [ ] Synthetic training data generator:
  - `ml/data/generate_progression_data.py`
  - Simulates a user's lift history under different progression patterns (linear, plateauing, deloading)
  - Outputs (features, label) pairs where label ∈ {increase_weight, increase_reps, hold, deload}
- [ ] Feature engineering:
  - Estimated 1RM (Epley)
  - Rolling avg RPE last 3 sessions
  - Rep range hit ratio
  - Days since last session for this exercise
  - Volume trend (slope over last 4 sessions)
- [ ] Model:
  - Train a scikit-learn classifier (start with LogisticRegression, also try RandomForest, GradientBoosting)
  - Evaluate with stratified k-fold, report precision/recall/F1 per class
  - Persist model with joblib in `ml/progression/model.joblib`
- [ ] Inference endpoint replaces the rules-based one (keep rules-based available behind a flag for comparison)
- [ ] Eval suite:
  - Hold-out test set with hand-labeled "correct" suggestions
  - Compare ML model vs. rules baseline
  - Track metrics over time as model changes

### Definition of done
Suggestion endpoint serves predictions from a trained model. Eval script outputs a comparison table of rules vs. ML. ADR written explaining feature choices and tradeoffs.

---

## Phase 3 — Port to Swift / iOS (3–4 weeks)

**Goal**: Native iOS client against the existing backend. Replace mocked HealthKit data with the real thing. The web frontend stays for development convenience but is no longer the primary client.

### Why iOS now (not later)
The ML features in Phases 4 and 5 depend heavily on health data (HRV, sleep, training load). Phases 1 and 2 prove the architecture with mocked data; Phase 3 swaps in real data before we go deep on the models that consume it. Also: the developer wants to use this app personally as their primary fitness tracker, and that requires iOS.

### Approach
Don't change the backend contract. The whole point of the API discipline so far is that the iOS client is just a new consumer of the same endpoints the web frontend and seeding scripts already use. Specifically: `POST /api/v1/health-snapshots/batch` is the same endpoint Phase 1.5's generator uses — the iOS app sends real HealthKit data through it with `source='healthkit'`.

### Swift learning curve
Budget the first ~1 week of this phase for Swift/SwiftUI fundamentals if not already known. Build a throwaway HealthKit-reading app first (just display some HRV data) before integrating with the real backend. Resist the urge to start with the real project; the fundamentals time pays for itself.

### Tasks
- [ ] Swift/SwiftUI fundamentals (skip if known): a throwaway app that reads recent HKWorkout and HRV samples, displays them in a list. Focus areas: SwiftUI views and state, async/await, HealthKit permissions and queries.
- [ ] Main app skeleton:
  - SwiftUI project, dependency setup
  - Auth flow: login, register, token storage in Keychain
  - Generated Swift client from OpenAPI (use `openapi-generator` Swift target, or hand-write for learning — recommend hand-writing the auth + a couple of endpoints, then generate the rest)
  - API client layer with automatic refresh-token handling
- [ ] Core screens:
  - Workout list (date-grouped)
  - Workout logging (live editing: add exercise, add set, edit weight/reps/RPE inline)
  - Workout detail (read-only history view)
  - Soreness log
  - Settings (unit preference, account management)
- [ ] HealthKit integration:
  - Permissions flow requesting read scopes for: workouts, HRV, resting HR, heart rate, sleep analysis, body mass, body fat %, active energy, wrist temperature, workout effort score
  - Daily sync routine that reads the last 24h of relevant data, aggregates per-day, and POSTs to `/api/v1/health-snapshots/batch` with `source='healthkit'`
  - Background delivery via `HKObserverQuery` so syncs happen without app being open
  - Write `HKWorkout` (type `.traditionalStrengthTraining`) on workout completion so Apple Health gives activity ring credit
  - Write `workoutEffortScore` if the user provides one
- [ ] Bluetooth scale: rely on HealthKit (most scales sync there automatically); no direct CoreBluetooth work needed in this phase
- [ ] Deprecate mocked health data flow: keep the generator for tests and eval but stop running it against your personal account; real HealthKit data replaces it

### Definition of done
- App installed on personal device, used at the gym for real workouts
- HealthKit data flowing into backend `health_snapshots` daily
- Mock data generator still works for tests/evals but isn't used in production for the developer's account
- Backend has not been substantively changed; iOS is purely a new client

---

## Phase 4 — LLM Coaching with RAG (2 weeks)

**Goal**: User can ask "How's my squat progressing?" or "Should I take a rest day?" and get a personalized, context-aware response that uses both lifting and HealthKit data.

By this phase, the user has real HealthKit data flowing, so coaching responses can reference HRV trends, sleep patterns, and training load alongside lifting performance.

### Tasks
- [ ] Embedding pipeline:
  - Embed user workout summaries (one row per workout) and soreness reports
  - Store in pgvector
  - Background job to re-embed on data changes (simple: re-embed on write for now)
- [ ] Retrieval:
  - Given a user question, retrieve top-K relevant past workouts + recent soreness + recent suggestions
  - Always include recent health snapshots (last 7 days) regardless of question — they're cheap and contextually valuable
  - Plain cosine similarity for now; experiment with hybrid (recency boost) later
- [ ] Coaching agent:
  - System prompt in `prompts/coach_system.md`
  - Constructs context window: user profile + retrieved data + recent health snapshots + question
  - Calls Claude via Anthropic SDK
  - Returns structured response (chat text + optional action: "log_rest_day", "suggest_alternative_exercise")
- [ ] Endpoint: `POST /api/v1/coach/message` (streaming optional but nice)
- [ ] Eval suite:
  - 20–30 test cases: question + user state + expected response qualities
  - Use a "judge" LLM (Claude in eval mode) to score responses on: factual accuracy (no hallucinated PRs), personalization (uses actual user data), actionability
  - Track regression across prompt changes
- [ ] iOS chat UI: SwiftUI chat view with message list and input field

### Definition of done
End-to-end coaching feature works on iOS. Eval suite runs with `make eval-coach`. Documented prompt iteration log in `prompts/coach_changelog.md`.

---

## Phase 5 — Recovery Modeling + Asymmetry Detection (1–2 weeks)

**Goal**: Given soreness reports, workout history, and health snapshots, predict per-muscle recovery curves; flag asymmetry between left and right.

By this phase you have real HealthKit data, so recovery models can use HRV and sleep as inputs alongside subjective soreness — meaningfully better than the soreness-only approach.

### Tasks
- [ ] Recovery curve estimation:
  - Per muscle group, fit a decay model to soreness data over time
  - Incorporate HRV and sleep as recovery accelerators in the model
  - Endpoint: `GET /api/v1/recovery/status` returns per-muscle expected recovery time
- [ ] Asymmetry detection:
  - Compare left vs. right soreness severity for paired muscle groups
  - Compare left vs. right body measurements over time
  - Compare per-side performance on unilateral exercises
  - Statistical test: are differences systematic or noise?
  - When systematic, surface in coaching prompts and in a dedicated endpoint
- [ ] Integration with coaching:
  - Coach prompt gains access to recovery + asymmetry signals
  - "Your right quad has been consistently more sore than your left — consider unilateral work this week"
- [ ] iOS UI: recovery dashboard showing per-muscle status; asymmetry callouts
- [ ] Eval: synthetic asymmetric users — does the model detect injected asymmetries?

### Definition of done
Recovery + asymmetry endpoints work, integrated into coaching, eval'd, surfaced in iOS UI.

---

## Phase 6 — Food Photo → Macros (1 week)

**Goal**: Take a photo of food, get estimated macros.

### Tasks
- [ ] Endpoint: `POST /api/v1/nutrition/parse-photo` accepts image, returns structured nutrition_entries
- [ ] Use Claude vision API; system prompt designed for structured JSON output
- [ ] Validation: reject low-confidence outputs, prompt user to confirm/edit
- [ ] Eval: hand-labeled set of food photos with known macros, measure error
- [ ] iOS UI: camera → review screen → save to nutrition_entries

---

## Phase 7 — Diet Tracking + Reminders

Notification logic, goal-setting, integration with workouts (pre/post workout nutrition). Spec TBD once we know more about how the user actually wants this to work.

---

## Cross-cutting future work (not yet scheduled)

- Sharing workouts
- Multi-device sync conflict resolution
- Production deployment hardening (HTTPS, rate limiting, audit logging)
- Real user signups (terms, privacy, GDPR considerations)
