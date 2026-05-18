# Audit — `singer_2024.py`

**Module audited:** `priors-handoff/app/priors/singer_2024.py`
**Source paper:** Singer A, Wolf M, Generoso L, Arias E, Delcastillo K, Echevarria E,
Martinez A, Androulakis Korakakis P, Refalo MC, Swinton PA, Schoenfeld BJ.
"Give it a rest: a systematic review with Bayesian meta-analysis on the effect of
inter-set rest interval duration on muscle hypertrophy." *Frontiers in Sports and
Active Living*. 2024;6:1429789. DOI: 10.3389/fspor.2024.1429789 · PMID: 39205815
**Date:** 2026-05-17
**Auditor:** independent priors-layer auditor

---

## Sources accessed

- PMC open-access full text — https://pmc.ncbi.nlm.nih.gov/articles/PMC11349676/
  — **full text obtained** (extracted via three separate WebFetch passes:
  quantitative results, Table 1 study list, abstract/methods).
- Frontiers publisher full text — https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2024.1429789/full
  — **full text obtained**; used to cross-check the Table 1 participant sum and
  measurement methods.
- OSF preregistration page — https://osf.io/ywevc — **NOT obtained** (page
  rendered as a near-empty shell; the preregistration document content could not
  be extracted). The pre-registration *status* of the region stratification is
  therefore left UNVERIFIED below.
- WebSearch (PubMed record, SportRxiv preprint, RGU repository, Biolayne, BarBend)
  — used only to corroborate the 9-RCT / 19-measurement framing.

The headline numbers were obtained from two independent renderings (PMC and
Frontiers) and agree, so the encoded effect sizes and credible intervals are
verified with high confidence. Only the OSF preregistration content is
genuinely unreachable.

---

## Verdict

**MINOR DISCREPANCIES**

Every encoded effect size, credible interval, recovered SE, scale, and the
quality-score arithmetic is correct and faithfully matches the paper. The
headline-estimate choice (univariate binary contrast), the exclusion of the
within-condition pre/post SMDs, the new `Topic.REST_INTERVAL_HYPERTROPHY`, and
the `_POOLABLE_OVERRIDE` keeping whole-body out of the pool are all sound,
well-documented judgement calls. Two issues keep this from `ACCURATE`, both
documentation-level rather than wrong encoded values: (1) the total participant
count is stated as **184** throughout the module but an independent sum of
Table 1 gives **185**; (2) the quality-score comment asserts the region splits
are "PRE-REGISTERED primary analyses" and on that basis declines the
subgroup-as-primary modifier — that pre-registration claim could not be
verified and the paper's own framing reads as exploratory subanalysis, so the
justification is unsupported even though the resulting 0.77 score is still
defensible. Neither issue changes a pooled result materially, hence MINOR.

---

## Value-by-value verification

