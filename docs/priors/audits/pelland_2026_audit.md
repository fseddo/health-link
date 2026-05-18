# Literature Audit — Pelland et al. 2026 (`pelland_2026.py`)

**Audited module:** `priors-handoff/app/priors/pelland_2026.py`
**Paper:** Pelland JC, Remmert JF, Robinson ZP, Hinson SR, Zourdos MC. "The Resistance
Training Dose Response: Meta-Regressions Exploring the Effects of Weekly Volume and
Frequency on Muscle Hypertrophy and Strength Gains." *Sports Medicine* 2026;56(2):481-505.
DOI 10.1007/s40279-025-02344-w.
**Audit date:** 2026-05-17
**Auditor:** Independent literature auditor (re-read paper from scratch; did not trust the encoding)

---

## Sources accessed

| Source | URL | Accessed? | Notes |
|---|---|---|---|
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/41343037/ | Yes | Abstract + affiliations + COI |
| Full-text PDF (open mirror) | https://www.fisiologiadelejercicio.com/wp-content/uploads/2025/12/The-Resistance-Training-Dose-Response.pdf | **Yes — full 25-page text** | Primary source for this audit. Extracted and read pages 1-21 verbatim. |
| Springer journal page | https://link.springer.com/article/10.1007/s40279-025-02344-w | No | Redirects to an auth gate; not needed (full text obtained elsewhere). |
| OSF project | https://osf.io/6z3xu | Not fetched | Project landing page only; raw datasets/supplementary CSVs not downloaded. Items requiring the OSF dataset are marked UNVERIFIED below. |

The full text was the open-access mirror PDF, which carries the published Springer
typesetting (`https://doi.org/10.1007/s40279-025-02344-w`, "Sports Medicine", accepted
14 Oct 2025). All page/section/table references below are to that PDF and match the
published article. The abstract was independently cross-checked against PubMed.

---

## Verdict

**MINOR DISCREPANCIES.**

The four effect estimates (point estimates and 95% credible intervals) are reproduced
**exactly** from the paper, on the correct scales, and the SE-recovery arithmetic and the
0.94 quality score are correct. The posterior probabilities and SDES values are correct.
However, several non-trivial issues exist: (1) the **population spec is wrong** —
`VOLUME_HYPERTROPHY_SLOPE` / `FREQUENCY_HYPERTROPHY_SLOPE` are tagged `training_status="trained"`
when the underlying regressions pooled **both untrained and trained** participants (the
study is `mixed`, and "trained" is only adjusted for as a covariate); (2) the `n` values
are wrong — hypertrophy regressions had **n=1032** (correct) but the module reuses 1032
for the hypertrophy *frequency* slope, which is fine, yet the **age_range (18,40) is not
stated anywhere in the paper** and is an inference; (3) the **strength curve-fit constants
do not reproduce the reported 0.21%/set marginal slope** — the encoded reciprocal model
yields ~0.287%/set at the reference volume; (4) the docstring claim that the CrI is
"symmetric on the log scale" is unsupported and slightly misleading. None of these
corrupt the headline effect sizes, hence MINOR rather than MATERIAL, but the population
mislabel will distort `applicability_to()` routing and should be fixed.

---

## Value-by-value verification

### Effect estimates

| Encoded value | Paper value | Match? | Source |
|---|---|---|---|
| VOLUME_HYPERTROPHY mean 0.24 | β = 0.24% | YES | §3.6.1 p.14; §4.4 p.18 |
| VOLUME_HYPERTROPHY CI 0.15–0.33 | 95% CrI 0.15, 0.33 | YES | §3.6.1 p.14 |
| VOLUME_STRENGTH mean 0.21 | β = 0.21% | YES | §3.6.2 p.15 |
| VOLUME_STRENGTH CI 0.16–0.26 | 95% CrI 0.16, 0.26 | YES | §3.6.2 p.15 |
| FREQUENCY_HYPERTROPHY mean 0.32 | β = 0.32% | YES | §3.5.1 p.13 |
| FREQUENCY_HYPERTROPHY CI −0.14–0.82 | 95% CrI −0.14, 0.82 | YES | §3.5.1 p.13 |
| FREQUENCY_STRENGTH mean 3.27 | β = 3.27% | YES | §3.5.2 p.13 |
| FREQUENCY_STRENGTH CI 2.74–3.84 | 95% CrI 2.74, 3.84 | YES | §3.5.2 p.13 |
| Scale: volume = `pct_per_fractional_set` | "% Muscle Size Per Set" / "% Maximal Strength Per Set" | YES | Fig. 7B, Fig. 8B |
| Scale: frequency = `pct_per_session_per_week` | "% Muscle Size Per Session" / "% Maximal Strength Per Session" | YES | Fig. 5B, Fig. 6B |
| "Marginal slope at mean volume of 12.25 fractional sets/wk" | "0.24% ... per additional set at the average 'fractional' weekly volume of 12.25 sets" | PARTIAL — see Concern C1 | §4.4 p.18 |
| "Square-root best-fit model" (hypertrophy volume) | square root model was best fit | YES | §3.6.1 p.14 |
| "Reciprocal best-fit" (volume→strength) | reciprocal model was best fit | YES | §3.6.2 p.15 |
| Frequency models reciprocal | reciprocal model best fit for both | YES | §3.5.1, §3.5.2 |

