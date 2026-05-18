# Priors Layer — Backlog

The forward-looking working file for the literature priors system. Read this
first when starting a new session.

**Current state** (2026-05-18 — see `SESSION_LOG.md` Session 6):

15 papers across 13 modules, every one independently audited (audit docs in
`docs/priors/audits/`). `registry.py` is the app-facing query layer — 14
topics, 40 effect estimates, 30 emphasis coefficients. A separate mechanistic
fallback tier (ADR-010) adds 26 biomechanics-derived priors for the
literature-blocked latissimus dorsi (17) and deltoids (9), each independently
audited by the `priors-mechanistic-auditor`. A THIRD shape — `ExerciseInvolvement`
(ADR-011, `app/priors/exercise_involvement.py`) — is the cross-muscle
volume-accounting map: 74 `(exercise, muscle)` rows for the 16 lat/deltoid
exercises, role → fractional set credit, audited by the new
`priors-involvement-auditor`. 244 tests in `tests/priors/`. Everything is
uncommitted; the layer is not yet integrated into the repo proper (still
`app/`-structured under `priors-handoff/`).

`COVERAGE.md` is the authoritative map of what is covered and what the gaps
are — read it for what to encode next. New papers are added via the 4-agent
pipeline (`.claude/agents/priors-*.md`): seeker → relevance-checker →
entry-maker → auditor, with an independent audit as a mandatory gate.

NOTE: the "papers to encode next" tiers further down are now largely stale —
trust `COVERAGE.md` §3 (priority gaps) over them. Current priority is
exercise-selection evidence for the remaining big muscle groups; lats and
deltoids are now covered by the mechanistic fallback tier (ADR-010).

## Encoded papers (with module file and quality score)

| Paper | Module | Quality | Notes |
|---|---|---|---|
| Pelland et al. 2026 | `pelland_2026.py` | 0.94 | Volume + frequency dose-response. |
| Vieira et al. 2021 | `failure_effects.py` | 0.51-0.74 | Failure vs non-failure. |
| Grgic et al. 2021 | `failure_effects.py` | 0.69-0.81 | Failure vs non-failure replication. |
| Refalo et al. 2023 | `failure_effects.py` | 0.87 | Proximity-to-failure (was mis-cited "Robinson 2022"). |
| Maeo et al. 2023 | `maeo_2023.py` | 0.89 | Triceps overhead vs neutral. ExerciseEmphasis. |
| Varovic et al. 2025 | `varovic_2025.py` | 0.83 | Regional hypertrophy meta-analysis. |
| Wolf et al. 2023 | `wolf_2023.py` | 0.81 | Partial vs full ROM meta-analysis. |
| Schoenfeld/Ogborn/Krieger 2017 | `schoenfeld_2017.py` | 0.75 | Volume dose-response MA. |
| Kassiano et al. 2023 | `kassiano_2023.py` | 0.78 | Gastrocnemius calf-raise ROM. ExerciseEmphasis. |
| Pedrosa et al. 2023 | `pedrosa_2023.py` | 0.83 | Elbow-flexor regional hypertrophy. |
| Schoenfeld/Grgic 2017 | `schoenfeld_load_2017.py` | 0.77 | Low- vs high-load MA. |
| Maeo et al. 2021 | `maeo_2021.py` | 0.88 | Hamstrings: seated vs prone leg curl. ExerciseEmphasis. |
| Singer et al. 2024 | `singer_2024.py` | 0.77 | Inter-set rest interval → hypertrophy MA. |
| Plotkin et al. 2023 | `plotkin_2023.py` | 0.875 | Hip thrust vs back squat, gluteus maximus. New `EXERCISE_SELECTION_HYPERTROPHY` topic. |
| Chaves et al. 2020 | `chaves_2020.py` | 0.79 | Incline vs flat bench press, pectoralis major. ExerciseEmphasis. |

## Infrastructure — the data shapes in `shared.py`

- `EffectEstimate` — scalar quantitative findings; pooled via inverse variance.
- `ExerciseEmphasis` — per-(exercise, muscle, region) emphasis coefficients
  from MEASURED longitudinal data; combined via `combine_emphasis_estimates()`
  (quality-weighted averaging, NOT inverse variance — different scale from SMDs).
- `MechanisticEmphasis` (ADR-010) — DERIVED biomechanics-based fallback priors
  for `literature-blocked` muscles; a distinct type that structurally cannot
  pool with measured emphasis. Lives in `app/priors/mechanistic/`.
