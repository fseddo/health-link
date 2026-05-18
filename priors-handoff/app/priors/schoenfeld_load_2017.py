"""
Schoenfeld BJ, Grgic J, Ogborn D, Krieger JW.
Strength and Hypertrophy Adaptations Between Low- vs. High-Load Resistance
Training: A Systematic Review and Meta-analysis.
Journal of Strength and Conditioning Research. 2017;31(12):3508-3523.
doi: 10.1519/JSC.0000000000002200
PMID: 28834797

NOT to be confused with schoenfeld_2017.py — that module encodes the VOLUME
dose-response meta-analysis (Schoenfeld, Ogborn & Krieger 2017, J Sports Sci).
This module encodes the LOAD / rep-range meta-analysis (Schoenfeld, GRGIC,
Ogborn & Krieger 2017, JSCR). Different paper, same year, overlapping authors.

KEY FINDINGS (meta-analysis of 21 studies; load = high >60% 1RM vs low <=60%
1RM, ALL sets taken to momentary muscular failure):

  Study-level effect size of HIGH vs LOW load (positive favours HIGH load):

    1RM (dynamic) strength: ES 0.58 (95% CI 0.28-0.89), p=0.002 — 14 studies.
                            HIGH load clearly better for maximal 1RM.
    Isometric strength:     ES 0.16 (95% CI -0.06 to 0.37 per Figure 3),
                            p=0.19 — 8 studies. No significant load effect.
    Muscle hypertrophy:     ES 0.03 (95% CI -0.16 to 0.22 per Figure 4),
                            p=0.56 — 10 studies. No load effect on hypertrophy;
                            growth is equivalent across the loading spectrum.

  NOTE — this paper is internally inconsistent on two CIs: the Results TEXT and
  the FOREST PLOTS disagree for isometric (text -0.10 to 0.41 vs Figure 3
  -0.06 to 0.37) and hypertrophy (text -0.08 to 0.14 vs Figure 4 -0.16 to
  0.22). 1RM is consistent. The effect-estimate comments below explain how
  each SE is set in light of this.

  Per-load absolute effect sizes (context, not encoded): 1RM high 1.69 / low
  1.32 (both large; +35.3% vs +28.0%); hypertrophy high 0.53 / low 0.42
  (+8.3% vs +7.0%).

The headline for a progression model: when sets are taken to failure,
HYPERTROPHY is load-independent (train any rep range), but maximal 1RM
STRENGTH favours heavy load (specificity — 1RM testing rewards training near
the 1RM). Isometric strength sits in between and is not load-sensitive.

----------------------------------------------------------------------------
TWO CAVEATS WORTH CARRYING
----------------------------------------------------------------------------

1. "To failure" is a hard scope limit. EVERY included study took all sets to
   momentary muscular failure. These results say nothing about load when sets
   are stopped short of failure — the paper is explicit that submaximal,
   non-failure training cannot be assumed to behave the same way.

2. The hypertrophy null is robust but the mean-ES trend was load-sensitive.
   The mean-ES analysis showed a non-significant trend (p=0.10) toward high
   load; the STUDY-LEVEL analysis (encoded here) was flatly null (ES 0.03,
   p=0.56); and sensitivity analysis found 5 influential studies — removing
   the 3 most influential pushed even the trend to p=0.22-0.46. The encoded
   study-level ES of 0.03 is the most conservative, most defensible reading.

----------------------------------------------------------------------------
SCALE / POOLABILITY
----------------------------------------------------------------------------

All three estimates are study-level standardized mean differences (high vs
low load). The 1RM and isometric estimates both concern "strength" but are
DIFFERENT outcomes — the paper's whole point is that load affects them
differently — so they must NOT be inverse-variance pooled with each other.
The registry files both under one topic (load -> strength) but a
_POOLABLE_OVERRIDE designates the 1RM estimate as the poolable representative.
"""

from __future__ import annotations

