"""
app/priors/registry.py — the single app-facing entry point to the priors layer.

Until now each paper module exported its own EffectEstimate / ExerciseEmphasis
objects and nothing collected them (BACKLOG.md: "prior modules aren't wired
into anything app-facing"). The registry is that collection layer. The
recommendation engine and optimizer should import ONLY this module, never the
individual paper modules.

What it does:
  1. Indexes every encoded EffectEstimate by the QUESTION it answers (a Topic),
     and every ExerciseEmphasis by (exercise, muscle, region).
  2. Provides query + pooling helpers, so a caller can ask "what does the
     literature say about volume -> hypertrophy for this user?" and get one
     answer with traceable provenance.

What it deliberately does NOT do: invent new scientific judgement. Pooling
reuses shared.combine_for_user; question-framing reuses each paper module's own
helper (e.g. failure_effects.hypertrophy_estimates_volume_equated). Every
judgement call is an explicit constant near the top of this file, not buried.

Open design questions (see BACKLOG.md) intentionally left for later:
  - cross-paper emphasis normalization once multiple "best in class" exercises
    exist for the same muscle;
  - whether higher-quality emphasis sources should dominate more aggressively
    than plain quality-weighted averaging.
These do not block the registry: today every emphasis (exercise, muscle,
region) KEY still has exactly one source, so combination is a passthrough.

Run as a module for a summary:  python -m app.priors.registry
"""

from __future__ import annotations

from enum import Enum

from .shared import (
    EffectEstimate,
    ExerciseEmphasis,
    ExerciseInvolvement,
    MechanisticEmphasis,
    UserProfile,
    combine_for_user,
    combine_emphasis_estimates,
)
from . import (
    pelland_2026, failure_effects, maeo_2023, varovic_2025, wolf_2023,
    schoenfeld_2017, kassiano_2023, pedrosa_2023, schoenfeld_load_2017,
    maeo_2021, singer_2024, plotkin_2023, chaves_2020, exercise_involvement,
)
from .mechanistic import lats as mechanistic_lats
from .mechanistic import deltoids as mechanistic_deltoids


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------
# ADR-007 (see priors-handoff/README.md): the `routines` table will store a
# `priors_version` so a program can be reproduced against the exact priors that
# generated it. Until the layer is integrated and committed, this is a
# placeholder; wire it to the git commit hash of app/priors/ at that point.
PRIORS_VERSION = "uncommitted-dev"


# ---------------------------------------------------------------------------
# Topics — the questions the encoded literature answers
# ---------------------------------------------------------------------------

class Topic(str, Enum):
    """A question the priors layer can answer. The value is a stable string
    key safe to log or persist alongside a recommendation."""
    VOLUME_HYPERTROPHY = "volume->hypertrophy"
    VOLUME_STRENGTH = "volume->strength"
    FREQUENCY_HYPERTROPHY = "frequency->hypertrophy"
    FREQUENCY_STRENGTH = "frequency->strength"
    LOAD_HYPERTROPHY = "load->hypertrophy"
    LOAD_STRENGTH = "load->strength"
    FAILURE_HYPERTROPHY = "failure->hypertrophy"
    FAILURE_STRENGTH = "failure->strength"
    ROM_HYPERTROPHY = "rom->hypertrophy"
    ROM_STRENGTH = "rom->strength"
    MUSCLE_LENGTH_REGIONAL_HYPERTROPHY = "muscle_length->regional_hypertrophy"
    ARM_POSITION_HYPERTROPHY = "arm_position->hypertrophy"
    REST_INTERVAL_HYPERTROPHY = "rest_interval->hypertrophy"
    # Exercise-vs-exercise selection. Distinct from every dose/form topic
    # above: those vary HOW you train and hold the exercise fixed; this varies
    # WHICH exercise. Estimates here are between-exercise contrasts and may sit
    # on per-paper raw scales (e.g. Plotkin 2023's raw-cm^2 CSA difference)
    # that are deliberately not poolable with the SMD / %-per-set topics.
    EXERCISE_SELECTION_HYPERTROPHY = "exercise_selection->hypertrophy"


