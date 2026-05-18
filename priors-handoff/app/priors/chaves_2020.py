"""
Chaves SFN, Rocha-Junior VA, Encarnacao IGA, Martins-Costa HC, Freitas EDS,
Coelho DB, Franco FSC, Loenneke JP, Bottaro M, Ferreira-Junior JB.
Effects of Horizontal and Incline Bench Press on Neuromuscular Adaptations in
Untrained Young Men.
International Journal of Exercise Science. 2020;13(6):859-872.
doi: 10.70252/FDNB1158
PMID: 32922646 . PMC7449336 (open access)

KEY FINDING (8-week, once-weekly, parallel-group RCT; 72 enrolled, 47 completed
the training protocol, pectoralis MUSCLE THICKNESS measured in 30 -- 10/group):

  Untrained men randomised to one of three bench-press training conditions
  for 8 weeks:
    - Horizontal-only bench press   (4-6 sets/session)
    - Incline-only bench press      (4-6 sets/session, ~30-45 deg incline)
    - Combination of both           (2-3 sets of each per session)
  All groups: 8-12 RM to failure, 2 s concentric / 2 s eccentric, 90 s rest.
  47 men completed the 8-week training protocol (15/15/17 per arm), but the
  pectoralis-thickness data -- the SOLE basis for every emphasis coefficient
  in this module -- was collected on a 30-subject subsample, 10 per group.
  The 47 / 15-17-per-arm figures are training-completer counts (and the n for
  the paper's isometric-strength outcome), NOT the n behind this module.

  Pectoralis major thickness was measured by B-mode ultrasound (Mindray DP-30,
  7.5 MHz probe) at THREE sites under the clavicle midpoint:
    - 2nd intercostal space -> CLAVICULAR head (upper chest)
    - 3rd intercostal space -> STERNOCOSTAL head (mid)
    - 5th intercostal space -> STERNOCOSTAL head (lower)

  Muscle thickness, mm, mean (SD), pre -> post:

    2nd intercostal (clavicular):
      Horizontal     11.9 (2.0) -> 15.7 (3.9)
      Incline        15.1 (3.8) -> 24.5 (4.1)
      Combination    14.3 (5.3) -> 18.8 (6.5)
    3rd intercostal (sternocostal):
      Horizontal     13.2 (3.5) -> 19.3 (5.0)
      Incline        15.4 (4.3) -> 23.8 (5.7)
      Combination    17.1 (5.0) -> 21.2 (4.9)
    5th intercostal (sternocostal):
      Horizontal     12.6 (2.7) -> 18.0 (5.1)
      Incline        14.4 (4.2) -> 22.8 (5.4)
      Combination    16.0 (5.5) -> 22.7 (5.9)

  The ONLY significant between-group difference was at the 2nd intercostal
  (clavicular / upper-chest) site (ANOVA P = 0.005):
    - Incline > Horizontal   (difference 0.62 cm, P = 0.003)
    - Incline > Combination  (difference 0.50 cm, P = 0.008)
    - Horizontal vs Combination: P = 0.524 (n.s.)
  The 3rd intercostal (P = 0.095) and 5th intercostal (P = 0.227) sternocostal
  sites showed NO significant between-group difference: all three exercises
  grew the mid/lower pectoralis comparably.

  Mechanistic core: the incline press preferentially grows the CLAVICULAR
  (upper) head of the pectoralis major. It does NOT preferentially grow the
  sternocostal (mid/lower) head -- there the three exercises are equivalent.
  The combination group's clavicular growth was no better than horizontal's:
  diluting incline volume with horizontal work erased the upper-chest benefit.

THIS MODULE ENCODES ExerciseEmphasis ONLY -- and deliberately so.

  This is an exercise-vs-exercise SELECTION question (Research Goal 1): "which
  bench-press variant grows which part of the pectoralis major?" It is not a
  dose-response question and maps to no registry `Topic`. Like maeo_2021,
  maeo_2023 and kassiano_2023, the data enters the SEPARATE emphasis index,
  keyed (exercise, muscle, region) and combined by quality-weighted averaging
  -- never the inverse-variance Topic pool. So this module exports NO
  Topic-keyed EffectEstimate, adds NO `Topic`, and needs NO _POOLABLE_OVERRIDE
  entry. See docs/priors/relevance/chaves_2020_relevance.md.

  (The closest existing Topic, ARM_POSITION_HYPERTROPHY, is about joint
  position WITHIN a single movement (Maeo 2023, overhead vs neutral elbow
  extension) and is a poolable whole-muscle SMD -- a different shape from a
  per-exercise emphasis coefficient. Bench-press inclination is a
  between-EXERCISE contrast and belongs in the emphasis index.)

This is the first chest / pectoralis-major source in the priors layer and the
fourth ExerciseEmphasis source (after Maeo 2023 triceps, Kassiano 2023
gastrocnemius, Maeo 2021 hamstrings, Plotkin 2023 gluteus maximus).

CONFIDENCE (mirrors how maeo_2021 / kassiano_2023 handle non-significant pairs):
  - The CLAVICULAR-head emphasis pairs are encoded at confidence="high": the
    incline > horizontal upper-chest advantage is the paper's one robust,
    significant between-group result (P = 0.003 / 0.008).
  - The two STERNOCOSTAL-head emphasis pairs are encoded at confidence="low":
    the between-group differences there were NOT significant (P = 0.095 at the
    3rd intercostal, P = 0.227 at the 5th). The fractional coefficients should
    be read as "effectively equal across exercises", not as a real ranking.

CAVEATS (carried into QUALITY and POPULATION):
  - Once-weekly training frequency -- unusually low; an 8-week, 1x/week dose is
    a weak stimulus relative to the 2-3x/week norm. The DIRECTION of the
    incline upper-chest advantage is the durable finding; the magnitude is
    dose-specific.
  - Untrained men only; small per-group n (15-17). Findings may not transfer to
    trained lifters or to women.
  - PROVISIONAL emphasis scale -- see the METHOD CAVEAT block below; the same
    caveat carried by every sibling emphasis module.
  - International Journal of Exercise Science is a smaller open-access journal
    (legitimately PubMed-indexed, not predatory -- no journal-quality flat
    modifier applied; see QUALITY notes).
  - UNVERIFIED: the accessible PMC full text did not surface an explicit
    funding statement, conflict-of-interest declaration, or trial-registration
    entry. Risk-of-bias and methodological-rigor scores reflect that absence
    conservatively -- see QUALITY notes.
"""