from .shared import Citation, PopulationSpec, EffectEstimate


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Schoenfeld, Grgic et al.",
    year=2017,
    doi="10.1519/JSC.0000000000002200",
    journal="Journal of Strength and Conditioning Research",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Study design     0.72 (meta-analysis of mostly-randomized controlled trials,
#                  a few within-participant designs; NOT pre-registered.
#                  PEDro quality of the pool: mean 5.6, "good to excellent".)
# Sample size      0.75 (per-analysis participant totals span ~176 [isometric,
#                  8 studies] to ~497 [1RM, 14 studies] — rubric's 0.7-0.8 MA
#                  band; the hypertrophy analysis is ~231)
# Measurement      0.85 (the hypertrophy estimate uses DIRECT measures only —
#                  MRI/CT/ultrasound; 1RM is direct dynamic testing; isometric
#                  is MVC. Body-composition/DXA studies were a separate,
#                  un-modelled analysis, so they do not dilute these estimates.)
# Methodological   0.80 (robust-variance meta-regression, PEDro assessment,
#                  sensitivity + interaction analyses; no pre-registration)
# Reporting        0.80 (full effect sizes with SEM and 95% CIs, three forest
#                  plots, sensitivity tables; no raw-data/code deposit)
# Risk of bias     0.80 (standard academic context; authors are industry-
#                  adjacent — rubric says do not penalise that alone. The COI
#                  statement could not be inspected in the obtained copy.)
# Population       0.62 (heterogeneous: mostly young untrained, some trained,
#                  some middle-aged/older; both sexes. Heterogeneity WAS
#                  analysed via body-half interaction and a training-status
#                  subanalysis.)
# Weighted average: 0.7685 -> 0.77. No flat modifiers (no I^2 reported; the
# influential-study fragility of the hypertrophy trend is documented in the
# estimate notes rather than scored).
QUALITY = 0.77


# ----------------------------------------------------------------------------
# Populations (one per outcome — PopulationSpec carries the outcome field)
# ----------------------------------------------------------------------------

POPULATION_HYPERTROPHY = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    # Studies span young (18-39), middle-aged and older adults; (18, 70) is the
    # envelope of the included studies, not a single tight cohort.
    age_range=(18, 70),
    outcome="hypertrophy",
    notes="Schoenfeld/Grgic 2017 load MA, hypertrophy analysis: 10 studies, "
          "direct muscle-size measures. Mixed training status and ages.",
)

POPULATION_STRENGTH = PopulationSpec(
    training_status="mixed",
    sex="mixed",
    age_range=(18, 70),
    outcome="strength",
    notes="Schoenfeld/Grgic 2017 load MA, strength analyses: 14 studies (1RM) "
          "/ 8 studies (isometric). Mixed training status and ages.",
)


# ----------------------------------------------------------------------------
# Effect estimates — study-level high-vs-low-load contrast per outcome
# ----------------------------------------------------------------------------
# Scale: study-level standardized mean difference (high load minus low load;
# positive favours HIGH load). These are the forest-plot "Overall ES" values
# (Figures 2-4), which are the cleanest between-condition contrasts.
#
# SE provenance (audit-reconciled 2026-05-17):
#  - 1RM se=0.16 — the paper-reported SEM; text and Figure 2 agree (CI 0.28-0.89).
#  - isometric se=0.11 — the paper-reported SEM; consistent with Figure 3's CI
#    (-0.06 to 0.37). The Results TEXT prints a wider CI (-0.10 to 0.41); the
#    SEM-based se is kept.
#  - hypertrophy se=0.097 — NOT the text SEM (0.05). The paper is internally
#    inconsistent here: the text says CI -0.08 to 0.14 (SEM 0.05) while Figure
#    4 says -0.16 to 0.22 (SE ~0.097). The wider Figure 4 value is used — see
#    that estimate's inline comment for the rationale.
# EffectEstimate.ci_95 reconstructs a Normal mean +/- 1.96*se interval.
#
# n is summed from Table 1 across the studies in each analysis's forest plot,
# and includes all study arms (the paper reports ES counts and study counts,
# not per-analysis participant totals). n_studies carries the exact study
# count for each analysis.

LOAD_HYPERTROPHY_HIGH_VS_LOW = EffectEstimate(
    mean=0.03,
    # PAPER-INTERNAL INCONSISTENCY, resolved conservatively. Schoenfeld/Grgic
    # 2017 reports this study-level hypertrophy ES two ways that disagree:
    #   - Results text:  "ES = 0.03 +/- 0.05 (SEM); CI: -0.08 to 0.14"
    #   - Figure 4 forest-plot diamond:  0.03 [-0.16, 0.22]
    # The text SEM implies SE ~0.05; the Figure 4 interval implies SE ~0.097
    # (= 0.38 / (2*1.96)). Both cannot be right. We encode the WIDER Figure 4
    # value, se=0.097: it is the forest-plot diamond (the canonical pooled-
    # estimate interval), Schoenfeld's own 2021 review quotes [-0.16, 0.22],
    # and for a near-zero estimate the conservative (wider) SE avoids
    # overstating its inverse-variance pooling weight (se=0.05 would overstate
    # it ~3.8x). Re-verify against Table 2 / Figure 4 if author data surfaces.
    se=0.097,
    n=231,                          # ~231 participants across 10 hypertrophy studies
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=10,
    notes="Study-level effect of HIGH vs LOW load on muscle hypertrophy: "
          "ES 0.03, 95% CI -0.16 to 0.22 (per Figure 4; the Results text gives "
          "a narrower -0.08 to 0.14 — the paper is internally inconsistent, "
          "see the se comment), p=0.56 — essentially zero. With sets taken to "
          "failure, hypertrophy is equivalent across the loading spectrum. "
          "(A separate mean-ES analysis showed a non-significant trend p=0.10 "
          "favouring high load, but it did not survive removal of influential "
          "studies; the study-level ES encoded here is the conservative reading.)",
)

