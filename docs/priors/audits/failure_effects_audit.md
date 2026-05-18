# Literature Audit — `failure_effects.py` (training-to-failure priors)

**Auditor:** Independent literature auditor (re-read papers from scratch; encoding NOT trusted)
**Module audited:** `priors-handoff/app/priors/failure_effects.py`
**Supporting context:** `docs/priors/QUALITY_RUBRIC.md`, `app/priors/shared.py`
**Date:** 2026-05-17

---

## Sources accessed

### Paper 1 — Vieira et al. 2021 (J Strength Cond Res), DOI 10.1519/JSC.0000000000003936

| Source | URL | Accessed? |
|---|---|---|
| PubMed record (abstract) | https://pubmed.ncbi.nlm.nih.gov/33555822/ | YES — abstract + effect sizes |
| Journal full text (LWW) | https://journals.lww.com/nsca-jscr/fulltext/2021/04000/effects_of_resistance_training_performed_to.39.aspx | NO — HTTP 402 paywall |
| ResearchGate | publication/349141660 | NO — HTTP 403 |
| Semantic Scholar | paper page | NO — page body did not render |

**Verifiable:** headline SMDs and p-values for hypertrophy, strength, power; volume-equated/non-equated framing.
**NOT verifiable from source:** exact CI for the 0.75 SMD (abstract reports no CI), exact volume-equated subgroup effect size, exact total participant count, per-outcome study counts, I².

### Paper 2 — Grgic et al. 2021 (J Sport Health Sci), DOI 10.1016/j.jshs.2021.01.007

| Source | URL | Accessed? |
|---|---|---|
| PMC full text (open access) | https://pmc.ncbi.nlm.nih.gov/articles/PMC9068575/ | YES — full text, results, included-study list |
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/33497853/ | YES (via search) |

**Verifiable:** all four encoded estimates, study counts, participant counts, subgroup composition. This is the best-verified paper of the three.

### Paper 3 — "Robinson et al. 2022", DOI 10.1007/s40279-022-01784-y (Sports Medicine)

**This is the central source-attribution problem of the module — see below.**

| Source | URL | Accessed? |
|---|---|---|
| Springer page for DOI .../s40279-022-01784-y | https://link.springer.com/article/10.1007/s40279-022-01784-y | Partial — redirect to IdP; metadata obtained via search |
| PMC full text for that DOI | https://pmc.ncbi.nlm.nih.gov/articles/PMC9935748/ | YES — full text, abstract, included studies, sample sizes, heterogeneity |
| PubMed record for that DOI | https://pubmed.ncbi.nlm.nih.gov/36334240/ | YES — abstract verbatim |
| Actual Robinson ZP et al. dose-response paper | https://pubmed.ncbi.nlm.nih.gov/38970765/ (DOI 10.1007/s40279-024-02069-2) | YES — metadata + abstract |

**Finding:** DOI `10.1007/s40279-022-01784-y` does **not** belong to a paper by Robinson. It is **Refalo MC, Helms ER, Trexler ET, Hamilton DL, Fyfe JJ. "Influence of Resistance Training Proximity-to-Failure on Skeletal Muscle Hypertrophy: A Systematic Review with Meta-analysis." Sports Medicine 2023;53:649–665.** The numbers encoded in the module (set-failure ES 0.19, momentary-failure ES 0.12) are the Refalo 2023 numbers and match it exactly — so the *DOI and the numbers are mutually consistent*, but the *author name "Robinson", year "2022", and the title given in the audit brief* are wrong for that DOI.

The genuine "Robinson ZP et al." paper — "Exploring the Dose–Response Relationship Between Estimated Resistance Training Proximity to Failure, Strength Gain, and Muscle Hypertrophy: A Series of Meta-Regressions" (the exact title in the audit brief) — is **Robinson ZP, Pelland JC, Remmert JF, Refalo MC, Jukic I, Steele J, Zourdos MC. Sports Medicine 2024. DOI 10.1007/s40279-024-02069-2.** It is a meta-*regression* of RIR slopes, not a categorical set-failure/momentary-failure SMD analysis, and it does not report the 0.19 / 0.12 effect sizes the module uses.

---

