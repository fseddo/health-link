"""
Tests for app/priors/registry.py — the app-facing query layer.

Verifies the index is wired to every paper module, that the poolable-set
overrides and overlap defaults behave, and that the emphasis lookups resolve.

Run from the priors-handoff root:  python -m pytest tests/priors/
"""

import pytest

from app.priors import registry
from app.priors.registry import Topic
from app.priors.shared import UserProfile, EffectEstimate, ExerciseEmphasis


TRAINED_MALE = UserProfile(age=28, sex="male", training_status="trained")
# A user pushed far outside every studied population (age 90 forces the
# applicability floor for all topics).
OUT_OF_RANGE = UserProfile(age=90, sex="male", training_status="trained")


# ---------------------------------------------------------------------------
# Index wiring
# ---------------------------------------------------------------------------

def test_all_topics_present():
    topics = registry.all_topics()
    assert len(topics) == 14
    assert Topic.VOLUME_HYPERTROPHY in topics
    assert Topic.ARM_POSITION_HYPERTROPHY in topics
    assert Topic.LOAD_HYPERTROPHY in topics
    assert Topic.LOAD_STRENGTH in topics
    assert Topic.REST_INTERVAL_HYPERTROPHY in topics
    assert Topic.EXERCISE_SELECTION_HYPERTROPHY in topics


def test_every_topic_has_at_least_one_estimate():
    for topic in registry.all_topics():
        assert registry.effects(topic), f"{topic} has no estimates"


def test_topic_value_is_a_stable_string():
    assert Topic.FAILURE_HYPERTROPHY.value == "failure->hypertrophy"
    assert isinstance(Topic.FAILURE_HYPERTROPHY, str)


def test_effects_returns_a_fresh_list():
    a = registry.effects(Topic.FAILURE_HYPERTROPHY)
    a.clear()
    assert registry.effects(Topic.FAILURE_HYPERTROPHY), "index was mutated"


def test_effects_are_effect_estimates():
    for e in registry.effects(Topic.ROM_HYPERTROPHY):
        assert isinstance(e, EffectEstimate)


# ---------------------------------------------------------------------------
# Poolable-set override
# ---------------------------------------------------------------------------

def test_failure_hypertrophy_poolable_excludes_vieira():
    full = registry.effects(Topic.FAILURE_HYPERTROPHY)
    poolable = registry.poolable_effects(Topic.FAILURE_HYPERTROPHY)
    assert len(full) == 5
    assert len(poolable) == 4          # Vieira's non-volume-equated 0.75 dropped


def test_non_override_topic_poolable_equals_full():
    for topic in (Topic.VOLUME_STRENGTH, Topic.ROM_HYPERTROPHY,
                  Topic.ARM_POSITION_HYPERTROPHY):
        assert registry.poolable_effects(topic) == registry.effects(topic)


def test_regional_hypertrophy_poolable_excludes_pedrosa():
    # Pedrosa 2023 (a single primary study) is registered under the same topic
    # as Varovic 2025's meta-analysis but kept out of the inverse-variance pool.
    full = registry.effects(Topic.MUSCLE_LENGTH_REGIONAL_HYPERTROPHY)
    poolable = registry.poolable_effects(Topic.MUSCLE_LENGTH_REGIONAL_HYPERTROPHY)
    assert len(full) == 6          # Varovic 3 + Pedrosa 3
    assert len(poolable) == 3      # Varovic only


def test_load_strength_poolable_is_1rm_only():
    # load->strength holds 1RM + isometric — different outcomes; the poolable
    # representative is the 1RM estimate.
    full = registry.effects(Topic.LOAD_STRENGTH)
    poolable = registry.poolable_effects(Topic.LOAD_STRENGTH)
    assert len(full) == 2
    assert len(poolable) == 1
    assert poolable[0].mean == 0.58          # the 1RM high-vs-low estimate


def test_volume_hypertrophy_poolable_excludes_schoenfeld():
    # Schoenfeld 2017 is registered for inspection but kept out of the pool:
    # it is not on a common scale with Pelland 2026 (SMD/set vs %/set).
    full = registry.effects(Topic.VOLUME_HYPERTROPHY)
    poolable = registry.poolable_effects(Topic.VOLUME_HYPERTROPHY)
    assert len(full) == 3          # Pelland 1 + Schoenfeld 2
    assert len(poolable) == 1      # Pelland only
    # pooling must NOT raise despite the mixed scales present in effects()
    pooled = registry.pooled_effect(Topic.VOLUME_HYPERTROPHY, TRAINED_MALE)
    assert pooled is not None
    assert pooled.mean == pytest.approx(0.24)


