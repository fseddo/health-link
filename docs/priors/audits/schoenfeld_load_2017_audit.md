# Literature Audit — `schoenfeld_load_2017.py`

**Module audited:** `priors-handoff/app/priors/schoenfeld_load_2017.py`
**Paper:** Schoenfeld BJ, Grgic J, Ogborn D, Krieger JW. "Strength and Hypertrophy
Adaptations Between Low- vs. High-Load Resistance Training: A Systematic Review
and Meta-analysis." *J Strength Cond Res.* 2017;31(12):3508-3523.
DOI 10.1519/JSC.0000000000002200. PMID 28834797.
**Audit date:** 2026-05-17
**Auditor:** Independent literature auditor (re-fetched the paper from scratch;
did not rely on the module's own encoding).

---

## Sources accessed

| Source | Reached? | What it gave |
|---|---|---|
| PubMed PMID 28834797 (`pubmed.ncbi.nlm.nih.gov/28834797/`) | YES | Full abstract, inclusion criteria, conclusion verbatim, n=21 studies, load definitions |
| JSCR full text (`journals.lww.com/.../31.aspx`) | NO — HTTP 402 Payment Required | Paywalled; could not read Table 1, Table 2, or the three forest plots |
| Open-access PDF mirror (`elementssystem.com/.../Schoenfeld-17-altas-bajas.pdf`) | NO — WebFetch permission denied, curl download denied | — |
| Alternate PDF mirror (`be-research-papers.s3.amazonaws.com/.../Schoenfeld-2017-...pdf`) | NO — WebFetch permission denied | — |
| Ovid PDF link | NO — WebFetch permission denied | — |
| ResearchGate full PDF | NO — HTTP 403 | — |
| Schoenfeld et al. 2021 "Loading Recommendations / Repetition Continuum" review (PMC7927075) — **a Schoenfeld-group paper that cites this MA** | YES (via WebFetch) | Verbatim citing sentences: ES 0.58 (14 studies), isometric ES 0.16, hypertrophy ES 0.03 with **95% CI −0.16 to 0.22** |
| Web search index (multiple queries) | YES | Confirmed study-level 1RM ES 0.58 ± 0.16 (CI 0.28–0.89, p=0.002); inclusion criterion "all sets to momentary muscular failure"; per-load ES 1.69/1.32 |

**Full-text status: NOT REACHED.** Every PDF mirror was blocked by a WebFetch
permission denial in this environment, the publisher's HTML is paywalled (402),
and Bash file download was denied. I could **not** inspect Table 1 (per-study
participant counts), Table 2 (the SEM-bearing summary table), or the three
forest plots (Figures 2–4) directly. Verification below rests on: (a) the
PubMed abstract, (b) verbatim citing sentences in Schoenfeld's own 2021 review,
and (c) cached Results-section fragments returned by the search index. Items
that depend solely on the un-reached full text are marked **UNVERIFIED**.

---

## Verdict

**MINOR DISCREPANCIES** (one of which is potentially material and should be
resolved before the module is trusted).

The module's three headline effect sizes, p-values, study counts, load
definitions, the "all sets to failure" scope limit, the disambiguation from the
sibling volume MA, and the poolability reasoning are all **consistent with what
I could verify** and are clearly the correct quantity (the study-level
forest-plot "Overall ES", not the per-load ES nor the mean-ES difference). The
1RM estimate (ES 0.58, CI 0.28–0.89, p=0.002, 14 studies) is confirmed verbatim
from two independent sources. **However, one discrepancy stands out:** the
module encodes the hypertrophy 95% CI as **−0.08 to 0.14**, but Schoenfeld's own
2021 review quotes this exact result as **ES 0.03, 95% CI −0.16 to 0.22**. If
the paper's printed CI is −0.16 to 0.22, then the module's encoded `se=0.05` is
wrong — the correct SE would be ≈0.097 — and the comment "(95% CI −0.08–0.14)"
misreports the paper. This is the single most important finding of the audit
and is currently **UNVERIFIED against the primary source** because the full text
could not be reached. Everything else is either confirmed or a minor wording
nit.

---

## Value-by-value verification

Positive ES = favours high load. "Confirmed" = matched against a source I
reached. "UNVERIFIED" = depends on full text (Table 1/2, forest plots) I could
not access.

| Encoded value | Module | Independent finding | Status |
|---|---|---|---|
| 1RM strength ES | 0.58 | "study-level analysis revealed an effect size that significantly favored high loads (ES = 0.58 ± 0.16; CI: 0.28–0.89; p = 0.002)" — confirmed verbatim via search index AND Schoenfeld 2021 review ("ES = 0.58 ... pooled data from 14 included studies") | **CONFIRMED** |
| 1RM 95% CI | 0.28–0.89 | Same source: CI 0.28–0.89 | **CONFIRMED** |
| 1RM p-value | 0.002 | Same source: p = 0.002 | **CONFIRMED** |
| 1RM SE (encoded `se=0.16`) | 0.16 | Search index reports "ES = 0.58 ± 0.16" (the ± value is the SEM). 0.58 ± 1.96·0.16 = 0.27–0.89 ≈ paper's 0.28–0.89. Internally consistent. | **CONFIRMED** (SEM ± value matches; exact paper text unread) |
| 1RM n_studies | 14 | Schoenfeld 2021 review: "pooled data from 14 included studies" | **CONFIRMED** |
| 1RM n (participants) | 497 | Summed by encoder from Table 1; Table 1 not reached | **UNVERIFIED** |
| Isometric strength ES | 0.16 | Schoenfeld 2021 review: "a small, statistically non-significant benefit (ES = 0.16) to the use of heavier loads when testing on an isometric device" | **CONFIRMED** (point estimate) |
| Isometric 95% CI | −0.10–0.41 | Not independently reached. Consistent with module's `se=0.11` (0.16 ± 1.96·0.11 = −0.056–0.376; paper's robust t-interval would be slightly wider). | **UNVERIFIED** (CI), plausible |
| Isometric p-value | 0.19 | Abstract: "no significant differences were found for isometric strength" — direction confirmed; exact p not reached | **PARTIALLY CONFIRMED** (non-significant confirmed; p=0.19 unread) |
| Isometric n_studies | 8 | Search index repeatedly associates the isometric analysis with "8 studies" / "23 effect sizes from 8 studies" | **CONFIRMED** (8 studies; the "23 ES" figure suggests Fig. 3 has 8 studies) |
| Isometric n (participants) | 176 | Summed from Table 1; not reached | **UNVERIFIED** |
| Hypertrophy ES | 0.03 | Schoenfeld 2021 review: "trivial effect size difference (0.03)"; abstract: "Changes in measures of muscle hypertrophy were similar" | **CONFIRMED** (point estimate) |
| **Hypertrophy 95% CI** | **−0.08 to 0.14** | Schoenfeld 2021 review quotes this result as **"relatively narrow 95% confidence intervals (−0.16 to 0.22)"** — a DIFFERENT, wider interval | **DISCREPANCY — see Concerns #1** |
| Hypertrophy p-value | 0.56 | Search index returns "study level analysis showed no impact of load (ES = 0.03 ± 0.05; CI: −0.08 to 0.14; p = 0.56)" — matches the module exactly | **CONFLICTING EVIDENCE — see Concerns #1** |
| Hypertrophy SE (encoded `se=0.05`) | 0.05 | Search index returns "0.03 ± 0.05" (matches module); but this is inconsistent with the −0.16 to 0.22 CI from the 2021 review | **CONFLICTING EVIDENCE — see Concerns #1** |
| Hypertrophy n_studies | 10 | Not independently confirmed by a clean source; search index conflated analyses. Abstract gives 21 studies total only. | **UNVERIFIED** |
| Hypertrophy n (participants) | 231 | Summed from Table 1; not reached | **UNVERIFIED** |
| Load definition (low ≤60% 1RM, high >60% 1RM) | yes | PubMed inclusion criteria, verbatim: "low-load training [≤60% 1 repetition maximum (1RM)] and high-load training (>60% 1RM)" | **CONFIRMED** |
| All sets to momentary muscular failure | hard scope limit | PubMed inclusion criteria, verbatim: "with all sets in the training protocols being performed to momentary muscular failure" | **CONFIRMED** — this is an explicit inclusion criterion, so every included study did use failure. Module's "hard scope limit" framing is correct. |
| Per-load ES 1RM 1.69/1.32 (context) | yes | Search index: "both heavy and light loads showed large effects for 1RM increases (1.69 and 1.32, respectively)" | **CONFIRMED** |
| Per-load ES hypertrophy 0.53/0.42 (context) | yes | Not independently reached | **UNVERIFIED** |
| Total studies = 21 | docstring | PubMed: "A total of 21 studies were ultimately included for analysis" | **CONFIRMED** |
| Mean-ES hypertrophy trend p=0.10 | caveat #2 | Search index returned a value "D = −0.11 ± 0.06 (CI −0.24 to 0.03; p = 0.10)" but attributed it ambiguously (the search model conflated outcomes). Direction (trend favouring high load) plausible; exact attribution not cleanly verified. | **UNVERIFIED** |
| Sensitivity: removing 3 influential studies → p=0.22–0.46 | caveat #2 | Not reached | **UNVERIFIED** |
| Sensitivity: removing Van Roie 2013b (isometric) | estimate notes | Not reached | **UNVERIFIED** |
| PEDro mean 5.6, "good to excellent" | quality comment | Not reached | **UNVERIFIED** |
| Conflict-of-interest statement | "could not be inspected" | Module already concedes this was not inspected. Honest. | n/a |
| Citation: JSCR 2017;31(12):3508-3523, DOI 10.1519/JSC.0000000000002200 | yes | PubMed: "J Strength Cond Res. 2017 Dec;31(12):3508-3523" — exact match | **CONFIRMED** |

