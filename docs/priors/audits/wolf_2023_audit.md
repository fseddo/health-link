# Literature Audit — Wolf et al. 2023 (Partial vs Full ROM Meta-Analysis)

**Module audited:** `priors-handoff/app/priors/wolf_2023.py`
**Paper:** Wolf M, Androulakis-Korakakis P, Fisher J, Schoenfeld B, Steele J. "Partial Vs Full Range of Motion Resistance Training: A Systematic Review and Meta-Analysis." *International Journal of Strength and Conditioning* 2023;3(1). DOI 10.47206/ijsc.v3i1.182.
**Audit date:** 2026-05-17
**Auditor:** Independent literature auditor (re-fetched paper from scratch; encoding NOT trusted)

---

## Sources accessed

| Source | URL | Result |
|---|---|---|
| Journal article landing page (abstract) | https://journal.iusca.org/index.php/Journal/article/view/182 | Accessed — full abstract retrieved |
| Journal full-text PDF | https://journal.iusca.org/index.php/Journal/article/download/182/250/5033 | Accessed — 1.77 MB PDF downloaded; text extracted via pdfminer (68k chars, 22 pp). **Full text including Results, Table 2 GRADE table, Discussion, Funding/Competing Interests read in full.** |
| WebSearch (journal.iusca.org, ResearchGate, Semantic Scholar, SportRxiv) | multiple | Confirmed identity of paper and main-model SMD figure |
| Wolf et al. 2025 lengthened-partials trial (for docstring context check) | https://pubmed.ncbi.nlm.nih.gov/39959841/ ; https://peerj.com/articles/18904/ | Accessed via search snippet — confirmed the trial exists and its conclusion |