## Verdict

**MATERIAL DISCREPANCIES.**

The point estimates and confidence intervals are, to the extent verifiable, faithfully transcribed — every encoded mean and CI that could be checked against an accessible abstract or full text matched the paper. The SE recovery math is arithmetically correct. However, three material problems prevent an ACCURATE verdict:

1. **Wrong citation for two of eight estimates.** `CITATION_ROBINSON` (`authors="Robinson et al."`, `year=2021`/`2022`) is attached to DOI `10.1007/s40279-022-01784-y`, which is actually **Refalo et al. 2023**. The module names the wrong authors, the wrong year, and (per the docstring "13 studies / 15 studies / Robinson 2022") effectively misidentifies the paper. A reader trusting the module would cite a non-existent Robinson 2022 set-failure SMD paper.
2. **Several sample sizes are materially wrong, not just "approximate."** Grgic's resistance-trained hypertrophy subgroup is **2 studies (~39 participants)**, not the encoded `n=140`. Grgic's hypertrophy analyses rest on 7 studies / 219 participants, not 15 / 312 (312/15 is the *strength* analysis). The Refalo set-failure and momentary-failure n's are also off.
3. **The volume-equation framing is half-right.** Vieira's non-equated framing is correct and well-supported. But the module's claim that Grgic and Refalo estimates are "volume-equated" is wrong for Refalo: Refalo 2023 explicitly found volume load had *no moderating effect* and did not restrict to volume-equated studies — its 0.19 pools equated and non-equated studies alike. The `hypertrophy_estimates_volume_equated()` helper therefore mislabels two of its four members.

The qualitative conclusion the module draws (failure offers a small, uncertain hypertrophy benefit at fixed volume; a small strength cost; high uncertainty) survives all of this. The discrepancies are in provenance, sample sizes, and framing precision, not in the headline direction. But for a "priors" layer whose entire value is traceability to literature, mis-citing a paper is material.

---

## Value-by-value verification (all 8 estimates)

| # | Encoded estimate | Encoded value | Paper value (source) | Match? | Notes |
|---|---|---|---|---|---|
| 1 | `VIEIRA_HYPERTROPHY_NONEQ_VOLUME` mean | 0.75 | SMD 0.75, p=0.005 (Vieira 2021 abstract, PubMed 33555822) | YES | Abstract: "RTF showed a greater increase in muscle hypertrophy than RTNF (SMD: 0.75; p = 0.005)". No CI in abstract. |
| 2 | `GRGIC_HYPERTROPHY_OVERALL` mean / CI | 0.22 / (−0.11, 0.55) | ES 0.22, 95% CI −0.11–0.55, p=0.152 (Grgic 2021, PMC9068575) | YES | Exact match. |
| 3 | `GRGIC_HYPERTROPHY_TRAINED` mean / CI | 0.15 / (0.03, 0.26) | ES 0.15, 95% CI 0.03–0.26, p=0.039 (Grgic 2021, PMC9068575) | YES (values) | Mean/CI exact. **But n and subgroup status wrong — see below.** |
| 4 | `ROBINSON_HYPERTROPHY_SET_FAILURE` mean / CI | 0.19 / (0.00, 0.37) | ES 0.19, 95% CI 0.00–0.37, p=0.045 (Refalo 2023, PubMed 36334240) | YES (values) | **Wrong attribution: this is Refalo 2023, not Robinson.** Also pools 9 studies, equated + non-equated. |
| 5 | `ROBINSON_HYPERTROPHY_MOMENTARY_FAILURE` mean / CI | 0.12 / (−0.13, 0.37) | ES 0.12, 95% CI −0.13–0.37, p=0.343 (Refalo 2023, PMC9935748) | YES (values) | **Wrong attribution (Refalo 2023).** 5 studies, 170 participants. |
| 6 | `VIEIRA_STRENGTH_OVERALL` mean | −0.08 | SMD −0.08, p=0.642 (Vieira 2021 abstract) | YES | Abstract confirms overall strength SMD −0.08, p=0.642. |
| 7 | `GRGIC_STRENGTH_OVERALL` mean / CI | −0.09 / (−0.22, 0.05) | ES −0.09, 95% CI −0.22–0.05, p=0.198 (Grgic 2021, PMC9068575) | YES | Exact match. |
| 8 | `GRGIC_STRENGTH_NONEQ_VOLUME` mean / CI | −0.32 / (−0.57, −0.07) | ES −0.32, 95% CI −0.57–−0.07, p=0.025 (Grgic 2021, PMC9068575) | YES | Exact match. Grgic non-volume-equated strength subgroup; module framing correct. |