def test_rest_interval_hypertrophy_poolable_excludes_whole_body():
    # Singer 2024 carries arm / thigh / whole-body region SMDs. The whole-body
    # estimate points the opposite way (-0.08) and is kept out of the pool;
    # the poolable set is arm + thigh.
    from app.priors import singer_2024
    full = registry.effects(Topic.REST_INTERVAL_HYPERTROPHY)
    poolable = registry.poolable_effects(Topic.REST_INTERVAL_HYPERTROPHY)
    assert len(full) == 3                                  # arm + thigh + whole body
    assert len(poolable) == 2                              # arm + thigh
    assert singer_2024.REST_INTERVAL_WHOLE_BODY_HYPERTROPHY in full
    assert singer_2024.REST_INTERVAL_WHOLE_BODY_HYPERTROPHY not in poolable


def test_exercise_selection_topic_carries_plotkin_contrasts():
    # Plotkin 2023 registers seven between-exercise (HT minus SQ) contrasts.
    full = registry.effects(Topic.EXERCISE_SELECTION_HYPERTROPHY)
    assert len(full) == 7
    # all on the dedicated raw-cm^2 between-exercise scale -- never poolable
    # with the layer's SMD / %-per-set estimates.
    assert {e.scale for e in full} == {"between_exercise_csa_diff_cm2"}


def test_exercise_selection_poolable_is_glute_max_only():
    # The poolable set is the three gluteus-maximus subregion contrasts only;
    # the four thigh/abductor by-product contrasts stay visible in effects().
    full = registry.effects(Topic.EXERCISE_SELECTION_HYPERTROPHY)
    poolable = registry.poolable_effects(Topic.EXERCISE_SELECTION_HYPERTROPHY)
    assert len(full) == 7
    assert len(poolable) == 3
    from app.priors import plotkin_2023
    assert poolable == list(plotkin_2023.GLUTEUS_MAXIMUS_ESTIMATES)
    assert plotkin_2023.QUADRICEPS_HT_VS_SQ in full
    assert plotkin_2023.QUADRICEPS_HT_VS_SQ not in poolable


def test_exercise_selection_glute_pool_is_a_null_result():
    # Pooling the three glute-max subregion contrasts yields a small negative
    # cm^2 difference whose interval crosses zero -- hip thrust and back squat
    # are interchangeable for glute hypertrophy.
    YOUNG_UNTRAINED = UserProfile(age=22, sex="female", training_status="untrained")
    pooled = registry.pooled_effect(
        Topic.EXERCISE_SELECTION_HYPERTROPHY, YOUNG_UNTRAINED)
    assert pooled is not None
    lo, hi = pooled.ci_95
    assert lo < 0 < hi              # CI crosses zero -> equivalence
    assert -2.0 < pooled.mean < 0.0  # small lean toward the squat, trivial


def test_registry_indexes_plotkin_glute_emphasis_equivalence():
    # Both exercises get equal 1.0 glute-max emphasis -- the paper measured no
    # winner, so the emphasis encoding is an equivalence, not a ranking.
    ht = registry.emphasis("barbell_hip_thrust", "gluteus_maximus", None)
    sq = registry.emphasis("barbell_back_squat", "gluteus_maximus", None)
    assert len(ht) == 1 and len(sq) == 1
    assert ht[0].emphasis == 1.0
    assert sq[0].emphasis == 1.0
    assert ht[0].confidence == "medium"
    assert sq[0].confidence == "medium"


def test_emphasis_for_muscle_ranks_glute_exercises_as_equal():
    glutes = registry.emphasis_for_muscle("gluteus_maximus")
    assert set(glutes) == {"barbell_hip_thrust", "barbell_back_squat"}
    # equal emphasis -- neither out-ranks the other for the glutes
    assert glutes["barbell_hip_thrust"].emphasis == glutes["barbell_back_squat"].emphasis == 1.0