I reached the **full text** of the paper under audit. The OSF supplementary materials (https://osf.io/fmvrw/, https://osf.io/j96e7) were referenced in the paper but not separately fetched; all numbers below come from the published article body and Table 2 (GRADE table), which report every estimate the module relies on, so no item is left unverifiable for lack of access.

---

## Verdict: **MATERIAL DISCREPANCIES**

The module's *strength* and *long-length* estimates are accurate, and the SE/quality math is essentially sound. **However, the module's headline "overall" estimate is mis-labelled.** `PARTIAL_VS_FULL_OVERALL` is encoded with `mean=0.04, QI −0.17–0.25` and described in both the docstring and the `notes` as the **"overall partial vs full ROM"** effect. In the paper, `0.04 (95% CI −0.17, 0.25)` is **not** the overall/main-model effect — it is specifically the **"muscle size" outcome sub-group** estimate (Table 2; Results, "Grouped by outcome type"). The paper's actual **main model** (all outcomes, all studies) is **SMD 0.12 (95% CI −0.02, 0.26)**. So the module either (a) mislabels a hypertrophy sub-group estimate as the overall effect, or (b) intends it to be the hypertrophy estimate but names the constant and its notes "OVERALL". Given this is a hypertrophy-focused app, (b) is the likely intent — but then the naming, the docstring line "Overall partial vs full ROM for hypertrophy", and the `notes` string are all wrong and must be fixed. Separately, the long-length sub-group `n=8` is wrong (paper says **6** long-length studies), and the docstring's `n=24` should be `23` for analysed studies. None of the *numeric values themselves* (0.04, −0.28, 0.14, and their intervals) is fabricated — each appears verbatim in the paper — but the **semantic labelling** of the first estimate is materially misleading for a pooling layer.

---

## Value-by-value verification

| Encoded item | Encoded value | Paper value | Match? | Source in paper |
|---|---|---|---|---|
| `PARTIAL_VS_FULL_OVERALL.mean` | 0.04 | 0.04 — but this is the **"muscle size"** outcome sub-group, NOT the overall/main model. Main model = **0.12**. | **NO (mislabelled)** | Results §"Grouped by outcome type": *"for 'muscle size' type outcomes … a trivial SMD (0.04; 95% CI: –0.17, 0.25)"*; Table 2 "Muscle size" row. Main model: Results §"Main Model": *"0.12; 95% CI: –0.02, 0.26"* |
| `PARTIAL_VS_FULL_OVERALL` interval | QI −0.17, 0.25 | −0.17, 0.25 (matches the muscle-size sub-group) | Value matches, label wrong | Table 2 "Muscle size": "(0.17 lower to 0.25 higher)" |
| `PARTIAL_LONG_LENGTH_VS_FULL.mean` | −0.28 | −0.28 | **YES** | Results §"Muscle Length & Muscle Hypertrophy": *"pROM at long muscle lengths … small SMD (–0.28; 95% CI: –0.81, 0.16) in favour of pROM"*; abstract confirms. |
| `PARTIAL_LONG_LENGTH_VS_FULL` interval | CI −0.81, 0.16 | −0.81, 0.16 | **YES** | Same section / abstract. |
| `PARTIAL_LONG_LENGTH_VS_FULL.n` | 8 ("approximate") | **6** long-length studies | **NO** | Results §"Muscle length of partial range of motion training": *"long muscle lengths (6/23)"*; Discussion: *"Six studies exist in this area."* |
| `PARTIAL_VS_FULL_STRENGTH.mean` | 0.14 | 0.14 | **YES — and it IS a strength figure** | Results §"Grouped by outcome type": *"For 'strength' type outcomes … a trivial SMD (0.14; 95% CI: -0.01, 0.29) in favour of fROM"*; Table 2 "Muscle Strength" row: "SMD 0.14 … (0.01 lower to 0.29 higher)". |
| `PARTIAL_VS_FULL_STRENGTH` interval | QI −0.01, 0.29 | −0.01, 0.29 | **YES** | Same. |
| `PARTIAL_VS_FULL_STRENGTH.n` | 24 | Table 2 "Muscle Strength" row: **"24" randomised trials** (311 fROM + 428 pROM patients) | **YES (study count)** — see honesty caveat in Concerns | Table 2. |
| `PARTIAL_VS_FULL_OVERALL.n` | 24 | Main model analysed **23 studies**; 24 studies summarised in Table 1; the muscle-size sub-group itself used only **8 studies** | **NO** (see Concerns) | Results §"Search Results" (24 in Table 1), §"Main Model" ("across 23 studies"), Table 2 "Muscle size" row (8 trials). |
| Docstring "24 studies (Bayesian MA)" | 24 | 24 included in Table 1; **23 analysed** in the main model | Partially — clarify | §"Search Results" and §"Main Model". |
| Docstring "Power SMD 0.19 (0.01, 0.37)" | 0.19 (0.01, 0.37) | 0.19 (95% CI 0.01, 0.37) | **YES** | Results §"Grouped by outcome type"; Table 2 "Power" row. |
| Docstring "Hypertrophy SMDs 0.05 to 0.20" | 0.05–0.20 | Abstract: *"all between 0.05 to 0.2"* — but this is the **range across ALL outcome types**, not hypertrophy-only | **NO (mislabelled)** | Abstract; Results. The 0.05–0.20 band spans muscle size (0.04), strength (0.14), power (0.19), sport (0.02), body fat (0.12) — it is not a hypertrophy-specific range. |
| Population: Bayesian, mixed status, young adults, upper+lower body | as encoded | Bayesian multilevel `brms`; both upper & lower body; no clear U/L difference | **YES** | Methods §"Meta-Analysis"; Results §"Upper vs Lower Body". |
| `CITATION` (authors/year/doi/journal) | Wolf et al., 2023, 10.47206/ijsc.v3i1.182, IJSC | matches | **YES** | Title page. |

### Outcome estimates the module does NOT encode (for reference)
From Results §"Grouped by outcome type" / Table 2:
- Sport: SMD 0.02 (95% CI −0.22, 0.26)
- Body fat: SMD 0.12 (95% CI −0.36, 0.60)
- Short-length partial vs full (hypertrophy): SMD **0.08 (95% CI −0.24, 0.42)** in favour of fROM — see "Missing short-length estimate" below.

---

## Math checks

### SE recovery — `_se_from_qi(low, high) = (high - low) / (2 * 1.96)`

The formula is the standard Normal-approximation SE from a 95% interval and is applied correctly.

| Estimate | Interval | Recomputed SE | Module SE (via `_se_from_qi`) | OK? |
|---|---|---|---|---|
| `PARTIAL_VS_FULL_OVERALL` | −0.17, 0.25 | (0.25 − (−0.17)) / 3.92 = **0.10714** | 0.10714 | Yes |
| `PARTIAL_LONG_LENGTH_VS_FULL` | −0.81, 0.16 | (0.16 − (−0.81)) / 3.92 = **0.24745** | 0.24745 | Yes |
| `PARTIAL_VS_FULL_STRENGTH` | −0.01, 0.29 | (0.29 − (−0.01)) / 3.92 = **0.07653** | 0.07653 | Yes |

All three SEs are arithmetically correct. All are > 0, so `EffectEstimate.__post_init__` passes.

### Asymmetry of the long-length interval — flag

The long-length interval **−0.81 to 0.16 is not symmetric about the encoded mean −0.28**:
midpoint = (−0.81 + 0.16) / 2 = **−0.325 ≠ −0.28**.

This is expected and correct as *paper output* — it is a **Bayesian posterior quantile interval**, and posterior densities for small-study sub-groups are routinely skewed; the posterior mean need not sit at the QI midpoint. But it has two consequences for the encoding:

1. **`_se_from_qi` silently discards the asymmetry.** It computes a single symmetric SE (0.24745) and `shared.py` then treats the estimate as Normal: `ci_95` would reconstruct **(−0.765, 0.205)**, not the paper's (−0.81, 0.16). The reconstructed interval is shifted right by ~0.045 at the bottom and is wrong at both ends. Any consumer that calls `.ci_95` will get an interval that does not match the paper.
2. **The skew means the true uncertainty is left-heavy** (more posterior mass toward favouring partials). Forcing it Normal understates the lower tail. For a single-SE pooling layer this is tolerable, but it should be documented in the `notes`, and ideally the SE should be recovered from the *wider* half-interval ((−0.28 − (−0.81)) / 1.96 = 0.270) if a conservative SE is wanted, or the mean re-encoded as the QI midpoint −0.325 if interval fidelity matters more. Recommend documenting the choice explicitly rather than leaving it implicit.

The other two intervals **are** symmetric about their means (0.04 and 0.14 are exact midpoints of their QIs), so `_se_from_qi` is exact for them.

### Quality score recomputation — `QUALITY = 0.84`

Per-dimension scores from the module comments, weights from `QUALITY_RUBRIC.md` v1.0:

| Dimension | Module score | Rubric weight | Contribution |
|---|---|---|---|
| Study design | 0.80 | 0.20 | 0.160 |
| Sample size | 0.85 | 0.15 | 0.1275 |
| Measurement quality | 0.80 | 0.20 | 0.160 |
| Methodological rigor | 0.90 | 0.15 | 0.135 |
| Reporting transparency | 0.90 | 0.10 | 0.090 |
| Risk of bias | 0.85 | 0.10 | 0.085 |
| Population specificity | 0.80 | 0.10 | 0.080 |

Weighted average = **0.8375 → 0.84** as encoded. **Arithmetic is correct.** Weights sum to 1.0.

Two scoring judgements are questionable, however (see Concerns):
- **Study design 0.80** is too high. The rubric explicitly says: *"score based on the worst design tier of included studies."* Table 1 shows the meta-analysis pools **within-participant designs** (Valamatos 2018, Sadacharan & Seo 2021, Werkhausen 2021, Pedrosa 2021). Within-subject side-to-side designs score **0.5** on the rubric ladder, and many included studies have no pre-registration. A meta-analysis "of mixed designs (RCT + non-randomized intervention)" is rubric tier **0.7**, not 0.80. The GRADE table itself labels all rows "randomised trials" but rates imprecision "serious" and notes data was missing.
- **Risk of bias 0.85** does not reflect the disclosed funding. The paper's FUNDING statement reads: *"Funding for the lead investigator's PhD project was provided by Renaissance Periodization"* — a commercial training-education company. The COMPETING INTERESTS statement declares none, but the rubric's 0.85 tier is "academic funding, modest conflicts." Industry/commercial funding of the lead author's PhD is closer to the 0.8 tier ("minor conflicts") at best; arguably lower. This is not flagged anywhere in the module.

If study design is corrected to 0.70 and risk of bias to 0.80, the weighted average drops to ≈0.81. Recommend re-scoring.

### Subgroup penalty — `QUALITY * 0.85` for `PARTIAL_LONG_LENGTH_VS_FULL`

0.84 × 0.85 = **0.714**. Arithmetic correct, and the ×0.85 "subgroup analysis presented as primary / post-hoc subgroups are exploratory" modifier is exactly what the rubric prescribes. **Defensible and well-applied.** If anything the long-length sub-group warrants *more* caution: the paper repeatedly calls all sub-group/regression analyses "exploratory" and states they "lack the data and statistical power to make any confident inferences" (Discussion, Limitations) — a 6-study sub-group with a CI of width ~0.97. The ×0.85 is the floor of what's reasonable, not generous.

---

## Strength-vs-power figure — is 0.14 correctly a strength SMD?

**Resolved: YES. 0.14 is unambiguously the STRENGTH SMD; it has NOT been confused with the power figure.**

The paper reports both, distinctly:
- **Strength** outcomes: *"a trivial SMD (0.14; 95% CI: -0.01, 0.29) in favour of fROM"* (Results §"Grouped by outcome type"; Table 2 "Muscle Strength" row, 24 trials, 311 fROM / 428 pROM patients).
- **Power** outcomes: *"a trivial SMD (0.19; 95% CI: 0.01, 0.37) in favour of fROM"* (same section; Table 2 "Power" row, 8 trials, 99/127 patients).

The module's `PARTIAL_VS_FULL_STRENGTH` encodes `mean=0.14, QI −0.01, 0.29` — an exact match to the paper's strength row. The docstring separately and correctly cites "Power SMD 0.19 (0.01, 0.37)" as a *different* figure it does not encode. So the encoding is internally consistent and the strength estimate is the genuine strength estimate. **No confusion exists.** The only related defect is cosmetic: the docstring presents "Hypertrophy SMD: 0.05 to 0.20" as a hypertrophy range when the paper's "0.05 to 0.2" actually describes the spread across *all five* outcome categories — see the table above.

---

## Missing short-length-partial estimate — FOUND

The module omits the short-length-partial-vs-full estimate, with a comment: *"Wolf reports this but I don't have exact numbers in search results; omitted … pending direct paper access."*

**The number exists and is now recovered from the full text.** Results §"Muscle Length & Muscle Hypertrophy":

> *"Analysis revealed a trivial SMD (0.08; 95% CI: –0.24, 0.42) in favour of fROM for muscle hypertrophy when pROM was performed at short muscle lengths."*

So the short-length-partial-vs-full hypertrophy estimate is:

- **SMD = 0.08, 95% CI (−0.24, 0.42)** — positive, favouring full ROM (consistent with the module's `scale` convention where positive favours full ROM, mirroring `PARTIAL_LONG_LENGTH_VS_FULL`'s negative-favours-partial sign).
- `_se_from_qi(-0.24, 0.42)` = (0.42 − (−0.24)) / 3.92 = **0.16837**. The interval is symmetric about 0.09, slightly off the reported mean 0.08, so a minor posterior skew exists — same caveat as the long-length estimate.
- Study count: **19 of 23** studies examined pROM at short lengths *for at least some volume* (Results §"Muscle length of partial range of motion training"). The short-length sub-group is therefore a larger sub-group than the long-length one. Using `n` honestly here is itself tricky — see Concerns.

Important nuance to encode in the `notes` if this estimate is added: the module's docstring and `GUIDANCE_FOR_OPTIMIZER` claim short-length partials are "genuinely inferior" / "clearly inferior." The paper's own short-length estimate is **trivial (0.08) with a CI spanning −0.24 to 0.42** — i.e. it does **not** by itself establish that short-length partials are clearly inferior; it shows a trivial full-ROM lean. The "inferior" framing comes from comparing the short-length estimate (0.08 favouring full) against the long-length estimate (−0.28 favouring partial), and from the Discussion's narrative. The optimizer guidance overstates the strength of the short-length finding relative to what this single paper's numbers support.

---

## Population & design — verified

| Claim | Verdict | Source |
|---|---|---|
| 24 studies | Partly — **24 studies summarised (Table 1); 23 analysed in the main model** ("across 23 studies"). 27 initially included in review; 1 excluded for missing data, 2 theses excluded as duplicate data. | §"Search Results", §"Main Model" |
| Bayesian meta-analysis | YES — Bayesian multilevel mixed-effects via `brms`, MCMC, posterior quantile ("credible/compatibility") intervals. Note these are **QIs/credible intervals**, not frequentist CIs; the module's mixed use of "QI" and "CI" is fine but the paper itself labels them inconsistently too. | §"Meta-Analysis" |
| Mixed training status | YES — inclusion criteria placed no restriction; Table 1 includes untrained, recreationally active and resistance-trained samples. The module's `training_status="mixed"` is appropriate. | Methods; Table 1 |
| Mostly young adults | Plausible but **not explicitly verified** — the paper extracted "weighted mean age" per study but no pooled age range is stated in the text body (would be in Table 1 columns / supplementary). The module's `age_range=(18, 40)` is a reasonable assumption for this literature but is an **assumption, not a paper-stated figure**. Mark as UNVERIFIED-but-reasonable. | Table 1 (per-study ages not in extracted text) |
| Both upper and lower body, no clear difference | YES — Upper SMD 0.07 (−0.18, 0.33); Lower SMD 0.10 (−0.07, 0.27). | §"Upper vs Lower Body" |

---

## The "literature has converged" docstring claims

These are context, not encoded data, but were checked:

- **"Wolf 2024/2025 (Lengthened Partials trial): found lengthened partials elicit similar adaptations to full ROM in trained individuals"** — **Substantiated.** Wolf et al. 2025, *PeerJ* (PMID 39959841): a within-participant 8-week trial in 30 trained individuals found similar hypertrophic responses between lengthened-partial and full-ROM conditions. The docstring's characterisation is accurate.
- **"Short-length partials are inferior"** — **Overstated relative to Wolf 2023's own data.** As noted above, the short-length estimate in this very paper is a trivial 0.08 (CI −0.24, 0.42). The claim is a defensible reading of the *broader* literature and of the long-vs-short contrast, but it is presented in the module as if it were a firm finding of Wolf 2023, which it is not.
- **"Varovic 2025 looked at REGIONAL hypertrophy … trivial effects"** and **"Maeo, Kassiano, Pedrosa found large long-length advantages"** — not independently verified in this audit (out of scope; these are not Wolf 2023). Maeo and Pedrosa are at least cited inside Wolf 2023's own Discussion as long-length-advantage studies, so those name-drops are consistent with the paper.
- **"The literature has CONVERGED on: full ROM and lengthened partials are roughly equivalent"** — a reasonable summary, but it is editorial. Wolf 2023 itself does **not** claim convergence (it predates the 2025 trial); its own long-length sub-group actually leans *toward partials* (−0.28). The docstring's framing is fine as forward-looking context but should not be read back into what Wolf 2023 concluded.

None of this affects encoded values, but the docstring blends Wolf 2023's findings with later literature in a way that could mislead a future reader into thinking the "converged" view is Wolf 2023's conclusion.

---

## Concerns & discrepancies

1. **[MATERIAL] `PARTIAL_VS_FULL_OVERALL` is mislabelled.** 0.04 (−0.17, 0.25) is the *muscle-size outcome sub-group*, not the overall/main-model effect. The paper's main model is 0.12 (−0.02, 0.26). The constant name, the docstring's "Overall partial vs full ROM for hypertrophy" line, and the `notes` string ("Overall: partial vs full ROM…") are all inconsistent with the paper. Because `shared.py` pools `EffectEstimate`s and routes via `best_applicable`, a mislabelled "overall" estimate is a real correctness risk.

2. **[MATERIAL] `n` values misrepresent statistical power.** `n` in `EffectEstimate` is documented as "total participants," and `best_applicable` weights by `sqrt(n)`. The module instead sets `n` to **study counts** (24, 8). This is wrong on two axes:
   - It is the wrong quantity (studies, not participants). The paper *does* give participant counts in Table 2: muscle size = 96 fROM + 116 pROM = **212**; strength = 311 + 428 = **739**.
   - Even as a study count, the values are wrong: the muscle-size sub-group used **8** studies (not 24); the long-length sub-group used **6** (not 8); the main model used 23. Encoding 24 for the muscle-size estimate roughly *triples* its real study base and would make `best_applicable` over-prefer it. The honest fix is to use participant totals from Table 2 (212 for muscle size, 739 for strength) and 6×~? for long-length (long-length participant count not in extracted text — would need Figure 9 / supplementary; could be left approximate with a note).

3. **[MATERIAL] Long-length sub-group `n=8` should be 6.** Paper: "long muscle lengths (6/23)" and "Six studies exist in this area."

4. **[MINOR] Quality score dimensions are arguably inflated.** Study design 0.80 ignores the rubric's "worst included design tier" rule (within-subject side-to-side studies are pooled → 0.5 tier; mixed-design meta-analysis → 0.7 tier). Risk of bias 0.85 ignores the disclosed Renaissance Periodization funding of the lead author's PhD. Re-scoring per rubric gives ≈0.81. The arithmetic for 0.84 is correct given the inputs; the *inputs* are the issue.

5. **[MINOR] Heterogeneity / modifier not considered.** The rubric has an "I² > 75% → ×0.85" modifier. Wolf 2023 is Bayesian and does not report a classical I², but the GRADE table rates imprecision "serious" and the explanatory note says "SMDs were as large as ~1.25" with substantial missing data. There is clearly meaningful heterogeneity. The module applies no heterogeneity modifier; at minimum this should be acknowledged as a deliberate non-application.

6. **[MINOR] Normal-approximation discards posterior skew.** The long-length (and short-length) intervals are asymmetric Bayesian QIs. `_se_from_qi` + `EffectEstimate.ci_95` will reconstruct intervals that do not match the paper. Acceptable for a single-SE pooling layer but should be documented in `notes`.

7. **[MINOR] Docstring "0.05 to 0.20" is an all-outcomes range, not hypertrophy-specific.** Mislabelled context.

8. **[MINOR] Docstring "24 studies" vs "23 analysed."** Minor but worth correcting for precision.

9. **[INFO] No competing-interests issue is surfaced in the module.** The paper declares no competing interests but is PhD-funded by a commercial entity (Renaissance Periodization). Worth a one-line note for transparency, consistent with how the rubric treats funding.

---

## Recommendations — concrete fixes to the module

1. **Rename / relabel the first estimate.** Either:
   - rename `PARTIAL_VS_FULL_OVERALL` → `PARTIAL_VS_FULL_HYPERTROPHY` and change its `notes` to *"'Muscle size' outcome sub-group, 8 studies. SMD 0.04 favouring full ROM (95% QI −0.17, 0.25)."*; **or**
   - keep an "overall" estimate but re-encode it with the paper's true main-model value **mean=0.12, QI −0.02, 0.26** (`_se_from_qi(-0.02, 0.26)` = 0.07143) and add a *separate* hypertrophy estimate at 0.04. Given the app is hypertrophy-centric, the first option is cleaner. Remove "Overall" from the docstring line 10–11.

2. **Fix `n`.** Set `n` to participant totals from Table 2: **212** for the muscle-size/hypertrophy estimate, **739** for strength. For the long-length sub-group, the participant count is not in the article body — either pull it from Figure 9 / OSF supplementary, or set an approximate value with an explicit `notes` caveat; do **not** leave it as the study count 8. At minimum correct the long-length study count to **6** if study-count is retained.

3. **Add the short-length estimate.** It exists:
   ```python
   PARTIAL_SHORT_LENGTH_VS_FULL = EffectEstimate(
       mean=0.08,
       se=_se_from_qi(-0.24, 0.42),   # = 0.16837
       n=...,                          # short-length sub-group; ~19/23 studies touched short lengths
       population=POPULATION_HYPERTROPHY,
       source=CITATION,
       quality_score=QUALITY * 0.85,   # exploratory sub-group
       scale="standardized_mean_diff",
       notes="Short-length partial ROM vs full ROM, hypertrophy. SMD 0.08 "
             "favouring full ROM (95% QI -0.24, 0.42) - trivial, crosses zero. "
             "Note: this paper's own short-length number does NOT establish "
             "short-length partials as 'clearly inferior'; that framing rests "
             "on the long-vs-short contrast and later literature.",
   )
   ```
   Then delete the "pending direct paper access" comment block.

4. **Re-score quality per rubric.** Drop study design to 0.70 (mixed designs incl. within-subject side-to-side), drop risk of bias to 0.80 (commercial PhD funding via Renaissance Periodization). Recompute → ≈0.81. Update `QUALITY` and the per-dimension comment block, and add a one-line note about the funding source.

5. **Document the Normal-approximation limitation** in the `notes` of `PARTIAL_LONG_LENGTH_VS_FULL` (and the new short-length estimate): the encoded SE is a symmetric approximation of an asymmetric Bayesian QI; `ci_95` will not exactly reproduce the paper's interval.

6. **Soften the docstring.** Clarify that (a) "0.05 to 0.20" is the across-all-outcomes SMD range, not hypertrophy-only; (b) "24 studies" → "24 studies reviewed, 23 in the main model"; (c) the "literature has converged"/"short-length partials inferior" lines are post-Wolf-2023 context, not conclusions of this paper. The Wolf 2025 trial reference itself is accurate and can stay.

7. **Optional:** consider applying the rubric's I²/heterogeneity modifier or at least noting explicitly why it is not applied (Bayesian model, no classical I² reported, but GRADE imprecision flagged "serious").
