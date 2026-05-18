"""
Exercise -> muscle involvement map (ADR-011).

For each exercise: which muscles does it train, and is each a prime mover, an
assisting synergist, or an isometric stabiliser? Via `ROLE_SET_CREDIT` that
role becomes a fractional training-volume credit (primary 1.0 / secondary 0.5 /
stabiliser 0.0) — Pelland 2026's direct/indirect counting.

----------------------------------------------------------------------------
WHAT THIS IS, AND WHAT IT IS NOT
----------------------------------------------------------------------------

This is the layer's CROSS-muscle volume-accounting map. It answers "one set of
a barbell row — how much volume does it credit to the lats, the biceps, the
rear delt?" It does NOT rank exercises within a muscle and does NOT say which
sub-region an exercise biases — that is the WITHIN-muscle emphasis layer
(`ExerciseEmphasis` measured, `MechanisticEmphasis` derived). "Overhead work
favours the triceps long head", "dips bias the lower chest" are emphasis
claims and live there, not here. See ADR-011 for the three-layer model.

It is NOT a measured per-exercise growth result. `role` is uncontested anatomy
(origin/insertion, line of pull, which joint action the resistance loads); the
1.0/0.5/0.0 weights are Pelland 2026's fractional-counting heuristic. That is
the whole of the claim — no effect magnitudes are derived here.

----------------------------------------------------------------------------
BOTH OUTCOMES
----------------------------------------------------------------------------

Every row carries `outcomes=("hypertrophy", "strength")`. The role is anatomy:
a prime mover is a prime mover whatever the training goal. Pelland 2026 applied
the same direct/indirect fractional counting to both its hypertrophy and its
strength volume regressions, so the 0.5 weight is grounded for both. The
`outcomes` field is the seam left open for the one case where outcome could
matter — Pelland publishes a SEPARATE strength exercise classification
(Table 2) that is not yet retrieved/encoded; if it ever shows a genuine
strength-specific reclassification, that becomes a row with
`outcomes=("strength",)`. Until then the map is honestly outcome-shared.

----------------------------------------------------------------------------
DELTOID TAXONOMY NOTE
----------------------------------------------------------------------------

The three deltoid heads are encoded as separate muscle keys —
`anterior_deltoid` / `lateral_deltoid` / `posterior_deltoid` — as Pelland's
table does. Involvement MUST be per-head: a bench press loads the anterior head
and not the posterior one. This differs from the mechanistic tier's
`deltoids` + `region` convention (`mechanistic/deltoids.py`). Unifying the
sub-muscle taxonomy across the layer is deferred (BACKLOG.md).

----------------------------------------------------------------------------
PROTOTYPE SCOPE (ADR-011 first implementation)
----------------------------------------------------------------------------

The 16 exercises in `mechanistic/lats.py` and `mechanistic/deltoids.py`, each
scored across every muscle it meaningfully trains. Grip/forearm involvement is
deliberately out of scope for the prototype. A full exercise-library catalogue
is future work.
"""

from __future__ import annotations

from .shared import ExerciseInvolvement


# `basis` values — how a row's role was determined.
BIOMECHANICAL = "biomechanical"        # derived from anatomy / line of pull
PELLAND_T1 = "pelland_2026_table1"     # the (exercise, muscle) pair is an exact
                                       # match in Pelland 2026 Table 1, which
                                       # corroborates the biomechanical call


# ============================================================================
# Lats-module exercises (mechanistic/lats.py) — 7 exercises
# ============================================================================

# --- The pullover family: shoulder extension from a deep overhead position ---