- `ExerciseInvolvement` (ADR-011) — the CROSS-muscle volume-accounting map: per
  `(exercise, muscle)`, a `role` (primary/secondary/stabilizer) → a fractional
  set credit via `ROLE_SET_CREDIT` (1.0/0.5/0.0, Pelland 2026's direct/indirect
  counting). Distinct from both emphasis shapes — it answers "how much volume
  to each muscle", not "which exercise is best for a muscle". Lives in
  `app/priors/exercise_involvement.py`.

## Exercise-catalogue build-out — ADR-012 (PROPOSED)

The involvement map is a 16-exercise prototype. Scaling it to a full exercise
library is specified in **`proposals/ADR-012-exercise-catalogue-and-trust-rubric.md`**
(PROPOSED, 2026-05-18 — awaiting review). It decides: a canonical exercise
catalogue; a computed **per-exercise trust score** (rubric →
`EXERCISE_TRUST_RUBRIC.md`); the `free-exercise-db` open dataset as spine with
Hevy/Strong name reconciliation; a new `catalogue-seeker → involvement-encoder
→ priors-involvement-auditor` pipeline (the literature pipeline untouched);
staged one movement pattern at a time. Build starts once ADR-012 is accepted.

Audit follow-ups from `exercise_involvement_audit.md` (all MINOR, folded into
the ADR-012 build-out):
- Add muscle keys for `supraspinatus` / external rotators / `serratus_anterior`
  so raises, flies and pullovers can be fully scored (consider a `stabilizer`
  serratus row on the pullover as honest documentation).
- Reconcile exercise-key strings with Pelland Table 1 (`barbell_row` vs
  `bent_over_barbell_row`, `overhead_press` vs `shoulder_press`) so legitimate
  Pelland corroboration can be claimed via `basis="pelland_2026_table1"`.
- Unify the deltoid sub-muscle taxonomy: involvement keys the heads as
  `anterior_deltoid` etc.; the mechanistic tier uses `deltoids` + `region`.

## Important conceptual clarifications surfaced during data sourcing

These should land in ADRs eventually but live here in the meantime:

1. **"Regional hypertrophy" is two questions, not one.**
   - Q1: Do exercises that train at longer muscle lengths grow the muscle more
     overall? Maeo says YES. This is exercise-level emphasis data.
   - Q2: Within a given training condition, does the muscle grow more at
     proximal vs distal sites? Varovic 2025 meta-analysis says NO (SMDs 0.05-0.09).
   - Don't conflate these. The optimizer should use Q1 data for exercise
     selection. Don't bake Q2 assumptions into prior coefficients.

2. **Maeo 2023 IS a regional-hypertrophy paper in the Q1 sense** —
   it shows overhead extensions grow the long head 28.5% vs 19.6% for pushdowns,
   and the long head is a distinct sub-muscle worth tracking. The optimizer
   needs to choose between exercises that differentially target sub-muscles
   like the long head.

3. **Abstracts often mislead in this literature.** Examples:
   - Vieira 2021 abstract says +0.75 SMD for failure on hypertrophy, but
     this was non-volume-equated; the volume-equated effect is null.
   - Maeo's findings get cited as "lengthened position = much more growth"
     but the meta-analysis (Varovic) shows the regional effect is trivial.
   - Wolf 2023's "lengthened partials may be better" sub-finding has a CI
     from -0.81 to +0.16, much wider than the headline suggests.
   - Deep mode (reading methods, not just abstracts) is consistently
     required to encode these correctly.

## Backlog: papers to encode next (priority order)

### Tier 1 — current priority (exercise selection)

The earlier Tier-1 papers (Schoenfeld/Ogborn/Krieger 2017 volume, Kassiano
2023, Schoenfeld/Grgic 2017 load) are all DONE — see the encoded-papers table.
Current priorities, ranked per `COVERAGE.md` §3:

- **Quads exercise selection** — Kassiano 2026 (back squat vs leg extension)
  and Grgic 2018 (frequency→strength) are shortlisted but BLOCKED on paywalls;
  Pedrosa 2022 (knee-extensor ROM) likewise blocked. Need full-text access.
- **Chest sub-region selection** — Chaves 2020 covers incline-vs-flat; decline
  press and adduction-biased "inner chest" work are unaddressed.
- **Smaller muscle groups** — traps, erectors, forearms, abs, brachialis, hip
  adductors/abductors, soleus, tibialis anterior, serratus (see COVERAGE §2).
- **Strengthen the THIN dose topics** — volume→strength, frequency, and load
  each rest on a single source.

### Tier 2 — useful