### Posterior probabilities

| Encoded note | Paper value | Match? | Source |
|---|---|---|---|
| Volume→hypertrophy P(slope>0)=1.00 | 100% | YES | §3.6.1 p.14 |
| Volume→strength P(slope>0)=1.00 | 100% | YES | §3.6.2 p.15 |
| Frequency→hypertrophy P(slope>0)=0.913 | 91.3% | YES | §3.5.1 p.13; §4.2 |
| Frequency→strength P(slope>0)=1.00 | 100% | YES | §3.5.2 p.13 |
| Freq→strength note "1→2 sessions: +4.6%" | ES 12.72% (freq 1) → 17.32% (freq 2) = +4.60% | YES | §4.3 p.17 |

### Sample sizes & study counts

| Encoded value | Paper value | Match? | Source |
|---|---|---|---|
| n=2058 total | 2058 participants | YES | Abstract; §3.3 p.10 |
| 67 studies | 67 studies | YES | Abstract; §3.1 p.8 |
| 28 untrained / 39 trained studies | 28 untrained, 39 trained | YES | §3.3 p.10 |
| VOLUME_HYPERTROPHY n=1032 | 1032 participants (35 studies, 220 effects) | YES | §3.6.1 p.14 |
| FREQUENCY_HYPERTROPHY n=1032 | 1032 participants (35 studies, 220 effects) | YES | §3.5.1 p.12 |
| VOLUME_STRENGTH n=2020 | 2020 participants (66 studies, 490 effects) | YES | §3.6.2 p.15 |
| FREQUENCY_STRENGTH n=2020 | 2020 participants (66 studies, 490 effects) | YES | §3.5.2 p.13 |

Note: the strength regressions used 2020 participants and **66** studies (not all 67);
the hypertrophy regressions used only **35** studies / 1032 participants. The module's
`n` fields are correct, but see Concern C2 about the population specs.

### Population spec

| Encoded value | Paper value | Match? | Source |
|---|---|---|---|
| 79.1% male / 20.9% female | 79.1% male, 20.9% female | YES | Abstract; §3.3 p.10 |
| 25.16 ± 5.22 years | mean age 25.16 ± 5.22 years | YES | Abstract; §3.3; §4.6 p.19 |
| "~10-week interventions" | mean 10.42 ± 4.48 weeks | YES (rounds to ~10) | §3.3 p.10; §4.6 p.19 |
| `age_range=(18, 40)` "95% of participants within this range" | **NOT STATED** | **NO — see Concern C3** | n/a |
| `sex="mixed"` | Pooled mixed-sex cohort | YES | §3.3 |
| `training_status="trained"` on hypertrophy/strength estimates | Regressions pool untrained **and** trained; status is a covariate | **NO — see Concern C2** | §2.7, §3.3 |

### Quality score

| Encoded value | Recomputed | Match? |
|---|---|---|
| QUALITY = 0.94 | 0.935 → rounds to 0.94 | YES (see Math checks) |

### Derived content