from __future__ import annotations

from .shared import Citation, PopulationSpec, ExerciseEmphasis


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Chaves et al.",
    year=2020,
    doi="10.70252/FDNB1158",
    journal="International Journal of Exercise Science",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# Full open-access text inspected (PMC7449336).
#
# Study design     0.85 -- parallel-group RANDOMISED controlled training trial,
#                  three arms, allocation randomised. No control (non-training)
#                  group, but the design is an exercise-vs-exercise contrast so
#                  a non-training arm is not required. No pre-registration
#                  found. Rubric's "RCT with minor design issues" band (0.9);
#                  held one notch lower at 0.85 for no pre-reg and a non-blinded
#                  intervention with no documented intention-to-treat handling.
# Sample size      0.70 (the encoded muscle-thickness outcome rests on a
#                  30-subject subsample, n=10 per arm -- rubric's 10-14 band,
#                  0.70. The 15/15/17 training-completer split is NOT the n
#                  behind the emphasis coefficients -- see the docstring.)
# Measurement      0.90 (site-specific pectoralis muscle thickness via B-mode
#                  ultrasound at three defined intercostal landmarks -- the
#                  rubric's high-quality ultrasound-MT row, 0.90. NOTE: the
#                  accessible full text did not report a measurement-reliability
#                  ICC/CV or explicit assessor blinding; this is the standard,
#                  validated MT method for chest hypertrophy, so the row is held
#                  at 0.90 rather than discounted, but the gap is logged.)
# Methodological   0.65 (per-protocol analysis -- 25 of 72 enrolled excluded,
#                  including for <80% attendance and for altered nutrition;
#                  the muscle-thickness outcome is a further 30/47 subsample
#                  with no stated selection mechanism; one-way ANOVA on change
#                  scores with post-hoc tests; no pre-registration, no
#                  documented missing-data handling, no multiple-comparison
#                  correction stated. Rubric 0.5-0.7 band; scored 0.65:
#                  competent standard methods but several rigor gaps.)
# Reporting        0.70 (full pre/post means with SDs for every site x group,
#                  ANOVA + post-hoc p-values and the 0.62/0.50 cm post-hoc
#                  differences reported in the body text. Held at 0.70 because
#                  between-group effect sizes with CIs are not given for the
#                  thickness outcomes -- only means/SDs and p-values -- so a
#                  reader must reconstruct any effect size, and no raw data or
#                  analysis code is deposited.)
# Risk of bias     0.80 -- DEVIATION, documented. The accessible full text did
#                  not surface an explicit funding statement or COI
#                  declaration. The rubric's top band requires a clean
#                  disclosure; absent one, a plain-academic context is the
#                  reasonable default (the finding favours a training position,
#                  not a commercial product, and the journal -- IJES, published
#                  by a university kinesiology program -- is non-commercial).
#                  Scored 0.80, one notch below the 0.90 disclosed-academic
#                  tier, to reflect the UNVERIFIED disclosure rather than assume
#                  the best case. The rubric's "don't score below 0.6 just
#                  because authors are in the industry" guidance is respected:
#                  there is no evidence of a conflict, only an unverified
#                  statement.
# Population       0.85 (untrained young men, 18-30, with explicit PAR-Q
#                  screening, a 6-month no-resistance-training criterion and a
#                  documented moderate-activity inclusion; mean 21.1 y. Tight,
#                  single-sex, well-described population. Rubric 0.9 band trimmed
#                  to 0.85 for the per-protocol exclusions narrowing the
#                  analysed sample.)
# Weighted average:
#   0.85*0.20 + 0.70*0.15 + 0.90*0.20 + 0.65*0.15 + 0.70*0.10 + 0.80*0.10
#   + 0.85*0.10
#   = 0.170 + 0.105 + 0.180 + 0.0975 + 0.070 + 0.080 + 0.085
#   = 0.7875 -> 0.79
#
# Flat modifiers: NONE. International Journal of Exercise Science is a smaller
# open-access journal but is PubMed-indexed and not on Beall's predatory list,
# so the "predatory / low-quality journal" x0.7 modifier does NOT apply. The
# once-weekly frequency and untrained-men limitations are applicability
# concerns (handled by PopulationSpec.applicability_to), not quality penalties,
# and are documented in POPULATION and the module docstring.
QUALITY = 0.79


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------