_DUMBBELL_PULLOVER: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="dumbbell_pullover", muscle="latissimus_dorsi",
        role="primary", basis=BIOMECHANICAL,
        rationale="The resisted action — the arm arcing from overhead back "
                  "toward the torso — is shoulder extension/adduction, the "
                  "latissimus dorsi's prime action.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_pullover", muscle="teres_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The teres major shares the lat's line of pull on shoulder "
                  "extension/adduction ('the lat's little helper') — a "
                  "synergist on every rep, not the prime mover.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_pullover", muscle="pectoralis_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The sternocostal fibres extend a flexed humerus. "
                  "`role=secondary` is the involvement taxonomy — the lat is "
                  "the prime mover of the resisted shoulder-extension action — "
                  "NOT a magnitude claim: dumbbell-pullover EMG often shows "
                  "the pec as the dominant agonist. The pullover genuinely "
                  "splits load between back and chest.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_pullover", muscle="triceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The long head crosses the shoulder and assists shoulder "
                  "extension; with the near-straight arm of a pullover it "
                  "co-contributes as a synergist.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_pullover", muscle="posterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A shoulder extensor — assists drawing the humerus down out "
                  "of the overhead position.",
    ),
]

_CABLE_PULLOVER: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="cable_pullover", muscle="latissimus_dorsi",
        role="primary", basis=BIOMECHANICAL,
        rationale="Shoulder extension against the cable — the latissimus "
                  "dorsi's prime action — is the resisted movement.",
    ),
    ExerciseInvolvement(
        exercise="cable_pullover", muscle="teres_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Shares the lat's shoulder-extension line of pull; a "
                  "synergist on every rep.",
    ),
    ExerciseInvolvement(
        exercise="cable_pullover", muscle="pectoralis_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The sternocostal fibres extend a flexed humerus. "
                  "`role=secondary` reflects the prime-mover taxonomy (the lat "
                  "leads the resisted shoulder extension), not relative "
                  "magnitude — pullover EMG can show a large pec contribution. "
                  "A cable line of pull can be set to bias the lat somewhat "
                  "more than a dumbbell.",
    ),
    ExerciseInvolvement(
        exercise="cable_pullover", muscle="triceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The long head assists shoulder extension with the "
                  "near-straight arm; a synergist.",
    ),
    ExerciseInvolvement(
        exercise="cable_pullover", muscle="posterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A shoulder extensor; assists pulling the humerus down from "
                  "overhead.",
    ),
]

_STRAIGHT_ARM_PULLDOWN: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="straight_arm_pulldown", muscle="latissimus_dorsi",
        role="primary", basis=BIOMECHANICAL,
        rationale="A straight-arm shoulder-extension movement — the lat's "
                  "prime action — driven directly against the cable.",
    ),
    ExerciseInvolvement(
        exercise="straight_arm_pulldown", muscle="teres_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Shares the lat's shoulder-extension line of pull; a "
                  "synergist.",
    ),
    ExerciseInvolvement(
        exercise="straight_arm_pulldown", muscle="triceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The long head assists shoulder extension; loaded across "
                  "the straight-arm range as a synergist.",
    ),
    ExerciseInvolvement(
        exercise="straight_arm_pulldown", muscle="posterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A shoulder extensor — assists the downward arc of the "
                  "humerus.",
    ),
    ExerciseInvolvement(
        exercise="straight_arm_pulldown", muscle="pectoralis_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The sternocostal fibres assist shoulder extension over the "
                  "early part of the range; a minor secondary contributor.",
    ),
]

# --- Vertical pulls ---

_PULL_UP: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="pull_up", muscle="latissimus_dorsi",
        role="primary", basis=BIOMECHANICAL,
        rationale="A vertical pull: lat-driven shoulder extension/adduction "
                  "is the prime action raising the body to the bar.",
    ),
    ExerciseInvolvement(
        exercise="pull_up", muscle="teres_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Shares the lat's shoulder-extension/adduction line of "
                  "pull; a synergist of the pull.",
    ),
    ExerciseInvolvement(
        exercise="pull_up", muscle="biceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Elbow flexion under load — a synergist of every pull; "
                  "Pelland-style indirect arm work.",
    ),
    ExerciseInvolvement(
        exercise="pull_up", muscle="brachialis",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A prime elbow flexor regardless of grip; loaded on the "
                  "elbow-flexion component of the pull.",
    ),
    ExerciseInvolvement(
        exercise="pull_up", muscle="posterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists shoulder extension/adduction through the pull; a "
                  "synergist.",
    ),
    ExerciseInvolvement(
        exercise="pull_up", muscle="trapezius",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The lower and middle traps drive scapular depression and "
                  "downward rotation as the body rises — a synergist of the "
                  "vertical pull.",
    ),
    ExerciseInvolvement(
        exercise="pull_up", muscle="rhomboids",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assist scapular retraction and downward rotation through "
                  "the pull; a synergist.",
    ),
]

