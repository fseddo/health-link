# ADR-012 — Exercise catalogue: the per-(exercise, muscle) trust rubric and the catalogue pipeline

**Status:** PROPOSED (2026-05-18). Awaiting review. No code written yet — this
document is the design gate, mirroring ADR-010 and ADR-011.
**Revised 2026-05-18** (review feedback, pre-acceptance): the trust score is
per-`(exercise, muscle)`, not per-exercise (§2); added §3 — mechanistic
emphasis fills exercises that have no trial, broadening ADR-010's scope from
literature-blocked *muscles* to untrialled *exercises*.
**Date:** 2026-05-18
**Builds on:** ADR-011 (the `ExerciseInvolvement` map). The involvement
prototype is 16 exercises; this ADR is the agreed catalogue build-out.
**Amends:** ADR-010 — see §3.
**Numbering:** provisional, following ADR-011.

---

## Context

ADR-011 built the exercise→muscle involvement map and validated the shape on a
16-exercise prototype. To be a real workout tracker, health-link needs a full
exercise library — and for the optimizer to use that library, every exercise
needs involvement scoring (both outcomes) and emphasis scoring where evidence
exists.

Two needs, set by the project owner (2026-05-18):

1. **A way to grade an exercise entry.** `QUALITY_RUBRIC.md` scores research
   *papers* (7 weighted dimensions → a `quality_score`). It does not transfer:
   an exercise entry is anatomy plus one heuristic, with no paper behind it.
   The catalogue needs its own rubric — a **per-`(exercise, muscle)` trust
   score**.
2. **A way to populate the catalogue at scale.** Hand-encoding 16 exercises
   was fine for a prototype; a full library needs a repeatable pipeline that
   pulls a canonical exercise list and maps each exercise to our scoring.

This ADR decides the catalogue's shape, the trust rubric, the data source, and
the pipeline.

## Decision

### 1. The exercise catalogue

A registry of **canonical exercise entries**. Each entry is metadata only —
the scoring lives in the existing indexes (`_INVOLVEMENT_INDEX`,
`_EMPHASIS_INDEX`, `_MECHANISTIC_INDEX`), keyed by the exercise's canonical
key. An entry carries:

- `key` — the canonical exercise key (the string already used as
  `ExerciseInvolvement.exercise`, `ExerciseEmphasis.exercise`, etc.).
