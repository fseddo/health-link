"""
Varovic D, Wolf M, Schoenfeld BJ, Steele J, Grgic J, Mikulic P.
Does Muscle Length Influence Regional Hypertrophy?
A Systematic Review and Meta-Analysis.
International Journal of Sports Medicine. 2025.
doi: 10.1055/a-2615-4935
PMID: 40570881

KEY FINDING (Bayesian meta-analysis of 12 studies on young adults):

When comparing training at LONGER vs SHORTER muscle lengths, the
STANDARDIZED differences in hypertrophy across REGIONS of the same muscle
(proximal, mid-belly, distal) are TRIVIAL:

  Proximal (25%):   SMD: 0.05 (95% QI: -0.07, 0.16)
  Mid-belly (50%):  SMD: 0.07 (95% QI: -0.02, 0.15)
  Distal (75%):     SMD: 0.09 (95% QI: -0.01, 0.19)

Exponentiated log response ratios (% difference):
  Proximal: +0.57% (-1.92%, +3.24%)
  Mid-belly: +1.22% (-0.77%, +3.22%)
  Distal: +1.88% (-0.44%, +4.34%)

CRITICAL CONTEXT — THIS IS A DIFFERENT QUESTION FROM MAEO 2023:

Varovic asks: "When you train at longer muscle lengths, does the muscle grow
MORE AT ONE REGION (proximal/mid/distal) THAN ANOTHER?"
Answer: NO — regional preferential growth from long-length training is trivial.

Maeo asks: "Do exercises that train at longer muscle lengths produce more
WHOLE-MUSCLE GROWTH than exercises at shorter lengths?"
Answer: YES, substantially.

These get conflated in popular fitness discourse. They are different questions
with different answers.

PRACTICAL IMPLICATION:

For your fitness app's exercise selection:
- Use Maeo-style data (whole-muscle differences between exercises) to inform
  exercise-emphasis coefficients for choosing between exercises.
- Do NOT bake in strong "regional growth" coefficients within a muscle based
  on length-of-training assumptions — the regional effects across studies are
  trivial.

POPULATION:
  12 studies, young adults. Mix of trained and untrained.

THIS MODULE PROVIDES:

1. Three EffectEstimate objects (one per region) for the regional length effect.
2. A practical note that emphasis coefficients within sub-muscles should NOT
   be derived from "longer length = more growth in this region" reasoning
   without strong direct evidence.

This is the kind of paper that constrains how the optimizer reasons, even if
it doesn't add many emphasis coefficients directly.
"""

from __future__ import annotations

from .shared import (
    Citation, PopulationSpec, EffectEstimate,
)


# ----------------------------------------------------------------------------
# Citation and quality
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Varovic et al.",
    year=2025,
    doi="10.1055/a-2615-4935",
    journal="International Journal of Sports Medicine",
)

# PREPRINT-VS-PUBLISHED NOTE (audit 2026-05-17): the SportRxiv preprint of this
# work reports LARGER point estimates (SMD 0.10/0.15/0.20) and a more
# "exploratory" conclusion. This module deliberately encodes the peer-reviewed
# PUBLISHED values (SMD 0.05/0.07/0.09); a re-auditor comparing against the
# preprint will see mismatches — the published values are authoritative.

# Per QUALITY_RUBRIC.md v1.0 (re-scored 2026-05-17 — earlier inputs were
# optimistic; see docs/priors/audits/varovic_2025_audit.md):
# Study design       0.75 (meta-analysis of mixed RCT + within-subject designs;
#                    rubric scores by the worst included design tier, and the
#                    included studies grade poor-to-fair on SMART-LD)
# Sample size        0.75 (rubric's meta-analysis column scores TOTAL pooled
#                    PARTICIPANTS, not study count; included studies are small)
# Measurement        0.85 (regional muscle thickness, predominantly ultrasound;
#                    inclusion criteria also allowed CT/MRI; site-specific)
# Methodological     0.95 (Bayesian framework, ROPE analysis, pre-registered,
#                    code on OSF/GitHub — very current methods)
# Reporting          0.95 (full QIs, ROPE, posterior probabilities; data + code)
# Risk of bias       0.85 (some authors do fitness-industry consulting; methods
#                    sound; rubric says don't penalise industry ties alone)
# Population         0.78 (young adults, described; training-status base is
#                    lopsided — see POPULATION note)
# Weighted average: 0.833 → 0.83
QUALITY = 0.83


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------

