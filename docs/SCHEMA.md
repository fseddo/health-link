# Database Schema

The authoritative description of the data model. Update this whenever a migration changes schema.

For concrete sample rows per table (useful for visualization and auditing), see [`schema-samples/`](schema-samples/README.md). When this file changes, refresh the affected sample file in the same commit — stale samples are a `/dual-review` blocker.

## Design principles

1. **Canonical units internal, display units at the edge.** Store kg / meters / seconds / cm. Convert in API serializers per `users.weight_unit_preference`.
2. **Soft delete on user-generated parents.** Children filter via JOIN to parent's `deleted_at`.
3. **`source` column on every imported table** to distinguish HealthKit / manual / photo / mock / estimated data sources. The global enum is `'manual' | 'healthkit' | 'photo' | 'mock' | 'estimated'`; each table's CHECK constraint is a deliberately chosen subset (see the per-table notes below). When adding a new table, pick the subset that actually makes sense for that data — don't widen to the full enum by default.
4. **UUIDs for all primary keys.**
5. **Idempotent client-generated IDs** on sync-sensitive tables (`workouts.client_id`).
6. **Asymmetry signal lives in `soreness_reports`, `body_measurements`, and unilateral `sets`** — bilateral sets do not split left/right.

## Tables

### users
- `id` uuid PK
- `email` text UNIQUE NOT NULL
- `password_hash` text NOT NULL — bcrypt or argon2
- `created_at` timestamptz NOT NULL DEFAULT now()
- `birth_date` date — nullable
- `sex` text — check: `'male' | 'female' | 'other' | NULL`
- `height_cm` numeric(5,2) — nullable
- `weight_unit_preference` text NOT NULL DEFAULT `'lbs'` — check: `'lbs' | 'kg'`
- `deleted_at` timestamptz — nullable (soft delete)

### refresh_tokens
- `id` uuid PK
- `user_id` uuid FK→users ON DELETE CASCADE
- `token_hash` text UNIQUE NOT NULL — store hash, never raw token
- `expires_at` timestamptz NOT NULL
- `revoked_at` timestamptz — nullable
- `created_at` timestamptz NOT NULL DEFAULT now()
- `user_agent` text — nullable

Index: `(user_id) WHERE revoked_at IS NULL`

### muscle_groups (seeded reference table)
- `id` uuid PK
- `name` text UNIQUE NOT NULL — e.g. "Triceps", "Triceps — Long Head", "Quadriceps", "Vastus Lateralis"
- `region` text NOT NULL — `'upper' | 'lower' | 'core'`
- `is_bilateral` boolean NOT NULL
- `parent_muscle_group_id` uuid FK→muscle_groups — nullable. NULL = top-level group (e.g. "Triceps", "Quadriceps", "Deltoids"). Non-NULL = sub-head / sub-region of a parent group (e.g. "Triceps — Long Head" parents "Triceps"). Depth is intentionally limited to two levels (parent + child) — no grandchildren, no transitive walks needed.

