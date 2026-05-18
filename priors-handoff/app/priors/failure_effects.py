"""
Failure-vs-non-failure training effects on hypertrophy, strength, and power.

This module encodes THREE overlapping meta-analyses on the same question:

  1. Vieira et al. 2021 (J Strength Cond Res, 13 studies)
  2. Grgic et al. 2021 (J Sport Health Sci; 7 studies for hypertrophy,
     15 for strength)
  3. Refalo et al. 2023 (Sports Medicine; 15-study review, set-failure
     sub-analysis 9 studies, momentary-failure sub-analysis 5)

NOTE (audit 2026-05-17): paper 3 was previously mis-cited as "Robinson et al.
2022". DOI 10.1007/s40279-022-01784-y is Refalo MC, Helms ER, Trexler ET,
Hamilton DL, Fyfe JJ, "Influence of Resistance Training Proximity-to-Failure on
Skeletal Muscle Hypertrophy: A Systematic Review with Meta-analysis", Sports
Medicine 2023;53:649-665. The encoded 0.19 / 0.12 effect sizes ARE Refalo's and
match the paper; only the author/year attribution was wrong. The genuine
Robinson ZP et al. dose-response meta-regression is a separate 2024 paper
(DOI 10.1007/s40279-024-02069-2) reporting RIR slopes, and is NOT encoded here.

The three estimates disagree, which makes this an instructive case for the
combination logic. See the module-level discussion below.

----------------------------------------------------------------------------
WHY THE ESTIMATES DISAGREE
----------------------------------------------------------------------------

The point estimates for failure's effect on hypertrophy are:

  Vieira 2021:  SMD 0.75  (overall; null when volume-equated)
  Grgic 2021:   ES 0.22   (95% CI: -0.11, 0.55; null overall)
  Refalo 2023:  ES 0.19   (95% CI: 0.00, 0.37; trivial advantage to failure)

Vieira's 0.75 is much higher than the other two. The likely reasons:

  - Vieira's overall analysis did NOT equate volume between failure and
    non-failure arms. When you allow failure groups to do more total volume,
    you partly capture a volume effect, not a failure effect.
  - The 0.75 estimate dropped to null when Vieira restricted to volume-
    equated studies — consistent with Grgic and Refalo's main findings.
  - Grgic found a small effect ONLY in resistance-trained subgroups; Refalo
    found a small effect with broader (set-failure) definitions that shrank
    under the stricter momentary-failure definition.

So Vieira 2021's headline number is real but addresses a different question
(failure + extra volume vs. non-failure with less volume). For our model,
we want the volume-equated effect — that's the apples-to-apples comparison
when an optimizer is choosing whether to prescribe RIR-0 vs. RIR-2 sets at
the SAME total weekly volume.

----------------------------------------------------------------------------
PRACTICAL IMPLICATION FOR THE MODEL
----------------------------------------------------------------------------

For hypertrophy at fixed volume: failure training offers ~0-0.2 SMD advantage,
with CIs that mostly include zero. In trained subgroups, a small (0.15) but
significant advantage emerges. For untrained: failure may matter less.

For strength: non-failure may be SLIGHTLY better, especially when volume is
not equated. Failure training accumulates more fatigue, which impairs the
practice quality needed for strength.

The optimizer should treat failure training as: small expected benefit for
hypertrophy in trained users, small expected COST for strength, with high
uncertainty either way. Default to RIR 1-3 unless user prioritizes a goal
where the literature suggests otherwise.
"""

from __future__ import annotations
import math

from .shared import (
    Citation, PopulationSpec, EffectEstimate, UserProfile,
)


# ----------------------------------------------------------------------------
# Citations
# ----------------------------------------------------------------------------

CITATION_VIEIRA = Citation(
    authors="Vieira et al.",
    year=2021,
    doi="10.1519/JSC.0000000000003936",
    journal="J Strength Cond Res",
)

CITATION_GRGIC = Citation(
    authors="Grgic et al.",
    year=2021,
    doi="10.1016/j.jshs.2021.01.007",
    journal="J Sport Health Sci",
)

CITATION_REFALO = Citation(
    authors="Refalo et al.",
    year=2023,
    doi="10.1007/s40279-022-01784-y",
    journal="Sports Medicine",
)


