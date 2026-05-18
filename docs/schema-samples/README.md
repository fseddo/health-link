# Schema samples

One file per table. Each file shows a few realistic sample rows for visualization and auditing — to make the schema in `docs/SCHEMA.md` concrete before any migration is written.

**These are illustrative samples, not seed data.** Real seed data for `muscle_groups` and the starter exercise catalog is generated during Phase 1 Checkpoint 4. If a sample row contradicts an `docs/SCHEMA.md` rule, that's a bug — please fix.

## Conventions in these files

- UUIDs are shortened for readability: `u-1`, `mg-tri-long`, `ex-skull-ez`. Real values are full UUIDs.
- Times are ISO-8601 UTC.
- Units are canonical: kg (mass), cm (length), seconds (duration). Display conversion to lbs/inches happens in the API serializer, not in storage.
- Long text columns (`description`, `form_cues`, etc.) may be truncated with `…` for display.

## One coherent week of data

All files reference the same set of user IDs, workout IDs, and exercise IDs so the cross-table relationships make sense end-to-end. Primary actor is `u-1` (Francesco). Reference data and exercises are shared across users.

## Files

| Table | File |
|---|---|
| `users` | [users-schema.md](users-schema.md) |
| `refresh_tokens` | [refresh-tokens-schema.md](refresh-tokens-schema.md) |
| `muscle_groups` | [muscle-groups-schema.md](muscle-groups-schema.md) |
| `exercises` | [exercises-schema.md](exercises-schema.md) |
| `exercise_muscle_map` | [exercise-muscle-map-schema.md](exercise-muscle-map-schema.md) |
| `routines` | [routines-schema.md](routines-schema.md) |
| `routine_exercises` | [routine-exercises-schema.md](routine-exercises-schema.md) |
| `workouts` | [workouts-schema.md](workouts-schema.md) |
| `workout_exercises` | [workout-exercises-schema.md](workout-exercises-schema.md) |
| `sets` | [sets-schema.md](sets-schema.md) |
| `soreness_reports` | [soreness-reports-schema.md](soreness-reports-schema.md) |
| `health_snapshots` | [health-snapshots-schema.md](health-snapshots-schema.md) |
| `workout_effort_ratings` | [workout-effort-ratings-schema.md](workout-effort-ratings-schema.md) |
| `body_measurements` | [body-measurements-schema.md](body-measurements-schema.md) |
| `nutrition_entries` | [nutrition-entries-schema.md](nutrition-entries-schema.md) |

## When to update these files

When the schema changes in `docs/SCHEMA.md`, refresh the affected sample file(s) in the same commit. Stale samples are a `/dual-review` blocker on schema changes.
