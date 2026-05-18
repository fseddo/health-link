# ADR-010 — Mechanistic exercise-selection priors

**Status:** ACCEPTED (2026-05-17). Prototype implemented — `MechanisticEmphasis`
in `shared.py`; `app/priors/mechanistic/lats.py` (17 priors); registry
`_MECHANISTIC_INDEX` + the tiered `selection_emphasis()` query; smoke + registry
tests (suite 214 → 228, all passing). The lats prototype validated the design;
the upper/lower regional entries are retained at `confidence="speculative"`.
Deltoids followed (`app/priors/mechanistic/deltoids.py`, 9 per-head priors at
`confidence="low"`). A dedicated `priors-mechanistic-auditor` agent gates the
tier — it re-derives the biomechanics independently (there is no paper to
re-read); audit docs in `docs/priors/audits/mechanistic_*_audit.md`.
**Date:** 2026-05-17
**Supersedes/addresses:** `BACKLOG.md` open infrastructure question 2
("stretch-mediated hypertrophy boost coefficient?").
**Numbering:** provisional. The priors layer's ADRs 007–009 are themselves
still pending integration into the repo's `docs/DECISIONS.md`; this would land
as ADR-010 alongside them.
**Amended by:** ADR-012 (2026-05-18, §3) — broadens the mechanistic tier's
scope from literature-blocked *muscles* to any untrialled *exercise*: a
mechanistic emphasis fills any `(exercise, muscle, region)` that lacks a
measured source, and tier resolution becomes per-exercise within a muscle. The
data shape, the derivation method, and the no-pool / confidence-cap / no-EMG
guarantees are unchanged.

---

## Context

Exercise-selection coverage is the priors layer's weakest area: of ~23 muscle
rows in `COVERAGE.md` §2, only 3 are `Covered` and 1 is `Thin`. Two major
muscle groups — **latissimus dorsi / mid-back** and **deltoids** — are
`literature-blocked`: no longitudinal head-to-head exercise-comparison RCT
exists. Their literature is almost entirely acute surface-EMG activation
studies, which the layer hard-excludes (ADR rationale: EMG's error is
*directional bias*, not variance, so down-weighting cannot rescue it).

Consequence: the optimizer cannot build an evidence-backed whole-body program —
a stated research goal — because for several muscles it has no exercise-
selection prior at all.

A candidate fix was evaluated: identify exercises that load a muscle at long
muscle length (our own encoded trials — Maeo 2023 triceps, Maeo 2021
hamstrings, Kassiano 2023 calves, Wolf 2023 ROM meta-analysis — consistently
show lengthened-biased training grows muscle more), and use that as a
selection prior. The originally-paired idea of confirming involvement with EMG
was **rejected**: surface-EMG amplitude is systematically *lower* at long
muscle lengths, so EMG is anti-correlated with the lengthened signal exactly
where it matters — it would reject the best candidates. EMG is out.

What remains is sound: a prior built from biomechanics + the layer's own
lengthened-position evidence, with no EMG.

## Decision

Introduce a **separate, explicitly-labelled mechanistic-prior tier** for
exercise selection: a `MechanisticEmphasis` data shape, derived from
biomechanical reasoning and the encoded lengthened-position evidence — never
from EMG, never from a single paper's measured per-exercise growth.

It is a **fallback prior**: the optimizer consults it for a `(muscle, region)`
only when no measured `ExerciseEmphasis` exists. A measured source always
supersedes it.

### How a mechanistic emphasis value is derived

For a given `(exercise, muscle, region)`:

1. **Involvement gate (anatomy).** Does the exercise load a joint action the
   muscle produces? (origin/insertion, line of pull). If not → not encoded.
   This is the question EMG is least-bad at, and anatomy answers it without
   EMG's bias.

2. **Loaded-length classification (biomechanics).** Find the *hardest point*
   of the exercise's resistance curve — where the external moment is largest
   relative to the muscle's leverage. At that point, classify the target
   muscle's length as **LONG / MID / SHORT**, from the joint angle(s) and the
   muscle's length-vs-angle relationship. Bi-articular muscles (lats, triceps
   long head, hamstrings, rectus femoris) depend on **two** joints — this is
   the subtle case (it was the whole point of Maeo's hamstring result: the
   *hip* angle, not the knee).

   Key refinement: it is not "does the ROM pass through a long length" but
   "is the muscle **loaded** while long." A standard pulldown stretches the
   lat at the top but is hardest near the bottom (contracted); a pullover
   loads the stretch. Same muscle, opposite verdict.

