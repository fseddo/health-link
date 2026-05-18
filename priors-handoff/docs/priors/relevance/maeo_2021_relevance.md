# Relevance assessment — Maeo et al. 2021 (hamstrings, seated vs prone leg curl)

**Candidate paper:** Maeo S, Huang M, Wu Y, Sakurai H, Kusagawa Y, Sugiyama T,
Kanehisa H, Isaka T. "Greater Hamstrings Muscle Hypertrophy but Similar Damage
Protection after Training at Long versus Short Muscle Lengths." *Medicine &
Science in Sports & Exercise.* 2021;53(4):825–837.
DOI: 10.1249/MSS.0000000000002523 · PMID: 33009197 · PMC7969179

**Date assessed:** 2026-05-17
**Checker:** priors-relevance-checker

---

## In scope? — YES

The paper is a 12-week within-participant resistance-training intervention
(one leg seated leg curl, the other prone leg curl, 70% 1RM, 5×10, 2×/week,
MRI-measured muscle volume). It directly serves two of the four priors research
goals:

1. **Exercise selection** — it is a head-to-head comparison of two real,
   commonly programmed hamstrings exercises (seated vs prone/lying leg curl)
   with longitudinal hypertrophy outcomes. This is exactly the
   `ExerciseEmphasis`-shaped evidence the layer needs.
4. **Coverage** — hamstrings is currently a hard **Gap** in COVERAGE.md
   section 2 (no encoded evidence). This paper fills it.

It is gold-standard for the layer's preferences: longitudinal MRI hypertrophy
data, not EMG/activation. The muscle-damage half of the paper (Part 2) is out
of scope (injury-protection/physiology, not a training-dose recommendation) and
should simply not be encoded — but it does not disqualify the in-scope Part 1.

## Data shape — ExerciseEmphasis (primary); EffectEstimate not cleanly recoverable

**ExerciseEmphasis — yes, this is the encodable shape.** Part 1 reports
per-condition % muscle-volume change from which within-muscle [0,1] emphasis
coefficients can be derived exactly as Maeo 2023 (triceps) and Kassiano 2023
(calf) already do — ratio of the weaker exercise's % growth to the stronger
exercise's % growth, normalized to the best exercise = 1.0. The reportable
numbers (Part 1, n=20 within-subject):

| Muscle / sub-muscle | Seated | Prone | Emphasis (prone ÷ seated) |
|---|---|---|---|
| Whole hamstrings | +14.1% | +9.3% | 0.66 |
| Biceps femoris long head | +14.4% | +6.5% | 0.45 |
| Semitendinosus | +23.6% | +19.3% | 0.82 |
| Semimembranosus | +8.2% | +3.6% | 0.44 |
| Biceps femoris short head | +10% | +9% | 0.90 (n.s. — see note) |

Seated leg curl is the higher-growth condition for every head and would be the
1.0 reference. The biceps femoris **short head** difference (+10% vs +9%) is
**not statistically significant** — its emphasis pair should be encoded at
`confidence="low"` (or omitted), and mechanistically it is expected: the short
head is monoarticular and is not lengthened differently by hip position.

**EffectEstimate — not cleanly encodable.** The WebFetch of the full text
confirms the paper reports group means and p-values (P ≤ 0.010 for WH, BFL, ST,
SM) and shows 95% CIs *in figures only* — it does not tabulate a
between-condition SMD/Cohen's d with a recoverable SE the way Maeo 2023 does.
An SE could in principle be reverse-engineered from the change-score SDs, but
those were not extractable from the abstract/figures here. Treat this as an
**ExerciseEmphasis-only encoding** unless the entry-maker can extract
change-score SDs from the full PDF. Even if recovered, see the Overlap section
— an `EffectEstimate` here would be redundant with Varovic 2025.

## Topic mapping

This is **emphasis data**, keyed by (exercise, muscle, region), NOT a registry
`Topic`. It enters `_EMPHASIS_INDEX` via a new `EMPHASIS_ESTIMATES` list, the
same path as `maeo_2023.py` and `kassiano_2023.py`. No new `Topic` is needed
and no `Topic`-keyed `EffectEstimate` should be added.

Sub-muscle keys to use (extends the taxonomy noted in BACKLOG open question 4):
`biceps_femoris_long_head`, `biceps_femoris_short_head`, `semitendinosus`,
`semimembranosus`, plus `region=None` for whole hamstrings. Exercise keys:
`seated_leg_curl`, `prone_leg_curl` (a.k.a. lying leg curl).

## Overlap — CRITICAL double-counting finding

**Maeo 2021 IS one of the 12 primary studies inside the already-encoded
Varovic 2025 meta-analysis.** This is confirmed: the published Varovic 2025
included-studies list (PubMed 40570881 / Thieme) names Maeo et al. 2021
explicitly alongside Alegre 2014, Bloomquist 2013, the McMahon 2014 pair,
Noorkõiv 2014/2015, Pedrosa 2022, Sato 2021, Valamatos 2018 and
Zabaleta-Korta 2023. The seeker's overlap flag is correct.

Consequences:

- **`varovic_2025.py` (EffectEstimate, `MUSCLE_LENGTH_REGIONAL_HYPERTROPHY`).**
  Varovic's three regional SMDs (proximal/mid/distal) already absorb Maeo
  2021's proximal-vs-distal regional contrast (BF +20.8 vs +8.7% proximal,
  +10.7 vs +5.4% distal, etc.). **Encoding Maeo 2021's *regional* data as a
  separate poolable `EffectEstimate` on this Topic would double-count it.**
  This is the same situation already handled for Pedrosa 2023 — also a Varovic
  constituent — via the existing `_POOLABLE_OVERRIDE` for
  `MUSCLE_LENGTH_REGIONAL_HYPERTROPHY` (pool = Varovic only). The clean
  resolution here is the same: **do not add a `Topic`-keyed `EffectEstimate`
  for Maeo 2021 at all.** If one were added it would need adding to that
  override's exclusion — but the simpler and correct move is to encode Maeo
  2021 purely as `ExerciseEmphasis`.

- **No conflict in the emphasis index.** Varovic 2025 is encoded only as
  `EffectEstimate`s (`REGIONAL_ESTIMATES`); it contributes nothing to
  `_EMPHASIS_INDEX`. `_EMPHASIS_INDEX` is keyed by (exercise, muscle, region)
  and pooled by `combine_emphasis_estimates` (quality-weighted averaging), an
  entirely separate path from the inverse-variance `Topic` pool. Maeo 2021's
  whole-muscle / sub-muscle *exercise-selection* result — seated vs prone leg
  curl — is **a distinct question Varovic does not answer** and is **not
  encoded anywhere**. Adding it to `_EMPHASIS_INDEX` does not double-count
  against Varovic's `EffectEstimate`s because they are different scales
  (emphasis coefficient vs SMD) on different indices.

  This is exactly the Q1-vs-Q2 distinction the layer already documents
  (BACKLOG conceptual clarifications; `varovic_2025.py` docstring): Maeo 2021
  supplies **Q1** data (which *exercise* grows the muscle more overall),
  Varovic answers **Q2** (does growth differ by *region* within a condition).
  Encoding Maeo 2021 as emphasis-only keeps the layer on the right side of
  that distinction.

- **No `_POOLABLE_OVERRIDE` needed** *if* Maeo 2021 is encoded as
  `ExerciseEmphasis` only — the override mechanism governs `Topic` pools, and
  emphasis data never enters one. A `_POOLABLE_OVERRIDE` change would only be
  required if someone insisted on adding a regional `EffectEstimate`, which
  this assessment recommends against.

- **No shared-dataset clash with other modules.** Maeo 2021 and Maeo 2023 are
  same-lab, same-design but **different muscles and different cohorts**
  (hamstrings/legs vs triceps/arms) — independent datasets, no double-count.

- **Scale note.** Maeo 2021's emphasis coefficients would be derived from
  12-week %-volume ratios — the same provisional, intervention-specific scale
  flagged in `maeo_2023.py` and `kassiano_2023.py`. The standard PROVISIONAL
  METHOD CAVEAT block must be copied in: these are within-study relative
  rankings, not stable exercise constants.

## Coverage

Fills the **Hamstrings** Gap in COVERAGE.md section 2 — currently zero encoded
evidence for a major muscle group, explicitly named priority gap #1 for the
seeker. It also adds the first sub-muscle resolution for the posterior thigh
(BF long head, BF short head, semitendinosus, semimembranosus). It is the third
`ExerciseEmphasis` source (after triceps and gastrocnemius) and the second for
the lower body, validating that the emphasis infrastructure generalizes — a
stated goal in BACKLOG Tier 2 for this exact paper.

## Recommendation — NEW MODULE

Encode Maeo 2021 as its own module, `app/priors/maeo_2021.py`, exporting an
`EMPHASIS_ESTIMATES` list of `ExerciseEmphasis` objects for seated vs prone leg
curl across whole hamstrings and the four sub-muscle heads, and registered via
`_EMPHASIS_SOURCES` in `registry.py`. It is a distinct primary study with its
own dataset filling a top-priority muscle-group gap, and its exercise-selection
result is encoded nowhere else.

**Constraint the entry-maker MUST honour:** encode it as `ExerciseEmphasis`
**only**. Do **not** add a `MUSCLE_LENGTH_REGIONAL_HYPERTROPHY` `EffectEstimate`
— Maeo 2021's regional data is already inside the Varovic 2025 meta-analysis,
and a separate poolable estimate would double-count. Because no `Topic`-keyed
estimate is added, **no `_POOLABLE_OVERRIDE` change is needed**; the emphasis
index is a separate path that does not pool against Varovic. Mark the BF
short-head pair `confidence="low"` (difference n.s.) and copy the PROVISIONAL
METHOD CAVEAT used in `maeo_2023.py` / `kassiano_2023.py`. Quality should be
scored fresh against `QUALITY_RUBRIC.md` — likely near Maeo 2023's 0.89 given
the near-identical MRI within-participant design, but the entry-maker should
confirm sample size (n=20) and reporting from the full text.

---

### Sources

- [Maeo 2021 full text (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7969179/)
- [Maeo 2021 (PubMed 33009197)](https://pubmed.ncbi.nlm.nih.gov/33009197/)
- [Varovic 2025 (PubMed 40570881)](https://pubmed.ncbi.nlm.nih.gov/40570881/)
- [Varovic 2025 (Thieme)](https://www.thieme-connect.com/products/ejournals/abstract/10.1055/a-2615-4935)
