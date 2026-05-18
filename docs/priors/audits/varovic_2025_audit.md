# Literature Prior Audit: Varovic et al. 2025

**Module audited:** `priors-handoff/app/priors/varovic_2025.py`
**Paper:** Varovic D, Wolf M, Schoenfeld BJ, Steele J, Grgic J, Mikulic P. "Does Muscle Length Influence Regional Hypertrophy? A Systematic Review and Meta-Analysis." *International Journal of Sports Medicine* 2025;46(14):1027-1036. DOI 10.1055/a-2615-4935. PMID 40570881. Online June 26, 2025.
**Audit date:** 2026-05-17
**Auditor:** Independent literature auditor (re-fetched paper from scratch; did not trust the encoding).

---

## Sources accessed

| Source | URL | Accessed? | What it gave |
|---|---|---|---|
| PubMed record (PMID 40570881) | https://pubmed.ncbi.nlm.nih.gov/40570881/ | YES | Abstract: study count, population, methods, all SMD + lnRR values, conclusion. |
| Thieme Connect journal abstract page | https://www.thieme-connect.com/products/ejournals/abstract/10.1055/a-2615-4935 | YES (abstract only; full text paywalled) | Confirmed all SMD + lnRR values, conclusion, muscle-length manipulation methods. |
| CoLab article page | https://colab.ws/articles/10.1055/a-2615-4935 | YES | Confirmed values, ROPE, "increasing trend toward distal", 21.8% mean length difference. |
| R Discovery article record | https://discovery.researcher.life/article/.../1daf5ba6f112397fac3e0892fefae998 | YES | Confirmed all six values verbatim, conclusion, ROPE statement. |
| SportRxiv **preprint** (full text PDF) | https://sportrxiv.org/index.php/server/preprint/view/464 and the version-591 PDF download | YES (full text — 23 pages, read in full) | Full methods, population breakdown, study list, SMART-LD quality grades, ROPE definition, heterogeneity (tau), discussion and conclusion. **NB: this is the Oct 2024 preprint with DIFFERENT numbers — see below.** |
| ResearchGate "Request PDF" page | https://www.researchgate.net/publication/393056938_... | NO — HTTP 403 Forbidden | — |
| Published full text (Thieme) | https://www.thieme-connect.com/products/ejournals/html/10.1055/a-2615-4935 | NO — paywalled | Full-text Methods/Results/Discussion of the **published** version not directly readable. |

**Key access caveat:** The **published-paper abstract** was verified from four independent sources and they agree exactly. However, the **published full text** (Methods, Results tables, Discussion) is paywalled and was NOT read. Full-text–dependent claims are verified instead against the **preprint** full text, with the explicit warning that the preprint and the published paper differ materially in their headline numbers and framing (documented below). Items that depend on published full-text wording I could not see are marked UNVERIFIED.

---

## Verdict: **MINOR DISCREPANCIES**

The six headline effect values encoded in the module (three SMDs, three exponentiated lnRRs, with intervals) **match the published abstract exactly** — verified against four independent sources. The SE recomputations are arithmetically correct, and the quality score rounds correctly (0.875 → 0.88). The core conceptual framing (Varovic = "regional growth within a muscle" question, answer "trivial") is **faithful to the published paper's own conclusion**, which explicitly invokes regions of practical equivalence.

The discrepancies are not in the numbers but in three softer areas: (1) the `n=12` field is study count, not participants — a known and arguably defensible modelling choice, but it silently distorts `best_applicable`'s `sqrt(n)` weighting and any pooled-n reporting, and is not flagged in the module; (2) the encoded `age_range=(18, 35)` is an inferred bound, not a figure stated by the paper (the underlying studies' reported mean ages span ~18.8–27.2 years per the preprint); (3) the population is described as "mixed" training status, which is technically true but materially lopsided — 11 of 12 studies used **untrained** participants, only 1 used trained, so "mixed" overstates how trained-applicable this prior is. None of these rise to "material" because they do not corrupt the effect estimates themselves, but they should be fixed or documented.

