"""
Pelland JC, Remmert JF, Robinson ZP, Hinson SR, Zourdos MC.
The Resistance Training Dose Response: Meta-Regressions Exploring the Effects
of Weekly Volume and Frequency on Muscle Hypertrophy and Strength Gains.
Sports Medicine. 2026 Feb;56(2):481-505. doi: 10.1007/s40279-025-02344-w

Open data + code: https://osf.io/6z3xu

Refactored to expose EffectEstimate objects so this paper can be combined
with other dose-response sources (e.g., Schoenfeld 2017, Baz-Valle 2022,
Currier 2023) as we add them.
"""

from __future__ import annotations
from dataclasses import dataclass
import math

from .shared import (
    Citation, PopulationSpec, EffectEstimate, UserProfile,
)


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Pelland et al.",
    year=2026,
    doi="10.1007/s40279-025-02344-w",
    journal="Sports Medicine",
    osf_url="https://osf.io/6z3xu",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Study design       0.85 (meta-analysis of RCTs, pre-registered on OSF)
# Sample size        1.00 (n=2058 across 67 studies)
# Measurement        0.95 (restricted to direct site-specific MT/CSA/MRI)
# Methodological     1.00 (Bayesian meta-regression, multiple functional forms,
#                          sensitivity analyses, fractional quantification)
# Reporting          1.00 (full data + R code on OSF)
# Risk of bias       0.85 (authors are commercial coaches; methods exemplary)
# Population         0.90 (clear inclusion criteria; young adults documented)
# Weighted average: 0.94. No modifiers.
QUALITY = 0.94


# ----------------------------------------------------------------------------
# Population studied
# ----------------------------------------------------------------------------
# 79.1% male / 20.9% female. 25.16 ± 5.22 years. ~10-week interventions.
# 28 untrained studies, 39 trained studies.
#
# IMPORTANT (audit 2026-05-17): the primary meta-regressions POOL untrained and
# trained participants and include training status only as an adjusted
# covariate. The marginal slopes encoded below are "proportionally marginalized
# across the categorical fixed effect (training status)" (Fig. 5-8 captions) —
# i.e. averaged over untrained AND trained, not specific to trained lifters.
# The correct training_status is therefore "mixed". The earlier "trained" label
# distorted applicability_to(): it wrongly penalised untrained users 0.5x and
# gave trained users a spurious perfect match.

POPULATION_MIXED_SEX = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    # ASSUMPTION: the paper reports only mean age 25.16 +/- 5.22 y and excludes
    # participants >70 y; it states no explicit min/max range. (18, 40) is an
    # inferred applicability envelope for the typical RT-study age band, not a
    # figure stated in the paper.
    age_range=(18, 40),
    outcome="hypertrophy",
    notes="Pelland 2026 hypertrophy regressions: 35 studies, 1032 participants. "
          "Untrained + trained pooled; status adjusted as a covariate.",
)

POPULATION_MIXED_STRENGTH = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    age_range=(18, 40),    # see ASSUMPTION note above
    outcome="strength",
    notes="Pelland 2026 strength regressions: 66 studies, 2020 participants. "
          "Untrained + trained pooled; status adjusted as a covariate.",
)


# ----------------------------------------------------------------------------
# Marginal slope estimates — one EffectEstimate per finding
# ----------------------------------------------------------------------------
# These are the LINEAR slopes at the population-average volume.
# Scale: percentage points of expected hypertrophy/strength gain per added
# weekly fractional set, over a ~10-week intervention.
#
# SE recovery (audit 2026-05-17): the paper reports quantile-based posterior
# compatibility intervals on the percentage scale (Fig. 5-8 captions) — NOT
# log-symmetric intervals, as an earlier comment here wrongly claimed. We
# approximate each posterior as Normal(mean, SE) with
#   SE = (upper - lower) / (2 * 1.96)
# This is an engineering approximation for inverse-variance pooling. It is
# least faithful for FREQUENCY_HYPERTROPHY_SLOPE, whose CrI is wide, mildly
# right-skewed, and crosses zero.