**Net:** All 8 point estimates and all 6 CIs that have a paper-reported CI match the literature. Estimates 4 and 5 are correctly transcribed *from the paper at that DOI* but are attributed to the wrong author/year.

### Failure-definition and volume-equation framing per estimate

- **#1 Vieira non-equated** — framing CORRECT. Vieira's headline 0.75 is the non-volume-equated overall pooled estimate; the abstract explicitly states the hypertrophy advantage disappears with equalized volumes.
- **#3 Grgic trained subgroup** — framing PARTIALLY CORRECT. It is genuinely a resistance-trained subgroup with a significant effect. But it is built on only **2 studies** (Karsten 2021, Pareja-Blanco 2017). Calling it `well_trained` population with `n=140` overstates it dramatically.
- **#4 "set failure"** vs **#5 "momentary failure"** — the failure-definition distinction is CORRECT and is genuinely Refalo 2023's Theme B (set failure / other definitions, 9 studies) vs Theme A (momentary muscular failure, 5 studies). The module's note that the stricter definition shows a weaker effect (0.12 < 0.19) is faithful to the paper. But describing these as "volume-equated" is wrong — Refalo found *no* moderating effect of volume load and did not equate.
- **#8 Grgic non-equated strength** — framing CORRECT. Grgic's non-volume-equated strength subgroup favored non-failure (−0.32); the module's note that this captures the fatigue cost when groups do their own volume is accurate.

---

## Math checks

### SE recovery — CI method `(upper − lower) / (2 × 1.96)`

| Estimate | Encoded computation | Recomputed SE | In module? |
|---|---|---|---|
| Grgic hypertrophy overall | `_se_from_ci(-0.11, 0.55)` | 0.1684 | correct |
| Grgic hypertrophy trained | `_se_from_ci(0.03, 0.26)` | 0.0587 | correct |
| Grgic strength overall | `_se_from_ci(-0.22, 0.05)` | 0.0689 | correct |
| Grgic strength non-eq | `_se_from_ci(-0.57, -0.07)` | 0.1276 | correct |
| Refalo set failure | `_se_from_ci(0.00, 0.37)` | 0.0944 | correct |
| Refalo momentary failure | `_se_from_ci(-0.13, 0.37)` | 0.1276 | correct |

All CI-based SE recoveries are arithmetically correct. **Caveat:** these CIs are from random-effects models; treating `(U−L)/(2×1.96)` as a Normal SE is a standard and acceptable approximation, and `EffectEstimate.ci_95` will faithfully reproduce the source CI. No issue.

### SE recovery — p-value method

| Estimate | Encoded | z used | Correct two-tailed z | Verdict |
|---|---|---|---|---|
| Vieira hypertrophy | SE = 0.75 / 2.81 = **0.2669** | 2.81 | z(p=0.005) = **2.807** | z is correct (2.81 rounds 2.807). SE ≈ 0.267. |
| Vieira strength | SE = 0.08 / 0.46 = **0.1739** | 0.46 | z(p=0.642) = **0.4649** | z is correct (0.46 ≈ 0.465). SE ≈ 0.174. |

Cross-check: z=2.81 implies two-tailed p=0.00495 (≈0.005 ✓); z=0.46 implies p=0.6455 (≈0.642 ✓). **Both z-values are right.**

**Reliability flag on the p-value method.** The arithmetic is sound, but two reliability concerns remain:

1. *p=0.005 is likely rounded/thresholded.* If the true p were anywhere in 0.004–0.006, z ranges 2.73–2.88 and SE ranges 0.260–0.275 — about ±3%. Tolerable.
2. *The Vieira strength SE is fragile.* Recovering SE from a large, non-significant p (0.642) divides a tiny effect (0.08) by a tiny, imprecisely-reported z (0.46). A reported p of 0.60 vs 0.68 swings z between 0.41 and 0.52 and SE between 0.154 and 0.195 — a ±12% swing. More importantly, near p≈0.64 the p-value carries almost no information about precision; the SE is essentially being invented. Vieira's strength SE should be treated as low-confidence. QUALITY_RUBRIC.md §"Reporting transparency" already says reconstructed-from-p reporting "shouldn't score above 0.6" — Vieira's 0.50 on that dimension honors this, but the *SE itself* should additionally carry an uncertainty caveat or be widened. The inverse-variance pooler in `shared.py` will weight this estimate by `1/SE²` and a too-small SE would over-weight it.

### Quality-score recomputation (rubric weights: design .20, n .15, measurement .20, rigor .15, reporting .10, bias .10, population .10)

| Paper | Per-dimension (from module comments) | Weighted base | Modifier | Final | Module value | Match? |
|---|---|---|---|---|---|---|
| Vieira non-eq hypertrophy | 0.70/0.80/0.75/0.70/0.50/0.85/0.85 | **0.735** | ×0.7 | **0.5145** | `QUALITY_VIEIRA_NONEQ = 0.51` | YES (0.5145→0.51) |
| Vieira strength | same dimensions, no modifier | **0.735** | none | **0.735** | `QUALITY_VIEIRA_STRENGTH = 0.74` | YES (within rounding; rubric §worked-example says 0.74) |
| Grgic overall | 0.75/0.80/0.80/0.85/0.85/0.85/0.85 | **0.8125** | none | **0.8125** | `QUALITY_GRGIC_OVERALL = 0.81` | YES (0.8125→0.81) |
| Grgic trained subgroup | same dimensions | 0.8125 | ×0.85 | **0.6906** | `QUALITY_GRGIC_SUBGROUP = 0.69` | YES |
| Robinson/Refalo | 0.85/0.80/0.90/0.90/0.90/0.85/0.85 | **0.865** | none | **0.865** | `QUALITY_ROBINSON = 0.87` | YES (0.865→0.87) |

**Modifier check on `GRGIC_STRENGTH_NONEQ_VOLUME`:** module applies `QUALITY_GRGIC_OVERALL * 0.8 = 0.81 × 0.8 = 0.648`. The rubric's modifier table has no ×0.8 entry — the "addresses a different question" modifier is ×0.7 and "subgroup as primary" is ×0.85. The code's 0.8 is an undocumented value sitting between the two. Arithmetic is correct (0.648) but the multiplier is not rubric-sanctioned. Either use ×0.7 (→0.567), ×0.85 (→0.689), or document why 0.8 was chosen. **Minor, but it violates "document every deviation."**

All five quality scores reconcile with the rubric's worked examples (0.51 / 0.74 / 0.81 / 0.69 / 0.87). The quality-score block is the cleanest part of the module.

---

## The volume-equation claim (the module's load-bearing assertion)

The module's central framing (docstring lines 14–37) is:

> Vieira's 0.75 is non-volume-equated and went null when restricted to volume-equated studies; Grgic and Robinson are "(mostly) volume-equated"; therefore the volume-equated comparison is the apples-to-apples one for the optimizer.

**Verified true:**
- Vieira 2021's 0.75 is the **non-volume-equated overall** pooled hypertrophy estimate. The abstract states the hypertrophy advantage "disappeared with equalized volumes" / "no difference was observed considering equalized RT volumes." ✓
- Vieira's strength and power non-equated subgroups favored non-failure (strength non-eq SMD −0.34, p=0.048; power non-eq −0.61, p=0.025), consistent with the module's strength narrative. ✓
- Grgic 2021 separates volume-equated from non-equated cleanly. Its non-volume-equated **strength** subgroup favored non-failure (−0.32), and its volume-equated strength subgroup was null (ES 0.01, 95% CI −0.12–0.15, p=0.860 — per PMC full text). ✓ The module's `GRGIC_STRENGTH_NONEQ_VOLUME` is correctly the non-equated one.

