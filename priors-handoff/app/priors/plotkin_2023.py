"""
Plotkin DL, Rodas MA, Vigotsky AD, McIntosh MC, Breeze E, Ubrik R, Robitzsch C,
Agyin-Birikorang A, Mattingly ML, Michel JM, Kontos NJ, Lennon S, Frugé AD,
Wilburn CM, Weimar WH, Bashir A, Beyers RJ, Henselmans M, Contreras BM,
Roberts MD.
"Hip thrust and back squat training elicit similar gluteus muscle hypertrophy
and transfer similarly to the deadlift."
Frontiers in Physiology. 2023;14:1279170.
doi: 10.3389/fphys.2023.1279170
PMID: 37877099 · PMC10593473 (open access)

KEY FINDING (9-week parallel-group RCT, n=34 untrained college-aged adults):

  34 participants completed a 9-week supervised, set-volume-equated barbell
  training programme, randomised to either the BACK SQUAT (SQ, n=16; 6M/10F;
  age 24+/-4) or the BARBELL HIP THRUST (HT, n=18; 5M/13F; age 22+/-3), 2
  sessions/week (week 1: 1 session), 8-12 reps, sets progressed identically
  3 -> 4 -> 5 -> 6 across the block. Hypertrophy measured by MRI cross-sectional
  area (mCSA) at three gluteus maximus subregions plus gluteus medius+minimus,
  quadriceps, hamstrings and adductors. Strength by 3RM squat / hip thrust /
  deadlift.

  BETWEEN-EXERCISE CONTRASTS, post-intervention score adjusted for the
  pre-intervention covariate (+/- SE; 95% bootstrap CI). All in RAW cm^2 mCSA
  difference. SIGN CONVENTION follows the paper's published notation: a
  NEGATIVE value favours the HIP THRUST (it grew the site more), a POSITIVE
  value favours the BACK SQUAT (it grew the site more):

    Gluteus maximus, upper subregion  -0.5 +/- 2.6 cm^2   CI95 (-5.8, 4.1)
    Gluteus maximus, middle subregion -0.5 +/- 1.7 cm^2   CI95 (-4.0, 2.6)
    Gluteus maximus, lower subregion  -1.6 +/- 2.1 cm^2   CI95 (-6.1, 2.0)
    Gluteus medius + minimus          -1.8 +/- 1.5 cm^2   CI95 (-4.6, 1.4)
    Quadriceps                        +3.6 +/- 1.5 cm^2   CI95 ( 0.7, 6.4)
    Adductors                         +2.5 +/- 0.7 cm^2   CI95 ( 1.2, 3.9)
    Hamstrings                        +0.1 +/- 0.6 cm^2   CI95 (-0.9, 1.4)

  Per that sign convention -- (-) favours the hip thrust, (+) favours the
  back squat. So:

  - GLUTEUS MAXIMUS: all three subregion contrasts are small and every CI
    spans zero. This is a genuine EQUIVALENCE / NULL result -- hip thrust and
    back squat produced statistically indistinguishable gluteus maximus
    hypertrophy. The point estimates lean trivially toward the hip thrust, but the
    CIs are far too wide to claim any winner. The honest reading is: for
    growing the glutes, the two exercises are roughly interchangeable.
  - GLUTEUS MEDIUS+MINIMUS: also crosses zero (-1.8, CI -4.6 to 1.4) -- no
    detectable difference.
  - QUADRICEPS and ADDUCTORS: the squat clearly out-grew the hip thrust
    (+3.6 and +2.5 cm^2, BOTH CIs exclude zero). This is the squat's thigh
    bonus -- a real, significant finding.
  - HAMSTRINGS: essentially identical (+0.1, CI crosses zero).

  STRENGTH TRANSFER (3RM, kg; same sign convention -- (-) favours the hip
  thrust, (+) favours the back squat):
    Back squat 3RM   +14 +/- 2 kg   CI95 ( 9, 18)   -> SQ trained the squat
    Hip thrust 3RM   -26 +/- 5 kg   CI95 (-34, -16) -> HT trained the hip thrust
    Deadlift 3RM      0 +/- 2 kg    CI95 ( -4,  3)  -> EQUAL transfer to deadlift
  Each exercise improves its own 3RM most (specificity); both transfer
  equally to the untrained deadlift. The strength numbers are encoded as
  module-level context constants, not EffectEstimates -- the optimizer's
  strength path is not exercise-selection-keyed and a single trial's raw-kg
  3RM transfer is not poolable with anything in the layer.

----------------------------------------------------------------------------
DATA SHAPE -- why this is encoded as between-exercise EffectEstimate contrasts
----------------------------------------------------------------------------

The authors deliberately ran NO within-group inferential statistics. They
state: "Notably, baseline and within-group inferential statistics were not
calculated, as baseline significance testing is inconsequential ... and
within-group outcomes are not the subject of our research question." The
entire inferential analysis is the BETWEEN-GROUP contrast (HT-vs-SQ),
reported as effect +/- SE with a 95% bootstrap CI.

That makes the paper a clean set of EffectEstimate-shaped contrasts -- each
has a mean and a directly-reported SE -- but NOT a clean ExerciseEmphasis
source. An ExerciseEmphasis coefficient is normally derived from each
exercise's OWN growth (cf. maeo_2021, maeo_2023, kassiano_2023, which all
normalise per-exercise % change within a muscle). Plotkin 2023 does not
support that: the per-exercise glute changes are presented only descriptively
in figures, never tested. Forcing a fractional emphasis ratio here would (a)
be built on numbers the authors declined to test, and (b) misrepresent a null
as a measured emphasis gap.

So this module's PRIMARY, faithful encoding is the between-exercise contrasts
as EffectEstimates on a raw-cm^2 difference scale (see SCALE below). It ALSO
exports two ExerciseEmphasis entries so the optimizer's exercise-selection
path can consume glute data -- but, because the paper measured NO winner for
the glutes, hip thrust and back squat BOTH get equal emphasis 1.0 for the
gluteus maximus at confidence="medium". That is an equivalence encoding, not
a measured ranking. See the EMPHASIS section for the full rationale.

----------------------------------------------------------------------------
SCALE -- raw cm^2 between-exercise difference; NOT poolable
----------------------------------------------------------------------------

scale = "between_exercise_csa_diff_cm2". This is a raw absolute cross-
sectional-area difference between two exercises. NO other EffectEstimate in
the layer uses it -- the encoded effect scales are standardized_mean_diff,
smd_per_set and pct_per_set. A raw-cm^2 between-exercise contrast cannot be
inverse-variance pooled with an SMD or a %/set slope: the units are
incommensurable and the question is different (exercise selection, not a
dose-response). The dedicated scale string is the guard against silent
pooling; it is also why this module's Topic is single-source and carries no
_POOLABLE_OVERRIDE -- there is nothing it could be wrongly pooled with.

----------------------------------------------------------------------------
TOPIC -- a new EXERCISE_SELECTION_HYPERTROPHY topic
----------------------------------------------------------------------------

The contrasts do not map onto any existing dose/form Topic
(volume/frequency/load/failure/ROM/muscle-length/arm-position/rest-interval
are all "how to train" axes; this paper holds all of those fixed and varies
the EXERCISE). It is exercise-selection evidence, for which the Topic enum had
no member. A new Topic EXERCISE_SELECTION_HYPERTROPHY is added. It is a
single-source, non-poolable Topic today (see SCALE) -- that is acceptable and
explicitly anticipated by the relevance assessment; it is the correct home
for between-exercise hypertrophy contrasts and future head-to-head trials.

----------------------------------------------------------------------------
OVERLAP / DOUBLE-COUNTING
----------------------------------------------------------------------------

No glute paper is currently encoded. The Krause Neto 2025 gluteus maximus
meta-analysis (the seeker's flagged overlap) is parked UNENCODED in
DEFERRED_CANDIDATES.md, appears in no module / index / Topic, and carries no
per-exercise data -- so there is no pool for Plotkin to double-count against,
and no _POOLABLE_OVERRIDE is needed now. ACTION FOR WHOEVER LATER ENCODES
KRAUSE NETO 2025: Plotkin 2023 is very plausibly one of its constituent
primary studies; record Plotkin as a constituent and keep it out of the
Krause Neto inverse-variance pool -- the same guard used for Pedrosa 2023 /
Maeo 2021 relative to Varovic 2025. Kassiano 2024 (hip thrust addition study,
also deferred) shares the muscle but no dataset -- a future separate emphasis
source, not an overlap.

----------------------------------------------------------------------------
CAVEATS
----------------------------------------------------------------------------

- NULL/EQUIVALENCE RESULT for the glutes: the glute-max contrasts cross zero
  with wide CIs. Encoded honestly as "no detectable difference" -- never as a
  coefficient implying one exercise wins. A null from a single n=34 trial is
  also an underpowered null: absence of evidence here is weak evidence of
  absence. The optimizer should read "roughly interchangeable for glutes",
  not "proven identical".
- The glute-max upper and middle point estimates are IDENTICAL (-0.5 cm^2)
  but with different SEs (2.6 vs 1.7). That is the paper's own reporting, not
  a transcription error.
- UNTRAINED young adults only -- applicability degrades for trained users.
- Untrained-trainee strength gains are large and somewhat noisy; the squat's
  quad/adductor advantage is robust here but is a squat-vs-hip-thrust
  contrast, not squat-vs-a-quad-isolation-exercise.
- The CIs are bias-corrected accelerated bootstrap (10,000 replicates) and
  are mildly asymmetric (e.g. deadlift 0 +/- 2 -> CI -4, 3). SE is reported
  DIRECTLY in the paper, so it is encoded directly; EffectEstimate.ci_95
  reconstructs a symmetric Normal interval that will NOT round-trip the
  paper's asymmetric bootstrap CI. The paper's CI is quoted in each note.
"""

