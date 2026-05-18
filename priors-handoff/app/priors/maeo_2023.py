"""
Maeo S, Wu Y, Huang M, Sakurai H, Kusagawa Y, Sugiyama T, Kanehisa H, Isaka T.
Triceps brachii hypertrophy is substantially greater after elbow extension
training performed in the overhead versus neutral arm position.
European Journal of Sport Science. 2023;23(7):1240-1250.
doi: 10.1080/17461391.2022.2100279
PMID: 35819335

KEY FINDING (12-week within-participant study, n=21 arms per condition):

  Cable overhead extension vs. cable pushdown, MRI-measured muscle volume:

  TBLong (long head):     +28.5% vs +19.6%   (Cohen's d = 0.61, P < 0.001)
  TBLat+Med (combined):   +14.6% vs +10.5%   (Cohen's d = 0.39, P = 0.002)
  Whole-TB (total triceps): +19.9% vs +13.9% (Cohen's d = 0.54, P < 0.001)

  Despite the overhead arm using 34-39% LOWER absolute load throughout.

POPULATION:
  21 healthy young adults (14 M, 7 F), mean age ~23 years, untrained.
  Within-participant design: each participant trained one arm overhead, the
  other neutral, for 12 weeks at 70% 1RM, 5x10, 2 sessions/week.

THIS MODULE DOES TWO THINGS:

1. Encodes the whole-muscle effect of "overhead vs neutral" as an
   EffectEstimate, useful when combining with other length-comparison studies.

2. Encodes per-exercise ExerciseEmphasis values for triceps long head vs
   lateral+medial heads. This is the data the optimizer needs to choose
   "which exercises to prescribe for a long-head emphasis goal".

CONTEXT TO REMEMBER:

Maeo found WHOLE-MUSCLE differences between exercises. The Varovic 2025
meta-analysis found that REGIONAL differences (proximal vs distal within
the SAME muscle) are trivial across studies. These are different questions:

- Maeo: "Does overhead extension grow the long head more than pushdown does?"
  YES, substantially (long head: 28.5% vs 19.6%).
- Varovic: "When training at long vs short lengths, does the muscle grow
  more at one site (proximal/mid/distal) than another?"
  No meaningful regional preference detected.

For your fitness app's needs (choosing exercises to emphasize specific
muscles or sub-muscles), Maeo's data is more directly useful.
"""

from __future__ import annotations
import math

from .shared import (
    Citation, PopulationSpec, EffectEstimate, ExerciseEmphasis,
)


# ----------------------------------------------------------------------------
# Citation and quality
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Maeo et al.",
    year=2023,
    doi="10.1080/17461391.2022.2100279",
    journal="European Journal of Sport Science",
)

# Per QUALITY_RUBRIC.md v1.0:
# Study design       0.90 — DELIBERATE DEVIATION. This is a within-participant
#                    contralateral-limb (side-to-side) training study; the
#                    rubric's literal row for side-to-side designs is 0.5.
#                    Scored 0.90 because arm assignment was randomized and
#                    counterbalanced and the contralateral model is an
#                    established, powerful design for hypertrophy comparisons
#                    (invoking the rubric's "When to deviate" clause).
# Sample size        0.80 (n=21 per condition; rubric's 15-24 band)
# Measurement        1.00 (MRI muscle volume — gold standard, blinded analysis)
# Methodological     0.85 (rigorous baseline-adjusted ANCOVA + mixed model; no pre-reg)
# Reporting          0.90 (full effect sizes with CIs, but the supplement is a
#                    results TABLE — not an OSF/code raw-data deposit — and the
#                    SE here had to be approximated; below the 0.95/1.0 tier)
# Risk of bias       0.90 (academic sports-science grant; "no conflict" declared)
# Population         0.85 (young adults, mixed sex, untrained — well described)
# Weighted average: 0.8925 → 0.89
QUALITY = 0.89


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------

POPULATION = PopulationSpec(
    training_status="untrained",
    sex="mixed",
    # Paper reports age as means±SD (M 23.0±1.4 y, F 24.3±1.6 y); nearly all
    # participants fall within ~21-27. Tightened from an earlier over-wide
    # (20, 30) so applicability_to() does not over-credit users near 30.
    age_range=(21, 27),
    outcome="hypertrophy",
    notes="21 young adults (14M, 7F), mean age ~23, untrained. "
          "Within-participant (contralateral-arm) design.",
)


