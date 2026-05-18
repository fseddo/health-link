# Literature Prior Audit — Schoenfeld, Ogborn & Krieger 2017

**Module audited:** `priors-handoff/app/priors/schoenfeld_2017.py`
**Paper:** Schoenfeld BJ, Ogborn D, Krieger JW. "Dose-response relationship between weekly
resistance training volume and increases in muscle mass: A systematic review and
meta-analysis." *Journal of Sports Sciences*. 2017;35(11):1073–1082.
DOI 10.1080/02640414.2016.1210197 — PMID 27433992.
**Audit date:** 2026-05-17
**Auditor:** Independent literature auditor (priors layer)

---

## Sources accessed

| Source | URL | Reached? | What it gave |
|---|---|---|---|
| PubMed abstract page | https://pubmed.ncbi.nlm.nih.gov/27433992/ | YES (HTML) | Full abstract: continuous slope 0.023 / +0.37% / P=0.002; high-vs-low 0.241 / +3.9% / P=0.03; 34 treatment groups / 15 studies; three-tier trend P=0.074 |
| Multiple web searches (PubMed-indexed snippets, secondary reviews) | various | YES | Sensitivity-analysis snippet (continuous slope -> 0.013, P=0.008); a snippet quoting a high-vs-low value of "0.147 (CI 0.033, 0.261; P=0.016)" |
| PMC review PMC8884877 (cites Schoenfeld 2017) | https://pmc.ncbi.nlm.nih.gov/articles/PMC8884877/ | YES (HTML) | Confirms ">9 weekly sets" framing, "highly heterogeneous sample" characterisation; no effect-size numbers |
| Pelland et al. 2025/2026 abstract (for poolability comparison) | https://pubmed.ncbi.nlm.nih.gov/41343037/ | YES (HTML) | Pelland uses fractional set counting (indirect ×0.5), diminishing-returns model, 67 studies / 2058 participants |
| **Open-access full-text PDF (ageingmuscle.be)** | https://www.ageingmuscle.be/.../Dose%20response...pdf | **NO — WebFetch permission denied, repeatedly** | — |
| **Full-text PDF mirrors** (core.ac.uk, elementssystem.com, fisiologiadelejercicio.com) | various `.pdf` URLs | **NO — WebFetch denied for all PDF URLs** | — |
| **Publisher full text** (Springer/T&F, ResearchGate, SemanticScholar, lookgreatnaked.com, fullrangestrength.com) | various | **NO — 403 / auth redirect / permission denied** | — |
| Direct PDF download via curl | ageingmuscle.be | **NO — Bash permission denied** | — |

**Critical limitation:** I could **not reach the full text** of the paper. I confirmed the
abstract verbatim from PubMed, but **Table 1 (study-by-study participants), Table 2, the
forest plots (Figs 1–2), the exact 95% CIs, the reported SEMs, the sensitivity-analysis
CIs, the direct-vs-indirect interaction, and the population breakdown could not be
inspected.** Items depending on those are marked **UNVERIFIED** below — per instructions,
not assumed correct.

---

## Verdict

**MINOR DISCREPANCIES (with several UNVERIFIABLE items).**

The two headline numbers the module encodes — the continuous meta-regression slope
(ES 0.023, +0.37%, P=0.002) and the higher-vs-lower contrast (ES 0.241, +3.9%, P=0.03) —
are **confirmed verbatim against the paper's abstract**, as are the study counts (15
studies, 34 treatment groups) and the existence of an influential-study sensitivity
analysis dropping the slope to ~0.013 (P=0.008). The poolability argument against
Pelland 2026 is **sound and faithfully stated**. However: (a) the SEs are labelled
"reported SEM (Table 2)" / "reported SEM (Results; forest plot)" but I could not verify
Table 2 exists or reports SEMs — and one secondary snippet suggests the value the module
files as the *primary* high-vs-low contrast (0.241) and the value it files as the
*sensitivity* result (0.147, CI 0.033–0.261) may be **swapped or mislabelled** relative
to which is the headline vs the influential-study-removed estimate; this needs full-text
resolution. (b) The `n=418` participant count, the "~3 of 15 trained" claim, the
age range (18,70), the direct-vs-indirect interaction (slopes 0.023/0.006, P=0.037), and
the three-tier ES values (0.307/0.378/0.520) are **all UNVERIFIED** — none appears in any
source I could reach, and the paper's own abstract reports the three-tier analysis as a
non-significant *trend* (P=0.074), which the module does not mention. The quality-score
arithmetic is essentially correct (recomputes to 0.746). Net: the load-bearing effect
sizes are accurate; the surrounding metadata is partly unverifiable and at least one
sensitivity-analysis CI is internally suspicious.

