# Architectural Decisions

A running log of non-obvious choices and why they were made. Add an entry when you make a decision that future-you might want to revisit or question.

Format: short, dated, problem → decision → rationale → consequences.

---

## ADR-001: Kg internal, lbs display
**Date**: project start
**Problem**: User trains in lbs at a US gym; should the database store lbs or kg?
**Decision**: Store kg in the database. Convert to lbs in API serializers based on `users.weight_unit_preference`.
**Rationale**: HealthKit stores mass in kg natively, so the iOS port has no conversion at the storage layer. Plate math is a UI concern, not a data concern. International users + kg-plate gyms supported without migration.
**Consequences**: API serializers carry conversion logic. ML pipelines work in kg. Tests must verify conversion at the boundary.

---

## ADR-002: Soft delete on user-generated journal data
**Date**: project start
**Problem**: Hard delete loses data useful for ML training; soft delete on every table adds query complexity.
**Decision**: Soft delete applies to **user-generated journal/event data**: users, workouts, soreness_reports, nutrition_entries, body_measurements. These are records of things the user did. Children of these (workout_exercises, sets) filter via JOIN to parent's `deleted_at`. **Reference tables**, including the user-extensible `exercises` table and the seeded `muscle_groups` table, use **hard delete with FK-restrict** — not soft delete. See `docs/SCHEMA.md` `exercises` "Deletion" note for the rationale on user-customisable reference data.
**Rationale**: Single source of truth per logical entity. Cascades naturally. Avoids "I deleted this workout but kept the sets" weirdness. The journal-vs-reference split mirrors the natural shape of the data: events soft-delete (history is precious, may want to undo), configuration hard-deletes (with FK protection so referenced rows can't be orphaned).
**Consequences**: All workout-data queries must JOIN to `workouts.deleted_at IS NULL`. ORM relationships should be configured to enforce this. Custom exercises that have been used in any workout cannot be deleted; the API returns 409 when the FK constraint fires.

---

## ADR-003: Raw Anthropic SDK, no LangChain
**Date**: project start
**Problem**: LangChain offers abstractions for prompts, agents, retrieval.
**Decision**: Use the Anthropic SDK directly. Build retrieval, prompt templating, and orchestration from scratch.
**Rationale**: The project's purpose is learning applied AI engineering. Abstractions hide the mechanics. Direct SDK use teaches the actual surface area being abstracted.
**Consequences**: More code to write upfront. Better understanding of what's actually happening. Easier to debug prompt issues.

---

## ADR-004: Postgres with pgvector from day one (skipping SQLite)
**Date**: project start
**Problem**: SQLite is simpler for early phases; Postgres requires Docker.
**Decision**: Postgres 16 with pgvector extension from Phase 1.
**Rationale**: Phase 3 needs vector search. Migration mid-project is friction. Docker Compose makes Postgres setup trivial.
**Consequences**: Slight setup overhead. Worth it.

---

## ADR-005: Web frontend is throwaway
**Date**: project start
**Superseded in part by**: ADR-007 (iOS-timing portion — iOS port now lands at Phase 3, not "after Phase 4"). The "web frontend is throwaway" decision itself still stands.
**Problem**: Native iOS is the long-term target but Swift learning curve would block ML work.
**Decision**: Build minimal Vite + React + shadcn frontend purely for development. iOS app comes after Phase 4. *(Superseded: see ADR-007 — iOS now lands at Phase 3.)*
**Rationale**: Lets the developer focus all early energy on backend + ML. The web frontend exists to click through features during ML development. API designed for mobile consumption from day one.
**Consequences**: Web frontend gets no polish, no tests, no responsiveness work. Easy to delete later.

---

## ADR-006: `client_id` for workout idempotency
**Date**: project start
**Problem**: Mobile clients on flaky connections may retry POST /workouts, creating duplicates.
**Decision**: Client generates a UUID per workout, server enforces UNIQUE (user_id, client_id) and returns existing record on collision (or 409).
**Rationale**: Standard mobile-sync pattern. Costs nothing now, saves pain at iOS port time (Phase 3).
**Consequences**: Frontend / iOS clients must generate and persist a client_id before first sync.

---

## ADR-007: iOS port at Phase 3, with synthetic HealthKit data in Phase 1.5
**Date**: project start (revised plan)
**Supersedes**: ADR-005 (iOS-timing portion only — the "web frontend is throwaway" decision in ADR-005 still stands).
**Problem**: Original plan put iOS port at Phase 5, after recovery and coaching ML. But those ML features depend heavily on HealthKit data (HRV, sleep, training load). Building them without real health data means either weak models or extensive mocking late in the project. Conversely, going iOS-first risks burning weeks on Swift fundamentals before any ML work begins.
**Decision**: Two-part change:
  1. Add Phase 1.5: synthetic HealthKit data generator that loads `health_snapshots` with `source='mock'`. ML code treats mock and real HealthKit data identically.
  2. Move iOS port from Phase 5 to Phase 3, immediately after the first classical ML feature ships against mocked data. iOS replaces the mocked health data with real HealthKit before the deeper ML in Phases 4–5.
**Rationale**:
  - Developer wants to use the app personally as their daily fitness tracker; iOS is required for that.
  - Phases 4 and 5 (coaching + recovery) genuinely need health data context to be valuable; building them against mocked data and then iOS-porting would mean validating the models twice.
  - Synthetic data is a legitimate ML engineering artifact in its own right — generators are how real ML teams develop before real pipelines exist.
  - The `source` column on `health_snapshots` is exactly what enables mock and real data to coexist with no code changes downstream.
**Consequences**:
  - Phase 3 has a Swift learning curve baked in (~1 week of fundamentals before integration).
  - Phases 4 and 5 ship with iOS UI components, not just web. The web frontend remains for dev convenience but is no longer the primary client past Phase 3.
  - The `POST /api/v1/health-snapshots/batch` endpoint must be designed in Phase 1.5 with the iOS use case in mind (it'll be the same endpoint the iOS app calls).

---

## ADR-008: Add `routines` / `routine_exercises` in Phase 1, with no target columns
**Date**: 2026-05-15
**Problem**: The original schema deferred workout templates as cross-cutting future work. But the existing `workouts.title` field is free-text — two "Push A" sessions are linked only by string match, with no way to ask "show me my Push A progression" cleanly. Once any UI ships, users will expect to pick a saved routine rather than re-pick exercises every session. Adding routines later means a schema migration plus a backfill that has to *guess* which historical workouts belong to which routine from titles alone.
**Decision**: Promote `routines` and `routine_exercises` from "deferred" into Phase 1, alongside the rest of the core schema. `workouts` gains a nullable `routine_id` FK so an instance can trace back to the template it was started from. Crucially, `routine_exercises` stores **no** target sets/reps/weight — Phase 2 progression ML owns those recommendations from real history.
**Rationale**:
  - Adding it now is one migration, cheap. Adding it later requires a heuristic backfill from `workouts.title` that will be wrong.
  - Soft delete on `routines` preserves the link from historical workouts even after the user "deletes" a template — matches the ADR-002 pattern for user-generated data that other rows depend on.
  - Omitting target columns avoids two systems of truth (the template's "you should do 8 reps at 60kg" vs. the ML's "based on last week, try 62.5kg"). The ML wins by definition once any history exists; the template would just be dead schema. For brand-new exercises with no history, the UI falls back to `exercises.default_rep_range_low/high` and prompts the user.
  - The shape of `routine_exercises` mirrors `workout_exercises` deliberately so "start workout from routine" is a trivial column-by-column copy.
**Consequences**:
  - `workouts.routine_id` is nullable — ad-hoc workouts stay first-class.
  - Soft-delete semantics now apply to `routines`; queries listing current templates must filter `deleted_at IS NULL`, but queries tracing a historical workout to its template do not.
  - `routine_exercises.exercise_id` uses ON DELETE RESTRICT — a custom exercise referenced by any routine cannot be deleted (matches the protection on `workout_exercises.exercise_id` from ADR-002).
  - If a routine is renamed, historical `workouts.title` snapshots do **not** auto-update. Title is a frozen-at-creation field.

---

## Add new ADRs below this line.