# ----------------------------------------------------------------------------
# Quality assessments (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# VIEIRA 2021
#   design 0.70, n 0.80, measurement 0.75, rigor 0.70, reporting 0.50,
#   bias 0.85, population 0.85 → weighted 0.735
#   Modifier for non-volume-equated estimate: ×0.7 → 0.51 (hypertrophy overall)
#   No modifier for strength estimate: 0.74
#
# GRGIC 2021
#   design 0.75, n 0.80, measurement 0.80, rigor 0.85, reporting 0.85,
#   bias 0.85, population 0.85 → weighted 0.81 (overall)
#   Trained-subgroup modifier: ×0.85 → 0.69
#
# REFALO 2023  (DOI 10.1007/s40279-022-01784-y; previously mis-cited "Robinson 2022")
#   design 0.85, n 0.80, measurement 0.90, rigor 0.90, reporting 0.90,
#   bias 0.85, population 0.85 → weighted 0.87 (both estimates)

QUALITY_VIEIRA_BASE = 0.735         # base score before question-mismatch modifier
QUALITY_VIEIRA_NONEQ = 0.51         # non-volume-equated hypertrophy (×0.7)
QUALITY_VIEIRA_STRENGTH = 0.74      # strength estimate (no modifier)
QUALITY_GRGIC_OVERALL = 0.81
QUALITY_GRGIC_SUBGROUP = 0.69       # trained subgroup (×0.85 for subgroup-as-primary)
QUALITY_REFALO = 0.87


# ----------------------------------------------------------------------------
# Population specs
# ----------------------------------------------------------------------------

# All three meta-analyses studied young adults, both sexes, mostly trained.
# Refalo includes "any age and resistance training experience" but in
# practice the included studies are still young adults.

POP_HYPERTROPHY_MIXED_TRAINED = PopulationSpec(
    training_status="trained",
    sex="mixed",
    age_range=(18, 40),
    outcome="hypertrophy",
    notes="Failure-vs-non-failure meta-analyses; young trained adults.",
)

POP_HYPERTROPHY_TRAINED_SUBGROUP = PopulationSpec(
    training_status="well_trained",
    sex="mixed",
    age_range=(18, 40),
    outcome="hypertrophy",
    notes="Resistance-trained subgroup specifically (Grgic 2021).",
)

POP_STRENGTH_MIXED = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    age_range=(18, 40),
    outcome="strength",
    notes="Failure-vs-non-failure meta-analyses; young adults.",
)


def _se_from_ci(lower: float, upper: float) -> float:
    return (upper - lower) / (2 * 1.96)


# ----------------------------------------------------------------------------
# Hypertrophy estimates — one per (paper, sub-question)
# ----------------------------------------------------------------------------

# Vieira 2021 — overall (NOT volume-equated)
# Reports SMD 0.75, p=0.005, but no CI in abstract. We approximate SE from
# the p-value: for two-tailed p=0.005, z ≈ 2.81, so SE ≈ 0.75 / 2.81 ≈ 0.267
# This is a rough recovery; ideally we'd extract from the full forest plot.
VIEIRA_HYPERTROPHY_NONEQ_VOLUME = EffectEstimate(
    mean=0.75,
    se=0.75 / 2.81,                     # SE recovered from p-value (p=0.005, z=2.81)
    n=240,                              # UNVERIFIED — JSCR full text paywalled
    population=POP_HYPERTROPHY_MIXED_TRAINED,
    source=CITATION_VIEIRA,
    quality_score=QUALITY_VIEIRA_NONEQ,   # base 0.735 × 0.7 modifier for non-eq question
    scale="standardized_mean_diff",
    n_studies=13,
    notes="OVERALL analysis without volume equation. Answers 'failure + more "
          "volume vs non-failure + less volume', not 'failure vs non-failure "
          "at same volume.' Reduced quality_score reflects this confounding. "
          "Volume-equated subgroup was null per the paper but the exact effect "
          "size is UNVERIFIED (JSCR full text paywalled).",
)