- `display_name` — human-readable.
- `aliases` — names from Hevy / Strong / source datasets that map to this key
  (so the iOS app's exercises resolve cleanly later).
- `movement_pattern` — e.g. `horizontal_press`, `vertical_pull`,
  `hip_hinge`. The unit the build is staged in.

At Phase-2 integration this catalogue is the natural seed for the repo's
`exercises` reference table (CLAUDE.md) — the fields above are its columns.

### 2. The per-`(exercise, muscle)` trust score

A **computed** 0–1 score — never hand-assigned — analogous to a paper's
`quality_score`, but graded per `(exercise, muscle)` pair, not per exercise.
The evidence genuinely varies by muscle: dips→chest may one day have a measured
trial while dips→triceps has only anatomy, so one flat per-exercise number
would blur exactly the distinction the optimizer needs. The score tells the
optimizer how much to trust what the layer knows about *training that muscle
with that exercise*. The full rubric lands as
`docs/priors/EXERCISE_TRUST_RUBRIC.md` at build time; this ADR fixes its
purpose and proposed dimensions:

- **Involvement coverage** — is this `(exercise, muscle)` involvement row
  encoded and passed by the `priors-involvement-auditor`? (audited > encoded
  but unaudited > absent). Anatomy is intrinsically high-trust, so this
  dimension grades *audit status*, not "is the anatomy right".
- **Emphasis evidence tier** — the emphasis tier for this `(exercise, muscle)`:
  measured `ExerciseEmphasis` (a longitudinal trial) > `MechanisticEmphasis`
  (derived, see §3) > none. The dimension that most separates a well-evidenced
  pairing from a bare one — and, being per-`(exercise, muscle)`, it needs no
  rollup.
- **Definition quality** — is the exercise a clean, distinct, canonically
  keyed movement, or an ambiguous variant / near-duplicate? (Per-exercise — the
  same for every muscle of a given exercise.)

The score is a weighted rollup, computed by a registry function from the
encoded data — so, like `set_credit`, the rule lives in one place and updates
automatically as evidence is added. Weights and per-dimension scoring are set
in the rubric doc.

### 3. Emphasis for exercises with no trial (broadens ADR-010)

Most catalogue exercises will have no published trial — even within a
well-studied muscle. The chest has Chaves 2020, but only for three bench-press
variants; dips, decline press, cable crossover and the rest have none. So the
catalogue's emphasis layer is two-tier:

- **measured `ExerciseEmphasis`** — used wherever a longitudinal trial exists.
- **`MechanisticEmphasis`** (ADR-010) — the derived fallback, used for every
  other `(exercise, muscle, region)`.

This **broadens ADR-010's scope**. ADR-010 built the mechanistic tier only for
*literature-blocked muscles* (lats, deltoids — muscles with no trial at all).
The catalogue makes the real unit of the gap the *exercise*, not the muscle: a
mechanistic prior fills any `(exercise, muscle, region)` that lacks a measured
one, and a measured source for that exact tuple always supersedes it. Tier
resolution therefore becomes **per-exercise within a muscle** — a muscle's
ranking can hold measured-tier and mechanistic-tier exercises side by side,
each tagged; they are compared by tier, never pooled (the ADR-010 guarantee
holds).

Three hard rules carry over from ADR-010, unchanged:

- **Derived, not sourced.** A mechanistic emphasis is reasoned from
  biomechanics (loaded muscle length at the resistance curve's hard point) plus
  the layer's own encoded lengthened-position evidence. It is **not** scraped
  from EMG studies or app/website muscle ratings. EMG is excluded by design —
  its error is *directional bias* (it under-reads long muscle lengths), and
  tagging an entry `speculative` caps *variance*, not *bias*: a speculative tag
  does not launder biased data.
- **Confidence hard-capped** at `low` / `speculative` — never `medium`/`high`.
  `speculative` is for genuinely contested calls, `low` for sound ones.
- **A distinct type** — `MechanisticEmphasis` structurally cannot pool with
  measured `ExerciseEmphasis`.

So: yes, an untrialled exercise gets an emphasis layer — a derived,
honestly-capped one, gated by the `priors-mechanistic-auditor` exactly as the
lats/deltoid modules are.

### 4. Data source

Spine: an **openly-licensed** exercise dataset — `free-exercise-db` (~870
exercises, public domain) — used for *coverage and naming*, never for its
muscle taggings (we generate our own involvement + emphasis). Then
**reconcile names to Hevy / Strong conventions** via the `aliases` field, so
the eventual iOS client maps onto the catalogue without a translation layer.
We do not scrape proprietary libraries; we use their *naming conventions*,
which are not copyrightable, as alias targets.

### 5. The catalogue pipeline

A **new, parallel mini-pipeline** — the literature pipeline
(`priors-seeker → relevance-checker → entry-maker → auditor`) is NOT touched.
Pulling movement lists from a dataset is a different job from scouting
research papers; folding it into `priors-seeker` would muddy a clean,
working pipeline.

```
catalogue-seeker  →  catalogue-encoder  →  priors-involvement-auditor
                                        →  priors-mechanistic-auditor
```

- **`catalogue-seeker`** (new agent) — for a target `movement_pattern`: pull
  the candidate exercises from the source dataset, propose canonical keys,
  display names and Hevy/Strong aliases, and **dedupe** (flag near-duplicates
  — incline barbell vs incline dumbbell vs incline machine press — for a keep/
  merge decision). Output: a candidates doc.
- **`catalogue-encoder`** (new agent) — for each accepted exercise: encode its
  `ExerciseInvolvement` rows (both outcomes, ADR-011); link measured
  `ExerciseEmphasis` where a trial covers a `(muscle, region)`; and **derive
  `MechanisticEmphasis`** (§3) for the `(muscle, region)` tuples with no
  measured source.
- **`priors-involvement-auditor`** (exists) — audits the involvement rows.
- **`priors-mechanistic-auditor`** (exists) — audits the derived emphasis.
  Both audits are mandatory before the trust score is computed.

The trust score is computed after audit. Catalogue dedupe is handled in the
pipeline (the seeker), NOT as a rubric — the rubric grades trust, not
admission.

### 6. Staged by movement pattern

The catalogue is built **one movement pattern at a time**, end to end
(seeker → encoder → auditor → trust scores), ~15–30 exercises per batch. This
validates the pipeline and the rubric on a real batch before scaling, and
keeps each audit tractable.

## What this explicitly is NOT

- **Not a re-use of the paper `quality_score`.** The trust score is a distinct,
  computed number for a distinct kind of entry.
- **Not measured data.** A high trust score means the layer's *characterisation*
  of an `(exercise, muscle)` pairing is well-grounded and audited — not that the
  exercise's effect on the muscle is measured. Emphasis tier is one input,
  honestly weighted.
- **Not scraped emphasis.** Emphasis for untrialled exercises is *derived*
  (§3) — never sourced from EMG or app muscle-ratings. `speculative` caps
  uncertainty, not bias; it cannot launder biased data.
- **Not a change to the literature pipeline.** New agents, separate flow.
- **Not a scrape of Hevy/Strong.** Open-licensed spine; their names are alias
  targets only.

## Consequences

**Benefits**
- Gives the optimizer a full exercise library with a confidence signal per
  exercise — it can prefer well-characterised exercises and flag thin ones.
- A repeatable pipeline replaces hand-encoding; the audit gate still holds.
- The catalogue is integration-ready: it seeds the `exercises` table and the
  alias list bridges the iOS client.

**Costs / risks**
- A full ~870-exercise catalogue is a large encoding + audit effort — the
  movement-pattern staging is the mitigation.
- The muscle taxonomy must grow new keys (`supraspinatus`, `serratus_anterior`,
  external rotators, quad heads…) and the deltoid-head key inconsistency
  (ADR-011) should be resolved before a big catalogue bakes it in.
- The trust score risks looking more authoritative than it is. Mitigated: it
  is computed and transparent, the rubric doc is explicit, and "emphasis tier"
  honestly down-weights bare exercises.

## Alternatives considered

1. **Re-use `QUALITY_RUBRIC.md`.** Rejected — it scores papers; an exercise has
   no paper.
2. **Extend `priors-seeker` to also pull exercises.** Rejected — different job,
   would muddy the literature pipeline.
3. **Scrape Hevy/Strong directly.** Rejected — ToS/IP risk; an open dataset
   plus alias reconciliation gets the same coverage cleanly.
4. **Catalogue all ~870 exercises in one pass.** Rejected — no early validation
   checkpoint, an unmanageable single audit.

## First implementation

- Write `docs/priors/EXERCISE_TRUST_RUBRIC.md` (dimensions above; fix weights
  and per-dimension scoring).
- Add the catalogue entry shape to `shared.py` and a `trust_score()` +
  catalogue index to `registry.py`.
- Create the `catalogue-seeker` and `catalogue-encoder` agents.
- Run the pipeline on **one movement pattern** end to end. Proposed first
  pattern: **horizontal press** (bench-press family) — well-defined, and it
  spans every tier of the trust rubric in one batch: incline/flat/combination
  bench press carry measured emphasis (Chaves 2020), while decline press,
  dumbbell/machine presses and dips need derived `MechanisticEmphasis` (§3).
  Open to a different first pattern.

## Open questions

1. **Trust score: single, or per-outcome?** Per-`(exercise, muscle)` resolves
   the per-muscle variation (§2); the hypertrophy/strength split is separate.
   Involvement covers both outcomes; emphasis evidence is mostly
   hypertrophy-only. A single score per `(exercise, muscle)` is simpler; a
   `× outcome` split is more honest about the strength side's thinner
   evidence. Leaning single for v1, revisit.
2. ~~**Emphasis tier rollup.**~~ RESOLVED — the trust score is
   per-`(exercise, muscle)` (§2), so the emphasis tier is read directly for
   that pair; no rollup across an exercise's muscles is needed.
3. **Catalogue entry: dataclass or dict?** A lightweight dataclass is likely
   cleanest; decide at build.
4. **Movement-pattern taxonomy.** Needs a small canonical list
   (`horizontal_press`, `vertical_pull`, `hip_hinge`, …) — write it as the
   first build step.
5. **Mechanistic emphasis at catalogue scale.** ADR-010's mechanistic
   derivation was done by hand for 26 priors. Deriving it for hundreds of
   untrialled exercises is a real effort — the movement-pattern staging and
   the `priors-mechanistic-auditor` gate both still apply, but the
   `catalogue-encoder`'s mechanistic step is the heaviest part of each batch.