def test_rest_interval_pooled_effect_is_trivial_and_positive():
    # Pooling arm (+0.13) and thigh (+0.17) yields a trivial positive SMD
    # whose interval crosses zero — a near-null rest-interval effect.
    pooled = registry.pooled_effect(Topic.REST_INTERVAL_HYPERTROPHY, TRAINED_MALE)
    assert pooled is not None
    assert 0.10 < pooled.mean < 0.20
    lo, hi = pooled.ci_95
    assert lo < 0 < hi
    # study count survives pooling: both estimates carry n_studies=9
    assert pooled.n_studies == 18


# ---------------------------------------------------------------------------
# pooled_effect
# ---------------------------------------------------------------------------

def test_pooled_failure_hypertrophy_matches_known_value():
    pooled = registry.pooled_effect(Topic.FAILURE_HYPERTROPHY, TRAINED_MALE)
    assert pooled is not None
    assert pooled.mean == pytest.approx(0.16, abs=0.02)
    assert pooled.n_studies == 23      # 7 + 2 + 9 + 5, summed through pooling


def test_pooled_effect_applies_topic_overlap_default():
    # The failure topics default to 1.35 SE inflation; passing 1.0 explicitly
    # must yield a tighter interval.
    default = registry.pooled_effect(Topic.FAILURE_HYPERTROPHY, TRAINED_MALE)
    no_overlap = registry.pooled_effect(
        Topic.FAILURE_HYPERTROPHY, TRAINED_MALE, overlap_se_inflation=1.0)
    assert default.se > no_overlap.se
    assert default.se == pytest.approx(no_overlap.se * 1.35)


def test_pooled_single_source_topic_returns_the_estimate():
    pooled = registry.pooled_effect(Topic.VOLUME_HYPERTROPHY, TRAINED_MALE)
    assert pooled is not None
    assert pooled.mean == pytest.approx(0.24)


def test_pooled_effect_none_when_user_out_of_range():
    assert registry.pooled_effect(Topic.VOLUME_HYPERTROPHY, OUT_OF_RANGE) is None


# ---------------------------------------------------------------------------
# Emphasis lookups
# ---------------------------------------------------------------------------

def test_emphasis_lookup_hits_known_key():
    items = registry.emphasis("cable_overhead_extension", "triceps_brachii",
                              "long_head")
    assert len(items) == 1
    assert items[0].emphasis == 1.0


def test_emphasis_lookup_unknown_key_is_empty():
    assert registry.emphasis("no_such_exercise", "triceps_brachii") == []


def test_combined_emphasis_passthrough_for_single_source():
    combined = registry.combined_emphasis(
        "cable_pushdown", "triceps_brachii", "long_head")
    assert isinstance(combined, ExerciseEmphasis)
    assert combined.emphasis == pytest.approx(0.69, abs=0.01)


def test_combined_emphasis_unknown_key_is_none():
    assert registry.combined_emphasis("no_such_exercise", "triceps_brachii") is None


def test_emphasis_for_muscle_ranks_exercises_by_region():
    long_head = registry.emphasis_for_muscle("triceps_brachii", "long_head")
    assert set(long_head) == {"cable_overhead_extension", "cable_pushdown"}
    # the reference exercise outranks the pushdown for the long head
    assert (long_head["cable_overhead_extension"].emphasis
            > long_head["cable_pushdown"].emphasis)


def test_emphasis_for_muscle_default_region_is_whole_muscle():
    whole = registry.emphasis_for_muscle("triceps_brachii")
    assert set(whole) == {"cable_overhead_extension", "cable_pushdown"}
    assert all(e.region is None for e in whole.values())


def test_registry_indexes_kassiano_gastrocnemius_emphasis():
    items = registry.emphasis("lengthened_partial_calf_raise", "gastrocnemius",
                              "medial_head")
    assert len(items) == 1
    assert items[0].emphasis == 1.0


def test_emphasis_for_muscle_ranks_calf_raise_variants():
    medial = registry.emphasis_for_muscle("gastrocnemius", "medial_head")
    assert set(medial) == {"lengthened_partial_calf_raise", "full_rom_calf_raise",
                           "shortened_partial_calf_raise"}
    # the lengthened partial is the top-ranked calf-raise variant
    best = max(medial.values(), key=lambda e: e.emphasis)
    assert best.exercise == "lengthened_partial_calf_raise"