| Encoded value | Paper value | Match? | Source |
|---|---|---|---|
| SDES_HYPERTROPHY_PCT = 2.05 | "2.05% ... for hypertrophy" | YES | §2.6 p.4; Table 3 |
| SDES_STRENGTH_PCT = 3.96 | "3.96% ... for strength" | YES | §2.6 p.4; Table 4 |
| HYPERTROPHY_TIERS (4 / 5-10 / 11-18 / 19-29 / 30-42 / 43+) and per-tier "~6 / ~8.5 / ~10.75 / ~12.5 additional sets" | Table 3 exactly | YES | Table 3 p.14 |
| STRENGTH_TIERS (MED=1 / 2 / 3-4 / 5+) and "~0.75 / ~2.25 additional sets" | Table 4 exactly | YES | Table 4 p.15 |
| `fractional_set_count`: DIRECT=1.0, INDIRECT=0.5 | "'fractional' counted indirect sets as half a set (indirect × 0.5 + direct)" | YES | §2.5 p.3-4 |
| HYPERTROPHY_CLASSIFICATIONS direct/indirect exercise lists | Table 1 | YES (see Concern C7) | Table 1 p.5 |
| `predicted_hypertrophy_pct` (a=1.68) | Author's own curve, not from paper | APPROXIMATION — see Concern C5 | — |
| `predicted_strength_pct` (c=25.0, k=0.4) | Author's own curve, not from paper | **DOES NOT MATCH reported slope** — see Concern C5 | — |

---

## Math checks

### SE recovery — `SE = (upper − lower) / (2 × 1.96)`

| Estimate | CI | Recomputed SE | Inline comment | Match? |
|---|---|---|---|---|
| Volume → hypertrophy | 0.15, 0.33 | 0.0459 | 0.046 | YES |
| Volume → strength | 0.16, 0.26 | 0.0255 | 0.026 | YES |
| Frequency → hypertrophy | −0.14, 0.82 | 0.2449 | 0.245 | YES |
| Frequency → strength | 2.74, 3.84 | 0.2806 | 0.281 | YES |

All four inline-comment SE values are arithmetically correct.

**Symmetry check.** The midpoint of each CI vs. the reported point estimate:

- Volume→hypertrophy: midpoint 0.240 = point 0.24 (symmetric).
- Volume→strength: midpoint 0.210 = point 0.21 (symmetric).
- Frequency→hypertrophy: midpoint 0.340 vs. point **0.32** (point sits 0.02 *below* midpoint).
- Frequency→strength: midpoint 3.290 vs. point **3.27** (point sits 0.02 *below* midpoint).

So the credible intervals are mildly **right-skewed** for both frequency slopes — the
posterior has a longer upper tail. The module docstring claims "The 95% CrI in the paper
is symmetric on the log scale." This is **not supported by the paper**: the paper reports
*quantile-based* (quartile-based) compatibility intervals from the posterior on the
response-ratio percentage scale (§3.5, Fig. 5/6 captions), not log-symmetric intervals.
Treating these as symmetric-Normal `mean ± 1.96·SE` is a reasonable engineering
approximation but the *justification given is wrong*. The approximation is worst for
`FREQUENCY_HYPERTROPHY_SLOPE`: a Normal(0.32, 0.245) implies P(slope>0) ≈ 0.904, whereas
the paper's actual posterior probability is 0.913 — close, but the encoded Normal
slightly understates the mass above zero and, more importantly, the wide skewed interval
crossing zero is exactly the case where a symmetric-Normal surrogate is least faithful.
This is acceptable for inverse-variance pooling but should be flagged in the notes.

### Quality score recomputation

Per-dimension scores from the module comments, weights from `QUALITY_RUBRIC.md` v1.0:

```
design   0.85 × 0.20 = 0.1700
sample   1.00 × 0.15 = 0.1500
measure  0.95 × 0.20 = 0.1900
method   1.00 × 0.15 = 0.1500
report   1.00 × 0.10 = 0.1000
ROB      0.85 × 0.10 = 0.0850
pop      0.90 × 0.10 = 0.0900
                       ------
weighted average     = 0.9350  → rounds to 0.94
```

`QUALITY = 0.94` is **correct** and matches the worked example in `QUALITY_RUBRIC.md`
(§"Pelland et al. 2026", which also derives 0.935 → 0.94). No modifiers apply.

**Defensibility of the dimension scores against the paper:**

- Study design 0.85 — meta-analysis of RCTs, pre-registered on OSF (osf.io/r958n).
  Rubric tier 0.8 = "meta-analysis of RCTs with pre-registered protocol". The paper
  states "some of the methods have changed since the original pre-registration" (§2),
  and inclusion criteria allowed pre-prints, theses, and abstracts (§2.1) — i.e. not
  purely peer-reviewed RCTs. 0.85 is slightly generous; 0.80–0.85 both defensible.