_LAT_PULLDOWN: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="lat_pulldown", muscle="latissimus_dorsi",
        role="primary", basis=BIOMECHANICAL,
        rationale="A vertical pull: lat-driven shoulder extension/adduction "
                  "is the prime action.",
    ),
    ExerciseInvolvement(
        exercise="lat_pulldown", muscle="teres_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Shares the lat's shoulder-extension/adduction line of "
                  "pull; a synergist.",
    ),
    ExerciseInvolvement(
        exercise="lat_pulldown", muscle="biceps_brachii",
        role="secondary", basis=PELLAND_T1,
        rationale="Elbow flexion under load. Pelland 2026 Table 1 lists "
                  "`lat_pulldown` as indirect work for the biceps brachii — "
                  "corroborating this secondary call.",
    ),
    ExerciseInvolvement(
        exercise="lat_pulldown", muscle="brachialis",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A prime elbow flexor regardless of grip; loaded on the "
                  "elbow-flexion component of the pull.",
    ),
    ExerciseInvolvement(
        exercise="lat_pulldown", muscle="posterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists shoulder extension/adduction through the pull; a "
                  "synergist.",
    ),
    ExerciseInvolvement(
        exercise="lat_pulldown", muscle="trapezius",
        role="secondary", basis=PELLAND_T1,
        rationale="The lower and middle traps drive scapular depression and "
                  "downward rotation. Pelland 2026 Table 1 lists "
                  "`lat_pulldown` as indirect work for the trapezius — "
                  "corroborating this secondary call.",
    ),
    ExerciseInvolvement(
        exercise="lat_pulldown", muscle="rhomboids",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assist scapular retraction and downward rotation through "
                  "the pull; a synergist.",
    ),
]

# --- Horizontal pulls (rows) ---
# A row has TWO prime actions — shoulder extension (lat-driven) AND scapular
# retraction (trapezius/rhomboid-driven) — so it carries multiple primaries.

_SEATED_CABLE_ROW: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="latissimus_dorsi",
        role="primary", basis=BIOMECHANICAL,
        rationale="Horizontal pull: lat-driven shoulder extension drawing the "
                  "elbow back is a prime action of the row.",
    ),
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="trapezius",
        role="primary", basis=BIOMECHANICAL,
        rationale="The middle traps drive scapular retraction — a prime "
                  "action of the row, not an assist.",
    ),
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="rhomboids",
        role="primary", basis=BIOMECHANICAL,
        rationale="Scapular retraction/adduction — a prime action of the row, "
                  "alongside the middle traps.",
    ),
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="posterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists horizontal shoulder extension as the elbow travels "
                  "back. Primary-vs-secondary here is a genuine judgement call "
                  "(ADR-011 flags it); encoded secondary because the row's "
                  "dominant resisted actions — shoulder extension and scapular "
                  "retraction — are led by the lats and the mid-back.",
    ),
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="teres_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists shoulder extension, sharing the lat's line of pull "
                  "as the elbow draws back — it contributes to the row's "
                  "pulling component only, not its scapular-retraction "
                  "component.",
    ),
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="biceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Elbow flexion under load — the row's classic indirect arm "
                  "work.",
    ),
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="brachialis",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A prime elbow flexor regardless of grip; loaded on the "
                  "elbow-flexion component of the row.",
    ),
    ExerciseInvolvement(
        exercise="seated_cable_row", muscle="erector_spinae",
        role="stabilizer", basis=BIOMECHANICAL,
        rationale="Holds the trunk position isometrically against the load; "
                  "braced, not dynamically trained — zero hypertrophy credit.",
    ),
]