def test_registry_indexes_maeo_2021_hamstrings_emphasis():
    items = registry.emphasis("seated_leg_curl", "hamstrings", None)
    assert len(items) == 1
    assert items[0].emphasis == 1.0


def test_emphasis_for_muscle_ranks_leg_curl_variants_whole_hamstrings():
    whole = registry.emphasis_for_muscle("hamstrings")
    assert set(whole) == {"seated_leg_curl", "prone_leg_curl"}
    # the seated leg curl out-grew the prone leg curl for the whole hamstrings
    assert whole["seated_leg_curl"].emphasis > whole["prone_leg_curl"].emphasis


def test_emphasis_for_muscle_resolves_hamstring_sub_muscles():
    # the sub-muscle taxonomy is queryable per biarticular head
    bfl = registry.emphasis_for_muscle("hamstrings", "biceps_femoris_long_head")
    assert set(bfl) == {"seated_leg_curl", "prone_leg_curl"}
    assert bfl["seated_leg_curl"].emphasis == 1.0


def test_registry_indexes_chaves_chest_emphasis():
    items = registry.emphasis("incline_bench_press", "pectoralis_major",
                              "clavicular_head")
    assert len(items) == 1
    assert items[0].emphasis == 1.0
    assert items[0].confidence == "high"


def test_emphasis_for_muscle_ranks_bench_press_variants_clavicular():
    # incline press out-grew the flat press for the upper (clavicular) chest
    clavicular = registry.emphasis_for_muscle("pectoralis_major",
                                              "clavicular_head")
    assert set(clavicular) == {"incline_bench_press", "horizontal_bench_press",
                               "combination_bench_press"}
    best = max(clavicular.values(), key=lambda e: e.emphasis)
    assert best.exercise == "incline_bench_press"
    assert (clavicular["incline_bench_press"].emphasis
            > clavicular["horizontal_bench_press"].emphasis)


def test_emphasis_for_muscle_chest_sternocostal_is_low_confidence():
    # the mid/lower chest showed no significant between-group difference
    sternocostal = registry.emphasis_for_muscle("pectoralis_major",
                                                "sternocostal_head")
    assert set(sternocostal) == {"incline_bench_press", "horizontal_bench_press",
                                 "combination_bench_press"}
    assert all(e.confidence == "low" for e in sternocostal.values())


# ---------------------------------------------------------------------------
# Guidance
# ---------------------------------------------------------------------------

def test_guidance_collects_module_contributions():
    g = registry.guidance()
    # 14 modules expose GUIDANCE_FOR_OPTIMIZER: schoenfeld (volume),
    # schoenfeld_load, varovic, wolf, maeo_2023, kassiano, pedrosa, maeo_2021,
    # singer_2024 (inter-set rest interval), plotkin_2023 (glute selection),
    # chaves_2020 (chest selection), mechanistic_lats + mechanistic_deltoids
    # (fallback priors), exercise_involvement (ADR-011 volume accounting)
    assert len(g) == 14
    assert "inter-set rest interval" in g
    assert "glute exercise selection (hip thrust vs back squat)" in g
    assert "chest exercise selection (incline vs flat bench press)" in g
    assert "lat exercise selection (mechanistic fallback prior)" in g
    assert "deltoid exercise selection (mechanistic fallback prior)" in g
    assert "exercise -> muscle involvement (volume accounting)" in g
    assert all(isinstance(v, str) and v for v in g.values())


# ---------------------------------------------------------------------------
# Mechanistic fallback tier (ADR-010)
# ---------------------------------------------------------------------------

def test_mechanistic_index_is_separate_from_measured_emphasis():
    # the mechanistic priors must NOT have leaked into the measured emphasis
    # index — they are a structurally separate fallback tier
    assert len(registry._MECHANISTIC_INDEX) == 26      # 17 lats + 9 deltoids
    for (exercise, muscle, region) in registry._MECHANISTIC_INDEX:
        assert muscle in ("latissimus_dorsi", "deltoids")
        assert (exercise, muscle, region) not in registry._EMPHASIS_INDEX


