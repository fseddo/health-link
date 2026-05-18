# `nutrition_entries` — sample rows

Food log: macros per consumed item or meal. User-generated journal data — soft-delete parent (ADR-002). Source can be manual, photo (Phase 6 vision LLM), or HealthKit. Optional link to a workout for pre/post-workout nutrition.

See [`docs/SCHEMA.md`](../SCHEMA.md#nutrition_entries) for the full column list.

## Columns

`id`, `user_id`, `consumed_at`, `meal_type`, `workout_id`, `food_name`, `calories`, `protein_g`, `carbs_g`, `fat_g`, `source`, `photo_url`, `confidence`, `created_at`, `deleted_at`

`meal_type` CHECK: `'breakfast' | 'lunch' | 'dinner' | 'snack' | 'pre_workout' | 'post_workout'`.
`source` CHECK: `'manual' | 'photo' | 'healthkit'`.

Index `(user_id, consumed_at DESC) WHERE deleted_at IS NULL`.

## Samples — manual entry (Phase 1)

| id | user_id | consumed_at | meal_type | workout_id | food_name | cal | prot_g | carb_g | fat_g | source | photo_url | confidence | created_at | deleted_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ne-1` | `u-1` | 2026-05-12T19:30:00Z | post_workout | `w-1` | "Chicken + rice bowl" | 720 | 52.0 | 90.0 | 14.0 | manual | NULL | NULL | 2026-05-12T19:31:00Z | NULL |
| `ne-2` | `u-1` | 2026-05-13T07:30:00Z | breakfast | NULL | "Oatmeal with whey" | 480 | 38.0 | 65.0 | 8.0 | manual | NULL | NULL | 2026-05-13T07:31:00Z | NULL |

## Samples — photo-parsed (Phase 6)

| id | user_id | consumed_at | meal_type | workout_id | food_name | cal | prot_g | carb_g | fat_g | source | photo_url | confidence | created_at | deleted_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ne-3` | `u-1` | 2026-05-13T13:00:00Z | lunch | NULL | "Turkey sandwich, chips" | 640 | 32.0 | 70.0 | 22.0 | photo | `s3://hl-photos/u-1/abc.jpg` | 0.78 | 2026-05-13T13:05:00Z | NULL |
| `ne-4` | `u-1` | 2026-05-13T20:00:00Z | dinner | NULL | "Pasta with meat sauce" | 880 | 38.0 | 110.0 | 28.0 | photo | `s3://hl-photos/u-1/def.jpg` | 0.65 | 2026-05-13T20:02:00Z | NULL |

## Samples — HealthKit (rare, third-party app writes)

| id | user_id | consumed_at | meal_type | workout_id | food_name | cal | prot_g | carb_g | fat_g | source | photo_url | confidence | created_at | deleted_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ne-5` | `u-1` | 2026-09-15T12:30:00Z | lunch | NULL | "MyFitnessPal — Salad bowl" | 410 | 28.0 | 30.0 | 18.0 | healthkit | NULL | NULL | 2026-09-15T12:35:00Z | NULL |

## Notes

- **`workout_id` is nullable** — most meals aren't tied to a workout. Use the link only for `pre_workout` / `post_workout` meal types.
- **`confidence` populated only when `source='photo'`.** Manual and HealthKit entries leave it NULL. Phase 6 will define a threshold below which the user is prompted to review/correct (probably ~0.70).
- **`photo_url` is opaque** — could be S3, could be local-filesystem path during dev. Validation only that it's set when `source='photo'`.
- **No `'mock'` source.** Phase 1.5's synthetic generator only mocks `health_snapshots`, not nutrition. Mock nutrition isn't on the roadmap.
- **No `'estimated'` source.** Nutrition is either logged by the user, photographed, or imported — never inferred from other signals.
- **Macros are nullable individually**. Some sources (HealthKit imports from another app) may have only calories, not protein/carbs/fat. ML code should handle this gracefully.
- **`consumed_at` is the domain timestamp** — when the food was eaten. `created_at` is when the row was inserted. They diverge if the user logs a meal hours later.