POPULATION = PopulationSpec(
    training_status="untrained",
    sex="male",
    # Inclusion criterion: men aged 18-30. Reported sample mean 21.1 +/- 3.3 y.
    age_range=(18, 30),
    outcome="hypertrophy",
    notes="Untrained young men (mean 21.1 y, 71.9 kg, 176 cm), randomised to "
          "horizontal-only, incline-only or combination bench press. 72 "
          "enrolled; 47 completed the 8-week training protocol (15/15/17 per "
          "arm); the pectoralis MUSCLE-THICKNESS outcome encoded here was "
          "measured on a 30-subject subsample, 10 per group -- that, not 47, "
          "is the n behind every emphasis coefficient in this module. "
          "Inclusion: 18-30 y, PAR-Q clear, moderately active ~3 d/week, no "
          "resistance training in the prior 6 months. 8-week parallel-group "
          "RCT. CAVEAT: training frequency was only ONCE WEEKLY (8-12 RM to "
          "failure, 2 s/2 s tempo, 90 s rest; horizontal/incline 4-6 sets, "
          "combination 2-3 sets of each). Per-protocol analysis: 25 of 72 "
          "enrolled were excluded (attendance <80%, altered nutrition). "
          "Single-sex, untrained -- transfer to trained lifters or to women "
          "is unverified.",
)


