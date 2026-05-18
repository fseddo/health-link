"""
Schoenfeld BJ, Ogborn D, Krieger JW.
Dose-response relationship between weekly resistance training volume and
increases in muscle mass: A systematic review and meta-analysis.
Journal of Sports Sciences. 2017;35(11):1073-1082.
doi: 10.1080/02640414.2016.1210197

KEY FINDINGS (meta-regression; 34 treatment groups from 15 studies, n=418):

  Continuous: each added weekly set per muscle -> +0.023 SMD
              (95% CI 0.010-0.036, P=0.002), equivalent to +0.37% muscle size.
  Higher-vs-lower volume within studies: SMD 0.241 (95% CI 0.026-0.457,
              P=0.03), equivalent to a +3.9% gain difference.
  Three-tier (context, not encoded): mean ES 0.307 / 0.378 / 0.520 for
              <5 / 5-9 / 10+ weekly sets per muscle — the paper reports this
              categorical analysis as a non-significant TREND (P=0.074), so
              treat the monotonic pattern as suggestive, not established.

A graded dose-response: more weekly sets -> more hypertrophy, no plateau
detected in the studied range (data thin out above ~12 sets/muscle/week).

----------------------------------------------------------------------------
WHY THIS IS NOT POOLABLE WITH PELLAND 2026
----------------------------------------------------------------------------

Both papers answer the same QUESTION (volume -> hypertrophy dose-response),
so the registry files them under the same Topic. But their headline estimates
are NOT on a common scale and must not be combined by inverse-variance
pooling:

  - Scale: Schoenfeld reports a standardized-mean-difference slope per set
    (SMD/set); Pelland reports a percentage slope (% per set). The "+0.37%"
    Schoenfeld quotes is a derived equivalent, not the primary metric.
  - Set counting: Schoenfeld counts raw direct sets per muscle. Pelland counts
    FRACTIONAL sets (indirect work x 0.5). The denominators differ.
  - Model form: Schoenfeld fits a LINEAR meta-regression slope. Pelland fits a
    square-root curve with diminishing returns and reports the marginal slope
    at the mean volume. A linear slope and a marginal slope are not the same
    quantity.

So Schoenfeld 2017 is encoded as DIRECTIONAL CORROBORATION of Pelland — a
second, older, independent meta-analysis pointing the same way — not as a
poolable estimate. The registry keeps it out of the volume->hypertrophy pool
via _POOLABLE_OVERRIDE. Harmonizing the two would require re-counting every
Schoenfeld study's volume fractionally; that is deliberately not attempted.

----------------------------------------------------------------------------
TWO CAVEATS WORTH CARRYING
----------------------------------------------------------------------------

1. One influential study. Sensitivity analysis (removing Radaelli, Fleck
   et al. 2014) nearly HALVES the continuous slope, 0.023 -> 0.013, and drops
   the higher-vs-lower contrast 0.241 -> 0.147. The dose-response direction
   survives; its magnitude does not. Both estimates' notes record this.
2. Measurement heterogeneity. A meaningful share of included studies used
   whole-body measures (DXA, BodPod). Schoenfeld's own interaction analysis
   found the volume effect was carried by the direct-measurement (MRI /
   ultrasound) studies (slope 0.023, CI 0.009-0.037) and was ~null for
   indirect measures (slope 0.006). The encoded slope is the overall one; the
   direct-measurement reading is the one to trust. (The paper prints the
   indirect-measures CI as "-0.023, 0.12"; that upper bound is almost
   certainly a typo in the paper — implausibly wide and asymmetric around
   0.006 — so it is not reproduced as a usable number here.)
"""

from __future__ import annotations

from .shared import Citation, PopulationSpec, EffectEstimate


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Schoenfeld et al.",
    year=2017,
    doi="10.1080/02640414.2016.1210197",
    journal="Journal of Sports Sciences",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Study design     0.72 (meta-analysis of experimental controlled trials:
#                  mostly parallel RCTs + 2 randomized within-participant
#                  contralateral trials, NOT pre-registered. Deliberate
#                  deviation from the rubric's "score by worst included tier"
#                  rule: the 2 within-participant studies are well-controlled
#                  randomized contralateral designs, NOT the 0.5 "side-to-side
#                  with confounds" tier — cf. the Maeo 2023 precedent.)
# Sample size      0.80 (418 pooled participants — rubric's 300-499 MA band)
# Measurement      0.70 (MIXED: MRI / ultrasound but also DXA / BodPod / biopsy;
#                  the paper itself shows indirect measures gave a ~null slope)
# Methodological   0.80 (robust-variance meta-regression, BIC model reduction,
#                  interaction + sensitivity analyses; no pre-reg)
# Reporting        0.80 (full effect sizes with SEM, 95% CIs, forest plot,
#                  tables; no raw-data / code deposit — it is a 2016 paper)
# Risk of bias     0.82 ("no conflict of interest reported"; authors are
#                  industry-adjacent — rubric says don't penalise that alone)
# Population       0.60 (very heterogeneous: untrained + trained, young +
#                  middle-aged + elderly, M/F/mixed; heterogeneity WAS analysed
#                  via interactions, all non-significant)
# Weighted average: 0.746 -> 0.75. No flat modifiers (no I^2 reported, so the
# heterogeneity modifier cannot be applied; the single-influential-study
# fragility is documented in the estimate notes rather than scored).
QUALITY = 0.75


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------

POPULATION = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    # Studied population spans young (18-29), middle-aged and elderly (50+)
    # adults; only ~3 of 15 studies used trained participants. age_range is the
    # envelope of the included studies, not a single tight cohort.
    age_range=(18, 70),
    outcome="hypertrophy",
    notes="Schoenfeld 2017 meta-analysis: 15 studies / 34 treatment groups / "
          "418 participants. Heterogeneous — mostly untrained, all ages, "
          "both sexes.",
)