LOAD_STRENGTH_1RM_HIGH_VS_LOW = EffectEstimate(
    mean=0.58,
    se=0.16,                        # reported SEM (Results: ES 0.58 +/- 0.16)
    n=497,                          # ~497 participants across 14 1RM studies
    population=POPULATION_STRENGTH,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=14,
    notes="Study-level effect of HIGH vs LOW load on 1RM (dynamic) strength: "
          "ES 0.58 (95% CI 0.28-0.89, p=0.002) — high load clearly better. "
          "Consistent with specificity: 1RM testing rewards training near the "
          "1RM. Both loads still produced large absolute gains (high +35.3%, "
          "low +28.0%).",
)

LOAD_STRENGTH_ISOMETRIC_HIGH_VS_LOW = EffectEstimate(
    mean=0.16,
    se=0.11,                        # reported SEM (Results: ES 0.16 +/- 0.11)
    n=176,                          # ~176 participants across 8 isometric studies
    population=POPULATION_STRENGTH,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    n_studies=8,
    notes="Study-level effect of HIGH vs LOW load on ISOMETRIC strength: "
          "ES 0.16, 95% CI -0.06 to 0.37 (per Figure 3; the Results text "
          "prints a wider -0.10 to 0.41 — the paper is internally "
          "inconsistent), p=0.19 — no significant load effect. "
          "A DIFFERENT outcome from 1RM: when training specificity is removed "
          "(neutral isometric test), the high-load advantage largely "
          "disappears. Sensitivity analysis (removing Van Roie 2013b) shifted "
          "the interval toward favouring high load — interpret with caution "
          "given only 8 studies.",
)


# Lists for the registry. The two strength estimates are DIFFERENT outcomes
# (1RM vs isometric) and must not be pooled together — the registry's
# _POOLABLE_OVERRIDE designates the 1RM estimate as the poolable representative.
LOAD_HYPERTROPHY_ESTIMATES: list[EffectEstimate] = [LOAD_HYPERTROPHY_HIGH_VS_LOW]
LOAD_STRENGTH_ESTIMATES: list[EffectEstimate] = [
    LOAD_STRENGTH_1RM_HIGH_VS_LOW,
    LOAD_STRENGTH_ISOMETRIC_HIGH_VS_LOW,
]


# ----------------------------------------------------------------------------
# Practical guidance
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
When sets are taken to (or near) failure, muscle HYPERTROPHY is essentially
load-independent: low loads (>15 reps, <=60% 1RM) and high loads grow muscle
about equally. So a hypertrophy-goal program has wide freedom in rep-range
prescription — choose load by joint comfort, exercise, fatigue and user
preference, not by a belief that a "hypertrophy rep range" is required.

Maximal 1RM STRENGTH is different: heavy load is clearly better (ES 0.58),
because 1RM testing rewards practising near-maximal loads (specificity). A
strength-goal program should bias toward heavy loads on the tested lifts.
Isometric strength is not load-sensitive.

HARD SCOPE LIMIT: every study here took sets to momentary muscular failure.
These conclusions do NOT transfer to submaximal, non-failure training. If the
optimizer prescribes low-load work, it must also prescribe a high level of
effort (low RIR) for the load-independence of hypertrophy to hold.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Schoenfeld/Grgic 2017 (load MA) — quality {QUALITY}")
    for e in (LOAD_HYPERTROPHY_HIGH_VS_LOW, LOAD_STRENGTH_1RM_HIGH_VS_LOW,
              LOAD_STRENGTH_ISOMETRIC_HIGH_VS_LOW):
        lo, hi = e.ci_95
        print(f"  {e.population.outcome:<12} ES={e.mean:+.2f}  "
              f"(95% CI {lo:+.2f}, {hi:+.2f})  n_studies={e.n_studies}")
