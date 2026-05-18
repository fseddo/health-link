"""
Maeo S, Huang M, Wu Y, Sakurai H, Kusagawa Y, Sugiyama T, Kanehisa H, Isaka T.
Greater Hamstrings Muscle Hypertrophy but Similar Damage Protection after
Training at Long versus Short Muscle Lengths.
Medicine & Science in Sports & Exercise. 2021;53(4):825-837.
doi: 10.1249/MSS.0000000000002523
PMID: 33009197 · PMC7969179 (open access)

KEY FINDING (Part 1: 12-week within-participant intervention, n=20 adults):

  Each participant trained one leg with the SEATED leg curl (hip flexed ~90 deg
  -> the biarticular hamstrings held at a LONG muscle length) and the other leg
  with the PRONE leg curl (hip ~30 deg -> a SHORT muscle length). Both legs:
  70% 1RM, 5 sets of 10 reps, 2 s concentric / 2 s eccentric, 2 sessions/week,
  full 0-90 deg knee ROM. MRI-measured muscle volume, pre vs post.

  ANCOVA-adjusted mean muscle-volume change, Seated-Leg vs Prone-Leg:

    Whole hamstrings (WH)          +14.1%  vs  +9.3%   P <= 0.010
    Biceps femoris long head (BFL) +14.4%  vs  +6.5%   P <= 0.010
    Semitendinosus (ST)            +23.6%  vs  +19.3%  P <= 0.010
    Semimembranosus (SM)           +8.2%   vs  +3.6%   P <= 0.010
    Biceps femoris short head (BFS) +10%   vs  +9%     P = 0.190  (n.s.)

  The three BIARTICULAR hamstrings (BFL, ST, SM) and the whole muscle all grew
  significantly more with the seated leg curl. The MONOARTICULAR biceps femoris
  short head -- which crosses only the knee and is therefore NOT lengthened
  differently by hip position -- showed no significant difference. That
  biarticular-vs-monoarticular dissociation is the mechanistic core of the
  paper: muscle length during training drove the hypertrophy difference.

THIS MODULE ENCODES ExerciseEmphasis ONLY -- and deliberately so.

  Maeo 2021 is one of the twelve primary studies pooled inside the already-
  encoded Varovic 2025 muscle-length meta-analysis (Topic
  MUSCLE_LENGTH_REGIONAL_HYPERTROPHY). Encoding Maeo 2021's regional data as a
  separate Topic-keyed EffectEstimate would double-count it against Varovic.
  This module therefore exports NO EffectEstimate and adds NO Topic. It mirrors
  exactly how Pedrosa 2023 (also a Varovic constituent) is kept out of that
  inverse-variance pool.

  The exercise-emphasis question Maeo 2021 answers -- "does the seated leg curl
  grow the (whole or sub-) hamstrings more than the prone leg curl?" -- is a
  distinct question (Q1, exercise selection) that Varovic does NOT answer
  (Varovic answers Q2, proximal-vs-distal within a condition). Emphasis data
  enters the SEPARATE emphasis index, keyed by (exercise, muscle, region) and
  pooled by quality-weighted averaging -- never the inverse-variance Topic
  pool. So adding emphasis-only does not double-count, and NO _POOLABLE_OVERRIDE
  is needed. See docs/priors/relevance/maeo_2021_relevance.md.

This is the third ExerciseEmphasis source in the layer (after Maeo 2023,
triceps; Kassiano 2023, gastrocnemius) and the first for the hamstrings. It is
also the first sub-muscle resolution for the posterior thigh.

CAVEATS:
  - Within-participant (contralateral-leg) design: the two legs' change scores
    are correlated, which the emphasis shape does not model -- but emphasis is a
    relative ranking, not an effect size, so this matters less here than for an
    EffectEstimate.
  - PROVISIONAL emphasis scale -- see the METHOD CAVEAT block below.
  - The BFS pair is encoded at confidence="low": the +10% vs +9% difference was
    NOT statistically significant (P = 0.190).
  - Demographics: the full text gives "20 young adults", none systematically
    resistance-trained in the prior 12 months. The exact sex split (13 men, 7
    women) is from a secondary source -- see POPULATION notes, flagged
    UNVERIFIED. The funder is the Mizuno Sports Promotion Foundation, a
    sporting-goods company's research foundation (no product conflict on this
    finding; "no conflict of interest" declared).
"""

from __future__ import annotations

from .shared import Citation, PopulationSpec, ExerciseEmphasis


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Maeo et al.",
    year=2021,
    doi="10.1249/MSS.0000000000002523",
    journal="Medicine & Science in Sports & Exercise",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Full open-access text inspected (PMC7969179).
