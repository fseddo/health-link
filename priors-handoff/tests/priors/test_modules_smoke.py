"""
Smoke tests for the individual paper modules.

Two layers:
  1. Generic invariants every encoded estimate must satisfy (valid SE, quality
     in range, emphasis in [0, 1], CI ordered, n_studies sane).
  2. Specific known-value checks that lock in the corrections from the
     2026-05-17 literature audit (docs/priors/audits/) so a regression that
     re-introduces a fixed bug fails loudly.

Run from the priors-handoff root:  python -m pytest tests/priors/
"""

import math

import pytest

from app.priors import (
    pelland_2026,
    failure_effects,
    maeo_2023,
    maeo_2021,
    varovic_2025,
    wolf_2023,
    schoenfeld_2017,
    kassiano_2023,
    pedrosa_2023,
    schoenfeld_load_2017,
    singer_2024,
    plotkin_2023,
    chaves_2020,
    exercise_involvement,
)
from app.priors.shared import (
    EffectEstimate,
    ExerciseEmphasis,
    ExerciseInvolvement,
    MechanisticEmphasis,
    UserProfile,
    combine_for_user,
)
from app.priors.mechanistic import lats as mechanistic_lats
from app.priors.mechanistic import deltoids as mechanistic_deltoids


# ---------------------------------------------------------------------------
# Collect everything the modules export, so the generic checks see it all.
# ---------------------------------------------------------------------------

EFFECT_LISTS = {
    "pelland.VOLUME_HYPERTROPHY": pelland_2026.VOLUME_HYPERTROPHY_ESTIMATES,
    "pelland.VOLUME_STRENGTH": pelland_2026.VOLUME_STRENGTH_ESTIMATES,
    "pelland.FREQUENCY_HYPERTROPHY": pelland_2026.FREQUENCY_HYPERTROPHY_ESTIMATES,
    "pelland.FREQUENCY_STRENGTH": pelland_2026.FREQUENCY_STRENGTH_ESTIMATES,
    "failure.HYPERTROPHY": failure_effects.HYPERTROPHY_ESTIMATES,
    "failure.STRENGTH": failure_effects.STRENGTH_ESTIMATES,
    "maeo.WHOLE_MUSCLE": maeo_2023.WHOLE_MUSCLE_EFFECTS,
    "varovic.REGIONAL": varovic_2025.REGIONAL_ESTIMATES,
    "wolf.HYPERTROPHY": wolf_2023.HYPERTROPHY_ESTIMATES,
    "wolf.STRENGTH": wolf_2023.STRENGTH_ESTIMATES,
    "schoenfeld.VOLUME_HYPERTROPHY": schoenfeld_2017.VOLUME_HYPERTROPHY_ESTIMATES,
    "pedrosa.REGIONAL": pedrosa_2023.REGIONAL_ESTIMATES,
    "schoenfeld_load.HYPERTROPHY": schoenfeld_load_2017.LOAD_HYPERTROPHY_ESTIMATES,
    "schoenfeld_load.STRENGTH": schoenfeld_load_2017.LOAD_STRENGTH_ESTIMATES,
    "singer.HYPERTROPHY": singer_2024.HYPERTROPHY_ESTIMATES,
    "plotkin.EXERCISE_SELECTION": plotkin_2023.EXERCISE_SELECTION_ESTIMATES,
}

ALL_EFFECTS = [
    pytest.param(e, id=f"{name}[{i}]")
    for name, lst in EFFECT_LISTS.items()
    for i, e in enumerate(lst)
]

EMPHASIS_LISTS = {
    "maeo": maeo_2023.EMPHASIS_ESTIMATES,
    "kassiano": kassiano_2023.EMPHASIS_ESTIMATES,
    "maeo_2021": maeo_2021.EMPHASIS_ESTIMATES,
    "plotkin": plotkin_2023.EMPHASIS_ESTIMATES,
    "chaves": chaves_2020.EMPHASIS_ESTIMATES,
}

ALL_EMPHASIS = [
    pytest.param(e, id=f"{name}.EMPHASIS[{i}]")
    for name, lst in EMPHASIS_LISTS.items()
    for i, e in enumerate(lst)
]


# ---------------------------------------------------------------------------
# Generic invariants
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("e", ALL_EFFECTS)
def test_effect_estimate_invariants(e):
    assert isinstance(e, EffectEstimate)
    assert e.se > 0
    assert 0.0 <= e.quality_score <= 1.0
    assert e.n > 0
    assert e.scale, "scale string must be non-empty"
    lo, hi = e.ci_95
    assert lo < hi
    if e.n_studies is not None:
        assert e.n_studies > 0


@pytest.mark.parametrize("e", ALL_EMPHASIS)
def test_exercise_emphasis_invariants(e):
    assert isinstance(e, ExerciseEmphasis)
    assert 0.0 <= e.emphasis <= 1.0
    assert e.confidence in ("high", "medium", "low", "speculative")
    assert 0.0 <= e.quality_score <= 1.0


# ---------------------------------------------------------------------------
# Pelland 2026
# ---------------------------------------------------------------------------

def test_pelland_quality_and_headline_slope():
    assert pelland_2026.QUALITY == 0.94
    e = pelland_2026.VOLUME_HYPERTROPHY_SLOPE
    assert e.mean == 0.24
    assert e.n == 1032


def test_pelland_population_is_mixed_not_trained():
    # Audit fix: the marginal slopes marginalise across training status, so
    # the population must be "mixed". Regressing to "trained" is the bug.
    for e in (pelland_2026.VOLUME_HYPERTROPHY_SLOPE,
              pelland_2026.VOLUME_STRENGTH_SLOPE,
              pelland_2026.FREQUENCY_HYPERTROPHY_SLOPE,
              pelland_2026.FREQUENCY_STRENGTH_SLOPE):
        assert e.population.training_status == "mixed"


