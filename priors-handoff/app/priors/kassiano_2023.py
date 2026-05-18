"""
Kassiano W, Costa B, Kunevaliki G, Soares D, Zacarias G, Manske I, Takaki Y,
Ruggiero MF, Stavinski N, Francsuel J, Tricoli I, Carneiro MAS, Cyrino ES.
Greater Gastrocnemius Muscle Hypertrophy After Partial Range of Motion
Training Performed at Long Muscle Lengths.
Journal of Strength & Conditioning Research. 2023;37(9):1746-1753.
doi: 10.1519/JSC.0000000000004460
PMID: 37015016

KEY FINDING (8-week RCT, 42 young women, n=14 per group):

  Calf raise on a pin-loaded horizontal leg-press machine, 3 sets of 15-20RM,
  3x/week, trained in one of three ankle ranges of motion:

    FULL ROM     ankle -25 deg to +25 deg
    INITIAL ROM  ankle -25 deg to 0 deg   -> the LONG / stretched muscle
                                            length (gastrocnemius lengthened)
    FINAL ROM    ankle 0 deg to +25 deg   -> the SHORT muscle length
                                            (gastrocnemius shortened)

  Medial gastrocnemius muscle-thickness gain (B-mode ultrasound):
    INITIAL +15.2%  vs  FULL +6.7%  vs  FINAL +3.4%
    INITIAL greater than both FULL and FINAL (p <= 0.009).

  Lateral gastrocnemius muscle-thickness gain:
    INITIAL +14.9%  vs  FULL +7.3%  vs  FINAL +6.2%
    INITIAL greater than FINAL (p < 0.024); INITIAL vs FULL did NOT reach
    significance (p = 0.060).

Training the stretched portion of the calf-raise ROM substantially out-grew
both full ROM and the shortened portion. The medial-head result is clear; the
lateral-head result points the same way but the lengthened-vs-full gap is not
statistically significant.

----------------------------------------------------------------------------
ABSTRACT-ONLY ENCODING
----------------------------------------------------------------------------

The JSCR full text is paywalled (HTTP 402) and the ResearchGate copy is
blocked (403). Every VALUE encoded here comes from the published abstract,
which is complete for the % muscle-thickness changes, the p-values, n, the
ROM definitions, the protocol and the measurement method. The full
Methods/Results could NOT be inspected, so:
  - this module encodes ExerciseEmphasis coefficients only — no EffectEstimate,
    because the abstract reports no effect sizes, CIs or SEs;
  - the quality dimensions that need the full text (methodological rigor,
    reporting transparency, risk of bias, population specificity) are scored
    CONSERVATIVELY and flagged UNVERIFIED — see the quality block.

----------------------------------------------------------------------------
WHAT THIS PAPER IS FOR
----------------------------------------------------------------------------

This is the second ExerciseEmphasis source in the priors layer (after Maeo
2023, triceps) and the first for the lower body. It answers an
exercise/ROM-SELECTION question — "does training the calf raise at a long vs
short muscle length grow the (whole) gastrocnemius head more?" — analogous to
Maeo's overhead-vs-neutral question, NOT the within-muscle proximal/distal
"regional hypertrophy" question that Varovic 2025 found to be trivial.

It is also a strong single-study data point for the "lengthened partials"
effect that Wolf 2023's meta-analysis could only estimate weakly (SMD -0.28,
95% CI -0.81 to 0.16). Kassiano shows that, for the calf specifically, the
long-length partial clearly beats the short-length partial.
"""

from __future__ import annotations

from .shared import Citation, PopulationSpec, ExerciseEmphasis


# ----------------------------------------------------------------------------
# Citation
# ----------------------------------------------------------------------------

CITATION = Citation(
    authors="Kassiano et al.",
    year=2023,
    doi="10.1519/JSC.0000000000004460",
    journal="Journal of Strength & Conditioning Research",
)


