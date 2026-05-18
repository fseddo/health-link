# `health_snapshots` — sample rows

Daily roll-up of HealthKit (and Phase 1.5 mock) data. One row per `(user_id, date, source)` — UNIQUE constraint on that triple. Never store sub-daily HealthKit data here (locked decision in root `CLAUDE.md`).

See [`docs/SCHEMA.md`](../SCHEMA.md#health_snapshots) for the full column list.

## Columns

`id`, `user_id`, `date`, `source`, `resting_heart_rate`, `hrv_sdnn_ms`, `sleep_hours`, `sleep_quality_score`, `wrist_temp_deviation_c`, `body_weight_kg`, `body_fat_percent`, `training_load_category`, `active_energy_kcal`, `created_at`

`source` CHECK: `'healthkit' | 'manual' | 'mock'`.
UNIQUE `(user_id, date, source)`. Index `(user_id, date DESC)`.

## Samples — Phase 1.5 synthetic data (source='mock')

| id | user_id | date | source | rhr | hrv_sdnn | sleep_h | sleep_q | temp_dev_c | weight_kg | bf_% | training_load | active_kcal | created_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `hs-1` | `u-1` | 2026-05-10 | mock | 58 | 64.20 | 7.80 | 0.82 | -0.10 | 79.50 | 16.20 | steady | 2840 | 2026-05-15T12:00:00Z |
| `hs-2` | `u-1` | 2026-05-11 | mock | 56 | 71.40 | 8.10 | 0.88 | -0.20 | 79.40 | 16.20 | well_below | 2510 | 2026-05-15T12:00:00Z |
| `hs-3` | `u-1` | 2026-05-12 | mock | 62 | 58.90 | 7.20 | 0.74 | 0.10 | 79.45 | NULL | above | 3120 | 2026-05-15T12:00:00Z |
| `hs-4` | `u-1` | 2026-05-13 | mock | 66 | 52.30 | 6.50 | 0.61 | 0.30 | 79.50 | NULL | above | 3060 | 2026-05-15T12:00:00Z |
| `hs-5` | `u-1` | 2026-05-14 | mock | 60 | 60.10 | 7.40 | 0.78 | 0.10 | 79.55 | 16.30 | steady | 2740 | 2026-05-15T12:00:00Z |

## Samples — Phase 3 real HealthKit data (source='healthkit')

| id | user_id | date | source | rhr | hrv_sdnn | sleep_h | sleep_q | temp_dev_c | weight_kg | bf_% | training_load | active_kcal | created_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `hs-100` | `u-1` | 2026-09-01 | healthkit | 57 | 62.10 | 7.60 | 0.80 | 0.00 | 79.20 | NULL | steady | 2780 | 2026-09-01T08:15:00Z |
| `hs-101` | `u-1` | 2026-09-02 | healthkit | 55 | 68.40 | 8.00 | 0.85 | NULL | 79.30 | NULL | well_below | 2440 | 2026-09-02T08:12:00Z |

## Samples — partial data day (real HealthKit gaps happen)

| id | user_id | date | source | rhr | hrv_sdnn | sleep_h | sleep_q | temp_dev_c | weight_kg | bf_% | training_load | active_kcal | created_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `hs-102` | `u-1` | 2026-09-03 | healthkit | 58 | NULL | NULL | NULL | NULL | NULL | NULL | NULL | 1820 | 2026-09-03T22:00:00Z |

## Notes

- **`source='mock'` vs `'healthkit'`**: ML code MUST treat these identically. The `source` column is for data-quality decisions only (e.g. don't train on mock data when real is available for the same date).
- **UNIQUE `(user_id, date, source)`**: a user can have one mock row AND one healthkit row for the same date if both exist (e.g. during the Phase 3 cutover). ML code should prefer `healthkit` over `mock` when both exist.
- **Partial data is normal.** Row `hs-102` has only `rhr` and `active_energy_kcal` — the user took off their Apple Watch overnight, so no HRV, no sleep, no temperature data. The generator in Phase 1.5 should reproduce this realism.
- **Realistic correlations in the mock data**: training_load `above` on the 12th and 13th (`hs-3`, `hs-4`) → elevated resting HR (62→66) and suppressed HRV (58.9→52.3) the following morning. Poor sleep on the 13th (6.5h, quality 0.61) → continued elevated RHR. The generator's job is to make this look like real data.
- **`created_at` for mock rows is a single batch timestamp** (2026-05-15T12:00:00Z) because the seed script wrote them all at once.
- **No sub-daily granularity.** HealthKit raw data is sample-by-sample; we roll up to one row per day at sync time. Don't store individual heart rate readings here.
- **No "estimated" source.** Health data is either measured or entered, never inferred — that's why the CHECK constraint omits `'estimated'`.