- **Schoenfeld, Grgic, Krieger 2019** — frequency MA. Provides a second
  source for combining with Pelland's frequency finding.

- **Currier et al. 2023** — newer network meta-analysis combining strength
  and hypertrophy. Useful for cross-validation.

- **Maeo 2024 or later updates** — Maeo's lab has continued this line of
  work. Check for newer publications on quads, deltoids, or other muscles.

### Tier 3 — specialized

- **Sleep & resistance training performance** — Dattilo et al., Bonnar et al.
  Needed for readiness-adjustment model.

- **RPE/RIR calibration** — Zourdos et al., Helms et al. on RIR accuracy
  across the rep range. Needed for progression model to interpret user-
  reported RPE correctly.

- **Protein intake and hypertrophy** — Morton et al. dose-response.
  Needed for nutrition-modifier component of the system.

- **Older adult resistance training response** — relevant if app ever
  serves users >50. Skip until needed.

- **Sex differences in resistance training** — emerging literature. Worth
  having a source for the applicability function to weight against when
  serving female users.

### Considered and explicitly deferred

- **Pelland frequency sub-analyses** — already captured at the marginal
  level in `pelland_2026.py`. Don't need deeper extraction unless we're
  modeling weekly frequency decisions specifically.

- **EMG activation studies for exercise selection** — tempting but
  hypertrophy-from-EMG is unreliable. Use longitudinal hypertrophy data
  (Maeo, Kassiano) instead of EMG when both exist.

- **Bret Contreras hip thrust / glute work** — interesting but the
  Plotkin 2023 hip thrust vs back squat paper found similar gluteus
  hypertrophy, so the specialized glute literature isn't urgently needed.

## Open infrastructure questions

1. **How does the optimizer choose between emphasis sources of different
   quality?** Currently `combine_emphasis_estimates` uses quality-weighted
   averaging. Is this right, or should higher-quality estimates dominate
   more aggressively? Decide when we have 3+ overlapping emphasis sources
   for the same exercise.

2. **Should there be a "stretch-mediated hypertrophy" boost coefficient in
   exercise emphasis?** Currently emphasis coefficients are derived from
   direct longitudinal hypertrophy data only. Some exercises (deep romanian
   deadlifts, lengthened position cable flies) lack direct hypertrophy
   data but theoretical reasoning predicts emphasis. Resist adding
   speculation; wait for direct data.
   **UPDATE 2026-05-17:** RESOLVED — ADR-010
   (`proposals/ADR-010-mechanistic-emphasis-priors.md`, ACCEPTED) added a
   separate, hard-confidence-capped `MechanisticEmphasis` tier (biomechanics +
   the encoded lengthened-position evidence; NOT EMG) as a fallback prior for
   `literature-blocked` muscles. The lats prototype is built
   (`app/priors/mechanistic/lats.py`, 17 priors, regional entries kept
   `speculative`); deltoids are the next candidate muscle.

3. **Cross-paper emphasis normalization.** Maeo's overhead extension is
   normalized to 1.0. When we add Kassiano's lengthened calf raise (also a
   "best in class" exercise for its muscle), we'll have two 1.0s for
   different muscles. Is that OK? Probably yes — emphasis is *within-muscle*
   relative, not across muscles. Document this when the registry is built.

4. **Sub-muscle taxonomy.** Currently we use "long_head",
   "lateral_and_medial_heads", etc. Will need a canonical sub-muscle
   taxonomy file that the exercise modules reference. Defer until
   we have data on more muscle groups (after Maeo 2021 hamstrings,
   Kassiano gastrocnemius are encoded).

## Things to write at some point but not blocking

- `APPLICABILITY_RUBRIC.md` (docs the population-matching weights)
- `docs/priors/README.md` (developer guide for adding new papers)
- ADRs 007-009 (priors as code; pooling method; quality rubric) — to write
  into the repo's `docs/DECISIONS.md` at integration. ADR-010 (mechanistic
  tier) is already written under `proposals/`.
- ~~Unit tests in `tests/priors/`~~ — DONE (228 tests).
- ~~Registry layer (`registry.py`)~~ — DONE.

## How to use this file

When opening a new session:
1. Read this BACKLOG.md first
2. Read SESSION_LOG.md for recent decisions
3. Confirm latest state matches assumption before adding new content

When closing a session:
1. Update the "Encoded papers" table with anything new
2. Move items off the "Backlog" section that were completed
3. Add notes to "Open infrastructure questions" if any surfaced
4. Update SESSION_LOG.md with what was done
