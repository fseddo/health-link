# ADR-011 — Exercise→muscle involvement map (fractional-set crediting)

**Status:** ACCEPTED (2026-05-18). Reviewed — two changes from the proposal:
(1) the tier gets its own lightweight audit gate, a `priors-involvement-auditor`
agent — every encoded module so far has come back from audit with at least
minor errors, so an independent re-derivation is warranted even for a map this
simple; (2) the map covers **both hypertrophy and strength**, not hypertrophy
only. Prototype implemented alongside this acceptance — see "First
implementation" below.
**Date:** 2026-05-18 (proposed and accepted same day)
**Supersedes/addresses:** the embryonic `HYPERTROPHY_CLASSIFICATIONS` map and
`fractional_set_count()` currently embedded in `pelland_2026.py`; the
overloaded `ExerciseEmphasis` docstring (see Context). Relates to `BACKLOG.md`
open infrastructure question 4 (sub-muscle taxonomy).
**Numbering:** provisional, following ADR-010. The priors layer's ADRs 007–011
all land in the repo's `docs/DECISIONS.md` at integration.

---

## Context

The optimizer must answer two structurally different questions about an
exercise, and the layer currently blurs them.

- **Q1 — Involvement / volume crediting.** One set of a barbell row — how much
  weekly *volume* does it credit to the lats, vs the biceps, vs the rear delt?
  This is cross-muscle bookkeeping. Without it the optimizer cannot do
  per-muscle weekly volume accounting, and so cannot build a balanced
  whole-body program or avoid double-prescribing a muscle that is already
  getting indirect work.
- **Q2 — Within-muscle selection / sub-region emphasis.** Given a hypertrophy
  goal and a choice, which exercise grows muscle M (or its long head / its
  lower fibres) more? This is the `ExerciseEmphasis` (measured) /
  `MechanisticEmphasis` (derived, ADR-010) layer.

Q1 partly exists, in the wrong shape and the wrong place. `pelland_2026.py`
holds `HYPERTROPHY_CLASSIFICATIONS` — a per-muscle `direct` / `indirect`
exercise map — and `fractional_set_count()`, which applies **direct ×1.0 /
indirect ×0.5**. That ×0.5 is *Pelland 2026's own methodology* (Sec. 2.5,
"indirect ×0.5 + direct"), with strong Bayes-factor support over total-counting
and direct-only counting — so the weight is grounded, not invented. Pelland's
authors do, however, call 0.5 "a heuristic … rather than a definitive
standard" (Sec. 4.1).

Four problems with the current state:

1. **Bounded to Pelland Table 1.** The map transcribes only the exercises
   Pelland's constituent studies happened to use. Dips, pull-ups, RDLs,
   lateral raises, and most of the lat/deltoid catalogue are absent.
   `fractional_set_count()` silently returns `0.0` for any unlisted exercise —
   a real under-counting bug, flagged in the module's own comment.
2. **Wrong home.** A paper module must stay a faithful transcription of *its*
   paper (the discipline that keeps provenance honest everywhere else in the
   layer). Adding biomechanically-derived rows into `pelland_2026.py` corrupts
   that. The general map needs its own module.
3. **Binary only.** `direct` / `indirect` — no room for a documented
   zero-credit stabilising role, and no single place that owns the crediting
   weights.
