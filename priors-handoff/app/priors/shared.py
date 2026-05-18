"""
Shared infrastructure for literature-derived priors.

Every prior module returns EffectEstimate objects with metadata about
the source population, sample size, and uncertainty. The registry layer
combines estimates across papers when appropriate.

Design principles:
- Estimates are immutable once created (dataclass with frozen=False but
  treated as read-only after construction).
- Combination logic lives outside individual prior modules.
- Population matching is fuzzy; estimates are scored for applicability
  rather than filtered binary.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional
import math


# ----------------------------------------------------------------------------
# Citations
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Citation:
    """A single literature source."""
    authors: str               # "Pelland et al." or "Smith, Jones & Lee"
    year: int
    doi: Optional[str] = None
    journal: Optional[str] = None
    osf_url: Optional[str] = None  # if raw data is available

    def __str__(self) -> str:
        return f"{self.authors} ({self.year})"

    def short(self) -> str:
        """First-author short form for inline mentions."""
        first = self.authors.split()[0].rstrip(",")
        return f"{first} {self.year}"


@dataclass(frozen=True)
class CombinedCitation:
    """Multiple sources pooled together."""
    sources: tuple[Citation, ...]

    def __str__(self) -> str:
        if len(self.sources) == 1:
            return str(self.sources[0])
        if len(self.sources) == 2:
            return f"{self.sources[0]} and {self.sources[1]}"
        return f"{self.sources[0]} and {len(self.sources) - 1} others"


# ----------------------------------------------------------------------------
# Population specs and user matching
# ----------------------------------------------------------------------------

TrainingStatus = Literal["untrained", "trained", "well_trained", "mixed"]
SexCategory = Literal["male", "female", "mixed"]


@dataclass(frozen=True)
class PopulationSpec:
    """
    Describes the population an estimate was derived from.
    Used for applicability scoring against individual users.
    """
    training_status: TrainingStatus
    sex: SexCategory
    age_range: tuple[int, int]    # inclusive
    outcome: str                   # "hypertrophy" | "strength" | "endurance" | ...
    notes: str = ""

    def applicability_to(self, user: "UserProfile") -> float:
        """
        Score 0-1 of how applicable this estimate is to a given user.
        1.0 = perfect match. 0.0 = inapplicable.

        Used both for routing (pick best estimate) and as a quality
        modifier when combining (weight by applicability).
        """
        score = 1.0

        # Training status
        if user.training_status != self.training_status:
            if self.training_status == "mixed":
                score *= 0.85
            elif {user.training_status, self.training_status} == {"trained", "well_trained"}:
                score *= 0.9   # close enough
            else:
                score *= 0.5   # genuinely different population

        # Sex
        if self.sex != user.sex and self.sex != "mixed":
            score *= 0.75      # cross-sex effects often differ but not by much

        # Age (graceful degradation outside studied range)
        lo, hi = self.age_range
        if user.age < lo:
            score *= max(0.3, 1 - (lo - user.age) / 20)
        elif user.age > hi:
            score *= max(0.3, 1 - (user.age - hi) / 20)

        return score


@dataclass
class UserProfile:
    """The user characteristics relevant for prior selection."""
    age: int
    sex: SexCategory
    training_status: TrainingStatus
    notes: str = ""


# ----------------------------------------------------------------------------
# Effect estimates — the core unit of literature-derived knowledge
# ----------------------------------------------------------------------------

@dataclass
class EffectEstimate:
    """
    A single quantitative finding from a paper (or pooled across papers).

    All effect sizes are stored on a consistent scale within a given
    `outcome` so they can be pooled. Document the scale in `notes`.
    """
    mean: float                    # point estimate
    se: float                      # standard error
    n: int                         # total PARTICIPANTS (not study count — use n_studies)
    population: PopulationSpec
    source: Citation | CombinedCitation
    quality_score: float           # 0-1, see QUALITY_RUBRIC.md
    scale: str                     # "pct_per_set" | "standardized_mean_diff" | ...
    n_studies: int | None = None   # for meta-analyses: number of pooled studies.
                                   # None for single primary studies. Keep `n` as
                                   # participants so best_applicable()'s sqrt(n)
                                   # weighting stays on a consistent unit.
    notes: str = ""

    def __post_init__(self):
        if self.se <= 0:
            raise ValueError(f"SE must be positive, got {self.se}")
        if not 0 <= self.quality_score <= 1:
            raise ValueError(f"quality_score must be in [0,1], got {self.quality_score}")
        if self.n_studies is not None and self.n_studies <= 0:
            raise ValueError(f"n_studies must be positive when set, got {self.n_studies}")

    @property
    def ci_95(self) -> tuple[float, float]:
        """95% confidence/credible interval (assumes Normal)."""
        return (self.mean - 1.96 * self.se, self.mean + 1.96 * self.se)

    @property
    def precision(self) -> float:
        """1 / variance — the weight in inverse-variance pooling."""
        return 1 / (self.se ** 2)

    def with_inflated_se(self, factor: float) -> "EffectEstimate":
        """Return a copy with SE multiplied (e.g., for overlap penalty)."""
        return EffectEstimate(
            mean=self.mean,
            se=self.se * factor,
            n=self.n,
            population=self.population,
            source=self.source,
            quality_score=self.quality_score,
            scale=self.scale,
            n_studies=self.n_studies,
            notes=self.notes + f" [SE inflated x{factor:.2f}]",
        )


# ----------------------------------------------------------------------------
# Exercise emphasis — per-exercise, per-muscle contribution coefficients
# ----------------------------------------------------------------------------
# Distinct shape from EffectEstimate because the question is different.
#
# EffectEstimate answers: "how much does VARIABLE X change OUTCOME Y?"
#   (e.g., per-set hypertrophy effect, failure vs not effect)
#
# ExerciseEmphasis answers: "when you do EXERCISE A, how much stimulus does
#   MUSCLE M (or sub-region R within M) receive relative to a maximum-emphasis
#   exercise for that muscle?"
#
# Used by:
#   - Exercise selection in the optimizer: when the user says "grow triceps long
#     head", pick exercises whose long-head emphasis is highest. This is a
#     WITHIN-muscle ranking — 1.0 is the best exercise FOR THAT MUSCLE.
#
# NOT for fractional-set / cross-muscle volume counting ("a bench press counts
# ~0.5 sets toward triceps, ~1.0 toward chest"). That is a different question —
# how much volume an exercise credits to EACH muscle it touches — and has its
# own shape: ExerciseInvolvement (see ADR-011). Do not conflate the two.
# Emphasis is within-muscle and relative; involvement is cross-muscle.
#
# Coefficients are on [0.0, 1.0]. 1.0 = the exercise that maximally stimulates
# this muscle/region in the studied population. Values are RELATIVE within a
# muscle, not absolute. They are NOT effect sizes — they're inputs to the
# optimizer's objective function.

@dataclass
class ExerciseEmphasis:
    """
    Evidence-based emphasis coefficient for a specific (exercise, muscle, region) tuple.

    Multiple ExerciseEmphasis entries can exist for the same exercise+muscle
    if different studies report different values; combine via weighted average
    by quality_score (NOT inverse variance — these aren't on the same scale as
    classical SMDs/effect sizes).
    """
    exercise: str                  # canonical exercise key, e.g. "cable_overhead_extension"
    muscle: str                    # canonical muscle key, e.g. "triceps_brachii"
    region: str | None             # sub-region within muscle: "long_head" | "lateral_head" | None for whole
    emphasis: float                # [0.0, 1.0] — fraction of maximum stimulus this exercise provides
    confidence: str                # "high" | "medium" | "low" | "speculative"
    source: Citation | CombinedCitation
    rationale: str                 # WHY this number — e.g. "based on +28.5% hypertrophy in Maeo 2023"
    population: PopulationSpec
    quality_score: float           # quality of the source, 0-1

    def __post_init__(self):
        if not 0.0 <= self.emphasis <= 1.0:
            raise ValueError(f"emphasis must be in [0.0, 1.0], got {self.emphasis}")
        if not 0 <= self.quality_score <= 1:
            raise ValueError(f"quality_score must be in [0,1], got {self.quality_score}")
        if self.confidence not in ("high", "medium", "low", "speculative"):
            raise ValueError(f"confidence must be one of high/medium/low/speculative, got {self.confidence}")


def combine_emphasis_estimates(
    estimates: list[ExerciseEmphasis],
    user: "UserProfile | None" = None,
) -> ExerciseEmphasis | None:
    """
    Combine multiple emphasis estimates for the same (exercise, muscle, region)
    via quality-weighted average. Unlike effect-size pooling, this isn't
    statistical meta-analysis — it's a consensus value across sources.

    If user is provided, also weight by applicability of each source's population.
    """
    if not estimates:
        return None
    if len(estimates) == 1:
        return estimates[0]

    # Verify all estimates are for the same (exercise, muscle, region)
    keys = {(e.exercise, e.muscle, e.region) for e in estimates}
    if len(keys) > 1:
        raise ValueError(f"Cannot combine emphasis across different keys: {keys}")

    weights = []
    for e in estimates:
        w = e.quality_score
        if user is not None:
            w *= e.population.applicability_to(user)
        weights.append(w)

    total_w = sum(weights)
    if total_w == 0:
        return None

    pooled_emphasis = sum(w * e.emphasis for w, e in zip(weights, estimates)) / total_w

    # Lowest confidence wins (conservative)
    conf_order = ["high", "medium", "low", "speculative"]
    pooled_conf = max((e.confidence for e in estimates), key=lambda c: conf_order.index(c))

    pooled_quality = min(e.quality_score for e in estimates)

    return ExerciseEmphasis(
        exercise=estimates[0].exercise,
        muscle=estimates[0].muscle,
        region=estimates[0].region,
        emphasis=pooled_emphasis,
        confidence=pooled_conf,
        source=CombinedCitation(tuple(_extract_emphasis_citations(estimates))),
        rationale=f"Quality-weighted consensus across {len(estimates)} sources.",
        population=_merge_populations([e.population for e in estimates]),
        quality_score=pooled_quality,
    )


def _extract_emphasis_citations(estimates: list[ExerciseEmphasis]) -> list[Citation]:
    out = []
    for e in estimates:
        if isinstance(e.source, Citation):
            out.append(e.source)
        else:
            out.extend(e.source.sources)
    return out


# ----------------------------------------------------------------------------
# Mechanistic emphasis — a derived, fallback exercise-selection prior
# ----------------------------------------------------------------------------
# A SEPARATE shape from ExerciseEmphasis, and deliberately so. See
# docs/priors/proposals/ADR-010-mechanistic-emphasis-priors.md.
#
# ExerciseEmphasis encodes a MEASURED per-exercise growth result from a
# longitudinal trial. MechanisticEmphasis encodes a DERIVED prior for muscles
# where no such trial exists (e.g. lats, deltoids — "literature-blocked" in
# COVERAGE.md). It is built from biomechanics — does the exercise load the
# muscle, and at what muscle length is it loaded hardest — weighted by the
# layer's own encoded lengthened-position -> growth evidence. It is NOT
# derived from EMG (EMG's error is directional bias, and it under-reads long
# muscle lengths — exactly the signal this prior is built on).
#
# It is a FALLBACK: the optimizer uses it for a (muscle, region) only when no
# measured ExerciseEmphasis exists. A measured source always supersedes it.
#
# Three structural guarantees stop a derived prior being mistaken for measured
# evidence:
#   1. Distinct type — combine_emphasis_estimates() accepts only
#      ExerciseEmphasis, so a mechanistic prior can NEVER be pooled with
#      measured data.
#   2. confidence is capped at "low" (and may be "speculative").
#   3. No `source: Citation` — provenance is a model; `grounded_in` names the
#      encoded modules supplying the lengthened-position evidence.

LoadedLength = Literal["long", "mid", "short"]


@dataclass
class MechanisticEmphasis:
    """
    A derived, biomechanics-based exercise-selection prior for one
    (exercise, muscle, region) tuple — a fallback where no longitudinal
    head-to-head trial exists. See ADR-010.

    `emphasis` is a COARSE bucket, not a fitted value: it follows directly
    from `loaded_length` (long -> high, mid -> moderate, short -> low). We do
    not have a continuous "degree of stretch -> growth" curve and must not
    imply one.
    """
    exercise: str                   # canonical exercise key
    muscle: str                     # canonical muscle key
    region: str | None              # sub-region, or None for whole muscle
    emphasis: float                 # [0.0, 1.0] — a coarse bucket (see ADR-010)
    loaded_length: LoadedLength     # muscle length at the HARDEST point of the
                                    # exercise's resistance curve
    confidence: str                 # "low" | "speculative" — hard ceiling; a
                                    # derived prior is never "medium"/"high"
    rationale: str                  # the biomechanical reasoning, explicit
    grounded_in: tuple[str, ...]    # encoded module names supplying the
                                    # lengthened-position -> growth evidence

    def __post_init__(self):
        if not 0.0 <= self.emphasis <= 1.0:
            raise ValueError(f"emphasis must be in [0.0, 1.0], got {self.emphasis}")
        if self.loaded_length not in ("long", "mid", "short"):
            raise ValueError(
                f"loaded_length must be long/mid/short, got {self.loaded_length}")
        if self.confidence not in ("low", "speculative"):
            raise ValueError(
                "MechanisticEmphasis.confidence is capped at 'low' (or "
                f"'speculative') — a derived prior is never higher; got "
                f"{self.confidence}")
        if not self.grounded_in:
            raise ValueError(
                "grounded_in must name at least one encoded evidence module")


# ----------------------------------------------------------------------------
# Exercise involvement — which muscles an exercise trains, and how much
# ----------------------------------------------------------------------------
# A THIRD shape, distinct from both emphasis shapes. See
# docs/priors/proposals/ADR-011-exercise-involvement-map.md.
#
# The emphasis shapes (ExerciseEmphasis, MechanisticEmphasis) answer a
# WITHIN-muscle question: "for muscle M, which exercise — or which sub-region —
# trains it best?" ExerciseInvolvement answers a CROSS-muscle question: "one set
# of exercise A — how much training volume does it credit to EACH muscle it
# touches?" That is volume bookkeeping, not selection. The two never mix.
#
# `role` is uncontested anatomy: a muscle is a prime mover, an assisting
# synergist, or an isometric stabiliser of the exercise. `set_credit` maps role
# to a fractional-set weight via ROLE_SET_CREDIT — Pelland 2026's direct=1.0 /
# indirect=0.5 fractional-counting methodology (Sec. 2.5), which the paper
# applied to BOTH its hypertrophy and its strength volume regressions (the
# strength slope is on the `pct_per_fractional_set` scale). A stabiliser banks
# no hypertrophy volume -> 0.0.

InvolvementRole = Literal["primary", "secondary", "stabilizer"]
InvolvementBasis = Literal["pelland_2026_table1", "biomechanical"]
OutcomeKind = Literal["hypertrophy", "strength"]

# role -> fractional set credit. The ONLY place the direct/indirect weighting
# lives; a row never carries its own number. Revise here if a dedicated
# fractional-/effective-set paper is ever encoded.
ROLE_SET_CREDIT: dict[str, float] = {
    "primary": 1.0,      # direct work — Pelland 2026 direct weight
    "secondary": 0.5,    # indirect work — Pelland 2026 indirect heuristic
    "stabilizer": 0.0,   # isometric stabilisation — no hypertrophy credit
}


@dataclass(frozen=True)
class ExerciseInvolvement:
    """
    One (exercise, muscle) involvement row: the role a muscle plays in an
    exercise, and — via ROLE_SET_CREDIT — the fractional training volume that
    one set of the exercise credits to that muscle. See ADR-011.

    `set_credit` is DERIVED from `role`, never stored, so the crediting
    heuristic lives in exactly one constant (ROLE_SET_CREDIT).

    `outcomes` defaults to both hypertrophy and strength: the role is anatomy
    and does not change with training goal. It narrows only if Pelland's
    separate strength classification (Table 2) is ever encoded and shows a
    genuine strength-specific reclassification.
    """
    exercise: str                   # canonical exercise key
    muscle: str                     # canonical muscle key
    role: InvolvementRole           # prime mover / synergist / stabiliser
    basis: InvolvementBasis         # how the role was determined
    rationale: str                  # the anatomical reasoning, explicit
    outcomes: tuple[OutcomeKind, ...] = ("hypertrophy", "strength")

    def __post_init__(self):
        if self.role not in ("primary", "secondary", "stabilizer"):
            raise ValueError(
                f"role must be primary/secondary/stabilizer, got {self.role}")
        if self.basis not in ("pelland_2026_table1", "biomechanical"):
            raise ValueError(
                "basis must be pelland_2026_table1/biomechanical, got "
                f"{self.basis}")
        if not self.outcomes:
            raise ValueError("outcomes must name at least one outcome")
        for o in self.outcomes:
            if o not in ("hypertrophy", "strength"):
                raise ValueError(f"outcome must be hypertrophy/strength, got {o}")
        if not self.rationale:
            raise ValueError("rationale must be non-empty")

    @property
    def set_credit(self) -> float:
        """Fractional sets that one raw set of this exercise credits to this
        muscle — Pelland 2026 fractional counting (direct 1.0 / indirect 0.5;
        a stabiliser banks 0.0)."""
        return ROLE_SET_CREDIT[self.role]


# ----------------------------------------------------------------------------
# Combination logic — pooling estimates across papers
# ----------------------------------------------------------------------------

def combine_inverse_variance(estimates: list[EffectEstimate]) -> EffectEstimate:
    """
    Fixed-effect meta-analytic pooling.
    Each estimate weighted by inverse variance (precision).
    Larger / more precise studies dominate appropriately.

    Requires all estimates to be on the same scale.
    """
    if not estimates:
        raise ValueError("Need at least one estimate to pool")
    if len(estimates) == 1:
        return estimates[0]

    scales = {e.scale for e in estimates}
    if len(scales) > 1:
        raise ValueError(f"Cannot pool different scales: {scales}")

    weights = [e.precision for e in estimates]
    total_weight = sum(weights)

    pooled_mean = sum(w * e.mean for w, e in zip(weights, estimates)) / total_weight
    pooled_se = math.sqrt(1 / total_weight)

    # Sum study counts only across estimates that report them; None if none do.
    study_counts = [e.n_studies for e in estimates if e.n_studies is not None]
    pooled_n_studies = sum(study_counts) if study_counts else None

    return EffectEstimate(
        mean=pooled_mean,
        se=pooled_se,
        n=sum(e.n for e in estimates),
        population=_merge_populations([e.population for e in estimates]),
        source=CombinedCitation(tuple(_extract_citations(estimates))),
        quality_score=min(e.quality_score for e in estimates),
        scale=estimates[0].scale,
        n_studies=pooled_n_studies,
        notes=f"Pooled from {len(estimates)} sources via inverse-variance weighting",
    )


def _extract_citations(estimates: list[EffectEstimate]) -> list[Citation]:
    out = []
    for e in estimates:
        if isinstance(e.source, Citation):
            out.append(e.source)
        else:
            out.extend(e.source.sources)
    return out


def _merge_populations(pops: list[PopulationSpec]) -> PopulationSpec:
    """Conservative merge — widest age range, most-restrictive status if matched."""
    age_lows = [p.age_range[0] for p in pops]
    age_highs = [p.age_range[1] for p in pops]
    outcomes = {p.outcome for p in pops}
    if len(outcomes) > 1:
        raise ValueError(f"Cannot merge populations with different outcomes: {outcomes}")
    statuses = {p.training_status for p in pops}
    sexes = {p.sex for p in pops}
    return PopulationSpec(
        training_status="mixed" if len(statuses) > 1 else next(iter(statuses)),
        sex="mixed" if len(sexes) > 1 else next(iter(sexes)),
        age_range=(min(age_lows), max(age_highs)),
        outcome=next(iter(outcomes)),
        notes=f"Merged from {len(pops)} populations",
    )


def best_applicable(
    estimates: list[EffectEstimate],
    user: UserProfile,
    min_applicability: float = 0.5,
) -> Optional[EffectEstimate]:
    """
    Return the single best estimate for a given user, or None if no
    estimate meets the minimum applicability threshold.

    "Best" = highest applicability * quality * sqrt(n) — a heuristic
    that rewards relevance, methodological quality, and statistical power.
    """
    scored = []
    for e in estimates:
        app = e.population.applicability_to(user)
        if app < min_applicability:
            continue
        score = app * e.quality_score * math.sqrt(e.n)
        scored.append((score, e))
    if not scored:
        return None
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def combine_for_user(
    estimates: list[EffectEstimate],
    user: UserProfile,
    min_applicability: float = 0.7,
    overlap_se_inflation: float = 1.0,
) -> Optional[EffectEstimate]:
    """
    Combine all sufficiently-applicable estimates for a user via
    inverse-variance pooling.

    Set overlap_se_inflation > 1.0 if some included estimates share
    underlying studies (rough adjustment for non-independence).
    """
    applicable = [
        e for e in estimates
        if e.population.applicability_to(user) >= min_applicability
    ]
    if not applicable:
        return None
    if overlap_se_inflation > 1.0:
        applicable = [e.with_inflated_se(overlap_se_inflation) for e in applicable]
    return combine_inverse_variance(applicable)