- Sample size 1.00 — 2058 total, well above the rubric's ≥800 threshold. Correct.
- Measurement 0.95 — hypertrophy restricted to direct site-specific MT/CSA/MRI/biopsy
  (§2.1 criterion 6). **But the strength outcome included estimated 1RM, isometric, and
  isokinetic measures** (Table 2 lists "estimated 1RM", "peak torque"), which the rubric
  scores 0.5–0.7. A single 0.95 covering both outcomes slightly over-credits the
  strength estimates' measurement quality. Minor.
- Methodological rigor 1.00 — Bayesian multi-level meta-regression, 7 functional forms
  compared via Bayes factors, sensitivity analyses, two-stage + contrast-based
  verification. Fully defensible.
- Reporting 1.00 — full dataset, R scripts, plots, supplementary on OSF. Defensible.
- Risk of bias 0.85 — all authors disclose they are "coaches and writers in the fitness
  industry"; no funding; no conflict specific to this article. Rubric says don't go
  below 0.6 just for industry ties; 0.85 is appropriate.
- Population specificity 0.90 — clear inclusion/exclusion criteria, age/sex/training
  status reported. Defensible, though see Concern C3 (the age *range* is not given).

Conclusion: 0.94 is correct arithmetic and broadly defensible. The strongest argument
for a small downgrade would be measurement quality for the *strength* estimates
specifically (estimated-1RM/isokinetic content), which the single global score hides.

### Curve-fit constant checks

`predicted_hypertrophy_pct`: `a·√x` with derivative `a/(2√x)`. Setting the derivative at
x=12.25 equal to 0.24 gives `a = 0.24 · 2 · √12.25 = 1.68`. The encoded `a=1.68` is
**internally consistent** with the 0.24%/set marginal slope. (The curve itself is the
module author's reconstruction, not a curve from the paper — the paper reports the
marginal slope and best-fit family but not the fitted intercept/coefficient.)

`predicted_strength_pct`: `c·(1 − 1/(1+kx))` with `c=25.0, k=0.4`. Derivative is
`c·k/(1+kx)²`. At the volume-strength reference (mean fractional volume 8.14, §4.3) the
derivative is 0.299; at 12.25 it is **0.287**. Either way this is **~40% larger than the
reported 0.21%/set marginal slope**. The docstring claims the curve is "calibrated to
0.21%/set at mean" — it is **not**. To hit 0.21%/set at x=12.25 with this functional
form and c=25.0 you would need k≈0.27 (giving derivative 0.21 at x=12.25), or a different
c. **This is a real bug**: the encoded strength curve is not consistent with the paper's
slope. It also predicts ~20.8% strength gain at 12.25 sets and 7.1% at one set, neither
of which is anchored to a paper-reported value.

---

## Concerns & discrepancies

**C1 — "12.25 fractional sets/wk" is the volume-on-hypertrophy reference, not a global mean.**
The paper states the 0.24%/set slope is evaluated "at the average 'fractional' weekly
volume of 12.25 sets" (§4.4) — this is the mean fractional volume *in the hypertrophy
volume regression*. The module attaches "Marginal slope at mean volume of 12.25
fractional sets/wk" to `VOLUME_HYPERTROPHY_SLOPE` (correct) **and** the curve-fit comments
treat 12.25 as the calibration point for the *strength* curve too. But §3.3 reports the
strength training-group mean fractional volume as **8.14 ± 6.23 sets/wk** and the
hypertrophy training-group mean as **13.00 ± 8.87** (median 10.5). The marginal strength
slope of 0.21%/set is evaluated at the strength model's own mean, which is ~8, not 12.25.
Using 12.25 to calibrate the strength curve is doubly wrong (wrong reference volume *and*
wrong resulting k). Low impact on the `EffectEstimate` objects (their means/CIs are
correct), but the predictive functions inherit the error.

