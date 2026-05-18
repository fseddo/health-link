# `body_measurements` — sample rows

Periodic anthropometric measurements: circumferences and similar, per side where applicable. User-generated journal data — soft-delete parent (ADR-002).

See [`docs/SCHEMA.md`](../SCHEMA.md#body_measurements) for the full column list.

## Columns

`id`, `user_id`, `measured_at`, `measurement_type`, `side`, `value_cm`, `notes`, `source`, `created_at`, `deleted_at`

`measurement_type` CHECK: `'waist' | 'chest' | 'hips' | 'neck' | 'bicep' | 'forearm' | 'thigh' | 'calf' | 'shoulders'`.
`side` CHECK: `'both' | 'left' | 'right'`, DEFAULT `'both'`.
`source` CHECK: `'manual' | 'healthkit'`.

Index `(user_id, measurement_type, measured_at DESC) WHERE deleted_at IS NULL`.

## Samples — April baseline

| id | user_id | measured_at | measurement_type | side | value_cm | source | created_at | deleted_at |
|---|---|---|---|---|---|---|---|---|
| `bm-1` | `u-1` | 2026-04-01T07:00:00Z | waist | both | 84.50 | manual | 2026-04-01T07:00:01Z | NULL |
| `bm-2` | `u-1` | 2026-04-01T07:05:00Z | bicep | left | 36.20 | manual | 2026-04-01T07:05:01Z | NULL |
| `bm-3` | `u-1` | 2026-04-01T07:05:00Z | bicep | right | 36.80 | manual | 2026-04-01T07:05:01Z | NULL |
| `bm-4` | `u-1` | 2026-04-01T07:08:00Z | chest | both | 102.00 | manual | 2026-04-01T07:08:01Z | NULL |
| `bm-5` | `u-1` | 2026-04-01T07:10:00Z | thigh | left | 58.50 | manual | 2026-04-01T07:10:01Z | NULL |
| `bm-6` | `u-1` | 2026-04-01T07:10:00Z | thigh | right | 58.30 | manual | 2026-04-01T07:10:01Z | NULL |

## Samples — May follow-up

| id | user_id | measured_at | measurement_type | side | value_cm | source | created_at | deleted_at |
|---|---|---|---|---|---|---|---|---|
| `bm-7` | `u-1` | 2026-05-01T07:00:00Z | waist | both | 83.80 | manual | 2026-05-01T07:00:01Z | NULL |
| `bm-8` | `u-1` | 2026-05-01T07:05:00Z | bicep | left | 36.50 | manual | 2026-05-01T07:05:01Z | NULL |
| `bm-9` | `u-1` | 2026-05-01T07:05:00Z | bicep | right | 37.00 | manual | 2026-05-01T07:05:01Z | NULL |
| `bm-10` | `u-1` | 2026-05-01T07:08:00Z | chest | both | 102.50 | manual | 2026-05-01T07:08:01Z | NULL |

## Notes

- **Per-side asymmetry signal**. The right bicep is ~6mm larger than the left at baseline AND growing slightly faster (+2mm right vs +3mm left over a month, but starting from a wider gap). Phase 5 asymmetry detection should flag this.
- **Bilateral measurements** (waist, chest, hips, neck, shoulders) use `side='both'`. Per-side measurements (bicep, forearm, thigh, calf) typically use `'left'` and `'right'`.
- **`source='healthkit'`** is in scope because some third-party scales and apps write circumference data into HealthKit. No `'photo'`, `'mock'`, or `'estimated'` until a real use case lands.
- **`value_cm` is canonical.** Display in inches happens at the API edge.
- **No `measurement_type='weight'`** — body weight lives in `health_snapshots.body_weight_kg` (daily roll-up). Don't duplicate.
- **`measured_at` is the domain timestamp** — when the tape measure was used. `created_at` is when the row was inserted (usually 1–5 seconds later for live entry).