# ---------------------------------------------------------------------------
# The effect index — every EffectEstimate, grouped by Topic
# ---------------------------------------------------------------------------

_EFFECT_INDEX: dict[Topic, list[EffectEstimate]] = {
    Topic.VOLUME_HYPERTROPHY: (pelland_2026.VOLUME_HYPERTROPHY_ESTIMATES
                               + schoenfeld_2017.VOLUME_HYPERTROPHY_ESTIMATES),
    Topic.VOLUME_STRENGTH: pelland_2026.VOLUME_STRENGTH_ESTIMATES,
    Topic.FREQUENCY_HYPERTROPHY: pelland_2026.FREQUENCY_HYPERTROPHY_ESTIMATES,
    Topic.FREQUENCY_STRENGTH: pelland_2026.FREQUENCY_STRENGTH_ESTIMATES,
    Topic.LOAD_HYPERTROPHY: schoenfeld_load_2017.LOAD_HYPERTROPHY_ESTIMATES,
    Topic.LOAD_STRENGTH: schoenfeld_load_2017.LOAD_STRENGTH_ESTIMATES,
    Topic.FAILURE_HYPERTROPHY: failure_effects.HYPERTROPHY_ESTIMATES,
    Topic.FAILURE_STRENGTH: failure_effects.STRENGTH_ESTIMATES,
    Topic.ROM_HYPERTROPHY: wolf_2023.HYPERTROPHY_ESTIMATES,
    Topic.ROM_STRENGTH: wolf_2023.STRENGTH_ESTIMATES,
    Topic.MUSCLE_LENGTH_REGIONAL_HYPERTROPHY: (varovic_2025.REGIONAL_ESTIMATES
                                               + pedrosa_2023.REGIONAL_ESTIMATES),
    Topic.ARM_POSITION_HYPERTROPHY: maeo_2023.WHOLE_MUSCLE_EFFECTS,
    Topic.REST_INTERVAL_HYPERTROPHY: singer_2024.HYPERTROPHY_ESTIMATES,
    Topic.EXERCISE_SELECTION_HYPERTROPHY: plotkin_2023.EXERCISE_SELECTION_ESTIMATES,
}

