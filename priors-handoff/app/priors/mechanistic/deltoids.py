"""
Mechanistic exercise-selection prior — deltoids (anterior / lateral / posterior).

PROTOTYPE (ADR-010). The deltoids are `literature-blocked` in COVERAGE.md §2:
no longitudinal head-to-head exercise-comparison hypertrophy trial exists (the
one longitudinal delt study, Coleman/Larsen 2024, is a dumbbell-vs-cable
equipment-equivalence question, not exercise selection — it stays deferred).
This module is the fallback: a DERIVED prior from biomechanics + the layer's
encoded lengthened-position evidence. It is NOT measured data, is never pooled
with measured `ExerciseEmphasis`, and a real delt RCT would supersede it.

----------------------------------------------------------------------------
WHY DELTOIDS ARE ENCODED PER HEAD AT confidence="low" (not "speculative")
----------------------------------------------------------------------------

The lats prototype split the muscle into upper/lower fibres at
confidence="speculative" — a contested within-muscle distinction. The deltoid
is different. Its three heads are FUNCTIONALLY DISTINCT — each has its own
prime action:

  - anterior  — shoulder flexion        (lengthened by shoulder EXTENSION:
                                          the upper arm drawn behind the body)
  - lateral   — shoulder abduction      (lengthened by ADDUCTION: arm down /
                                          across the body)
  - posterior — horizontal abduction /  (lengthened by horizontal ADDUCTION:
                shoulder extension       arm reaching across the front)

Targeting a head with an exercise that loads its prime action is not
speculative — it is basic, uncontested anatomy. So the heads are encoded as
regions at confidence="low", the standard mechanistic cap. The ONLY mechanistic
inference here is the loaded-length -> emphasis weighting (the soft prior that
loading a head while it is long grows it more); that inference is what keeps
this at "low" rather than "medium"/"high". region=None (whole deltoid) is
deliberately NOT encoded — deltoid training is head-specific; query by head.

----------------------------------------------------------------------------
THE DERIVATION (see ADR-010)
----------------------------------------------------------------------------

For each (exercise, head): is the head loaded — at the HARDEST point of the
exercise's resistance curve — at long, mid or short muscle length?
Bucket: long -> 1.0, mid -> 0.70, short -> 0.50 (coarse, not a fitted curve).

The recurring pattern: a free-weight raise/fly loaded by vertical gravity is
hardest at the TOP, where the trained head is SHORT (contracted) — the
lengthened bottom carries almost no moment. A cable variant set up to keep
tension on the lengthened (across-/behind-the-body) start loads the head while
it is LONG. This is why cable laterals and cable rear-delt work outrank their
dumbbell equivalents on a lengthened-position prior.

----------------------------------------------------------------------------
"""

from __future__ import annotations

from ..shared import MechanisticEmphasis


# Encoded modules whose longitudinal evidence establishes the
# lengthened-position -> growth principle this prior leans on.
GROUNDED_IN: tuple[str, ...] = (
    "maeo_2023",       # triceps long head: overhead (lengthened) > pushdown
    "maeo_2021",       # hamstrings: seated (hip-flexed, lengthened) > prone
    "kassiano_2023",   # gastrocnemius: lengthened-ROM calf raise favoured
    "wolf_2023",       # ROM meta-analysis: training through long lengths
)

MUSCLE = "deltoids"

# Coarse emphasis buckets — one value per loaded-length class. NOT fitted.
_LONG = 1.0
_MID = 0.70
_SHORT = 0.50


# ============================================================================
# Anterior deltoid (region="anterior") — prime action: shoulder flexion;
# lengthened when the upper arm is drawn behind the torso (shoulder extension).
# ============================================================================

_ANTERIOR: list[MechanisticEmphasis] = [
    MechanisticEmphasis(
        exercise="incline_bench_press",
        muscle=MUSCLE, region="anterior",
        emphasis=_LONG, loaded_length="long", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="At the bottom of an incline press the upper arm reaches "
                  "roughly the plane of the torso under heavy load — the most "
                  "lengthened, loaded position any common anterior-deltoid "
                  "exercise reaches. (Travelling behind the torso plane would "
                  "be an impingement fault, not the target.) Encoded `long` as "
                  "the within-head maximum: relative to the other anterior "
                  "exercises it loads the head longest and heaviest — not "
                  "because it reaches a deep anterior-delt stretch.",
    ),
    MechanisticEmphasis(
        exercise="overhead_press",
        muscle=MUSCLE, region="anterior",
        emphasis=_MID, loaded_length="mid", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="The overhead press is hardest near the bottom, with the "
                  "upper arm around shoulder height — the anterior delt is at "
                  "mid length there. It does not travel behind the torso, so "
                  "the deepest stretch is not loaded.",
    ),
    MechanisticEmphasis(
        exercise="dumbbell_front_raise",
        muscle=MUSCLE, region="anterior",
        emphasis=_MID, loaded_length="mid", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="A front raise is hardest with the arm horizontal (peak "
                  "moment for a vertical dumbbell load), where the anterior "
                  "delt is at mid length. The lengthened position (arm behind "
                  "the body) is never entered. Mid.",
    ),
]


# ============================================================================
# Lateral deltoid (region="lateral") — prime action: shoulder abduction;
# lengthened when the arm is adducted (down by, or across, the body).
# ============================================================================