# ----------------------------------------------------------------------------
# Quality assessment (per QUALITY_RUBRIC.md v1.0)
# ----------------------------------------------------------------------------
# ABSTRACT-ONLY ENCODING (full text paywalled — see module docstring). Values
# are abstract-complete; the dimensions needing the full Methods/Results are
# conservative estimates flagged UNVERIFIED.
# Study design     0.85 (parallel-group RCT, randomized to 3 ROM conditions,
#                  8-week intervention; pre-registration status unverifiable)
# Sample size      0.70 (n=14 per arm — rubric's 10-14 band)
# Measurement      0.90 (site-specific medial + lateral gastrocnemius muscle
#                  thickness by B-mode ultrasound — rubric's 0.9 tier)
# Methodological   0.75 (UNVERIFIED — full Methods not inspectable; abstract
#                  shows randomization and a standardized 15-20RM load)
# Reporting        0.65 (UNVERIFIED — abstract gives % changes + p-values but
#                  no effect sizes or CIs; full-text reporting not inspectable)
# Risk of bias     0.82 (UNVERIFIED — academic Brazilian research group, no
#                  obvious commercial conflict; funding/COI not in the abstract)
# Population       0.70 (single-sex young-adult sample, reasonably specific;
#                  age range and training status not stated in the abstract)
# Weighted average: 0.784 -> 0.78. No flat modifiers applied: the abstract-only
# limitation is already reflected in the four conservative dimension scores
# rather than double-counted via the access modifier.
QUALITY = 0.78


# ----------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------

POPULATION = PopulationSpec(
    training_status="untrained",
    sex="female",
    # The abstract says "young women" — no explicit age range. (18, 30) is the
    # young-adult envelope, not a paper figure.
    age_range=(18, 30),
    outcome="hypertrophy",
    notes="42 young women, 14 per ROM group. Training status is INFERRED as "
          "untrained — the abstract does not state it, but 6-15% muscle "
          "thickness gain in 8 weeks is a novice-range response. Confirm "
          "against the full text if it becomes accessible.",
)


# ----------------------------------------------------------------------------
# Exercise emphasis coefficients
# ----------------------------------------------------------------------------
# Derived from the abstract's muscle-thickness % gains, normalized within each
# gastrocnemius head to the best-growing ROM variant (the lengthened partial).
# Three ROM configurations of the calf raise are encoded as three distinct
# exercise keys (the same way Maeo 2023 encodes overhead vs neutral extension
# as distinct exercises).
#
# PROVISIONAL — METHOD CAVEAT (same as maeo_2023): shared.py defines `emphasis`
# as a study-independent "fraction of maximum stimulus." A ratio of 8-week
# percent-growth outcomes is NOT that — it is intervention-, duration- and
# population-specific, and its implicit zero is anchored at "the weakest of
# three real ROM variants" rather than "no stimulus" (the shortened partial
# still grew the medial head +3.4%). Treat these six values as a PROVISIONAL
# within-this-study relative ranking, not stable exercise constants; the
# optimizer should consume them as soft priors with wide uncertainty.
#
# Normalizing the lengthened-partial calf raise to 1.0 for the gastrocnemius,
# while Maeo's overhead extension is also 1.0 for the triceps, is intentional
# and fine — emphasis is WITHIN-muscle relative, not across muscles (BACKLOG.md
# open question 3).
#
# Confidence: medial-head entries are "high" — INITIAL ROM significantly beat
# both FULL and FINAL (p <= 0.009). Lateral-head entries are "medium" — INITIAL
# beat FINAL (p < 0.024) but the INITIAL-vs-FULL gap was NOT significant
# (p = 0.060), so the lateral lengthened-vs-full ranking is uncertain.

# --- Medial gastrocnemius ---------------------------------------------------

LENGTHENED_PARTIAL_CALF_RAISE_MEDIAL = ExerciseEmphasis(
    exercise="lengthened_partial_calf_raise",
    muscle="gastrocnemius",
    region="medial_head",
    emphasis=1.0,            # reference: best-growing ROM variant in this study
    confidence="high",
    source=CITATION,
    rationale="+15.2% medial gastrocnemius thickness in 8 weeks (INITIAL ROM, "
              "ankle -25 to 0 deg = long muscle length). Significantly greater "
              "than full ROM and the shortened partial (p <= 0.009).",
    population=POPULATION,
    quality_score=QUALITY,
)

FULL_ROM_CALF_RAISE_MEDIAL = ExerciseEmphasis(
    exercise="full_rom_calf_raise",
    muscle="gastrocnemius",
    region="medial_head",
    emphasis=6.7 / 15.2,     # ~= 0.44
    confidence="high",
    source=CITATION,
    rationale="+6.7% medial gastrocnemius thickness vs +15.2% for the "
              "lengthened partial. Normalized to the lengthened partial = 1.0.",
    population=POPULATION,
    quality_score=QUALITY,
)

