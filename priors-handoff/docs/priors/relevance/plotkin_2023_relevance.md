# Relevance Assessment — Plotkin et al. 2023 (hip thrust vs back squat, glute hypertrophy)

**Candidate paper:** Plotkin DL, Rodas MA, Vigotsky AD, McIntosh MC, Breeze E,
Ubrik R, Robitzsch C, Agyin-Birikorang A, Mattingly ML, Michel JM, Kontos NJ,
Lennon S, Frugé AD, Wilburn CM, Weimar WH, Bashir A, Beyers RJ, Henselmans M,
Contreras BM, Roberts MD. "Hip thrust and back squat training elicit similar
gluteus muscle hypertrophy and transfer similarly to the deadlift."
*Frontiers in Physiology*, 2023, 14:1279170.
**DOI:** 10.3389/fphys.2023.1279170 · **PMID:** 37877099 · **PMC:** PMC10593473
**Date assessed:** 2026-05-17
**Checker:** priors-relevance-checker

---

## In scope? — YES

The paper is a true head-to-head exercise-vs-exercise longitudinal RCT: 34
untrained college-aged adults (HT n=18, 5M/13F; SQ n=16, 6M/10F) randomised to
9 weeks of supervised, volume-equated barbell back squat OR barbell hip thrust,
2 sessions/week, 8–12 reps, sets progressed identically (3→6). Outcomes are
MRI cross-sectional area (gold-standard measurement) at three gluteus maximus
sites plus gluteus medius+minimus and thigh musculature, with 3RM strength
transfer.

Against the four research goals:

1. **Exercise selection** — directly served. It answers exactly the question
   COVERAGE.md §2 names for gluteus maximus ("hip thrust vs squat vs lunge
   selection") with the highest-value design (longitudinal, randomised,
   volume-equated, direct hypertrophy measurement). It is not EMG/activation
   work — it is the longitudinal hypertrophy data the rubric prefers.
2. **Form / execution** — not addressed (no ROM/tempo/length manipulation).
3. **Dose & paths** — not addressed (volume-equated by design; no dose
   contrast).
4. **Coverage** — high value: gluteus maximus is a `Gap` for a major lower-body
   muscle group, currently with **zero** encoded sources.

It is squarely in the core in-scope class (RT intervention study informing
exercise selection). The "similar hypertrophy" headline is a near-null /
equivalence result, but a credible null is itself encodable and useful — it
tells the optimizer hip thrust and back squat are roughly interchangeable for
glute growth, with the squat additionally buying quadriceps and adductor
hypertrophy.

---

## Data shape — EffectEstimate (between-exercise contrasts), NOT cleanly ExerciseEmphasis

This is the most important finding of the assessment, and it diverges from the
seeker shortlist's expectation that the paper "yields actionable
`ExerciseEmphasis` data."

