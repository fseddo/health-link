"""
Unit tests for app/priors/shared.py — the priors-layer infrastructure.

Covers the load-bearing logic that has no other check: applicability scoring,
the dataclass validators, inverse-variance pooling, population merging,
emphasis combination, and the n_studies plumbing added in the 2026-05-17 audit.

Run from the priors-handoff root:  python -m pytest tests/priors/
"""

import math

import pytest

from app.priors.shared import (
    Citation,
    CombinedCitation,
    PopulationSpec,
    UserProfile,
    EffectEstimate,
    ExerciseEmphasis,
    combine_inverse_variance,
    combine_emphasis_estimates,
    best_applicable,
    combine_for_user,
    _merge_populations,
)


# ---------------------------------------------------------------------------
# Small builders so each test reads as one idea, not ten keyword args.
# ---------------------------------------------------------------------------

CIT = Citation(authors="Pelland et al.", year=2026, doi="10.0/x")


def pop(training_status="trained", sex="male", age_range=(20, 30),
        outcome="hypertrophy"):
    return PopulationSpec(
        training_status=training_status, sex=sex,
        age_range=age_range, outcome=outcome,
    )


def est(mean=0.2, se=0.1, n=100, quality=0.8, scale="standardized_mean_diff",
        n_studies=None, population=None):
    return EffectEstimate(
        mean=mean, se=se, n=n,
        population=population or pop(),
        source=CIT, quality_score=quality, scale=scale, n_studies=n_studies,
    )


def emph(exercise="cable_overhead_extension", muscle="triceps_brachii",
         region="long_head", emphasis=1.0, confidence="high", quality=0.89):
    return ExerciseEmphasis(
        exercise=exercise, muscle=muscle, region=region, emphasis=emphasis,
        confidence=confidence, source=CIT, rationale="test",
        population=pop(), quality_score=quality,
    )


# ---------------------------------------------------------------------------
# Citations
# ---------------------------------------------------------------------------

def test_citation_str_and_short():
    assert str(CIT) == "Pelland et al. (2026)"
    assert CIT.short() == "Pelland 2026"


def test_combined_citation_formatting():
    a = Citation(authors="A et al.", year=2020)
    b = Citation(authors="B et al.", year=2021)
    c = Citation(authors="C et al.", year=2022)
    assert str(CombinedCitation((a,))) == "A et al. (2020)"
    assert str(CombinedCitation((a, b))) == "A et al. (2020) and B et al. (2021)"
    assert str(CombinedCitation((a, b, c))) == "A et al. (2020) and 2 others"


# ---------------------------------------------------------------------------
# PopulationSpec.applicability_to
# ---------------------------------------------------------------------------

def test_applicability_perfect_match():
    p = pop(training_status="trained", sex="male", age_range=(20, 30))
    user = UserProfile(age=25, sex="male", training_status="trained")
    assert p.applicability_to(user) == 1.0


def test_applicability_mixed_status_soft_penalty():
    p = pop(training_status="mixed")
    user = UserProfile(age=25, sex="male", training_status="trained")
    assert p.applicability_to(user) == pytest.approx(0.85)


def test_applicability_trained_vs_well_trained_close():
    p = pop(training_status="trained")
    user = UserProfile(age=25, sex="male", training_status="well_trained")
    assert p.applicability_to(user) == pytest.approx(0.9)


def test_applicability_genuinely_different_status():
    p = pop(training_status="trained")
    user = UserProfile(age=25, sex="male", training_status="untrained")
    assert p.applicability_to(user) == pytest.approx(0.5)


def test_applicability_sex_mismatch_penalised_but_mixed_is_free():
    user = UserProfile(age=25, sex="male", training_status="trained")
    assert pop(sex="female").applicability_to(user) == pytest.approx(0.75)
    assert pop(sex="mixed").applicability_to(user) == pytest.approx(1.0)


def test_applicability_age_degrades_outside_range():
    p = pop(age_range=(20, 30))
    below = UserProfile(age=10, sex="male", training_status="trained")
    above = UserProfile(age=40, sex="male", training_status="trained")
    # 10y below a lower bound of 20 -> 1 - 10/20 = 0.5
    assert p.applicability_to(below) == pytest.approx(0.5)
    # 10y above an upper bound of 30 -> 1 - 10/20 = 0.5
    assert p.applicability_to(above) == pytest.approx(0.5)


def test_applicability_age_floor_is_030():
    p = pop(age_range=(20, 30))
    far = UserProfile(age=80, sex="male", training_status="trained")
    assert p.applicability_to(far) == pytest.approx(0.3)