from __future__ import annotations

from .shared import Citation, PopulationSpec, EffectEstimate, ExerciseEmphasis


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Plotkin et al.",
    year=2023,
    doi="10.3389/fphys.2023.1279170",
    journal="Frontiers in Physiology",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Full open-access text inspected (PMC10593473).
#
# Study design     0.90 (parallel-group RCT, randomised allocation to back
#                  squat vs hip thrust, supervised, set-volume-equated. No
#                  pre-registration mentioned -> rubric's 0.90 "RCT with minor
#                  design issues, no pre-reg but solid randomisation" tier.)
# Sample size      0.80 (per-arm n is 16 SQ and 18 HT -- both inside the
#                  rubric's 15-24 "0.80" band. Score by participants per arm,
#                  not total N, per the rubric.)
# Measurement      1.00 (MRI cross-sectional area -- gold standard for
#                  hypertrophy; three gluteus maximus subregions resolved.)
# Methodological   0.80 (frequentist linear regression with the baseline score
#                  as a covariate; bias-corrected accelerated stratified
#                  bootstrap, 10,000 replicates, for 95% compatibility
#                  intervals. Competent, modern estimation-statistics
#                  approach; no pre-registration. Rubric's 0.80 "no pre-reg
#                  but otherwise rigorous" tier.)
# Reporting        0.90 (every contrast reported as effect +/- SE WITH a 95%
#                  CI; no SE had to be reconstructed. Held below 1.00 because
#                  no raw-data / analysis-code deposit is cited in the
#                  inspected text.)
# Risk of bias     0.80 (funded partly by the International Scientific Research
#                  Foundation for Fitness and Nutrition and by author BC, via
#                  gift funds; BC and MH "disclose that they sell exercise-
#                  related products and services" but state neither was
#                  "involved in any aspect of the study beyond assisting with
#                  the study design and providing funds." BC is associated
#                  with the barbell hip thrust commercially -- a disclosed
#                  commercial tie to one of the two compared exercises -- yet
#                  the headline glute result is an EQUIVALENCE, not a finding
#                  favouring the hip thrust, and the squat actually wins the
#                  thigh contrasts. Rubric: a disclosed commercial tie with
#                  methods that appear sound and a result NOT favourable to
#                  the conflicted party -> 0.80, the "standard academic
#                  context, minor conflicts" tier, not the 0.60 commercial-
#                  interest tier.)
# Population       0.85 (well-described: n, per-group sex split, mean+/-SD age,
#                  training history -- "<= 1 day/week resistance training for
#                  the last 5 years". Single tight cohort. Rubric 0.7-0.9
#                  band; scored 0.85 -- minor ambiguity only in that ages are
#                  given as mean+/-SD not an explicit min-max range.)
# Weighted average:
#   0.90*0.20 + 0.80*0.15 + 1.00*0.20 + 0.80*0.15 + 0.90*0.10 + 0.80*0.10
#   + 0.85*0.10
#   = 0.180 + 0.120 + 0.200 + 0.120 + 0.090 + 0.080 + 0.085
#   = 0.875 -> 0.875
# No flat modifiers apply (not a meta-analysis, not predatory, not a
# subgroup-as-primary, not retracted, full text freely accessible).
QUALITY = 0.875


