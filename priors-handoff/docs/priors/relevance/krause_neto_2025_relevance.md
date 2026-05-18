# Relevance assessment — Krause Neto et al. 2025 (gluteus maximus hypertrophy)

**Candidate paper:** Krause Neto W, Vieira TLK, Gama EF. "The impact of
resistance training on gluteus maximus hypertrophy: a systematic review and
meta-analysis." *Frontiers in Physiology*, 2025, 16:1542334.
DOI: 10.3389/fphys.2025.1542334 · PMID: 40276368

**Date assessed:** 2026-05-17
**Checker:** priors-relevance-checker

---

## In scope? — PARTIAL

The paper is a resistance-training intervention meta-analysis on a major,
currently-uncovered muscle group (gluteus maximus), so it sits squarely in the
core paper type for the priors layer. Against the four research goals:

- **Exercise selection (goal 1):** This is why the seeker queued it, and it is
  the goal the paper most wants to serve — but it does so only *narratively*.
  See "Data shape" below: the meta-analysis pools no per-exercise effect and
  runs no head-to-head exercise comparison, so it cannot produce
  `ExerciseEmphasis` coefficients.
- **Form / execution (goal 2):** The paper discusses ROM (full vs parallel vs
  90° squat; full vs partial hip thrust) but again only narratively, citing
  individual primary studies. No pooled ROM effect for the glutes.
- **Dose & paths (goal 3):** Not its subject. No volume/frequency/load/failure
  dose-response.
- **Coverage (goal 4):** This is the paper's real value. Glutes are a `Gap` in
  COVERAGE.md sections 1 and 2. The paper supplies the first encodable glute
  evidence — but as a dose/effect estimate, not as exercise selection.

PARTIAL rather than YES because the *reason it was queued* (closing the glute
exercise-selection gap) is not deliverable from this paper's data. What is
encodable is a different, narrower thing than the queue rationale implies.

## Data shape — EffectEstimate only (one whole-muscle RT-vs-baseline effect);
## NOT ExerciseEmphasis

The meta-analysis (11 studies in the quantitative synthesis, 12 in the review;
~318 participants) pools **pre-post change in gluteus maximus size against
baseline**, expressed as a standardized mean difference:

- Overall: **SMD 0.71, 95% CI [0.50, 0.91]**, I² = 22%, p < 0.00001.
- Subgroups by assessment: volume 0.95 [0.33, 1.57]; CSA 0.93 [0.43, 1.43];
  thickness 0.61 [0.38, 0.84].
- Subgroups by protocol: single-exercise 0.74 [0.36, 1.13]; combined 0.68
  [0.44, 0.92].
- Subgroups by status: untrained 0.74 [0.47, 1.01]; trained 0.64 [0.30, 0.98].

These are clean `EffectEstimate`-shape findings — mean SMD with a recoverable
SE from the 95% CI. The overall 0.71 estimate is the encodable core.

**It is NOT `ExerciseEmphasis` data.** Confirmed against the methods/results:
the review did **not** compute per-exercise pooled effects (no pooled hip-thrust
SMD, no pooled squat SMD) and ran **no head-to-head between-exercise contrast**.
The "single vs combined" subgroup is a protocol *structure* split, not an
exercise comparison. The exercise-selection conclusions — "prioritise the
barbell hip thrust when emphasising GMax at the expense of other muscles",
"full/parallel-ROM back squats enhance GMax hypertrophy" — are **qualitative
narrative synthesis of individual primary studies**, with no pooled numbers
behind them. Per-exercise percent-change figures quoted in the discussion
(e.g. full-ROM squat +6.7%, half-squat +2.2%; one within-study squat 9.4% vs
partial hip thrust 3.7%) come from *single* constituent studies, not the
meta-analysis, and are reported with inconsistent measurement modalities
(volume vs thickness vs CSA) and no common reference exercise. Deriving [0,1]
emphasis coefficients from them would be the entry-maker manufacturing data the
meta-analysis deliberately did not produce — exactly the over-reach the
`maeo_2023` "PROVISIONAL — METHOD CAVEAT" block warns against, and worse here
because Maeo at least had one controlled within-subject contrast.

So: encodable as **one EffectEstimate** ("does RT grow the glutes", SMD 0.71),
plus optionally its assessment/status subgroup estimates as non-poolable
context. Not encodable as `ExerciseEmphasis`.

## Topic mapping

No existing `Topic` fits. The registry's hypertrophy Topics are all
dose/execution variables (volume, frequency, load, failure, ROM, muscle length,
arm position). An "RT vs baseline grows muscle X" effect is a different
question — a *coverage / efficacy* claim, not a dose-response slope.

Two options for the entry-maker / orchestrator to decide:

1. **New Topic** — something like `RT_HYPERTROPHY_GLUTEUS_MAXIMUS` or, more
   generally, a `MUSCLE_TRAINABILITY` family keyed per muscle. This is the
   honest mapping but it adds a Topic that no optimizer query currently
   consumes, and the value (SMD vs baseline) is not on the same scale as any
   other encoded hypertrophy estimate, so it would be a permanent single-source,
   non-poolable Topic.