---

## Math checks

### 1. Independent participant-count re-sum (hypertrophy 10-study set)

**Could not be performed.** The re-sum requires Table 1 of the paper, which is
in the paywalled / WebFetch-blocked full text. I could not reach Table 1, nor
identify which 10 studies constitute the hypertrophy forest plot. The encoded
`n=231` (hypertrophy), `n=497` (1RM), `n=176` (isometric) are therefore
**UNVERIFIED**.

Methodological flag on the encoder's *approach*, independent of the numbers:
the module comment says "n is summed from Table 1 across the studies in each
analysis's forest plot, and includes **all study arms**." Summing all arms of
each included study is a defensible proxy for "participants contributing to
this analysis," but note two structural caveats:

- **Over-count risk:** the 21-study pool overlaps across the three forest plots
  (a single study can contribute to both the 1RM and the hypertrophy analysis).
  The three n's (497 + 176 + 231 = 904) therefore must NOT be added together —
  they are not 904 distinct people. The module keeps them as three separate
  `EffectEstimate.n` values and never sums them, so this is fine *as encoded*,
  but a future maintainer pooling these must not treat them as additive.
- **Arm-counting vs analysis-contributing:** if any included study had an arm
  that did not contribute to a given outcome (e.g., a study measured 1RM but
  not muscle thickness), counting "all arms" for that outcome's n slightly
  over-states the participants for that specific forest plot. Whether this bites
  depends on study design and is **UNVERIFIED**.