---

## Value-by-value verification

| Encoded value | Paper value (published abstract) | Match? | Notes |
|---|---|---|---|
| Proximal SMD `mean=0.05` | SMD 0.05 | ✅ | Confirmed: PubMed, Thieme, CoLab, R Discovery. |
| Proximal QI (−0.07, 0.16) | 95% QI −0.07, 0.16 | ✅ | Confirmed all 4 sources. |
| Mid-belly SMD `mean=0.07` | SMD 0.07 | ✅ | Confirmed all 4 sources. |
| Mid-belly QI (−0.02, 0.15) | 95% QI −0.02, 0.15 | ✅ | Confirmed all 4 sources. |
| Distal SMD `mean=0.09` | SMD 0.09 | ✅ | Confirmed all 4 sources. |
| Distal QI (−0.01, 0.19) | 95% QI −0.01, 0.19 | ✅ | Confirmed all 4 sources. |
| Proximal lnRR +0.57% (−1.92%, +3.24%) | Exp. lnRR 0.57% [−1.92%, 3.24%] | ✅ | Confirmed PubMed + R Discovery. |
| Mid-belly lnRR +1.22% (−0.77%, +3.22%) | Exp. lnRR 1.22% [−0.77%, 3.22%] | ✅ | Confirmed PubMed + R Discovery. |
| Distal lnRR +1.88% (−0.44%, +4.34%) | Exp. lnRR 1.88% [−0.44%, 4.34%] | ✅ | Confirmed PubMed + R Discovery. |
| Contrast = longer-vs-shorter muscle length, positive favors longer | Paper: "RT at both longer and shorter mean muscle lengths produces similar hypertrophic effects"; preprint confirms positive SMD favors **longer** length | ✅ | Direction correct. The SMD is the "slope of muscle length" at each site (slope of a +50% length difference), i.e. the longer-vs-shorter contrast at that anatomical region. The module's framing ("longer-length vs short-length training" at each site) is accurate. |
| "12 studies" | 12 studies meta-analyzed (13 in systematic review; 1 dropped as duplicate dataset — Noorkõiv 2015 reused Noorkõiv 2014) | ✅ | Confirmed. The "12" vs "13" nuance is harmless for this module. |
| "young adults" | "studies conducted among young adults"; preprint: all studies aged 18.8–27.2 yr | ✅ (label) / ⚠️ (range) | See age-range note below. |
| `age_range=(18, 35)` | Paper states "young adults"; preprint gives study mean ages 18.8–27.2 yr | ⚠️ INFERRED | The paper does not state an 18–35 range. 35 is an over-wide upper bound relative to the actual data (no study mean above ~27). Not wrong per se as an applicability envelope, but it is an auditor-unverifiable inference, not a paper figure. |
| `training_status="mixed"` | 11/12 studies untrained, 1/12 trained (Zabaleta-Korta 2023) | ⚠️ MISLEADING | "Mixed" is literally true but the population is ~92% untrained. See concerns. |
| Bayesian meta-analysis | "performed within the Bayesian meta-analytic framework" | ✅ | Confirmed. |
| Regional muscle thickness via ultrasound | Inclusion criteria allowed ultrasound, CT, or MRI direct imaging; ultrasound predominant | ⚠️ PARTLY | "via ultrasound" is the typical method but the paper explicitly admits CT/MRI. Module comment "regional muscle thickness via ultrasound; mostly site-specific" is approximately right but slightly overstated as ultrasound-only. |
| ROPE / equivalence testing used | Yes — paper notes "percentage of posterior distributions falling within regions of practical equivalence was high across all sites"; preprint defines ROPE as SMD (−0.1, 0.1) and lnRR (−3%, 3%) | ✅ | Confirmed. |
| `scale="standardized_mean_diff"` | SMD is the encoded `mean`; lnRR carried only in notes text | ✅ | Consistent — `mean` holds the SMD, scale matches. |

