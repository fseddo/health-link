"""
Wolf M, Androulakis-Korakakis P, Fisher J, Schoenfeld B, Steele J.
Partial Vs Full Range of Motion Resistance Training: A Systematic Review
and Meta-Analysis.
International Journal of Strength and Conditioning. 2023;3(1).
doi: 10.47206/ijsc.v3i1.182

KEY FINDINGS (Bayesian meta-analysis; 24 studies reviewed, 23 in the main model):

Main model (all outcomes pooled):
  SMD: 0.12 (95% CI: -0.02, 0.26) — trivial, in favor of full ROM

"Muscle size" outcome sub-group (8 studies) — the hypertrophy estimate:
  SMD: 0.04 (95% QI: -0.17, 0.25) — trivial, in favor of full ROM

Sub-group: long-length partial ROM vs full ROM for hypertrophy (6 studies):
  SMD: -0.28 (95% CI: -0.81, 0.16) — trend favoring lengthened partials,
  but CI is wide and crosses zero

Sub-group: short-length partial ROM vs full ROM for hypertrophy:
  SMD: 0.08 (95% CI: -0.24, 0.42) — trivial, in favor of full ROM

When grouped by outcome type, SMDs span 0.05 to 0.20 ACROSS ALL FIVE outcome
categories — this is NOT a hypertrophy-specific range. Per outcome:
  Muscle size 0.04, strength 0.14, power 0.19, sport 0.02, body fat 0.12.
  Power SMD: 0.19 (0.01, 0.37) — trivial-small favoring full ROM.
  Strength: greatest gains in the ROM that was trained (specificity).

CONTEXT:

This was the FOUNDATIONAL meta-analysis on ROM effects. Subsequently:
- Varovic 2025 looked at REGIONAL hypertrophy specifically: trivial effects
- Wolf 2024/2025 (Lengthened Partials trial): found lengthened partials
  ELICIT SIMILAR adaptations to full ROM in trained individuals
- Several individual studies (Maeo, Kassiano, Pedrosa) found large
  long-length advantages in specific contexts

The broader literature (this paper PLUS the post-2023 work listed above)
points toward: full ROM and lengthened partials are roughly equivalent for
hypertrophy; short-length partials are weaker; exercise selection matters
MORE than ROM choice within a sensible exercise. Wolf 2023 alone does not
claim this convergence — it predates the 2025 trial, and its own long-length
sub-group leans toward partials (-0.28).

WHY THIS MATTERS FOR THE FITNESS APP:

This paper constrains how the optimizer should think about ROM. Don't
penalize partial ROM training if it's at long muscle lengths. Don't reward
"longer ROM" exercises across the board — the effect is trivial when the
shorter ROM is at appropriate lengths.

POPULATION:
  24 studies (Bayesian meta-analysis), mixed training status, mostly young
  adults. Both upper and lower body outcomes (no clear upper/lower difference).
"""

from __future__ import annotations

from .shared import (
    Citation, PopulationSpec, EffectEstimate,
)


CITATION = Citation(
    authors="Wolf et al.",
    year=2023,
    doi="10.47206/ijsc.v3i1.182",
    journal="International Journal of Strength and Conditioning",
)

# Per QUALITY_RUBRIC.md v1.0 (re-scored 2026-05-17 — see
# docs/priors/audits/wolf_2023_audit.md):
# Study design       0.70 (meta-analysis of mixed designs incl. within-subject
#                    side-to-side studies; rubric scores by the worst included
#                    design tier — dropped from an earlier optimistic 0.80)
# Sample size        0.85 (24 studies; hundreds of pooled participants)
# Measurement        0.80 (mixed muscle thickness / CSA / fiber CSA across studies)
# Methodological     0.90 (Bayesian framework with QIs, sub-group + moderator analyses)
# Reporting          0.90 (full QIs, sub-group breakdown, raw data discussed)
# Risk of bias       0.80 (the lead author's PhD was funded by Renaissance
#                    Periodization, a commercial training-education company;
#                    "no competing interests" declared, but this is a disclosed
#                    commercial tie — dropped from an earlier 0.85)
# Population         0.80 (mixed populations across included studies)
# Weighted average: 0.8125 → 0.81
QUALITY = 0.81


POPULATION_HYPERTROPHY = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    age_range=(18, 40),    # ASSUMPTION — paper reports per-study ages, no pooled range
    outcome="hypertrophy",
    notes="Wolf 2023 meta-analysis: 24 studies reviewed, 23 in the main model; "
          "mixed training status and populations.",
)


def _se_from_qi(low: float, high: float) -> float:
    return (high - low) / (2 * 1.96)


# Hypertrophy effect: the paper's "muscle size" outcome sub-group (8 studies).
# RELABELLED 2026-05-17: previously named PARTIAL_VS_FULL_OVERALL and described
# as the overall/main-model effect. It is NOT — 0.04 (-0.17, 0.25) is the
# muscle-size outcome sub-group. The paper's actual main model (all outcomes,
# 23 studies) is SMD 0.12 (95% CI -0.02, 0.26). For this hypertrophy-focused
# app the muscle-size sub-group is the right estimate to carry; it is just
# named and documented honestly now.
PARTIAL_VS_FULL_HYPERTROPHY = EffectEstimate(
    mean=0.04,
    se=_se_from_qi(-0.17, 0.25),
    n=212,                   # participants: 96 fROM + 116 pROM (Table 2, "muscle size")
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=8,
    notes="'Muscle size' outcome sub-group (8 studies). Partial vs full ROM "
          "for hypertrophy: SMD 0.04 favoring full ROM, but trivial. 95% QI: "
          "-0.17, 0.25 — crosses zero. This is NOT the paper's overall/main "
          "model (that is SMD 0.12, 95% CI -0.02, 0.26 across all outcomes).",
)

