# Priors Layer — Session Log

A running journal of what got done each session. Date-stamped. For
archaeology when future-you wonders when something got decided.

Separate from `BACKLOG.md`, which is forward-looking. This is backward-
looking and immutable: don't edit past entries, only append.

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
