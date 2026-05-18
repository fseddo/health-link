"""
Pedrosa GF, Simoes MG, Figueiredo MOC, Lacerda LT, Schoenfeld BJ, Lima FV,
Chagas MH, Diniz RCR.
Training in the Initial Range of Motion Promotes Greater Muscle Adaptations
Than at Final in the Arm Curl.
Sports (Basel). 2023;11(2):39.
doi: 10.3390/sports11020039
PMID: 36828324  (open access)

KEY FINDING (8-week within-participant study, 21 enrolled / 19 completed,
untrained young women):

  Seated dumbbell preacher curl, 3x/week, 4-5 sets to volitional failure.
  Each participant trained ONE arm in the INITIAL ROM and the CONTRALATERAL
  arm in the FINAL ROM (arms randomized/counterbalanced):

    INITIAL ROM  elbow 0-68 deg   (0 = extended elbow) -> elbow flexors at the
                                  LONGER muscle length
    FINAL ROM    elbow 68-135 deg                      -> elbow flexors SHORTER

  Biceps brachii cross-sectional area (B-mode ultrasound) — between-condition
  effect size (INITIAL minus FINAL; positive favours the longer length):

    70% of the acromion-to-lateral-epicondyle distance (DISTAL):  d = 0.89 (large),  p = 0.001
    50% of the acromion-to-lateral-epicondyle distance (MID):     d = 0.23 (small),  p = 0.331  (n.s.)
    Summed 50%+70% (whole-ish):      d = 0.39 (small),  p = 0.111  (n.s.)

  Strength (1RM tested at full ROM): INITIAL +42.8% vs FINAL +19.0%,
  d = 1.05, p < 0.001 — NOT encoded here (a strength outcome from a single
  within-participant study; recorded for context only).

So initial-ROM (long-length) training grew the DISTAL biceps substantially
more, but the mid-belly and the whole-muscle (summed) differences were small
and non-significant. The effect is REGIONAL, not whole-muscle.

----------------------------------------------------------------------------
WHAT THIS PAPER IS — AND HOW IT RELATES TO VAROVIC 2025
----------------------------------------------------------------------------

This is a REGIONAL-hypertrophy study: it measures growth at two sites along
ONE muscle (the biceps brachii) and asks whether long-length training grows
the muscle preferentially at the distal site. That is exactly the question
Varovic 2025's meta-analysis pooled — and Varovic concluded the regional
effect of muscle length is TRIVIAL on average (SMDs 0.05-0.09, intervals
mostly crossing zero).

Pedrosa 2023, a single primary study, found a LARGE distal effect (d = 0.89).
That is the honest tension: direct experimental evidence of a length-driven
distal bias in the biceps, against a meta-analytic consensus that the regional
effect is trivial across muscles. Encode both; do not let the one primary
study overturn the meta-analysis.

Consequences for the registry:
  - These estimates are filed under the SAME topic as Varovic
    (muscle_length -> regional_hypertrophy).
  - They are deliberately kept OUT of that topic's inverse-variance pool
    (_POOLABLE_OVERRIDE -> Varovic only). Two reasons: (1) Pedrosa 2023 is
    CONFIRMED to be one of the 12 studies inside Varovic's meta-analysis (the
    2026-05-17 audit checked Varovic's included-study list), so pooling the two
    would double-count it outright; (2) the region definitions do not match
    1:1 (Pedrosa 50%/70%; Varovic proximal-25% / mid-50% / distal-75%). The
    meta-analysis is the authoritative pooled source; this study is a visible
    primary-evidence companion.

----------------------------------------------------------------------------
WHY EffectEstimate AND NOT ExerciseEmphasis
----------------------------------------------------------------------------

The BACKLOG queued this as an ExerciseEmphasis source ("biceps, analogous to
Kassiano"). Reading the full text shows it is not that shape: the paper
reports BETWEEN-CONDITION Cohen's d values (a within-participant contrast),
not per-arm percentage growth, so there are no growth ratios from which to
build [0,1] emphasis coefficients the way maeo_2023 / kassiano_2023 do.
Encoding it honestly means EffectEstimate objects on the SMD scale — the same
shape as maeo_2023's whole-muscle effects and varovic_2025's regional effects.
"""

from __future__ import annotations
import math

from .shared import Citation, PopulationSpec, EffectEstimate


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Pedrosa et al.",
    year=2023,
    doi="10.3390/sports11020039",
    journal="Sports",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Study design     0.88 — DELIBERATE DEVIATION, as for maeo_2023. This is a
#                  within-participant contralateral-limb training study; the
#                  rubric's literal "side-to-side" row is 0.5. Scored 0.88
#                  because arms were randomized and counterbalanced and the
#                  contralateral model is an established, powerful design
#                  (rubric "When to deviate" clause).
# Sample size      0.80 (19 completers, each contributing both arms; rubric's
#                  15-24 band. 21 enrolled, 2 withdrew.)
# Measurement      0.85 (biceps cross-sectional area by B-mode ultrasound,
#                  blinded analysis, ICC 0.92-0.94 — rubric's CSA-via-
#                  ultrasound 0.85 tier)
# Methodological   0.80 (within-participant control, blinded CSA analysis,
#                  metronome-paced tempo, load standardized to a rep target;
#                  no pre-registration mentioned)
# Reporting        0.80 (effect sizes, p-values, ICCs and CIs reported — but
#                  the CIs are on the raw cm^2 difference, and no per-arm
#                  pre/post descriptives are given)
# Risk of bias     0.84 (academic Brazilian funding, FAPEMIG/CAPES; one author
#                  (BJS) discloses a Tonal Corp. scientific-advisory-board
#                  role — disclosed, not specific to a ROM finding)
# Population       0.80 (untrained young women, training status explicitly
#                  defined; single sex. The reported age "22.8 +/- 10.5 y" has
#                  an implausibly large SD — likely a paper typo; see POPULATION)
# Weighted average: 0.830 -> 0.83. No flat modifiers (the distal-site result is
# a pre-planned regional comparison, not a post-hoc subgroup).
QUALITY = 0.83


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------