**C2 — Population `training_status` is mislabelled "trained" (MATERIAL for routing).**
`VOLUME_HYPERTROPHY_SLOPE` and `FREQUENCY_HYPERTROPHY_SLOPE` use
`POPULATION_TRAINED_MIXED_SEX` (`training_status="trained"`), and the volume/frequency
strength slopes use `POPULATION_TRAINED_STRENGTH` (`training_status="trained"`). The
paper's primary meta-regressions **pool untrained and trained participants** and include
training status only as a binary covariate ("All models were adjusted for ... training
status", §2.7; 28 untrained + 39 trained studies, §3.3). The marginal slopes are
"proportionally marginalized across the categorical fixed effect (i.e., training status)"
(Fig. 5-8 captions) — i.e. they are *averaged over* untrained and trained, not specific
to trained lifters. The correct `training_status` for all four estimates is **`"mixed"`**.
This matters: `shared.py:applicability_to()` multiplies score by 0.85 when the spec is
`"mixed"` and the user is e.g. `"trained"`, but by **0.5** when the spec says `"trained"`
and the user is `"untrained"`. With the current mislabel, an untrained user is wrongly
penalised 0.5× and a trained user wrongly gets a perfect 1.0. The module even documents
"39 trained studies" / "28 untrained studies" in its own comments, contradicting its own
`PopulationSpec`. `POPULATION_UNTRAINED_*` specs are defined but **never used** by any
`EffectEstimate` — dead code that should be removed or the estimates re-pointed.

**C3 — `age_range=(18, 40)` is not in the paper (UNVERIFIED / likely fabricated).**
The paper reports only mean age **25.16 ± 5.22 years** and that participants >70 years
were *excluded* (§2.1 criterion 4); it describes the cohort as "predominantly young
adults" (§4.6). It never states an 18-40 range, and the inline comment "95% of
participants within this range" has no basis in the text. A Normal(25.16, 5.22) has its
central 95% at roughly 14.9-35.4, not 18-40 — and individual studies set their own age
limits. The lower bound 18 is plausible (most RT studies recruit ≥18) but is an
assumption; 40 as an upper bound is an invention. Recommend either widening the documented
basis or relabelling the comment honestly as an assumption. Mark **UNVERIFIED**.

**C4 — Strength `n` and study count nuance.** Strength regressions used 2020 participants
across **66** studies / 490 effects (§3.5.2, §3.6.2); hypertrophy used 1032 across **35**
studies / 220 effects. The module's `n` values (2020, 1032) are correct. No fix needed,
but the population `notes` ("39 studies", "strength assessment population") are loose —
the "39 trained studies" figure is the trained subset of all 67, not the count in any
single regression.

**C5 — `predicted_strength_pct` is not consistent with the reported slope (BUG).**
See Math checks. The reciprocal curve `25·(1 − 1/(1+0.4x))` has a marginal slope of
~0.287%/set at x=12.25 (and ~0.30 at the true strength reference x≈8), versus the paper's
0.21%/set. The docstring's "calibrated to 0.21%/set at mean" is false. Additionally, the
paper's strength model is a *reciprocal of volume* fit on the exponentiated-response-ratio
scale with a "functional plateau"; the plateau height (`c`) of 25% is not a paper-reported
number. `predicted_hypertrophy_pct` is at least internally consistent (a=1.68 ⇒ 0.24%/set
at 12.25) but the √-curve intercept is still a reconstruction. Both functions are flagged
"For production: refit against the OSF dataset" — good — but the strength one is
shipping a wrong derivative *now* and any optimizer using it today is mis-calibrated.

**C6 — Frequency slope is "per session per week" but interpretation needs care.**
`FREQUENCY_*_SLOPE.scale = "pct_per_session_per_week"` matches the paper's axis labels
("% ... Per Session"). Fine. But note the frequency variable in the paper is itself
*fractional* frequency (indirect sessions × 0.5), exactly as for volume (§2.5 examples
give fractional frequency of 1.5 and 2.5). The scale string and notes don't say
"fractional" for frequency the way they do for volume. Minor labelling inconsistency;
recommend `"pct_per_fractional_session_per_week"` or a note.

**C7 — Fractional set counting (direct=1.0 / indirect=0.5) is genuinely Pelland's method.**
Confirmed: §2.5 — "'fractional' counted indirect sets as half a set (indirect × 0.5 +
direct)". The 0.5 weight is the paper's method, and the paper found "strong"/"very strong"
Bayes-factor evidence favouring it over 'total' (1.0) and 'direct' (0.0) (§3.4). Two
caveats the module should carry: (i) the paper explicitly calls 0.5 "still an assumption"
and "a heuristic ... rather than a definitive standard" (§4.1) — the module's docstring
presents it more confidently than the authors do; (ii) the `HYPERTROPHY_CLASSIFICATIONS`
dict faithfully transcribes Table 1, **but** Table 1 also lists `rectus_femoris`
(direct: leg extension; indirect: smith machine squat, leg press, squat) and `trapezius`
(indirect: lat pulldown, seated row) which the module **omits**. Conversely the module's
generic `quadriceps` entry merges Table 1's "Quadriceps/knee extensors/vastus..." row.
Not wrong, but incomplete relative to the paper, and `fractional_set_count` returns 0.0
for any unlisted exercise — silent under-counting. The strength-side classifications
(Table 2, much larger) are **not encoded at all**; `fractional_set_count` is hypertrophy-only
despite the paper applying fractional counting to strength too.