_BARBELL_ROW: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="barbell_row", muscle="latissimus_dorsi",
        role="primary", basis=BIOMECHANICAL,
        rationale="Horizontal pull: lat-driven shoulder extension drawing the "
                  "elbow back is a prime action of the row.",
    ),
    ExerciseInvolvement(
        exercise="barbell_row", muscle="trapezius",
        role="primary", basis=BIOMECHANICAL,
        rationale="The middle traps drive scapular retraction — a prime "
                  "action of the row.",
    ),
    ExerciseInvolvement(
        exercise="barbell_row", muscle="rhomboids",
        role="primary", basis=BIOMECHANICAL,
        rationale="Scapular retraction/adduction — a prime action of the row, "
                  "alongside the middle traps.",
    ),
    ExerciseInvolvement(
        exercise="barbell_row", muscle="posterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists horizontal shoulder extension as the elbow travels "
                  "back. Primary-vs-secondary here is a genuine judgement call "
                  "(ADR-011 flags it); encoded secondary because the row's "
                  "dominant resisted actions — shoulder extension and scapular "
                  "retraction — are led by the lats and the mid-back.",
    ),
    ExerciseInvolvement(
        exercise="barbell_row", muscle="teres_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists shoulder extension, sharing the lat's line of pull "
                  "as the elbow draws back — it contributes to the row's "
                  "pulling component only, not its scapular-retraction "
                  "component.",
    ),
    ExerciseInvolvement(
        exercise="barbell_row", muscle="biceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Elbow flexion under load — the row's classic indirect arm "
                  "work.",
    ),
    ExerciseInvolvement(
        exercise="barbell_row", muscle="brachialis",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A prime elbow flexor regardless of grip; loaded on the "
                  "elbow-flexion component of the row.",
    ),
    ExerciseInvolvement(
        exercise="barbell_row", muscle="erector_spinae",
        role="stabilizer", basis=BIOMECHANICAL,
        rationale="Works hard isometrically to hold the bent-over torso "
                  "against the load — but the work is isometric stabilisation, "
                  "so no dynamic hypertrophy volume is credited.",
    ),
]


# ============================================================================
# Deltoid-module exercises (mechanistic/deltoids.py) — 9 exercises
# ============================================================================

# --- Anterior-deltoid exercises ---

_INCLINE_BENCH_PRESS: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="incline_bench_press", muscle="pectoralis_major",
        role="primary", basis=BIOMECHANICAL,
        rationale="A press: pec-driven horizontal shoulder flexion/adduction "
                  "is the prime action; the incline biases the clavicular "
                  "fibres but the whole pec is a prime mover.",
    ),
    ExerciseInvolvement(
        exercise="incline_bench_press", muscle="anterior_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Shoulder flexion is a prime action of the press; the "
                  "incline angle makes the anterior deltoid a co-prime mover, "
                  "not merely an assistant.",
    ),
    ExerciseInvolvement(
        exercise="incline_bench_press", muscle="triceps_brachii",
        role="secondary", basis=PELLAND_T1,
        rationale="Elbow extension through the lockout. Pelland 2026 Table 1 "
                  "lists `incline_bench_press` as indirect work for the "
                  "triceps brachii — corroborating this secondary call.",
    ),
]

_OVERHEAD_PRESS: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="overhead_press", muscle="anterior_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Overhead pressing is anterior-deltoid-driven shoulder "
                  "flexion — the prime action.",
    ),
    ExerciseInvolvement(
        exercise="overhead_press", muscle="lateral_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists abduction/elevation of the humerus through the "
                  "press; a strong synergist but not the prime mover.",
    ),
    ExerciseInvolvement(
        exercise="overhead_press", muscle="triceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Elbow extension through the lockout — indirect arm work.",
    ),
    ExerciseInvolvement(
        exercise="overhead_press", muscle="trapezius",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The upper traps upwardly rotate the scapula to complete "
                  "the overhead position — a genuine synergist of overhead "
                  "pressing.",
    ),
]

_DUMBBELL_FRONT_RAISE: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="dumbbell_front_raise", muscle="anterior_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Isolated shoulder flexion in the sagittal plane — the "
                  "anterior deltoid's prime action.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_front_raise", muscle="pectoralis_major",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The clavicular fibres assist shoulder flexion; a secondary "
                  "contributor to the raise.",
    ),
]