3. **Map to a coefficient via the lengthened-position prior.** LONG → high,
   MID → moderate, SHORT → low (a short-loaded exercise still trains the
   muscle — the layer's evidence says it grows it *less*, not *none*). These
   are **coarse buckets**, not a fitted dose-response: we do not have a
   continuous "degree of stretch → growth" curve, and must not pretend to.

### Data shape

A new dataclass in `shared.py`, distinct from `ExerciseEmphasis`:

```
MechanisticEmphasis(
    exercise, muscle, region,
    emphasis: float,            # [0,1], coarse bucket
    loaded_length: "long" | "mid" | "short",
    confidence: "low",          # HARD CEILING — never above "low"
    rationale: str,             # the biomechanical reasoning, explicit
    grounded_in: list[str],     # encoded modules supplying the lengthened
                                # principle, e.g. ["maeo_2023","wolf_2023"]
)
```

Deliberately **no `source: Citation`** to one paper — its provenance is a
model, and the shape should say so. `grounded_in` cites the encoded modules
that justify the lengthened-position weighting.

### Walling-off (non-negotiable)

- A separate registry index (`_MECHANISTIC_EMPHASIS`), queried **only** as a
  fallback when measured `ExerciseEmphasis` is absent for that `(muscle,
  region)`.
- `combine_emphasis_estimates()` accepts only `ExerciseEmphasis` — it is
  *structurally* impossible to pool a mechanistic prior with measured data.
- `confidence` is capped at `"low"`. When a measured source later lands, the
  mechanistic entry is removed (or retained only as a flagged cross-check).

## What this explicitly is NOT

- Not EMG-derived. EMG is excluded, including as a confirmation filter.
- Not a claim of measured magnitude. The numbers are buckets.
- Not permitted to override or pool with a longitudinal trial.
- Not a continuous stretch-dose-response — we don't have that curve.

## Consequences

**Benefits**
- Unblocks lats and deltoids: gives the optimizer a defensible, honestly-
  labelled prior where it currently has nothing.
- Fits the project's framing. The README describes an evidence-informed
  system with Bayesian updating; a mechanistic *prior* that is replaced by a
  measured *posterior* when an RCT publishes is a clean prior→posterior
  pipeline — and pedagogically on-target for the learning goal.

**Costs / risks**
- Requires a per-exercise biomechanical model (joint angles through ROM,
  resistance profile, muscle length-tension). This is a modelling sub-project,
  not a paper encoding.
- Bi-articular muscles make loaded-length genuinely subtle.
- Coarser than `COVERAGE.md` §2's head-level granularity for some muscles.
- The central risk is dressing speculation as data. Mitigated by: the hard
  `confidence` ceiling, the distinct data shape, the structural no-pooling
  rule, and `grounded_in` provenance. If those guards feel insufficient in
  review, that is an argument to reject this ADR.

## Alternatives considered

1. **Hold the line** — lats/delts stay `Gap`; optimizer has no prior there.
   Rejected: blocks the whole-body-program goal indefinitely.
2. **Admit EMG as a capped low-confidence tier.** Rejected: EMG's error is
   directional bias, anti-correlated with the lengthened signal; capping
   confidence addresses variance, not bias.
3. **Mechanistic tier (this ADR).** Chosen.

## Proposed first implementation — lats prototype

Before generalising, prototype **one muscle (latissimus dorsi)** to check the
output reads as credible:

- Add `MechanisticEmphasis` to `shared.py`.
- New module `app/priors/mechanistic/lats.py`: encode the common lat exercises
  (wide / neutral pulldown, pull-up, straight-arm pulldown, dumbbell & cable
  pullover, barbell & cable row variants) with loaded-length classification
  and rationale.
- Expected sanity pattern: pullover / straight-arm and other stretch-loaded
  work rate high; standard pulldown mid; short-range-loaded pulls lower.
- A smoke test pinning the coefficients; a registry fallback-query test.
- If the lats output does **not** read as credible to a knowledgeable reader,
  that is signal to revise or abandon the approach before encoding more.

## Open questions

1. How is per-exercise resistance-profile data sourced and encoded? (free-
   weight vs cable vs machine differ; a small reference table may be needed.)
2. Sub-region granularity — the mechanistic prior is coarser than §2's
   head-level map. Encode at whole-muscle only, or attempt regions?
3. Keep a coarse EMG *negative* check ("near-zero EMG ⇒ probably not
   involved") as a sanity floor, or exclude EMG entirely? Leaning: exclude
   entirely, to keep the rule simple and the bias fully out.