POPULATION = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    # Paper says "young adults"; underlying study mean ages span ~18.8-27.2 y.
    # Narrowed from an earlier over-wide (18, 35) — 35 is not a paper figure.
    age_range=(18, 30),
    outcome="hypertrophy",
    # CAUTION: "mixed" training status is literally true but LOPSIDED — 11 of
    # the 12 meta-analyzed studies used UNTRAINED participants; only one
    # (Zabaleta-Korta 2023) used trained participants. applicability_to() will
    # apply only the ×0.85 "mixed" penalty for a trained user, which understates
    # the mismatch. Treat this prior as predominantly untrained-derived.
    notes="Varovic 2025 meta-analysis: 12 studies of young adults; training "
          "status nominally mixed but ~11/12 studies untrained.",
)


# ----------------------------------------------------------------------------
# Regional effect estimates
# ----------------------------------------------------------------------------
# Each represents the SMD for the difference in hypertrophy at that anatomical
# region between longer-length vs shorter-length training conditions.
# 95% Quantile Intervals from the Bayesian posterior.

def _se_from_qi(low: float, high: float) -> float:
    """Approximate SE from 95% QI assuming symmetric posterior."""
    return (high - low) / (2 * 1.96)


REGIONAL_HYPERTROPHY_PROXIMAL = EffectEstimate(
    mean=0.05,
    se=_se_from_qi(-0.07, 0.16),    # ≈ 0.0587
    # n is PARTICIPANTS (shared.py contract). The true pooled participant count
    # is UNVERIFIED — the published full text is paywalled and the OSF data was
    # not accessed. 150 is a deliberately conservative lower-bound estimate so
    # best_applicable()'s sqrt(n) weighting under- rather than over-weights this
    # prior. n_studies carries the verified study count (12).
    n=150,
    n_studies=12,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="Regional hypertrophy advantage at PROXIMAL site (25% muscle length) "
          "for long-length vs short-length training. SMD 0.05 — trivial. "
          "95% QI crosses zero. Exponentiated lnRR: +0.57% (-1.92%, +3.24%).",
)

REGIONAL_HYPERTROPHY_MIDBELLY = EffectEstimate(
    mean=0.07,
    se=_se_from_qi(-0.02, 0.15),   # ≈ 0.0434
    n=150,                           # PARTICIPANTS — conservative estimate; see PROXIMAL note
    n_studies=12,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="Regional hypertrophy advantage at MID-BELLY (50% muscle length) "
          "for long-length training. SMD 0.07 — trivial. "
          "Exponentiated lnRR: +1.22% (-0.77%, +3.22%).",
)

REGIONAL_HYPERTROPHY_DISTAL = EffectEstimate(
    mean=0.09,
    se=_se_from_qi(-0.01, 0.19),   # ≈ 0.0510
    n=150,                           # PARTICIPANTS — conservative estimate; see PROXIMAL note
    n_studies=12,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="Regional hypertrophy advantage at DISTAL site (75% muscle length) "
          "for long-length training. SMD 0.09 — trivial (largest of the three). "
          "Exponentiated lnRR: +1.88% (-0.44%, +4.34%). "
          "Slight trend toward distal favoring, but uncertain.",
)


REGIONAL_ESTIMATES: list[EffectEstimate] = [
    REGIONAL_HYPERTROPHY_PROXIMAL,
    REGIONAL_HYPERTROPHY_MIDBELLY,
    REGIONAL_HYPERTROPHY_DISTAL,
]


# ----------------------------------------------------------------------------
# Practical guidance derived from this paper
# ----------------------------------------------------------------------------
# This is a HEURISTIC, not data, but it follows directly from the meta-
# analysis findings:

GUIDANCE_FOR_OPTIMIZER = """
Do not assign emphasis coefficients to specific REGIONS of a muscle (e.g.,
"upper chest" vs "lower chest", "proximal biceps" vs "distal biceps") based
purely on training-length theory. The Varovic 2025 meta-analysis shows that
the regional advantage of long-length training is trivial (SMDs 0.05-0.09)
with credible intervals that mostly cross zero.

If a user asks about "growing the lower lats" or "upper chest emphasis",
respond with appropriate uncertainty: there is some emerging evidence for
exercise-specific regional bias, but the meta-analytic effect is small and
direct experimental evidence within most muscle groups is limited.
"""