- The `n` only feeds `best_applicable()`'s `sqrt(n)` term and the pooled-`n`
  display, not the statistics, so a moderate mis-count is low-stakes — but it
  should not be presented as exact. The module's "~231" / "~497" / "~176"
  wording with a tilde is appropriately hedged.

**Recommendation:** when the full text becomes reachable, re-sum Table 1 for the
hypertrophy forest plot and confirm 231. Until then, mark these n's as
encoder-estimated.

### 2. Quality-score recomputation (rubric v1.0)

Per-dimension scores from the module comments and the rubric weights:

| Dimension | Weight | Module score | Weighted |
|---|---|---|---|
| Study design | 0.20 | 0.72 | 0.1440 |
| Sample size | 0.15 | 0.75 | 0.1125 |
| Measurement quality | 0.20 | 0.85 | 0.1700 |
| Methodological rigor | 0.15 | 0.80 | 0.1200 |
| Reporting transparency | 0.10 | 0.80 | 0.0800 |
| Risk of bias | 0.10 | 0.80 | 0.0800 |
| Population specificity | 0.10 | 0.62 | 0.0620 |
| **Sum** | 1.00 | | **0.7685** |

Arithmetic **checks out**: 0.7685 → rounds to **0.77**. The module's stated
"Weighted average: 0.7685 → 0.77" is correct. `QUALITY = 0.77` is internally
consistent and `0 ≤ 0.77 ≤ 1` passes `EffectEstimate.__post_init__`.