# Sub-group: LONG-LENGTH partial ROM vs full ROM
# Note SMD is NEGATIVE = favoring partial-long over full
PARTIAL_LONG_LENGTH_VS_FULL = EffectEstimate(
    mean=-0.28,
    # NORMAL-APPROXIMATION CAVEAT: the QI (-0.81, 0.16) is an asymmetric
    # Bayesian posterior interval (midpoint -0.325 != mean -0.28). _se_from_qi
    # forces a single symmetric SE, so ci_95 reconstructs ~(-0.765, 0.205),
    # NOT the paper's (-0.81, 0.16). Acceptable for single-SE pooling; do not
    # expect ci_95 to round-trip the paper's interval.
    se=_se_from_qi(-0.81, 0.16),
    n=130,                   # UNVERIFIED — participant count not in article body;
                             # 6 studies. Conservative estimate.
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY * 0.85,    # 0.81 × 0.85 = 0.6885 — subgroup-as-primary penalty
    scale="standardized_mean_diff",
    n_studies=6,
    notes="LENGTHENED partial ROM vs full ROM. SMD -0.28 favoring partials "
          "at long lengths (negative = favors partials). 95% CI: -0.81, 0.16 "
          "— wide and crosses zero. Exploratory 6-study subgroup — the paper "
          "itself says such analyses 'lack the data and statistical power to "
          "make any confident inferences'. Interpret with caution.",
)

# Sub-group: SHORT-LENGTH partial ROM vs full ROM
# RECOVERED 2026-05-17 from the full text (Results, "Muscle Length & Muscle
# Hypertrophy") — the number does exist and is no longer omitted.
PARTIAL_SHORT_LENGTH_VS_FULL = EffectEstimate(
    mean=0.08,
    se=_se_from_qi(-0.24, 0.42),     # = 0.16837; QI mildly skewed (midpoint 0.09)
    n=150,                   # UNVERIFIED — participant count not in article body;
                             # short-length partials touched in ~19/23 studies.
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY * 0.85,    # exploratory subgroup
    scale="standardized_mean_diff",
    notes="SHORT-LENGTH partial ROM vs full ROM, hypertrophy. SMD 0.08 "
          "favoring full ROM (95% QI -0.24, 0.42) — trivial, crosses zero. "
          "This paper's own short-length number does NOT by itself establish "
          "short-length partials as 'clearly inferior'; that framing rests on "
          "the long-vs-short contrast and later literature.",
)


HYPERTROPHY_ESTIMATES: list[EffectEstimate] = [
    PARTIAL_VS_FULL_HYPERTROPHY,
    PARTIAL_LONG_LENGTH_VS_FULL,
    PARTIAL_SHORT_LENGTH_VS_FULL,
]


# ----------------------------------------------------------------------------
# Strength sub-finding
# ----------------------------------------------------------------------------

POPULATION_STRENGTH = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    age_range=(18, 40),
    outcome="strength",
    notes="Wolf 2023 strength outcomes.",
)


PARTIAL_VS_FULL_STRENGTH = EffectEstimate(
    mean=0.14,
    se=_se_from_qi(-0.01, 0.29),
    n=739,                   # participants: 311 fROM + 428 pROM (Table 2, "muscle strength")
    population=POPULATION_STRENGTH,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=24,
    notes="Partial vs full ROM for strength: SMD 0.14 favoring full ROM. "
          "Trivial-to-small. Sub-analyses suggested STRENGTH GAINS ARE GREATEST "
          "IN THE ROM TRAINED — i.e. specificity. If you test strength at full "
          "ROM, full ROM training wins; if you test at partial ROM, partial wins.",
)


STRENGTH_ESTIMATES: list[EffectEstimate] = [PARTIAL_VS_FULL_STRENGTH]


# ----------------------------------------------------------------------------
# Practical guidance
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
ROM choice has trivial-to-small effects on hypertrophy on average. Don't
penalize an exercise based on whether it uses full or partial ROM, as long
as the partial ROM is at long muscle lengths.

Short-length partials (e.g., top-half squats, top-half pushdowns) lean
toward inferior for hypertrophy, but Wolf 2023's own short-length estimate
is only a trivial SMD 0.08 (95% CI -0.24, 0.42). The "inferior" view rests
on the contrast between the short-length (+0.08, favours full) and
long-length (-0.28, favours partial) sub-groups plus the Discussion
narrative — not on a single decisive number. The optimizer may mildly
down-weight exercises that fundamentally train at short lengths for a
hypertrophy goal, but should not treat them as strongly inferior.

For strength: train through the ROM you're being tested on, or close to it.
This is the 'specificity principle' applied to ROM.
"""
