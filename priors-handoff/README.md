# Priors Layer Bundle — Handoff to Claude Code

This bundle contains the literature priors system for the health-link
fitness app. Designed and built across three Claude Project chat sessions.
This README is written for Claude Code (or a human reading the diff) to
integrate the contents into the existing repo at
`~/Documents/Development/health-link/`.

---

## What this bundle contains

```
priors-handoff/
├── README.md                          # this file
├── app/
│   └── priors/
│       ├── __init__.py                # package marker
│       ├── shared.py                  # infrastructure (EffectEstimate, ExerciseEmphasis, pooling)
│       ├── pelland_2026.py            # volume/frequency dose-response priors
│       ├── failure_effects.py         # three-paper synthesis on training to failure
│       ├── maeo_2023.py               # triceps overhead vs neutral — emphasis coefficients
│       ├── varovic_2025.py            # regional hypertrophy meta-analysis
│       ├── wolf_2023.py               # partial vs full ROM meta-analysis
│       └── demo_combine.py            # runnable demonstration of combination logic
└── docs/
    └── priors/
        ├── QUALITY_RUBRIC.md          # v1.0 rubric for scoring papers
        ├── BACKLOG.md                 # forward-looking working file (READ FIRST)
        └── SESSION_LOG.md             # archaeology, chronological journal of decisions
```

## What this layer is

A system for encoding peer-reviewed research as structured Python priors
that the recommendation engine and optimizer will consume.

Two distinct data shapes are supported:

**`EffectEstimate`** — a quantitative finding from a paper. Mean, SE, n,
population, source, quality. Used for: "what is the effect of X on Y?"
Examples in this bundle:
- Pelland: +0.24% hypertrophy per added weekly set
- Vieira/Grgic/Robinson: failure vs non-failure SMDs
- Maeo: paired Cohen's d for overhead vs neutral arm position
- Varovic: regional hypertrophy SMDs

**`ExerciseEmphasis`** — per-(exercise, muscle, region) coefficient on [0, 1]
indicating how much stimulus an exercise provides to a target muscle.
Distinct shape because emphasis coefficients aren't on the same scale as
SMDs and shouldn't be pooled the same way. Used for exercise selection.
Examples in this bundle:
- cable_overhead_extension → triceps_brachii/long_head: 1.00 (high confidence)
- cable_pushdown → triceps_brachii/long_head: 0.69 (high confidence)

Multiple papers on the same question can be combined:
- `combine_inverse_variance` for effect estimates
- `combine_for_user` for applicability-filtered pooling
- `combine_emphasis_estimates` for quality-weighted averaging of emphasis coefficients

## Where files go in the repo

**Assumption**: the repo has `app/` and `docs/` at the root. If the
existing structure differs (e.g., `backend/` or `health_link/`), adjust
paths to match and update the relative imports as needed (currently
`from .shared import ...`, which works under any parent package).

| Source path in this bundle | Destination in repo |
|---|---|
| `app/priors/*.py` | `app/priors/*.py` (or equivalent) |
| `docs/priors/*.md` | `docs/priors/*.md` |

Also create an empty `tests/priors/` directory as a placeholder. No test
files yet — they're a follow-up task tracked in `BACKLOG.md`.

## Verification after placement

```bash
cd ~/Documents/Development/health-link

# Run the demo from the repo root
python -m app.priors.demo_combine
```

Expected: a multi-section report ending with a pooled effect of approximately
+0.16 SMD (95% CI: 0.04, 0.28) for failure training on hypertrophy.

Also verify individual modules:

```bash
python -c "
from app.priors import maeo_2023, varovic_2025, wolf_2023
for e in maeo_2023.EMPHASIS_ESTIMATES:
    region = e.region or 'whole'
    print(f'{e.exercise} → {e.muscle}/{region}: {e.emphasis:.2f}')
"
```