| Encoded value | Paper value | Match? | Notes / citation |
|---|---|---|---|
| Arm SMD `mean=0.13` | 0.13 | ✅ | Binary controlled (between-condition) contrast, arm region. Confirmed PMC Results + abstract. |
| Arm CrI `-0.27, 0.51` | 95% CrI −0.27 to 0.51 | ✅ | PMC Results. |
| Thigh SMD `mean=0.17` | 0.17 | ✅ | PMC Results. Thigh = 10 effect measurements (best-evidenced). |
| Thigh CrI `-0.13, 0.43` | 95% CrI −0.13 to 0.43 | ✅ | PMC Results. |
| Whole-body SMD `mean=-0.08` | −0.08 | ✅ | PMC Results. Only region favouring shorter rest. |
| Whole-body CrI `-0.45, 0.29` | 95% CrI −0.45 to 0.29 | ✅ | PMC Results. |
| `scale="standardized_mean_diff"` | SMD throughout | ✅ | Correct shape; all three estimates are between-condition SMDs. |
| `n_studies=9` (all three) | 9 RCTs total | ⚠️ partial | 9 is the paper's total RCT count; each region uses a subset. See Concern 2. |
| Arm `n=60` | not reported per region | ❌ UNVERIFIED | Documented approximation; flagged in field comment. See Concern 1. |
| Thigh `n=100` | not reported per region | ❌ UNVERIFIED | Documented approximation. See Concern 1. |
| Whole-body `n=45` | not reported per region | ❌ UNVERIFIED | Documented approximation. See Concern 1. |
| Total participants "184" (docstring, POPULATION.notes, `__main__`) | Table 1 sum = **185** | ❌ | 12+20+21+18+28+21+21+22+22 = 185. See Concern 3 (MODERATE). |
| 19 effect measurements (6 arm / 10 thigh / 3 whole-body) | 19 (thigh 10, arm 6, whole body 3) | ✅ | Abstract, verbatim. |
| Multivariate values "arm 0.11, thigh 0.16, whole body 0.03" | 0.11 / 0.16 / 0.03 | ✅ | PMC Results. Whole-body multivariate is POSITIVE (+0.03) — correctly noted in docstring. |
| Within-condition pre/post "short 0.48, longer 0.56" | 0.48 (0.19–0.81) / 0.56 (0.24–0.86) | ✅ | Correctly EXCLUDED from EffectEstimates. See Concern 5 — verified clean. |
| Four-tier within-condition "0.47/0.65/0.55/0.50" | 0.47 / 0.65 / 0.55 / 0.50 | ✅ | Docstring values match; correctly not encoded. |
| Training status "6 untrained / 3 trained" | 6 untrained, 3 resistance-trained | ✅ | PMC study composition. |
| Sex "6 male / 1 female / 1 mixed / 1 n/a" | 6 male-only, 1 female-only, 1 mixed, 1 unspecified | ✅ | PMC study composition. |
| Age "8 young (18–35), 1 elderly (>65)" | 8 young adults, 1 older adults | ✅ | PMC study composition. `age_range=(18,70)` is a reasonable envelope. |
| Funding "no financial support" | "no financial support was received" | ✅ | PMC funding statement, verbatim. |
| Conflict "Schoenfeld formerly on Tonal advisory board" | confirmed | ✅ | PMC conflict statement. |
| tau "~0.08–0.17" | arm τ 0.10, thigh τ 0.17, whole-body τ 0.08 | ✅ | PMC heterogeneity table. Range stated in quality comment is correct. |
| "no appreciable differences resting >90 s" | paper: "casts doubt as to any beneficial effects" beyond 90 s | ✅ | Paraphrase is faithful. |

---

## Math checks

### SE recovery — `(hi - lo) / (2 × 1.96)`

| Estimate | CrI | Recomputed SE | Module comment | Match? |
|---|---|---|---|---|
| Arm | (−0.27, 0.51) | 0.78 / 3.92 = **0.198980** | `0.19898` | ✅ |
| Thigh | (−0.13, 0.43) | 0.56 / 3.92 = **0.142857** | `0.14286` | ✅ |
| Whole-body | (−0.45, 0.29) | 0.74 / 3.92 = **0.188776** | `0.18878` | ✅ |

All three inline-comment SEs are correct to the displayed precision.

### CrI round-trip (`ci_95` reconstruction from the symmetric SE)

| Estimate | Paper CrI | `ci_95` reconstructs | Asymmetry |
|---|---|---|---|
| Arm | (−0.27, 0.51) | (−0.26, 0.52) | mild — paper CrI midpoint 0.12 vs mean 0.13 |
| Thigh | (−0.13, 0.43) | (−0.11, 0.45) | mild — paper CrI midpoint 0.15 vs mean 0.17 |
| Whole-body | (−0.45, 0.29) | (−0.45, 0.29) | none — paper CrI is exactly symmetric here |

The docstring caveat about Bayesian-CrI asymmetry is accurate. The thigh
posterior is the most skewed (mean 0.17 sits above the CrI midpoint 0.15), but
the discrepancy is ~0.02 SMD — immaterial for inverse-variance pooling. Caveat
correctly mirrors `wolf_2023.PARTIAL_LONG_LENGTH_VS_FULL`.