def test_pelland_meta_analysis_estimates_carry_study_counts():
    assert pelland_2026.VOLUME_HYPERTROPHY_SLOPE.n_studies == 35
    assert pelland_2026.VOLUME_STRENGTH_SLOPE.n_studies == 66


def test_pelland_fractional_set_counting():
    fsc = pelland_2026.fractional_set_count
    # direct work counts fully
    assert fsc("triceps_pushdown", 3, "triceps_brachii") == 3.0
    # indirect work counts at half
    assert fsc("flat_bench_press", 3, "triceps_brachii") == 1.5
    # an exercise not classified for that muscle contributes nothing
    assert fsc("leg_curl", 3, "triceps_brachii") == 0.0
    # an unknown muscle falls back to raw sets
    assert fsc("anything", 3, "no_such_muscle") == 3.0


def test_pelland_table1_rows_recovered_in_audit_are_present():
    cls = pelland_2026.HYPERTROPHY_CLASSIFICATIONS
    assert "rectus_femoris" in cls
    assert "trapezius" in cls
    assert "leg_extension" in cls["rectus_femoris"]["direct"]


# ---------------------------------------------------------------------------
# failure_effects — the citation correction is the headline audit fix
# ---------------------------------------------------------------------------

def test_failure_effects_list_sizes():
    assert len(failure_effects.HYPERTROPHY_ESTIMATES) == 5
    assert len(failure_effects.STRENGTH_ESTIMATES) == 3


def test_failure_effects_paper3_is_refalo_not_robinson():
    # Audit fix: DOI 10.1007/s40279-022-01784-y is Refalo et al. 2023, not
    # "Robinson 2022". Both estimates at that DOI must carry the Refalo cite.
    assert failure_effects.CITATION_REFALO.authors == "Refalo et al."
    assert failure_effects.CITATION_REFALO.year == 2023
    for e in (failure_effects.REFALO_HYPERTROPHY_SET_FAILURE,
              failure_effects.REFALO_HYPERTROPHY_MOMENTARY_FAILURE):
        assert e.source is failure_effects.CITATION_REFALO


def test_failure_effects_corrected_sample_sizes():
    # Audit fixes — the previously inflated / mislabelled n values.
    assert failure_effects.GRGIC_HYPERTROPHY_OVERALL.n == 219
    assert failure_effects.GRGIC_HYPERTROPHY_TRAINED.n == 39
    assert failure_effects.GRGIC_HYPERTROPHY_TRAINED.n_studies == 2
    assert failure_effects.GRGIC_STRENGTH_OVERALL.n == 394
    assert failure_effects.REFALO_HYPERTROPHY_SET_FAILURE.n == 284
    assert failure_effects.REFALO_HYPERTROPHY_MOMENTARY_FAILURE.n == 170


def test_failure_effects_volume_equated_filter_excludes_vieira():
    veq = failure_effects.hypertrophy_estimates_volume_equated()
    assert len(veq) == 4
    assert failure_effects.VIEIRA_HYPERTROPHY_NONEQ_VOLUME not in veq


def test_failure_effects_pooled_effect_matches_demo():
    # The demo's headline number: pooled volume-equated failure effect for a
    # trained male, with overlap adjustment, is ~+0.16 SMD.
    user = UserProfile(age=28, sex="male", training_status="trained")
    pooled = combine_for_user(
        failure_effects.hypertrophy_estimates_volume_equated(),
        user, min_applicability=0.7,
        overlap_se_inflation=failure_effects.OVERLAP_SE_INFLATION,
    )
    assert pooled is not None
    assert pooled.mean == pytest.approx(0.16, abs=0.02)
    # n_studies must survive pooling: 7 + 2 + 9 + 5 = 23
    assert pooled.n_studies == 23


# ---------------------------------------------------------------------------
# Maeo 2023
# ---------------------------------------------------------------------------

def test_maeo_list_sizes_and_quality():
    assert len(maeo_2023.WHOLE_MUSCLE_EFFECTS) == 3
    assert len(maeo_2023.EMPHASIS_ESTIMATES) == 6
    assert maeo_2023.QUALITY == 0.89


def test_maeo_reference_exercise_normalised_to_one():
    assert maeo_2023.CABLE_OVERHEAD_EXTENSION_LONG_HEAD.emphasis == 1.0
    # pushdown long-head emphasis is the 19.6/28.5 growth ratio
    assert maeo_2023.CABLE_PUSHDOWN_LONG_HEAD.emphasis == pytest.approx(0.69, abs=0.01)


def test_maeo_effects_are_difference_smds():
    # Audit fix: d is a between-condition difference SMD and IS poolable.
    for e in maeo_2023.WHOLE_MUSCLE_EFFECTS:
        assert e.scale == "standardized_mean_diff"


# ---------------------------------------------------------------------------
# Varovic 2025
# ---------------------------------------------------------------------------

def test_varovic_regional_estimates_and_quality():
    assert len(varovic_2025.REGIONAL_ESTIMATES) == 3
    assert varovic_2025.QUALITY == 0.83          # audit re-score from 0.88
    for e in varovic_2025.REGIONAL_ESTIMATES:
        # n is participants (an estimate), n_studies carries the verified 12
        assert e.n_studies == 12
        assert e.n != 12, "n must be participants, not the study count"


def test_varovic_regional_effects_are_trivial():
    means = [e.mean for e in varovic_2025.REGIONAL_ESTIMATES]
    assert means == [0.05, 0.07, 0.09]


# ---------------------------------------------------------------------------
# Wolf 2023
# ---------------------------------------------------------------------------

def test_wolf_quality_rescored():
    assert wolf_2023.QUALITY == 0.81             # audit re-score from 0.84


