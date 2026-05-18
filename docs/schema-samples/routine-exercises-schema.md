# `routine_exercises` — sample rows

Join row between a routine and an exercise. Mirrors `workout_exercises` in shape: `order_index` controls display order, `superset_group` groups exercises performed back-to-back. Cascades on routine delete (the parent's soft-delete handles filtering for current-template reads).

No target sets / reps / weight columns — that information comes from the progression ML, not the template (see [`routines-schema.md`](routines-schema.md) notes).

See [`docs/SCHEMA.md`](../SCHEMA.md#routine_exercises) for the full column list.

## Columns

`id`, `routine_id`, `exercise_id`, `order_index`, `superset_group`, `notes`

Index `(routine_id, order_index)`.

## Samples — Push A, Pull A, Legs A

| id | routine_id | exercise_id | order_index | superset_group | notes |
|---|---|---|---|---|---|
| `re-1` | `r-push-a` | `ex-bench` | 1 | NULL | NULL |
| `re-2` | `r-push-a` | `ex-skull-ez` | 2 | 1 | NULL |
| `re-3` | `r-push-a` | `ex-pushdown-cab` | 3 | 1 | "Superset with skullcrushers" |
| `re-4` | `r-pull-a` | `ex-row-bb` | 1 | NULL | NULL |
| `re-5` | `r-pull-a` | `ex-row-db-1` | 2 | NULL | "Unilateral row for asymmetry signal" |
| `re-6` | `r-legs-a` | `ex-squat-hb` | 1 | NULL | NULL |
| `re-7` | `r-legs-a` | `ex-fr-step` | 2 | NULL | NULL |

## Notes

- **Shape mirrors `workout_exercises` on purpose.** When a user starts a workout from a routine, the API copies `(exercise_id, order_index, superset_group, notes)` from `routine_exercises` into new `workout_exercises` rows under the new workout. The two tables are intentionally interchangeable in shape so this copy is trivial. They are *not* the same table — the workout instance can be edited (added/removed/reordered exercises) without mutating the template.
- **`order_index`** is 1-based and dense within a routine. Reordering renumbers; this matches the `workout_exercises` convention.
- **Superset support**: `re-2` and `re-3` share `superset_group=1` inside `r-push-a`, so any workout started from Push A starts with those two grouped.
- **Custom exercises**: a routine can reference user-custom exercises (`exercises.created_by_user_id IS NOT NULL`). Because deleting a custom exercise is FK-RESTRICTED by any `workout_exercises` reference, a custom exercise *used in any past workout* cannot be deleted. Whether `routine_exercises` should also block deletion via RESTRICT is decided when the migration is written — current intent is yes, same protection.
- **No `source` column**: routines and their children are pure user configuration, never imported or synthesized.
