# `exercises` — sample rows

User-extensible reference table. `name` holds the movement name only; `equipment` is a separate dimension. Same movement with different equipment = separate rows. Hard delete with FK-restrict (see [ADR-002](../DECISIONS.md) and [`docs/SCHEMA.md`](../SCHEMA.md#exercises)).

## Columns

`id`, `name`, `slug`, `category`, `equipment`, `is_unilateral`, `exercise_type`, `default_rep_range_low`, `default_rep_range_high`, `description`, `form_cues`, `notes`, `created_by_user_id`

## Samples — built-in catalog

| id | name | slug | category | equipment | is_unilateral | exercise_type | reps | description (truncated) | form_cues (truncated) | created_by_user_id |
|---|---|---|---|---|---|---|---|---|---|---|
| `ex-skull-ez` | Skull Crusher | `skull_crusher_ez_bar` | isolation | barbell | false | weight_reps | 8–12 | Lying tricep extension with EZ bar. Biases the long head due to shoulder extension… | Elbows tucked and stationary; lower to forehead or behind the head… | NULL |
| `ex-skull-db` | Skull Crusher | `skull_crusher_dumbbell` | isolation | dumbbell | false | weight_reps | 8–12 | Same movement with dumbbells. Allows neutral grip and per-side load matching… | Same elbow position; lower DBs beside the head… | NULL |
| `ex-pushdown-cab` | Tricep Pushdown | `tricep_pushdown_cable` | isolation | cable | false | weight_reps | 10–15 | Cable pushdown biasing the lateral head; constant tension throughout the range… | Pin elbows to ribs; full extension without leaning… | NULL |
| `ex-row-bb` | Row | `row_barbell` | compound | barbell | false | weight_reps | 6–10 | Bent-over barbell row. Targets mid-back (lats, rhomboids, mid traps) and rear delts… | Hip hinge to ~45°; pull bar to lower ribs; control eccentric… | NULL |
| `ex-row-db` | Row | `row_dumbbell` | compound | dumbbell | false | weight_reps | 6–12 | Two-arm bent-over dumbbell row. Same target as barbell row… | Same hinge; allow slight elbow flare for upper-back bias… | NULL |
| `ex-row-db-1` | One-Arm Row | `one_arm_dumbbell_row` | compound | dumbbell | true | weight_reps | 8–12 | Single-arm dumbbell row from a bench. Unilateral; exposes left/right strength imbalance… | Brace opposite hand on bench; drive elbow back, not up… | NULL |
| `ex-bench` | Bench Press | `bench_press_barbell` | compound | barbell | false | weight_reps | 5–8 | Flat barbell bench. Sternal pec primary; anterior delt and triceps secondary… | Retract scapulae; bar to mid-chest; legs driving… | NULL |
| `ex-squat-hb` | Squat | `squat_barbell_high_bar` | compound | barbell | false | weight_reps | 5–8 | High-bar back squat. Knee-dominant; quad primary, glutes/hams secondary. Biases vastus lateralis at depth… | Brace; sit between hips; knees track toes… | NULL |
| `ex-fr-step` | Forward Step-Up | `forward_step_up_dumbbell` | compound | dumbbell | true | weight_reps | 8–12 | Unilateral leg work. Trains single-leg stability and exposes quad imbalances… | Full foot on box; drive through heel; no push-off from rear leg… | NULL |

## Samples — custom user exercise

| id | name | slug | category | equipment | is_unilateral | exercise_type | reps | description | form_cues | notes | created_by_user_id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ex-custom-1` | Banded Pull-Apart | `francescos_banded_pull_apart` | mobility | other | false | weight_reps | 15–25 | *(custom; user-created warm-up)* | Light band, slow tempo, scapular retraction focus | "Use red band — blue is too heavy for warmup" | `u-1` |

## Notes

- `name` is the movement only. `slug` carries the variant disambiguation (`skull_crusher_ez_bar` vs `skull_crusher_dumbbell`). Display layer composes `"{name} ({equipment_display})"` → "Skull Crusher (EZ Bar)".
- One-arm dumbbell row has a different `name` ("One-Arm Row") because it's a meaningfully different movement, not just a different implement.
- `description` covers what muscles and what biases; `form_cues` covers how to perform the lift. These get used together in Phase 4 coaching prompts.
- `notes` is for custom exercises — the user's personal annotation about *their* version. Built-ins leave it NULL.
- Deletion: built-ins are never deleted in normal operation. Custom exercises can be deleted only if no `workout_exercises` row references them. `ex-custom-1` is currently unreferenced, so deletion would succeed.
- Slug uniqueness is scoped: `(slug)` unique among built-ins, `(created_by_user_id, slug)` unique among customs — see [`docs/SCHEMA.md`](../SCHEMA.md#exercises) partial indexes.
