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
    assert len(topics) == 12
    assert Topic.VOLUME_HYPERTROPHY in topics
    assert Topic.ARM_POSITION_HYPERTROPHY in topics
    assert Topic.LOAD_HYPERTROPHY in topics
    assert Topic.LOAD_STRENGTH in topics


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


# ---------------------------------------------------------------------------
# Guidance
# ---------------------------------------------------------------------------

def test_guidance_collects_module_contributions():
    g = registry.guidance()
    # 7 modules expose GUIDANCE_FOR_OPTIMIZER: schoenfeld (volume),
    # schoenfeld_load, varovic, wolf, maeo, kassiano, pedrosa
    assert len(g) == 7
    assert all(isinstance(v, str) and v for v in g.values())
