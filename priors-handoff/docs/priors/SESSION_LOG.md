# Priors Layer — Session Log

A running journal of what got done each session. Date-stamped. For
archaeology when future-you wonders when something got decided.

Separate from `BACKLOG.md`, which is forward-looking. This is backward-
looking and immutable: don't edit past entries, only append.

---

## Session 6 — Exercise→muscle involvement map (ADR-011)

**Date:** 2026-05-18

### What got built

- Wrote and accepted **ADR-011**
  (`proposals/ADR-011-exercise-involvement-map.md`) — a new
  `ExerciseInvolvement` shape and a standalone `app/priors/exercise_involvement.py`
  module: the layer's CROSS-muscle volume-accounting map. For each exercise it
  lists every muscle trained and a `role` (primary / secondary / stabilizer);
  `role` maps to a fractional set credit (1.0 / 0.5 / 0.0) via a single
  `ROLE_SET_CREDIT` constant — Pelland 2026's direct/indirect counting.
- This is a THIRD shape, walled off from both emphasis shapes. It answers "one
  set of exercise A — how much volume to each muscle?", NOT "which exercise is
  best for muscle M" (that stays `ExerciseEmphasis` / `MechanisticEmphasis`).
  Rewrote the `ExerciseEmphasis` docstring, which had conflated the two (it
  used a set-counting example for an emphasis shape).
- Prototype: the 16 exercises already in `mechanistic/lats.py` +
  `mechanistic/deltoids.py`, scored across every muscle each trains — **74
  `(exercise, muscle)` rows**. Registry wired: `_INVOLVEMENT_INDEX` +
  `involvement_for_exercise` / `involvement_for_muscle` / `set_credit` /
  `fractional_set_count`. `set_credit()` returns `None` for an unknown pair —
  fixing the silent-`0.0` under-counting of `pelland_2026.fractional_set_count`.
- Created `.claude/agents/priors-involvement-auditor.md` — a lightweight audit
  gate for the involvement map (re-derives functional anatomy; no
  resistance-curve modelling, so lighter than the mechanistic auditor).
- Audited the module — verdict **MINOR ERRORS**: all 74 roles correct, all 3
  `pelland_2026_table1` basis citations verified, walling-off clean. Three
  rationale-wording fixes applied (pullover-pec EMG honesty; rear-delt-in-row
  hedge; teres-major row wording). Audit doc:
  `audits/exercise_involvement_audit.md`.
- Tests: 228 → 244, all passing.

### Decisions made

- **Both outcomes, one map.** `ExerciseInvolvement.outcomes` defaults to
  `("hypertrophy", "strength")`. The role is anatomy — outcome-shared — and
  Pelland applied the 0.5 fractional weight to both its hypertrophy and
  strength volume regressions, so the weight is grounded for both. `outcomes`
  is the seam left open if Pelland's strength Table 2 is ever encoded and
  shows a genuine strength-specific reclassification. (User decision.)
- **Dedicated lightweight auditor, not the standard `priors-auditor`.** Every
  encoded module to date has come back from audit with at least minor errors,
  so even an anatomy-only map gets an independent re-derivation gate. (User
  decision.)