def test_wolf_hypertrophy_estimate_relabelled_and_uses_participant_n():
    # Audit fix: the old PARTIAL_VS_FULL_OVERALL was the muscle-size subgroup.
    e = wolf_2023.PARTIAL_VS_FULL_HYPERTROPHY
    assert e.mean == 0.04
    assert e.n == 212                            # participants, not study count
    assert e.n_studies == 8
    assert not hasattr(wolf_2023, "PARTIAL_VS_FULL_OVERALL")


def test_wolf_short_length_estimate_was_added():
    # Audit recovered this from the full text; it had been omitted.
    assert len(wolf_2023.HYPERTROPHY_ESTIMATES) == 3
    e = wolf_2023.PARTIAL_SHORT_LENGTH_VS_FULL
    assert e.mean == 0.08
    assert e in wolf_2023.HYPERTROPHY_ESTIMATES


def test_wolf_strength_estimate_uses_participant_n():
    assert wolf_2023.PARTIAL_VS_FULL_STRENGTH.n == 739
    assert wolf_2023.PARTIAL_VS_FULL_STRENGTH.n_studies == 24


# ---------------------------------------------------------------------------
# Schoenfeld 2017
# ---------------------------------------------------------------------------

def test_schoenfeld_quality_and_list_size():
    assert schoenfeld_2017.QUALITY == 0.75
    assert len(schoenfeld_2017.VOLUME_HYPERTROPHY_ESTIMATES) == 2


def test_schoenfeld_continuous_slope():
    e = schoenfeld_2017.VOLUME_HYPERTROPHY_SLOPE
    assert e.mean == 0.023
    assert e.se == 0.006
    assert e.n == 418
    assert e.n_studies == 15
    # distinct scale string — the guardrail that keeps it out of the Pelland pool
    assert e.scale == "smd_per_set"


def test_schoenfeld_high_vs_low_contrast():
    e = schoenfeld_2017.VOLUME_HYPERTROPHY_HIGH_VS_LOW
    assert e.mean == 0.241
    assert e.se == 0.101
    assert e.scale == "standardized_mean_diff"


def test_schoenfeld_scale_differs_from_pelland():
    # The two volume->hypertrophy papers must NOT share a scale string, or the
    # registry could accidentally inverse-variance pool incommensurable slopes.
    schoenfeld_scales = {e.scale for e in schoenfeld_2017.VOLUME_HYPERTROPHY_ESTIMATES}
    assert pelland_2026.VOLUME_HYPERTROPHY_SLOPE.scale not in schoenfeld_scales


# ---------------------------------------------------------------------------
# Kassiano 2023 (second ExerciseEmphasis source — gastrocnemius)
# ---------------------------------------------------------------------------

def test_kassiano_quality_and_list_size():
    assert kassiano_2023.QUALITY == 0.78
    assert len(kassiano_2023.EMPHASIS_ESTIMATES) == 6


def test_kassiano_lengthened_partial_is_the_reference():
    # the lengthened (INITIAL ROM) calf raise is normalized to 1.0 per head
    assert kassiano_2023.LENGTHENED_PARTIAL_CALF_RAISE_MEDIAL.emphasis == 1.0
    assert kassiano_2023.LENGTHENED_PARTIAL_CALF_RAISE_LATERAL.emphasis == 1.0


def test_kassiano_emphasis_ratios_and_ordering():
    assert kassiano_2023.FULL_ROM_CALF_RAISE_MEDIAL.emphasis == pytest.approx(6.7 / 15.2)
    assert kassiano_2023.SHORTENED_PARTIAL_CALF_RAISE_MEDIAL.emphasis == pytest.approx(3.4 / 15.2)
    # lengthened > full > shortened, for the medial head
    assert (kassiano_2023.LENGTHENED_PARTIAL_CALF_RAISE_MEDIAL.emphasis
            > kassiano_2023.FULL_ROM_CALF_RAISE_MEDIAL.emphasis
            > kassiano_2023.SHORTENED_PARTIAL_CALF_RAISE_MEDIAL.emphasis)


def test_kassiano_confidence_reflects_significance():
    # medial-head comparisons were significant -> "high"; the lateral
    # INITIAL-vs-FULL gap was not (p=0.060) -> "medium"
    medial = [e for e in kassiano_2023.EMPHASIS_ESTIMATES if e.region == "medial_head"]
    lateral = [e for e in kassiano_2023.EMPHASIS_ESTIMATES if e.region == "lateral_head"]
    assert len(medial) == 3 and len(lateral) == 3
    assert all(e.confidence == "high" for e in medial)
    assert all(e.confidence == "medium" for e in lateral)


# ---------------------------------------------------------------------------
# Maeo 2021 (third ExerciseEmphasis source — hamstrings, seated vs prone)
# ---------------------------------------------------------------------------

def test_maeo_2021_quality_and_list_size():
    assert maeo_2021.QUALITY == 0.88
    # 5 muscle/region keys (whole + 4 sub-muscles) x 2 exercises
    assert len(maeo_2021.EMPHASIS_ESTIMATES) == 10


def test_maeo_2021_emphasis_only_no_effect_estimates():
    # Maeo 2021 is a Varovic 2025 constituent — it must NOT export a
    # Topic-keyed EffectEstimate (that would double-count). Emphasis only.
    assert not hasattr(maeo_2021, "REGIONAL_ESTIMATES")
    assert not hasattr(maeo_2021, "WHOLE_MUSCLE_EFFECTS")
    assert not hasattr(maeo_2021, "EFFECT_ESTIMATES")


def test_maeo_2021_seated_leg_curl_is_the_reference():
    # the seated leg curl won every comparison -> normalized to 1.0 per muscle
    for e in maeo_2021.EMPHASIS_ESTIMATES:
        if e.exercise == "seated_leg_curl":
            assert e.emphasis == 1.0