# ----------------------------------------------------------------------------
# Strength-transfer context (NOT encoded as EffectEstimates -- see docstring)
# ----------------------------------------------------------------------------
# Between-exercise 3RM contrasts, kg, effect +/- SE; CI95. Sign convention as
# in the docstring: a negative value favours the hip thrust, a positive value
# favours the back squat. Kept as plain constants for guidance text and
# traceability. They are not EffectEstimates: the layer's strength path is not
# exercise-selection-keyed, and a single trial's raw-kg 3RM transfer is
# poolable with nothing encoded.
STRENGTH_TRANSFER_CONTRASTS_KG = {
    "back_squat_3rm":  {"effect": 14.0, "se": 2.0, "ci95": (9.0, 18.0)},
    "hip_thrust_3rm":  {"effect": -26.0, "se": 5.0, "ci95": (-34.0, -16.0)},
    "deadlift_3rm":    {"effect": 0.0, "se": 2.0, "ci95": (-4.0, 3.0)},
}


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------
# One PopulationSpec per outcome. Every EffectEstimate in this module is a
# hypertrophy (mCSA) contrast, so one hypertrophy spec serves them all.

POPULATION_HYPERTROPHY = PopulationSpec(
    training_status="untrained",
    sex="mixed",
    # SQ group age 24+/-4, HT group 22+/-3 (mean+/-SD). The paper does not print
    # an explicit min-max; (18, 30) is the college-aged-untrained envelope that
    # the two mean+/-SD ranges sit inside, NOT a verbatim paper figure.
    age_range=(18, 30),
    outcome="hypertrophy",
    notes="Plotkin 2023 RCT: 34 untrained college-aged adults completing 9 "
          "weeks of supervised, set-volume-equated barbell training -- back "
          "squat (n=16, 6M/10F, age 24+/-4) vs barbell hip thrust (n=18, "
          "5M/13F, age 22+/-3). Training history: <= 1 day/week resistance "
          "training over the prior 5 years. age_range (18,30) is a young-adult "
          "envelope around the reported mean+/-SD ages, not a verbatim figure.",
)