**C8 — `outcome` field on populations.** `POPULATION_TRAINED_MIXED_SEX` has
`outcome="hypertrophy"` and is reused for `FREQUENCY_HYPERTROPHY_SLOPE` — consistent.
`POPULATION_TRAINED_STRENGTH` has `outcome="strength"`. Fine.

**Items requiring OSF raw data to fully confirm (UNVERIFIED):**
- Exact posterior SDs / whether the published CrIs are exactly quantile-based vs HDI
  (paper says "quartile-based ... credible and prediction intervals", §3.5 caption —
  consistent with the module treating them as 95% CrI, but the precise posterior shape
  is on OSF only).
- The fitted intercepts/coefficients of the square-root and reciprocal best-fit models
  (the paper reports marginal slopes and model family, not the full coefficient vector;
  full model summary tables are "in the supplementary materials", §3.5/§3.6).

---

## Recommendations

Concrete fixes, roughly in priority order:

1. **Fix the population `training_status` (C2).** Change `POPULATION_TRAINED_MIXED_SEX`
   and `POPULATION_TRAINED_STRENGTH` to `training_status="mixed"` (rename to
   `POPULATION_MIXED_*`). The primary regressions pool untrained+trained and marginalize
   over status. Delete the unused `POPULATION_UNTRAINED_*` specs or document why they
   exist. This is the highest-impact fix because it changes `applicability_to()` routing.

2. **Fix `predicted_strength_pct` (C5).** Either re-derive `k` so the derivative equals
   0.21%/set at the strength model's reference volume (~8 fractional sets, per §3.3 — not
   12.25), or replace the function with an honest "not yet refit — do not use in
   optimizer" stub. As shipped it mis-states its own calibration and is ~40% too steep.

3. **Correct the curve-fit reference volume (C1).** The 12.25 figure is the *hypertrophy*
   volume regression mean; the strength regression mean fractional volume is 8.14 (§3.3,
   §4.3). Don't reuse 12.25 for strength.

4. **Rewrite the "symmetric on the log scale" docstring claim (Math checks).** The paper
   uses quantile-based posterior compatibility intervals on the percentage scale, and
   the frequency CrIs are mildly right-skewed. State plainly: "We approximate the
   posterior as Normal(mean, SE) for pooling; the paper's CrIs are quantile-based and
   slightly asymmetric, so this is an engineering approximation — worst for
   FREQUENCY_HYPERTROPHY_SLOPE whose interval crosses zero."

5. **Re-document `age_range` honestly (C3).** The paper gives mean 25.16 ± 5.22 y and
   excludes >70 y; it does not state an 18-40 range. Either change the comment to
   "assumption: most included RT studies recruit 18-40 y; paper reports only mean
   25.16 ± 5.22" or set a range actually supported by the data.

6. **Soften the fractional-counting docstring and complete the tables (C7).** Note that
   the authors call the 0.5 weight "a heuristic ... not a definitive standard" (§4.1).
   Add the missing Table 1 rows (`rectus_femoris`, `trapezius`); decide whether the
   silent `return 0.0` for unclassified exercises is desired (it causes under-counting)
   — at minimum log/flag it. Encode Table 2 (strength) or document that strength
   fractional counting is intentionally out of scope.

7. **Minor: scale string for frequency (C6).** Consider
   `"pct_per_fractional_session_per_week"` and add "fractional" to the frequency notes
   for parity with the volume estimates.

8. **Optional: quality score note (Math checks).** 0.94 is correct, but consider a note
   that the 0.95 measurement-quality score is hypertrophy-grade; the strength estimates'
   underlying measures include estimated 1RM / isokinetic torque (Table 2), which the
   rubric would score lower. Not required — the global 0.94 is within rubric variance.

**Not a problem (verified correct, no action):** all four point estimates and 95% CrIs;
all four SE recoveries; all four posterior probabilities; n=2058 / 1032 / 2020; 67 / 28 /
39 study counts; SDES 2.05% and 3.96%; both efficiency-tier tables (Tables 3 & 4
verbatim); the direct=1.0/indirect=0.5 fractional weighting; the "1→2 sessions +4.6%"
note; the 0.94 quality arithmetic; best-fit model families (square-root for
volume→hypertrophy, reciprocal for the other three).