**Challenged / incorrect:**
- **Refalo 2023 is not a volume-equated analysis.** Refalo explicitly tested volume load as a moderator and found **no moderating effect**; the 0.19 set-failure and 0.12 momentary-failure estimates pool equated and non-equated studies together. Calling them "volume-equated (mostly)" in the docstring and including both in `hypertrophy_estimates_volume_equated()` is a misframing. The correct statement is: Refalo found the failure effect to be small *regardless of* volume equating — which still supports the module's optimizer conclusion, but for a different reason than stated.
- **Grgic's overall hypertrophy estimate (0.22) is not described by Grgic as volume-equated either.** The 0.22 is the overall pooled hypertrophy effect across all 7 hypertrophy studies. Grgic's volume-equated *vs* non-equated split is reported prominently for **strength**, not given the same clean treatment for hypertrophy in the accessible abstract/results. The comment `# Grgic 2021 — overall (volume-equated, mostly)` overstates this.
- The docstring asserts "The 0.75 estimate dropped to null when Vieira restricted to volume-equated studies." This is directionally supported by the abstract ("no difference ... considering equalized RT volumes") but the **exact volume-equated hypertrophy effect size is UNVERIFIED** — it is behind the JSCR paywall and not in the abstract. The module itself concedes this (note on `VIEIRA_HYPERTROPHY_NONEQ_VOLUME`: "exact effect size not extracted"). Acceptable as flagged, but mark it UNVERIFIED rather than asserted.

**Bottom line:** the Vieira half of the central claim is solid. The "Grgic and Robinson are volume-equated" half is not — neither Grgic's 0.22 nor either Refalo estimate is a volume-equated-only analysis. The optimizer-facing conclusion (small failure benefit at fixed volume) is not invalidated, because the modern view (Refalo, the real Robinson 2024 meta-regression) is that volume equating does not change the small-failure-effect picture much. But the helper function name `hypertrophy_estimates_volume_equated()` makes a promise the contents do not keep.

---

## Sample-size verification

| Estimate | Encoded n | Paper-reported n | Verdict |
|---|---|---|---|
| Vieira (both outcomes) | 240 | "~240" plausible but **UNVERIFIED** — abstract/PubMed give no total; full text paywalled | UNVERIFIED. 13 studies confirmed. Module flags "approx". |
| Grgic hypertrophy overall | 312 | **219** participants across **7** hypertrophy studies (PMC9068575) | WRONG. 312/15 is the *strength* sample. Hypertrophy is 7 studies / 219. |
| Grgic hypertrophy trained subgroup | 140 | **2 studies** (Karsten 2021, Pareja-Blanco 2017) ≈ **~39 participants** | MATERIALLY WRONG. Encoded n is ~3.5× too large. |
| Grgic strength overall | 312 | **394** participants across **15** strength studies (PMC9068575) | WRONG (under-counts). 15 studies confirmed; n is 394, not 312. |
| Grgic strength non-eq subgroup | 180 | Not separately reported in accessible text | UNVERIFIED — but given the overall is 15 studies/394, a non-equated subgroup of 180 is plausible. |
| Refalo set failure | 300 | **9 studies, ~284 participants** (10+25+89+32+14+41+18+28+27) | CLOSE but slightly high; also 9 studies, not "15". |
| Refalo momentary failure | 200 | **5 studies, 170 participants** (Refalo Theme A, PMC9935748) | WRONG — 170, not 200. |

Module-wide: the docstring says "Grgic 15 studies" and "Robinson 15 studies." Grgic's 15 is its strength dataset; its hypertrophy dataset is 7. Refalo's review is 15 studies *total* but the set-failure and momentary-failure sub-analyses are 9 and 5 respectively — and those are the analyses the estimates come from. Using "15" and "300" for the set-failure estimate conflates the whole-review count with the sub-analysis count.

These n's feed `EffectEstimate.precision` only indirectly (precision uses SE, not n), but `n` is used in `best_applicable()` as `sqrt(n)` and in `combine_inverse_variance()` for the pooled total. An inflated Grgic-subgroup n=140 makes that 2-study subgroup look far more authoritative in `best_applicable` ranking than 2 studies warrant. **This is the most consequential numeric error in the module.**

---

## Concerns & discrepancies (ranked)