def test_maeo_2021_prone_emphasis_ratios_pin_paper_numbers():
    # ANCOVA-adjusted MRI muscle-volume % changes, prone / seated:
    assert maeo_2021.PRONE_LEG_CURL_WHOLE.emphasis == pytest.approx(9.3 / 14.1)
    assert maeo_2021.PRONE_LEG_CURL_BFL.emphasis == pytest.approx(6.5 / 14.4)
    assert maeo_2021.PRONE_LEG_CURL_ST.emphasis == pytest.approx(19.3 / 23.6)
    assert maeo_2021.PRONE_LEG_CURL_SM.emphasis == pytest.approx(3.6 / 8.2)
    assert maeo_2021.PRONE_LEG_CURL_BFS.emphasis == pytest.approx(9.0 / 10.0)
    # whole-hamstrings prone emphasis is ~0.66
    assert maeo_2021.PRONE_LEG_CURL_WHOLE.emphasis == pytest.approx(0.66, abs=0.01)


def test_maeo_2021_bfs_pair_is_low_confidence():
    # the monoarticular biceps femoris short head difference was n.s.
    # (+10% vs +9%, P=0.190) -> both BFS entries encoded at confidence="low"
    bfs = [e for e in maeo_2021.EMPHASIS_ESTIMATES
           if e.region == "biceps_femoris_short_head"]
    assert len(bfs) == 2
    assert all(e.confidence == "low" for e in bfs)


def test_maeo_2021_biarticular_and_whole_pairs_are_high_confidence():
    # WH + the three biarticular sub-muscles all reached significance
    high_regions = {None, "biceps_femoris_long_head",
                    "semitendinosus", "semimembranosus"}
    for e in maeo_2021.EMPHASIS_ESTIMATES:
        if e.region in high_regions:
            assert e.confidence == "high"


def test_maeo_2021_seated_outgrows_prone_for_every_muscle():
    # the headline: the seated leg curl >= prone leg curl for all 5 keys
    by_key: dict = {}
    for e in maeo_2021.EMPHASIS_ESTIMATES:
        by_key.setdefault(e.region, {})[e.exercise] = e.emphasis
    assert len(by_key) == 5
    for region, pair in by_key.items():
        assert pair["seated_leg_curl"] >= pair["prone_leg_curl"]


# ---------------------------------------------------------------------------
# Pedrosa 2023 (elbow flexors — regional EffectEstimates, Varovic companion)
# ---------------------------------------------------------------------------

def test_pedrosa_quality_and_list_size():
    assert pedrosa_2023.QUALITY == 0.83
    assert len(pedrosa_2023.REGIONAL_ESTIMATES) == 3


def test_pedrosa_distal_effect_is_the_headline():
    e = pedrosa_2023.BICEPS_DISTAL_INITIAL_VS_FINAL
    assert e.mean == 0.89
    assert e.n == 19
    assert e.scale == "standardized_mean_diff"
    # the distal effect is much larger than the mid-belly effect
    assert e.mean > pedrosa_2023.BICEPS_MID_INITIAL_VS_FINAL.mean


def test_pedrosa_se_reconstruction_matches_unpaired_formula():
    e = pedrosa_2023.BICEPS_DISTAL_INITIAL_VS_FINAL
    expected = math.sqrt(1 / 19 + 0.89 ** 2 / (2 * 19))
    assert e.se == pytest.approx(expected)


def test_pedrosa_is_a_single_study_not_a_meta_analysis():
    # single primary study -> n_studies stays None (not a pooled count)
    assert all(e.n_studies is None for e in pedrosa_2023.REGIONAL_ESTIMATES)


# ---------------------------------------------------------------------------
# Schoenfeld/Grgic 2017 (low-vs-high-load meta-analysis)
# ---------------------------------------------------------------------------

def test_schoenfeld_load_quality():
    assert schoenfeld_load_2017.QUALITY == 0.77


def test_schoenfeld_load_hypertrophy_is_null():
    # the headline: load does not affect hypertrophy (study-level ES ~0)
    e = schoenfeld_load_2017.LOAD_HYPERTROPHY_HIGH_VS_LOW
    assert e.mean == 0.03
    assert e.n_studies == 10
    lo, hi = e.ci_95
    assert lo < 0 < hi               # CI crosses zero — no load effect


def test_schoenfeld_load_1rm_favours_high_load():
    e = schoenfeld_load_2017.LOAD_STRENGTH_1RM_HIGH_VS_LOW
    assert e.mean == 0.58
    assert e.n_studies == 14
    lo, _ = e.ci_95
    assert lo > 0                    # CI excludes zero — high load reliably better


def test_schoenfeld_load_distinct_from_volume_module():
    # the two 2017 Schoenfeld modules must cite different papers
    assert schoenfeld_load_2017.CITATION.doi != schoenfeld_2017.CITATION.doi


# ---------------------------------------------------------------------------
# Singer 2024 (inter-set rest interval -> hypertrophy)
# ---------------------------------------------------------------------------

def test_singer_quality_and_list_size():
    assert singer_2024.QUALITY == 0.77
    assert len(singer_2024.HYPERTROPHY_ESTIMATES) == 3


def test_singer_between_condition_means_pin_paper_numbers():
    # The encoded estimates are the between-condition (controlled) binary
    # SMDs — short rest (<=60 s) vs longer rest (>60 s). Positive = longer rest.
    assert singer_2024.REST_INTERVAL_ARM_HYPERTROPHY.mean == 0.13
    assert singer_2024.REST_INTERVAL_THIGH_HYPERTROPHY.mean == 0.17
    assert singer_2024.REST_INTERVAL_WHOLE_BODY_HYPERTROPHY.mean == -0.08


