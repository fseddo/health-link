# `sets` — sample rows

The atomic record of a single set: reps × weight × RPE, optionally per-side for unilateral exercises. Cascades on `workout_exercises` delete. Weight stored in kg (canonical).

See [`docs/SCHEMA.md`](../SCHEMA.md#sets) for the full column list.

## Columns

`id`, `workout_exercise_id`, `set_index`, `set_type`, `reps`, `weight_kg`, `distance_m`, `duration_seconds`, `rpe`, `side`, `completed_at`, `notes`

Index `(workout_exercise_id, set_index)`.

## Samples — bench press (bilateral)

| id | workout_exercise_id | set_index | set_type | reps | weight_kg | rpe | side | completed_at |
|---|---|---|---|---|---|---|---|---|
| `s-1` | `we-1` | 1 | warmup | 8 | 40.00 | 5.0 | both | 2026-05-12T17:32:00Z |
| `s-2` | `we-1` | 2 | normal | 5 | 80.00 | 7.0 | both | 2026-05-12T17:38:00Z |
| `s-3` | `we-1` | 3 | normal | 5 | 80.00 | 7.5 | both | 2026-05-12T17:43:00Z |
| `s-4` | `we-1` | 4 | normal | 5 | 82.50 | 8.5 | both | 2026-05-12T17:49:00Z |

## Samples — superset (skullcrusher + pushdown)

| id | workout_exercise_id | set_index | set_type | reps | weight_kg | rpe | side | completed_at |
|---|---|---|---|---|---|---|---|---|
| `s-5` | `we-2` | 1 | normal | 10 | 25.00 | 7.0 | both | 2026-05-12T17:55:00Z |
| `s-6` | `we-3` | 1 | normal | 12 | 30.00 | 6.5 | both | 2026-05-12T17:57:00Z |
| `s-7` | `we-2` | 2 | normal | 10 | 25.00 | 7.5 | both | 2026-05-12T17:59:00Z |
| `s-8` | `we-3` | 2 | normal | 12 | 30.00 | 7.0 | both | 2026-05-12T18:01:00Z |
| `s-9` | `we-2` | 3 | normal | 9 | 25.00 | 8.5 | both | 2026-05-12T18:03:00Z |
| `s-10` | `we-3` | 3 | normal | 11 | 30.00 | 8.0 | both | 2026-05-12T18:05:00Z |

## Samples — one-arm row (unilateral, per-side rows)

| id | workout_exercise_id | set_index | set_type | reps | weight_kg | rpe | side | completed_at |
|---|---|---|---|---|---|---|---|---|
| `s-11` | `we-5` | 1 | normal | 10 | 24.00 | 7.5 | right | 2026-05-13T17:51:00Z |
| `s-12` | `we-5` | 2 | normal | 10 | 24.00 | 7.5 | right | 2026-05-13T17:53:00Z |
| `s-13` | `we-5` | 3 | normal | 10 | 24.00 | 8.0 | left | 2026-05-13T17:55:00Z |
| `s-14` | `we-5` | 4 | normal | 8 | 24.00 | 9.0 | left | 2026-05-13T17:58:00Z |

## Notes

- **Bilateral exercises stay `side='both'`.** Don't try to split a barbell bench set into per-side data — the load isn't decomposable.
- **Unilateral exercises** (where `exercises.is_unilateral=true`) write per-side rows. Same `set_index` for the left and right "set" is fine; what matters is the sequence the user did them in (typically right first, then left).
- **The asymmetry signal lives here.** In the one-arm row sample, the left side fatigued faster (`s-14` rep drop + RPE 9 vs RPE 7.5 on the right at the same weight). Phase 5 recovery/asymmetry detection mines this pattern.
- **`set_type='warmup'`** is included in volume aggregation only when explicitly asked. Most "working volume" queries should filter to `set_type IN ('normal', 'failure', 'dropset')`.
- **`weight_kg` is canonical.** When the user trains in lbs, the API serializer converts on display. Internal aggregations never see lbs.
- **Cardio exercises** (`exercise_type='distance_timed'`, etc.) use `distance_m` and `duration_seconds` and leave `weight_kg` / `reps` NULL. No cardio samples here because Phase 1 is strength-focused.
- **`rpe`** is 1.0–10.0 (numeric with one decimal). 6.5 means "4-ish reps in reserve." 9.0 means "1 rep in reserve."