**Hierarchy policy**: A muscle group is either a parent (no children's worth of bias matters yet) or it has children that represent biomechanically meaningful sub-divisions. Examples of parents with children: Triceps (long/lateral/medial), Quadriceps (rectus femoris, vastus lateralis, vastus medialis, vastus intermedius), Deltoids (anterior, lateral, posterior), Pectorals (clavicular, sternal), Latissimus Dorsi (upper, lower), Hamstrings (biceps femoris, semitendinosus, semimembranosus). Examples of parents without children (no useful sub-division for our purposes): Biceps Brachii, Trapezius (could split upper/mid/lower later), Glutes (could split maximus/medius/minimus later — deferred).

**Linking from `exercise_muscle_map`**: each exercise links to whichever level reflects its biomechanical bias. Skull crushers link to "Triceps — Long Head" (primary). Close-grip bench links to "Triceps" (parent, primary) because all three heads fire roughly equally. Aggregation queries that want total tricep volume sum over the parent and all its children — a recursive CTE or a denormalized lookup handles this cleanly.

**Linking from `soreness_reports`**: same policy — the user can report soreness at either level. "Left lateral tricep is sore" links to "Triceps — Long Head" with `side = 'left'`; "left tricep is sore" links to "Triceps".

### exercises
- `id` uuid PK
- `name` text NOT NULL — **movement name only**, no equipment in the string. Examples: "Skull Crusher", "Bench Press", "Row". The same movement with different equipment is a separate row (different `equipment`, different `slug`, same `name`).
- `slug` text NOT NULL — unique per scope (built-in or per-user). Encodes movement + equipment + any other disambiguator. Example slugs: `skull_crusher_ez_bar`, `skull_crusher_dumbbell`, `row_barbell`, `row_dumbbell`, `row_cable`.
- `category` text NOT NULL — `'compound' | 'isolation' | 'cardio' | 'mobility'`
- `equipment` text NOT NULL — `'barbell' | 'dumbbell' | 'machine' | 'bodyweight' | 'cable' | 'other'`. Separate dimension from `name`. The display layer (API serializer / UI) composes the user-facing label, typically `"{name} ({equipment_display})"` → e.g. "Skull Crusher (EZ Bar)".
- `is_unilateral` boolean NOT NULL DEFAULT false
- `exercise_type` text NOT NULL — `'weight_reps' | 'bodyweight_reps' | 'timed' | 'distance_timed' | 'distance_only'`
- `default_rep_range_low` int — nullable
- `default_rep_range_high` int — nullable
- `description` text — nullable; brief overview of *this specific variant*, the muscle groups worked, any head/region biases, and tips or accommodations. Aim for 2–3 sentences. Consumed by the Phase 4 coaching LLM as exercise context. Example for the `skull_crusher_ez_bar` row: "Lying tricep extension performed with an EZ bar. Biases the long head of the triceps because shoulder extension places it on stretch. Suitable as a primary isolation movement on push days."
- `form_cues` text — nullable; specific form / technique cues distinct from `description`. Example: "Keep elbows tucked and stationary; lower the bar to the forehead or behind the head for more long-head stretch; pause briefly at the bottom and drive back up by extending the elbows, not by pressing." Used in the UI (collapsible "how to" panel) and in coaching prompts when a user asks about form.
- `notes` text — nullable; freeform notes specific to a user's instance of a custom exercise. Built-in exercises should leave this NULL; canonical info lives in `description` / `form_cues`.
- `created_by_user_id` uuid FK→users — NULL means built-in

Partial unique indexes:
```sql
CREATE UNIQUE INDEX exercises_slug_builtin ON exercises (slug) WHERE created_by_user_id IS NULL;
CREATE UNIQUE INDEX exercises_slug_custom ON exercises (created_by_user_id, slug) WHERE created_by_user_id IS NOT NULL;
```

**Deletion**: `exercises` is user-extensible **reference data**, not journal data, so it uses **hard delete with FK-restrict** — not soft delete. This applies to both built-in and custom rows. The intent:

- Built-in exercises (`created_by_user_id IS NULL`) are seed data and effectively immutable. They are not deleted in normal operation; rename or replace via a new migration.
- Custom user exercises (`created_by_user_id IS NOT NULL`) can be deleted only if no `workout_exercises` row references them. Implemented via `workout_exercises.exercise_id` FK with `ON DELETE RESTRICT` — Postgres rejects the delete (the API maps this to 409 Conflict) when the exercise has been used. Once a custom exercise has any workout history attached, it is effectively immutable too; the user can edit `name`/`notes` but not delete. This protects workout history (a primary ML training signal) without denormalizing the exercise name into every set.

The soft-delete rule in ADR-002 covers journal/event data (`workouts`, `soreness_reports`, `body_measurements`, `nutrition_entries`) — rows that are records of things the user did. `exercises` is configuration referenced by journal rows, and follows the reference-table convention instead.

### exercise_muscle_map
- `exercise_id` uuid FK
- `muscle_group_id` uuid FK
- `involvement` text NOT NULL — `'primary' | 'secondary' | 'stabilizer'`
- PRIMARY KEY (exercise_id, muscle_group_id)

### routines
- `id` uuid PK
- `user_id` uuid FK NOT NULL ON DELETE CASCADE
- `name` text NOT NULL — e.g. "Push A". Not unique per user; the DB does not enforce uniqueness on routine names.
- `notes` text — nullable
- `created_at` timestamptz NOT NULL DEFAULT now()
- `updated_at` timestamptz NOT NULL DEFAULT now() — bumped on edits to the routine row or its child `routine_exercises`
- `deleted_at` timestamptz — nullable (soft delete; preserves `workouts.routine_id` links)

Index: `(user_id) WHERE deleted_at IS NULL`

**No target sets / reps / weight stored on routines.** Phase 2 progression ML owns weight and rep recommendations from the user's actual `sets` history per `(routine_id, exercise_id)`. For first-time exercises with no history, the UI falls back to `exercises.default_rep_range_low/high` and prompts the user for a working weight. See ADR-008.

**Deletion**: soft delete. A routine the user "deletes" is hidden from current-template lists but its row and its `routine_exercises` children remain. Historical `workouts.routine_id` references stay valid — progression ML can still answer "show me Push A history" even after the user deleted the template. To filter current routines, JOIN with `deleted_at IS NULL`.

### routine_exercises
- `id` uuid PK
- `routine_id` uuid FK ON DELETE CASCADE
- `exercise_id` uuid FK ON DELETE RESTRICT — same protection as `workout_exercises.exercise_id`. A custom exercise referenced by any routine cannot be deleted; the API returns 409.
- `order_index` int NOT NULL — 1-based, dense within a routine
- `superset_group` int — nullable; shared int across exercises within the same routine = grouped as superset (same semantics as `workout_exercises.superset_group`)
- `notes` text — nullable

Index: `(routine_id, order_index)`

**Shape mirrors `workout_exercises` deliberately.** When a user starts a workout from a routine, the API copies `(exercise_id, order_index, superset_group, notes)` into new `workout_exercises` rows under the new `workouts` row. The two tables are *not* the same table — edits to the workout instance must not mutate the template, and vice versa.

### workouts
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `routine_id` uuid FK→routines — nullable. Links the workout instance back to the template it was started from (if any). Ad-hoc workouts leave this NULL. Allows the progression ML to group sessions by routine without title string-matching. The FK does **not** cascade; `routines` uses soft delete, so a soft-deleted routine still satisfies the constraint and historical links remain intact.
- `title` text — nullable. Free-text snapshot, captured at workout creation and not auto-updated if the linked routine is later renamed.
- `started_at` timestamptz NOT NULL — domain timestamp: when the workout actually happened (may be backfilled by the user days later)
- `ended_at` timestamptz — nullable until finished
- `notes` text
- `client_id` text NOT NULL — for idempotent inserts from mobile
- `created_at` timestamptz NOT NULL DEFAULT now() — audit timestamp: when the row was inserted. Distinct from `started_at` for ML signals (e.g. "logged the workout 3 days late").
- `deleted_at` timestamptz — nullable
- UNIQUE (user_id, client_id)

Index: `(user_id, started_at DESC) WHERE deleted_at IS NULL`

### workout_exercises
- `id` uuid PK
- `workout_id` uuid FK ON DELETE CASCADE
- `exercise_id` uuid FK
- `order_index` int NOT NULL
- `superset_group` int — nullable; shared int across exercises = grouped as superset
- `notes` text

Index: `(workout_id, order_index)`

### sets
- `id` uuid PK
- `workout_exercise_id` uuid FK ON DELETE CASCADE
- `set_index` int NOT NULL — 1-based
- `set_type` text NOT NULL DEFAULT `'normal'` — check: `'normal' | 'warmup' | 'failure' | 'dropset'`
- `reps` int — nullable (for timed exercises)
- `weight_kg` numeric(7,2) — nullable (for bodyweight)
- `distance_m` numeric(10,2) — nullable
- `duration_seconds` int — nullable
- `rpe` numeric(3,1) — nullable, 1.0–10.0
- `side` text NOT NULL DEFAULT `'both'` — check: `'both' | 'left' | 'right'`
- `completed_at` timestamptz NOT NULL
- `notes` text

Index: `(workout_exercise_id, set_index)`

### soreness_reports
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `reported_at` timestamptz NOT NULL — domain timestamp: when the soreness was felt / measured
- `muscle_group_id` uuid FK NOT NULL
- `side` text NOT NULL — check: `'both' | 'left' | 'right'`
- `severity` int NOT NULL — check: 0–10
- `notes` text
- `created_at` timestamptz NOT NULL DEFAULT now() — audit timestamp
- `deleted_at` timestamptz — nullable

Indexes:
- `(user_id, reported_at DESC) WHERE deleted_at IS NULL`
- `(user_id, muscle_group_id, reported_at DESC) WHERE deleted_at IS NULL`

### health_snapshots
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `date` date NOT NULL
- `source` text NOT NULL — check: `'healthkit' | 'manual' | 'mock'`. Phase 1.5's synthetic generator writes `'mock'` here; iOS in Phase 3 writes `'healthkit'`. No `'photo'` or `'estimated'` — health data is either measured by a device or entered by the user.
- `resting_heart_rate` int — nullable
- `hrv_sdnn_ms` numeric(6,2) — nullable
- `sleep_hours` numeric(4,2) — nullable
- `sleep_quality_score` numeric(4,2) — nullable
- `wrist_temp_deviation_c` numeric(4,2) — nullable
- `body_weight_kg` numeric(6,2) — nullable
- `body_fat_percent` numeric(4,2) — nullable
- `training_load_category` text — nullable; `'well_below' | 'below' | 'steady' | 'above' | 'well_above'`
- `active_energy_kcal` int — nullable
- `created_at` timestamptz NOT NULL DEFAULT now()
- UNIQUE (user_id, date, source)

Index: `(user_id, date DESC)`

### workout_effort_ratings
- `id` uuid PK
- `workout_id` uuid FK UNIQUE ON DELETE CASCADE
- `effort_score` int NOT NULL — check: 1–10 (matches Apple's workoutEffortScore scale)
- `source` text NOT NULL — check: `'manual' | 'estimated' | 'healthkit'`. `'estimated'` is the only table where this value applies: future ML can infer an effort score from session volume / RPE / HRV when the user didn't enter one. No `'mock'` or `'photo'`.
- `rated_at` timestamptz NOT NULL

### body_measurements
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `measured_at` timestamptz NOT NULL — domain timestamp: when the measurement was taken
- `measurement_type` text NOT NULL — check constraint enum:
  `'waist' | 'chest' | 'hips' | 'neck' | 'bicep' | 'forearm' | 'thigh' | 'calf' | 'shoulders'`
- `side` text NOT NULL DEFAULT `'both'` — check: `'both' | 'left' | 'right'`
- `value_cm` numeric(6,2) NOT NULL
- `notes` text
- `source` text NOT NULL DEFAULT `'manual'` — check: `'manual' | 'healthkit'`. (HealthKit can report some circumferences via third-party scales / apps; no `'photo'`, `'mock'`, or `'estimated'` until a use case lands.)
- `created_at` timestamptz NOT NULL DEFAULT now() — audit timestamp
- `deleted_at` timestamptz — nullable

Index: `(user_id, measurement_type, measured_at DESC) WHERE deleted_at IS NULL`

### nutrition_entries
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `consumed_at` timestamptz NOT NULL — domain timestamp: when the food was eaten
- `meal_type` text — nullable; `'breakfast' | 'lunch' | 'dinner' | 'snack' | 'pre_workout' | 'post_workout'`
- `workout_id` uuid FK — nullable; link to workout for pre/post
- `food_name` text NOT NULL
- `calories` numeric(7,2) — nullable
- `protein_g` numeric(6,2) — nullable
- `carbs_g` numeric(6,2) — nullable
- `fat_g` numeric(6,2) — nullable
- `source` text NOT NULL — check: `'manual' | 'photo' | 'healthkit'`. No `'mock'` (Phase 1.5's synthetic generator only mocks `health_snapshots`) or `'estimated'` (nutrition is either logged or photographed, never inferred).
- `photo_url` text — nullable
- `confidence` numeric(3,2) — nullable, 0.00–1.00 (for AI-parsed entries)
- `created_at` timestamptz NOT NULL DEFAULT now() — audit timestamp
- `deleted_at` timestamptz — nullable

Index: `(user_id, consumed_at DESC) WHERE deleted_at IS NULL`

## Derived data (do not store)

These should always be computed at query time:
- Estimated 1RM (Epley formula)
- Total volume per workout / per muscle group
- Personal records
- Rep range hit ratios
- Recovery curves (until materialization is justified by performance)

## Intentionally deferred

- `user_goals` (cut/maintain/bulk, target weights/lifts)
- `foods` catalog normalization (USDA-style food database)
- Per-set tempo, rest time
- Workout sharing / multi-user features
- Materialized PR table
- **`exercise_families` (movement-pattern grouping)** — a future many-to-many table linking exercises that share a movement pattern (e.g. all rows, all chest flies, all squat variants). Variants are tracked as fully independent `exercises` rows today; the muscle map handles recovery/volume aggregation across them. Add this table when Phase 2 progression or Phase 4 coaching needs to reason about variants as a group (e.g. "show me my row strength across barbell / dumbbell / cable" or "did the user replace conventional deadlift with Romanian — count toward hinge volume"). Don't add it until that pressure is real.

## Conventions for code that touches the schema

- Always JOIN to `workouts.deleted_at IS NULL` when reading workout-child data.
- Always pass `source` explicitly when inserting health, nutrition, body, or effort data.
- Never accept user input in `lbs`/`miles` into the database without converting first.
- When deleting a workout, do NOT delete child sets/exercises — soft-delete the workout and let JOINs handle it.