# ----------------------------------------------------------------------------
# Exercise emphasis coefficients
# ----------------------------------------------------------------------------
# Derived from the per-site muscle-thickness % growth, normalised WITHIN each
# (muscle, region) to the highest-growth exercise at that site. Three exercise
# keys -- "incline_bench_press", "horizontal_bench_press",
# "combination_bench_press" -- mirror how maeo_2021 / maeo_2023 / kassiano_2023
# encode multiple exercise variants for one muscle.
#
# % growth used for the ratios = (post - pre) / pre * 100, computed from the
# mm means above:
#
#   2nd intercostal (CLAVICULAR head):
#     Horizontal   (15.7 - 11.9) / 11.9 = +31.9%
#     Incline      (24.5 - 15.1) / 15.1 = +62.3%   <- reference (1.0)
#     Combination  (18.8 - 14.3) / 14.3 = +31.5%
#   3rd intercostal (STERNOCOSTAL head, mid):
#     Horizontal   (19.3 - 13.2) / 13.2 = +46.2%
#     Incline      (23.8 - 15.4) / 15.4 = +54.5%   <- highest at this site
#     Combination  (21.2 - 17.1) / 17.1 = +24.0%
#   5th intercostal (STERNOCOSTAL head, lower):
#     Horizontal   (18.0 - 12.6) / 12.6 = +42.9%
#     Incline      (22.8 - 14.4) / 14.4 = +58.3%   <- highest at this site
#     Combination  (22.7 - 16.0) / 16.0 = +41.9%
#
# The two sternocostal sites (3rd, 5th intercostal) both measure the
# STERNOCOSTAL head. They are encoded as ONE region key,
# "sternocostal_head", using the 3rd-intercostal (mid) site as the
# representative -- the relevance-checker's mapping. The 3rd intercostal is the
# primary mid-sternocostal landmark; the 5th-intercostal numbers are noted in
# rationale strings for transparency. Both sites agreed: no significant
# between-group difference, incline numerically highest, combination lowest.
#
# PROVISIONAL -- METHOD CAVEAT (same as maeo_2023 / maeo_2021 / kassiano_2023):
# shared.py defines `emphasis` as a study-independent "fraction of maximum
# stimulus." A ratio of 8-week percent-thickness-growth outcomes is NOT that --
# it is intervention-, frequency-, duration- and population-specific (here,
# once-weekly training in untrained men), and its implicit zero is anchored at
# "the weaker of the bench-press variants tested", not at no stimulus
# (horizontal press still grew the clavicular head +31.9%). It will not
# generalise across studies with different baselines, frequencies or
# measurement modalities. Treat the values below as a PROVISIONAL
# within-this-study relative ranking, not stable exercise constants; the
# optimizer should consume them as soft priors with wide uncertainty. The
# "high" confidence on the clavicular pairs means the DIRECTION of the incline
# upper-chest advantage is well established -- NOT that the exact ratios are
# precise.
#
# Normalising the incline press to 1.0 for the clavicular head, while Maeo
# 2023's overhead extension is 1.0 for the triceps etc., is intentional and
# fine: emphasis is WITHIN-(muscle, region) relative, never across muscles
# (BACKLOG.md open question 3).

# --- Clavicular head (2nd intercostal / upper chest) ------------------------
# SIGNIFICANT between-group result: incline > horizontal (P = 0.003) and
# incline > combination (P = 0.008). Encoded at confidence="high".