def _se_from_ci(lower: float, upper: float) -> float:
    return (upper - lower) / (2 * 1.96)


VOLUME_HYPERTROPHY_SLOPE = EffectEstimate(
    mean=0.24,
    se=_se_from_ci(0.15, 0.33),    # = 0.046
    n=1032,                         # participants in hypertrophy regressions
    population=POPULATION_MIXED_SEX,
    source=CITATION,
    quality_score=QUALITY,
    scale="pct_per_fractional_set",
    n_studies=35,                   # 35 studies / 220 effects in the volume-hypertrophy regression
    notes="Marginal slope at mean volume of 12.25 fractional sets/wk. "
          "Square-root best-fit model with diminishing returns. "
          "Posterior P(slope>0)=1.00.",
)

VOLUME_STRENGTH_SLOPE = EffectEstimate(
    mean=0.21,
    se=_se_from_ci(0.16, 0.26),    # = 0.026
    n=2020,                         # participants in strength regressions
    population=POPULATION_MIXED_STRENGTH,
    source=CITATION,
    quality_score=QUALITY,
    scale="pct_per_fractional_set",
    n_studies=66,                   # 66 studies / 490 effects in the volume-strength regression
    notes="Marginal slope at the strength regression's mean fractional volume "
          "(~8.14 sets/wk, not 12.25). Reciprocal best-fit with strong "
          "diminishing returns and functional plateau. Posterior P(slope>0)=1.00.",
)

FREQUENCY_HYPERTROPHY_SLOPE = EffectEstimate(
    mean=0.32,
    se=_se_from_ci(-0.14, 0.82),   # = 0.245 (wide — note the CrI crosses zero)
    n=1032,
    population=POPULATION_MIXED_SEX,
    source=CITATION,
    quality_score=QUALITY,
    scale="pct_per_fractional_session_per_week",
    n_studies=35,
    notes="At fixed volume, frequency effect on hypertrophy is compatible "
          "with negligible. Frequency is itself fractional (indirect sessions "
          "x 0.5). Posterior P(slope>0)=0.913 (CrI includes 0). "
          "Practical implication: prioritize total volume over frequency for "
          "hypertrophy goals.",
)

FREQUENCY_STRENGTH_SLOPE = EffectEstimate(
    mean=3.27,
    se=_se_from_ci(2.74, 3.84),    # = 0.281
    n=2020,
    population=POPULATION_MIXED_STRENGTH,
    source=CITATION,
    quality_score=QUALITY,
    scale="pct_per_fractional_session_per_week",
    n_studies=66,
    notes="Strong positive effect of frequency on strength with diminishing "
          "returns. Frequency is fractional (indirect sessions x 0.5). "
          "1→2 sessions: +4.6%; 2→3: smaller; 3+: smaller still. "
          "Posterior P(slope>0)=1.00.",
)


# ----------------------------------------------------------------------------
# Lists for the registry to consume
# ----------------------------------------------------------------------------

VOLUME_HYPERTROPHY_ESTIMATES: list[EffectEstimate] = [VOLUME_HYPERTROPHY_SLOPE]
VOLUME_STRENGTH_ESTIMATES: list[EffectEstimate] = [VOLUME_STRENGTH_SLOPE]
FREQUENCY_HYPERTROPHY_ESTIMATES: list[EffectEstimate] = [FREQUENCY_HYPERTROPHY_SLOPE]
FREQUENCY_STRENGTH_ESTIMATES: list[EffectEstimate] = [FREQUENCY_STRENGTH_SLOPE]