# Some topics carry estimates that should NOT all be pooled together because
# they answer subtly different framings. The paper module owns that judgement
# and exposes a helper; the registry just calls it. For every other topic the
# poolable set is the whole indexed list.
_POOLABLE_OVERRIDE = {
    # Vieira's non-volume-equated 0.75 must be excluded — see failure_effects.
    Topic.FAILURE_HYPERTROPHY: failure_effects.hypertrophy_estimates_volume_equated,
    Topic.FAILURE_STRENGTH: failure_effects.strength_estimates_volume_equated,
    # Schoenfeld 2017 and Pelland 2026 both answer volume->hypertrophy but are
    # NOT on a common scale (SMD/set vs %/set, raw vs fractional set counting,
    # linear vs square-root model). Pooling them would manufacture false
    # precision, so the poolable set is Pelland only; Schoenfeld stays visible
    # in effects() as directional corroboration. See schoenfeld_2017.py.
    Topic.VOLUME_HYPERTROPHY: lambda: list(pelland_2026.VOLUME_HYPERTROPHY_ESTIMATES),
    # Varovic 2025 is a meta-analysis; Pedrosa 2023 is a single primary study
    # on the same regional question. The pool is Varovic only: (1) Pedrosa 2023
    # is CONFIRMED to be one of Varovic's 12 included studies, so pooling both
    # would double-count it outright; (2) the region definitions differ
    # (Pedrosa 50%/70% vs Varovic proximal-25%/mid-50%/distal-75%). Pedrosa
    # stays visible in effects() as primary-evidence context. See pedrosa_2023.py.
    Topic.MUSCLE_LENGTH_REGIONAL_HYPERTROPHY: lambda: list(varovic_2025.REGIONAL_ESTIMATES),
    # load->strength carries two estimates from Schoenfeld/Grgic 2017 — 1RM
    # (dynamic) and isometric strength. They are DIFFERENT outcomes (the paper's
    # finding is that load affects them differently), so they must not be
    # inverse-variance pooled. The 1RM estimate is the poolable representative
    # — it is the strength outcome a progression model acts on.
    Topic.LOAD_STRENGTH: lambda: [schoenfeld_load_2017.LOAD_STRENGTH_1RM_HIGH_VS_LOW],
    # rest_interval->hypertrophy carries Singer 2024's three region-keyed
    # estimates (arm / thigh / whole body). The whole-body estimate points the
    # OPPOSITE way (-0.08) to arm and thigh (+0.13 / +0.17) and rests on a
    # different measurement construct (whole-body FFM, only 3 effect
    # measurements). Inverse-variance pooling all three would manufacture a
    # near-zero average representing none of them. The poolable set is arm +
    # thigh; Singer's module owns that judgement via poolable_estimates().
    # Whole body stays visible in effects() for inspection. See singer_2024.py.
    Topic.REST_INTERVAL_HYPERTROPHY: singer_2024.poolable_estimates,
    # exercise_selection->hypertrophy carries Plotkin 2023's seven
    # between-exercise (hip thrust minus back squat) contrasts. They share one
    # raw-cm^2 scale, so combine_inverse_variance would NOT raise -- but they
    # are contrasts for SEVEN DIFFERENT muscles (three glute-max subregions,
    # glute med+min, quadriceps, adductors, hamstrings). Pooling them would
    # average unrelated muscles into a meaningless number. The poolable set is
    # the three gluteus-maximus subregion contrasts only -- the paper's
    # primary, homogeneous question (one muscle, three subregions). The thigh
    # by-product contrasts stay visible in effects() for inspection. Even the
    # glute-max subset is a single-RCT result on a raw-cm^2 scale shared with
    # no other encoded estimate, so it never pools cross-paper. See
    # plotkin_2023.py.
    Topic.EXERCISE_SELECTION_HYPERTROPHY:
        lambda: list(plotkin_2023.GLUTEUS_MAXIMUS_ESTIMATES),
}

# Recommended SE-inflation when a topic's poolable set spans overlapping
# meta-analyses that share primary studies. Default is 1.0 (no inflation):
# every topic except the failure ones is currently single-source.
_OVERLAP_DEFAULT: dict[Topic, float] = {
    Topic.FAILURE_HYPERTROPHY: failure_effects.OVERLAP_SE_INFLATION,
    Topic.FAILURE_STRENGTH: failure_effects.OVERLAP_SE_INFLATION,
}


# ---------------------------------------------------------------------------
# The emphasis index — every ExerciseEmphasis, keyed (exercise, muscle, region)
# ---------------------------------------------------------------------------

# Maeo 2021 contributes emphasis only (seated vs prone leg curl, hamstrings).
# It is a Varovic 2025 constituent study, so it deliberately exports NO
# Topic-keyed EffectEstimate and needs NO _POOLABLE_OVERRIDE entry: the emphasis
# index is a separate path that never pools against Varovic's regional Topic.
#
# Chaves 2020 contributes emphasis only (incline vs horizontal vs combination
# bench press, pectoralis major clavicular & sternocostal heads). It is an
# exercise-vs-exercise SELECTION study mapping to no Topic, so -- like maeo_2021
# -- it exports NO Topic-keyed EffectEstimate and needs NO _POOLABLE_OVERRIDE
# entry; emphasis is routed through this separate index.
_EMPHASIS_SOURCES = (maeo_2023, kassiano_2023, maeo_2021, plotkin_2023, chaves_2020)