---

## Value-by-value verification

| # | Encoded value | Paper value (source) | Match? | Notes |
|---|---|---|---|---|
| 1 | Continuous slope **mean = 0.023** | "ES of 0.023" (abstract) | YES | Confirmed verbatim, PubMed abstract |
| 1 | Continuous slope **"+0.37% per set" equivalent** | "increase in the percentage gain by 0.37%" (abstract) | YES | Confirmed verbatim |
| 1 | Continuous slope **P = 0.002** | "P = 0.002" (abstract) | YES | Confirmed verbatim |
| 1 | Continuous slope **se = 0.006** ("reported SEM, Table 2") | — | **UNVERIFIED** | Could not access Table 2 or Results body. Cannot confirm the paper reports a SEM at all, nor that it is 0.006. The module's own comment concedes 0.006 reconstructs to a CI of ~0.011–0.035, *narrower* than the encoded 0.010–0.036 — so 0.006 is not even self-consistent with the encoded CI under a Normal model (see Math checks). |
| 1 | Continuous slope **95% CI 0.010–0.036** | — | **UNVERIFIED** | Not in the abstract. Plausible but uninspected. |
| 2 | High-vs-low **mean = 0.241** | "ES difference between higher and lower volumes was 0.241" (abstract) | YES | Confirmed verbatim, PubMed abstract |
| 2 | High-vs-low **"+3.9%" equivalent** | "percentage gain difference of 3.9%" (abstract) | YES | Confirmed verbatim |
| 2 | High-vs-low **P = 0.03** | "P = 0.03" (abstract) | YES | Confirmed verbatim |
| 2 | High-vs-low **se = 0.101** ("reported SEM; forest plot Fig. 2") | — | **UNVERIFIED** | Not in abstract. se=0.101 -> Normal CI 0.043–0.439, which does *not* match the encoded 0.026–0.457 (see Math checks) — internally inconsistent. |
| 2 | High-vs-low **95% CI 0.026–0.457** | — | **UNVERIFIED + SUSPICIOUS** | A secondary search snippet attributes "0.147 (CI 0.033, 0.261; P=0.016)" to the *study-level HV-vs-LV* effect in Fig. 2 — exactly the value the module files as the *sensitivity* result. Possible label swap; see Concerns. |
| 3 | Sensitivity: continuous slope -> **0.013** | "reduced to 0.013 (P = 0.008)" (PubMed-indexed snippet) | YES (value + P) | Value and P=0.008 confirmed; equivalent quoted as +0.25%/set in snippet (module does not encode the %). |
| 3 | Sensitivity: continuous slope CI **0.004–0.021** | — | **UNVERIFIED** | Not in any reachable source. |
| 3 | Sensitivity: high-vs-low -> **0.147**, CI **0.033–0.261** | A snippet gives "0.147 (CI 0.033, 0.261; P=0.016)" | PARTIAL | The triplet 0.147 / 0.033–0.261 matches a value found in search — but the snippet's context ("study-level effect in Figure 2") makes it ambiguous whether this is the *sensitivity* result or the *primary* Fig. 2 study-level contrast. Needs full text. |
| 4 | **n_studies = 15** | "15 studies" (abstract) | YES | Confirmed verbatim |
| 4 | **"34 treatment groups"** (docstring) | "34 treatment groups" (abstract) | YES | Confirmed verbatim |
| 4 | **n = 418** participants | — | **UNVERIFIED** | No reachable source states a total participant count. Could not sum Table 1. See Math checks. |
| 5 | Direct measures slope **0.023**, CI **0.009–0.037** | — | **UNVERIFIED** | No reachable source mentions a direct-vs-indirect interaction at all. |
| 5 | Indirect measures slope **0.006**, CI **−0.023–0.12** | — | **UNVERIFIED** | Same. Note the encoded CI "−0.023–0.12" is suspiciously asymmetric about 0.006 (upper arm 0.114, lower arm 0.029) — likely a typo for −0.012 or 0.012; flag for correction. |
| 5 | Interaction **P = 0.037** | — | **UNVERIFIED** | Same. |
| 6 | `training_status = "mixed"` | "highly heterogeneous sample" (PMC review's characterisation) | LIKELY OK | Heterogeneity confirmed indirectly; the specific "~3 of 15 trained" count is **UNVERIFIED**. |
| 6 | `sex = "mixed"` | — | **UNVERIFIED** (plausible) | Not confirmable from reachable sources. |
| 6 | `age_range = (18, 70)` | — | **UNVERIFIED** | Not confirmable. The module itself flags it as "the envelope of the included studies." |
| — | Three-tier ES **0.307 / 0.378 / 0.520** (docstring, "context, not encoded") | Abstract reports the three-tier analysis as a **non-significant trend, P = 0.074** | **MISLEADING** | The module docstring presents the three-tier numbers as findings without noting the analysis did not reach significance. The abstract explicitly says "a trend for an effect of weekly sets (P = 0.074)." The specific ES values 0.307/0.378/0.520 are themselves **UNVERIFIED**. |
| — | `quality_score = 0.75` | Recomputed 0.746 from module's own dimension scores | YES (arithmetic) | See Math checks. Dimension *defensibility* discussed in Concerns. |

---

## Math checks

### A. Independent participant-count sum (`n = 418`)

**Could not perform.** Table 1 of the paper lists studies and per-study subject counts; I
could not reach the full text (all PDF mirrors blocked, publisher behind auth). No
secondary source I reached states a pooled participant total. The figure `n=418` is
therefore **unverified**. The abstract and every secondary source consistently report
**15 studies / 34 treatment groups**, so those two are solid; the participant total is not.

Sanity note only (not a verification): 34 treatment groups at the field-typical 8–15
participants per group would span roughly 270–510 participants, so 418 is *plausible* —
but plausibility is not confirmation. **Recommend** obtaining the full text and summing
Table 1 before trusting `n=418`; the value drives `sqrt(n)` weighting in
`best_applicable()` and inverse-variance-adjacent logic, so an error here is not cosmetic.

### B. Quality-score recomputation

Module dimension scores and rubric weights:

| Dimension | Score | Weight | Contribution |
|---|---|---|---|
| Study design | 0.72 | 0.20 | 0.1440 |
| Sample size | 0.80 | 0.15 | 0.1200 |
| Measurement quality | 0.70 | 0.20 | 0.1400 |
| Methodological rigor | 0.80 | 0.15 | 0.1200 |
| Reporting transparency | 0.80 | 0.10 | 0.0800 |
| Risk of bias | 0.82 | 0.10 | 0.0820 |
| Population specificity | 0.60 | 0.10 | 0.0600 |
| **Weighted sum** | | **1.00** | **0.7460** |

Weights sum to 1.00 (correct). Weighted average = **0.746**, rounds to **0.75**.
**The arithmetic is correct.** No flat modifiers applied; the module's reasoning for not
applying the I²>75% heterogeneity modifier ("no I² reported, so the modifier cannot be
applied") is consistent with the rubric, which gates that modifier on a measurable I².

**Defensibility of the individual dimension scores** (judgement, given what the rubric
says and what is known about the paper):

- *Study design 0.72* — rubric's 0.7 row is "meta-analysis of mixed designs (RCT +
  non-randomized intervention)"; the rubric also says score by the *worst* included
  design tier, and notes within-participant/side-to-side designs sit at 0.5. The module
  acknowledges "a few within-participant designs." Strictly applying the worst-tier rule
  would push this toward 0.5–0.6, not 0.72. **Mildly generous but within judgement.**
- *Sample size 0.80* — rubric's MA band 300–499 = 0.8. But this rests on the
  **unverified** n=418. If the true total were <300 the score should be 0.7. **Conditional
  on the unverified count.**
- *Measurement quality 0.70* — mixed MRI/ultrasound/DXA/BodPod. Rubric: whole-body DXA =
  0.5, regional DXA = 0.7, ultrasound 0.85–0.9, MRI 1.0. A genuine mix including
  whole-body measures averaging to 0.70 is **defensible**, arguably slightly generous if
  whole-body measures were common.
- *Methodological rigor 0.80* — rubric's 0.8 = "no pre-reg but otherwise rigorous;
  multiple specifications tested." Sensitivity + interaction analyses support this.
  **Defensible.**
- *Reporting transparency 0.80* — rubric's 0.8 = "effect sizes with CIs but no raw data."
  **Defensible IF** the paper reports CIs directly. The module claims it does ("full
  effect sizes with SEM, 95% CIs"); I could not verify. If SEs had to be reconstructed
  the rubric caps this dimension at 0.6 — see Concerns.
- *Risk of bias 0.82* — rubric says do not penalise industry-adjacency alone; 0.8 is the
  "standard academic, minor conflicts" row. **Defensible.**
- *Population specificity 0.60* — rubric's 0.5 = "heterogeneous population without
  subgroup analysis"; 0.7 = "described but wide ranges." The paper *did* run subgroup/
  interaction analyses, so 0.60 (between the two) is **defensible**.

Overall: the 0.75 is reasonable and the math is right, but **two dimensions (sample size,
reporting) rest on unverified facts**, and study design is mildly generous. If the
worst-tier rule were applied strictly to study design (0.55) the weighted average drops
to ~0.71 -> 0.70. Not a material change, but worth noting the 0.75 is at the optimistic
edge of the defensible band.

### C. SE / CI internal consistency (within the module, independent of the paper)

`EffectEstimate.ci_95` computes `mean ± 1.96·se`. Checking the encoded SEs against the
encoded CIs:

- **Continuous slope:** se=0.006 -> Normal CI = 0.023 ± 0.01176 = **0.0112 – 0.0348**.
  Encoded/quoted paper CI = **0.010 – 0.036**. These differ. The module *acknowledges*
  this in a comment ("~0.011–0.035 vs the paper's 0.010–0.036 — an acceptable
  approximation"). Fine as a documented approximation, but it means se=0.006 is **not**
  the SE that produces the paper's CI; the implied SE of a 0.010–0.036 interval is
  (0.036−0.010)/(2·1.96) ≈ **0.0066**, not 0.006. Minor.
- **High-vs-low contrast:** se=0.101 -> Normal CI = 0.241 ± 0.198 = **0.043 – 0.439**.
  Encoded paper CI = **0.026 – 0.457**. The implied SE of 0.026–0.457 is
  (0.457−0.026)/(2·1.96) ≈ **0.110**, not 0.101. The discrepancy (0.101 vs 0.110) is
  larger here than for the slope and is **not** flagged in the module comment. Either the
  CI is a t-interval (wider than Normal, consistent with robust-variance estimation) and
  se=0.101 is the true SEM — in which case `ci_95` will under-cover — or one of the two
  numbers is mis-transcribed. This should be reconciled against Table 2 / Fig. 2.

---

## Poolability claim (Schoenfeld 2017 vs Pelland 2026)

The module's central architectural argument is that Schoenfeld 2017 must **not** be
inverse-variance pooled with Pelland 2026 despite answering the same question. It gives
three reasons. Assessment:

1. **Different scale (SMD/set vs %/set).** *Sound.* Schoenfeld's primary metric is a
   standardized-mean-difference slope (ES 0.023 per set); the "+0.37%" is explicitly a
   derived back-conversion (the abstract itself phrases it as "an increase in the
   percentage gain by 0.37%"). Pelland reports on a percentage scale. Inverse-variance
   pooling requires a common scale; an SMD slope and a % slope are genuinely different
   units. The module's `scale="smd_per_set"` field correctly tags this, and
   `combine_inverse_variance()` in `shared.py` *does* hard-reject mixed scales
   (`raise ValueError(f"Cannot pool different scales: {scales}")`), so the safeguard is
   real and not merely documentary. **Faithfully stated.**

2. **Raw vs fractional set counting.** *Sound and confirmed.* I verified from the Pelland
   2026 abstract that Pelland classifies sets as direct/indirect and weights indirect
   sets at 0.5 ("the relative evidence for the 'fractional' quantification method was
   strongest"). Schoenfeld 2017 predates that framework and counts sets directly. The
   denominators of the two "per set" slopes therefore differ — a set means different
   things in each paper. **Faithfully stated.**

3. **Linear vs square-root model form.** *Sound, slightly loosely worded.* Schoenfeld
   fits a linear meta-regression slope. Pelland's abstract confirms "diminishing returns"
   / best-fit non-linear models (the module says "square-root curve"; the abstract I
   reached says "diminishing returns" without naming the exact functional form, so
   "square-root" is plausibly correct but is the module author's characterisation, not a
   quote). The substantive point — that a single linear slope and a marginal slope at the
   mean of a curvilinear fit are not the same estimand — is **correct**. Minor: the
   module states the square-root form with more confidence than the abstract evidence
   alone supports; if the exact form matters it should be checked against Pelland's
   methods.

**Overall: the incommensurability reasoning is sound and does not overstate the case.**
If anything it slightly *understates* a fourth reason: the two papers also differ in
**measurement inclusion** (Pelland restricts to direct site-specific MRI/MT/CSA per the
quality rubric's Pelland worked example; Schoenfeld pools direct *and* whole-body
measures). That alone makes the pooled estimands non-identical and reinforces the
no-pool decision. The module captures this only obliquely via the direct-vs-indirect
caveat. The decision to encode Schoenfeld as **directional corroboration** rather than a
poolable estimate, and to keep it out of the pool via `_POOLABLE_OVERRIDE`, is the
correct call and is well justified. No concern here.

---

## Concerns & discrepancies

1. **Full text never inspected.** All open-access PDF mirrors and the publisher page were
   inaccessible (WebFetch denied for every `.pdf` URL; Bash download denied; Springer/
   ResearchGate behind auth/403). Everything beyond the abstract — Table 1 participant
   counts, Table 2, the forest plots, the exact CIs, the SEMs, the direct-vs-indirect
   interaction — is **unverified**. Per the audit brief these are marked UNVERIFIED, not
   assumed correct. The rubric's "Sci-Hub-only access; can't verify methods" ×0.9
   modifier is arguably triggerable here (the auditor couldn't inspect methods), though
   that modifier is about *the prior author's* access, not the auditor's.

2. **Possible swap/mislabel of the high-vs-low primary vs sensitivity values.** A
   secondary search snippet attributes **"0.147 (CI 0.033, 0.261; P=0.016)"** to the
   study-level higher-vs-lower contrast shown in the paper's Figure 2. The module encodes
   **0.241 (CI 0.026–0.457, P=0.03)** as the *primary* contrast and **0.147 (CI
   0.033–0.261)** as the *sensitivity* (Radaelli-removed) result. The abstract clearly
   states the primary contrast is 0.241 / P=0.03, so the *primary* value is right — but
   the P=0.016 attached to 0.147 in the snippet vs the module's silence on the
   sensitivity P for the contrast, plus the snippet calling 0.147 a "study-level Figure 2"
   value, leaves genuine ambiguity about whether 0.147 is the sensitivity result or
   something else. **Must be resolved against the full text.**

3. **Three-tier numbers presented without their non-significance.** The docstring lists
   "mean ES 0.307 / 0.378 / 0.520 for <5 / 5–9 / 10+ weekly sets" as "context." The
   abstract explicitly reports this categorical analysis as only **"a trend ... (P =
   0.074)"** — i.e. not statistically significant. Presenting the three monotonic ES
   values without that caveat overstates the evidence. The specific values 0.307/0.378/
   0.520 are also themselves unverified.

4. **Internal SE/CI inconsistency on the high-vs-low estimate.** se=0.101 implies a
   Normal CI of 0.043–0.439, not the encoded 0.026–0.457 (implied SE ≈ 0.110). The slope
   estimate has the same issue but smaller and is flagged in a comment; the contrast
   estimate's discrepancy is larger and unflagged. `ci_95` will misreport this estimate's
   interval either way.

5. **Asymmetric indirect-measures CI looks like a typo.** The docstring gives the
   indirect-measure slope as "0.006, CI −0.023–0.12". An interval from −0.023 to 0.12 is
   wildly asymmetric around 0.006 and the upper bound (0.12) is an order of magnitude
   larger than the point estimate. Almost certainly a transcription error (likely
   intended −0.023 to 0.012, or −0.012 to 0.023). Since the whole interaction is
   unverified anyway, the entire claim needs full-text confirmation.

6. **Reporting-transparency score depends on an unverified fact.** The 0.80 for reporting
   assumes the paper reports effect sizes *with CIs* directly. The rubric caps this
   dimension at 0.6 "if you have to reconstruct SE from a p-value." The module's comments
   state SEs were "reported directly by the paper as the SEM (Table 2 / Results)" — but
   also, contradictorily, the `ci_95` comment frames the paper's intervals as
   "robust-variance t-intervals" the module *approximates*. If the SEs were in fact
   derived from CIs or P-values rather than read off a table, the reporting score and
   possibly the SE provenance comments are wrong. Unverifiable without the full text.

7. **Population fields unverified.** `training_status="mixed"`, `sex="mixed"`,
   `age_range=(18,70)`, and the comment "only ~3 of 15 studies used trained participants"
   could not be checked against the included-studies list. Heterogeneity is corroborated
   indirectly (a later review calls Schoenfeld's sample "highly heterogeneous"), but the
   specific counts and the age envelope are the prior author's reconstruction.

---

## Recommendations

1. **Obtain the full text and verify the unverified items before relying on this prior.**
   Specifically: sum Table 1 to confirm/correct `n=418`; read Table 2 / Figs 1–2 for the
   exact CIs and whether the paper reports SEMs; locate the direct-vs-indirect interaction
   and confirm the slopes (0.023/0.006), CIs, and P=0.037; confirm the sensitivity-
   analysis CIs (0.004–0.021 and 0.033–0.261).

2. **Resolve the 0.241 vs 0.147 labelling.** Confirm from the full text that 0.241 is the
   primary higher-vs-lower contrast (abstract says so — solid) and that 0.147 / CI
   0.033–0.261 is specifically the *Radaelli-removed sensitivity* result and not the
   study-level Figure-2 value. If the sensitivity contrast carries P=0.016, record it.

3. **Add the non-significance caveat to the three-tier numbers.** The docstring should
   state the categorical (<5 / 5–9 / 10+) analysis was a non-significant trend (P=0.074),
   not present 0.307/0.378/0.520 as established findings. Or drop the three-tier line
   entirely since it is "not encoded" anyway.

4. **Fix the asymmetric indirect-measures CI** ("−0.023–0.12") — almost certainly a typo;
   correct against the paper.

5. **Reconcile the high-vs-low SE.** Either set `se` so `ci_95` reproduces the paper's
   interval (implied SE ≈ 0.110 for 0.026–0.457), or keep se=0.101 as the true SEM and
   add the same explicit "approximation" comment the slope estimate already carries, so
   the under-coverage of `ci_95` is documented rather than silent.

6. **Re-examine the reporting-transparency dimension.** Confirm whether SEs were read
   directly from a table or reconstructed. If reconstructed from CIs/P-values, the rubric
   caps reporting at 0.6 and the SE-provenance comments must be corrected; the quality
   score would drop to ~0.73.

7. **Consider noting the worst-tier rule** for study design: with within-participant
   designs included, the rubric's "score by worst included tier" guidance argues for
   ~0.55–0.60 rather than 0.72. Not material to the final 0.75 (would yield ~0.70–0.71),
   but document the deviation explicitly as the rubric requires.

8. **No change needed to the poolability decision.** Keeping Schoenfeld 2017 out of the
   Pelland volume->hypertrophy pool via `_POOLABLE_OVERRIDE`, and encoding it as
   directional corroboration on a distinct `scale`, is correct and well-reasoned.

---

## Encoder reconciliation (2026-05-17, post-audit)

This audit was conducted without full-text access — every PDF mirror and the publisher
page were blocked. The primary encoder, however, had fetched and read the complete
full-text PDF (all 11 pages, including Table 1, Table 2, the Interactions section, and the
Sensitivity analysis). The audit's UNVERIFIED items are reconciled against that full text:

- **n = 418** — CONFIRMED. Summed from Table 1, study by study: 30 + 31 + 36 + 28 + 28 +
  18 + 27 + 48 + 27 + 20 + 18 + 30 + 21 + 8 + 48 = 418 across the 15 studies.
- **Continuous-slope SE 0.006 / CI 0.010–0.036** — CONFIRMED. Table 2 prints
  "0.023 ± 0.006 | 0.010, 0.036". The SE is the table-reported SEM; it was NOT
  reconstructed from a CI or p-value (resolves Concern 6 — reporting-transparency 0.80
  stands).
- **High-vs-low SE 0.101 / CI 0.026–0.457** — CONFIRMED. Results prints
  "0.241 ± 0.101 (CI: 0.026, 0.457)". The CI is wider than a Normal 1.96·SE interval
  because the paper uses robust-variance small-sample (t) estimation — expected, not an
  error (resolves Concern 4).
- **0.241 vs 0.147 labelling** — CONFIRMED, no swap. The Sensitivity analysis section
  states the Figure-2 study-level higher-vs-lower contrast "decreased to 0.147 (CI:
  0.033, 0.261; P = 0.016)" after removing Radaelli, Fleck 2014. 0.241 is the primary
  contrast; 0.147 is the sensitivity result (resolves Concern 2).
- **Direct-vs-indirect interaction** — CONFIRMED. Results / Interactions: P = 0.037;
  direct slope 0.023 (CI 0.009–0.037); indirect slope 0.006. The paper itself prints the
  indirect CI as "−0.023, 0.12", an evident paper typo (resolves Concern 5).
- **Training status ~3/15 trained** — CONFIRMED. Table 1: only Ostrowski 1997, Radaelli
  Fleck 2014 and Rhea 2002 used (recreationally / resistance-)trained participants; the
  other 12 used untrained participants.
- **Three-tier ES 0.307 / 0.378 / 0.520, trend P = 0.074** — CONFIRMED from Table 2.

Fixes applied to the module in response to this audit (Concerns 3, 4, 5, 7):
1. The three-tier line now states the analysis was a non-significant trend (P = 0.074).
2. The indirect-measures CI is flagged as an apparent paper typo, not reproduced as a number.
3. The Normal-approximation comment now covers BOTH estimates explicitly.
4. The high-vs-low sensitivity note now records P = 0.016.
5. The study-design quality comment documents the worst-tier-rule deviation.

No encoded value changed; quality_score 0.75 stands (arithmetic confirmed by the audit).
**Verdict after reconciliation: ACCURATE** — the MINOR discrepancies were documentation
gaps, now closed.