# --- Lateral-deltoid exercises ---

_CABLE_LATERAL_RAISE: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="cable_lateral_raise", muscle="lateral_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Shoulder abduction in the frontal/scapular plane — the "
                  "lateral deltoid's prime action.",
    ),
    ExerciseInvolvement(
        exercise="cable_lateral_raise", muscle="anterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists humeral elevation depending on the exact arm path; "
                  "a synergist of the raise.",
    ),
    ExerciseInvolvement(
        exercise="cable_lateral_raise", muscle="trapezius",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The upper traps upwardly rotate the scapula through the "
                  "raise — a synergist.",
    ),
]

_UPRIGHT_ROW: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="upright_row", muscle="lateral_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Abduction of the humerus as the elbows rise is a prime "
                  "action of the upright row.",
    ),
    ExerciseInvolvement(
        exercise="upright_row", muscle="trapezius",
        role="primary", basis=BIOMECHANICAL,
        rationale="The upright row is a prime trapezius exercise — the upper "
                  "traps elevate the shoulder girdle and upwardly rotate the "
                  "scapula.",
    ),
    ExerciseInvolvement(
        exercise="upright_row", muscle="anterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists humeral elevation through the pull; a synergist.",
    ),
    ExerciseInvolvement(
        exercise="upright_row", muscle="biceps_brachii",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Elbow flexion under load as the bar rises — indirect arm "
                  "work.",
    ),
    ExerciseInvolvement(
        exercise="upright_row", muscle="brachialis",
        role="secondary", basis=BIOMECHANICAL,
        rationale="A prime elbow flexor regardless of grip; loaded on the "
                  "elbow-flexion component of the pull.",
    ),
]

_DUMBBELL_LATERAL_RAISE: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="dumbbell_lateral_raise", muscle="lateral_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Shoulder abduction in the frontal/scapular plane — the "
                  "lateral deltoid's prime action.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_lateral_raise", muscle="anterior_deltoid",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assists humeral elevation depending on the exact arm path; "
                  "a synergist of the raise.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_lateral_raise", muscle="trapezius",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The upper traps upwardly rotate the scapula through the "
                  "raise — a synergist.",
    ),
]

# --- Posterior-deltoid exercises ---

_CABLE_REAR_DELT_FLY: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="cable_rear_delt_fly", muscle="posterior_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Horizontal shoulder abduction/extension — the posterior "
                  "deltoid's prime action.",
    ),
    ExerciseInvolvement(
        exercise="cable_rear_delt_fly", muscle="rhomboids",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assist scapular retraction as the arms travel out and "
                  "back; a synergist of the fly.",
    ),
    ExerciseInvolvement(
        exercise="cable_rear_delt_fly", muscle="trapezius",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The middle traps assist scapular retraction during the "
                  "fly; a synergist.",
    ),
]

_REVERSE_PEC_DECK: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="reverse_pec_deck", muscle="posterior_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Horizontal shoulder abduction/extension — the posterior "
                  "deltoid's prime action.",
    ),
    ExerciseInvolvement(
        exercise="reverse_pec_deck", muscle="rhomboids",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assist scapular retraction as the arms travel back; a "
                  "synergist of the movement.",
    ),
    ExerciseInvolvement(
        exercise="reverse_pec_deck", muscle="trapezius",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The middle traps assist scapular retraction through the "
                  "movement; a synergist.",
    ),
]

_DUMBBELL_REVERSE_FLY: list[ExerciseInvolvement] = [
    ExerciseInvolvement(
        exercise="dumbbell_reverse_fly", muscle="posterior_deltoid",
        role="primary", basis=BIOMECHANICAL,
        rationale="Horizontal shoulder abduction/extension — the posterior "
                  "deltoid's prime action.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_reverse_fly", muscle="rhomboids",
        role="secondary", basis=BIOMECHANICAL,
        rationale="Assist scapular retraction as the arms travel out and "
                  "back; a synergist of the fly.",
    ),
    ExerciseInvolvement(
        exercise="dumbbell_reverse_fly", muscle="trapezius",
        role="secondary", basis=BIOMECHANICAL,
        rationale="The middle traps assist scapular retraction during the "
                  "fly; a synergist.",
    ),
]