def test_applicability_penalties_compound():
    p = pop(training_status="mixed", sex="female", age_range=(20, 30))
    user = UserProfile(age=40, sex="male", training_status="trained")
    # 0.85 (mixed) * 0.75 (sex) * 0.5 (age 10y over) = 0.31875
    assert p.applicability_to(user) == pytest.approx(0.85 * 0.75 * 0.5)


# ---------------------------------------------------------------------------
# EffectEstimate validation and derived properties
# ---------------------------------------------------------------------------

def test_effect_estimate_rejects_non_positive_se():
    with pytest.raises(ValueError):
        est(se=0.0)
    with pytest.raises(ValueError):
        est(se=-0.1)


def test_effect_estimate_rejects_out_of_range_quality():
    with pytest.raises(ValueError):
        est(quality=1.5)
    with pytest.raises(ValueError):
        est(quality=-0.01)


def test_effect_estimate_rejects_non_positive_n_studies():
    with pytest.raises(ValueError):
        est(n_studies=0)
    with pytest.raises(ValueError):
        est(n_studies=-3)
    # None is allowed (single primary study, or unknown)
    assert est(n_studies=None).n_studies is None


def test_ci_95_and_precision():
    e = est(mean=0.2, se=0.1)
    lo, hi = e.ci_95
    assert lo == pytest.approx(0.2 - 1.96 * 0.1)
    assert hi == pytest.approx(0.2 + 1.96 * 0.1)
    assert e.precision == pytest.approx(1 / 0.1 ** 2)


def test_with_inflated_se_carries_n_studies():
    e = est(se=0.1, n_studies=9)
    inflated = e.with_inflated_se(1.35)
    assert inflated.se == pytest.approx(0.135)
    assert inflated.n_studies == 9          # n_studies must survive the copy
    assert "SE inflated" in inflated.notes
    assert e.se == pytest.approx(0.1)       # original untouched


# ---------------------------------------------------------------------------
# combine_inverse_variance
# ---------------------------------------------------------------------------

def test_inverse_variance_pooling_known_values():
    # e1: mean 0.2, se 0.1 -> precision 100
    # e2: mean 0.4, se 0.2 -> precision 25
    # pooled mean = (100*0.2 + 25*0.4) / 125 = 0.24
    # pooled se   = sqrt(1/125)             = 0.0894427
    pooled = combine_inverse_variance([est(mean=0.2, se=0.1),
                                       est(mean=0.4, se=0.2)])
    assert pooled.mean == pytest.approx(0.24)
    assert pooled.se == pytest.approx(math.sqrt(1 / 125))


def test_inverse_variance_single_estimate_passthrough():
    e = est()
    assert combine_inverse_variance([e]) is e


def test_inverse_variance_rejects_mixed_scales():
    with pytest.raises(ValueError):
        combine_inverse_variance([est(scale="standardized_mean_diff"),
                                  est(scale="pct_per_set")])


def test_inverse_variance_rejects_empty():
    with pytest.raises(ValueError):
        combine_inverse_variance([])


def test_inverse_variance_sums_n_studies_when_present():
    pooled = combine_inverse_variance([est(n_studies=7), est(n_studies=2)])
    assert pooled.n_studies == 9


def test_inverse_variance_n_studies_none_when_none_reported():
    pooled = combine_inverse_variance([est(n_studies=None), est(n_studies=None)])
    assert pooled.n_studies is None


def test_inverse_variance_n_studies_partial_sums_what_it_has():
    # Only one estimate reports n_studies — sum should be just that one,
    # not None and not an error.
    pooled = combine_inverse_variance([est(n_studies=5), est(n_studies=None)])
    assert pooled.n_studies == 5


def test_inverse_variance_pools_participant_n():
    pooled = combine_inverse_variance([est(n=100), est(n=250)])
    assert pooled.n == 350


# ---------------------------------------------------------------------------
# _merge_populations
# ---------------------------------------------------------------------------

def test_merge_populations_widens_age_and_generalises_status():
    merged = _merge_populations([
        pop(training_status="trained", sex="male", age_range=(20, 30)),
        pop(training_status="untrained", sex="female", age_range=(25, 45)),
    ])
    assert merged.age_range == (20, 45)
    assert merged.training_status == "mixed"
    assert merged.sex == "mixed"


def test_merge_populations_keeps_status_when_uniform():
    merged = _merge_populations([pop(training_status="trained"),
                                 pop(training_status="trained")])
    assert merged.training_status == "trained"


def test_merge_populations_rejects_mixed_outcomes():
    with pytest.raises(ValueError):
        _merge_populations([pop(outcome="hypertrophy"),
                            pop(outcome="strength")])


# ---------------------------------------------------------------------------
# best_applicable
# ---------------------------------------------------------------------------