4. **`ExerciseEmphasis` is overloaded.** Its docstring uses a *set-counting*
   example ("a bench press counts for ~0.5 sets toward triceps but ~1.0 toward
   chest") — i.e. it describes `ExerciseEmphasis` as doing Q1's job, when its
   actual job is Q2 (within-muscle/sub-region selection on a [0,1] scale where
   1.0 = the best exercise *for that muscle*). This conflation is precisely the
   trap to remove.

## Decision

Introduce a **separate exercise→muscle involvement map** as first-class layer
infrastructure: an `ExerciseInvolvement` data shape and a standalone module.
It answers Q1 only. `ExerciseEmphasis` / `MechanisticEmphasis` answer Q2 only.
The two never merge.

It is **universal infrastructure**, not a literature-blocked fallback — it
applies to every exercise regardless of how well its muscles are studied.
Therefore it lives at `app/priors/exercise_involvement.py`, **not** inside
`app/priors/mechanistic/` and **not** inside `pelland_2026.py`.

### The data shape

A new dataclass in `shared.py`:

```
ExerciseInvolvement(
    exercise: str,                 # canonical exercise key
    muscle: str,                   # canonical muscle key (same taxonomy the
                                   # rest of the layer uses)
    role: "primary" | "secondary" | "stabilizer",
    basis: "pelland_2026_table1" | "biomechanical",
    outcomes: tuple[str, ...],     # ("hypertrophy", "strength") — which
                                   # outcomes this row's classification holds
                                   # for; defaults to both
    rationale: str,                # why this role — anatomy / line of pull
)

# set_credit is a derived @property, NOT a stored field:
ROLE_SET_CREDIT = {"primary": 1.0, "secondary": 0.5, "stabilizer": 0.0}
```

Design points:

- **`role` is the claim; `set_credit` is a convention.** The role assignment
  (prime mover vs assistant vs stabiliser) is uncontested anatomy. The
  1.0 / 0.5 / 0.0 mapping is Pelland's heuristic. Keeping `set_credit` a
  derived property — never a hand-typed per-row number — means the heuristic
  lives in exactly one constant, and is trivially revisable if a dedicated
  fractional-counting paper is ever encoded.
- **One `ROLE_SET_CREDIT`, both outcomes.** The weights are *not* outcome-keyed.
  Pelland 2026 applied the same direct=1.0 / indirect=0.5 fractional counting
  to *both* its hypertrophy and its strength volume regressions (the strength
  slope is encoded on the `pct_per_fractional_set` scale — see
  `pelland_2026.py`), so the 0.5 weight is grounded for both. The `outcomes`
  field is what carries the hypertrophy/strength dimension instead (next
  point) — it is the *classification*, not the *weight*, that can diverge by
  outcome.
- **`outcomes` — the classification is anatomy, so it is outcome-shared by
  default.** A muscle that is a prime mover of an exercise is a prime mover
  regardless of training goal; the same is true of a synergist. So every
  biomechanically-derived row defaults to `outcomes=("hypertrophy",
  "strength")` and one row serves both. The field exists for the one case
  where outcome genuinely matters: Pelland publishes *separate* exercise
  classifications for hypertrophy (Table 1) and strength (Table 2). If Table 2
  is ever retrieved and shows an exercise classified differently for strength,
  that becomes a second row with `outcomes=("strength",)` and the
  hypertrophy row narrows to `("hypertrophy",)`. Until then, the prototype is
  outcome-shared and honestly says so.
- **`stabilizer` → 0.0 credit.** Encoding a stabilising role (erectors in a
  squat, abs bracing) at zero credit is *documentation*: it records "yes this
  muscle is engaged, and we deliberately credit it no hypertrophy volume,"
  which is more honest than an omitted row that looks like an oversight.
  Optional per exercise — omit if not informative.
- **`basis` carries provenance.** Rows lifted from Pelland Table 1 are
  `pelland_2026_table1` (transcription of an encoded, audited, quality-0.94
  paper). Rows added beyond it are `biomechanical` (derived anatomy — lower
  trust, but role assignment is still uncontested for the vast majority of
  exercises).
- **Whole-muscle granularity.** The key is `(exercise, muscle)` — no `region`.
  Sub-region targeting is Q2's job. Where a head is *already* a first-class
  muscle key in the layer's taxonomy (Pelland's map keys `anterior_deltoid`
  and `rectus_femoris` separately), involvement reuses that key as-is. It does
  **not** introduce new regional splits; fixing the inconsistent sub-muscle
  taxonomy is a separate, deferred task (`BACKLOG.md` Q4).

### How a row is derived

For a given `(exercise, muscle)`:

1. **Is the muscle involved at all?** Does the exercise load a joint action the
   muscle produces (origin/insertion, line of pull)? If not → no row.
2. **Prime mover or assistant?** Is the muscle a primary agonist of the
   exercise's main joint action, or a synergist/assistant? → `primary` /
   `secondary`. If it only contracts isometrically to stabilise → `stabilizer`.
3. **`set_credit` follows from `role`** via `ROLE_SET_CREDIT`. No per-exercise
   tuning.

This is pure anatomy. Unlike ADR-010's loaded-length classification, it needs
no resistance-curve modelling and no lengthened-position evidence — which is
why involvement can be encoded broadly and confidently while sub-region
emphasis (Q2) stays gated.

### Walling-off (non-negotiable)

- A separate registry index (`_INVOLVEMENT_INDEX`), with its own query
  (`involvement_for_exercise()` / `set_credit(exercise, muscle)`).