- **Deltoid heads keyed as separate muscles** (`anterior_deltoid` etc., as
  Pelland's table does) — involvement MUST be per-head. This differs from the
  mechanistic tier's `deltoids` + `region` convention; unifying the sub-muscle
  taxonomy is deferred (BACKLOG Q4).
- **`stabilizer` rows encoded at 0.0 credit** (e.g. erectors in a bent-over
  row) — an explicit zero-credit row is honest documentation; an omitted row
  reads as an oversight.

### Open / next

- Agreed next direction (user): a rubric for the new exercise-based data type,
  then a catalogue pipeline that pulls the full exercise library from apps
  like Hevy/Strong and maps each to involvement (+ emphasis) scoring. This is
  the ADR-011 "catalogue build-out". Design not yet started — see BACKLOG.
- Audit follow-ups (BACKLOG): supraspinatus / external rotators / serratus
  anterior need muscle keys before raises/flies/pullovers can be fully scored;
  reconcile exercise-key strings with Pelland Table 1 (`barbell_row` vs
  `bent_over_barbell_row`) to claim more Pelland corroboration.
- Everything remains uncommitted.

---

## Session 5 — Pipeline run: hamstrings + rest-interval papers

**Date:** 2026-05-17

### What got built

- Ran the full 4-agent priors pipeline (seeker → relevance-checker →
  entry-maker → auditor) on a fresh seeker pass against the `COVERAGE.md`
  priority gaps.
- Seeker produced a 5-paper priority shortlist
  (`docs/priors/candidates/2026-05-17-candidates.md`) and parked 3 on-topic
  non-priority papers in `DEFERRED_CANDIDATES.md`.
- Encoded **Maeo 2021** (`maeo_2021.py`, quality 0.88) — seated vs prone leg
  curl, 10 `ExerciseEmphasis` coefficients (whole hamstrings + 4 sub-muscles).
  Closes the hamstrings exercise-selection gap. Audit verdict: **ACCURATE**.
- Encoded **Singer 2024** (`singer_2024.py`, quality 0.77) — inter-set
  rest-interval → hypertrophy Bayesian MA, 3 `EffectEstimate`s (arm / thigh /
  whole-body). New `Topic.REST_INTERVAL_HYPERTROPHY`. Audit verdict: **MINOR
  DISCREPANCIES** — fixes applied (below).
- Registry: 12→13 topics, 30→33 effect estimates, 12→22 emphasis coefficients.
  Tests: 140→173, all passing.
- Rebuilt `COVERAGE.md` §2 (exercise selection) at **sub-muscle granularity**:
  12 muscle-group rows → 23 rows across 7 body-region sub-tables, with a new
  "Heads / regions for selection" column. Added muscle groups that were absent
  from the map entirely (hip adductors, hip abductors, hip flexors, brachialis,
  tibialis anterior, serratus anterior, pec minor) and split bundled rows
  (traps/rhomboids/erectors; forearms/abdominals). Tally: 3 Covered, 1 Thin,
  19 Gap. The seeker reads §2 to decide what to hunt, so previously-unlisted
  muscles are now discoverable.

### Decisions made

- **Krause Neto 2025** (glute hypertrophy MA) was shortlisted but, after
  relevance-check, **deferred not encoded** — the MA pools only a generic
  whole-muscle RT-vs-baseline effect (SMD 0.71) with no per-exercise
  comparison, so it yields no `ExerciseEmphasis` and does not fill the glute
  exercise-selection gap. Parked in `DEFERRED_CANDIDATES.md`; glutes stay a
  Gap. (User decision.)
- **Maeo 2021 encoded emphasis-only** — it is a constituent primary study
  inside the encoded Varovic 2025 meta-analysis. A Topic-keyed `EffectEstimate`
  would double-count; emphasis data flows through the separate emphasis index
  (quality-weighted averaging), so no `_POOLABLE_OVERRIDE` is needed. Mirrors
  how Pedrosa 2023 (also a Varovic constituent) is handled.
- **Singer 2024 whole-body estimate excluded from the inverse-variance pool**
  via `poolable_estimates()` + a `_POOLABLE_OVERRIDE` — it disagrees in sign
  with arm/thigh and uses a different (whole-body FFM) measurement construct.
  Poolable set is {arm, thigh}.

### Audit findings fixed

- `singer_2024.py`: participant total corrected **184 → 185** (independent
  Table 1 sum from two full-text mirrors); the quality-comment justification
  for omitting the subgroup-as-primary ×0.85 modifier was rewritten to a
  model-agnostic rationale (the OSF preregistration could not be retrieved to
  confirm the region stratification was a priori); the `n_studies` double-count
  on a pooled arm+thigh result is now documented inline. Quality score 0.77
  unchanged.
- `maeo_2021.py`: ACCURATE — no fixes required.

### Blocked / deferred

- Chest and lats/mid-back exercise selection remain Gaps — the seeker found no
  strong longitudinal exercise-comparison trials (literature dominated by
  rubric-excluded acute EMG studies). Flagged for a dedicated follow-up search.
- 2 shortlisted priority candidates not yet processed — **Kassiano 2026**
  (quads, paywalled) and **Grgic 2018** (frequency→strength MA, paywalled) —
  remain in the 2026-05-17 shortlist for a future pipeline run.
- Everything from this session is still uncommitted.

### (continued) Big-5 exercise-selection pipeline pass

After the round above, amended the `priors-seeker` agent and ran a second
pipeline pass focused on exercise selection for the large muscle groups.

- **Amended `.claude/agents/priors-seeker.md`** — added an "Exercise-selection
  hunts" section: for selection gaps the target is a head-to-head
  exercise-vs-exercise RCT (not a meta-analysis); a "muscle-X hypertrophy MA"
  usually carries no per-exercise contrast (the Krause Neto 2025 lesson); hunt
  at sub-muscle granularity; report EMG-dominated gaps as literature-blocked
  rather than forcing weak papers in. The evidence hierarchy is now
  question-type-conditional.
- **Big-5 seeker pass**
  (`docs/priors/candidates/2026-05-17-big5-selection-candidates.md`) — found
  acceptable head-to-head evidence for 2 of 4 target muscles.
- Encoded **Plotkin 2023** (`plotkin_2023.py`, quality 0.875) — hip thrust vs
  back squat, gluteus maximus. 7 between-exercise `EffectEstimate` contrasts on
  a new non-poolable raw-cm² scale + 2 equal-1.0 emphasis entries. New
  `Topic.EXERCISE_SELECTION_HYPERTROPHY`. Closes the glutes gap. Audit verdict:
  **MATERIAL DISCREPANCIES** — fixed (below).
- Encoded **Chaves 2020** (`chaves_2020.py`, quality 0.79) — incline vs flat vs
  combination bench press, 6 pectoralis `ExerciseEmphasis` coefficients. Moves
  chest Gap → Thin. Audit verdict: **MATERIAL DISCREPANCIES** — fixed (below).
- Registry now: 14 topics, 40 effect estimates, 30 emphasis coefficients.
  Tests: 173 → 214, all passing.
- Annotated `COVERAGE.md` §2 lats and deltoids rows as **literature-blocked**
  (searched 2026-05-17 — no longitudinal exercise-comparison trial exists, only
  acute EMG) so future seeker passes don't re-grind the same literature.

Decisions:
- **Plotkin encoded as between-exercise `EffectEstimate` contrasts** (the paper
  ran no within-group stats), on a dedicated non-poolable `scale`
  (`between_exercise_csa_diff_cm2`), under a new `EXERCISE_SELECTION_HYPERTROPHY`
  Topic with a `_POOLABLE_OVERRIDE` restricting the pool to the 3 glute-max
  subregion contrasts. The glute result is a genuine equivalence (hip thrust ≈
  back squat) — encoded as both exercises at equal 1.0 emphasis, never a
  fractional winner.
- **Krause Neto 2025 deferral held** — Plotkin's true head-to-head RCT
  supersedes the deferred glute MA; the amended seeker rules would now reject
  such a generic MA at the seeker stage.

Audit findings fixed:
- `plotkin_2023.py`: the sign convention was stated backwards — the paper's
  notation is "(−) favours hip thrust, (+) favours back squat"; the module
  asserted the reverse and the error had propagated into the glute-region
  notes (the quad/adductor notes used the correct convention, so the file was
  self-contradictory). Corrected throughout; no encoded value changed.
- `chaves_2020.py`: the encoded muscle-thickness outcome rests on a 30-subject
  subsample (10/group), not the 47 (15/15/17) training-completer count the
  module stated. Sample-size quality dimension corrected (15–24 band → 10–14
  band); quality re-scored **0.80 → 0.79**. No emphasis coefficient changed.

Still open:
- Lats/mid-back and deltoid exercise selection are literature-blocked (see
  `COVERAGE.md` §2) — no longitudinal head-to-head trials exist; revisit if new
  RCTs publish.
- Quads exercise selection still a Gap — Kassiano 2026 (shortlisted) and
  Grgic 2018 (frequency→strength) remain unprocessed, both paywalled.
- Everything remains uncommitted.

### (continued) Mechanistic-prior tier — ADR-010

The literature-blocked muscles (lats, deltoids) prompted a new design: a
fallback exercise-selection prior derived from biomechanics + the layer's own
lengthened-position evidence, NOT from EMG. An earlier idea — cross-referencing
lengthened exercises with EMG — was rejected: surface EMG under-reads long
muscle lengths, so it is anti-correlated with the lengthened signal exactly
where it matters.

- Wrote `proposals/ADR-010-mechanistic-emphasis-priors.md` — **ACCEPTED**. A
  separate `MechanisticEmphasis` shape: distinct type (so it can never pool
  with measured `ExerciseEmphasis`), `confidence` hard-capped at low/
  speculative, no single-paper `source`. Derivation: involvement gate →
  loaded-length classification (long/mid/short at the resistance curve's hard
  point) → coarse emphasis bucket.
- Built the lats prototype: `MechanisticEmphasis` in `shared.py`;
  `app/priors/mechanistic/lats.py` (17 priors — 7 whole-muscle at
  `confidence=low`, 10 upper/lower regional at `confidence=speculative`);
  registry `_MECHANISTIC_INDEX` + `mechanistic_emphasis_for_muscle()` +
  `selection_emphasis()` (returns a `measured`/`mechanistic`/`none` tier tag).
- DECISION (user): the upper/lower regional entries are kept, tagged
  `speculative`. The whole-muscle tier reads credible (stretch-loaded
  isolation on top, contracted-loaded rows at the bottom); the regional split
  is acknowledged as the speculative edge and Varovic 2025 cautions against
  over-trusting it.
- Tests 214 → 223, all passing. Resolves BACKLOG open question 2.

Then, same session: built the deltoids mechanistic module and a dedicated
audit gate for the tier.

- `app/priors/mechanistic/deltoids.py` — 9 priors, 3 per head
  (anterior/lateral/posterior), all `confidence=low`: the deltoid heads are
  distinct, established functional targets, unlike the lats' contested
  upper/lower split, so they are NOT `speculative`. Registry wired; tests
  223 → 228. Mechanistic tier now 26 priors (lats 17, deltoids 9).
- Created `.claude/agents/priors-mechanistic-auditor.md` — the audit gate for
  the mechanistic tier. It has no paper to re-read; instead it independently
  re-derives each exercise's loaded muscle length from biomechanics and checks
  the classifications, buckets, `grounded_in`, confidence caps and
  walling-off.
- Audited both mechanistic modules:
  - **deltoids — MINOR REASONING GAPS** → two rationale-honesty wording fixes
    applied (the incline-press anterior rationale overstated the stretch; a
    cable entry's setup caveat made consistent). No classification changed.
  - **lats — auditor returned MATERIAL REASONING ERRORS; orchestrator
    REVIEWED and REJECTED the finding.** The auditor claimed `dumbbell_pullover`
    should be `mid` not `long` — it had conflated external resistance load
    (peaks at the stretch — longest moment arm) with muscle force-output
    capacity (which falls toward long length). `long` is correct; verified
    against biomechanics references. Lats module unchanged. The
    `priors-mechanistic-auditor` definition was hardened with a CAUTION against
    that exact conflation. See `audits/mechanistic_lats_audit.md`
    "Orchestrator review" — the audit gate is reviewed, not rubber-stamped.
- Net: lats + deltoids exercise selection now have a mechanistic fallback
  prior; both remain measured-evidence Gaps.

---

## Session 4 — Audit pass, registry, expansion, and the encoding pipeline

**Date:** 2026-05-17

### What got built

- Independently audited all 7 originally-encoded papers (5 modules) with
  fresh-read subagents — audit docs in `docs/priors/audits/`. Fixed every
  finding (see below).
- Added an `n_studies` field to `EffectEstimate` in `shared.py` (participants
  vs pooled study count) and carried it through the pooling functions.
- Built `registry.py` — the app-facing query layer. Indexes every estimate by
  `Topic`; `_POOLABLE_OVERRIDE` keeps incommensurable / non-independent
  estimates out of the inverse-variance pool. 12 topics, 30 effect estimates,
  12 emphasis coefficients.
- Built the test suite (`tests/priors/`): `test_shared.py`,
  `test_modules_smoke.py`, `test_registry.py` — 140 tests.
- Encoded 4 new papers, each independently audited: Schoenfeld/Ogborn/Krieger
  2017 (`schoenfeld_2017.py`, volume dose-response MA); Kassiano 2023
  (`kassiano_2023.py`, gastrocnemius calf-raise ROM, ExerciseEmphasis);
  Pedrosa 2023 (`pedrosa_2023.py`, elbow-flexor regional hypertrophy);
  Schoenfeld/Grgic 2017 (`schoenfeld_load_2017.py`, low- vs high-load MA).
- Wrote `COVERAGE.md` (coverage map) and `DEFERRED_CANDIDATES.md` (parking lot
  for on-topic-but-not-priority papers).
- Defined a 4-agent encoding pipeline in `.claude/agents/`: priors-seeker →
  priors-relevance-checker → priors-entry-maker → priors-auditor. Added a
  `/handoff` skill (`.claude/skills/handoff/`).

### Audit findings fixed

- `failure_effects.py`: "Robinson et al. 2022" was a mis-citation — that DOI
  belongs to **Refalo et al. 2023**. Renamed throughout. Several sample sizes
  corrected (Grgic trained subgroup 140→39, etc.).
- Quality re-scores against the rubric: Varovic 0.88→0.83, Wolf 0.84→0.81.
  Wolf's "overall" estimate was relabelled (it was the muscle-size subgroup);
  its short-length-partial estimate was added.
- `n` fields corrected to participants; `n_studies` added across the
  meta-analysis modules.

### Decisions made

- **DECISION**: a paper on a different scale, or a primary study already
  inside an encoded meta-analysis, is registered under its `Topic` but kept
  OUT of that topic's pool via `_POOLABLE_OVERRIDE`. **REASON**: naive
  inverse-variance pooling of incommensurable or non-independent estimates
  manufactures false precision. (Schoenfeld-volume vs Pelland; Pedrosa 2023
  vs Varovic; 1RM vs isometric.)
- **DECISION**: every new paper module gets an independent audit (a fresh
  re-read of the paper) before it is trusted — now a mandatory pipeline gate.
- **DECISION**: encoding shape follows the data — `EffectEstimate` when the
  paper reports effect sizes/CIs, `ExerciseEmphasis` only when per-exercise
  growth ratios exist. Do not force a shape.

### Blocked / deferred

- **Pedrosa 2022** (knee-extensor ROM) — full text paywalled; the abstract
  carries no effect-size data, so it cannot be encoded without the PDF.
- Integration into the repo proper — ADRs 007-009, the ROADMAP Phase-2 split,
  and moving the layer out of `priors-handoff/` — still pending.
- Everything from this session is uncommitted.

---

## Session 3 — Regional Hypertrophy

### What got built

- Extended `shared.py` with `ExerciseEmphasis` dataclass and
  `combine_emphasis_estimates()` function. This is the second supported
  shape alongside `EffectEstimate`. Distinct because emphasis coefficients
  are not on the same scale as effect sizes and can't be combined via
  inverse variance.

- Encoded `maeo_2023.py` — Maeo et al. on cable overhead extension vs
  cable pushdown for triceps. Quality 0.89. Includes:
  - Three whole-muscle effect estimates (TBLong, TBLat+Med, Whole-TB)
    with Cohen's d and recovered SE from the paired design
  - Six emphasis coefficients (overhead extension and pushdown each, for
    long head / lat+med / whole muscle)

- Encoded `varovic_2025.py` — Bayesian meta-analysis on regional
  hypertrophy (proximal/mid/distal). Quality 0.88. Three regional effect
  estimates, all SMD 0.05-0.09 with QIs crossing zero — trivial effects.

- Encoded `wolf_2023.py` — original Wolf meta-analysis on partial vs full
  ROM. Quality 0.84. Three effect estimates: overall (trivial),
  long-length partial (modest favoring partial, wide CI), strength.

### Critical insight surfaced

The literature treats "regional hypertrophy" as a single phenomenon, but
it's actually two questions:

- "Do exercises trained at different muscle lengths produce different
  whole-muscle growth?" → Maeo answer: YES (substantial, e.g. +28.5% vs
  +19.6% for long head with overhead vs pushdown)

- "Within a given training condition, does the muscle grow more at some
  regions (proximal/distal) than others?" → Varovic 2025 meta-analysis
  answer: NO (SMDs 0.05-0.09, QIs cross zero)

Casual fitness discourse conflates these. The first informs exercise
selection (good). The second would inform "grow my upper chest" claims
(weak evidence). Our priors infrastructure now distinguishes them: Maeo's
data lives as ExerciseEmphasis (used for selection), Varovic's lives as
EffectEstimate (used as a regional-effect prior that the optimizer should
respect as small).

### Decisions made this session

- **DECISION**: Emphasis coefficients should be combined via quality-
  weighted averaging, not inverse-variance pooling.
  **REASON**: Emphasis coefficients are derived numbers (ratios of
  observed growth), not statistical effect estimates with proper SEs.
  Inverse-variance doesn't make sense here.

- **DECISION**: Maeo's overhead extension is normalized to 1.0 emphasis
  for triceps long head and whole muscle, treating it as our "best
  available" reference exercise.
  **REASON**: Maeo provides the strongest direct longitudinal evidence
  for long-head emphasis. As we add more papers with direct comparisons,
  we'll need to renormalize if anything beats it.

- **DECISION**: Do NOT add speculative "regional preference within a sub-
  muscle" emphasis coefficients (e.g., "exercise X grows proximal long
  head more than distal long head").
  **REASON**: Varovic 2025 found no meaningful regional effect. Adding
  speculative regional coefficients would propagate noise.

### Open questions raised, not resolved

- Cross-paper emphasis normalization once we have multiple "best in
  class" exercises across multiple muscles.
- Whether to add a sub-muscle taxonomy file or let it grow organically.
- How aggressively higher-quality emphasis sources should dominate lower-
  quality ones in pooling.

### What was deferred

- Building the registry layer (still appropriate to defer; we have 5
  paper modules now but the pattern needs more variety before registry
  shape is obvious)
- Quality rubric updates (no changes needed; rubric scored fine on the
  three new papers)
- Writing ADRs for the priors layer (still appropriate to wait until
  more is built)
- Encoding Kassiano 2023 (next session)

---

## Session 2 — Multi-paper pooling on failure effects

### What got built

- Built `failure_effects.py` synthesizing Vieira 2021, Grgic 2021, and
  Robinson 2022 meta-analyses on training to failure.
- Demonstrated inverse-variance pooling with overlap adjustment.
- Wrote `QUALITY_RUBRIC.md` v1.0 with seven weighted dimensions.

### Decisions made

- Vieira's non-volume-equated SMD of 0.75 is excluded from pooling
  because it answers a different question. The volume-equated effect
  is what the optimizer needs.
- Apply ~1.35 SE inflation when pooling overlapping meta-analyses.
- Quality scores from rubric are applied per-paper at module-write time.

### Outcome

For trained males, hypertrophy: failure training has small positive
effect at fixed volume (+0.16 SMD, 95% CI: 0.04 to 0.28 after overlap
adjustment).

---

## Session 1 — Foundation

### What got built

- `shared.py` with `EffectEstimate`, `PopulationSpec`, `Citation`
- `pelland_2026.py` encoding the volume/frequency dose-response from
  Pelland et al. 2026
- `__init__.py`, `demo_combine.py`
- Initial design discussions on priors-as-code vs priors-as-DB

### Decisions made

- Priors live as Python modules, not database rows
- Effect estimates are immutable; combine via pooling functions
- Each EffectEstimate carries population, source, quality, scale, notes

### Outcome

First working prior module with sanity-checked predictions matching the
paper's reported numbers.