# ----------------------------------------------------------------------------
# Effect estimates
# ----------------------------------------------------------------------------
# Both SEs below are read directly off the paper's Table 2 (printed there as
# "ES +/- SEM"); no recovery from a CI or p-value was needed. Note
# EffectEstimate.ci_95 reconstructs a Normal mean +/- 1.96*se interval, which
# is slightly NARROWER than the paper's robust-variance small-sample
# t-intervals. This applies to BOTH estimates:
#   - slope:       ci_95 gives ~0.011-0.035  vs the paper's 0.010-0.036
#   - high-vs-low: ci_95 gives ~0.043-0.439  vs the paper's 0.026-0.457
# Each estimate's `notes` quotes the paper's (wider) t-interval; ci_95 returns
# the Normal approximation. Acceptable for pooling — just don't expect ci_95
# to round-trip the paper's printed CI.

VOLUME_HYPERTROPHY_SLOPE = EffectEstimate(
    mean=0.023,
    se=0.006,                       # reported SEM (Table 2)
    n=418,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="smd_per_set",            # distinct scale — see module docstring;
                                    # deliberately NOT poolable with Pelland
    n_studies=15,
    notes="Continuous meta-regression: each added weekly set per muscle -> "
          "+0.023 SMD (95% CI 0.010-0.036, P=0.002), equivalent to +0.37% "
          "muscle size per set. NOT poolable with Pelland 2026's volume slope "
          "(different scale, raw vs fractional set counting, linear vs "
          "square-root model — see module docstring). Sensitivity: removing "
          "the one influential study (Radaelli, Fleck 2014) nearly halves the "
          "slope to 0.013 (95% CI 0.004-0.021, P=0.008).",
)

VOLUME_HYPERTROPHY_HIGH_VS_LOW = EffectEstimate(
    mean=0.241,
    se=0.101,                       # reported SEM (Results; forest plot Fig. 2)
    n=418,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=15,
    notes="Within-study higher- vs lower-volume contrast: SMD 0.241 "
          "(95% CI 0.026-0.457, P=0.03), equivalent to a +3.9% gain "
          "difference favouring higher volume. 'Higher' / 'lower' are "
          "study-relative, not fixed set counts. Sensitivity: removing "
          "Radaelli, Fleck 2014 drops it to 0.147 (95% CI 0.033-0.261, P=0.016).",
)

VOLUME_HYPERTROPHY_ESTIMATES: list[EffectEstimate] = [
    VOLUME_HYPERTROPHY_SLOPE,
    VOLUME_HYPERTROPHY_HIGH_VS_LOW,
]


# ----------------------------------------------------------------------------
# Practical guidance
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
Volume and hypertrophy are graded: more weekly sets per muscle produce more
growth, with no plateau detected in the studied range (data thin out above
~12 sets/muscle/week, so the upper bound is genuinely unknown). Schoenfeld
2017 suggests >=10 direct weekly sets per muscle to maximise growth, while
noting that substantial hypertrophy is still achievable at <=4 sets — useful
for time-constrained users.

This is a SECOND, older, independent source on volume -> hypertrophy. It
corroborates Pelland 2026 directionally but is encoded on a different scale
and must NOT be pooled with Pelland numerically (see the estimate notes and
module docstring). Use it as a cross-check.

Caveat: weight the direct-measurement (MRI / ultrasound) reading — Schoenfeld's
own interaction analysis found the volume effect was ~null for the whole-body
(DXA / BodPod) studies.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    _e0 = VOLUME_HYPERTROPHY_SLOPE
    print(f"Schoenfeld 2017 — quality {QUALITY}, "
          f"n={_e0.n} participants across {_e0.n_studies} studies")
    for e in VOLUME_HYPERTROPHY_ESTIMATES:
        lo, hi = e.ci_95
        print(f"  {e.scale:<24} mean={e.mean:+.3f}  "
              f"(95% CI {lo:+.3f}, {hi:+.3f})  n_studies={e.n_studies}")