SHORTENED_PARTIAL_CALF_RAISE_MEDIAL = ExerciseEmphasis(
    exercise="shortened_partial_calf_raise",
    muscle="gastrocnemius",
    region="medial_head",
    emphasis=3.4 / 15.2,     # ~= 0.22
    confidence="high",
    source=CITATION,
    rationale="+3.4% medial gastrocnemius thickness vs +15.2% for the "
              "lengthened partial (FINAL ROM, ankle 0 to +25 deg = short "
              "muscle length). Clearly the weakest variant for the medial head.",
    population=POPULATION,
    quality_score=QUALITY,
)

# --- Lateral gastrocnemius --------------------------------------------------

LENGTHENED_PARTIAL_CALF_RAISE_LATERAL = ExerciseEmphasis(
    exercise="lengthened_partial_calf_raise",
    muscle="gastrocnemius",
    region="lateral_head",
    emphasis=1.0,            # reference: best-growing ROM variant in this study
    confidence="medium",     # INITIAL vs FULL not significant for this head
    source=CITATION,
    rationale="+14.9% lateral gastrocnemius thickness in 8 weeks (INITIAL ROM). "
              "Significantly greater than the shortened partial (p < 0.024); "
              "the gap over full ROM did NOT reach significance (p = 0.060).",
    population=POPULATION,
    quality_score=QUALITY,
)

FULL_ROM_CALF_RAISE_LATERAL = ExerciseEmphasis(
    exercise="full_rom_calf_raise",
    muscle="gastrocnemius",
    region="lateral_head",
    emphasis=7.3 / 14.9,     # ~= 0.49
    confidence="medium",
    source=CITATION,
    rationale="+7.3% lateral gastrocnemius thickness vs +14.9% for the "
              "lengthened partial. Normalized. The lengthened-vs-full "
              "difference for the lateral head was not significant (p = 0.060), "
              "so this 0.49 vs 1.0 ranking is uncertain.",
    population=POPULATION,
    quality_score=QUALITY,
)

SHORTENED_PARTIAL_CALF_RAISE_LATERAL = ExerciseEmphasis(
    exercise="shortened_partial_calf_raise",
    muscle="gastrocnemius",
    region="lateral_head",
    emphasis=6.2 / 14.9,     # ~= 0.42
    confidence="medium",
    source=CITATION,
    rationale="+6.2% lateral gastrocnemius thickness vs +14.9% for the "
              "lengthened partial (FINAL ROM, short muscle length). "
              "Significantly below the lengthened partial (p < 0.024).",
    population=POPULATION,
    quality_score=QUALITY,
)


EMPHASIS_ESTIMATES: list[ExerciseEmphasis] = [
    LENGTHENED_PARTIAL_CALF_RAISE_MEDIAL,
    FULL_ROM_CALF_RAISE_MEDIAL,
    SHORTENED_PARTIAL_CALF_RAISE_MEDIAL,
    LENGTHENED_PARTIAL_CALF_RAISE_LATERAL,
    FULL_ROM_CALF_RAISE_LATERAL,
    SHORTENED_PARTIAL_CALF_RAISE_LATERAL,
]


# ----------------------------------------------------------------------------
# Practical guidance
# ----------------------------------------------------------------------------

GUIDANCE_FOR_OPTIMIZER = """
For the gastrocnemius, calf raises trained at LONG muscle lengths — the bottom,
stretched portion of the range (ankle dorsiflexed) — produced substantially
more muscle-thickness growth over 8 weeks than full ROM or short-length
partials. The medial head showed this clearly (lengthened partial +15.2% vs
full +6.7% vs short +3.4%); the lateral head pointed the same way but the
lengthened-vs-full gap did not reach significance.

When prescribing calf work for hypertrophy, bias toward the stretched portion
of the calf-raise ROM. This is single-study evidence in untrained young women:
the DIRECTION is solid, the exact emphasis coefficients are provisional (see
the module's method caveat). It corroborates Wolf 2023's long-length-partial
sub-finding for one specific muscle.
"""


# ----------------------------------------------------------------------------
# Sanity check
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Kassiano 2023 — quality {QUALITY}, abstract-only encoding")
    print(f"{len(EMPHASIS_ESTIMATES)} emphasis coefficients:")
    for em in EMPHASIS_ESTIMATES:
        print(f"  {em.exercise:<32} -> {em.muscle}/{em.region}: "
              f"{em.emphasis:.2f} ({em.confidence})")