# ----------------------------------------------------------------------------
# Predictive functions — derived from the slopes + best-fit functional forms
# ----------------------------------------------------------------------------
# WARNING (audit 2026-05-17): these are the module author's RECONSTRUCTIONS of
# the paper's best-fit curve families, not curves reported in the paper. The
# paper publishes marginal slopes and the best-fit family, not fitted
# coefficients/intercepts. Refit against the OSF dataset before any optimizer
# relies on absolute predictions. predicted_hypertrophy_pct is at least
# internally consistent with the 0.24%/set slope; predicted_strength_pct is
# NOT consistent with the reported 0.21%/set slope — see its docstring.

def predicted_hypertrophy_pct(fractional_weekly_sets: float) -> float:
    """Square-root model. Returns expected % muscle size change over ~10wk.

    Internally consistent: derivative a/(2*sqrt(x)) = 0.24 at x=12.25 (the
    hypertrophy regression's mean fractional volume) gives a=1.68. The curve
    INTERCEPT is still a reconstruction, not a paper-reported value.
    """
    if fractional_weekly_sets <= 0:
        return 0.0
    a = 1.68  # derivative a / (2 * sqrt(12.25)) = 0.24 -> a = 1.68
    return a * math.sqrt(fractional_weekly_sets)


def predicted_strength_pct(fractional_weekly_sets: float) -> float:
    """Reciprocal placeholder — NOT YET CALIBRATED. Do not use in the optimizer.

    Audit 2026-05-17: an earlier docstring claimed this was "calibrated to
    0.21%/set at mean". It is not. With c=25.0, k=0.4 the marginal slope is
    ~0.287%/set at x=12.25 and ~0.30%/set at the strength regression's actual
    mean fractional volume (~8.14 sets/wk) — i.e. ~40% steeper than the paper's
    reported 0.21%/set. The plateau height c=25% is also not a paper-reported
    number. Refit against the OSF dataset (https://osf.io/6z3xu) before use.
    """
    if fractional_weekly_sets <= 0:
        return 0.0
    c, k = 25.0, 0.4  # PLACEHOLDER constants — see docstring; not calibrated
    return c * (1 - 1 / (1 + k * fractional_weekly_sets))


# ----------------------------------------------------------------------------
# Volume efficiency tiers — for use in optimizer soft constraints
# ----------------------------------------------------------------------------

SDES_HYPERTROPHY_PCT = 2.05
SDES_STRENGTH_PCT = 3.96


@dataclass
class EfficiencyTier:
    name: str
    sets_per_week_min: float
    sets_per_week_max: float | None
    description: str


HYPERTROPHY_TIERS = [
    EfficiencyTier("minimum_effective_dose", 4, 4,
                   "Sufficient to elicit detectable hypertrophy."),
    EfficiencyTier("higher_efficiency", 5, 10,
                   "~6 additional sets per next detectable bump."),
    EfficiencyTier("intermediate_efficiency", 11, 18,
                   "~8.5 additional sets per next bump. Typical recommendation."),
    EfficiencyTier("lower_efficiency", 19, 29,
                   "~10.75 additional sets per next bump."),
    EfficiencyTier("lowest_efficiency", 30, 42,
                   "~12.5 additional sets per next bump."),
    EfficiencyTier("unclear", 43, None,
                   "Insufficient data; possibly counterproductive."),
]

STRENGTH_TIERS = [
    EfficiencyTier("minimum_effective_dose", 1, 1,
                   "Sufficient to elicit detectable strength gain."),
    EfficiencyTier("higher_efficiency", 2, 2,
                   "~0.75 additional sets per next bump."),
    EfficiencyTier("intermediate_efficiency", 3, 4,
                   "~2.25 additional sets per next bump."),
    EfficiencyTier("lower_efficiency", 5, None,
                   "Additional sets do not consistently exceed SDES."),
]