### Critical discrepancy flag — preprint vs published numbers

The SportRxiv **preprint** (last updated 6 Oct 2024) reports **substantially larger** point estimates and a **different conclusion**:

| Site | Preprint SMD | Published SMD | Preprint lnRR | Published lnRR |
|---|---|---|---|---|
| Proximal | 0.10 | 0.05 | 1.1% | 0.57% |
| Mid-belly | 0.15 | 0.07 | 2.61% | 1.22% |
| Distal | 0.20 | 1.88%→ | 4.13% | 1.88% |

Preprint conclusion: *"if positive effects of training at longer muscle lengths on regional muscle hypertrophy exist, they may be the greatest at the distal sites … our findings should be considered exploratory."* The published abstract is markedly more null/equivalence-leaning. **The module correctly uses the PUBLISHED numbers** — this is the right choice. But anyone re-verifying against the preprint (or against the WebFetch summary of the preprint, which returned yet a third set: 0.04/0.07/0.09) will see mismatches. Recommend the module add a one-line note that the preprint values differ and the published values are authoritative.

---

## Math checks

### SE recovery — `_se_from_qi(low, high) = (high - low) / (2 * 1.96)`

| Region | QI | Recomputed SE | Module comment | Verdict |
|---|---|---|---|---|
| Proximal | (−0.07, 0.16) | (0.16 − (−0.07)) / 3.92 = 0.23/3.92 = **0.058673** | "≈ 0.0587" | ✅ correct |
| Mid-belly | (−0.02, 0.15) | (0.15 − (−0.02)) / 3.92 = 0.17/3.92 = **0.043367** | "≈ 0.0434" | ✅ correct |
| Distal | (−0.01, 0.19) | (0.19 − (−0.01)) / 3.92 = 0.20/3.92 = **0.051020** | "≈ 0.0510" | ✅ correct |

All three inline comments are arithmetically accurate to the stated precision.

**Caveat on the SE method itself (not an arithmetic error):** `_se_from_qi` assumes a symmetric posterior, but the encoded means are NOT the QI midpoints:

| Region | QI midpoint | Encoded mean | Offset |
|---|---|---|---|
| Proximal | 0.045 | 0.05 | +0.005 |
| Mid-belly | 0.065 | 0.07 | +0.005 |
| Distal | 0.090 | 0.09 | 0.000 |

The proximal and mid-belly posteriors are very slightly right-skewed (mean above midpoint). The offsets are tiny (0.005, ~9% of one SE) and immaterial for pooling, but they confirm the docstring's `_se_from_qi` "assuming symmetric posterior" is a genuine approximation. This is fine and honest; no action needed beyond the existing comment. A reconstructed Normal `ci_95` from `mean ± 1.96·se` will be slightly shifted from the paper's actual QI for proximal/mid-belly — acceptable, but worth being aware of.

### Quality-score recomputation (QUALITY_RUBRIC.md v1.0 weights)

| Dimension | Weight | Module score | Contribution |
|---|---|---|---|
| Study design | 0.20 | 0.85 | 0.1700 |
| Sample size | 0.15 | 0.85 | 0.1275 |
| Measurement quality | 0.20 | 0.85 | 0.1700 |
| Methodological rigor | 0.15 | 0.95 | 0.1425 |
| Reporting transparency | 0.10 | 0.95 | 0.0950 |
| Risk of bias | 0.10 | 0.85 | 0.0850 |
| Population specificity | 0.10 | 0.85 | 0.0850 |
| **Weighted average** | 1.00 | | **0.8750** |

Module states `QUALITY = 0.88`. **0.875 rounds to 0.88 — arithmetic is correct** and within the rubric's stated "acceptable variance" tolerance.

**However, several per-dimension scores are not well-defended by the rubric:**