2. **Encode the module but expose it as guidance, not as a pooled Topic** —
   register a glute module that contributes `GUIDANCE_FOR_OPTIMIZER` text
   ("the glutes respond robustly to RT, SMD ~0.71; hip thrust is the
   glute-specific choice, full/parallel-ROM squats also effective") and holds
   the EffectEstimate for inspection, without wiring it into `_EFFECT_INDEX`
   under a query Topic the optimizer never asks.

Recommendation leans option 2 — see below.

## Overlap

No glute paper is currently encoded, so there is **no module-level overlap and
no double-counting risk against the current layer**. None of the encoded
modules (pelland_2026, failure_effects, maeo_2023, varovic_2025, wolf_2023,
schoenfeld_2017, kassiano_2023, pedrosa_2023, schoenfeld_load_2017) touch the
gluteus maximus or share this paper's scale.

**Scale mismatch (for the record):** the encodable estimate is an
RT-vs-baseline SMD. It is not poolable with any encoded estimate — different
question and different scale from every existing hypertrophy Topic. If a glue
module is created it must be flagged single-source / non-poolable, like the
note already attached to Schoenfeld 2017 in `_POOLABLE_OVERRIDE`.

**Constituent primary studies — record so future seeker passes do not
re-propose them as standalone glute candidates:**

1. Popov et al. 2006
2. Trindade et al. 2019
3. Kubo et al. 2019
4. Barbalho et al. 2020
5. Barbalho et al. 2021
6. Nakamura et al. 2021
7. Short et al. 2021
8. Balshaw et al. 2023
9. Plotkin et al. 2023
10. Wei et al. 2023
11. Kassiano et al. 2024
12. Bartolomei et al. 2024

If any of these is later encoded as a standalone primary study on the same
RT-vs-baseline glute question, a `_POOLABLE_OVERRIDE` would be needed to avoid
double-counting it inside this meta-analysis. (The two Barbalho et al. papers
have a known data-integrity history in the field — flag for the auditor if
either is ever queued individually.) None are currently encoded, so no action
needed now.

## Coverage

Muscle group: **gluteus maximus** — a large muscle group and an explicit `Gap`
in COVERAGE.md section 2 ("Gluteus maximus / medius — No evidence") and a named
priority-1 gap in section 3 ("Exercise selection for the large muscle
groups ... glutes").

The paper **partially** fills that gap. It establishes, with a meta-analysis,
*that* the gluteus maximus responds robustly to resistance training (a
trainability/efficacy fact worth having for whole-body coverage). It does
**not** fill the *exercise-selection* sub-gap the coverage table is really
asking for — there is still no encodable evidence ranking glute exercises. The
COVERAGE update should reflect this: glutes move from pure `Gap` to "Thin —
RT-vs-baseline efficacy only; exercise-selection still a gap." Gluteus *medius*
remains entirely uncovered (this paper is gluteus maximus only).

## Recommendation — NEW MODULE (narrow scope; guidance-first)

Encode it as its own module — it is a distinct paper with its own data and no
existing module can host it. **But scope the module deliberately narrowly:**

- Encode the overall **SMD 0.71 [0.50, 0.91]** as a single `EffectEstimate`,
  with the assessment-type and training-status subgroup estimates available for
  inspection but explicitly **non-poolable** (different sub-question/scale).
- Do **not** fabricate `ExerciseEmphasis` coefficients. The meta-analysis
  produced no per-exercise pooled effect and no head-to-head contrast; any
  [0,1] glute coefficients would be invented, not encoded. The entry-maker
  should record the hip-thrust / full-ROM-squat findings as
  `GUIDANCE_FOR_OPTIMIZER` narrative with a clear "qualitative, not pooled"
  caveat, not as `ExerciseEmphasis` objects.
- Prefer **not** to wire a new pooled `Topic` into `_EFFECT_INDEX` — an
  RT-vs-baseline efficacy SMD is not a dose-response the optimizer queries.
  Surface the module through `_GUIDANCE_SOURCES` instead, and let the
  orchestrator decide whether a `MUSCLE_TRAINABILITY`-style Topic is worth
  adding for future cross-muscle coverage.

Justification: the paper is genuinely in scope and fills a real coverage gap,
so SKIP would lose useful whole-body-coverage evidence and an ADDENDUM has no
host module to attach to. But the queue rationale — "closes the glute
exercise-selection gap" — overstates what the paper delivers: it is a
narrative review on exercise choice wrapped around a single pooled
RT-vs-baseline effect. The honest encoding is a small, narrow module that
records the one solid pooled number and the qualitative hip-thrust guidance,
explicitly flagged single-source and non-poolable, and that does NOT pretend to
be `ExerciseEmphasis` data. The seeker should keep hunting for a real glute
exercise-comparison study (a controlled hip-thrust vs squat hypertrophy trial,
e.g. Plotkin et al. 2023 / Bartolomei et al. 2024 as standalone candidates) to
actually close the exercise-selection gap.
