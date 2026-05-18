# `routines` — sample rows

User-defined workout templates. A routine is a named, ordered list of exercises (e.g. "Push A") that the user can start a workout from. Soft-delete parent — preserves the link from historical `workouts.routine_id` even after the user deletes the template.

Targets (sets, reps, weight) are deliberately **not** stored here. Phase 2 progression ML owns weight/rep recommendations from the user's actual history; the routine just specifies *which* exercises and *in what order*.

See [`docs/SCHEMA.md`](../SCHEMA.md#routines) for the full column list.

## Columns

`id`, `user_id`, `name`, `notes`, `created_at`, `updated_at`, `deleted_at`

Index `(user_id) WHERE deleted_at IS NULL`.

## Samples

| id | user_id | name | notes | created_at | updated_at | deleted_at |
|---|---|---|---|---|---|---|
| `r-push-a` | `u-1` | Push A | "Heavy chest + tricep day" | 2026-04-01T10:00:00Z | 2026-04-15T09:00:00Z | NULL |
| `r-pull-a` | `u-1` | Pull A | NULL | 2026-04-01T10:05:00Z | 2026-04-01T10:05:00Z | NULL |
| `r-legs-a` | `u-1` | Legs A | "Quad-focused" | 2026-04-01T10:10:00Z | 2026-04-01T10:10:00Z | NULL |
| `r-push-old` | `u-1` | Old Push | "Replaced by Push A" | 2026-02-10T12:00:00Z | 2026-02-10T12:00:00Z | 2026-04-01T10:00:00Z |

## Notes

- **`name` is not unique per user.** A user can have two "Push A" routines if they want, distinguished by `id`. The UI is expected to nudge against duplicates but the DB doesn't enforce it.
- **`updated_at`** distinct from `created_at` because routines are edited frequently (swap an exercise, reorder, rename). Updated on every change to the routine row or its child `routine_exercises`.
- **Soft-deleted `r-push-old`**: historical workouts (`workouts.routine_id = 'r-push-old'`) keep their link. Queries that list "user's current routines" filter `deleted_at IS NULL`; queries that trace a workout back to its template do not. Child `routine_exercises` rows still exist physically — filtered out via JOIN to `routines.deleted_at IS NULL` when reading current-template data.
- **No `client_id`**: routines are created on the device through normal CRUD, not synced from a journal stream. Idempotency lives on `workouts`, not here.
- **No targets stored here.** The progression ML (Phase 2) reads the user's prior `sets` for `(routine_id, exercise_id)` and recommends weight/reps. If a brand-new user has no history, the UI falls back to `exercises.default_rep_range_low/high` and prompts for a working weight.
