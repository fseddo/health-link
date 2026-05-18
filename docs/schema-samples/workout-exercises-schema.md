# `workout_exercises` — sample rows

Join row between a workout and an exercise. `order_index` controls display order; `superset_group` groups exercises performed back-to-back. Cascades on workout delete (the parent's soft-delete handles filtering).

See [`docs/SCHEMA.md`](../SCHEMA.md#workout_exercises) for the full column list.

## Columns

`id`, `workout_id`, `exercise_id`, `order_index`, `superset_group`, `notes`

Index `(workout_id, order_index)`.

## Samples — one push, one pull, one legs session

| id | workout_id | exercise_id | order_index | superset_group | notes |
|---|---|---|---|---|---|
| `we-1` | `w-1` | `ex-bench` | 1 | NULL | NULL |
| `we-2` | `w-1` | `ex-skull-ez` | 2 | 1 | NULL |
| `we-3` | `w-1` | `ex-pushdown-cab` | 3 | 1 | "Superset with skullcrushers" |
| `we-4` | `w-2` | `ex-row-bb` | 1 | NULL | NULL |
| `we-5` | `w-2` | `ex-row-db-1` | 2 | NULL | "Add unilateral row for asymmetry signal" |
| `we-6` | `w-3` | `ex-squat-hb` | 1 | NULL | NULL |
| `we-7` | `w-3` | `ex-fr-step` | 2 | NULL | NULL |

## Notes

- **Superset group**: `we-2` and `we-3` share `superset_group=1` inside workout `w-1`. Same int value across multiple rows in the same workout = grouped. NULL = not in a superset. The int is only meaningful within one workout — there's no separate `superset_groups` table.
- **Order**: `order_index` is 1-based and dense within a workout. Adding an exercise in the middle requires renumbering.
- **No `weight_unit` here.** Sets always store weight in kg; per-user display unit lives on `users`.
- The custom exercise `ex-custom-1` from [exercises-schema.md](exercises-schema.md) is currently unused — no row references it, which is why it can still be deleted.
