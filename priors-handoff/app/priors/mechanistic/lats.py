"""
Mechanistic exercise-selection prior — latissimus dorsi.

PROTOTYPE (ADR-010, proposed). The latissimus dorsi is `literature-blocked` in
COVERAGE.md §2: no longitudinal head-to-head exercise-comparison hypertrophy
trial exists — the lat-selection literature is almost entirely acute surface
EMG, which the priors layer hard-excludes. This module is the fallback: a
DERIVED prior, built from biomechanics + the layer's own encoded
lengthened-position evidence. It is NOT measured data and is never pooled with
measured `ExerciseEmphasis`. A real lat RCT, if one is ever published and
encoded, supersedes this module entirely.

----------------------------------------------------------------------------
THE DERIVATION (see ADR-010)
----------------------------------------------------------------------------

For each exercise, ask:

  1. INVOLVEMENT — does the exercise load an action the lat produces? The lat
     extends, adducts and internally rotates the humerus and assists scapular
     depression. Every exercise below loads shoulder extension/adduction, so
     all clear the involvement gate.

  2. LOADED LENGTH — at the HARDEST point of the exercise's resistance curve,
     is the lat long, mid or short? The lat is LONG with the arm overhead
     (shoulder flexed) and SHORT with the arm pulled down/back (shoulder
     extended). The decisive question is not "does the range pass through a
     stretch" but "is the muscle loaded WHILE stretched": a cable pulldown
     stretches the lat at the top but is hardest mid-range; a dumbbell pullover
     is hardest with the arm overhead — at the lat's longest length.

  3. EMPHASIS BUCKET — long -> 1.0, mid -> 0.70, short -> 0.50. COARSE buckets,
     not a fitted curve. The layer's encoded evidence (Maeo 2023 triceps,
     Maeo 2021 hamstrings, Kassiano 2023 calves, Wolf 2023 ROM meta-analysis)
     shows lengthened-biased loading grows muscle more — but with real
     magnitude uncertainty (Wolf's lengthened-partial CI ran -0.81 to +0.16),
     so this is a soft prior, hence confidence is capped at "low".

----------------------------------------------------------------------------
WHOLE MUSCLE vs UPPER / LOWER FIBRES — read this
----------------------------------------------------------------------------

The whole-muscle entries (region=None, confidence="low") are the defensible
deliverable: loaded length is a sound, mechanically-determinable property of
an exercise.

The regional entries (region="upper_fibres" / "lower_fibres",
confidence="speculative") are the SPECULATIVE EDGE of the method and are
flagged as such:

  - The loaded-length engine is a whole-muscle property — the lat lengthens
    largely as one unit at the humeral insertion.
  - Splitting upper vs lower rests on a weaker, secondary argument: the upper
    (costal/scapular) fibres' length is governed mainly by HUMERAL ELEVATION,
    while the lower (iliac / thoracolumbar) fibres also answer to TRUNK and
    PELVIC position. So overhead stretch-isolation work loads the upper
    fibres at length, and a bodyweight vertical pull — where the pelvis hangs
    as the far anchor — loads the long iliac-fibre line.
  - This is fibre-line-of-pull reasoning, not measured fact. Varovic 2025
    (encoded) found WITHIN-muscle regional hypertrophy effects trivial, which
    is a direct caution against over-trusting any regional split.

Treat the regional entries as tie-breakers at most. If they do not read as
credible, that is the prototype doing its job — drop the regional section and
keep whole-muscle.

Rows are encoded WHOLE-MUSCLE ONLY: a horizontal pull's upper/lower-fibre
behaviour is the murkiest case and is not worth a speculative guess.

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

MUSCLE = "latissimus_dorsi"

# Coarse emphasis buckets — one value per loaded-length class. NOT fitted.
_LONG = 1.0
_MID = 0.70
_SHORT = 0.50


# ============================================================================
# Whole-muscle priors (region=None) — the defensible deliverable
# ============================================================================

_WHOLE: list[MechanisticEmphasis] = [
    MechanisticEmphasis(
        exercise="dumbbell_pullover",
        muscle=MUSCLE, region=None,
        emphasis=_LONG, loaded_length="long", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="Lying pullover: the humerus arcs into deep flexion behind "
                  "the head. With a vertical dumbbell load the shoulder "
                  "resistance moment peaks when the upper arm is horizontal "
                  "behind the head — the lat is loaded HARDEST at near-maximal "
                  "length. The canonical lengthened-loaded lat exercise.",
    ),
    MechanisticEmphasis(
        exercise="cable_pullover",
        muscle=MUSCLE, region=None,
        emphasis=_LONG, loaded_length="long", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="Straight/slightly-bent-arm shoulder extension against a high "
                  "pulley. The cable holds tension into the fully-overhead "
                  "stretched start, so the lat is loaded at long length "
                  "through the part of the range where it is most stretched.",
    ),
    MechanisticEmphasis(
        exercise="straight_arm_pulldown",
        muscle=MUSCLE, region=None,
        emphasis=_LONG, loaded_length="long", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="Long straight-arm lever, high pulley. The straight arm "
                  "keeps a large shoulder moment at the overhead (lengthened) "
                  "start and the cable maintains tension there — the lat is "
                  "loaded while long.",
    ),
    MechanisticEmphasis(
        exercise="pull_up",
        muscle=MUSCLE, region=None,
        emphasis=_MID, loaded_length="mid", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="Vertical pull. The shoulder resistance moment peaks "
                  "mid-range (upper arm ~horizontal), where the lat is at mid "
                  "length. Note the coarse MID bucket understates one point: "
                  "the dead-hang start DOES load the lengthened lat under full "
                  "bodyweight — unlike a cable pulldown the top cannot be "
                  "unloaded — a genuine advantage for the pull-up.",
    ),
    MechanisticEmphasis(
        exercise="lat_pulldown",
        muscle=MUSCLE, region=None,
        emphasis=_MID, loaded_length="mid", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="Vertical cable pull. The resistance moment peaks mid-range "
                  "at mid muscle length; the fully-overhead (stretched) start "
                  "can be largely unloaded by relaxing into the top.",
    ),
    MechanisticEmphasis(
        exercise="seated_cable_row",
        muscle=MUSCLE, region=None,
        emphasis=_MID, loaded_length="mid", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="Horizontal pull. Constant cable tension does load the "
                  "somewhat-lengthened start, but the hardest leverage sits "
                  "across the mid-to-short range — mid loaded length overall.",
    ),
    MechanisticEmphasis(
        exercise="barbell_row",
        muscle=MUSCLE, region=None,
        emphasis=_SHORT, loaded_length="short", confidence="low",
        grounded_in=GROUNDED_IN,
        rationale="Torso horizontal, vertical gravity load. The shoulder "
                  "resistance moment peaks near the TOP of the row, where the "
                  "lat is SHORT (shoulder extended). The lengthened bottom "
                  "position carries little load (arm near-parallel to "
                  "gravity). Loaded hardest contracted.",
    ),
]


# ============================================================================
# Regional priors — SPECULATIVE (see the module docstring)
# ============================================================================
# region="upper_fibres": length governed mainly by humeral elevation, so
# overhead stretch-isolation work loads them at length.
# region="lower_fibres": iliac / thoracolumbar fibres; their long vertical
# line is loaded best by a bodyweight vertical pull hanging from a fixed bar.
# Rows are deliberately omitted here.

_UPPER: list[MechanisticEmphasis] = [
    MechanisticEmphasis(
        exercise="dumbbell_pullover", muscle=MUSCLE, region="upper_fibres",
        emphasis=_LONG, loaded_length="long", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. Overhead shoulder-isolation loads the lat via "
                  "humeral elevation, which governs the upper (costal/scapular) "
                  "fibres' length most directly — loaded long.",
    ),
    MechanisticEmphasis(
        exercise="cable_pullover", muscle=MUSCLE, region="upper_fibres",
        emphasis=_LONG, loaded_length="long", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. As dumbbell pullover — overhead humeral "
                  "elevation under cable tension loads the upper-fibre stretch.",
    ),
    MechanisticEmphasis(
        exercise="straight_arm_pulldown", muscle=MUSCLE, region="upper_fibres",
        emphasis=_LONG, loaded_length="long", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. Straight-arm overhead loading of the "
                  "humerus-governed upper fibres at length.",
    ),
    MechanisticEmphasis(
        exercise="pull_up", muscle=MUSCLE, region="upper_fibres",
        emphasis=_MID, loaded_length="mid", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. Hardest mid-range; upper fibres at mid length.",
    ),
    MechanisticEmphasis(
        exercise="lat_pulldown", muscle=MUSCLE, region="upper_fibres",
        emphasis=_MID, loaded_length="mid", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. Hardest mid-range; upper fibres at mid length.",
    ),
]

_LOWER: list[MechanisticEmphasis] = [
    MechanisticEmphasis(
        exercise="pull_up", muscle=MUSCLE, region="lower_fibres",
        emphasis=_LONG, loaded_length="long", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. A bodyweight pull hanging from a fixed bar "
                  "loads the long vertical hand-to-pelvis line; the lower "
                  "(iliac / thoracolumbar) fibres, whose length also answers "
                  "to trunk/pelvic position, are loaded at length here in a "
                  "way a benched or seated movement is not.",
    ),
    MechanisticEmphasis(
        exercise="lat_pulldown", muscle=MUSCLE, region="lower_fibres",
        emphasis=_MID, loaded_length="mid", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. Same vertical line as the pull-up but seated "
                  "with the pelvis fixed to a pad — the lower fibres are loaded "
                  "at mid length, not the hanging long line.",
    ),
    MechanisticEmphasis(
        exercise="straight_arm_pulldown", muscle=MUSCLE, region="lower_fibres",
        emphasis=_MID, loaded_length="mid", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. Loads the lat via humeral elevation; the "
                  "iliac-fibre length is governed partly by trunk/pelvis, "
                  "which this movement does not load at length — mid.",
    ),
    MechanisticEmphasis(
        exercise="dumbbell_pullover", muscle=MUSCLE, region="lower_fibres",
        emphasis=_MID, loaded_length="mid", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. Strong upper-fibre stretch loader, but the "
                  "lower (iliac) fibres, lying on a bench with the pelvis "
                  "unloaded, are not loaded at their long length — mid.",
    ),
    MechanisticEmphasis(
        exercise="cable_pullover", muscle=MUSCLE, region="lower_fibres",
        emphasis=_MID, loaded_length="mid", confidence="speculative",
        grounded_in=GROUNDED_IN,
        rationale="SPECULATIVE. As dumbbell pullover — upper-fibre stretch "
                  "loader; lower fibres at mid length.",
    ),
]


# Every mechanistic prior this module exports — consumed by the registry's
# separate _MECHANISTIC_INDEX (never the measured _EMPHASIS_INDEX).
MECHANISTIC_EMPHASIS: list[MechanisticEmphasis] = _WHOLE + _UPPER + _LOWER


# ----------------------------------------------------------------------------
# Practical guidance derived from this prior
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
There is no longitudinal head-to-head hypertrophy trial for lat exercise
selection — the literature is acute EMG, which the priors layer excludes. This
is a DERIVED fallback prior (ADR-010): biomechanics weighted by the layer's
encoded lengthened-position evidence. Use it only until a real lat RCT is
encoded; treat it as a soft prior, never as measured fact.

Whole-muscle reading the optimizer can act on: for lat hypertrophy, prefer
exercises that load the lat while it is LONG — dumbbell and cable pullovers and
the straight-arm pulldown load the stretched (overhead) position hardest.
Vertical pulls (pull-ups, pulldowns) and horizontal rows are loaded hardest at
mid or short length and rate lower on this prior — they still train the lat,
just less stretch-biased. A balanced lat session pairs a stretch-loaded
isolation movement with a pull.

Upper vs lower fibres: SPECULATIVE — the regional split rests on
fibre-line-of-pull reasoning, not measured data, and Varovic 2025 found
within-muscle regional effects trivial. At most a tie-breaker: overhead
stretch-isolation leans upper-fibre; a hanging bodyweight pull-up leans
lower-fibre. Do not build strong regional prescriptions on it.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Mechanistic prior — latissimus dorsi  (ADR-010 prototype)")
    print(f"grounded in: {', '.join(GROUNDED_IN)}")
    print(f"{len(MECHANISTIC_EMPHASIS)} entries "
          f"({len(_WHOLE)} whole-muscle, {len(_UPPER)} upper, {len(_LOWER)} lower)")
    for region_name, entries in (
        ("whole muscle", _WHOLE), ("upper_fibres", _UPPER), ("lower_fibres", _LOWER),
    ):
        print(f"\n  {region_name}:")
        for m in sorted(entries, key=lambda e: -e.emphasis):
            print(f"    {m.exercise:<24} {m.emphasis:.2f}  "
                  f"[{m.loaded_length:<5}] ({m.confidence})")
    assert all(0.0 <= m.emphasis <= 1.0 for m in MECHANISTIC_EMPHASIS)
    assert all(m.confidence == "low" for m in _WHOLE)
    assert all(m.confidence == "speculative" for m in _UPPER + _LOWER)
    print("\n  sanity checks passed.")
