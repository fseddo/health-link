# `muscle_groups` — sample rows

Seeded reference table with **two-level hierarchy** via `parent_muscle_group_id`. Top-level groups have NULL parent; sub-heads / sub-regions reference their parent group. Hard delete (reference data); see [ADR-002](../DECISIONS.md).

See [`docs/SCHEMA.md`](../SCHEMA.md#muscle_groups-seeded-reference-table) for the full column list and hierarchy policy.

## Columns

`id`, `name`, `region`, `is_bilateral`, `parent_muscle_group_id`

## Samples — parents with children

| id | name | region | is_bilateral | parent_muscle_group_id |
|---|---|---|---|---|
| `mg-tri` | Triceps | upper | true | NULL |
| `mg-tri-long` | Triceps — Long Head | upper | true | `mg-tri` |
| `mg-tri-lat` | Triceps — Lateral Head | upper | true | `mg-tri` |
| `mg-tri-med` | Triceps — Medial Head | upper | true | `mg-tri` |
| `mg-quad` | Quadriceps | lower | true | NULL |
| `mg-quad-rf` | Rectus Femoris | lower | true | `mg-quad` |
| `mg-quad-vl` | Vastus Lateralis | lower | true | `mg-quad` |
| `mg-quad-vm` | Vastus Medialis | lower | true | `mg-quad` |
| `mg-quad-vi` | Vastus Intermedius | lower | true | `mg-quad` |
| `mg-delt` | Deltoids | upper | true | NULL |
| `mg-delt-ant` | Anterior Deltoid | upper | true | `mg-delt` |
| `mg-delt-lat` | Lateral Deltoid | upper | true | `mg-delt` |
| `mg-delt-post` | Posterior Deltoid | upper | true | `mg-delt` |
| `mg-pec` | Pectorals | upper | true | NULL |
| `mg-pec-clav` | Pectoralis — Clavicular Head | upper | true | `mg-pec` |
| `mg-pec-stern` | Pectoralis — Sternal Head | upper | true | `mg-pec` |
| `mg-lat` | Latissimus Dorsi | upper | true | NULL |
| `mg-ham` | Hamstrings | lower | true | NULL |
| `mg-ham-bf` | Biceps Femoris | lower | true | `mg-ham` |
| `mg-ham-st` | Semitendinosus | lower | true | `mg-ham` |
| `mg-ham-sm` | Semimembranosus | lower | true | `mg-ham` |

## Samples — parents without children (flat)

| id | name | region | is_bilateral | parent_muscle_group_id |
|---|---|---|---|---|
| `mg-bi` | Biceps Brachii | upper | true | NULL |
| `mg-trap` | Trapezius | upper | true | NULL |
| `mg-rhom` | Rhomboids | upper | true | NULL |
| `mg-glute` | Glutes | lower | true | NULL |
| `mg-calf` | Calves | lower | true | NULL |
| `mg-fore` | Forearms | upper | true | NULL |
| `mg-core` | Rectus Abdominis | core | false | NULL |
| `mg-obl` | Obliques | core | true | NULL |
| `mg-erec` | Erector Spinae | core | true | NULL |

## Notes

- Depth is intentionally limited to two levels — parent + child. No grandchildren.
- A muscle is either a parent **with** children (sub-heads worth distinguishing biomechanically) or **without** children (no useful split yet — may gain children in a future migration).
- `is_bilateral=false` only for genuinely midline muscles. Rectus abdominis is midline; obliques and erectors come in pairs.
- Trapezius could split into upper/mid/lower in a future migration if Phase 4 coaching needs it. Deferred.
- Glutes could split into max/medius/minimus likewise. Deferred.
- `exercise_muscle_map` and `soreness_reports` reference `muscle_groups.id` at whichever level is meaningful — see [exercise-muscle-map-schema.md](exercise-muscle-map-schema.md) for the policy.
