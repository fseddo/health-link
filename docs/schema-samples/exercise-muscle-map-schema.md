# `exercise_muscle_map` — sample rows

Many-to-many between `exercises` and `muscle_groups`, with an `involvement` qualifier. Composite PK on `(exercise_id, muscle_group_id)`. An exercise links to whichever level of the muscle hierarchy reflects its bias — parent for compound work that hits all heads, child for an exercise that biases a specific head.

See [`docs/SCHEMA.md`](../SCHEMA.md#exercise_muscle_map) for the full column list and [muscle-groups-schema.md](muscle-groups-schema.md) for the hierarchy.

## Columns

`exercise_id`, `muscle_group_id`, `involvement`

## Samples — exercises that link to specific muscle heads

| exercise_id | muscle_group_id | involvement |
|---|---|---|
| `ex-skull-ez` | `mg-tri-long` | primary |
| `ex-skull-ez` | `mg-tri-lat` | secondary |
| `ex-skull-ez` | `mg-tri-med` | secondary |
| `ex-pushdown-cab` | `mg-tri-lat` | primary |
| `ex-pushdown-cab` | `mg-tri-med` | secondary |
| `ex-pushdown-cab` | `mg-tri-long` | secondary |
| `ex-squat-hb` | `mg-quad-vl` | primary |
| `ex-squat-hb` | `mg-quad-rf` | secondary |
| `ex-squat-hb` | `mg-quad-vm` | secondary |
| `ex-squat-hb` | `mg-glute` | secondary |
| `ex-squat-hb` | `mg-ham` | stabilizer |

## Samples — exercises that link to parent muscle groups

| exercise_id | muscle_group_id | involvement |
|---|---|---|
| `ex-bench` | `mg-pec-stern` | primary |
| `ex-bench` | `mg-pec-clav` | secondary |
| `ex-bench` | `mg-delt-ant` | secondary |
| `ex-bench` | `mg-tri` | secondary |
| `ex-fr-step` | `mg-quad` | primary |
| `ex-fr-step` | `mg-glute` | secondary |
| `ex-fr-step` | `mg-ham` | stabilizer |
| `ex-fr-step` | `mg-core` | stabilizer |

## Samples — back movements

| exercise_id | muscle_group_id | involvement |
|---|---|---|
| `ex-row-bb` | `mg-lat` | primary |
| `ex-row-bb` | `mg-rhom` | primary |
| `ex-row-bb` | `mg-trap` | secondary |
| `ex-row-bb` | `mg-delt-post` | secondary |
| `ex-row-bb` | `mg-bi` | secondary |
| `ex-row-bb` | `mg-erec` | stabilizer |
| `ex-row-db-1` | `mg-lat` | primary |
| `ex-row-db-1` | `mg-rhom` | primary |
| `ex-row-db-1` | `mg-delt-post` | secondary |
| `ex-row-db-1` | `mg-bi` | secondary |
| `ex-row-db-1` | `mg-core` | stabilizer |

## Notes

- **Heterogeneous map by design.** Skull crushers link to specific tricep heads (`mg-tri-long`, `mg-tri-lat`, `mg-tri-med`) because the bias matters. Bench press links to the **parent** `mg-tri` because all three heads fire roughly equally — splitting would be false precision.
- **Aggregation queries** need to walk the hierarchy. "Total tricep volume" = sum over sets where the linked muscle group is `mg-tri` OR any group whose `parent_muscle_group_id = mg-tri`. A recursive CTE handles this cleanly:
  ```sql
  WITH RECURSIVE tri AS (
    SELECT id FROM muscle_groups WHERE id = 'mg-tri'
    UNION ALL
    SELECT mg.id FROM muscle_groups mg JOIN tri ON mg.parent_muscle_group_id = tri.id
  )
  SELECT … FROM sets s
  JOIN workout_exercises we ON we.id = s.workout_exercise_id
  JOIN exercise_muscle_map emm ON emm.exercise_id = we.exercise_id
  WHERE emm.muscle_group_id IN (SELECT id FROM tri)
    AND emm.involvement IN ('primary', 'secondary');
  ```
- **`involvement` semantics**: `primary` = main mover, drives the load; `secondary` = meaningful contributor, included in volume calculations; `stabilizer` = involved but excluded from volume (e.g. core in a row).
- The map is built-in / read-only in Phase 1. Future phases may let users edit the map for custom exercises.