POPULATION = PopulationSpec(
    training_status="untrained",
    sex="female",
    # The paper reports age as 22.8 +/- 10.5 y. A SD of 10.5 on a mean of 22.8
    # for "young untrained women" is implausible (it would imply early-teens
    # participants) and is most likely a typo in the paper. (18, 30) is used as
    # the young-adult envelope rather than trusting that SD.
    age_range=(18, 30),
    outcome="hypertrophy",
    notes="21 untrained young women enrolled, 19 completed (2 withdrew). "
          "Within-participant contralateral-arm design. Training status "
          "explicitly stated (no physical activity for >=6 months).",
)


# ----------------------------------------------------------------------------
# Effect estimates — regional biceps growth, INITIAL vs FINAL ROM
# ----------------------------------------------------------------------------
# Scale: paper-reported between-condition Cohen's d (INITIAL minus FINAL;
# positive = the longer muscle length grew the site more). These ARE difference
# SMDs and are poolable as such — same shape as maeo_2023's whole-muscle d
# values and varovic_2025's regional SMDs.
#
# SE recovery: the paper reports 95% CIs only on the raw cm^2 difference, not
# on d, so the SE of d is reconstructed from (d, n) below. _unpaired_d_se is
# the independent-groups SE formula (same helper as maeo_2023): for a
# within-participant design it ignores the arm-to-arm correlation and is
# therefore a CONSERVATIVE (too-wide) approximation. EffectEstimate.ci_95 will
# not reproduce the paper's cm^2 interval — different quantity.
#
# Note on n: n=19 is the within-participant completer count. The between-
# condition contrast does not have 19 independent observations per arm, so
# downstream sqrt(n) weighting in best_applicable slightly over-credits this
# study's statistical power.

def _unpaired_d_se(cohens_d: float, n: int) -> float:
    """Approximate SE for Cohen's d via the independent-groups formula.

    This is the large-sample SE for an UNPAIRED d. Pedrosa 2023 is a
    within-participant design, so the true paired SE is smaller; this is a
    deliberately conservative approximation (cf. maeo_2023._unpaired_d_se).
    """
    return math.sqrt(1 / n + (cohens_d ** 2) / (2 * n))


BICEPS_DISTAL_INITIAL_VS_FINAL = EffectEstimate(
    mean=0.89,
    se=_unpaired_d_se(0.89, 19),
    n=19,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="DISTAL biceps brachii (70% of the acromion-to-lateral-epicondyle distance): between-condition "
          "Cohen's d 0.89 (large), p=0.001, favouring INITIAL (long-length) "
          "ROM training. The paper's headline regional finding.",
)

BICEPS_MID_INITIAL_VS_FINAL = EffectEstimate(
    mean=0.23,
    se=_unpaired_d_se(0.23, 19),
    n=19,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="MID biceps brachii (50% of the acromion-to-lateral-epicondyle distance): between-condition "
          "Cohen's d 0.23 (small), p=0.331 — NOT significant. (The paper is "
          "internally inconsistent on this p-value: the Results text says "
          "0.331, the Abstract says 0.311; non-significant either way.) "
          "Long-length training did not preferentially grow the mid-belly.",
)

BICEPS_SUMMED_INITIAL_VS_FINAL = EffectEstimate(
    mean=0.39,
    se=_unpaired_d_se(0.39, 19),
    n=19,
    population=POPULATION,
    source=CITATION,
    quality_score=QUALITY,
    scale="standardized_mean_diff",
    notes="SUMMED biceps brachii CSA (50%+70%, whole-ish): between-condition "
          "Cohen's d 0.39 (small), p=0.111 — NOT significant. The whole-muscle "
          "advantage of long-length training was small; the effect was "
          "concentrated distally.",
)


REGIONAL_ESTIMATES: list[EffectEstimate] = [
    BICEPS_DISTAL_INITIAL_VS_FINAL,
    BICEPS_MID_INITIAL_VS_FINAL,
    BICEPS_SUMMED_INITIAL_VS_FINAL,
]


# ----------------------------------------------------------------------------
# Practical guidance
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
Training the elbow flexors at a long muscle length — the stretched, initial
portion of the curl (elbow extended) — grew the DISTAL biceps substantially
more than short-length training (d=0.89). The mid-belly and whole-muscle
(summed) differences were small and non-significant.

This is direct experimental evidence of a length-driven DISTAL regional bias
in the biceps. But it is a SINGLE study, and Varovic 2025's meta-analysis
found regional effects of muscle length to be trivial on average across
muscles. So: bias elbow-flexor work toward the stretched portion of the ROM
(this also corroborates Wolf 2023 and Kassiano 2023 on lengthened partials),
but do NOT generalize a strong "distal biceps" regional claim — treat it as
muscle-specific, single-study evidence pending replication.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Pedrosa 2023 — quality {QUALITY}, n=19 within-participant")
    print("Regional biceps effects (INITIAL vs FINAL ROM, between-condition d):")
    for e in REGIONAL_ESTIMATES:
        lo, hi = e.ci_95
        print(f"  d={e.mean:+.2f}  (95% CI {lo:+.2f}, {hi:+.2f})  "
              f"se={e.se:.3f}  {e.notes[:38]}")