def test_singer_se_recovered_from_credible_intervals():
    # SE = (high - low) / (2 * 1.96) from each paper-reported 95% CrI.
    assert singer_2024.REST_INTERVAL_ARM_HYPERTROPHY.se == pytest.approx(
        (0.51 - -0.27) / (2 * 1.96))
    assert singer_2024.REST_INTERVAL_THIGH_HYPERTROPHY.se == pytest.approx(
        (0.43 - -0.13) / (2 * 1.96))
    assert singer_2024.REST_INTERVAL_WHOLE_BODY_HYPERTROPHY.se == pytest.approx(
        (0.29 - -0.45) / (2 * 1.96))


def test_singer_estimates_are_difference_smds():
    for e in singer_2024.HYPERTROPHY_ESTIMATES:
        assert e.scale == "standardized_mean_diff"
        assert e.population.outcome == "hypertrophy"
        # meta-analysis of 9 RCTs — study count carried, not None
        assert e.n_studies == 9


def test_singer_whole_body_points_opposite_to_limbs():
    # The headline heterogeneity: whole body disagrees in SIGN with arm/thigh.
    arm = singer_2024.REST_INTERVAL_ARM_HYPERTROPHY.mean
    thigh = singer_2024.REST_INTERVAL_THIGH_HYPERTROPHY.mean
    whole = singer_2024.REST_INTERVAL_WHOLE_BODY_HYPERTROPHY.mean
    assert arm > 0 and thigh > 0
    assert whole < 0


def test_singer_poolable_set_is_arm_and_thigh_only():
    # The whole-body estimate is deliberately excluded from the pool.
    pool = singer_2024.poolable_estimates()
    assert len(pool) == 2
    assert singer_2024.REST_INTERVAL_ARM_HYPERTROPHY in pool
    assert singer_2024.REST_INTERVAL_THIGH_HYPERTROPHY in pool
    assert singer_2024.REST_INTERVAL_WHOLE_BODY_HYPERTROPHY not in pool


def test_singer_within_condition_smds_are_not_encoded():
    # The within-condition pre/post SMDs (~0.48 / 0.56) describe how much each
    # group grew — NOT the rest-interval effect. They must not appear as
    # EffectEstimates. Guard against a regression that re-introduces them.
    encoded_means = {e.mean for e in singer_2024.HYPERTROPHY_ESTIMATES}
    assert 0.48 not in encoded_means
    assert 0.56 not in encoded_means


def test_singer_all_credible_intervals_cross_zero():
    # Every region estimate's CrI crosses zero — a near-null rest-interval
    # effect across the board.
    for e in singer_2024.HYPERTROPHY_ESTIMATES:
        lo, hi = e.ci_95
        assert lo < 0 < hi


# ---------------------------------------------------------------------------
# Plotkin 2023 — hip thrust vs back squat, glute hypertrophy
# ---------------------------------------------------------------------------

def test_plotkin_quality_and_list_sizes():
    assert plotkin_2023.QUALITY == 0.875
    assert len(plotkin_2023.EXERCISE_SELECTION_ESTIMATES) == 7
    assert len(plotkin_2023.GLUTEUS_MAXIMUS_ESTIMATES) == 3
    assert len(plotkin_2023.EMPHASIS_ESTIMATES) == 2


def test_plotkin_all_estimates_on_raw_cm2_between_exercise_scale():
    # The dedicated scale string is the guard against pooling these raw-cm^2
    # between-exercise contrasts with the layer's SMD / %-per-set estimates.
    for e in plotkin_2023.EXERCISE_SELECTION_ESTIMATES:
        assert e.scale == "between_exercise_csa_diff_cm2"
        # single primary RCT — not a meta-analysis
        assert e.n_studies is None
        assert e.n == 34
        assert e.population.training_status == "untrained"
        assert e.population.outcome == "hypertrophy"


def test_plotkin_glute_max_contrast_values_pinned():
    # HT-minus-SQ between-exercise contrasts in raw cm^2; SE read directly off
    # the paper ("effect +/- SE"). Pin every encoded number.
    upper = plotkin_2023.GLUTE_MAX_UPPER_HT_VS_SQ
    middle = plotkin_2023.GLUTE_MAX_MIDDLE_HT_VS_SQ
    lower = plotkin_2023.GLUTE_MAX_LOWER_HT_VS_SQ
    assert (upper.mean, upper.se) == (-0.5, 2.6)
    assert (middle.mean, middle.se) == (-0.5, 1.7)
    assert (lower.mean, lower.se) == (-1.6, 2.1)


def test_plotkin_thigh_contrast_values_pinned():
    medmin = plotkin_2023.GLUTE_MED_MIN_HT_VS_SQ
    quad = plotkin_2023.QUADRICEPS_HT_VS_SQ
    add = plotkin_2023.ADDUCTORS_HT_VS_SQ
    ham = plotkin_2023.HAMSTRINGS_HT_VS_SQ
    assert (medmin.mean, medmin.se) == (-1.8, 1.5)
    assert (quad.mean, quad.se) == (3.6, 1.5)
    assert (add.mean, add.se) == (2.5, 0.7)
    assert (ham.mean, ham.se) == (0.1, 0.6)


def test_plotkin_glute_max_is_a_null_result():
    # All three gluteus-maximus subregion contrasts must cross zero — the
    # honest equivalence result. A regression that narrows a CI off zero or
    # flips a sign should fail loudly.
    for e in plotkin_2023.GLUTEUS_MAXIMUS_ESTIMATES:
        lo, hi = e.ci_95
        assert lo < 0 < hi, f"{e.notes[:40]} no longer crosses zero"