_EMPHASIS_INDEX: dict[tuple[str, str, str | None], list[ExerciseEmphasis]] = {}
for _module in _EMPHASIS_SOURCES:
    for _e in _module.EMPHASIS_ESTIMATES:
        _EMPHASIS_INDEX.setdefault((_e.exercise, _e.muscle, _e.region), []).append(_e)
del _module, _e


# ---------------------------------------------------------------------------
# The mechanistic index — DERIVED fallback exercise-selection priors
# ---------------------------------------------------------------------------
# A structurally separate index (ADR-010, proposed). It holds MechanisticEmphasis
# objects — biomechanics-derived priors for muscles with no longitudinal
# head-to-head trial (currently lats; deltoids next). It is NOT merged into
# _EMPHASIS_INDEX and is NEVER pooled with measured ExerciseEmphasis: a
# mechanistic prior is a fallback the optimizer reads only when measured
# emphasis is absent for a (muscle, region). One entry per key by construction.
_MECHANISTIC_SOURCES = (mechanistic_lats, mechanistic_deltoids)

_MECHANISTIC_INDEX: dict[tuple[str, str, str | None], MechanisticEmphasis] = {}
for _module in _MECHANISTIC_SOURCES:
    for _m in _module.MECHANISTIC_EMPHASIS:
        _key = (_m.exercise, _m.muscle, _m.region)
        if _key in _MECHANISTIC_INDEX:
            raise ValueError(f"duplicate mechanistic emphasis key: {_key}")
        _MECHANISTIC_INDEX[_key] = _m
del _module, _m, _key


# ---------------------------------------------------------------------------
# The involvement index — exercise -> muscle volume-accounting map (ADR-011)
# ---------------------------------------------------------------------------
# A THIRD index, separate from both _EMPHASIS_INDEX and _MECHANISTIC_INDEX. It
# answers a cross-muscle question — "one set of exercise A, how much volume to
# each muscle?" — not a within-muscle selection question. It is keyed
# (exercise, muscle); one row per key by construction. set_credit() returns
# None for an unknown pair (an explicit "flag for review"), so the silent-0.0
# under-counting of pelland_2026.fractional_set_count() does not recur here.
_INVOLVEMENT_INDEX: dict[tuple[str, str], ExerciseInvolvement] = {}
for _r in exercise_involvement.EXERCISE_INVOLVEMENT:
    _ikey = (_r.exercise, _r.muscle)
    if _ikey in _INVOLVEMENT_INDEX:
        raise ValueError(f"duplicate involvement key: {_ikey}")
    _INVOLVEMENT_INDEX[_ikey] = _r
del _r, _ikey


# ---------------------------------------------------------------------------
# Practical guidance text contributed by individual modules
# ---------------------------------------------------------------------------

_GUIDANCE_SOURCES = {
    "training volume": schoenfeld_2017,
    "training load (rep range)": schoenfeld_load_2017,
    "muscle_length / regional hypertrophy": varovic_2025,
    "range of motion": wolf_2023,
    "exercise selection / sub-muscle emphasis": maeo_2023,
    "calf training (range of motion)": kassiano_2023,
    "elbow flexor (range of motion / regional)": pedrosa_2023,
    "hamstrings exercise selection (seated vs prone leg curl)": maeo_2021,
    "inter-set rest interval": singer_2024,
    "glute exercise selection (hip thrust vs back squat)": plotkin_2023,
    "chest exercise selection (incline vs flat bench press)": chaves_2020,
    "lat exercise selection (mechanistic fallback prior)": mechanistic_lats,
    "deltoid exercise selection (mechanistic fallback prior)": mechanistic_deltoids,
    "exercise -> muscle involvement (volume accounting)": exercise_involvement,
}


# ---------------------------------------------------------------------------
# Query API
# ---------------------------------------------------------------------------

def all_topics() -> list[Topic]:
    """Every Topic the registry currently has evidence for."""
    return list(_EFFECT_INDEX.keys())


