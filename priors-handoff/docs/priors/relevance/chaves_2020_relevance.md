# Relevance Assessment — Chaves et al. 2020 (incline vs horizontal bench press, regional chest hypertrophy)

**Candidate paper:** Chaves SFN, Rocha-Júnior VA, Encarnação IGA, Martins-Costa HC,
Freitas EDS, Coelho DB, Franco FSC, Loenneke JP, Bottaro M, Ferreira-Júnior JB.
"Effects of Horizontal and Incline Bench Press on Neuromuscular Adaptations in
Untrained Young Men." *International Journal of Exercise Science*, 2020,
13(6):859–872.
**DOI:** 10.70252/FDNB1158 · **PMID:** 32922646 · PMC7449336
**Date assessed:** 2026-05-17
**Checker:** priors-relevance-checker

---

## In scope? — YES

The paper directly serves **Research Goal 1 (exercise selection)** and
**Goal 4 (whole-body coverage)**:

- It is a longitudinal **exercise-vs-exercise RCT**: 47 untrained young men
  randomised to three 8-week, once-weekly training groups — horizontal-only
  bench press (n=15), incline-only bench press (n=15), and a combination of
  both (n=17).
- Outcomes are **direct hypertrophy measurements** (B-mode ultrasound muscle
  thickness) at three pectoralis major sites, *not* surface-EMG activation. It
  is not an acute study. This is exactly the design the seeker brief privileges
  for selection gaps and is well inside scope.
- It answers the question COVERAGE.md §2 flags as the key chest selection
  question — does incline press preferentially grow the **clavicular (upper)**
  region relative to the **sternocostal (mid/lower)** region — at sub-muscle
  granularity.

The seeker's flagged caveats (once-weekly frequency, untrained men, small
per-group n ≈ 15–17, smaller open-access journal) are **quality-scoring**
concerns for the entry-maker downstream. They do not affect scope. They should
be carried into the module's QUALITY block, not used to reject the paper.

Distinct from the DEFERRED Lanza 2024 paper, which is bench-press-vs-control
(no A-vs-B contrast). Chaves is the genuine selection paper.

## Data shape — ExerciseEmphasis (primary) + EffectEstimate (secondary, optional)

**Primary: `ExerciseEmphasis`.** The paper reports per-site, per-group muscle
thickness pre/post means with SDs, from which within-site % growth can be
derived and normalised to the best-growing exercise — exactly the derivation
used by maeo_2023, maeo_2021, and kassiano_2023. Verified site numbers (mm,
mean (SD)):

| Site | Group | Pre | Post | Δ (≈ % growth) |
|---|---|---|---|---|
| 2nd intercostal (clavicular / upper) | Horizontal | 11.9 (2.0) | 15.7 (3.9) | +3.8 (≈ +32%) |
| | Incline | 15.1 (3.8) | 24.5 (4.1) | +9.4 (≈ +62%) |
| | Combination | 14.3 (5.3) | 18.8 (6.5) | +4.5 (≈ +31%) |
| 3rd intercostal (sternocostal) | Horizontal | 13.2 (3.5) | 19.3 (5.0) | +6.1 (≈ +46%) |
| | Incline | 15.4 (4.3) | 23.8 (5.7) | +8.4 (≈ +55%) |
| | Combination | 17.1 (5.0) | 21.2 (4.9) | +4.1 (≈ +24%) |
| 5th intercostal (sternocostal) | Horizontal | 12.6 (2.7) | 18.0 (5.1) | +5.4 (≈ +43%) |
| | Incline | 14.4 (4.2) | 22.8 (5.4) | +8.4 (≈ +58%) |
| | Combination | 16.0 (5.5) | 22.7 (5.9) | +6.7 (≈ +42%) |

This supports emphasis coefficients keyed `(exercise, muscle="pectoralis_major",
region)` with `region` ∈ {`clavicular_head`, `sternocostal_head`} (and optionally
a whole-muscle `region=None`). Exercise keys would be `incline_bench_press`,
`horizontal_bench_press`, and `combination_bench_press`.

Two derivation caveats the entry-maker must apply, consistent with the
PROVISIONAL/METHOD-CAVEAT blocks already in the sibling emphasis modules:

1. **The clavicular split is the real, significant finding; the sternocostal
   split is not.** Between-group ANOVA was significant only at the 2nd
   intercostal site — incline > horizontal (0.62 cm difference, p=0.003) and
   incline > combination (0.50 cm, p=0.008). The 3rd (p=0.095) and 5th (p=0.227)
   intercostal sites showed **no significant between-group difference**. So the
   `clavicular_head` emphasis pair should be encoded at `confidence="high"`
   (direction solid) and the `sternocostal_head` pairs at `confidence="low"`
   ("effectively equal across exercises"), mirroring how maeo_2021 handles the
   non-significant BF-short-head pair.