def test_plotkin_squat_thigh_advantage_excludes_zero():
    # Quadriceps and adductors are the squat's real, significant bonus:
    # both CIs must EXCLUDE zero, on the favours-squat (positive) side.
    for e in (plotkin_2023.QUADRICEPS_HT_VS_SQ, plotkin_2023.ADDUCTORS_HT_VS_SQ):
        lo, hi = e.ci_95
        assert 0 < lo, f"{e.notes[:40]} CI no longer excludes zero"
        assert e.mean > 0  # positive HT-minus-SQ contrast == favours the squat


def test_plotkin_emphasis_is_equal_equivalence_encoding():
    # The paper measured NO glute winner — both exercises get emphasis 1.0.
    # A fractional coefficient implying a measured winner is the bug to catch.
    ht = plotkin_2023.EMPHASIS_HIP_THRUST_GLUTE_MAX
    sq = plotkin_2023.EMPHASIS_BACK_SQUAT_GLUTE_MAX
    assert ht.emphasis == 1.0
    assert sq.emphasis == 1.0
    assert ht.emphasis == sq.emphasis
    # equivalence from a single n=34 trial -> medium confidence, not high
    assert ht.confidence == "medium"
    assert sq.confidence == "medium"
    # whole-muscle emphasis (region=None); no fractional per-subregion entries
    for em in plotkin_2023.EMPHASIS_ESTIMATES:
        assert em.region is None
        assert em.muscle == "gluteus_maximus"


def test_plotkin_strength_transfer_context_constants():
    # Strength transfer is kept as context constants, not EffectEstimates.
    st = plotkin_2023.STRENGTH_TRANSFER_CONTRASTS_KG
    assert st["back_squat_3rm"]["effect"] == 14.0
    assert st["hip_thrust_3rm"]["effect"] == -26.0
    # equal transfer to the untrained deadlift — the headline strength finding
    assert st["deadlift_3rm"]["effect"] == 0.0
    # none of these leaked into the encoded EffectEstimate list
    assert not hasattr(plotkin_2023, "STRENGTH_ESTIMATES")


# ---------------------------------------------------------------------------
# Chaves 2020 — incline vs horizontal vs combination bench press, chest
# ---------------------------------------------------------------------------

def test_chaves_quality_and_list_size():
    assert chaves_2020.QUALITY == 0.79
    # 2 region keys (clavicular + sternocostal head) x 3 exercises
    assert len(chaves_2020.EMPHASIS_ESTIMATES) == 6


def test_chaves_emphasis_only_no_effect_estimates():
    # Exercise-selection study mapping to no Topic — emphasis only, no
    # Topic-keyed EffectEstimate (mirrors maeo_2021).
    assert not hasattr(chaves_2020, "REGIONAL_ESTIMATES")
    assert not hasattr(chaves_2020, "WHOLE_MUSCLE_EFFECTS")
    assert not hasattr(chaves_2020, "EFFECT_ESTIMATES")
    assert not hasattr(chaves_2020, "EXERCISE_SELECTION_ESTIMATES")


def test_chaves_incline_is_the_reference_at_every_site():
    # the incline press grew (or numerically led) every site -> normalized to
    # 1.0 per (muscle, region)
    for e in chaves_2020.EMPHASIS_ESTIMATES:
        if e.exercise == "incline_bench_press":
            assert e.emphasis == 1.0


def test_chaves_clavicular_emphasis_ratios_pin_paper_numbers():
    # The module normalizes ROUNDED per-site % growth to the incline press.
    # % growth from the mm means: post/pre - 1.
    #   incline clavicular = (24.5-15.1)/15.1 = +62.3%  -> reference
    #   horizontal         = (15.7-11.9)/11.9 = +31.9%
    #   combination        = (18.8-14.3)/14.3 = +31.5%
    # The encoded emphasis is the rounded-percentage ratio (the value the
    # module's rationale strings document); pin exactly that.
    assert chaves_2020.HORIZONTAL_BENCH_PRESS_CLAVICULAR.emphasis == 31.9 / 62.3
    assert chaves_2020.COMBINATION_BENCH_PRESS_CLAVICULAR.emphasis == 31.5 / 62.3
    # horizontal provides roughly half the incline upper-chest stimulus
    assert chaves_2020.HORIZONTAL_BENCH_PRESS_CLAVICULAR.emphasis == pytest.approx(
        0.51, abs=0.02)
    # the rounded ratio is within rounding distance of the raw-mm ratio
    raw = ((15.7 - 11.9) / 11.9) / ((24.5 - 15.1) / 15.1)
    assert chaves_2020.HORIZONTAL_BENCH_PRESS_CLAVICULAR.emphasis == pytest.approx(
        raw, abs=0.005)


def test_chaves_sternocostal_emphasis_ratios_pin_paper_numbers():
    # 3rd-intercostal (mid) site is the sternocostal representative:
    #   incline     = (23.8-15.4)/15.4 = +54.5%  -> reference
    #   horizontal  = (19.3-13.2)/13.2 = +46.2%
    #   combination = (21.2-17.1)/17.1 = +24.0%
    # Encoded emphasis is the rounded-percentage ratio; pin exactly that.
    assert chaves_2020.HORIZONTAL_BENCH_PRESS_STERNOCOSTAL.emphasis == 46.2 / 54.5
    assert chaves_2020.COMBINATION_BENCH_PRESS_STERNOCOSTAL.emphasis == 24.0 / 54.5


def test_chaves_clavicular_pairs_are_high_confidence():
    # the upper-chest incline advantage is the one significant between-group
    # result (P=0.003 / 0.008) -> all clavicular pairs confidence="high"
    clavicular = [e for e in chaves_2020.EMPHASIS_ESTIMATES
                  if e.region == "clavicular_head"]
    assert len(clavicular) == 3
    assert all(e.confidence == "high" for e in clavicular)