def test_mechanistic_emphasis_for_muscle_lats():
    whole = registry.mechanistic_emphasis_for_muscle("latissimus_dorsi")
    upper = registry.mechanistic_emphasis_for_muscle("latissimus_dorsi", "upper_fibres")
    lower = registry.mechanistic_emphasis_for_muscle("latissimus_dorsi", "lower_fibres")
    assert len(whole) == 7 and len(upper) == 5 and len(lower) == 5
    # stretch-loaded isolation tops the whole-muscle prior
    assert whole["dumbbell_pullover"].emphasis == 1.0
    assert whole["barbell_row"].emphasis == 0.50


def test_selection_emphasis_picks_the_right_tier():
    # a muscle with a measured trial -> "measured", never the fallback
    tier, mapping = registry.selection_emphasis("triceps_brachii", "long_head")
    assert tier == "measured" and mapping
    # lats: no measured trial -> the mechanistic fallback
    tier, mapping = registry.selection_emphasis("latissimus_dorsi")
    assert tier == "mechanistic" and len(mapping) == 7
    # nothing encoded at all
    tier, mapping = registry.selection_emphasis("spleen")
    assert tier == "none" and mapping == {}


def test_mechanistic_emphasis_for_muscle_deltoids():
    for head in ("anterior", "lateral", "posterior"):
        entries = registry.mechanistic_emphasis_for_muscle("deltoids", head)
        assert len(entries) == 3
    # deltoids has no measured trial -> selection_emphasis returns the fallback
    tier, mapping = registry.selection_emphasis("deltoids", "lateral")
    assert tier == "mechanistic" and len(mapping) == 3


# ---------------------------------------------------------------------------
# Involvement map — cross-muscle volume accounting (ADR-011)
# ---------------------------------------------------------------------------

def test_involvement_index_size_and_type():
    from app.priors.shared import ExerciseInvolvement
    assert len(registry._INVOLVEMENT_INDEX) == 74
    # a structurally separate index — its own type, never an emphasis estimate
    for v in registry._INVOLVEMENT_INDEX.values():
        assert isinstance(v, ExerciseInvolvement)


def test_involvement_for_exercise():
    rows = registry.involvement_for_exercise("barbell_row")
    muscles = {r.muscle for r in rows}
    assert {"latissimus_dorsi", "biceps_brachii", "erector_spinae"} <= muscles
    # an unknown exercise -> empty, not an error
    assert registry.involvement_for_exercise("no_such_exercise") == []


def test_involvement_for_muscle():
    rows = registry.involvement_for_muscle("biceps_brachii")
    exercises = {r.exercise for r in rows}
    # rows and vertical pulls all bank indirect biceps volume
    assert {"barbell_row", "pull_up", "lat_pulldown"} <= exercises
    # every biceps row in the prototype is a secondary (indirect) contributor
    assert all(r.role == "secondary" for r in rows)


def test_set_credit_values_follow_role():
    assert registry.set_credit("barbell_row", "latissimus_dorsi") == 1.0  # primary
    assert registry.set_credit("barbell_row", "biceps_brachii") == 0.5    # secondary
    assert registry.set_credit("barbell_row", "erector_spinae") == 0.0    # stabiliser


def test_set_credit_unknown_pair_is_none_not_zero():
    # the silent-0.0 fix: an unclassified pair returns None — distinct from a
    # stabiliser's KNOWN 0.0 credit
    assert registry.set_credit("barbell_row", "gastrocnemius") is None
    assert registry.set_credit("no_such_exercise", "latissimus_dorsi") is None
    # and 0.0 really is reserved for a known stabiliser
    assert registry.set_credit("barbell_row", "erector_spinae") == 0.0


def test_set_credit_serves_both_outcomes():
    for outcome in ("hypertrophy", "strength"):
        assert registry.set_credit(
            "barbell_row", "latissimus_dorsi", outcome) == 1.0
    # an outcome no row carries -> None
    assert registry.set_credit(
        "barbell_row", "latissimus_dorsi", "endurance") is None


def test_fractional_set_count():
    # 4 sets of barbell row: 4.0 fractional sets to the lats, 2.0 to the
    # biceps, 0.0 to the bracing erectors
    assert registry.fractional_set_count("barbell_row", "latissimus_dorsi", 4) == 4.0
    assert registry.fractional_set_count("barbell_row", "biceps_brachii", 4) == 2.0
    assert registry.fractional_set_count("barbell_row", "erector_spinae", 4) == 0.0
    # unknown pair -> None, never a misleading 0.0
    assert registry.fractional_set_count("barbell_row", "gastrocnemius", 4) is None
