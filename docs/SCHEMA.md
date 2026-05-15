# Database Schema

The authoritative description of the data model. Update this whenever a migration changes schema.

## Design principles

1. **Canonical units internal, display units at the edge.** Store kg / meters / seconds / cm. Convert in API serializers per `users.weight_unit_preference`.
2. **Soft delete on user-generated parents.** Children filter via JOIN to parent's `deleted_at`.
3. **`source` column on every imported table** to distinguish HealthKit / manual / photo / mock / estimated data sources.
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
- `name` text UNIQUE NOT NULL — e.g. "Quadriceps", "Latissimus Dorsi"
- `region` text NOT NULL — `'upper' | 'lower' | 'core'`
- `is_bilateral` boolean NOT NULL

### exercises
- `id` uuid PK
- `name` text NOT NULL
- `slug` text NOT NULL — unique per scope (built-in or per-user)
- `category` text NOT NULL — `'compound' | 'isolation' | 'cardio' | 'mobility'`
- `equipment` text NOT NULL — `'barbell' | 'dumbbell' | 'machine' | 'bodyweight' | 'cable' | 'other'`
- `is_unilateral` boolean NOT NULL DEFAULT false
- `exercise_type` text NOT NULL — `'weight_reps' | 'bodyweight_reps' | 'timed' | 'distance_timed' | 'distance_only'`
- `default_rep_range_low` int — nullable
- `default_rep_range_high` int — nullable
- `notes` text
- `created_by_user_id` uuid FK→users — NULL means built-in

Partial unique indexes:
```sql
CREATE UNIQUE INDEX exercises_slug_builtin ON exercises (slug) WHERE created_by_user_id IS NULL;
CREATE UNIQUE INDEX exercises_slug_custom ON exercises (created_by_user_id, slug) WHERE created_by_user_id IS NOT NULL;
```

### exercise_muscle_map
- `exercise_id` uuid FK
- `muscle_group_id` uuid FK
- `involvement` text NOT NULL — `'primary' | 'secondary' | 'stabilizer'`
- PRIMARY KEY (exercise_id, muscle_group_id)

### workouts
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `title` text — nullable
- `started_at` timestamptz NOT NULL
- `ended_at` timestamptz — nullable until finished
- `notes` text
- `client_id` text NOT NULL — for idempotent inserts from mobile
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
- `reported_at` timestamptz NOT NULL
- `muscle_group_id` uuid FK NOT NULL
- `side` text NOT NULL — check: `'both' | 'left' | 'right'`
- `severity` int NOT NULL — check: 0–10
- `notes` text
- `deleted_at` timestamptz — nullable

Indexes:
- `(user_id, reported_at DESC) WHERE deleted_at IS NULL`
- `(user_id, muscle_group_id, reported_at DESC) WHERE deleted_at IS NULL`

### health_snapshots
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `date` date NOT NULL
- `source` text NOT NULL — `'healthkit' | 'manual' | 'mock'`
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
- `source` text NOT NULL — `'manual' | 'estimated' | 'healthkit'`
- `rated_at` timestamptz NOT NULL

### body_measurements
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `measured_at` timestamptz NOT NULL
- `measurement_type` text NOT NULL — check constraint enum:
  `'waist' | 'chest' | 'hips' | 'neck' | 'bicep' | 'forearm' | 'thigh' | 'calf' | 'shoulders'`
- `side` text NOT NULL DEFAULT `'both'` — check: `'both' | 'left' | 'right'`
- `value_cm` numeric(6,2) NOT NULL
- `notes` text
- `source` text NOT NULL DEFAULT `'manual'`
- `deleted_at` timestamptz — nullable

Index: `(user_id, measurement_type, measured_at DESC) WHERE deleted_at IS NULL`

### nutrition_entries
- `id` uuid PK
- `user_id` uuid FK NOT NULL
- `consumed_at` timestamptz NOT NULL
- `meal_type` text — nullable; `'breakfast' | 'lunch' | 'dinner' | 'snack' | 'pre_workout' | 'post_workout'`
- `workout_id` uuid FK — nullable; link to workout for pre/post
- `food_name` text NOT NULL
- `calories` numeric(7,2) — nullable
- `protein_g` numeric(6,2) — nullable
- `carbs_g` numeric(6,2) — nullable
- `fat_g` numeric(6,2) — nullable
- `source` text NOT NULL — `'manual' | 'photo' | 'healthkit'`
- `photo_url` text — nullable
- `confidence` numeric(3,2) — nullable, 0.00–1.00 (for AI-parsed entries)
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

- `routines` and `routine_exercises` (workout templates)
- `user_goals` (cut/maintain/bulk, target weights/lifts)
- `foods` catalog normalization (USDA-style food database)
- Per-set tempo, rest time
- Workout sharing / multi-user features
- Materialized PR table

## Conventions for code that touches the schema

- Always JOIN to `workouts.deleted_at IS NULL` when reading workout-child data.
- Always pass `source` explicitly when inserting health, nutrition, body, or effort data.
- Never accept user input in `lbs`/`miles` into the database without converting first.
- When deleting a workout, do NOT delete child sets/exercises — soft-delete the workout and let JOINs handle it.