1. **[MATERIAL] Mis-citation of Refalo 2023 as "Robinson."** `CITATION_ROBINSON` carries `authors="Robinson et al."`, `year=2021` (the dataclass) / "2022" (docstring), on DOI `10.1007/s40279-022-01784-y`. That DOI is Refalo MC, Helms ER, Trexler ET, Hamilton DL, Fyfe JJ, *Sports Medicine* 2023;53:649–665. The genuine Robinson ZP et al. paper (the dose-response meta-regression named in the brief) is a *different* 2024 paper, DOI 10.1007/s40279-024-02069-2, and reports RIR slopes, not the 0.19/0.12 SMDs. Two of eight estimates are attributed to the wrong authors and year.

2. **[MATERIAL] Grgic trained-subgroup n=140 vs actual ~39 (2 studies).** Overstates a 2-study post-hoc subgroup by ~3.5×, inflating its weight in `best_applicable()`.

3. **[MODERATE] Grgic hypertrophy n mislabeled.** Encoded 312 is Grgic's strength sample (15 studies); the hypertrophy analyses are 7 studies / 219 participants. Grgic strength n should be 394, not 312.

4. **[MODERATE] "Volume-equated" mislabeling of Refalo estimates.** Refalo found no volume-load moderation; its 0.19/0.12 are not volume-equated-only analyses. `hypertrophy_estimates_volume_equated()` returning these is inaccurate, though the optimizer conclusion is unaffected.

5. **[MODERATE] Refalo momentary-failure n=200 vs actual 170; set-failure n "300/15 studies" vs actual ~284/9 studies.**

6. **[MINOR] Undocumented ×0.8 modifier** on `GRGIC_STRENGTH_NONEQ_VOLUME` quality. Not in the rubric's modifier table (which has ×0.7 and ×0.85). Arithmetic correct (0.648); the multiplier is a silent deviation.

7. **[MINOR] Vieira strength SE recovered from p=0.642 is statistically fragile.** Near a large p-value, the SE is essentially unidentified. The encoded 0.174 is arithmetically right but should carry a low-confidence caveat; it currently feeds inverse-variance pooling at face value.

8. **[MINOR] Vieira n=240 and the volume-equated null effect size are both UNVERIFIED** (JSCR full text paywalled). The module flags both as approximate/not-extracted — acceptable, but they should be explicitly marked UNVERIFIED, not silently trusted.

9. **[INFO] Overlap estimates — see below.**

### Overlap estimate assessment (`OVERLAP_SE_INFLATION = 1.35`)

The module states Vieira↔Grgic ~40%, Grgic↔Refalo("Robinson") ~50%, Vieira↔Refalo ~30%, all as judgment calls "without full reference-list comparison." A partial check is now possible:

- **Grgic's 15 included studies** (verified from PMC9068575): Drinkwater 2005, Fisher 2016, Folland 2002, Izquierdo 2006, Karsten 2021, Kraemer 1997, Lacerda 2020, Lasevicius 2019, Martorelli 2017, Nóbrega 2018, Pareja-Blanco 2017, Rooney 1994, Sampson 2016, Sanborn 2000, Vieira 2019.
- **Refalo's set-failure + momentary-failure studies** (verified from PMC9935748): Lacerda 2020, Lasevicius 2019, Martorelli 2017, Nóbrega 2018, Santanielo 2020, Bergamasco 2020, Karsten 2021, Sampson 2016, Terada 2021.
- **Overlap Grgic↔Refalo:** Lacerda, Lasevicius, Martorelli, Nóbrega, Karsten, Sampson = **6 of Refalo's 9 set-failure studies (~67%)**, or 6 of 15 of Grgic's. The module's "~50%" is in the right ballpark and arguably slightly conservative on the Refalo side. Reasonable.
- Vieira's included-study list could not be retrieved (paywall), so the ~40% and ~30% figures remain genuinely unverifiable. They are plausible given all three papers cover the same ~2017–2021 RT-to-failure literature and the same canonical studies (Pareja-Blanco, Martorelli, Sampson, etc.) recur everywhere.