- **Study design 0.85** — overstated. Rubric: 0.8 = "meta-analysis of RCTs with pre-registered protocol"; 0.7 = "meta-analysis of mixed designs (RCT + non-randomized intervention)". The rubric also says to "score based on the *worst* design tier of included studies." The included studies are RCTs *or* within-subject randomized designs; the preprint grades them poor-to-fair on SMART-LD (mean 11±2, six "poor", six "fair"). 0.85 is above even the pre-registered-RCT-meta-analysis tier. **Rubric-consistent value is ~0.75–0.80, not 0.85.**
- **Sample size 0.85** — **not defensible.** The rubric's meta-analysis column scores by *total unique participants* (0.85 ≈ 300–499 pooled). The module sets the score using study *count* logic ("12 studies; n not pooled but each study contributes"). The preprint shows the studies are small (e.g. Stasinaki n=10) and there are 22 intervention arms total — pooled participants are plausibly ~150–300, which the rubric would score 0.7–0.8. The 0.85 is not anchored to the rubric's actual scale and should be revisited (likely **0.7–0.8**).
- **Methodological rigor 0.95** — defensible: pre-registered on OSF, Bayesian with multiple prior specifications and sensitivity analyses, code on GitHub. Rubric 1.0/0.9 territory; 0.95 is fine.
- **Reporting transparency 0.95** — defensible: full data + code on OSF/GitHub, full QIs. Rubric 1.0 = "Raw data + analysis code on OSF/GitHub". 0.95 is if anything slightly conservative.
- **Risk of bias 0.85** — defensible per rubric's explicit guidance (Schoenfeld on Tonal advisory board, Steele does fitness-industry consulting; methods sound; no funding; rubric says don't go below 0.6 for industry ties alone, 0.8 = "minor conflicts").
- **Population 0.85** — borderline generous given the training-status skew (see below); 0.7–0.8 would be more honest.

**Net:** the *weighted average arithmetic* is correct, but the **inputs lean optimistic on three dimensions** (study design, sample size, population). A stricter rubric-consistent re-score lands closer to **~0.80–0.83**, not 0.88. This is a MINOR issue (consistent with how QUALITY_RUBRIC.md itself found 0.03–0.05 over-scoring in other modules) but should be corrected for consistency with the rubric's own reconciliation precedent.

---

## The `n` semantics issue (dedicated note)

`EffectEstimate.n` is documented in `shared.py` as **"total participants"**. The module sets `n=12` with the inline comment "studies in the meta-analysis." **This is a semantic mismatch and it has real downstream consequences.**

`n` is consumed in two places in `shared.py`:

1. **`best_applicable()`** ranks estimates by `app * quality_score * sqrt(n)`. With `n=12`, `sqrt(n)=3.46`. If `n` were instead the true pooled participant count (the preprint implies on the order of ~150–300 across 22 arms), `sqrt(n)` would be ~12–17 — a **3–5× difference** in the power term. Encoding study count instead of participants therefore **systematically under-weights this prior** whenever it competes against participant-count-encoded estimates in `best_applicable`. If other modules in the registry encode `n` as participants (the documented contract), this prior loses ranking contests it should sometimes win, purely because of an inconsistent unit.

2. **`combine_inverse_variance()`** reports pooled `n = sum(e.n for e in estimates)`. Pooling this estimate with others would add "12" (studies) to a running total of participants — producing a **meaningless mixed-unit pooled-n**. The pooled SE is unaffected (it uses `precision`, not `n`), so estimates are not corrupted, but any pooled-n surfaced to a user or logged for reporting would be wrong.

**Is it "correct/honest"?** It is honest in intent (the comment says plainly what 12 means) but **incorrect against the dataclass contract** and **not honest about the consequences**. A reader of `best_applicable`'s scoring would assume `n` is participants, as the field doc says.