### Quality-score weighted average

```
0.80×0.20 + 0.70×0.15 + 0.60×0.20 + 1.00×0.15 + 0.90×0.10 + 0.85×0.10 + 0.60×0.10
= 0.160 + 0.105 + 0.120 + 0.150 + 0.090 + 0.085 + 0.060
= 0.770
```

Arithmetic is correct; `QUALITY = 0.77` is the rounded weighted average. No flat
modifiers applied. See Concern 4 for whether the subgroup-as-primary modifier
*should* have been applied.

### Participant arithmetic

Independent sum of Table 1 study sizes:
`12 + 20 + 21 + 18 + 28 + 21 + 21 + 22 + 22 = `**`185`**.
The module states **184** in three places (docstring header, `POPULATION.notes`,
`__main__` print). This is a 1-participant discrepancy — see Concern 3.

The per-region approximations sum to `60 + 100 + 45 = 205`, which deliberately
exceeds 185 because a single participant contributes effect measurements to more
than one region (e.g. a study measuring both arm and thigh). That overshoot is
expected and not itself an error — see Concern 1.

---

## Concerns & discrepancies (ranked)

### 1. Per-region participant counts (n=60/100/45) — UNVERIFIED — **MODERATE**

The paper does not publish a per-region participant breakdown; both the PMC and
Frontiers renderings confirm Table 1 reports only per-study totals. The encoded
`n` values are documented approximations scaled from the 6/10/3 effect-measurement
split, and every field carries an explicit `UNVERIFIED` comment — that is honest
and meets the rubric's expectation for documented deviations.

The judgement to use *approximate per-region n* rather than a *shared n=185 on
all three* is defensible: `n` feeds `best_applicable()`'s `sqrt(n)` weighting and
`combine_inverse_variance` sums `n` across pooled estimates. A shared 185 would
overstate the arm estimate's power (only 6 of 19 measurements) and, when arm+thigh
are pooled, sum to 370 — implying more independent participants than the study
base contains. The split-based approximation keeps the *relative* weighting
roughly right (thigh > arm) and the pooled `n` (160) closer to the true unique
base. **Note** the approximations sum to 205 > 185 because of cross-region
participant overlap; this is inherent and acceptable. Recommendation: leave as
is, but the field comments should state the 185 base (not 184 — see Concern 3)
and explicitly say the 205 sum exceeds 185 by design.

### 2. `n_studies=9` on every estimate; pooled arm+thigh reports `n_studies=18` — **MINOR**

Each region draws on a subset of the 9 RCTs, yet all three estimates carry
`n_studies=9`. When `combine_inverse_variance` pools arm+thigh it sums study
counts → `n_studies=18`, double-counting every RCT that measured both regions.
This is real double-counting, but its consequences are contained:

- `n_studies` is **not** used in any pooling weight — `combine_inverse_variance`
  weights purely by `precision` (1/SE²) and only *sums* `n_studies` for display.
- The pooled `n_studies` is a provenance/label field, not an input to a
  recommendation.

So it produces a cosmetically wrong "18" but cannot bias an optimizer decision.
It is nonetheless misleading to anyone inspecting `pooled_effect()`. The honest
encoding would be the per-region subset count (the module would need the paper's
Table 1 region flags to know how many of the 9 measured arm vs thigh). Since the
paper does not cleanly publish that split, a reasonable interim fix is a one-line
note in each estimate that `n_studies=9` is the *paper-level* count and that the
pooled arm+thigh figure overstates unique studies. Recommend documenting rather
than leaving silent.

### 3. Total participant count stated as 184, should be 185 — **MODERATE**

The module says "184 total participants" / "184 participants" in the docstring
header, `POPULATION.notes`, and the `__main__` sanity print. Two independent
full-text renderings of Table 1 sum to **185** (12+20+21+18+28+21+21+22+22). The
paper does not print a headline total, so 184 appears to be an arithmetic slip by
the entry-maker (or a transposed study size). This is a wrong encoded fact, not
just wording — hence MODERATE rather than MINOR. It does not affect any encoded
`EffectEstimate.n` (those are the region approximations) and does not change the
0.77 quality score (185 is still inside the rubric's 150–299 meta-analysis band,
score 0.70). But it should be corrected to 185 in all three locations, and the
per-region `n` comments that reference "184 across 9 studies" updated to 185.