def effects(topic: Topic) -> list[EffectEstimate]:
    """All encoded estimates for a topic — including ones excluded from
    pooling. Use for inspection / display. A fresh list; safe to mutate."""
    return list(_EFFECT_INDEX.get(topic, []))


def poolable_effects(topic: Topic) -> list[EffectEstimate]:
    """The subset of `effects(topic)` that the paper module considers an
    apples-to-apples set for pooling (e.g. failure-hypertrophy excludes
    Vieira's non-volume-equated estimate)."""
    override = _POOLABLE_OVERRIDE.get(topic)
    if override is not None:
        return list(override())
    return effects(topic)


def pooled_effect(
    topic: Topic,
    user: UserProfile,
    *,
    min_applicability: float = 0.7,
    overlap_se_inflation: float | None = None,
) -> EffectEstimate | None:
    """Single best literature answer for `topic`, tailored to `user`.

    Pools the topic's poolable set via inverse-variance weighting, filtering to
    estimates applicable to the user. Returns None if nothing is applicable.

    `overlap_se_inflation` defaults to the topic's recommended value (1.35 for
    the failure topics, which span overlapping meta-analyses; 1.0 otherwise).
    Pass an explicit value to override.
    """
    if overlap_se_inflation is None:
        overlap_se_inflation = _OVERLAP_DEFAULT.get(topic, 1.0)
    return combine_for_user(
        poolable_effects(topic), user,
        min_applicability=min_applicability,
        overlap_se_inflation=overlap_se_inflation,
    )


def emphasis(
    exercise: str, muscle: str, region: str | None = None,
) -> list[ExerciseEmphasis]:
    """Every ExerciseEmphasis for one (exercise, muscle, region) key. Usually
    one entry today; multiple once more papers cover the same key."""
    return list(_EMPHASIS_INDEX.get((exercise, muscle, region), []))


def combined_emphasis(
    exercise: str, muscle: str, region: str | None = None,
    user: UserProfile | None = None,
) -> ExerciseEmphasis | None:
    """The consensus emphasis coefficient for one key — quality-weighted
    average across sources (passthrough when there is only one). Returns None
    if the key is unknown."""
    return combine_emphasis_estimates(emphasis(exercise, muscle, region), user=user)


def emphasis_for_muscle(
    muscle: str, region: str | None = None,
) -> dict[str, ExerciseEmphasis]:
    """Map of exercise -> combined emphasis for a (muscle, region). This is what
    an optimizer reads to rank exercises for a muscle goal. `region` matches
    exactly: the default None selects whole-muscle coefficients; pass e.g.
    "long_head" to rank exercises for that sub-muscle."""
    out: dict[str, ExerciseEmphasis] = {}
    for (exercise, m, r), items in _EMPHASIS_INDEX.items():
        if m != muscle or r != region:
            continue
        combined = combine_emphasis_estimates(items)
        if combined is not None:
            out[exercise] = combined
    return out


def mechanistic_emphasis_for_muscle(
    muscle: str, region: str | None = None,
) -> dict[str, MechanisticEmphasis]:
    """Map of exercise -> DERIVED mechanistic prior for a (muscle, region).

    This is the fallback tier (ADR-010): biomechanics-derived, not measured,
    and NOT pooled with measured `ExerciseEmphasis`. The optimizer should call
    `emphasis_for_muscle()` first and consult this only when that returns
    nothing. Use `selection_emphasis()` to get the right tier automatically."""
    out: dict[str, MechanisticEmphasis] = {}
    for (exercise, m, r), entry in _MECHANISTIC_INDEX.items():
        if m == muscle and r == region:
            out[exercise] = entry
    return out