**Why it is not a clean ExerciseEmphasis source.** An `ExerciseEmphasis`
coefficient is a per-(exercise, muscle, region) [0,1] value, and the sibling
modules (maeo_2021, maeo_2023, kassiano_2023) all derive it from **per-exercise
growth** (each exercise's own % change), then normalise within-muscle to the
higher-growth exercise. Plotkin 2023 deliberately does **not** support that:
the authors state explicitly that "within-group inferential statistics were not
calculated … within-group outcomes are not the subject of our research
question," and present within-group changes only descriptively in figures. The
entire inferential analysis is the **between-group contrast** (HT minus SQ),
reported as effect ± SE with 95% CI:

- Glute max upper:  −0.5 ± 2.6 cm²; CI95 (−5.8, 4.1)
- Glute max middle: −0.5 ± 1.7 cm²; CI95 (−4.0, 2.6)
- Glute max lower:  −1.6 ± 2.1 cm²; CI95 (−6.1, 2.0)
- Glute med+min:    −1.8 ± 1.5 cm²; CI95 (−4.6, 1.4)
- Quadriceps:       +3.6 ± 1.5 cm²; CI95 (0.7, 6.4)  [favours SQ]
- Adductors:        +2.5 ± 0.7 cm²; CI95 (1.2, 3.9)  [favours SQ]
- Hamstrings:       +0.1 ± 0.6 cm²; CI95 (−0.9, 1.4)

These are clean **EffectEstimate**-shaped contrasts: each has a mean and a
recoverable SE (SE is reported directly; CIs corroborate). They are in absolute
cm² (a between-group raw mean difference scale), not SMD and not %-per-set.

For glute max, all three site contrasts cross zero with wide CIs — a genuine
**equivalence/null** result that must be encoded honestly as "no detectable
difference, HT numerically/modestly ahead" rather than as a coefficient that
implies one exercise wins. Forcing an `ExerciseEmphasis` here (e.g. squat = HT
× ratio-of-descriptive-figure-values) would (a) be built on numbers the authors
declined to test, and (b) misrepresent a null as a measured emphasis gap.

**Practical encoding recommendation for the entry-maker:** encode the
between-exercise CSA contrasts as `EffectEstimate`s on a clearly-documented raw
cm² difference scale, paired with strong `GUIDANCE_FOR_OPTIMIZER` text stating
the glute-max equivalence and the squat's thigh (quad + adductor) bonus. If an
`ExerciseEmphasis` representation is wanted so the optimizer's exercise-ranking
path can consume glute data, it can be encoded only as an **equivalence**
coefficient — hip thrust and back squat both ~1.0 for gluteus maximus at
`confidence="medium"` (CIs span zero) — with the descriptive within-group
figures cited as rationale and the provisional-scale method caveat that
maeo_2021/maeo_2023/kassiano_2023 already carry. That is defensible because the
optimizer's selection question ("are these interchangeable for glutes?") is
answered directly; what is NOT defensible is a fractional coefficient implying a
measured winner. The entry-maker should pick one of these and document the
choice; the EffectEstimate-contrast path is the more faithful primary encoding.

---

## Topic mapping

The between-exercise contrasts do not map onto any existing dose/form `Topic`
(volume/frequency/load/failure/ROM/muscle-length/arm-position/rest-interval are
all "how to train" axes; this paper holds all of those fixed and varies the
exercise). This is **exercise-selection** evidence.

- If encoded as `ExerciseEmphasis` (equivalence form): it enters the separate
  emphasis index keyed by `(exercise, muscle, region)` — e.g.
  `("barbell_hip_thrust", "gluteus_maximus", None)` and
  `("barbell_back_squat", "gluteus_maximus", None)`, plus optionally per-site
  regions (`upper` / `middle` / `lower`). No new `Topic` and no
  `_POOLABLE_OVERRIDE` entry are needed — exactly as for maeo_2021.
- If encoded as `EffectEstimate` contrasts: this would need a **NEW Topic**,
  e.g. `EXERCISE_SELECTION_HYPERTROPHY` or a muscle-scoped variant, because the
  Topic enum currently has no exercise-vs-exercise selection question. Note
  that a single between-exercise raw-cm² contrast is not poolable with anything
  encoded today (different scale, different question), so it would be a
  single-source non-poolable Topic — the entry-maker should weigh that against
  the cleaner emphasis-index route. Either way, no existing Topic fits.

Recommended: treat it primarily as exercise-selection data feeding the emphasis
index, with the contrast magnitudes preserved in module-level constants and
guidance text. This keeps it on the same registry path as the other three
selection papers and avoids minting a barely-populated Topic.

---

## Overlap & double-counting

**Krause Neto 2025 (the seeker's flagged overlap) — NO double-counting risk.
RESOLVED.** Krause Neto W, Vieira TLK, Gama EF (2025), the gluteus maximus
hypertrophy systematic review and meta-analysis (DOI 10.3389/fphys.2025.1542334),
is **parked in `DEFERRED_CANDIDATES.md` and is NOT encoded** — it appears in no
module, no `_EFFECT_INDEX` entry, and no registry Topic. Plotkin 2023 is very
plausibly one of its constituent primary studies, but:

1. Because Krause Neto is unencoded, there is no pool for Plotkin to
   double-count against today. Encoding Plotkin creates no conflict.
2. Krause Neto, per its own deferral note, pools only a generic whole-muscle
   RT-vs-baseline effect (SMD 0.71) and carries **no per-exercise data** — so
   even if it were later encoded, it would not be on a common scale with
   Plotkin's between-exercise cm² contrasts and could not be inverse-variance
   pooled with them.
3. If Krause Neto is ever promoted, the standard guard already used twice in
   the layer applies: the constituent primary study (Plotkin) stays out of the
   inverse-variance pool — the same treatment Pedrosa 2023 and Maeo 2021 get
   relative to Varovic 2025. A `_POOLABLE_OVERRIDE` would be added **at that
   time, for the Krause Neto Topic**, not now. **Action for whoever later
   encodes Krause Neto:** record that Plotkin 2023 is a constituent and must be
   excluded from its pool.

No other overlap exists:

- **No glute paper is currently encoded** — gluteus maximus, medius and
  minimus are all `Gap` in COVERAGE.md §2. Plotkin touches no encoded module.
- **Kassiano et al. 2024** (barbell hip thrust *addition* study, also in
  `DEFERRED_CANDIDATES.md`) overlaps the same muscle but is unencoded, is an
  addition design (not a head-to-head A-vs-B), shares no dataset with Plotkin,
  and is explicitly parked as a *future second* glute source. No conflict;
  when promoted it would be a separate emphasis source for the same muscle and
  combine via quality-weighted averaging — which is the intended multi-source
  emphasis path, not double-counting.
- **No shared dataset / companion / re-analysis** concern: Plotkin 2023 is a
  standalone primary RCT with its own cohort.
- **Scale:** the between-exercise contrasts are in raw cm² difference — a scale
  no encoded `EffectEstimate` uses (encoded scales are SMD and %-per-set). This
  must be documented in the module `scale=` field and is a further reason it
  cannot be pooled with existing effect estimates.

---

## Coverage value

- **Gluteus maximus** — fills a `Gap` for a major lower-body muscle group with
  zero prior coverage. High value: glutes are one of COVERAGE.md §3's named
  "five big movers" for exercise selection. The MRI sub-site data (upper /
  middle / lower) also gives sub-muscle resolution, matching the granularity
  the coverage map asks for.
- **Gluteus medius + minimus (hip abductors)** — the paper reports a combined
  med+min CSA contrast; touches the `Hip abductors` `Gap` row, though only as a
  by-product (combined, not separated; no abduction-specific exercise).
- **Quadriceps and hip adductors** — the paper also yields squat-favouring
  thigh contrasts (quads +3.6 cm², adductors +2.5 cm²). These are real,
  significant findings (CIs exclude zero) and partially inform the `Quadriceps`
  and `Hip adductors` `Gap` rows — squat clearly out-grows the hip thrust for
  the thigh. This is secondary coverage (the comparison is squat-vs-hip-thrust,
  not squat-vs-a-quad-isolation-exercise) but is worth encoding as guidance.

Net: closes the gluteus maximus selection gap and contributes partial,
honest evidence to three further `Gap` rows.

---

## Recommendation — NEW MODULE

Encode Plotkin 2023 as its own module (suggested `plotkin_2023.py`). It is a
distinct primary RCT with its own cohort and its own data, filling a
zero-coverage major-muscle gap — the default case for NEW MODULE.

Justification: the paper is solidly in scope, high measurement quality (MRI),
and directly answers the gluteus-maximus exercise-selection question that
COVERAGE.md flags as a priority gap, while also delivering a clean,
honestly-null glute result plus significant squat-favouring thigh contrasts.
The Krause Neto overlap flag is fully resolved — Krause Neto is unencoded,
carries no per-exercise data, and would not be poolable with Plotkin even if
later encoded; **no `_POOLABLE_OVERRIDE` is required now**, and the only future
action is to record Plotkin as a constituent if Krause Neto is ever promoted.
The one substantive instruction for the entry-maker: the paper supports
**between-exercise `EffectEstimate` contrasts**, not per-exercise growth ratios
— the authors deliberately ran no within-group inferential statistics — so the
glute-max result must be encoded as an equivalence/null (hip thrust ≈ back
squat), never as a fractional `ExerciseEmphasis` coefficient implying a
measured winner. Encode the contrasts on a documented raw-cm² scale (not
poolable with existing SMD/%-per-set estimates) and, if an emphasis-index entry
is wanted for the optimizer's selection path, give hip thrust and back squat
equal ~1.0 glute-max emphasis at `confidence="medium"`.
