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
    varovic_2025,
    wolf_2023,
    schoenfeld_2017,
    kassiano_2023,
    pedrosa_2023,
    schoenfeld_load_2017,
)
from app.priors.shared import (
    EffectEstimate,
    ExerciseEmphasis,
    UserProfile,
    combine_for_user,
)


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
}

ALL_EFFECTS = [
    pytest.param(e, id=f"{name}[{i}]")
    for name, lst in EFFECT_LISTS.items()
    for i, e in enumerate(lst)
]

EMPHASIS_LISTS = {
    "maeo": maeo_2023.EMPHASIS_ESTIMATES,
    "kassiano": kassiano_2023.EMPHASIS_ESTIMATES,
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