# ----------------------------------------------------------------------------
# Between-exercise EffectEstimate contrasts
# ----------------------------------------------------------------------------
# scale = "between_exercise_csa_diff_cm2": a RAW cm^2 cross-sectional-area
# between-exercise difference. SIGN CONVENTION (per the paper): a negative
# value favours the HIP THRUST, a positive value favours the BACK SQUAT. The
# estimate variable names below carry an "_HT_VS_SQ" suffix -- that only names
# the two exercises compared; it does NOT assert a hip-thrust-minus-squat
# subtraction order. The paper's "(-) favours HT, (+) favours SQ" notation is
# authoritative. This scale is unique in the layer and is the guard against
# pooling these with SMD / %-per-set estimates (see module docstring).
#
# SE is read DIRECTLY off the paper (reported as "effect +/- SE"); no recovery
# from a CI or p-value was needed. The paper's 95% CI is a bias-corrected
# accelerated bootstrap interval (asymmetric); EffectEstimate.ci_95 returns a
# symmetric Normal mean +/- 1.96*SE interval that will NOT round-trip the
# printed CI. Each note quotes the paper's bootstrap CI.
#
# n = 34 (the participants who completed and were analysed) for every estimate.
# n_studies = None: this is a single primary RCT, not a meta-analysis.

_SCALE = "between_exercise_csa_diff_cm2"


