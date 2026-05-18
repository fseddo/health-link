"""
Singer A, Wolf M, Generoso L, Arias E, Delcastillo K, Echevarria E,
Martinez A, Androulakis Korakakis P, Refalo MC, Swinton PA, Schoenfeld BJ.
"Give it a rest: a systematic review with Bayesian meta-analysis on the
effect of inter-set rest interval duration on muscle hypertrophy."
Frontiers in Sports and Active Living. 2024;6:1429789.
doi: 10.3389/fspor.2024.1429789 · PMID: 39205815
Open-access full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC11349676/
Preregistration: https://osf.io/ywevc

KEY FINDINGS (Bayesian meta-analysis; 9 RCTs, 19 effect measurements,
185 total participants):

The encodable estimates are the BETWEEN-CONDITION (controlled) binary
contrasts — short rest (<=60 s) vs longer rest (>60 s) — the actual effect of
rest-interval duration on hypertrophy, separated by body region. A POSITIVE
SMD favours LONGER rest.

  Arm hypertrophy (6 effect measurements):
      SMD  0.13 (95% CrI -0.27 to 0.51)  — central estimate favours longer rest
  Thigh hypertrophy (10 effect measurements):
      SMD  0.17 (95% CrI -0.13 to 0.43)  — central estimate favours longer rest
  Whole-body / fat-free-mass (3 effect measurements):
      SMD -0.08 (95% CrI -0.45 to 0.29)  — central estimate slightly favours
                                           shorter rest (opposite direction)

All three credible intervals comfortably cross zero. The multivariate model
gave very similar numbers (arm 0.11, thigh 0.16, whole body 0.03). The paper's
overall conclusion: a SMALL benefit at most to longer rest for limb
hypertrophy, with "no appreciable differences in hypertrophy when resting
>90 s between sets", and substantial residual uncertainty.

----------------------------------------------------------------------------
WHAT IS DELIBERATELY NOT ENCODED
----------------------------------------------------------------------------

The paper also reports WITHIN-CONDITION pre-to-post (non-controlled) SMDs:
  Binary:  short rest 0.48 (0.19-0.81),  longer rest 0.56 (0.24-0.86)
  Four-tier: short 0.47, intermediate 0.65, long 0.55, very long 0.50.
These describe how much each rest-length GROUP grew over the training period.
They are NOT a contrast between rest lengths — both groups grew, which only
confirms that resistance training causes hypertrophy. They are NOT the
rest-interval effect and are NOT encoded as EffectEstimates. The encodable
rest-interval effect is the between-condition difference, above.

----------------------------------------------------------------------------
WHY THE THREE REGION ESTIMATES ARE NOT POOLED INTO ONE NUMBER
----------------------------------------------------------------------------

The paper itself never pools arm + thigh + whole-body into a single SMD; it
deliberately models them region-by-region. Two reasons the registry follows
that choice and keeps them OUT of one inverse-variance pool (see
`poolable_estimates()` and the `_POOLABLE_OVERRIDE` in registry.py):

  1. The whole-body estimate points the OPPOSITE way (-0.08) to arm and thigh
     (+0.13, +0.17). Inverse-variance pooling three estimates that disagree in
     SIGN manufactures a near-zero "average" that represents none of them and
     hides the region heterogeneity the paper was built to expose.
  2. The whole-body outcome is a different MEASUREMENT construct — it is
     dominated by fat-free-mass methods (DXA, hydrodensitometry, bioelectrical
     impedance) rather than the site-specific MRI/ultrasound that underlie the
     arm and thigh estimates, and rests on only 3 effect measurements.

Arm and thigh ARE commensurable with each other (same scale, same sign, both
site-specific limb hypertrophy), so the module's poolable set is {arm, thigh}.
Whole body is exported for inspection/display but excluded from the pool. This
is a WITHIN-PAPER override, analogous to load->strength carrying 1RM +
isometric as different outcomes.

----------------------------------------------------------------------------
CAVEATS
----------------------------------------------------------------------------

1. Bayesian-credible-interval asymmetry. The CrIs are posterior intervals and
   may be mildly asymmetric; `_se_from_qi` forces a single symmetric SE, so
   `ci_95` will not round-trip the paper's CrI exactly. Same caveat as
   `wolf_2023.PARTIAL_LONG_LENGTH_VS_FULL`. Acceptable for inverse-variance
   pooling.
2. Mostly UNTRAINED, mostly MALE. 6 of 9 studies untrained, 3 trained;
   6 of 9 male-only. PopulationSpec is "mixed" / "mixed" accordingly. The
   rest-interval effect could differ in trained lifters (intuitively, longer
   rest matters more once loads are heavier), but this paper cannot resolve
   that — its trained-subgroup data are too thin.
3. Region participant counts are UNVERIFIED. Table 1 reports per-study totals
   (185 across 9 studies) but not a per-region participant breakdown. The `n`
   on each estimate is a documented approximation derived from the effect-
   measurement split (arm 60 / thigh 100 / whole-body 45); these sum to 205,
   which exceeds 185 by design because a participant contributes effect
   measurements to more than one region.
4. No strength outcomes. This paper analyses hypertrophy only — it does not
   inform a rest-interval->strength Topic, which remains a coverage Gap.

WHY THIS MATTERS FOR THE FITNESS APP:

This closes the hypertrophy half of the rest-interval coverage Gap. For the
optimizer: rest-interval duration is a near-trivial lever for limb
hypertrophy. Do not heavily penalise a short-rest prescription, but a mild
preference for >=90-120 s rest on compound limb work is directionally
supported and costs nothing. Do not encode a strong rest-interval effect.
"""