- `ExerciseInvolvement` is a distinct type. It is not accepted by
  `combine_emphasis_estimates()` or any pooling function — it is a categorical
  map, not an estimate, and cannot be pooled with anything.
- The crediting weights live in the single `ROLE_SET_CREDIT` constant. No row
  carries its own number.

## What this explicitly is NOT

- **Not emphasis.** It does not say which sub-region an exercise biases, and
  does not rank exercises within a muscle. "Overhead work → triceps long head"
  and "dips → lower/sternocostal pec" are Q2 claims and stay in the emphasis
  layer — which means they require a measured trial or the gated mechanistic
  tier (and the chest is `Thin`, not `literature-blocked`, so it is *not*
  currently eligible for a mechanistic dips-emphasis prior).
- **Not a measured per-exercise growth result.** It is an anatomical map with
  one literature-grounded crediting heuristic on top.
- **Not a claim that hypertrophy and strength involvement are proven
  identical.** They are *encoded* identical because biomechanics gives no
  reason to split them and Pelland's strength Table 2 is not yet retrieved.
  The `outcomes` field is the seam left open for that split.
- **Not the fix for the sub-muscle taxonomy.** It reuses existing keys, warts
  and all — including encoding the three deltoid heads as separate muscle keys
  (`anterior_deltoid` / `lateral_deltoid` / `posterior_deltoid`, as Pelland's
  table does), which differs from the mechanistic tier's `deltoids` + `region`
  convention. Involvement *must* be per-head (a bench press loads the anterior
  head and not the posterior), so the keys diverge; unifying them is deferred.

## Relationship to the existing layers

Three layers, cleanly separated:

| Layer | Question | Shape | Status |
|---|---|---|---|
| **L1 — Involvement** | Which muscles, how much volume credit? | `ExerciseInvolvement` (this ADR) | proposed |
| **L2 — Selection / emphasis** | Within a muscle, which exercise / which sub-region? | `ExerciseEmphasis` (measured) · `MechanisticEmphasis` (derived, ADR-010) | exists |
| **L3 — Dose-response** | How much growth per (fractional) set? | `EffectEstimate` — Pelland 2026 etc. | exists |

The optimizer consults them for *different* decisions, and they are **not**
naively multiplied:

- **Weekly volume accounting** uses L1: effective sets for muscle M =
  Σ over the program of `raw_sets × set_credit(exercise, M)`. That total feeds
  L3's dose-response curve.
- **"Which exercise should I add for muscle M?"** uses L2.
- **"I want long-head / lower-chest growth specifically"** uses L2 with a
  region.

The precise way the optimizer combines an L1 volume figure with an L2 emphasis
coefficient (e.g. a region-weighted effective volume) is an optimizer-design
question, out of scope for this ADR — see Open Questions.

Part of accepting this ADR is **rewriting the `ExerciseEmphasis` docstring** to
drop its set-counting example and point Q1 at `ExerciseInvolvement`.

## Consequences

**Benefits**
- Fixes the silent `0.0` under-counting bug: every exercise in the catalogue
  gets an involvement entry, so the optimizer can credit volume for any
  program.
- Unlocks per-muscle weekly volume accounting — a prerequisite for balanced
  whole-body programming and for not double-prescribing indirectly-hit
  muscles.
- Removes the Q1/Q2 conflation from `ExerciseEmphasis`; each shape now answers
  exactly one question.
- Cheap and well-grounded: role assignment is anatomy, the one heuristic
  (0.5) is already encoded and audited via Pelland 2026.
- At Phase-2 integration this map is a natural seed for the real app's
  `exercises` reference data (an `exercise_muscles` join).

**Costs / risks**
- A per-exercise anatomical map is a cataloguing effort — modest, but it grows
  with the exercise library.
- `primary` vs `secondary` is occasionally genuinely debatable (is the rear
  delt secondary or stabilising in a given row?). Mitigated: `basis` and
  `rationale` make each call inspectable; edge calls can be revisited.
- The 0.5 weight is a heuristic. Mitigated: it is isolated in one constant,
  flagged in code and here, and Pelland-grounded. A dedicated
  fractional-counting paper is a reasonable future seeker target.
- Low risk of "speculation as data" — this ADR's content is anatomy plus one
  cited heuristic, not derived effect magnitudes. The ADR-010 guard rails
  (distinct type, no pooling) still apply, but the central ADR-010 risk does
  not really arise here.

## Alternatives considered