*If the orchestrator can re-confirm against the paper PDF and finds 184 printed
somewhere explicit, defer to the paper — but the Table 1 sum independently
produces 185 from both mirrors, so 185 is the auditor's finding.*

### 4. Quality score 0.77 — sound number, but the modifier justification is unverified — **MINOR**

The seven dimension scores are individually defensible:

- Study design 0.80 — correct: SR/MA of RCTs; the rubric's 0.80 tier is "SR/MA
  of RCTs with pre-registered protocol." The overall protocol *was* preregistered
  on OSF, so 0.80 (not the 0.70 mixed-design tier) is right — all 9 included
  studies are randomized.
- Sample size 0.70 — correct for the 150–299 band (185 participants).
- Measurement 0.60 — defensible: limbs use MRI/ultrasound (0.85–1.0 tier) but
  the whole-body region leans on DXA-FFM/BIA/hydrodensitometry (0.2–0.5 tier) and
  some studies used circumference; a blended 0.60 is reasonable, arguably even
  slightly generous given BIA/hydrodensitometry are at the rubric's floor.
- Methodological 1.00 — correct: preregistered, hierarchical Bayesian,
  univariate + multivariate specs, funnel plot. Top tier.
- Reporting 0.90 — correct: full CrIs for every estimate, region breakdown,
  tau reported, OSF prereg; no separate code/data deposit beyond registration.
- Risk of bias 0.85 — correct: "no financial support," one disclosed *past*
  Tonal tie not bearing on a rest-interval finding, clean funnel plot.
- Population 0.60 — correct: heterogeneous untrained/trained, mixed sex,
  described per study.

The arithmetic (0.770) is right. **The problem is the stated reason for omitting
the subgroup-as-primary ×0.85 modifier.** The quality comment asserts: "The
region splits are PRE-REGISTERED primary analyses, not post-hoc subgroups, so the
subgroup-as-primary modifier does not apply." The auditor could not verify this:
the OSF preregistration page would not load, and the paper's own framing presents
the body-region stratification as a subanalysis (the abstract describes the
*non-controlled* 19-measurement model as primary; region splits read as
exploratory). One WebFetch pass over the methods explicitly concluded the
regional stratification "appears post-hoc."

If the region stratification is in fact post-hoc, the rubric's ×0.85
subgroup-as-primary modifier would apply, taking the score to 0.77 × 0.85 ≈
**0.65**. That is a one-tier drop and would change pooling weight.

This is rated MINOR rather than MATERIAL only because: (a) the *between-condition*
region SMDs are arguably the paper's central question (the title is about the
rest-interval *effect*), and the region grouping is a natural axis, not a
data-dredged subgroup; (b) the modifier is explicitly a judgement call. But the
module currently rests an omitted-modifier decision on an unverified
pre-registration claim. **Recommend** either (i) verifying the OSF prereg lists
body-region stratification a priori and citing it, or (ii) softening the comment
to "the region grouping is the paper's natural reporting axis, not a post-hoc
data-driven subgroup, so the ×0.85 modifier is judged not to apply" — a
judgement that does not depend on the prereg. Do not leave an unverifiable
factual claim ("PRE-REGISTERED") as the load-bearing justification.

### 5. Headline-estimate choice (univariate binary contrast) — verified CORRECT — no concern

