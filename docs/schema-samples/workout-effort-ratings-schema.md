# `workout_effort_ratings` — sample rows

One effort score per workout. UNIQUE on `workout_id` — a workout has at most one rating. Cascades on workout delete.

See [`docs/SCHEMA.md`](../SCHEMA.md#workout_effort_ratings) for the full column list.

## Columns

`id`, `workout_id`, `effort_score`, `source`, `rated_at`

`effort_score` CHECK: 1–10 (matches Apple's `workoutEffortScore` scale).
`source` CHECK: `'manual' | 'estimated' | 'healthkit'`.
UNIQUE `(workout_id)`.

## Samples

| id | workout_id | effort_score | source | rated_at |
|---|---|---|---|---|
| `wer-1` | `w-1` | 7 | manual | 2026-05-12T18:43:00Z |
| `wer-2` | `w-2` | 6 | estimated | 2026-05-13T18:36:00Z |
| `wer-3` | `w-4` | 4 | manual | 2026-05-15T11:02:00Z |
| `wer-4` | `w-100` *(future iOS workout)* | 8 | healthkit | 2026-09-15T18:30:00Z |

## Notes

- **`source='estimated'`** is unique to this table — see [`docs/SCHEMA.md`](../SCHEMA.md#workout_effort_ratings). Future ML can derive an effort score from volume + RPE + HRV when the user didn't enter one (workout `w-2` shows this case).
- **`source='manual'`** is the user entering the score themselves after the session. Workout `w-1` shows this.
- **`source='healthkit'`** is the iOS app reading Apple's `workoutEffortScore` from HealthKit (Phase 3+). Apple's scale is 1–10, same as ours by design.
- **UNIQUE on `workout_id`** means re-rating a workout updates (upserts) rather than inserts a duplicate. The API should handle this as a PUT or PATCH, not POST.
- **`rated_at`** is when the rating was given — for `manual` this is when the user tapped it, for `estimated` this is when the ML inference ran, for `healthkit` this is when iOS synced.
- **Workout `w-3` in [workouts-schema.md](workouts-schema.md) is missing here** — it's still in progress (`ended_at` NULL), so no rating yet.
- **Workout `w-5`** (soft-deleted in [workouts-schema.md](workouts-schema.md)) — its `workout_effort_ratings` row, if any, was cascade-deleted because `workout_id` has `ON DELETE CASCADE`. The soft-delete on the parent doesn't delete this row; only a hard parent-delete would. In practice, soft-deleted workouts retain their ratings.