Expected output: six lines showing emphasis coefficients for cable
overhead extension (1.00) and cable pushdown (~0.69-0.72) across long_head,
lateral_and_medial_heads, and whole-muscle regions.

## Critical files to read first

If you're a fresh Claude Code session (or a human picking this up after
time away), read in this order:

1. **`docs/priors/BACKLOG.md`** — current state, what's encoded, what's
   queued, open questions. Forward-looking.
2. **`docs/priors/SESSION_LOG.md`** — chronological journal of decisions.
   Backward-looking, immutable.
3. **`docs/priors/QUALITY_RUBRIC.md`** — how papers get scored.
4. **`app/priors/shared.py`** — the infrastructure shapes.
5. Any individual paper module to see how a real prior is encoded.

The BACKLOG.md and SESSION_LOG.md are the persistence mechanism for this
work across chat sessions. They live in the repo (durable) and get
uploaded to Project Knowledge in the Claude Project (visible to chats).

## Updates needed to existing project docs

These updates have NOT been made in this bundle; they need to be applied
to the live repo files after review. Each is a meaningful change worth
its own commit.

### `docs/ROADMAP.md`

The existing Phase 2 ("Classical ML: Progression Suggestions") should be
reframed to include the priors layer as a foundational sub-phase. Proposed:

- **Phase 2a — Literature priors layer.** Build infrastructure (done in
  this bundle). Encode 8-12 anchor papers total. Write rubrics. Build
  registry. Estimate: 3-4 weeks of focused work, currently ~1/3 complete
  with 7 papers encoded across 5 modules.

- **Phase 2b — Feature layer + first models.** Materialized views for
  weekly muscle volume, progression slopes, recovery state. Volume
  recommender that combines priors with personal data. Estimate: 3 weeks.

Add a sentence to the phase summary explaining that progression suggestions
are now **evidence-informed** (priors + personal data via Bayesian updating)
rather than trained-from-scratch ML.

### `docs/DECISIONS.md`

Three new ADRs to add. The reasoning is captured in `SESSION_LOG.md` and
expanded here:

**ADR-007: Literature priors stored as Python modules, not database tables**
- *Problem*: How to encode research evidence (effect sizes, dose-response
  curves) so the optimizer can use them.
- *Decision*: Python modules in `app/priors/`, version-controlled with git.
- *Rationale*: Slow-changing data; logic colocated with values; type
  checking; IDE support; PR-reviewable diffs; no migrations needed.
- *Consequences*: iOS can't read priors directly — must go through API.
  New papers require code changes. The `routines` table needs
  `priors_version` (git commit hash) for reproducibility.

**ADR-008: Multi-paper synthesis via inverse-variance pooling with overlap adjustment**
- *Problem*: Multiple meta-analyses on the same question give different
  point estimates (Vieira/Grgic/Robinson on failure; Maeo/Varovic on
  regional hypertrophy).
- *Decision*: Pool via inverse-variance weighting; apply SE inflation
  (~1.35) when meta-analyses share underlying studies.
- *Rationale*: Standard meta-analytic technique; honest about
  non-independence; single estimate the optimizer can act on.
- *Consequences*: Pooling is heuristic, not full random-effects MA;
  overlap factors are judgment calls.

**ADR-009: Quality scoring via documented rubric**
- *Problem*: How to weight papers in pooling and filter low-quality evidence.
- *Decision*: `docs/priors/QUALITY_RUBRIC.md` v1.0 — seven weighted
  dimensions, per-paper scoring with reasoning in module comments.
- *Rationale*: Consistency, traceability, defensibility.
- *Consequences*: 10-20 minutes per paper to score; subjective weights
  but documented. Quality modulates pooling weight; doesn't gate inclusion.

### `CLAUDE.md`

Add a section describing the priors layer:

> ## Evidence-informed recommendation system
>
> Beyond model training, this project encodes published research as
> structured Python priors. Each meta-analysis or key paper becomes a
> module in `app/priors/` that exposes `EffectEstimate` and/or
> `ExerciseEmphasis` objects with population specs, uncertainty, and
> quality scores. Multiple papers on the same question are combined via
> inverse-variance pooling (for effect estimates) or quality-weighted
> averaging (for emphasis coefficients), with overlap adjustment for
> non-independent meta-analyses.
>
> This makes the recommendation system evidence-traceable: every program
> decision can point to specific papers backing it. New evidence is
> incorporated by adding a module, not retraining a model. Quality scores
> follow `docs/priors/QUALITY_RUBRIC.md`.

### `docs/SCHEMA.md`

Add a section clarifying that priors don't live in the database, and note
the `priors_version` column to be added to the `routines` table when
Phase 2b lands.

## Important conceptual point captured in this work

The "regional hypertrophy" literature is actually two distinct questions
that get conflated in popular discourse:

1. **"Do different exercises produce different whole-muscle (or distinct
   sub-muscle) growth?"** Maeo 2023 says YES — overhead extensions grow the
   long head substantially more than pushdowns. This is real, replicated.

2. **"Within a given training condition, does the muscle grow more at
   proximal vs distal regions?"** Varovic 2025 meta-analysis says NO —
   regional effects are trivial (SMDs 0.05-0.09, mostly null).

The optimizer should use Q1 data for exercise selection (which is what
`ExerciseEmphasis` encodes). The optimizer should NOT bake in strong
"regional preferences within a sub-muscle" based on length-of-training
theory alone — Varovic's meta-analysis shows that effect is small.

This kind of nuance is exactly why deep-mode literature reading matters.
Abstracts and popular fitness discourse routinely conflate these.

## Suggested commit structure

```
1. Add literature priors infrastructure (shared.py with both shapes, __init__.py)
2. Add Pelland 2026 priors module
3. Add failure-effects synthesis (Vieira + Grgic + Robinson)
4. Add Maeo 2023 (regional hypertrophy — exercise emphasis)
5. Add Varovic 2025 (regional hypertrophy meta-analysis)
6. Add Wolf 2023 (partial vs full ROM meta-analysis)
7. Add QUALITY_RUBRIC.md, BACKLOG.md, SESSION_LOG.md
8. Add demo_combine.py
9. Update CLAUDE.md to describe priors layer
10. Add ADRs 007, 008, 009
11. Update ROADMAP.md to split Phase 2
12. Update SCHEMA.md with "what's not in the database" section
```

Each commit message should explain why, not just what. The reasoning lives
in SESSION_LOG.md and is worth preserving in git history.

## Known follow-ups (tracked in BACKLOG.md)

1. **Build the registry layer** (`app/priors/registry.py`) — currently
   prior modules aren't wired into anything app-facing.
2. **Write unit tests** for `shared.py` (pooling math, applicability
   scoring) and a smoke test per prior module.
3. **More prior modules** — priority order in BACKLOG.md. Top candidates:
   Schoenfeld 2017 (volume), Kassiano 2023 (calf), Pedrosa 2022 (biceps),
   Maeo 2021 (hamstrings).
4. **Write `APPLICABILITY_RUBRIC.md`** documenting population-matching
   weights with the same rigor as `QUALITY_RUBRIC.md`.

## Final review checklist before committing

- [ ] Files placed in correct directory matching existing repo structure
- [ ] `python -m app.priors.demo_combine` runs successfully from repo root
- [ ] `python -c "from app.priors import maeo_2023; print(len(maeo_2023.EMPHASIS_ESTIMATES))"` returns 6
- [ ] BACKLOG.md and SESSION_LOG.md uploaded to Claude Project Knowledge
- [ ] Three new ADRs added
- [ ] CLAUDE.md updated
- [ ] ROADMAP.md updated
- [ ] SCHEMA.md updated
- [ ] `tests/priors/` directory created (empty)
- [ ] No `__pycache__` directories committed (check `.gitignore`)

End of handoff.