from __future__ import annotations

from .shared import Citation, PopulationSpec, EffectEstimate


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Singer et al.",
    year=2024,
    doi="10.3389/fspor.2024.1429789",
    journal="Frontiers in Sports and Active Living",
    osf_url="https://osf.io/ywevc",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Study design     0.80 (systematic review / meta-analysis of RCTs with a
#                  PRE-REGISTERED protocol — the rubric's 0.80 tier exactly.
#                  Included trials are controlled resistance-training RCTs;
#                  none drop to the within-subject-with-confounds tier.)
# Sample size      0.70 (185 pooled participants — rubric's 150-299 MA band.
#                  Only 9 RCTs and 19 effect measurements; small for a MA.)
# Measurement      0.60 (MIXED and partly weak: site-specific MRI/ultrasound
#                  for limbs but the whole-body outcome leans on DXA / BIA /
#                  hydrodensitometry FFM and one study used circumference /
#                  biopsy. Averages below the site-specific tier.)
# Methodological   1.00 (pre-registered on OSF, hierarchical Bayesian models
#                  with informative priors, univariate + multivariate
#                  specifications, region-stratified analysis, funnel plot —
#                  the rubric's top tier.)
# Reporting        0.90 (full credible intervals for every estimate, region
#                  breakdown, tau reported, OSF preregistration; no separate
#                  raw-data/code deposit beyond the registration page.)
# Risk of bias     0.85 ("no financial support" declared; one author
#                  (Schoenfeld) FORMERLY served on the Tonal Corporation
#                  scientific advisory board — a disclosed past tie, not a
#                  conflict on this rest-interval finding; funnel plot showed
#                  no evidence of small-study bias.)
# Population       0.60 (heterogeneous: 6 untrained / 3 trained studies;
#                  6 male-only, 1 female-only, 1 mixed, 1 unspecified; 8 young
#                  + 1 elderly. Described per study but pooled across a wide,
#                  predominantly untrained-and-male mix.)
# Weighted average:
#   0.80*0.20 + 0.70*0.15 + 0.60*0.20 + 1.00*0.15 + 0.90*0.10
#   + 0.85*0.10 + 0.60*0.10
#   = 0.160 + 0.105 + 0.120 + 0.150 + 0.090 + 0.085 + 0.060 = 0.770
# Flat modifiers: NONE. The body-region grouping (arm / thigh / whole-body) is
#   the paper's natural reporting axis for the rest-interval effect, not a
#   post-hoc data-driven subgroup, so the subgroup-as-primary x0.85 modifier is
#   judged not to apply. (The OSF preregistration page could not be retrieved to
#   confirm the region stratification was specified a priori; this decision
#   rests on the model-agnostic judgement above, not on the prereg.) The paper
#   reports between-study SD (tau ~0.08-0.17), not I^2, so the I^2 > 75%
#   heterogeneity modifier cannot be evaluated and is not applied.
QUALITY = 0.77


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------
# One PopulationSpec — every encoded estimate is a hypertrophy outcome.

POPULATION = PopulationSpec(
    training_status="mixed",     # 6 untrained + 3 trained studies
    sex="mixed",                 # 6 male-only, 1 female-only, 1 mixed, 1 n/a
    age_range=(18, 70),          # 8 studies young adults (18-35); 1 study >65
    outcome="hypertrophy",
    notes="Singer 2024 meta-analysis: 9 RCTs, 19 effect measurements, "
          "185 participants. Predominantly untrained and male; mostly young "
          "adults with one elderly study.",
)


# ----------------------------------------------------------------------------
# SE recovery
# ----------------------------------------------------------------------------
# Each estimate is a Bayesian posterior mean with a 95% credible interval.
# A symmetric SE is recovered as (high - low) / (2 * 1.96) — the same
# `_se_from_qi` approach used in wolf_2023.py. CAVEAT: the CrIs are posterior
# intervals and may be mildly asymmetric; this forces a single symmetric SE,
# so EffectEstimate.ci_95 will not round-trip the paper's printed CrI exactly.

def _se_from_cri(low: float, high: float) -> float:
    """Recover a symmetric SE from a 95% (credible) interval."""
    return (high - low) / (2 * 1.96)


# ----------------------------------------------------------------------------
# Effect estimates — between-condition (controlled) binary SMDs
# ----------------------------------------------------------------------------
# Contrast: short rest (<=60 s) vs longer rest (>60 s). Positive SMD = longer
# rest favoured. Univariate binary controlled analysis (Table / forest plot).
# The multivariate model gave very similar values (arm 0.11, thigh 0.16,
# whole body 0.03); the univariate binary estimate is the headline one encoded.

REST_INTERVAL_ARM_HYPERTROPHY = EffectEstimate(
    mean=0.13,
    se=_se_from_cri(-0.27, 0.51),    # = 0.19898
    n=60,                    # UNVERIFIED — region participant count not broken
                             # out in Table 1 (only per-study totals, 185 across
                             # 9 studies). 6 of 19 effect measurements are arm;
                             # ~60 is a conservative documented approximation.
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=9,             # paper-level RCT count; arm outcomes use a subset
                             # of the 9. Pooling arm+thigh sums this to 18,
                             # overstating unique studies — a display-only
                             # artifact; n_studies feeds no pooling weight.
    notes="Arm hypertrophy: short rest (<=60 s) vs longer rest (>60 s), "
          "controlled binary contrast. SMD +0.13 favouring LONGER rest "
          "(95% CrI -0.27 to 0.51 — crosses zero, trivial). 6 effect "
          "measurements (elbow flexors/extensors). Multivariate model gave "
          "0.11. POOLABLE with the thigh estimate (same scale, same sign, "
          "site-specific limb hypertrophy); NOT with whole body. Bayesian "
          "CrI is a posterior interval — ci_95 (symmetric) will not round-trip "
          "it exactly. n is UNVERIFIED — see field comment.",
)

REST_INTERVAL_THIGH_HYPERTROPHY = EffectEstimate(
    mean=0.17,
    se=_se_from_cri(-0.13, 0.43),    # = 0.14286
    n=100,                   # UNVERIFIED — region participant count not broken
                             # out in Table 1. 10 of 19 effect measurements are
                             # thigh; ~100 is a conservative documented
                             # approximation scaled from the 185 total.
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=9,             # paper-level RCT count (see arm estimate); thigh
                             # outcomes use a subset of the 9.
    notes="Thigh hypertrophy: short rest (<=60 s) vs longer rest (>60 s), "
          "controlled binary contrast. SMD +0.17 favouring LONGER rest "
          "(95% CrI -0.13 to 0.43 — crosses zero, trivial-to-small). 10 effect "
          "measurements (quadriceps/hamstrings) — the best-evidenced region. "
          "Multivariate model gave 0.16. POOLABLE with the arm estimate; NOT "
          "with whole body. Bayesian CrI is a posterior interval — ci_95 "
          "(symmetric) will not round-trip it exactly. n is UNVERIFIED — see "
          "field comment.",
)

REST_INTERVAL_WHOLE_BODY_HYPERTROPHY = EffectEstimate(
    mean=-0.08,
    se=_se_from_cri(-0.45, 0.29),    # = 0.18878
    n=45,                    # UNVERIFIED — region participant count not broken
                             # out in Table 1. Only 3 of 19 effect measurements
                             # are whole-body; ~45 is a conservative documented
                             # approximation.
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=9,             # paper-level RCT count (see arm estimate);
                             # whole-body outcomes use a subset of the 9.
    notes="Whole-body / fat-free-mass hypertrophy: short rest (<=60 s) vs "
          "longer rest (>60 s), controlled binary contrast. SMD -0.08 — the "
          "ONLY region pointing toward SHORTER rest (95% CrI -0.45 to 0.29 — "
          "crosses zero, trivial). Only 3 effect measurements, and the outcome "
          "is dominated by whole-body FFM methods (DXA / hydrodensitometry / "
          "bioelectrical impedance), a different and weaker measurement "
          "construct than the site-specific arm/thigh estimates. DELIBERATELY "
          "EXCLUDED from the inverse-variance pool — see module docstring and "
          "poolable_estimates(). Multivariate model gave +0.03. n is "
          "UNVERIFIED — see field comment.",
)


# Every encoded EffectEstimate, indexed by the registry under
# Topic.REST_INTERVAL_HYPERTROPHY. Includes the whole-body estimate so it is
# visible in effects() for inspection; poolable_estimates() drops it.
HYPERTROPHY_ESTIMATES: list[EffectEstimate] = [
    REST_INTERVAL_ARM_HYPERTROPHY,
    REST_INTERVAL_THIGH_HYPERTROPHY,
    REST_INTERVAL_WHOLE_BODY_HYPERTROPHY,
]


def poolable_estimates() -> list[EffectEstimate]:
    """The apples-to-apples subset of HYPERTROPHY_ESTIMATES for
    inverse-variance pooling: arm + thigh only.

    The whole-body estimate is excluded — it points the opposite way (-0.08 vs
    +0.13 / +0.17), rests on a different measurement construct (whole-body FFM
    rather than site-specific limb hypertrophy), and is built on only 3 effect
    measurements. Pooling three sign-disagreeing estimates would manufacture a
    near-zero average that represents none of them. See the module docstring.
    """
    return [REST_INTERVAL_ARM_HYPERTROPHY, REST_INTERVAL_THIGH_HYPERTROPHY]


# ----------------------------------------------------------------------------
# Practical guidance
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
Inter-set rest-interval duration is a near-trivial lever for muscle
hypertrophy. Singer 2024 (9 RCTs) found, for the contrast short rest (<=60 s)
vs longer rest (>60 s):
  - limb hypertrophy (arm SMD +0.13, thigh SMD +0.17) trivially favours
    longer rest;
  - whole-body / fat-free-mass hypertrophy trivially favours shorter rest
    (SMD -0.08);
  - every credible interval crosses zero.

The paper found no appreciable additional benefit beyond ~90 s of rest. So:
  - Do NOT heavily penalise a short-rest prescription for a hypertrophy goal —
    the cost is trivial.
  - A MILD preference for >=90-120 s rest on heavier compound limb work is
    directionally supported and essentially free; longer rest also preserves
    per-set performance, which feeds volume.
  - Do not encode rest interval as a strong driver of growth, and do not let
    it outweigh volume, proximity-to-failure, or exercise selection.

Caveat: the evidence base is mostly untrained and mostly male. In trained
lifters longer rest may matter somewhat more (heavier loads, slower
recovery), but this paper cannot resolve that. There is no rest-interval
evidence for STRENGTH in the layer at all.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Singer 2024 — quality {QUALITY}, "
          f"9 RCTs, 19 effect measurements, n=185 participants")
    for e in HYPERTROPHY_ESTIMATES:
        lo, hi = e.ci_95
        print(f"  {e.notes.split(':')[0]:<28} mean={e.mean:+.3f}  "
              f"se={e.se:.4f}  (95% CI {lo:+.3f}, {hi:+.3f})")
    pool = poolable_estimates()
    print(f"  poolable set: {len(pool)} of {len(HYPERTROPHY_ESTIMATES)} "
          f"(arm + thigh; whole-body excluded)")
    assert len(pool) == 2
    assert REST_INTERVAL_WHOLE_BODY_HYPERTROPHY not in pool
    assert all(e.se > 0 for e in HYPERTROPHY_ESTIMATES)
    print("  sanity checks passed.")