#
# Study design     0.90 -- DELIBERATE DEVIATION. Within-participant
#                  contralateral-leg (side-to-side) 12-week training study; the
#                  rubric's literal row for side-to-side designs is 0.5. Scored
#                  0.90 because leg-to-condition assignment was randomized via a
#                  computer-generated list with the dominant/nondominant legs
#                  counterbalanced, and the contralateral-limb model is an
#                  established, high-power design for hypertrophy comparisons
#                  (rubric "When to deviate" clause). Identical reasoning to the
#                  documented deviation in maeo_2023.py.
# Sample size      0.80 (n=20 legs per condition -- rubric's 15-24 band)
# Measurement      1.00 (3-T MRI muscle volume, gold standard; analysts blinded
#                  to training condition; pretraining test-retest CV 1.4-2.1%)
# Methodological   0.85 (baseline-adjusted ANCOVA + linear mixed-effects model;
#                  residual normality/homoscedasticity checked, nonparametric
#                  cross-check; bootstrap 95% CIs via estimation statistics. No
#                  pre-registration mentioned.)
# Reporting        0.85 (full per-muscle % changes and bootstrap 95% CIs in the
#                  figures; descriptive + test statistics in Supplemental
#                  Digital Content tables. Held below 0.90 because exact
#                  per-muscle p-values for the four significant muscles are
#                  collapsed to a single "P <= 0.010" threshold in the text.)
# Risk of bias     0.85 (funded by the Mizuno Sports Promotion Foundation -- a
#                  sporting-goods company's research foundation. No conflict on
#                  THIS finding: the result favours a training position, not a
#                  product, and the authors declare "no conflict of interest"
#                  and that "no companies or manufacturers will benefit". Held
#                  one notch below the 0.90 plain-academic-grant tier because
#                  the funder is a manufacturer-affiliated foundation.)
# Population       0.80 (20 young untrained adults, well-described training
#                  history; exact age range not stated in the inspectable text
#                  and the sex split is from a secondary source -- see
#                  POPULATION. Rubric 0.7-0.9 band, scored at 0.80.)
# Weighted average:
#   0.90*0.20 + 0.80*0.15 + 1.00*0.20 + 0.85*0.15 + 0.85*0.10 + 0.85*0.10
#   + 0.80*0.10
#   = 0.180 + 0.120 + 0.200 + 0.1275 + 0.085 + 0.085 + 0.080
#   = 0.8775 -> 0.88
# No flat modifiers apply.
QUALITY = 0.88


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------

POPULATION = PopulationSpec(
    training_status="untrained",
    sex="mixed",
    # The inspectable full text describes participants only as "20 young
    # adults" with no systematic resistance training in the prior 12 months; it
    # does NOT state an explicit age range in the extractable body text (the
    # demographic detail sits in Figure 2's flow diagram, which is an image).
    # (20, 30) is the conventional young-adult envelope, NOT a paper figure.
    age_range=(20, 30),
    outcome="hypertrophy",
    notes="20 young untrained adults (none systematically resistance-trained "
          "in the prior 12 months). Within-participant contralateral-leg "
          "design: one leg trained seated leg curl, the other prone. "
          "UNVERIFIED: a secondary source (sci-sport.com) reports the sex "
          "split as 13 men / 7 women; the exact split and age range could not "
          "be confirmed from the inspectable full text (Figure 2 demographic "
          "panel is an image). age_range (20,30) is a young-adult envelope, "
          "not a paper figure.",
)


# ----------------------------------------------------------------------------
# Exercise emphasis coefficients
# ----------------------------------------------------------------------------
# Derived from the ANCOVA-adjusted muscle-volume % changes in Part 1,
# normalized WITHIN each muscle/region to the higher-growth condition (the
# seated leg curl, which won every comparison). The prone leg curl's emphasis
# is the prone/seated growth ratio. Two leg-curl positions are encoded as two
# distinct exercise keys -- the same way Maeo 2023 encodes overhead vs neutral
# extension and Kassiano 2023 encodes the three calf-raise ROM variants.
#
# PROVISIONAL -- METHOD CAVEAT (same as maeo_2023 / kassiano_2023): shared.py
# defines `emphasis` as a study-independent "fraction of maximum stimulus." A
# ratio of 12-week percent-volume-growth outcomes is NOT that -- it is
# intervention-, duration- and population-specific, and its implicit zero is
# anchored at "the weaker of two real exercises" (the prone leg curl still grew
# the whole hamstrings +9.3%, not "0.66 of nothing"). It will not generalize
# across studies with different baselines, durations or measurement modalities.
# Treat the ten values below as a PROVISIONAL within-this-study relative
# ranking, not stable exercise constants; the optimizer should consume them as
# soft priors with wide uncertainty. The "high" confidence on the biarticular
# pairs means the DIRECTION of the seated-leg-curl advantage is well
# established -- NOT that the exact ratios are precise.
#
# Normalizing the seated leg curl to 1.0 for the hamstrings, while Maeo 2023's
# overhead extension is 1.0 for the triceps and Kassiano's lengthened partial
# is 1.0 for the gastrocnemius, is intentional and fine -- emphasis is
# WITHIN-muscle relative, never across muscles (BACKLOG.md open question 3).
#
# Exercise keys: "seated_leg_curl", "prone_leg_curl" (a.k.a. lying leg curl).
# Sub-muscle region keys: "biceps_femoris_long_head", "biceps_femoris_short_head",
# "semitendinosus", "semimembranosus"; region=None for the whole hamstrings.
#
# Confidence: the whole-muscle and the three BIARTICULAR sub-muscle pairs are
# "high" -- the seated > prone difference reached significance (P <= 0.010) for
# WH, BFL, ST and SM. The MONOARTICULAR biceps femoris short head pair is "low"
# -- its +10% vs +9% difference was NOT significant (P = 0.190), and
# mechanistically no difference is expected because the short head crosses only
# the knee.

