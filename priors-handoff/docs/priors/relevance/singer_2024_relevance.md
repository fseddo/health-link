# Relevance Assessment — Singer et al. 2024 (inter-set rest interval & hypertrophy)

**Candidate paper:** Singer A, Wolf M, Generoso L, et al. "Give it a rest: a
systematic review with Bayesian meta-analysis on the effect of inter-set rest
interval duration on muscle hypertrophy." *Frontiers in Sports and Active
Living*, 2024; 6:1429789.
**DOI:** 10.3389/fspor.2024.1429789 · **PMID:** 39205815
**Open-access full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11349676/
**Date assessed:** 2026-05-17
**Checker:** priors-relevance-checker

---

## In scope? — YES

The paper is a systematic review with Bayesian meta-analysis of resistance-
training RCTs (9 RCTs, 19 effect measurements) measuring the effect of
inter-set rest interval duration on **muscle hypertrophy**. It maps directly to
research goal 3 (**dose & paths for hypertrophy** — rest interval is a
programming dimension the optimizer has to set for any prescribed set). It is
longitudinal hypertrophy data, not acute/EMG work, so it clears the core
in-scope test. It is a meta-analysis of intervention studies — the preferred
evidence tier for this layer.

Note it is a **hypertrophy-only** paper. Strength outcomes are not analyzed,
so it does not inform the strength path. That makes it in-scope but partial in
breadth — fine, since the queued gap is the hypertrophy/strength rest-interval
dimension and this is the hypertrophy half.