1. **Expand `HYPERTROPHY_CLASSIFICATIONS` in place.** Rejected: corrupts
   `pelland_2026.py`'s provenance as a faithful transcription of one paper.
2. **Overload `ExerciseEmphasis` to also carry set credit.** Rejected: it is
   the exact Q1/Q2 conflation this ADR removes; and emphasis is
   *within-muscle relative* while involvement is *cross-muscle*, so they are
   not even on the same scale.
3. **Put involvement in `app/priors/mechanistic/`.** Rejected: the mechanistic
   tier is a fallback for `literature-blocked` muscles only. Involvement is
   universal and applies to every muscle.
4. **Standalone `ExerciseInvolvement` module (this ADR).** Chosen.

## First implementation — lats + deltoids prototype

Scoped to the 16 exercises already in the two mechanistic modules
(`mechanistic/lats.py` — 7; `mechanistic/deltoids.py` — 9), so the prototype
directly serves the "deepen lats/deltoids" goal that prompted it. Each
exercise is scored across **all** the muscles it meaningfully trains — 74
`(exercise, muscle)` rows. BUILT and audited 2026-05-18 — the
`priors-involvement-auditor` returned **MINOR ERRORS** (all 74 roles correct,
provenance and walling-off clean; three rationale-wording fixes applied). Audit
doc: `docs/priors/audits/exercise_involvement_audit.md`.

- Add `ExerciseInvolvement` + `ROLE_SET_CREDIT` to `shared.py`.
- New module `app/priors/exercise_involvement.py`: the rows, derived
  biomechanically. Where a row's `(exercise, muscle)` pair is an *exact* match
  for a Pelland 2026 Table 1 classification (e.g. `lat_pulldown` is listed
  indirect for `biceps_brachii` and `trapezius`; `incline_bench_press` is
  listed indirect for `triceps_brachii`), that row carries
  `basis="pelland_2026_table1"` — Pelland's audited table corroborates it.
  Every other row is `basis="biomechanical"`. (A full import of Pelland Table 1
  is deferred to the catalogue build-out — most of its keys are not lat/delt
  exercises.)
- Registry: `_INVOLVEMENT_INDEX` + `involvement_for_exercise()` /
  `involvement_for_muscle()` / `set_credit()` / `fractional_set_count()`.
  `set_credit()` returns `None` for an unknown `(exercise, muscle)` — fixing
  the silent-`0.0` under-counting of Pelland's embedded map.
- Rewrite the `ExerciseEmphasis` docstring (drop the set-counting example).
- Smoke + registry tests: every exercise in the lats/deltoid mechanistic
  modules has involvement rows; `set_credit` follows `role`; an unknown pair
  returns `None`, not a silent `0.0`.
- **Audit gate:** a new `priors-involvement-auditor` agent re-derives the
  anatomy of every row independently and checks the role calls, the `basis`
  provenance (including the Pelland Table 1 citations), and the
  `set_credit`/`ROLE_SET_CREDIT` arithmetic. Audit doc lands in
  `docs/priors/audits/`. The module is not trusted until audited.

If the prototype output does not read as anatomically correct to a
knowledgeable reader (or to the auditor), that is signal to revise before
cataloguing the full exercise library.

## Open questions

1. ~~**Audit gate.**~~ RESOLVED at acceptance — a dedicated lightweight
   `priors-involvement-auditor` agent, because every encoded module to date has
   come back from audit with at least minor errors. It re-derives the anatomy
   independently; it is not as deep as the mechanistic auditor (no
   resistance-curve modelling to re-run) but it is a real gate.
2. **Optimizer composition.** How exactly does a region-level emphasis (L2)
   weight an L1 volume figure? Decide when the optimizer is built.
3. ~~**`stabilizer` rows — encode or omit?**~~ RESOLVED — encode them at 0.0
   credit. An explicit zero-credit row ("erectors brace the bent-over row but
   bank no hypertrophy volume") is honest documentation; an omitted row reads
   as an oversight.
4. ~~**Strength crediting.**~~ RESOLVED at acceptance — the map covers both
   outcomes via the `outcomes` field; see the "What this is NOT" and Decision
   sections. Retrieving Pelland Table 2 to check for a genuine strength-only
   reclassification remains a follow-up (a `BACKLOG.md` item), not a blocker.
5. **A second source for the 0.5 weight.** Worth a seeker pass for a dedicated
   fractional-/effective-set paper, to move the weight off a single source.