GLUTE_MAX_UPPER_HT_VS_SQ = EffectEstimate(
    mean=-0.5,
    se=2.6,
    n=34,
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale=_SCALE,
    n_studies=None,
    notes="Gluteus maximus UPPER subregion, HT-vs-SQ: -0.5 +/- 2.6 cm^2 "
          "mCSA (95% bootstrap CI -5.8, 4.1). CI spans zero -- no detectable "
          "difference; trivial lean toward the hip thrust. Equivalence result. "
          "Same point estimate as the middle subregion (-0.5) but a wider SE "
          "-- the paper's own reporting, not a transcription error.",
)

GLUTE_MAX_MIDDLE_HT_VS_SQ = EffectEstimate(
    mean=-0.5,
    se=1.7,
    n=34,
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale=_SCALE,
    n_studies=None,
    notes="Gluteus maximus MIDDLE subregion, HT-vs-SQ: -0.5 +/- 1.7 cm^2 "
          "mCSA (95% bootstrap CI -4.0, 2.6). CI spans zero -- no detectable "
          "difference. Equivalence result.",
)

GLUTE_MAX_LOWER_HT_VS_SQ = EffectEstimate(
    mean=-1.6,
    se=2.1,
    n=34,
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale=_SCALE,
    n_studies=None,
    notes="Gluteus maximus LOWER subregion, HT-vs-SQ: -1.6 +/- 2.1 cm^2 "
          "mCSA (95% bootstrap CI -6.1, 2.0). CI spans zero -- no detectable "
          "difference; the largest (still trivial) glute-max lean toward the "
          "hip thrust. Equivalence result.",
)

GLUTE_MED_MIN_HT_VS_SQ = EffectEstimate(
    mean=-1.8,
    se=1.5,
    n=34,
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale=_SCALE,
    n_studies=None,
    notes="Gluteus MEDIUS + MINIMUS (combined), HT-vs-SQ: -1.8 +/- 1.5 "
          "cm^2 mCSA (95% bootstrap CI -4.6, 1.4). CI spans zero -- no "
          "detectable difference. Reported as a single combined measure; the "
          "two abductor muscles are NOT separated, and neither exercise is an "
          "abduction-specific movement. Touches the hip-abductor coverage gap "
          "only as a by-product.",
)

QUADRICEPS_HT_VS_SQ = EffectEstimate(
    mean=3.6,
    se=1.5,
    n=34,
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale=_SCALE,
    n_studies=None,
    notes="QUADRICEPS, HT-vs-SQ: +3.6 +/- 1.5 cm^2 mCSA (95% bootstrap CI "
          "0.7, 6.4). CI EXCLUDES zero -- the back squat grew the quadriceps "
          "significantly more than the hip thrust. The squat's thigh bonus. "
          "This is a squat-vs-hip-thrust contrast, not squat-vs-a-quad-"
          "isolation-exercise.",
)

ADDUCTORS_HT_VS_SQ = EffectEstimate(
    mean=2.5,
    se=0.7,
    n=34,
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale=_SCALE,
    n_studies=None,
    notes="ADDUCTORS, HT-vs-SQ: +2.5 +/- 0.7 cm^2 mCSA (95% bootstrap CI "
          "1.2, 3.9). CI EXCLUDES zero -- the back squat grew the hip "
          "adductors significantly more than the hip thrust. Part of the "
          "squat's thigh bonus. Squat-vs-hip-thrust contrast, not "
          "squat-vs-an-adduction-isolation-exercise.",
)

HAMSTRINGS_HT_VS_SQ = EffectEstimate(
    mean=0.1,
    se=0.6,
    n=34,
    population=POPULATION_HYPERTROPHY,
    source=CITATION,
    quality_score=QUALITY,
    scale=_SCALE,
    n_studies=None,
    notes="HAMSTRINGS, HT-vs-SQ: +0.1 +/- 0.6 cm^2 mCSA (95% bootstrap CI "
          "-0.9, 1.4). CI spans zero -- essentially identical hamstring "
          "growth. Neither barbell exercise is a notable hamstring builder.",
)