# ----------------------------------------------------------------------------
# Whole-muscle effect estimates (overhead vs neutral)
# ----------------------------------------------------------------------------
# Effect size scale: paper-reported Cohen's d.
#
# CORRECTION (audit 2026-05-17): an earlier comment here claimed d was "the
# ABSOLUTE growth in the overhead condition, not a difference effect size."
# That is backwards. The paper's Statistical analysis section defines d as the
# BETWEEN-CONDITION difference effect size (overhead - neutral) computed from
# absolute change values and standardized by the pooled SD of those change
# scores. Reconstruction from the published change-score means/SDs reproduces
# 0.61/0.39/0.54 exactly. So the encoded `mean` values ARE difference SMDs and
# ARE poolable as such — scale="standardized_mean_diff" is correct.
#
# The paper reports these between-condition Cohen's d values:
#   TBLong:    d = 0.61, P < 0.001
#   TBLat+Med: d = 0.39, P = 0.002
#   Whole-TB:  d = 0.54, P < 0.001
#
# Note on n: all three estimates use n=21, the within-participant count. The
# between-condition contrast does not have 21 INDEPENDENT observations per arm,
# so downstream sqrt(n) weighting in best_applicable slightly over-credits this
# study's statistical power.

def _unpaired_d_se(cohens_d: float, n: int) -> float:
    """Approximate SE for Cohen's d via the independent-groups formula.

    NOTE: this is the large-sample SE for an UNPAIRED (between-subjects) d.
    Maeo's design is within-participant (each subject trained one arm each
    way), so the two arms' change scores are correlated and the true paired
    SE is smaller than this. Recovering the exact paired SE needs the
    arm-to-arm correlation, which lives only in the paper's unread
    Supplementary data 1. This formula is therefore a deliberately
    CONSERVATIVE (too-wide) approximation — the Reporting quality dimension
    was dropped to 0.90 to reflect that SE had to be approximated.
    """
    return math.sqrt(1/n + (cohens_d ** 2) / (2 * n))


TRICEPS_LONG_HEAD_OVERHEAD_VS_NEUTRAL = EffectEstimate(
    mean=0.61,
    se=_unpaired_d_se(0.61, 21),
    n=21,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",  # between-condition Cohen's d (overhead - neutral)
    notes="TBLong (long head) growth advantage for overhead vs neutral arm "
          "position. Absolute growth: +28.5% vs +19.6% over 12 weeks. "
          "MRI-measured. P < 0.001.",
)

TRICEPS_LATMED_OVERHEAD_VS_NEUTRAL = EffectEstimate(
    mean=0.39,
    se=_unpaired_d_se(0.39, 21),
    n=21,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="TBLat+Med (lateral + medial heads combined) growth advantage for "
          "overhead vs neutral. Absolute growth: +14.6% vs +10.5%. P = 0.002. "
          "Notably, lateral and medial heads are monoarticular and theoretically "
          "shouldn't be affected by shoulder position — but were. Authors "
          "speculate metabolic stress and altered force distribution.",
)

TRICEPS_WHOLE_OVERHEAD_VS_NEUTRAL = EffectEstimate(
    mean=0.54,
    se=_unpaired_d_se(0.54, 21),
    n=21,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="Whole-TB growth advantage for overhead vs neutral. "
          "Absolute growth: +19.9% vs +13.9%. P < 0.001.",
)

WHOLE_MUSCLE_EFFECTS: list[EffectEstimate] = [
    TRICEPS_LONG_HEAD_OVERHEAD_VS_NEUTRAL,
    TRICEPS_LATMED_OVERHEAD_VS_NEUTRAL,
    TRICEPS_WHOLE_OVERHEAD_VS_NEUTRAL,
]


# ----------------------------------------------------------------------------
# Exercise emphasis coefficients
# ----------------------------------------------------------------------------
# Derived from the absolute growth rates in Maeo 2023.
#
# Interpretation: if cable overhead extension produces +28.5% long-head growth
# over 12 weeks, and pushdown produces +19.6%, then overhead extension provides
# (28.5 / 28.5) = 1.0 emphasis for long head, and pushdown provides
# (19.6 / 28.5) = 0.69 emphasis for long head, relative to the best exercise
# we have data for.
#
# This is a strong simplification — we're assuming the best exercise we have
# data for is also the best exercise that exists. As we add more papers
# (e.g., comparing overhead extensions to skullcrushers, JM presses, etc.),
# the coefficients should be re-normalized.
#
# PROVISIONAL — METHOD CAVEAT (audit 2026-05-17): shared.py defines `emphasis`
# as a study-independent "fraction of maximum stimulus." A ratio of 12-week
# percent-growth outcomes is NOT that — it is intervention-, duration-, and
# population-specific, its implicit zero is anchored at "the weaker of two
# real exercises" (a pushdown still grew the long head +19.6%, not "0.69 of
# nothing"), and it will not generalize across studies with different baselines
# or measurement modalities. Treat the six values below as a PROVISIONAL
# within-this-study relative ranking, not stable exercise constants; the
# optimizer should consume them as soft priors with wide uncertainty. The
# "high" confidence on the long-head values means the DIRECTION of the
# long-head advantage is well-established — NOT that the exact 0.69 is.

