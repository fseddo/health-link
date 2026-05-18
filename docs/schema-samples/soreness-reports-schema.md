# `soreness_reports` — sample rows

User-reported subjective soreness, per muscle group, per side. User-generated journal data — soft-delete parent (ADR-002). Can reference either parent or child muscle groups per the hierarchy policy.

See [`docs/SCHEMA.md`](../SCHEMA.md#soreness_reports) for the full column list.

## Columns

`id`, `user_id`, `reported_at`, `muscle_group_id`, `side`, `severity`, `notes`, `created_at`, `deleted_at`

Indexes:
- `(user_id, reported_at DESC) WHERE deleted_at IS NULL`
- `(user_id, muscle_group_id, reported_at DESC) WHERE deleted_at IS NULL`

## Samples

| id | user_id | reported_at | muscle_group_id | side | severity | notes | created_at | deleted_at |
|---|---|---|---|---|---|---|---|---|
| `sr-1` | `u-1` | 2026-05-13T08:00:00Z | `mg-tri-long` | both | 6 | "Long-head specifically" | 2026-05-13T08:00:00Z | NULL |
| `sr-2` | `u-1` | 2026-05-13T08:00:00Z | `mg-delt-ant` | both | 4 | NULL | 2026-05-13T08:00:00Z | NULL |
| `sr-3` | `u-1` | 2026-05-13T08:00:00Z | `mg-pec-stern` | both | 5 | NULL | 2026-05-13T08:00:00Z | NULL |
| `sr-4` | `u-1` | 2026-05-14T08:00:00Z | `mg-lat` | both | 5 | "From rows" | 2026-05-14T08:00:00Z | NULL |
| `sr-5` | `u-1` | 2026-05-14T08:00:00Z | `mg-rhom` | both | 4 | NULL | 2026-05-14T08:00:00Z | NULL |
| `sr-6` | `u-1` | 2026-05-14T08:00:00Z | `mg-bi` | right | 3 | "Slight imbalance with left" | 2026-05-14T08:00:00Z | NULL |
| `sr-7` | `u-1` | 2026-05-14T08:00:00Z | `mg-bi` | left | 5 | "Felt the one-arm row more on this side" | 2026-05-14T08:00:00Z | NULL |
| `sr-8` | `u-1` | 2026-05-16T08:00:00Z | `mg-quad-vl` | both | 7 | "Outer quad pumped after high-bar squat" | 2026-05-16T08:00:00Z | NULL |

## Notes

- **Hierarchy in action.** `sr-1` links to a *child* muscle (`mg-tri-long`) because the user could distinguish which tricep head was sore. `sr-4` links to the *parent* (`mg-lat`) — no useful split. Both are valid.
- **Per-side data** (`sr-6` and `sr-7`) is the asymmetry signal. The left bicep is reporting consistently higher soreness than the right — combined with the `sets` data from [sets-schema.md](sets-schema.md) (where the left side fatigued faster on one-arm rows) this is a strong asymmetry candidate for Phase 5.
- **`severity` is 0–10**, integer. 0 = no soreness; 10 = can't use the muscle. Most reports cluster 3–7.
- **`reported_at` is the domain timestamp** — when the soreness was felt. `created_at` is when the row was inserted. They'll usually match for live entry but diverge on backfill.
- **No `source` column** on this table — soreness is always user-reported. No mock generator writes here in Phase 1.5 (HealthKit doesn't have a soreness signal).
- **Aggregation across hierarchy**: "total tricep soreness today" sums severity for rows where `muscle_group_id` is `mg-tri` or any of its children — same recursive CTE pattern as the exercise muscle map. See [exercise-muscle-map-schema.md](exercise-muscle-map-schema.md).