**Recommended fix (in order of preference):**
- **Best:** put the true pooled unique-participant count in `n`. This requires reading the published full text or the OSF supplement (`https://osf.io/c2657/`, study summary table `https://osf.io/zq2cr`) to total participants across the 12 meta-analyzed studies. I could not access that full text, so I cannot supply the number — but it is obtainable from the OSF data and should be used.
- **Acceptable interim:** keep `n` as participants-estimate with a conservative lower bound and a note; do NOT leave it as study count.
- **If study count must be retained:** that is a `shared.py`-level change — add a separate `n_studies` field to `EffectEstimate` and have `best_applicable`/pooled-n use `n` (participants) only. Encoding study count into a field defined as participants is the wrong place to solve it.

This is the single most important finding of the audit. It does not corrupt the effect sizes, but it silently biases estimate *selection*.

---

## Concerns & discrepancies

1. **`n=12` is study count, not participants** — see dedicated note above. Most important issue.

2. **Quality sub-scores lean optimistic** — study design (0.85), sample size (0.85), and population (0.85) are above what QUALITY_RUBRIC.md v1.0 would produce. A rubric-consistent re-score is ~0.80–0.83, not 0.88. The arithmetic from the stated sub-scores is correct; the sub-scores themselves are the issue. Sample size 0.85 in particular is scored on study-count reasoning while the rubric's meta-analysis scale is explicitly total participants.

3. **`training_status="mixed"` overstates trained-applicability** — 11 of 12 meta-analyzed studies used untrained participants; only Zabaleta-Korta 2023 used (recreationally) trained women. "Mixed" is literally accurate but `applicability_to()` will treat a trained user's mismatch against "mixed" as only a ×0.85 penalty, when the evidence base is almost entirely untrained and arguably warrants closer to the ×0.5 "genuinely different population" treatment. Consider `training_status="untrained"` with a note, or keep "mixed" but document the 11:1 skew prominently. The preprint itself flags this: "only one study … on trained participants has been published … in a peer-reviewed journal to date."

4. **`age_range=(18, 35)` is inferred, not stated** — the paper says "young adults"; the preprint's actual study mean ages span 18.8–27.2 years. The encoded upper bound of 35 is wider than the data supports. Not wrong as a soft applicability envelope, but it is not a paper figure and the module presents it without that caveat. Consider `(18, 30)` or a note.

5. **"trivial" framing — is it the paper's own word?** YES, defensible. The published abstract describes "trivial hypertrophic effects" and concludes "RT at both longer and shorter mean muscle lengths produces similar hypertrophic effects," and the paper used ROPE/equivalence testing (smallest effect size of interest SMD ±0.1, lnRR ±3%) with "high" posterior mass inside the ROPE across all sites. So "trivial regional effects" is a fair, paper-grounded summary, and the module's claim that the paper used equivalence testing is correct. **Caveat:** the distal site is the weakest case for "trivial" — the preprint's full ROPE breakdown shows only ~18.6% (SMD) / ~33.7% (lnRR) of the distal posterior inside the ROPE, i.e. the *majority* of the distal posterior is *outside* the practical-equivalence zone. The module's distal note ("trivial … largest of the three … slight trend toward distal favoring, but uncertain") handles this honestly. Good.

6. **Conceptual Varovic-vs-Maeo framing is sound** — Varovic's research question, verified from the published abstract and the preprint introduction, is indeed regional/site-specific hypertrophy *within* a muscle (proximal/mid-belly/distal). Maeo 2021/2023 (which Varovic *excluded* from this meta-analysis precisely because they "did not assess regional changes") concern whole-muscle/whole-head differences between exercises. The module's sharp distinction is accurate and is, if anything, reinforced by the fact that Varovic's own authors excluded the Maeo studies for being a different question. The docstring's "different questions with different answers" is fair.