def test_chaves_sternocostal_pairs_are_low_confidence():
    # both sternocostal sites showed NO significant between-group difference
    # (3rd intercostal P=0.095, 5th P=0.227) -> all sternocostal pairs
    # confidence="low" (mirrors maeo_2021's n.s. BF-short-head pair)
    sternocostal = [e for e in chaves_2020.EMPHASIS_ESTIMATES
                    if e.region == "sternocostal_head"]
    assert len(sternocostal) == 3
    assert all(e.confidence == "low" for e in sternocostal)


def test_chaves_population_is_untrained_men():
    for e in chaves_2020.EMPHASIS_ESTIMATES:
        assert e.population.training_status == "untrained"
        assert e.population.sex == "male"
        assert e.population.outcome == "hypertrophy"
        assert e.muscle == "pectoralis_major"


def test_chaves_incline_leads_at_every_region():
    # the headline: incline press >= the other two variants for both heads
    by_key: dict = {}
    for e in chaves_2020.EMPHASIS_ESTIMATES:
        by_key.setdefault(e.region, {})[e.exercise] = e.emphasis
    assert set(by_key) == {"clavicular_head", "sternocostal_head"}
    for region, pair in by_key.items():
        assert pair["incline_bench_press"] >= pair["horizontal_bench_press"]
        assert pair["incline_bench_press"] >= pair["combination_bench_press"]


def test_chaves_combination_did_not_beat_horizontal_for_upper_chest():
    # the documented anti-finding: diluting incline volume with flat work
    # erased the upper-chest benefit -> combination ~= horizontal, both ~half incline
    horiz = chaves_2020.HORIZONTAL_BENCH_PRESS_CLAVICULAR.emphasis
    combo = chaves_2020.COMBINATION_BENCH_PRESS_CLAVICULAR.emphasis
    assert combo == pytest.approx(horiz, abs=0.05)
    assert combo < chaves_2020.INCLINE_BENCH_PRESS_CLAVICULAR.emphasis


# ---------------------------------------------------------------------------
# Mechanistic prior — latissimus dorsi (ADR-010 prototype, fallback tier)
# ---------------------------------------------------------------------------

def test_mechanistic_lats_entry_count_and_types():
    ms = mechanistic_lats.MECHANISTIC_EMPHASIS
    assert len(ms) == 17                       # 7 whole + 5 upper + 5 lower
    assert all(isinstance(m, MechanisticEmphasis) for m in ms)
    # a mechanistic prior is a DIFFERENT type from a measured one — it can
    # never be confused for, or pooled with, measured ExerciseEmphasis
    assert not any(isinstance(m, ExerciseEmphasis) for m in ms)


def test_mechanistic_lats_invariants():
    for m in mechanistic_lats.MECHANISTIC_EMPHASIS:
        assert 0.0 <= m.emphasis <= 1.0
        assert m.loaded_length in ("long", "mid", "short")
        assert m.muscle == "latissimus_dorsi"
        assert m.grounded_in                    # provenance is non-empty
        # confidence is hard-capped — a derived prior is never medium/high
        assert m.confidence in ("low", "speculative")


def test_mechanistic_lats_whole_is_low_regional_is_speculative():
    for m in mechanistic_lats.MECHANISTIC_EMPHASIS:
        if m.region is None:
            assert m.confidence == "low"
        else:
            assert m.region in ("upper_fibres", "lower_fibres")
            assert m.confidence == "speculative"


def test_mechanistic_lats_loaded_length_drives_emphasis():
    # coarse buckets: long -> 1.0, mid -> 0.70, short -> 0.50
    bucket = {"long": 1.0, "mid": 0.70, "short": 0.50}
    for m in mechanistic_lats.MECHANISTIC_EMPHASIS:
        assert m.emphasis == pytest.approx(bucket[m.loaded_length])


def test_mechanistic_lats_known_values():
    by_key = {(m.exercise, m.region): m for m in mechanistic_lats.MECHANISTIC_EMPHASIS}
    # stretch-loaded isolation tops the whole-muscle prior
    assert by_key[("dumbbell_pullover", None)].emphasis == 1.0
    assert by_key[("dumbbell_pullover", None)].loaded_length == "long"
    # the row is loaded contracted -> lowest
    assert by_key[("barbell_row", None)].emphasis == 0.50
    assert by_key[("barbell_row", None)].loaded_length == "short"
    # the one speculative lower-fibre "long" call is the bodyweight pull-up
    assert by_key[("pull_up", "lower_fibres")].loaded_length == "long"


def test_mechanistic_emphasis_rejects_high_confidence():
    # the hard ceiling is structural, not a convention
    with pytest.raises(ValueError):
        MechanisticEmphasis(
            exercise="x", muscle="y", region=None, emphasis=1.0,
            loaded_length="long", confidence="high",
            rationale="should fail", grounded_in=("maeo_2023",),
        )


# ---------------------------------------------------------------------------
# Mechanistic prior — deltoids (ADR-010 prototype, fallback tier)
# ---------------------------------------------------------------------------

def test_mechanistic_deltoids_entry_count_and_types():
    ms = mechanistic_deltoids.MECHANISTIC_EMPHASIS
    assert len(ms) == 9                        # 3 exercises per head
    assert all(isinstance(m, MechanisticEmphasis) for m in ms)
    assert not any(isinstance(m, ExerciseEmphasis) for m in ms)


def test_mechanistic_deltoids_invariants():
    for m in mechanistic_deltoids.MECHANISTIC_EMPHASIS:
        assert 0.0 <= m.emphasis <= 1.0
        assert m.loaded_length in ("long", "mid", "short")
        assert m.muscle == "deltoids"
        assert m.region in ("anterior", "lateral", "posterior")
        assert m.grounded_in
        # the three delt heads are distinct functional targets — encoded at
        # "low", NOT the "speculative" tag the contested lat upper/lower split
        # carries; only the loaded-length stretch-bias is the soft inference
        assert m.confidence == "low"