# --- Whole hamstrings -------------------------------------------------------

SEATED_LEG_CURL_WHOLE = ExerciseEmphasis(
    exercise="seated_leg_curl",
    muscle="hamstrings",
    region=None,                 # whole muscle
    emphasis=1.0,                # reference: higher-growth condition in this study
    confidence="high",
    source=CITATION,
    rationale="+14.1% whole-hamstrings muscle volume in 12 weeks (MRI). "
              "Significantly greater than the prone leg curl (P <= 0.010). "
              "Reference exercise for the whole hamstrings.",
    population=POPULATION,
    quality_score=QUALITY,
)

PRONE_LEG_CURL_WHOLE = ExerciseEmphasis(
    exercise="prone_leg_curl",
    muscle="hamstrings",
    region=None,
    emphasis=9.3 / 14.1,         # ~= 0.66
    confidence="high",
    source=CITATION,
    rationale="+9.3% whole-hamstrings volume vs +14.1% for the seated leg "
              "curl. Normalized to the seated leg curl = 1.0. The hip-extended "
              "(prone) position holds the biarticular hamstrings shorter, "
              "reducing the hypertrophic stimulus.",
    population=POPULATION,
    quality_score=QUALITY,
)

# --- Biceps femoris long head (biarticular) ---------------------------------

SEATED_LEG_CURL_BFL = ExerciseEmphasis(
    exercise="seated_leg_curl",
    muscle="hamstrings",
    region="biceps_femoris_long_head",
    emphasis=1.0,
    confidence="high",
    source=CITATION,
    rationale="+14.4% biceps femoris long head volume in 12 weeks. "
              "Significantly greater than the prone leg curl (P <= 0.010).",
    population=POPULATION,
    quality_score=QUALITY,
)

PRONE_LEG_CURL_BFL = ExerciseEmphasis(
    exercise="prone_leg_curl",
    muscle="hamstrings",
    region="biceps_femoris_long_head",
    emphasis=6.5 / 14.4,         # ~= 0.45
    confidence="high",
    source=CITATION,
    rationale="+6.5% biceps femoris long head volume vs +14.4% for the seated "
              "leg curl. Normalized. The largest seated-vs-prone gap of any "
              "hamstring muscle -- BFL is biarticular and is lengthened most "
              "by hip flexion.",
    population=POPULATION,
    quality_score=QUALITY,
)

# --- Semitendinosus (biarticular) -------------------------------------------

SEATED_LEG_CURL_ST = ExerciseEmphasis(
    exercise="seated_leg_curl",
    muscle="hamstrings",
    region="semitendinosus",
    emphasis=1.0,
    confidence="high",
    source=CITATION,
    rationale="+23.6% semitendinosus volume in 12 weeks -- the largest "
              "absolute growth of any hamstring muscle. Significantly greater "
              "than the prone leg curl (P <= 0.010).",
    population=POPULATION,
    quality_score=QUALITY,
)

PRONE_LEG_CURL_ST = ExerciseEmphasis(
    exercise="prone_leg_curl",
    muscle="hamstrings",
    region="semitendinosus",
    emphasis=19.3 / 23.6,        # ~= 0.82
    confidence="high",
    source=CITATION,
    rationale="+19.3% semitendinosus volume vs +23.6% for the seated leg "
              "curl. Normalized. The semitendinosus grew strongly in BOTH "
              "conditions, so the seated advantage is real but proportionally "
              "the smallest among the biarticular muscles.",
    population=POPULATION,
    quality_score=QUALITY,
)

# --- Semimembranosus (biarticular) ------------------------------------------

SEATED_LEG_CURL_SM = ExerciseEmphasis(
    exercise="seated_leg_curl",
    muscle="hamstrings",
    region="semimembranosus",
    emphasis=1.0,
    confidence="high",
    source=CITATION,
    rationale="+8.2% semimembranosus volume in 12 weeks. Significantly "
              "greater than the prone leg curl (P <= 0.010).",
    population=POPULATION,
    quality_score=QUALITY,
)