The module encodes the univariate binary between-condition contrast
(0.13/0.17/−0.08) rather than the multivariate model (0.11/0.16/+0.03). This is
the right primary estimate: the binary short(≤60s)-vs-longer(>60s) contrast is
the simplest, most directly actionable framing for an optimizer, and the
univariate model is the conventional headline. The docstring correctly notes the
multivariate whole-body estimate is POSITIVE (+0.03) and that the two models
otherwise agree closely. Crucially, the whole-body *sign disagreement* that
drives the pool exclusion is a univariate-model artifact (−0.08); under the
multivariate model whole-body would not disagree in sign. The module's
`_POOLABLE_OVERRIDE` rationale leans partly on the −0.08 sign — but it also rests
on the independent, model-agnostic argument that whole-body uses a different
measurement construct (FFM vs site-specific) and only 3 measurements. That second
argument stands regardless of model, so the exclusion is robust. No change
needed; the choice is sound and honestly documented.

### 6. Within-condition pre/post SMDs correctly excluded — verified CLEAN — no concern

The within-condition pre-to-post SMDs (binary 0.48/0.56; four-tier
0.47/0.65/0.55/0.50) are described in the docstring's "WHAT IS DELIBERATELY NOT
ENCODED" section and appear in **no** `EffectEstimate`. The exclusion reasoning —
that these measure how much each rest-length *group grew*, not the *contrast
between* rest lengths — is correct and exactly the right call. Only the
between-condition difference SMDs are encoded. Verified.

### 7. `Topic.REST_INTERVAL_HYPERTROPHY` and `_POOLABLE_OVERRIDE` — verified SOUND — no concern

- The new enum value `"rest_interval->hypertrophy"` follows the established
  `variable->outcome` naming convention exactly.
- All three estimates are registered under that single Topic in `_EFFECT_INDEX`.
- The `_POOLABLE_OVERRIDE` entry routes to `singer_2024.poolable_estimates`,
  which returns arm+thigh only. This correctly mirrors the existing pattern
  (Schoenfeld/Pelland, Varovic/Pedrosa, load→strength 1RM-vs-isometric): the
  paper module owns the scientific judgement and the registry just calls the
  helper.
- The exclusion of whole-body is a *within-paper* override (different
  measurement construct + sign disagreement + thin 3-measurement base), correctly
  analogous to `load->strength` carrying 1RM and isometric as different outcomes.
- The `__main__` block asserts the poolable set has length 2 and excludes
  whole-body — a good built-in guard.

No registry or topic concern.

---

## Recommendations

1. **(MODERATE) Fix the participant total: 184 → 185.** Update the docstring
   header ("184 total participants"), `POPULATION.notes` ("184 participants"),
   and the `__main__` print ("n=184 participants"). Independent Table 1 sum from
   two mirrors = 185.

2. **(MINOR) Update the per-region `n` field comments** that say "184 across 9
   studies" to "185 across 9 studies," and add one clause noting the three
   approximations sum to 205 > 185 by design because participants contribute to
   multiple regions.

3. **(MINOR) Re-justify the omitted subgroup-as-primary modifier without the
   unverified pre-registration claim.** Either confirm against the OSF prereg
   (osf.io/ywevc) that body-region stratification was specified a priori and cite
   it, or rewrite the quality comment to rest the decision on the model-agnostic
   judgement that body region is the paper's natural reporting axis rather than a
   data-driven post-hoc subgroup. Do not leave "PRE-REGISTERED primary analyses"
   as the stated reason unless it can be verified. The 0.77 score itself is
   defensible and need not change; only the justification needs to be honest.
   (If the prereg is checked and the splits turn out to be post-hoc, apply the
   ×0.85 modifier → ~0.65 and re-score.)

4. **(MINOR) Document the `n_studies` double-count.** Add a clause to each
   estimate's note stating `n_studies=9` is the paper-level RCT count and that a
   pooled arm+thigh result will report `n_studies=18`, overstating unique
   studies; this is a display-only artifact and does not affect pooling weights.

5. **No change needed** to: the three effect sizes, all CrIs, the recovered SEs,
   the `scale`, the `PopulationSpec` fields, the headline-estimate choice, the
   exclusion of within-condition SMDs, `Topic.REST_INTERVAL_HYPERTROPHY`, or the
   `_POOLABLE_OVERRIDE`. These are all verified correct.

---

*End of audit.*