def test_mechanistic_deltoids_loaded_length_drives_emphasis():
    bucket = {"long": 1.0, "mid": 0.70, "short": 0.50}
    for m in mechanistic_deltoids.MECHANISTIC_EMPHASIS:
        assert m.emphasis == pytest.approx(bucket[m.loaded_length])


def test_mechanistic_deltoids_known_values():
    by_key = {(m.exercise, m.region): m
              for m in mechanistic_deltoids.MECHANISTIC_EMPHASIS}
    # cable variants load the stretched start -> top of each head
    assert by_key[("cable_lateral_raise", "lateral")].loaded_length == "long"
    assert by_key[("cable_rear_delt_fly", "posterior")].loaded_length == "long"
    # free-weight raises/flies are loaded contracted -> short
    assert by_key[("dumbbell_lateral_raise", "lateral")].emphasis == 0.50
    assert by_key[("dumbbell_reverse_fly", "posterior")].emphasis == 0.50
    # each head carries exactly 3 entries
    for head in ("anterior", "lateral", "posterior"):
        assert sum(1 for (_, r) in by_key if r == head) == 3


# ---------------------------------------------------------------------------
# Exercise -> muscle involvement map (ADR-011)
# ---------------------------------------------------------------------------

def test_involvement_row_count_and_types():
    rows = exercise_involvement.EXERCISE_INVOLVEMENT
    assert len(rows) == 74                       # 16 exercises, lats + deltoids
    assert all(isinstance(r, ExerciseInvolvement) for r in rows)
    # involvement is its own shape — never an emphasis estimate
    assert not any(isinstance(r, (ExerciseEmphasis, MechanisticEmphasis))
                   for r in rows)


def test_involvement_invariants():
    for r in exercise_involvement.EXERCISE_INVOLVEMENT:
        assert r.role in ("primary", "secondary", "stabilizer")
        assert r.basis in ("pelland_2026_table1", "biomechanical")
        assert r.rationale
        assert r.outcomes
        assert all(o in ("hypertrophy", "strength") for o in r.outcomes)


def test_involvement_set_credit_follows_role():
    # the crediting heuristic lives only in ROLE_SET_CREDIT — pin it
    bucket = {"primary": 1.0, "secondary": 0.5, "stabilizer": 0.0}
    for r in exercise_involvement.EXERCISE_INVOLVEMENT:
        assert r.set_credit == bucket[r.role]


def test_involvement_one_row_per_exercise_muscle():
    keys = [(r.exercise, r.muscle)
            for r in exercise_involvement.EXERCISE_INVOLVEMENT]
    assert len(keys) == len(set(keys))


def test_involvement_every_exercise_has_a_primary():
    by_exercise: dict = {}
    for r in exercise_involvement.EXERCISE_INVOLVEMENT:
        by_exercise.setdefault(r.exercise, []).append(r)
    assert len(by_exercise) == 16
    for exercise, rows in by_exercise.items():
        assert any(r.role == "primary" for r in rows), f"{exercise}: no primary"


def test_involvement_prototype_is_outcome_shared():
    # every prototype row serves both hypertrophy and strength — role is anatomy
    for r in exercise_involvement.EXERCISE_INVOLVEMENT:
        assert set(r.outcomes) == {"hypertrophy", "strength"}


def test_involvement_pelland_corroborated_rows():
    # exactly three (exercise, muscle) pairs are exact Pelland 2026 Table 1
    # matches and carry basis="pelland_2026_table1"; the rest are biomechanical
    pelland_rows = {(r.exercise, r.muscle)
                    for r in exercise_involvement.EXERCISE_INVOLVEMENT
                    if r.basis == "pelland_2026_table1"}
    assert pelland_rows == {
        ("lat_pulldown", "biceps_brachii"),
        ("lat_pulldown", "trapezius"),
        ("incline_bench_press", "triceps_brachii"),
    }
    # and each genuinely sits in Pelland's encoded Table 1 indirect class
    cls = pelland_2026.HYPERTROPHY_CLASSIFICATIONS
    assert "lat_pulldown" in cls["biceps_brachii"]["indirect"]
    assert "lat_pulldown" in cls["trapezius"]["indirect"]
    assert "incline_bench_press" in cls["triceps_brachii"]["indirect"]


def test_involvement_known_rows():
    by_key = {(r.exercise, r.muscle): r
              for r in exercise_involvement.EXERCISE_INVOLVEMENT}
    # a row is a prime mover for several back muscles at once
    assert by_key[("barbell_row", "latissimus_dorsi")].role == "primary"
    assert by_key[("barbell_row", "trapezius")].role == "primary"
    assert by_key[("barbell_row", "rhomboids")].role == "primary"
    # the biceps get fractional (indirect) credit from a row
    assert by_key[("barbell_row", "biceps_brachii")].set_credit == 0.5
    # the erectors only brace the bent-over row -> stabiliser, zero credit
    assert by_key[("barbell_row", "erector_spinae")].role == "stabilizer"
    assert by_key[("barbell_row", "erector_spinae")].set_credit == 0.0
    # an isolation raise has one primary head
    assert by_key[("dumbbell_lateral_raise", "lateral_deltoid")].role == "primary"


def test_involvement_rejects_bad_inputs():
    with pytest.raises(ValueError):
        ExerciseInvolvement(exercise="x", muscle="y", role="prime_mover",
                            basis="biomechanical", rationale="bad role")
    with pytest.raises(ValueError):
        ExerciseInvolvement(exercise="x", muscle="y", role="primary",
                            basis="guesswork", rationale="bad basis")
    with pytest.raises(ValueError):
        ExerciseInvolvement(exercise="x", muscle="y", role="primary",
                            basis="biomechanical", rationale="")