Defensibility of the per-dimension scores:
- **Study design 0.72** — defensible. Rubric: MA of mixed RCT + non-randomized
  intervention = 0.7. The +0.02 nudge for "PEDro mean 5.6, good to excellent" is
  minor and consistent with the sibling `schoenfeld_2017.py` (also 0.72). OK.
- **Sample size 0.75** — defensible but slightly generous. Rubric's MA band:
  150–299 → 0.7, 300–499 → 0.8. The 1RM analysis (n≈497) sits at 0.8, the
  hypertrophy (≈231) and isometric (≈176) at 0.7. A single QUALITY shared across
  all three estimates is a simplification; 0.75 is a reasonable midpoint, though
  arguably the hypertrophy and isometric estimates each merit 0.7. Low-stakes.
- **Measurement quality 0.85** — defensible. Hypertrophy restricted to direct
  measures (MRI/CT/ultrasound) and 1RM is direct dynamic testing → high. Note
  the *isometric* estimate's measurement is isometric MVC, which the rubric
  scores at 0.7 for strength ("isometric or isokinetic peak torque,
  well-controlled"). Again the shared QUALITY blurs this; the isometric estimate
  is mildly over-scored on measurement. Minor.
- **Reporting 0.80** — defensible (full ES + SEM + CIs + 3 forest plots, no data
  deposit). The rubric says reconstructing SE from a p-value caps this at 0.6 —
  the module claims SEs were read directly off the paper (Results/Table 2), so
  0.80 is allowed *if that claim is true*. **It is UNVERIFIED** (Table 2 not
  reached). If the SEs were in fact reconstructed, reporting must drop to ≤0.6.
- **Risk of bias 0.80** — defensible; rubric explicitly says don't penalise
  industry-adjacent authors below 0.6 absent a direct conflict. OK.
- **Population 0.62** — defensible for a heterogeneous mixed-status, mixed-age,
  mixed-sex pool with subgroup analyses. OK.

No flat modifiers applied. That is defensible: no I² reported (so the >75%
heterogeneity modifier cannot be triggered), not a different question, not a
predatory journal, not retracted. **Quality score 0.77: arithmetic correct,
scores defensible.** The only soft concern is that a single shared QUALITY
across three estimates of differing precision/measurement slightly over-credits
the isometric estimate — acceptable but worth a note.

### 3. ci_95 reconstruction checks (mean ± 1.96·se)

`EffectEstimate.ci_95` uses a Normal `mean ± 1.96·se`.

- **1RM:** 0.58 ± 1.96·0.16 = **(0.266, 0.894)**. Paper: 0.28–0.89. The module's
  comment ("ci_95 ~0.27–0.89 vs the paper's 0.28–0.89") is accurate — Normal
  approximation is marginally narrower than the paper's small-sample t-interval.
  Acceptable, and consistent with the sibling module's stated convention.
- **Isometric:** 0.16 ± 1.96·0.11 = **(−0.056, 0.376)**. Module comment claims
  the paper's CI is −0.10–0.41. The Normal reconstruction (−0.06–0.38) is
  *noticeably* narrower than the claimed paper interval (−0.10–0.41) — a wider
  gap than for 1RM. This is plausible (small-sample t with only 8 studies and
  robust variance can be appreciably wider than Normal), but it means the
  encoded `se=0.11` does **not** reproduce the −0.10–0.41 interval. If the paper
  actually reports −0.10–0.41, the implied SE is ≈(0.41−0.16)/1.96 ≈ 0.128 on
  the upper side, ≈(0.16+0.10)/1.96 ≈ 0.133 on the lower side — i.e. ~0.13, not
  0.11. The asymmetric paper CI around a Normal-symmetric `se` cannot be exactly
  reproduced either way; the discrepancy is within the module's stated
  "acceptable approximation" caveat but is larger than the 1RM case.
- **Hypertrophy:** 0.03 ± 1.96·0.05 = **(−0.068, 0.128)** ≈ −0.07 to 0.13. The
  module comment says the paper's CI is −0.08–0.14. Reconstruction matches the
  module's *claimed* paper CI well. **BUT** Schoenfeld's own 2021 review reports
  this result's CI as **−0.16 to 0.22**. If −0.16 to 0.22 is correct, the SE is
  ≈(0.22−0.03)/1.96 ≈ **0.097**, roughly double the encoded 0.05, and `ci_95`
  would return (−0.07, 0.13) — far too narrow versus the true (−0.16, 0.22).
  See Concerns #1.

---

## Poolability claim (1RM vs isometric)

The module argues 1RM (dynamic) strength and isometric strength are **different
outcomes** that must not be inverse-variance pooled, and that the registry keeps
only the 1RM estimate poolable for the load→strength topic via a
`_POOLABLE_OVERRIDE`.

**Assessment: sound, and well-reasoned.** Three independent arguments support it:

1. **The paper's own thesis.** The whole point of the MA is that load affects
   the two outcomes *differently* — 1RM significantly favours high load (ES
   0.58, p=0.002) while isometric does not (ES 0.16, p≈0.19). Pooling them would
   average away the very finding the paper exists to report. Confirmed: the
   abstract treats "1RM strength" and "isometric strength" as separate result
   lines with opposite significance.
2. **Construct validity / specificity.** 1RM is a trained, dynamic,
   load-specific test; isometric MVC is a neutral test of a different strength
   construct. They are correlated but not interchangeable. Inverse-variance
   pooling assumes the estimates target a common underlying parameter; here they
   do not.
3. **Consistency with the codebase pattern.** `shared.combine_inverse_variance`
   only guards on `scale` (both are `standardized_mean_diff`), so it would
   *silently* pool these two if both were handed to it. Both estimates also
   share `POPULATION_STRENGTH` with `outcome="strength"`, so `_merge_populations`
   would not catch the difference either. A `_POOLABLE_OVERRIDE` in the registry
   is therefore the *correct and necessary* mechanism — the scale/outcome guards
   in `shared.py` are not enough on their own. The module is right to rely on it
   and right to flag it loudly in both the docstring and the inline comment on
   `LOAD_STRENGTH_ESTIMATES`.

One caveat for the registry author: the override must actually exist and must
designate the 1RM estimate. This audit verified the *module's* intent and
documentation; it did **not** inspect the registry file, so the existence and
correctness of `_POOLABLE_OVERRIDE` is **UNVERIFIED** here and should be checked
separately. If the override is missing, `LOAD_STRENGTH_ESTIMATES` (a 2-element
list) handed to `combine_inverse_variance` would produce a nonsensical pooled
"strength" effect.

Filing both under one `load → strength` topic while keeping only 1RM poolable
is a reasonable design — it preserves the isometric estimate as visible
context/corroboration without letting it contaminate the pooled number.

---

## Disambiguation from `schoenfeld_2017.py`

**Confirmed distinct, and the module handles it correctly.** The two papers:

| | `schoenfeld_load_2017.py` (this) | `schoenfeld_2017.py` (sibling) |
|---|---|---|
| Topic | Load / rep-range → strength & hypertrophy | Weekly volume → hypertrophy |
| Journal | J Strength Cond Res 31(12):3508-3523 | J Sports Sciences 35(11):1073-1082 |
| DOI | 10.1519/JSC.0000000000002200 | 10.1080/02640414.2016.1210197 |
| Authors | Schoenfeld, **Grgic**, Ogborn, Krieger | Schoenfeld, Ogborn, Krieger |
| n studies | 21 | 15 |

The DOIs and journals are different and correctly encoded in each module's
`CITATION`. The new module's docstring opens with an explicit "NOT to be
confused with schoenfeld_2017.py" note naming Grgic as the distinguishing
fourth author and the JSCR-vs-JSS journal split. The two modules do not share
estimates, scales, or population objects. No confusion or duplication detected.
The `CITATION.authors` string "Schoenfeld, Grgic et al." correctly surfaces
Grgic so `Citation.short()` won't collide with the sibling. Good.

---

## Concerns & discrepancies

**1. (POTENTIALLY MATERIAL — UNRESOLVED) Hypertrophy 95% CI / SE conflict.**
The module encodes hypertrophy `se=0.05` and comments "(95% CI −0.08–0.14)".
Schoenfeld's *own* 2021 review (PMC7927075, "Loading Recommendations / Repetition
Continuum") quotes this exact 2017 result as: *"The trivial effect size
difference (0.03) and relatively narrow 95% confidence intervals (−0.16 to
0.22)..."*. That is a substantially wider interval. Meanwhile a cached
Results-fragment returned by the search index reads "ES = 0.03 ± 0.05; CI:
−0.08 to 0.14; p = 0.56", which matches the module exactly.

So there are **two conflicting candidate intervals** for the same result:
   - **−0.08 to 0.14** (module + one search fragment) → implies SE ≈ 0.05
   - **−0.16 to 0.22** (Schoenfeld's own later review) → implies SE ≈ 0.097

These cannot both be the paper's reported study-level CI. Possible explanations:
(a) the −0.16 to 0.22 interval in the 2021 review is the *mean-ES* analysis CI,
not the study-level one, and the 2021 review (or the auditor's reading of it)
conflated the two — in which case the module is correct; (b) the module
mistranscribed the study-level CI and the SE is wrong by ~2×; (c) one of the two
is a different sub-analysis. **I could not resolve this without the full text,
which was unreachable.** This is the highest-priority open item. If the true
study-level SE is ~0.097 rather than 0.05, the encoded estimate's `precision`
(1/se²) is overstated ~3.8× — it would receive nearly 4× too much weight in any
inverse-variance pool, and its `ci_95` would be far too narrow. **Flagged as
UNVERIFIED; must be checked against Table 2 / the Figure 4 forest plot before
this estimate is trusted in pooling.**

**2. (UNVERIFIED) SEMs (0.16 / 0.11 / 0.05) and isometric/hypertrophy CIs.**
The module states all three SEs are "the paper-reported SEM (Results / Table
2); no recovery needed." Only the 1RM "± 0.16" is independently corroborated
(search index, "0.58 ± 0.16"). The isometric "± 0.11" and hypertrophy "± 0.05"
were not reachable in a clean primary source. Reporting-transparency was scored
0.80 on the premise that SEs were read directly; if any were reconstructed from
a p-value, the rubric caps that dimension at 0.6 and the quality score would
fall. Mark UNVERIFIED.

**3. (UNVERIFIED) Per-analysis study counts 14 / 8 / 10.** Only the 1RM "14
studies" is independently confirmed (Schoenfeld 2021 review, verbatim). The
isometric "8 studies" is strongly corroborated (search index repeatedly says 8
studies / 23 ES for the isometric forest plot). The hypertrophy "10 studies" is
**not** independently confirmed — the abstract gives only the 21-study total,
and the search index conflated the three analyses. 14 + 8 + 10 = 32 forest-plot
slots from a 21-study pool, which is internally plausible (studies appear in
multiple plots) but unconfirmed for the hypertrophy figure specifically.

**4. (UNVERIFIED) Participant n's (231 / 497 / 176).** Depend on Table 1, not
reached. See Math check #1. The encoder's "sum all arms" approach is defensible
but the module should not present these as exact (the tilde hedging helps).

**5. (UNVERIFIED) Sensitivity-analysis specifics.** The caveats — "5 influential
studies", "removing the 3 most influential pushes p to 0.22–0.46", "removing Van
Roie 2013b shifts the isometric interval" — are detailed and specific but could
not be checked against the paper's sensitivity table. They are plausible and
the module presents them honestly as caveats; just unverified.

**6. (MINOR — wording) Mean-ES vs study-level framing.** The module is *careful*
and *correct* to encode the study-level forest-plot "Overall ES" rather than the
per-load ES (1.69/1.32) or the mean-ES difference. This is exactly the right
quantity and the docstring explains the choice well. The only nit: caveat #2
asserts the mean-ES hypertrophy analysis "showed a non-significant trend
(p=0.10)". The search index returned a "D = −0.11 ± 0.06 (CI −0.24 to 0.03;
p=0.10)" fragment but attributed it ambiguously across outcomes. The p=0.10
trend claim is plausible and internally coherent but **unverified** — treat it
as such.

**7. (MINOR) Single shared QUALITY across three estimates.** All three
estimates carry `quality_score=0.77`, but the per-dimension scores that produce
0.77 (sample size, measurement quality) genuinely differ between the
larger/direct-measure 1RM analysis and the smaller isometric analysis. The
isometric estimate is mildly over-scored (its isometric-MVC measurement would be
~0.7 not 0.85; its n≈176 is the 0.7 band not 0.75). Impact is small and a single
shared score is a reasonable simplification, but worth a one-line acknowledgement.

**8. Full text not reached — transparency.** Per the QUALITY_RUBRIC flat
modifier list, "Sci-Hub-only access; can't verify methods" carries a ×0.9
penalty. The intent of that modifier — a slight haircut when the methods/
supplement cannot be inspected — arguably applies here too: the auditor (and,
it appears, the encoder, who concedes "the COI statement could not be inspected
in the obtained copy") could not read Table 1, Table 2, or the forest plots. The
module did **not** apply any such modifier. This is a judgement call: the
encoder evidently *did* have *some* copy of the paper (the per-load ES and
sensitivity details are too specific to come from the abstract). If the encoder
genuinely read the full text and only the COI page was unreadable, no modifier
is needed. If the encoder also worked from a partial copy, a ×0.9 (→ 0.69) would
be defensible. Recommend the encoder state explicitly which copy they used.

---

## Recommendations

1. **Resolve the hypertrophy CI conflict before this estimate is pooled
   (highest priority).** Obtain the JSCR full text (or a complete PDF) and read
   the Figure 4 forest plot and Table 2 for the hypertrophy study-level result.
   Confirm whether the study-level 95% CI is **−0.08 to 0.14** (SE ≈ 0.05, as
   encoded) or **−0.16 to 0.22** (SE ≈ 0.097, as Schoenfeld's 2021 review
   states). If the latter, change `se=0.05` → `se≈0.097` and fix the inline
   comment. Until resolved, annotate `LOAD_HYPERTROPHY_HIGH_VS_LOW.notes` that
   the SE is provisional.
2. **Verify the SEMs 0.11 (isometric) and 0.05 (hypertrophy)** against Table 2.
   If either was reconstructed rather than read, drop the Reporting-transparency
   dimension to ≤0.6 and recompute QUALITY.
3. **Re-sum Table 1** for the hypertrophy 10-study forest plot and confirm
   `n=231`; do the same for 497 and 176. Until then, keep the tilde hedging and
   consider adding "(encoder-estimated from Table 1)" to the inline `n` comments.
4. **Confirm the hypertrophy study count = 10** from the Figure 4 forest plot
   (the only one of the three counts not independently corroborated here).
5. **Verify the registry `_POOLABLE_OVERRIDE` actually exists** and designates
   the 1RM estimate. The scale/outcome guards in `shared.py` will NOT prevent
   1RM and isometric from being silently pooled — the override is load-bearing.
6. **Consider per-estimate quality scores**, or at least a one-line note that
   the shared 0.77 mildly over-credits the smaller isometric analysis on sample
   size and measurement quality.
7. **State which copy of the paper the encoder used.** If only a partial copy,
   consider the rubric's ×0.9 "can't verify methods" modifier (0.77 → 0.69).
8. **Once the full text is in hand**, verify caveat #2's specifics: the mean-ES
   trend p=0.10, the "5 influential studies", and the "remove 3 → p=0.22–0.46"
   claim, plus the Van Roie 2013b isometric sensitivity note.

### What is solid and needs no change
- The 1RM estimate (ES 0.58, CI 0.28–0.89, p=0.002, 14 studies) — fully
  confirmed against two independent sources.
- Load definitions (≤60% / >60% 1RM) and the "all sets to momentary muscular
  failure" hard scope limit — confirmed verbatim from the inclusion criteria.
- Disambiguation from the sibling volume MA — correct, explicit, no confusion.
- The 1RM-vs-isometric non-poolability reasoning — sound and well-argued.
- Quality-score arithmetic — 0.7685 → 0.77 is correct.
- Citation metadata (journal, volume, pages, DOI, PMID) — exact match to PubMed.
- The choice to encode the study-level "Overall ES" rather than per-load ES or
  mean-ES difference — the correct quantity, clearly documented.

---

## Encoder reconciliation (2026-05-17, post-audit)

This audit was access-limited (every full-text mirror was blocked). The
encoder, however, had read the complete full text (the open-access PDF
mirror, all 16 pages incl. Table 1, Table 2, Table 3 and the three forest
plots). The audit's UNVERIFIED items are reconciled here:

- **The hypertrophy CI conflict — CONFIRMED, and it is real.** The audit's
  central finding is correct: Schoenfeld/Grgic 2017 is internally
  inconsistent. The Results text states the study-level hypertrophy ES as
  "0.03 ± 0.05 (SEM); CI: −0.08 to 0.14", while the Figure 4 forest-plot
  diamond shows "0.03 [−0.16, 0.22]". Both are in the paper. The same
  text-vs-figure discrepancy exists for isometric strength (text −0.10 to
  0.41 vs Figure 3 −0.06 to 0.37); 1RM is consistent (0.28–0.89 both).
  **Resolution:** the module now encodes the hypertrophy `se` as **0.097**
  (the wider Figure 4 interval) rather than 0.05 — the conservative choice,
  which avoids overstating a near-zero estimate's pooling weight. The
  isometric `se` stays 0.11 (the reported SEM, which matches Figure 3). Both
  estimate `notes` and the module docstring now document the inconsistency.
- **n_studies (14 / 8 / 10)** — CONFIRMED from the Results text ("84 ESs from
  14 studies"; "23 ESs from 8 studies"; "41 ESs from 10 studies").
- **Participant n (497 / 176 / 231)** — CONFIRMED by summing Table 1 across
  each analysis's forest-plot studies. (Includes all study arms; the paper
  reports no per-analysis participant total — an upper-bound proxy, as the
  module notes.)
- **Sensitivity analysis** — CONFIRMED from Table 3: removing the 3 most
  influential studies moved the hypertrophy difference to p=0.22–0.46; the
  mean-ES trend was p=0.10. caveat #2 in the module is accurate.
- **The 1RM estimate, load definitions, failure scope limit, quality
  arithmetic, and volume-MA disambiguation** — all confirmed (the audit
  already verified these via secondary sources).

No other encoded value changed. **Verdict after reconciliation: ACCURATE** —
the one MATERIAL-risk item (the hypertrophy SE) is resolved conservatively and
the paper-internal inconsistency is now documented in the module itself.