# Full ordered list -- glutes first (the paper's primary target), then the
# thigh-musculature contrasts. Registered under EXERCISE_SELECTION_HYPERTROPHY.
EXERCISE_SELECTION_ESTIMATES: list[EffectEstimate] = [
    GLUTE_MAX_UPPER_HT_VS_SQ,
    GLUTE_MAX_MIDDLE_HT_VS_SQ,
    GLUTE_MAX_LOWER_HT_VS_SQ,
    GLUTE_MED_MIN_HT_VS_SQ,
    QUADRICEPS_HT_VS_SQ,
    ADDUCTORS_HT_VS_SQ,
    HAMSTRINGS_HT_VS_SQ,
]

# The gluteus-maximus subset, for callers that want just the headline
# equivalence result without the thigh by-products.
GLUTEUS_MAXIMUS_ESTIMATES: list[EffectEstimate] = [
    GLUTE_MAX_UPPER_HT_VS_SQ,
    GLUTE_MAX_MIDDLE_HT_VS_SQ,
    GLUTE_MAX_LOWER_HT_VS_SQ,
]


# ----------------------------------------------------------------------------
# Exercise emphasis coefficients -- EQUIVALENCE encoding only
# ----------------------------------------------------------------------------
# These exist solely so the optimizer's exercise-selection path can consume
# glute data; the FAITHFUL primary encoding is the EffectEstimate contrasts
# above.
#
# CRITICAL: the paper measured NO winner for the gluteus maximus -- all three
# subregion contrasts cross zero. So the barbell hip thrust and the barbell
# back squat BOTH receive emphasis = 1.0 for the gluteus maximus. This is an
# EQUIVALENCE encoding: it says "these two exercises are interchangeable for
# the glutes", which is exactly what the trial found. A fractional coefficient
# (e.g. squat = HT x ratio-of-descriptive-figure-values) is deliberately NOT
# used -- it would invent a measured ranking the authors never tested and
# would misrepresent a null as an emphasis gap.
#
# confidence = "medium": the DIRECTION here is "no difference", and that null
# rests on a single n=34 untrained-trainee trial whose CIs, while spanning
# zero, are wide enough that a real moderate difference is not excluded. An
# underpowered equivalence is medium-confidence, not high. (Contrast maeo_2021,
# where the significant seated-leg-curl advantage justified confidence="high"
# on direction.)
#
# region = None (whole gluteus maximus). Per-subregion emphasis entries are
# deliberately NOT minted: all three subregion contrasts are equivalent too,
# so per-subregion entries would just be three more identical 1.0/1.0 pairs
# carrying no extra optimizer signal. The subregion resolution is preserved in
# the EffectEstimate contrasts and in GUIDANCE_FOR_OPTIMIZER.
#
# NO emphasis entry is minted for the quadriceps or adductors. There the squat
# DID win -- but emphasis coefficients are normalised from each exercise's own
# growth, and the hip thrust's own quad/adductor growth was not tested. A
# between-exercise contrast is not an emphasis coefficient; that finding lives
# in QUADRICEPS_HT_VS_SQ / ADDUCTORS_HT_VS_SQ and the guidance text.
#
# PROVISIONAL-SCALE METHOD CAVEAT (same as maeo_2021 / maeo_2023 /
# kassiano_2023): shared.py defines `emphasis` as a study-independent
# "fraction of maximum stimulus." The 1.0 / 1.0 pair here is not that -- it is
# a within-this-study equivalence statement. Treat it as a soft prior: "for a
# glute goal, hip thrust and back squat are interchangeable", not as a stable
# absolute constant.
#
# Exercise keys: "barbell_hip_thrust", "barbell_back_squat".

EMPHASIS_HIP_THRUST_GLUTE_MAX = ExerciseEmphasis(
    exercise="barbell_hip_thrust",
    muscle="gluteus_maximus",
    region=None,
    emphasis=1.0,
    confidence="medium",
    source=CITATION,
    rationale="9-week volume-equated RCT (MRI mCSA): hip thrust vs back squat "
              "produced statistically indistinguishable gluteus maximus "
              "hypertrophy at all three subregions (HT-vs-SQ contrasts "
              "-0.5, -0.5, -1.6 cm^2, every 95% CI spanning zero). Encoded as "
              "an EQUIVALENCE -- hip thrust = 1.0, equal to the back squat -- "
              "NOT a measured ranking. The authors ran no within-group tests, "
              "so no fractional coefficient is defensible. confidence=medium: "
              "an underpowered (n=34) null.",
    population=POPULATION_HYPERTROPHY,
    quality_score=QUALITY,
)