# Long head emphasis
CABLE_OVERHEAD_EXTENSION_LONG_HEAD = ExerciseEmphasis(
    exercise="cable_overhead_extension",
    muscle="triceps_brachii",
    region="long_head",
    emphasis=1.0,        # baseline: best we have direct data for
    confidence="high",
    source=CITATION,
    rationale="+28.5% long-head muscle volume in 12 weeks (Maeo 2023). "
              "Highest direct evidence for long-head emphasis to date.",
    population=POPULATION,
    quality_score=QUALITY,
)

CABLE_PUSHDOWN_LONG_HEAD = ExerciseEmphasis(
    exercise="cable_pushdown",
    muscle="triceps_brachii",
    region="long_head",
    emphasis=19.6 / 28.5,    # ≈ 0.69
    confidence="high",
    source=CITATION,
    rationale="+19.6% long-head growth vs +28.5% for overhead extension. "
              "Normalized to overhead = 1.0. The long head is shortened "
              "during pushdowns (shoulder neutral), explaining reduced stimulus.",
    population=POPULATION,
    quality_score=QUALITY,
)

# Lat+Med (combined) emphasis
# These two heads are monoarticular and "should" be equivalent across positions,
# but Maeo found 1.4-fold greater growth in overhead anyway. We encode the
# observed values, not the theoretical "should be equal" expectation.

CABLE_OVERHEAD_EXTENSION_LATMED = ExerciseEmphasis(
    exercise="cable_overhead_extension",
    muscle="triceps_brachii",
    region="lateral_and_medial_heads",
    emphasis=1.0,        # baseline
    confidence="medium",  # lower than long-head: unexpected finding, mechanism unclear
    source=CITATION,
    rationale="+14.6% lat+med growth in 12 weeks. Higher than expected for "
              "monoarticular heads; authors attribute to metabolic stress or "
              "altered force distribution from weakened long-head contribution.",
    population=POPULATION,
    quality_score=QUALITY,
)

CABLE_PUSHDOWN_LATMED = ExerciseEmphasis(
    exercise="cable_pushdown",
    muscle="triceps_brachii",
    region="lateral_and_medial_heads",
    emphasis=10.5 / 14.6,   # ≈ 0.72
    confidence="medium",
    source=CITATION,
    rationale="+10.5% lat+med growth vs +14.6% for overhead. Normalized.",
    population=POPULATION,
    quality_score=QUALITY,
)

# Whole-muscle emphasis (sum of regional effects)
CABLE_OVERHEAD_EXTENSION_WHOLE = ExerciseEmphasis(
    exercise="cable_overhead_extension",
    muscle="triceps_brachii",
    region=None,         # whole muscle
    emphasis=1.0,
    confidence="high",
    source=CITATION,
    rationale="+19.9% whole-triceps growth in 12 weeks. Reference exercise.",
    population=POPULATION,
    quality_score=QUALITY,
)

CABLE_PUSHDOWN_WHOLE = ExerciseEmphasis(
    exercise="cable_pushdown",
    muscle="triceps_brachii",
    region=None,
    emphasis=13.9 / 19.9,   # ≈ 0.70
    confidence="high",
    source=CITATION,
    rationale="+13.9% whole-triceps growth vs +19.9% for overhead extension.",
    population=POPULATION,
    quality_score=QUALITY,
)


EMPHASIS_ESTIMATES: list[ExerciseEmphasis] = [
    CABLE_OVERHEAD_EXTENSION_LONG_HEAD,
    CABLE_PUSHDOWN_LONG_HEAD,
    CABLE_OVERHEAD_EXTENSION_LATMED,
    CABLE_PUSHDOWN_LATMED,
    CABLE_OVERHEAD_EXTENSION_WHOLE,
    CABLE_PUSHDOWN_WHOLE,
]


# ----------------------------------------------------------------------------
# Practical guidance derived from this paper
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
Exercise emphasis coefficients SHOULD be assigned for distinct biarticular
sub-muscles (like triceps long head vs lateral/medial heads, hamstring
biarticular vs short head), because those reflect actual functional anatomy.
Maeo 2023 is direct evidence for this: overhead vs neutral elbow extension
produced substantially different growth in the triceps long head specifically
(d = 0.61). That is a between-exercise, between-head claim — distinct from the
"proximal vs distal within the same muscle" question, where the meta-analytic
effect is trivial (see varovic_2025).
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Maeo 2023 — quality {QUALITY}, n=21 within-participant")
    print()
    print("Whole-muscle effects (overhead vs neutral, between-condition Cohen's d):")
    for e in WHOLE_MUSCLE_EFFECTS:
        lo, hi = e.ci_95
        print(f"  {e.notes[:50]}")
        print(f"    d = {e.mean:.2f}  (95% CI: {lo:.2f}, {hi:.2f})")
    print()
    print("Exercise emphasis values:")
    for em in EMPHASIS_ESTIMATES:
        region = em.region if em.region else "whole_muscle"
        print(f"  {em.exercise:<32} → {em.muscle}/{region}: {em.emphasis:.2f} "
              f"({em.confidence})")