INCLINE_BENCH_PRESS_CLAVICULAR = ExerciseEmphasis(
    exercise="incline_bench_press",
    muscle="pectoralis_major",
    region="clavicular_head",
    emphasis=1.0,                 # reference: highest-growth variant at this site
    confidence="high",
    source=CITATION,
    rationale="+62.3% clavicular (upper-chest, 2nd intercostal) pectoralis "
              "thickness in 8 weeks. Significantly greater than the horizontal "
              "bench press (P = 0.003) and the combination group (P = 0.008). "
              "Reference exercise for the clavicular head.",
    population=POPULATION,
    quality_score=QUALITY,
)

HORIZONTAL_BENCH_PRESS_CLAVICULAR = ExerciseEmphasis(
    exercise="horizontal_bench_press",
    muscle="pectoralis_major",
    region="clavicular_head",
    emphasis=31.9 / 62.3,         # ~= 0.51
    confidence="high",
    source=CITATION,
    rationale="+31.9% clavicular thickness vs +62.3% for the incline press. "
              "Normalized to incline = 1.0. The horizontal (flat) bench press "
              "provides roughly half the upper-chest stimulus of the incline "
              "press; the incline advantage was statistically significant "
              "(P = 0.003).",
    population=POPULATION,
    quality_score=QUALITY,
)

COMBINATION_BENCH_PRESS_CLAVICULAR = ExerciseEmphasis(
    exercise="combination_bench_press",
    muscle="pectoralis_major",
    region="clavicular_head",
    emphasis=31.5 / 62.3,         # ~= 0.51
    confidence="high",
    source=CITATION,
    rationale="+31.5% clavicular thickness vs +62.3% for the incline-only "
              "press. Normalized. Mixing horizontal work into the program "
              "(2-3 sets of each) erased the upper-chest benefit: combination "
              "clavicular growth was no better than horizontal-only and "
              "significantly below incline-only (P = 0.008). For an upper-chest "
              "goal, incline volume should not be diluted with flat pressing.",
    population=POPULATION,
    quality_score=QUALITY,
)

# --- Sternocostal head (3rd / 5th intercostal / mid-lower chest) ------------
# NO significant between-group difference at either sternocostal site (3rd
# intercostal P = 0.095, 5th intercostal P = 0.227). All three exercises grew
# the sternocostal head comparably. Encoded at confidence="low": the
# coefficients capture the observed near-equivalence, but the differences are
# within noise -- the optimizer should treat the mid/lower chest as roughly
# bench-angle-agnostic. Mirrors how maeo_2021 encodes the non-significant
# biceps-femoris-short-head pair.

INCLINE_BENCH_PRESS_STERNOCOSTAL = ExerciseEmphasis(
    exercise="incline_bench_press",
    muscle="pectoralis_major",
    region="sternocostal_head",
    emphasis=1.0,                 # numerically highest, but difference n.s.
    confidence="low",             # between-group difference n.s. -- see note above
    source=CITATION,
    rationale="+54.5% sternocostal (mid, 3rd intercostal) pectoralis thickness "
              "in 8 weeks; +58.3% at the lower (5th intercostal) site. The "
              "incline press was numerically highest at both sternocostal "
              "sites, but the between-group difference was NOT significant "
              "(3rd intercostal P = 0.095, 5th intercostal P = 0.227). "
              "Encoded at confidence=low: treat the mid/lower chest as roughly "
              "bench-angle-agnostic.",
    population=POPULATION,
    quality_score=QUALITY,
)

HORIZONTAL_BENCH_PRESS_STERNOCOSTAL = ExerciseEmphasis(
    exercise="horizontal_bench_press",
    muscle="pectoralis_major",
    region="sternocostal_head",
    emphasis=46.2 / 54.5,         # ~= 0.85 -- difference n.s.; effectively equal
    confidence="low",             # between-group difference n.s. (P = 0.095)
    source=CITATION,
    rationale="+46.2% sternocostal (mid, 3rd intercostal) thickness vs +54.5% "
              "for the incline press; +42.9% vs +58.3% at the lower (5th "
              "intercostal) site. NOT a significant difference (3rd "
              "intercostal P = 0.095, 5th P = 0.227). The 0.85 coefficient "
              "should be read as 'effectively equal to incline' for the "
              "mid/lower chest, not as a real horizontal disadvantage.",
    population=POPULATION,
    quality_score=QUALITY,
)