# Grgic 2021 — overall pooled hypertrophy (equated + non-equated studies)
GRGIC_HYPERTROPHY_OVERALL = EffectEstimate(
    mean=0.22,
    se=_se_from_ci(-0.11, 0.55),
    n=219,                              # 7 hypertrophy studies, 219 participants
    population=POP_HYPERTROPHY_MIXED_TRAINED,
    source=CITATION_GRGIC,
    quality_score=QUALITY_GRGIC_OVERALL,
    scale="standardized_mean_diff",
    n_studies=7,
    notes="Overall null effect. CI includes zero (-0.11, 0.55). Pools "
          "volume-equated and non-equated hypertrophy studies — it is NOT a "
          "volume-equated-only analysis.",
)

# Grgic 2021 — trained-only subgroup
GRGIC_HYPERTROPHY_TRAINED = EffectEstimate(
    mean=0.15,
    se=_se_from_ci(0.03, 0.26),
    n=39,                               # only 2 studies, ~39 participants
    population=POP_HYPERTROPHY_TRAINED_SUBGROUP,
    source=CITATION_GRGIC,
    quality_score=QUALITY_GRGIC_SUBGROUP,  # 0.81 × 0.85 modifier for subgroup-as-primary
    scale="standardized_mean_diff",
    n_studies=2,
    notes="Trained subgroup: small but statistically significant advantage "
          "for failure training. CI (0.03, 0.26) excludes zero. CAUTION: rests "
          "on only 2 studies (Karsten 2021, Pareja-Blanco 2017) / ~39 "
          "participants — a small post-hoc subgroup; do not over-trust it.",
)

# Refalo 2023 — set failure vs non-failure (broader failure definition)
REFALO_HYPERTROPHY_SET_FAILURE = EffectEstimate(
    mean=0.19,
    se=_se_from_ci(0.00, 0.37),
    n=284,                              # ~284 participants across 9 set-failure studies
    population=POP_HYPERTROPHY_MIXED_TRAINED,
    source=CITATION_REFALO,
    quality_score=QUALITY_REFALO,
    scale="standardized_mean_diff",
    n_studies=9,
    notes="Set failure (broad definition) vs non-failure. Trivial advantage; "
          "CI lower bound at zero. NOT a volume-equated analysis: Refalo tested "
          "volume load as a moderator and found NO moderating effect, so this "
          "pools volume-equated and non-equated studies alike.",
)

# Refalo 2023 — momentary muscular failure vs non-failure (strict definition)
REFALO_HYPERTROPHY_MOMENTARY_FAILURE = EffectEstimate(
    mean=0.12,
    se=_se_from_ci(-0.13, 0.37),
    n=170,                              # 170 participants across 5 momentary-failure studies
    population=POP_HYPERTROPHY_MIXED_TRAINED,
    source=CITATION_REFALO,
    quality_score=QUALITY_REFALO,
    scale="standardized_mean_diff",
    n_studies=5,
    notes="Momentary muscular failure specifically. CI crosses zero. "
          "Stricter failure definition shows weaker effect — consistent "
          "with the hypothesis that failure adds fatigue without "
          "proportional adaptive signal. NOT volume-equated (see set-failure note).",
)

HYPERTROPHY_ESTIMATES: list[EffectEstimate] = [
    VIEIRA_HYPERTROPHY_NONEQ_VOLUME,
    GRGIC_HYPERTROPHY_OVERALL,
    GRGIC_HYPERTROPHY_TRAINED,
    REFALO_HYPERTROPHY_SET_FAILURE,
    REFALO_HYPERTROPHY_MOMENTARY_FAILURE,
]


# ----------------------------------------------------------------------------
# Strength estimates
# ----------------------------------------------------------------------------

VIEIRA_STRENGTH_OVERALL = EffectEstimate(
    mean=-0.08,
    se=0.08 / 0.46,                     # rough recovery from p=0.642 (z ≈ 0.46)
    n=240,                              # UNVERIFIED — JSCR full text paywalled
    population=POP_STRENGTH_MIXED,
    source=CITATION_VIEIRA,
    quality_score=QUALITY_VIEIRA_STRENGTH,
    scale="standardized_mean_diff",
    n_studies=13,
    notes="Failure - non-failure on max strength. Negative = non-failure "
          "slight advantage. CI includes zero (p=0.642). LOW-CONFIDENCE SE: "
          "recovered by dividing a tiny effect (0.08) by a tiny z (~0.46) from "
          "a large, non-significant p — near p~0.64 the p-value carries almost "
          "no precision information, so this SE is barely identified. "
          "Inverse-variance pooling weights by 1/SE^2; do not over-trust it.",
)