2. The combination group is a genuine third exercise condition, not a pooling
   artefact — it can be its own emphasis key, but note its clavicular growth was
   *no better* than horizontal (more volume on incline did not help once incline
   was diluted with horizontal work).

**Secondary: `EffectEstimate`.** A between-group SMD for incline vs horizontal
at the clavicular site is recoverable (p=0.003 with the reported per-group n and
change SDs yields a mean and SE). This is optional — see Topic mapping below;
the layer has no chest-selection Topic and emphasis is the natural home. The
strength outcomes (isometric strength ~null, p=0.776 / 0.333; first-set load
favours the trained lift specifically) are too thin and too confounded by
specificity to encode as a useful strength prior — treat as context only.

## Topic mapping — no existing Topic; belongs in the emphasis index

This is **exercise-selection (Q1) data**, not a dose-response question. It does
not map to any registry `Topic` — the closest, `ARM_POSITION_HYPERTROPHY`, is
about joint position within a single elbow-extension movement (Maeo 2023) and is
a poolable whole-muscle SMD, not a per-exercise coefficient. Bench-press
inclination is a between-*exercise* contrast and belongs in the separate
`_EMPHASIS_INDEX`, keyed `(exercise, muscle, region)`, exactly as maeo_2021,
maeo_2023, and kassiano_2023 are routed.

**Recommendation: do NOT create a new Topic and export NO Topic-keyed
`EffectEstimate`** — same pattern as maeo_2021. Emphasis is the right and
sufficient shape. (If a future chest meta-analysis on incline-vs-flat is
encoded, a new `Topic` could be considered then; not now.)

## Overlap — none; first chest source, clean

- **No chest paper is currently encoded.** COVERAGE.md §2 lists pectoralis major
  as a `Gap` with no sources. There is no module to double-count against.
- **No shared dataset** with any encoded paper. Chaves is a stand-alone primary
  RCT and is not a constituent of any encoded meta-analysis (Varovic 2025,
  Wolf 2023, Pelland 2026, Singer 2024 — none cover chest exercise selection).
- **No scale-mismatch issue**, because nothing else occupies this space.
- It enters the `_EMPHASIS_INDEX` on a fresh set of keys
  (`pectoralis_major` / `clavicular_head` & `sternocostal_head`) that no
  existing emphasis source touches (current emphasis keys: triceps_brachii,
  hamstrings, gastrocnemius). `combine_emphasis_estimates` will be a passthrough.
- **No `_POOLABLE_OVERRIDE` entry needed.** Override entries exist only for
  Topic-keyed inverse-variance pools; an emphasis-only module never pools
  against a Topic. This mirrors the explicit note in maeo_2021.py.

## Coverage — fills a priority gap (chest, pectoralis major)

Chest / pectoralis major is one of the five large-muscle-group selection gaps
COVERAGE.md §3 ranks as the seeker's top priority. Encoding Chaves moves the
**clavicular (upper) head** from `Gap` to `Thin` with a real, significant
exercise contrast, and gives the **sternocostal head** a first (low-confidence,
~null) data point. It does not cover the sternal "inner"/adduction-biased fibres
(cable crossover, pec-deck end-range) — that sub-target remains a gap — so the
pectoralis major row should move from `Gap` to `Thin`, not `Covered`. It is the
first chest source in the layer and meaningfully advances whole-body coverage.

## Recommendation — NEW MODULE

Encode Chaves 2020 as its own module, `chaves_2020.py`, exporting
`EMPHASIS_ESTIMATES` only (no Topic-keyed `EffectEstimate`, no new `Topic`, no
`_POOLABLE_OVERRIDE`) and add it to `registry._EMPHASIS_SOURCES` alongside
maeo_2023, maeo_2021, kassiano_2023. It is a distinct primary study with its own
dataset, zero overlap with anything encoded, and it fills the highest-priority
selection gap (chest) at the exact sub-muscle granularity COVERAGE.md asks for.
The entry-maker should: (a) encode the clavicular incline-vs-horizontal pair at
`confidence="high"` and the two sternocostal pairs at `confidence="low"`
(between-group differences n.s.); (b) carry the once-weekly frequency, untrained
population, small per-group n, and smaller open-access journal into a QUALITY
block scored accordingly (expect a score below the maeo_2021/maeo_2023 tier);
(c) reuse the PROVISIONAL emphasis-scale caveat block from the sibling modules.