def test_best_applicable_prefers_higher_combined_score():
    user = UserProfile(age=25, sex="male", training_status="trained")
    strong = est(quality=0.9, n=400, population=pop())            # app 1.0
    weak = est(quality=0.5, n=20,
               population=pop(training_status="untrained"))       # app 0.5
    assert best_applicable([weak, strong], user) is strong


def test_best_applicable_returns_none_below_threshold():
    user = UserProfile(age=25, sex="male", training_status="trained")
    # age far outside range drives applicability to the 0.3 floor (< 0.5)
    far = est(population=pop(age_range=(60, 70)))
    assert best_applicable([far], user, min_applicability=0.5) is None


# ---------------------------------------------------------------------------
# combine_for_user
# ---------------------------------------------------------------------------

def test_combine_for_user_filters_then_pools():
    user = UserProfile(age=25, sex="male", training_status="trained")
    keep = est(mean=0.2, se=0.1, population=pop())
    drop = est(mean=0.9, se=0.1, population=pop(training_status="untrained"))
    pooled = combine_for_user([keep, drop], user, min_applicability=0.7)
    # 'drop' has applicability 0.5 < 0.7 and is excluded; result is just 'keep'
    assert pooled.mean == pytest.approx(0.2)


def test_combine_for_user_overlap_inflation_widens_se():
    user = UserProfile(age=25, sex="male", training_status="trained")
    estimates = [est(mean=0.2, se=0.1, population=pop()),
                 est(mean=0.3, se=0.1, population=pop())]
    naive = combine_for_user(estimates, user, overlap_se_inflation=1.0)
    adjusted = combine_for_user(estimates, user, overlap_se_inflation=1.35)
    assert adjusted.se > naive.se
    assert adjusted.se == pytest.approx(naive.se * 1.35)


def test_combine_for_user_returns_none_when_nothing_applies():
    user = UserProfile(age=25, sex="male", training_status="trained")
    far = est(population=pop(age_range=(60, 70)))
    assert combine_for_user([far], user, min_applicability=0.7) is None


# ---------------------------------------------------------------------------
# ExerciseEmphasis validation
# ---------------------------------------------------------------------------

def test_exercise_emphasis_rejects_out_of_range_emphasis():
    with pytest.raises(ValueError):
        emph(emphasis=1.5)
    with pytest.raises(ValueError):
        emph(emphasis=-0.1)


def test_exercise_emphasis_rejects_bad_confidence():
    with pytest.raises(ValueError):
        emph(confidence="very_high")


def test_exercise_emphasis_rejects_out_of_range_quality():
    with pytest.raises(ValueError):
        emph(quality=1.2)


# ---------------------------------------------------------------------------
# combine_emphasis_estimates
# ---------------------------------------------------------------------------

def test_combine_emphasis_quality_weighted_average():
    # weights are quality scores: 0.9 and 0.6
    # pooled = (0.9*1.0 + 0.6*0.6) / 1.5 = 1.26 / 1.5 = 0.84
    pooled = combine_emphasis_estimates([
        emph(emphasis=1.0, quality=0.9),
        emph(emphasis=0.6, quality=0.6),
    ])
    assert pooled.emphasis == pytest.approx(0.84)


def test_combine_emphasis_single_passthrough():
    e = emph()
    assert combine_emphasis_estimates([e]) is e


def test_combine_emphasis_empty_returns_none():
    assert combine_emphasis_estimates([]) is None


def test_combine_emphasis_rejects_different_keys():
    with pytest.raises(ValueError):
        combine_emphasis_estimates([
            emph(region="long_head"),
            emph(region="lateral_head"),
        ])


def test_combine_emphasis_takes_lowest_confidence_and_quality():
    pooled = combine_emphasis_estimates([
        emph(emphasis=1.0, confidence="high", quality=0.9),
        emph(emphasis=0.6, confidence="low", quality=0.6),
    ])
    assert pooled.confidence == "low"          # conservative: lowest wins
    assert pooled.quality_score == pytest.approx(0.6)


def test_combine_emphasis_weights_by_applicability_when_user_given():
    # A user far outside one source's population should pull the pooled value
    # toward the better-matching source.
    user = UserProfile(age=25, sex="male", training_status="trained")
    matched = emph(emphasis=1.0, quality=0.8)
    matched.population = pop(training_status="trained")
    mismatched = emph(emphasis=0.0, quality=0.8)
    mismatched.population = pop(training_status="untrained")
    pooled = combine_emphasis_estimates([matched, mismatched], user=user)
    # matched weight 0.8*1.0=0.8 ; mismatched 0.8*0.5=0.4
    # pooled = (0.8*1.0 + 0.4*0.0) / 1.2 = 0.6667
    assert pooled.emphasis == pytest.approx(0.8 / 1.2)