`COVERAGE.md` section 1 lists "Rest-interval duration → hypertrophy/strength"
as an explicit **Gap** ("a whole programming dimension currently with no
encoded evidence"). This paper closes the hypertrophy half of that gap.

---

## Data shape — EffectEstimate (with a caveat on which estimate to encode)

The paper reports two kinds of pooled numbers, and the entry-maker must not
confuse them:

1. **Within-condition pre-to-post SMDs** (non-controlled SMDs):
   - Binary split: short ≤60 s → SMD 0.48 (95% CrI 0.19–0.81);
     longer >60 s → SMD 0.56 (95% CrI 0.24–0.86).
   - Four-category: short 0.47, intermediate 0.65, long 0.55, very long 0.50.
   These describe "how much each group grew", **not** a contrast between rest
   lengths. They are NOT directly encodable as a rest-interval *effect* — both
   conditions grew, which only says training works. Do **not** encode these as
   the rest-interval effect estimate.

2. **Between-condition difference SMDs** — the actual rest-interval effect:
   - Arm hypertrophy: **SMD 0.13 (95% CrI −0.27 to 0.51)**, positive favors
     longer rest.
   - Thigh hypertrophy: **SMD 0.17 (95% CrI −0.13 to 0.43)**, positive favors
     longer rest.
   - Whole body: **SMD −0.08 (95% CrI −0.45 to 0.29)**, slightly favors shorter
     rest.

The between-condition estimates (arm, thigh, whole body) are the encodable
ones. Each is a posterior mean with a 95% credible interval, so a symmetric SE
is recoverable via `(high − low) / (2 × 1.96)` — exactly the `_se_from_qi`
helper already used in `wolf_2023.py`. Scale is `standardized_mean_diff`. So
the paper fits the **`EffectEstimate`** shape cleanly for those three
region-level contrasts.

Caveat the entry-maker must carry: Bayesian credible intervals here are
posterior intervals and may be mildly asymmetric (same caveat already
documented on `wolf_2023.PARTIAL_LONG_LENGTH_VS_FULL`). Forcing a single
symmetric SE is acceptable for inverse-variance pooling but `ci_95` will not
round-trip the paper's CrI exactly — note this in the module.

Not an `ExerciseEmphasis` paper: it does not compare exercises, so no
per-(exercise, muscle, region) coefficient is derivable.

---

## Topic mapping — NEW Topic required

The `Topic` enum in `registry.py` (lines 64–78) has **no rest-interval Topic**.
The existing dose Topics are volume / frequency / load / failure / ROM /
muscle-length / arm-position, each paired with hypertrophy and/or strength.
Rest interval is a distinct programming variable not covered by any of them.

**Proposed new Topic:**
```python
REST_INTERVAL_HYPERTROPHY = "rest_interval->hypertrophy"
```
Only the hypertrophy variant is justified by this paper. Do **not** add a
`REST_INTERVAL_STRENGTH` Topic now — there is no encoded strength evidence for
rest interval and the enum should not carry empty Topics (every other Topic in
`_EFFECT_INDEX` has at least one estimate). A strength variant can be added if
and when a rest-interval strength source is encoded.

Open design question for the entry-maker / orchestrator: the three encodable
estimates are **region-keyed** (arm, thigh, whole body), not a single pooled
number. The cleanest fit is to index all three under the one
`REST_INTERVAL_HYPERTROPHY` Topic and let the paper module decide the poolable
set. The arm and thigh estimates are on the same scale and the same contrast
direction, so they are plausibly poolable into one rest-interval effect; the
whole-body estimate points the other way (−0.08) and is the noisiest (only 3
effect measurements) — the module should expose a `poolable` helper and the
registry will likely need a `_POOLABLE_OVERRIDE` entry. Flag this for the
entry-maker rather than forcing it here.

---

## Overlap & double-counting

No rest-interval source is encoded, so there is **no Topic-level overlap** — this
is a genuinely new corner of the layer.

**Co-author overlap is NOT a dataset overlap.** The seeker correctly flagged
that this paper shares authors with the encoded Schoenfeld-group work:
- M. Wolf is a co-author here and lead author of encoded `wolf_2023.py`
  (partial vs full ROM).
- The group also produced encoded Refalo 2023 (`failure_effects.py`).
Shared authorship is irrelevant to double-counting — what matters is shared
*data*. The included-studies lists do not overlap in subject matter:
`wolf_2023` pools ROM studies; this paper pools rest-interval RCTs (Buresh
2009, de Souza 2010, Fink 2017, Hill-Haas 2007, Longo 2022, Piirainen 2011,
Schoenfeld 2016, Souza-Junior 2011, Villanueva 2015). Different research
question, different primary studies, different outcome contrast. **No
shared-dataset problem. No `_POOLABLE_OVERRIDE` needed for cross-paper
overlap.**

**Primary-study-inside-encoded-meta-analysis check:** none of this paper's 9
RCTs is encoded as its own module, so there is no "primary study inside an
encoded meta-analysis" double-count risk against the current layer.

**Scale check:** the encodable estimates are `standardized_mean_diff` — the
same scale family as `wolf_2023`, `varovic_2025`, `failure_effects`, etc. But
they are on a different *Topic*, so they will never be pooled against those.
Within the new Topic, all three estimates share one scale (SMD), so the only
pooling judgement is the within-paper arm/thigh/whole-body question noted
above — not a scale mismatch.

---

## Coverage

Muscle groups touched: **arm** (elbow flexors / extensors — 6 effect
measurements) and **thigh** (quadriceps / hamstrings — 10 effect measurements),
plus a whole-body aggregate (3 measurements).

This is **programming/dose coverage, not exercise-selection coverage** — it
fills a row in `COVERAGE.md` section 1, not section 2. It does not give
per-exercise data for the chest/back/quad/hamstring/glute/delt gaps in section
2. Its value is closing the section-1 "Rest-interval duration → hypertrophy"
Gap, converting it from Gap to Thin (single source). It does not by itself
address the rest-interval **strength** half — that stays a Gap.

Quality is likely to land in the moderate band when the rubric is applied:
Bayesian framework with credible intervals and region sub-analyses is a
strength, but only 9 RCTs, mean methodological quality 15/20, mixed and
predominantly untrained samples, and wide credible intervals that all cross
zero. The entry-maker should score it formally against `QUALITY_RUBRIC.md`;
expect something in the 0.75–0.83 range, comparable to `wolf_2023`.

---

## Recommendation — **NEW MODULE**

Encode as its own module, e.g. `app/priors/singer_2024.py`, exporting
`HYPERTROPHY_ESTIMATES` (the arm, thigh, and whole-body between-condition SMDs)
plus `GUIDANCE_FOR_OPTIMIZER`. This is the default case: a distinct paper with
its own data, its own primary-study set, answering a question nothing else in
the layer answers.

Required follow-on changes for the entry-maker, called out so they are not
missed:
1. **Add a new `Topic`** — `REST_INTERVAL_HYPERTROPHY` in `registry.py`. This
   is the first Topic added since the enum was written, so confirm with the
   orchestrator before editing the taxonomy.
2. **Encode only the between-condition difference SMDs** (arm 0.13, thigh 0.17,
   whole body −0.08). The within-condition pre/post SMDs (0.48 / 0.56 etc.) are
   not rest-interval effects and must not be encoded as such.
3. **A `_POOLABLE_OVERRIDE` will likely be required** — not for cross-paper
   overlap (there is none) but because the three within-paper estimates are
   region-keyed and the whole-body estimate points opposite to arm/thigh. The
   module should own the judgement of which estimates form the apples-to-apples
   poolable set. This is a within-paper override, analogous to
   `LOAD_STRENGTH` carrying two different outcomes.
4. Carry the Bayesian-credible-interval asymmetry caveat in the module, mirroring
   `wolf_2023.PARTIAL_LONG_LENGTH_VS_FULL`.

No `ADDENDUM` or `SKIP`: it shares no dataset with any encoded paper and is not
a sub-study or corrigendum of one. Co-authorship with Wolf/Refalo papers does
not change this.