`OVERLAP_SE_INFLATION = 1.35` as a single blanket factor for "pooling all three" is a defensible rough adjustment given confirmed substantial overlap. It is a judgment call and the module honestly labels it as such. **No change required**, but note the genuine Robinson 2024 dose-response paper (if ever added) shares even more studies with all three and the 1.35 factor would need revisiting.

---

## Recommendations (concrete)

1. **Fix the citation.** Rename `CITATION_ROBINSON` → `CITATION_REFALO` with `authors="Refalo et al."`, `year=2023`, `journal="Sports Medicine"`, DOI unchanged (`10.1007/s40279-022-01784-y` is correct for Refalo). Rename `ROBINSON_HYPERTROPHY_SET_FAILURE` / `ROBINSON_HYPERTROPHY_MOMENTARY_FAILURE` and `QUALITY_ROBINSON` accordingly. Update the module docstring lines 6, 21, 23, 31, 202, 215 and the `# Grgic-equivalent paper ... (the Sci Direct one)` comment which is also confused. If the team specifically wants the genuine Robinson ZP et al. dose-response paper, that is a *separate* paper (DOI 10.1007/s40279-024-02069-2, 2024) and would need its own estimates extracted — it reports RIR slopes, not categorical SMDs.

2. **Fix sample sizes.**
   - `GRGIC_HYPERTROPHY_OVERALL.n`: 312 → **219** (7 studies).
   - `GRGIC_HYPERTROPHY_TRAINED.n`: 140 → **~39** (2 studies: Karsten 2021, Pareja-Blanco 2017). This is the highest-priority fix — it materially affects `best_applicable()` ranking.
   - `GRGIC_STRENGTH_OVERALL.n`: 312 → **394** (15 studies).
   - `ROBINSON_HYPERTROPHY_MOMENTARY_FAILURE.n` (→ Refalo): 200 → **170** (5 studies).
   - `ROBINSON_HYPERTROPHY_SET_FAILURE.n` (→ Refalo): 300 → **~284** (9 studies). Update docstring "15 studies" to note the set-failure analysis pools 9.

3. **Correct the volume-equation framing.** Change the comment on `GRGIC_HYPERTROPHY_OVERALL` from "volume-equated, mostly" to "overall pooled, equated + non-equated." Change the Refalo estimates' notes to state Refalo found *no moderating effect of volume load* rather than implying they are volume-equated. Rename `hypertrophy_estimates_volume_equated()` to something like `hypertrophy_estimates_fixed_volume_question()` or document explicitly that the Refalo members are "volume-load-insensitive" rather than "volume-equated."

4. **Document or replace the ×0.8 modifier** on `GRGIC_STRENGTH_NONEQ_VOLUME`. Either switch to a rubric value (×0.7 for different-question → 0.567, or ×0.85 → 0.689) or add a one-line justification for 0.8 in the comment, per QUALITY_RUBRIC.md's "document every deviation" rule.

5. **Add an SE-reliability caveat to `VIEIRA_STRENGTH_OVERALL`.** The SE recovered from p=0.642 is statistically near-unidentified. Consider either widening it conservatively or adding a `notes` flag so downstream inverse-variance pooling does not over-trust it. The same applies less severely to the Vieira hypertrophy SE.

6. **Mark UNVERIFIED items explicitly.** Vieira n=240, Vieira per-outcome study split, the volume-equated hypertrophy null effect size, and Grgic's non-equated strength subgroup n=180 could not be confirmed against accessible text. Keep them but label them `# UNVERIFIED — JSCR full text paywalled` rather than `# approx`.

7. **Quality scores need no change** — all five reconcile with the rubric. Optionally bump Vieira strength 0.74→0.735 for exactness, but the rubric itself calls 0.74 "defensible."

8. **Overlap factor** `OVERLAP_SE_INFLATION = 1.35` is acceptable as a labelled judgment call; no change needed. Add a note that if the genuine Robinson 2024 dose-response paper is later added, overlap with all three existing sources is high and the factor should be revisited.

---

*End of audit. Papers re-read from primary sources (PubMed, PMC, Springer) on 2026-05-17. Items marked UNVERIFIED could not be confirmed because the J Strength Cond Res full text is paywalled (HTTP 402) and ResearchGate returned 403.*