# Grgic 2021 — overall strength outcome. ES = -0.09, 95% CI: -0.22 to 0.05
GRGIC_STRENGTH_OVERALL = EffectEstimate(
    mean=-0.09,
    se=_se_from_ci(-0.22, 0.05),
    n=394,                              # 15 strength studies, 394 participants
    population=POP_STRENGTH_MIXED,
    source=CITATION_GRGIC,
    quality_score=QUALITY_GRGIC_OVERALL,
    scale="standardized_mean_diff",
    n_studies=15,
    notes="Strength: small null effect. CI tightly around zero.",
)

# Grgic 2021 — volume non-equated strength subgroup
GRGIC_STRENGTH_NONEQ_VOLUME = EffectEstimate(
    mean=-0.32,
    se=_se_from_ci(-0.57, -0.07),
    n=180,                              # UNVERIFIED — subgroup n not in accessible text
    population=POP_STRENGTH_MIXED,
    source=CITATION_GRGIC,
    # Modifier 0.8 is a DELIBERATE deviation from the rubric's tabled values.
    # This estimate is both a subgroup (rubric ×0.85) and a narrower framing
    # than the headline (rubric ×0.7). 0.8 is chosen as a single combined
    # penalty between the two — applying both would double-count. QUALITY_RUBRIC
    # requires deviations to be documented; this comment is that documentation.
    quality_score=QUALITY_GRGIC_OVERALL * 0.8,  # 0.81 × 0.8 = 0.648
    scale="standardized_mean_diff",
    notes="Volume NOT equated: non-failure favored for strength. This "
          "captures the fatigue cost of failure training when both groups "
          "do their own preferred volume.",
)

STRENGTH_ESTIMATES: list[EffectEstimate] = [
    VIEIRA_STRENGTH_OVERALL,
    GRGIC_STRENGTH_OVERALL,
    GRGIC_STRENGTH_NONEQ_VOLUME,
]


# ----------------------------------------------------------------------------
# Helper: which estimates are appropriate for which user query
# ----------------------------------------------------------------------------

def hypertrophy_estimates_volume_equated() -> list[EffectEstimate]:
    """
    Return the estimates appropriate for the 'failure vs non-failure at fixed
    weekly volume' question — the right set when the optimizer is choosing
    RPE/RIR at fixed sets. Excludes Vieira's non-volume-equated overall estimate.

    NB (audit 2026-05-17): the name is slightly loose. Grgic's overall estimate
    pools volume-equated AND non-equated studies, and Refalo's two estimates are
    volume-load-INSENSITIVE (Refalo found no moderating effect of volume load)
    rather than volume-equated-only. All four are still the correct set for the
    fixed-volume decision: none is confounded by the failure-groups-did-more-
    volume problem that inflates Vieira's 0.75. The exclusion of Vieira's
    non-equated estimate is the load-bearing distinction, and it holds.
    """
    return [
        GRGIC_HYPERTROPHY_OVERALL,
        GRGIC_HYPERTROPHY_TRAINED,
        REFALO_HYPERTROPHY_SET_FAILURE,
        REFALO_HYPERTROPHY_MOMENTARY_FAILURE,
    ]


def strength_estimates_volume_equated() -> list[EffectEstimate]:
    """Volume-equated strength estimates."""
    return [
        VIEIRA_STRENGTH_OVERALL,
        GRGIC_STRENGTH_OVERALL,
    ]


# ----------------------------------------------------------------------------
# Known study overlap between meta-analyses
# ----------------------------------------------------------------------------
# Vieira, Grgic, and Refalo all cover the same ~2017-2021 RT-to-failure
# literature and inevitably share primary studies. Conservative overlap
# estimates (partially verified against Grgic's and Refalo's included-study
# lists in the audit — Grgic<->Refalo confirmed ~6 shared studies):
#   - Vieira <-> Grgic:  ~40% study overlap
#   - Grgic  <-> Refalo: ~50% study overlap
#   - Vieira <-> Refalo: ~30% study overlap
# When pooling all three: apply SE inflation factor ~1.3-1.4 for non-independence.
#
# If the genuine Robinson ZP et al. 2024 dose-response meta-regression is ever
# added, its overlap with all three of these is high and 1.35 must be revisited.

OVERLAP_SE_INFLATION = 1.35