_LATERAL: list[MechanisticEmphasis] = [
    MechanisticEmphasis(
        exercise="cable_lateral_raise",
        muscle=MUSCLE, region="lateral",
        emphasis=_LONG, loaded_length="long", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="A cross-body / behind-the-body cable lateral raise begins "
                  "with the arm adducted across the body — the lateral delt at "
                  "long length — and the cable holds tension there. The "
                  "lateral delt is loaded while stretched. (Assumes the cable "
                  "variant set up to load the bottom, not a token cable swap.)",
    ),
    MechanisticEmphasis(
        exercise="upright_row",
        muscle=MUSCLE, region="lateral",
        emphasis=_MID, loaded_length="mid", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="The upright row loads abduction through a mid arc; the "
                  "lateral delt is at mid length across the hardest part of "
                  "the pull.",
    ),
    MechanisticEmphasis(
        exercise="dumbbell_lateral_raise",
        muscle=MUSCLE, region="lateral",
        emphasis=_SHORT, loaded_length="short", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="A dumbbell lateral raise is hardest at the TOP (arm "
                  "horizontal — peak moment for the vertical load), where the "
                  "lateral delt is SHORT/contracted. At the stretched bottom "
                  "the moment arm is near zero. Loaded short.",
    ),
]


# ============================================================================
# Posterior deltoid (region="posterior") — prime action: horizontal abduction
# / shoulder extension; lengthened when the arm reaches across the front body.
# ============================================================================

_POSTERIOR: list[MechanisticEmphasis] = [
    MechanisticEmphasis(
        exercise="cable_rear_delt_fly",
        muscle=MUSCLE, region="posterior",
        emphasis=_LONG, loaded_length="long", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="A cross-body cable rear-delt fly begins with the arm "
                  "horizontally adducted across the front of the body — the "
                  "posterior delt at long length — and the cable keeps tension "
                  "there. Loaded while stretched. (Assumes the cross-body "
                  "cable setup that loads the across-body start, not a token "
                  "cable swap.)",
    ),
    MechanisticEmphasis(
        exercise="reverse_pec_deck",
        muscle=MUSCLE, region="posterior",
        emphasis=_MID, loaded_length="mid", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="The reverse pec deck holds fairly even machine tension "
                  "across the arc; the posterior delt is loaded around mid "
                  "length — the across-body start is loaded but not maximally "
                  "stretched.",
    ),
    MechanisticEmphasis(
        exercise="dumbbell_reverse_fly",
        muscle=MUSCLE, region="posterior",
        emphasis=_SHORT, loaded_length="short", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="A bent-over dumbbell reverse fly is hardest at the TOP (arm "
                  "out wide — peak moment for the vertical load), where the "
                  "posterior delt is SHORT. The stretched across-body bottom "
                  "carries almost no load. Loaded short.",
    ),
]


# Every mechanistic prior this module exports — consumed by the registry's
# separate _MECHANISTIC_INDEX (never the measured _EMPHASIS_INDEX).
MECHANISTIC_EMPHASIS: list[MechanisticEmphasis] = _ANTERIOR + _LATERAL + _POSTERIOR


# ----------------------------------------------------------------------------
# Practical guidance derived from this prior
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
There is no longitudinal head-to-head hypertrophy trial for deltoid exercise
selection — the literature is acute EMG, which the priors layer excludes. This
is a DERIVED fallback prior (ADR-010): biomechanics weighted by the layer's
encoded lengthened-position evidence. Use it only until a real delt RCT is
encoded; treat it as a soft prior.

The deltoid is trained PER HEAD — anterior, lateral, posterior — each with a
distinct prime action. Query by head, not whole-muscle.

Within each head, this prior prefers exercises that load the head while it is
LONG. The pattern is consistent: a free-weight raise or fly loaded by vertical
gravity is hardest at the top, where the trained head is SHORT (a dumbbell
lateral raise, a dumbbell reverse fly) — these rate lower. A cable variant set
up to keep tension on the across-/behind-the-body lengthened start (cable
lateral raise, cable rear-delt fly) loads the head stretched and rates highest.
For the anterior head an incline press loads the stretched (behind-torso)
bottom; vertical presses and front raises are loaded mid-range.

These exercises all still train their head — the bucket reflects stretch-bias,
not whether the exercise "works". A balanced delt plan can pair a stretch-biased
cable movement with a press; the prior just says, given a hypertrophy goal and
a choice, bias toward the lengthened-loaded option.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print("Mechanistic prior — deltoids  (ADR-010 prototype)")
    print(f"grounded in: {', '.join(GROUNDED_IN)}")
    print(f"{len(MECHANISTIC_EMPHASIS)} entries "
          f"({len(_ANTERIOR)} anterior, {len(_LATERAL)} lateral, "
          f"{len(_POSTERIOR)} posterior)")
    for head_name, entries in (
        ("anterior", _ANTERIOR), ("lateral", _LATERAL), ("posterior", _POSTERIOR),
    ):
        print(f"\n  {head_name}:")
        for m in sorted(entries, key=lambda e: -e.emphasis):
            print(f"    {m.exercise:<24} {m.emphasis:.2f}  "
                  f"[{m.loaded_length:<5}] ({m.confidence})")
    assert all(0.0 <= m.emphasis <= 1.0 for m in MECHANISTIC_EMPHASIS)
    assert all(m.confidence == "low" for m in MECHANISTIC_EMPHASIS)
    assert all(m.region in ("anterior", "lateral", "posterior")
               for m in MECHANISTIC_EMPHASIS)
    print("\n  sanity checks passed.")
