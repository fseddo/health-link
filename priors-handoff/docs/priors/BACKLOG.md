# Priors Layer — Backlog

The forward-looking working file for the literature priors system. Read this
first when starting a new session.

**Current state** (2026-05-17 — see `SESSION_LOG.md` Session 4):

11 papers across 9 modules, every one independently audited (audit docs in
`docs/priors/audits/`). `registry.py` is the app-facing query layer — 12
topics, 30 effect estimates, 12 emphasis coefficients. 140 tests in
`tests/priors/`. Everything is uncommitted; the layer is not yet integrated
into the repo proper (still `app/`-structured under `priors-handoff/`).

`COVERAGE.md` is the authoritative map of what is covered and what the gaps
are — read it for what to encode next. New papers are added via the 4-agent
pipeline (`.claude/agents/priors-*.md`): seeker → relevance-checker →
entry-maker → auditor, with an independent audit as a mandatory gate.

NOTE: the "papers to encode next" tiers further down are partly stale —
Tier-1 (Schoenfeld 2017 volume, Kassiano 2023, Pedrosa 2023, Schoenfeld 2017
rep-range/load) is largely done; Pedrosa 2022 is blocked (paywall). Trust
`COVERAGE.md` over those tiers.

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

## Infrastructure additions in last session

Extended `shared.py` with:
- `ExerciseEmphasis` dataclass — per-(exercise, muscle, region) emphasis
  coefficients, distinct from scalar `EffectEstimate`
- `combine_emphasis_estimates()` — quality-weighted averaging (NOT inverse
  variance) for emphasis values

These exist because emphasis coefficients aren't on the same scale as SMDs
and shouldn't be combined the same way.

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

### Tier 1 — strongly needed

- **Schoenfeld, Ogborn, Krieger 2017** — the classic volume dose-response MA.
  Will combine with Pelland 2026 to demonstrate overlap-adjusted pooling on
  volume. Expected to confirm directionally; estimate similar magnitudes.

- **Kassiano 2023 calf raise study** — already cited in the
  regional-hypertrophy infrastructure work. Direct evidence for lengthened
  partials specifically in gastrocnemius. Encode as: ExerciseEmphasis for
  lengthened-partial calf raise vs full ROM vs shortened-partial.

- **Pedrosa et al. 2022** on partial ROM in elbow flexors — analogous to
  Kassiano but for biceps. Cited in Wolf and Varovic.

- **Schoenfeld 2017 (rep range MA)** — load and rep-range effects on
  hypertrophy vs strength. Needed before progression model can recommend
  rep ranges based on goal.

### Tier 2 — useful

- **Schoenfeld, Grgic, Krieger 2019** — frequency MA. Provides a second
  source for combining with Pelland's frequency finding.

- **Currier et al. 2023** — newer network meta-analysis combining strength
  and hypertrophy. Useful for cross-validation.

- **Maeo 2021 (hamstrings)** — same lab as Maeo 2023, same design but on
  hamstrings. Direct emphasis-coefficient extraction for seated vs lying
  leg curl. Extends triceps pattern to a second muscle group, validating
  the infrastructure works generally.

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
- Three new ADRs (priors as code; pooling method; quality rubric)
- Unit tests in `tests/priors/`
- Registry layer (`registry.py`)

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