EMPHASIS_BACK_SQUAT_GLUTE_MAX = ExerciseEmphasis(
    exercise="barbell_back_squat",
    muscle="gluteus_maximus",
    region=None,
    emphasis=1.0,
    confidence="medium",
    source=CITATION,
    rationale="9-week volume-equated RCT (MRI mCSA): back squat vs hip thrust "
              "produced statistically indistinguishable gluteus maximus "
              "hypertrophy at all three subregions. Encoded as an EQUIVALENCE "
              "-- back squat = 1.0, equal to the hip thrust -- NOT a measured "
              "ranking. confidence=medium: an underpowered (n=34) null. The "
              "back squat additionally out-grows the hip thrust for the "
              "quadriceps and adductors (see QUADRICEPS_HT_VS_SQ / "
              "ADDUCTORS_HT_VS_SQ), which is a reason to prefer it when those "
              "muscles are also goals -- but that does not change its glute "
              "emphasis.",
    population=POPULATION_HYPERTROPHY,
    quality_score=QUALITY,
)


EMPHASIS_ESTIMATES: list[ExerciseEmphasis] = [
    EMPHASIS_HIP_THRUST_GLUTE_MAX,
    EMPHASIS_BACK_SQUAT_GLUTE_MAX,
]


# ----------------------------------------------------------------------------
# Practical guidance derived from this paper
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
For GLUTEUS MAXIMUS hypertrophy, the barbell hip thrust and the barbell back
squat are roughly INTERCHANGEABLE. A 9-week volume-equated RCT in untrained
adults found no detectable difference in MRI cross-sectional-area growth at
any of three gluteus maximus subregions (upper, middle, lower) -- every
between-exercise contrast was small and its 95% CI crossed zero. Do not rank
one above the other for a glute goal; pick on preference, equipment,
loadability or programme fit. This is a single n=34 trial, so the equivalence
is medium-confidence, not proven identity.

The back squat additionally out-grew the hip thrust for the QUADRICEPS
(+3.6 cm^2, CI 0.7-6.4) and the ADDUCTORS (+2.5 cm^2, CI 1.2-3.9) -- both
statistically clear. So when the user wants glutes PLUS quads/adductors, the
squat is the more efficient single choice; when the goal is glutes in
isolation, or the squat is contraindicated, the hip thrust is an equal-value
substitute. Hamstring growth was negligible for both -- neither exercise is a
hamstring builder.

Strength transfer follows specificity: each exercise improved its own 3RM
most (squat +14 kg, hip thrust +26 kg, HT-vs-SQ), and BOTH transferred
EQUALLY to an untrained deadlift 3RM (contrast 0 +/- 2 kg). If the goal is a
bigger deadlift, hip thrust and back squat are again interchangeable.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Plotkin 2023 -- quality {QUALITY}, n=34 RCT (HT n=18 vs SQ n=16), "
          f"full text PMC10593473")
    print(f"{len(EXERCISE_SELECTION_ESTIMATES)} between-exercise contrasts "
          f"(HT-vs-SQ, raw cm^2 mCSA):")
    for e in EXERCISE_SELECTION_ESTIMATES:
        lo, hi = e.ci_95
        crosses = "crosses 0" if lo < 0 < hi else "EXCLUDES 0"
        print(f"  mean={e.mean:+.1f} cm^2  SE={e.se:.1f}  "
              f"Normal-CI ({lo:+.2f}, {hi:+.2f})  [{crosses}]")
    print(f"{len(EMPHASIS_ESTIMATES)} emphasis coefficients "
          f"(gluteus maximus, equivalence encoding):")
    for em in EMPHASIS_ESTIMATES:
        print(f"  {em.exercise:<20} -> gluteus_maximus: "
              f"{em.emphasis:.2f} ({em.confidence})")