7. **GUIDANCE_FOR_OPTIMIZER — mostly faithful, one mild overreach.** The core guidance ("do not assign region-level emphasis coefficients within a muscle from training-length theory; the regional advantage is trivial, SMDs 0.05–0.09, CIs mostly cross zero") is a faithful, well-calibrated reading of the published paper. The second paragraph — that emphasis coefficients *should* be assigned for biarticular sub-muscles (triceps long head, hamstring biarticular heads) — is **reasonable but goes beyond what Varovic 2025 establishes**; Varovic neither tested nor supports that claim (it is a separate-exercise / whole-head question, the Maeo domain). The guidance text does flag it as "a different claim," which is honest, but a strict auditor would note this paragraph is not *derived from* Varovic and should be attributed to other sources, not this module's paper. The third paragraph (respond with uncertainty about "lower lats"/"upper chest") is appropriately hedged. **Verdict: faithful with one paragraph that is adjacent inference rather than Varovic-derived — acceptable given it is labelled as a heuristic, but tighten the attribution.**

8. **Full published text not inspected** — Methods, Results tables and Discussion of the *published* version are paywalled. All full-text-dependent specifics (exact pooled participant N, exact ROPE percentages in the published version, whether the published Discussion changed the preprint's "exploratory" hedge) are verified only against the preprint and are marked UNVERIFIED where the published wording could differ. The six headline numbers and the conclusion sentence ARE verified from the published abstract via four independent sources.

---

## Recommendations (concrete fixes to the module)

1. **Fix the `n` field.** Replace `n=12` with the true pooled unique-participant count from the meta-analysis (obtainable from the OSF data at https://osf.io/c2657/ / study table https://osf.io/zq2cr). If study count must be preserved as information, add a `n_studies` field to `EffectEstimate` in `shared.py` rather than overloading `n`. As-is, `best_applicable`'s `sqrt(n)` weighting is biased and `combine_inverse_variance`'s pooled-n is unit-inconsistent. **Highest priority.**

2. **Re-score `QUALITY` against QUALITY_RUBRIC.md v1.0.** Lower study design to ~0.75–0.80 (rubric tier for meta-analysis of mixed/within-subject designs; SMART-LD grades poor-to-fair), lower sample size to ~0.7–0.8 (rubric's meta-analysis column is total participants, and the included studies are small), and consider lowering population to ~0.75–0.80. Expected rubric-consistent result ≈ **0.80–0.83**. Update the per-dimension justification comments accordingly. (Consistent with the precedent in QUALITY_RUBRIC.md's "Reconciliation with current code" section.)

3. **Reconsider `training_status`.** Either set it to `"untrained"` (11/12 of the evidence base) or keep `"mixed"` but add a prominent note that the data are ~92% untrained, so applicability to trained users is weaker than the ×0.85 "mixed" penalty implies.

4. **Soften / annotate `age_range`.** The paper says "young adults"; underlying study mean ages are ~18.8–27.2. Consider `(18, 30)` or add a comment that 35 is a deliberately generous applicability envelope, not a paper figure.

5. **Add a preprint-vs-published note.** State explicitly that the SportRxiv preprint (DOI 10.51224/SRXIV.461) reports larger point estimates (SMD 0.10/0.15/0.20) and a more "exploratory" conclusion, and that the module deliberately uses the peer-reviewed published values. This pre-empts confusion for any future re-auditor.

6. **Tighten `measurement` comment.** Change "regional muscle thickness via ultrasound" to acknowledge the paper's inclusion criteria allowed ultrasound, CT, or MRI (ultrasound predominant).

7. **Tighten GUIDANCE_FOR_OPTIMIZER attribution.** The biarticular-sub-muscle paragraph is reasonable but is not established by Varovic 2025; mark it explicitly as cross-referencing other evidence (e.g. Maeo-type data) rather than reading as a Varovic implication.

8. **(Optional) Note the symmetric-posterior approximation's effect.** The encoded means (0.05, 0.07) sit slightly above their QI midpoints; reconstructing `ci_95` via Normal `mean ± 1.96·se` shifts the interval ~0.005 from the paper's QI for proximal/mid-belly. Immaterial, but a one-line comment would make it fully transparent.