# ============================================================================
# Aggregate — consumed by the registry's _INVOLVEMENT_INDEX
# ============================================================================

_LATS_EXERCISES: list[list[ExerciseInvolvement]] = [
    _DUMBBELL_PULLOVER, _CABLE_PULLOVER, _STRAIGHT_ARM_PULLDOWN,
    _PULL_UP, _LAT_PULLDOWN, _SEATED_CABLE_ROW, _BARBELL_ROW,
]
_DELTOID_EXERCISES: list[list[ExerciseInvolvement]] = [
    _INCLINE_BENCH_PRESS, _OVERHEAD_PRESS, _DUMBBELL_FRONT_RAISE,
    _CABLE_LATERAL_RAISE, _UPRIGHT_ROW, _DUMBBELL_LATERAL_RAISE,
    _CABLE_REAR_DELT_FLY, _REVERSE_PEC_DECK, _DUMBBELL_REVERSE_FLY,
]

EXERCISE_INVOLVEMENT: list[ExerciseInvolvement] = [
    row
    for group in (_LATS_EXERCISES + _DELTOID_EXERCISES)
    for row in group
]


# ----------------------------------------------------------------------------
# Practical guidance derived from this map
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
This is the exercise -> muscle INVOLVEMENT map (ADR-011) — cross-muscle volume
bookkeeping. For each exercise it lists every muscle trained and a role
(primary / secondary / stabiliser); `set_credit` turns that into fractional
training volume (1.0 / 0.5 / 0.0) per Pelland 2026's direct/indirect counting.

Use it for per-muscle weekly volume accounting: a barbell row credits 1.0 set
each to the lats, mid-traps and rhomboids, 0.5 each to the biceps, rear delt,
brachialis and teres major, and 0.0 to the erectors (braced, not trained). So a
program that already has heavy rowing has banked real biceps and rear-delt
volume — do not prescribe those as if untouched.

Do NOT use this map to choose between exercises for one muscle, or to target a
sub-region. That is the emphasis layer (`emphasis_for_muscle` /
`selection_emphasis`). Involvement says THAT a muscle is trained and how much
volume it banks; emphasis says how WELL, and where within the muscle.

Every row applies to both hypertrophy and strength — role is anatomy. The 0.5
indirect weight is Pelland 2026's heuristic, applied to both its hypertrophy
and strength volume regressions; treat it as a working assumption.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise -> muscle involvement map  (ADR-011 prototype)")
    by_exercise: dict[str, list[ExerciseInvolvement]] = {}
    for r in EXERCISE_INVOLVEMENT:
        by_exercise.setdefault(r.exercise, []).append(r)
    print(f"{len(EXERCISE_INVOLVEMENT)} rows across "
          f"{len(by_exercise)} exercises\n")
    for exercise, rows in by_exercise.items():
        print(f"  {exercise}")
        for r in sorted(rows, key=lambda x: -x.set_credit):
            tag = "" if r.basis == BIOMECHANICAL else "  [Pelland T1]"
            print(f"    {r.muscle:<20} {r.role:<10} "
                  f"credit {r.set_credit:.1f}{tag}")
    # invariants
    assert all(r.set_credit in (1.0, 0.5, 0.0) for r in EXERCISE_INVOLVEMENT)
    assert all(set(r.outcomes) == {"hypertrophy", "strength"}
               for r in EXERCISE_INVOLVEMENT)
    # one row per (exercise, muscle)
    keys = [(r.exercise, r.muscle) for r in EXERCISE_INVOLVEMENT]
    assert len(keys) == len(set(keys)), "duplicate (exercise, muscle) row"
    # every exercise has exactly one primary-or-more
    for exercise, rows in by_exercise.items():
        assert any(r.role == "primary" for r in rows), \
            f"{exercise} has no primary mover"
    print("\n  sanity checks passed.")