def selection_emphasis(
    muscle: str, region: str | None = None,
) -> tuple[str, dict]:
    """Exercise-selection priors for a (muscle, region), with the evidence tier
    made explicit. Returns `(tier, mapping)`:

      - `("measured", {exercise: ExerciseEmphasis})`   — a longitudinal trial
        exists; the mechanistic fallback is NOT consulted.
      - `("mechanistic", {exercise: MechanisticEmphasis})` — no measured
        source; derived fallback prior (ADR-010).
      - `("none", {})` — nothing encoded for this key.

    The tier tag tells the caller which value type it holds and how much to
    trust it; the two tiers are never mixed."""
    measured = emphasis_for_muscle(muscle, region)
    if measured:
        return ("measured", measured)
    mechanistic = mechanistic_emphasis_for_muscle(muscle, region)
    if mechanistic:
        return ("mechanistic", mechanistic)
    return ("none", {})


# ---------------------------------------------------------------------------
# Involvement queries — cross-muscle volume accounting (ADR-011)
# ---------------------------------------------------------------------------

def involvement_for_exercise(exercise: str) -> list[ExerciseInvolvement]:
    """Every muscle one exercise trains, each with its role and set credit.
    Empty if the exercise is not in the involvement map."""
    return [v for (ex, _m), v in _INVOLVEMENT_INDEX.items() if ex == exercise]


def involvement_for_muscle(muscle: str) -> list[ExerciseInvolvement]:
    """Every exercise that trains one muscle, each with its role and set
    credit. This is what an optimizer reads to see where a muscle's weekly
    volume is coming from. Empty if no encoded exercise trains the muscle."""
    return [v for (_ex, m), v in _INVOLVEMENT_INDEX.items() if m == muscle]


def set_credit(
    exercise: str, muscle: str, outcome: str = "hypertrophy",
) -> float | None:
    """Fractional sets that one raw set of `exercise` credits to `muscle`
    (ADR-011): 1.0 primary / 0.5 secondary / 0.0 stabiliser.

    Returns None when the (exercise, muscle) pair is not in the map — an
    explicit 'unknown, flag for review'. A 0.0 is a *known* stabiliser, never
    a stand-in for 'unclassified'; this is the distinction
    pelland_2026.fractional_set_count()'s silent 0.0 fallback could not make."""
    row = _INVOLVEMENT_INDEX.get((exercise, muscle))
    if row is None or outcome not in row.outcomes:
        return None
    return row.set_credit


def fractional_set_count(
    exercise: str, muscle: str, raw_sets: float, outcome: str = "hypertrophy",
) -> float | None:
    """`raw_sets` scaled by the (exercise, muscle) set credit — the per-muscle
    weekly-volume contribution of an exercise. None when the pair is unknown
    (see set_credit)."""
    credit = set_credit(exercise, muscle, outcome)
    if credit is None:
        return None
    return raw_sets * credit


def guidance() -> dict[str, str]:
    """Plain-language optimizer guidance contributed by the paper modules
    (e.g. 'do not over-penalise partial ROM'). Keyed by subject area."""
    out: dict[str, str] = {}
    for subject, module in _GUIDANCE_SOURCES.items():
        text = getattr(module, "GUIDANCE_FOR_OPTIMIZER", None)
        if text:
            out[subject] = text.strip()
    return out


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Priors registry — version {PRIORS_VERSION}")
    print(f"{len(all_topics())} topics, "
          f"{sum(len(v) for v in _EFFECT_INDEX.values())} effect estimates, "
          f"{sum(len(v) for v in _EMPHASIS_INDEX.values())} emphasis coefficients")
    print(f"{len(_MECHANISTIC_INDEX)} mechanistic (fallback) emphasis priors "
          f"— biomechanics-derived, never pooled with measured emphasis")
    print(f"{len(_INVOLVEMENT_INDEX)} exercise->muscle involvement rows "
          f"— cross-muscle volume accounting (ADR-011)")
    print()
    for topic in all_topics():
        full = effects(topic)
        poolable = poolable_effects(topic)
        extra = "" if len(poolable) == len(full) else f" ({len(poolable)} poolable)"
        print(f"  {topic.value:<38} {len(full)} estimate(s){extra}")