PRONE_LEG_CURL_SM = ExerciseEmphasis(
    exercise="prone_leg_curl",
    muscle="hamstrings",
    region="semimembranosus",
    emphasis=3.6 / 8.2,          # ~= 0.44
    confidence="high",
    source=CITATION,
    rationale="+3.6% semimembranosus volume vs +8.2% for the seated leg curl. "
              "Normalized. Roughly a 2-fold seated advantage.",
    population=POPULATION,
    quality_score=QUALITY,
)

# --- Biceps femoris short head (MONOARTICULAR) ------------------------------
# The short head crosses only the knee, so hip position does NOT change its
# muscle length. The paper found no significant seated-vs-prone difference
# (+10% vs +9%, P = 0.190). These two entries are encoded at confidence="low":
# they capture the observed near-equivalence, but the difference is within
# noise and the optimizer should treat the short head as position-agnostic.

SEATED_LEG_CURL_BFS = ExerciseEmphasis(
    exercise="seated_leg_curl",
    muscle="hamstrings",
    region="biceps_femoris_short_head",
    emphasis=1.0,
    confidence="low",            # difference n.s. (P = 0.190) -- see note above
    source=CITATION,
    rationale="+10% biceps femoris short head volume in 12 weeks. The "
              "seated-vs-prone difference was NOT significant (P = 0.190): the "
              "short head is monoarticular and is not lengthened differently "
              "by hip position. Encoded at confidence=low; treat the short "
              "head as roughly position-agnostic.",
    population=POPULATION,
    quality_score=QUALITY,
)

PRONE_LEG_CURL_BFS = ExerciseEmphasis(
    exercise="prone_leg_curl",
    muscle="hamstrings",
    region="biceps_femoris_short_head",
    emphasis=9.0 / 10.0,         # = 0.90 -- difference n.s.; effectively equal
    confidence="low",            # difference n.s. (P = 0.190)
    source=CITATION,
    rationale="+9% biceps femoris short head volume vs +10% for the seated "
              "leg curl -- NOT a significant difference (P = 0.190). The 0.90 "
              "coefficient should be read as 'effectively equal to seated', "
              "not as a real prone disadvantage. The paper reports these "
              "values to whole-percent precision only.",
    population=POPULATION,
    quality_score=QUALITY,
)


EMPHASIS_ESTIMATES: list[ExerciseEmphasis] = [
    SEATED_LEG_CURL_WHOLE,
    PRONE_LEG_CURL_WHOLE,
    SEATED_LEG_CURL_BFL,
    PRONE_LEG_CURL_BFL,
    SEATED_LEG_CURL_ST,
    PRONE_LEG_CURL_ST,
    SEATED_LEG_CURL_SM,
    PRONE_LEG_CURL_SM,
    SEATED_LEG_CURL_BFS,
    PRONE_LEG_CURL_BFS,
]


# ----------------------------------------------------------------------------
# Practical guidance derived from this paper
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
For the hamstrings, the SEATED leg curl (hip flexed) grew the muscle
substantially more than the PRONE / lying leg curl over 12 weeks of matched
training: +14.1% vs +9.3% whole-hamstrings MRI volume. The advantage was
present and significant in all three BIARTICULAR hamstrings -- biceps femoris
long head (+14.4% vs +6.5%), semitendinosus (+23.6% vs +19.3%) and
semimembranosus (+8.2% vs +3.6%) -- because hip flexion holds those muscles at
a longer length during the exercise. The MONOARTICULAR biceps femoris short
head, which hip position does not lengthen, showed no significant difference
(+10% vs +9%).

When prescribing isolated knee-flexion work for hamstrings hypertrophy, bias
toward the seated leg curl over the prone/lying variant. This is single-study
evidence in young untrained adults: the DIRECTION is solid, the exact emphasis
coefficients are provisional (see the module's method caveat). It is the
exercise-selection (Q1) counterpart to the muscle-length regional-hypertrophy
question that Varovic 2025 addresses meta-analytically (Q2); Maeo 2021 is in
fact one of Varovic's pooled studies, which is why it is encoded here as
emphasis only, not as a poolable regional effect.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Maeo 2021 -- quality {QUALITY}, n=20 within-participant (full text)")
    print(f"{len(EMPHASIS_ESTIMATES)} emphasis coefficients "
          f"(seated vs prone leg curl, hamstrings):")
    for em in EMPHASIS_ESTIMATES:
        region = em.region if em.region else "whole_muscle"
        print(f"  {em.exercise:<18} -> hamstrings/{region:<26}: "
              f"{em.emphasis:.2f} ({em.confidence})")