COMBINATION_BENCH_PRESS_STERNOCOSTAL = ExerciseEmphasis(
    exercise="combination_bench_press",
    muscle="pectoralis_major",
    region="sternocostal_head",
    emphasis=24.0 / 54.5,         # ~= 0.44 -- difference n.s.; effectively equal
    confidence="low",             # between-group difference n.s. (P = 0.095)
    source=CITATION,
    rationale="+24.0% sternocostal (mid, 3rd intercostal) thickness vs +54.5% "
              "for the incline press; +41.9% vs +58.3% at the lower (5th "
              "intercostal) site. The 3rd-intercostal number is the lowest of "
              "the three groups, but the between-group difference was NOT "
              "significant (P = 0.095) and the 5th-intercostal site put "
              "combination on par with horizontal. Encoded at confidence=low: "
              "do not read the 0.44 as a real combination deficit -- the "
              "mid/lower chest is bench-angle-agnostic within this study.",
    population=POPULATION,
    quality_score=QUALITY,
)


EMPHASIS_ESTIMATES: list[ExerciseEmphasis] = [
    INCLINE_BENCH_PRESS_CLAVICULAR,
    HORIZONTAL_BENCH_PRESS_CLAVICULAR,
    COMBINATION_BENCH_PRESS_CLAVICULAR,
    INCLINE_BENCH_PRESS_STERNOCOSTAL,
    HORIZONTAL_BENCH_PRESS_STERNOCOSTAL,
    COMBINATION_BENCH_PRESS_STERNOCOSTAL,
]


# ----------------------------------------------------------------------------
# Practical guidance derived from this paper
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
For the pectoralis major, bench-press inclination matters for the CLAVICULAR
(upper) head but not for the STERNOCOSTAL (mid/lower) head. Over 8 weeks of
once-weekly training in untrained men, the INCLINE bench press grew the upper
chest substantially more than the flat (horizontal) press: +62% vs +32%
clavicular muscle thickness, a significant difference (P = 0.003). The
mid/lower chest grew comparably with every variant -- no significant
between-group difference at either sternocostal site (P = 0.095, P = 0.227).

A combination program (some flat, some incline pressing) did NOT preserve the
upper-chest benefit: its clavicular growth (+31%) matched the flat press, not
the incline press, and was significantly below incline-only (P = 0.008).
Diluting incline volume with flat work appears to cost the upper-chest gain.

When prescribing for an UPPER-CHEST (clavicular) hypertrophy goal, bias toward
the incline bench press and do not crowd it out with flat pressing. When the
goal is mid/lower chest, bench angle can be chosen on other grounds (loadability,
shoulder comfort) -- this study found no thickness advantage for either angle
there.

This is single-study evidence in untrained young men trained only ONCE PER
WEEK: the DIRECTION of the incline upper-chest advantage is solid, the exact
emphasis coefficients are provisional (see the module's method caveat), and
transfer to trained lifters, to women, and to higher training frequencies is
unverified. It is the first chest exercise-selection (Goal 1) source in the
layer.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Chaves 2020 -- quality {QUALITY}, muscle-thickness n=30 (10/group; "
          f"47 completed the training protocol) parallel-group RCT")
    print(f"{len(EMPHASIS_ESTIMATES)} emphasis coefficients "
          f"(incline vs horizontal vs combination bench press, "
          f"pectoralis major):")
    for em in EMPHASIS_ESTIMATES:
        region = em.region if em.region else "whole_muscle"
        print(f"  {em.exercise:<24} -> pectoralis_major/{region:<18}: "
              f"{em.emphasis:.2f} ({em.confidence})")