# ----------------------------------------------------------------------------
# Fractional set counting (required preprocessing for these priors)
# ----------------------------------------------------------------------------
# The direct=1.0 / indirect=0.5 weighting IS Pelland 2026's own methodology
# (Sec. 2.5: "indirect x 0.5 + direct"), and the paper found strong Bayes-factor
# support for it over 'total' (1.0) and 'direct' (0.0) counting. But the authors
# explicitly call the 0.5 weight "a heuristic ... rather than a definitive
# standard" (Sec. 4.1) — treat it as a working assumption, not settled fact.
#
# HYPERTROPHY_CLASSIFICATIONS transcribes Pelland 2026 Table 1 and is
# hypertrophy-only: the paper's separate strength classification (Table 2) is
# intentionally NOT encoded here. fractional_set_count() returns 0.0 for any
# exercise not listed for a muscle, which silently UNDER-counts — callers
# should flag unclassified exercises for review rather than trust the 0.0.

DIRECT_SET_WEIGHT = 1.0
INDIRECT_SET_WEIGHT = 0.5

HYPERTROPHY_CLASSIFICATIONS = {
    "triceps_brachii": {
        "direct": {"triceps_pushdown", "triceps_extension", "triceps_kickback",
                   "skullcrusher", "lying_triceps_press", "lying_triceps_extension",
                   "cable_overhead_extension", "overhead_dumbbell_extension",
                   "close_grip_bench"},
        "indirect": {"flat_bench_press", "incline_bench_press", "decline_bench_press",
                     "shoulder_press", "dumbbell_shoulder_press",
                     "incline_dumbbell_press", "incline_machine_press", "machine_press"},
    },
    "biceps_brachii": {
        "direct": {"biceps_curl", "dumbbell_biceps_curl", "hammer_curl",
                   "dumbbell_incline_curl", "barbell_preacher_curl",
                   "dumbbell_preacher_curl", "machine_curl"},
        "indirect": {"lat_pulldown", "neutral_grip_lat_pulldown", "supine_grip_pulldown",
                     "machine_lat_pulldown", "seated_row", "close_grip_machine_row",
                     "wide_grip_machine_row", "bent_over_barbell_row",
                     "supine_grip_bent_over_row"},
    },
    "pectoralis_major": {
        "direct": {"bench_press", "flat_dumbbell_fly"},
        "indirect": set(),
    },
    "quadriceps": {
        "direct": {"back_squat", "leg_press", "dumbbell_lunge", "leg_extension",
                   "hack_squat", "smith_machine_squat", "barbell_split_squat",
                   "dumbbell_split_squat", "bulgarian_split_squat"},
        "indirect": set(),
    },
    "hamstrings": {
        "direct": {"leg_curl"},
        "indirect": set(),
    },
    "anterior_deltoid": {
        "direct": {"barbell_shoulder_press", "barbell_shoulder_front_raise"},
        "indirect": {"bench_press", "chest_press", "barbell_close_grip_press"},
    },
    # Table 1 rows previously omitted (audit 2026-05-17):
    "rectus_femoris": {
        "direct": {"leg_extension"},
        "indirect": {"smith_machine_squat", "leg_press", "back_squat"},
    },
    "trapezius": {
        "direct": set(),
        "indirect": {"lat_pulldown", "seated_row"},
    },
}


def fractional_set_count(exercise: str, raw_sets: int, target_muscle: str) -> float:
    """Convert raw sets to fractional sets per Pelland 2026 methodology."""
    cls = HYPERTROPHY_CLASSIFICATIONS.get(target_muscle)
    if cls is None:
        return float(raw_sets)  # unknown muscle — fall back; flag for review
    if exercise in cls["direct"]:
        return raw_sets * DIRECT_SET_WEIGHT
    if exercise in cls["indirect"]:
        return raw_sets * INDIRECT_SET_WEIGHT
    return 0.0   # not classified for this muscle


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Pelland 2026 — quality {QUALITY}, n={VOLUME_HYPERTROPHY_SLOPE.n}")
    e = VOLUME_HYPERTROPHY_SLOPE
    print(f"  Volume → hypertrophy slope: {e.mean:.3f}%/set "
          f"(95% CI {e.ci_95[0]:.3f}, {e.ci_95[1]:.3f})")
    print(f"  Precision: {e.precision:.1f}")
    print(f"  Source: {e.source}")
