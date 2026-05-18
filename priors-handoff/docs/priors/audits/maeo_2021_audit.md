# Audit — `maeo_2021.py`

**Module audited:** `priors-handoff/app/priors/maeo_2021.py`
**Source paper:** Maeo S, Huang M, Wu Y, Sakurai H, Kusagawa Y, Sugiyama T,
Kanehisa H, Isaka T. "Greater Hamstrings Muscle Hypertrophy but Similar Damage
Protection after Training at Long versus Short Muscle Lengths." *Medicine &
Science in Sports & Exercise.* 2021;53(4):825–837.
DOI: 10.1249/MSS.0000000000002523 · PMID: 33009197 · PMC7969179
**Date:** 2026-05-17
**Auditor:** independent priors-layer auditor

---

## Sources accessed

| Source | URL | Full text obtained? |
|---|---|---|
| PMC open-access record (HTML) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7969179/ | Partial — body text extracted; demographics not present in HTML |
| Open-access PDF mirror (uniguacu.com.br) | https://uniguacu.com.br/wp-content/uploads/2023/09/Artigo-Hipertrofia-muscular-dos-isquiotibiais-maiores.pdf | **YES — full text.** WebFetch could not parse the binary PDF but saved it locally; text was extracted from the PDF content streams and the Methods, Results, Abstract, Acknowledgements and reference list were all read. |
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/33009197/ | Abstract only (via search result) |
| Sci-Sport secondary article | https://sci-sport.com/en/hypertrophy-and-hamstring-protection-seated-prone-leg-curl/ | N/A — secondary source, used only to check the disputed 13M/7W sex split |

The PMC link supplied in the brief (PMC11349676) was indeed wrong; the correct
record is **PMC7969179**, which the module already cites. Confirmed.

**Full text was obtained.** Every encoded value except the participant
demographics (age, sex split) was verified against the paper's own Methods,
Results and Abstract. The demographics are genuinely not in the inspectable
text — see Concern 1.

---

## Verdict

**ACCURATE.**

Every encoded number traces to the paper exactly. The five per-muscle growth
percentages (WH +14.1/+9.3, BFL +14.4/+6.5, ST +23.6/+19.3, SM +8.2/+3.6, BFS
+10/+9) are verbatim from the paper — the four significant pairs from the
Results text, the BFS pair from the Abstract — all ten emphasis ratios
recompute exactly, the quality-score weighted average is arithmetically correct
(0.8775 → 0.88), the p-value collapse ("P ≤ 0.010" / "P = 0.190") matches the
paper's own reporting, and the funding/COI statement is quoted faithfully. The
two key judgement calls are sound: `ExerciseEmphasis`-only is the right shape,
and exporting **no** Topic-keyed `EffectEstimate` and **no** `_POOLABLE_OVERRIDE`
is correct because emphasis data never enters the inverse-variance Topic pool
that holds Varovic 2025 — so there is no double-counting path to guard. The
only soft spots are documentation-grade: the participant age range and sex split
are honestly flagged UNVERIFIED and the design-dimension deviation is
documented per the rubric. No encoded value is wrong. This does not rise even
to MINOR DISCREPANCIES because the unverified items are correctly labelled as
such in the module rather than asserted.

---

## Value-by-value verification

### Per-muscle growth percentages (the basis of the emphasis coefficients)

| Encoded value | Paper value | Match? | Notes |
|---|---|---|---|
| WH +14.1% vs +9.3% | "+14.1% vs +9.3%" | ✅ | Results, "Part 1 Muscle volume": *"The increases in muscle volume were greater for Seated-Leg than Prone-Leg in the WH (ANCOVA-adjusted mean change: +14.1% vs +9.3%)"*. Also restated in Discussion ("Seated-Leg: +14.1%, Prone-Leg: +9.3%"). |
| BFL +14.4% vs +6.5% | "BFL +14.4% vs +6.5%" | ✅ | Results, same sentence. Re-confirmed in Discussion ("BFL, +14.4% vs +6.5%"). |
| ST +23.6% vs +19.3% | "ST +23.6% vs +19.3%" | ✅ | Results, same sentence. Re-confirmed in Discussion ("ST, +23.6% vs +19.3%"). |
| SM +8.2% vs +3.6% | "SM +8.2% vs +3.6%" | ✅ | Results, same sentence. |
| BFS +10% vs +9% | "+10% vs +9%" | ✅ (whole-percent) | **Source is the Abstract, not the Results text.** Abstract: *"…each biarticular (+8%–24% vs +4%–19%) but not monoarticular (+10% vs +9%) hamstring muscle."* The Results body text gives the four significant muscles' exact percentages but **not** the BFS pair; only the Abstract reports BFS, and only to whole-percent precision. The module's docstring and the `PRONE_LEG_CURL_BFS.rationale` both correctly state "The paper reports these values to whole-percent precision only." The coarse precision is the paper's, not the encoder's. |

### P-values

| Encoded value | Paper value | Match? | Notes |
|---|---|---|---|
| WH/BFL/ST/SM "P ≤ 0.010" | "P ≤ 0.010" | ✅ | Results: *"There were significant differences in mean muscle volume change between the legs in each of the WH, BFL, ST, SM, and SAR (P ≤ 0.010), but not in the BFS (P = 0.190) and GRA (P = 0.097)."* Per-muscle exact p-values are **not** in the text — collapsed by the paper itself. The module documents this honestly (Reporting dimension held to 0.85 for exactly this reason). |
| BFS "P = 0.190" | "P = 0.190" | ✅ | Same sentence. Drives `confidence="low"` on the BFS pair — correct. |

### Emphasis coefficients (recomputed independently)

| Encoded | Formula | Recomputed | Match? |
|---|---|---|---|
| SEATED WH = 1.0 | reference | 1.0 | ✅ |
| PRONE WH = 9.3/14.1 | 9.3 ÷ 14.1 | 0.6596 (~0.66) | ✅ |
| SEATED BFL = 1.0 | reference | 1.0 | ✅ |
| PRONE BFL = 6.5/14.4 | 6.5 ÷ 14.4 | 0.4514 (~0.45) | ✅ |
| SEATED ST = 1.0 | reference | 1.0 | ✅ |
| PRONE ST = 19.3/23.6 | 19.3 ÷ 23.6 | 0.8178 (~0.82) | ✅ |
| SEATED SM = 1.0 | reference | 1.0 | ✅ |
| PRONE SM = 3.6/8.2 | 3.6 ÷ 8.2 | 0.4390 (~0.44) | ✅ |
| SEATED BFS = 1.0 | reference | 1.0 | ✅ |
| PRONE BFS = 9.0/10.0 | 9.0 ÷ 10.0 | 0.90 | ✅ |

All ten coefficients are in `[0, 1]` (the `ExerciseEmphasis.__post_init__`
constraint). The seated leg curl wins every comparison, so normalizing seated =
1.0 is the correct "higher-growth condition" choice and is consistent with
`maeo_2023.py` (overhead = 1.0) and `kassiano_2023.py` (lengthened partial =
1.0). Module imports cleanly and the registry indexes all 10 under
`hamstrings`.

### Confidence labels

| Pair | Encoded confidence | Defensible? | Notes |
|---|---|---|---|
| WH, BFL, ST, SM (8 entries) | `high` | ✅ | Difference reached significance (P ≤ 0.010). "High" correctly means the *direction* of the seated advantage is established, not that the exact ratio is precise — the docstring states this. |
| BFS (2 entries) | `low` | ✅ | Difference n.s. (P = 0.190); short head is monoarticular so no length difference is mechanistically expected. `low` is the correct label and the rationale text tells the optimizer to read 0.90 as "effectively equal", not a real prone disadvantage. |

### Measurement / design facts

| Encoded claim | Paper value | Match? |
|---|---|---|
| "3-T MRI muscle volume" | "3-T magnet bore (MAGNETOM Skyra, Siemens Healthineers)" | ✅ |
| "analysts blinded to training condition" | "MRI data anonymized and investigators blinded to the training conditions" | ✅ |
| "pretraining test-retest CV 1.4-2.1%" | Muscle-volume CVs: WH 1.4%, BFL 1.6%, ST 1.7%, SM 1.4%, BFS 2.1%, GRA 1.4%, SAR 1.5% | ✅ — range stated exactly |
| "randomized via a computer-generated list with dominant/nondominant legs counterbalanced" | "Each leg was randomly assigned to Seated-Leg or Prone-Leg, with the dominant and nondominant legs counterbalanced by the use of a computer-generated list." | ✅ — verbatim |
| "baseline-adjusted ANCOVA + linear mixed-effects model … bootstrap 95% CIs via estimation statistics" | "An ANCOVA was used … with the Pre-TR values as covariates … A linear mixed-effects model was used with a subject as a random effect … bootstrap 95% confidence interval (CI) was calculated by using estimation statistics" | ✅ |
| "residual normality/homoscedasticity checked" | "Residuals were checked for normality and homoscedasticity by Shapiro–Wilk's test and Levene's test" | ✅ |
| "70% 1RM, 5 sets of 10 reps, 2 s/2 s tempo, 2 sessions/week, 0–90° knee ROM" | "70% one-repetition maximum (1RM), 10 repetitions per set, 5 sets per session, 2 sessions per week for 12 wk … 2 s for each of the concentric/eccentric phases … knee joint angle ranging from 0° to 90°" | ✅ |
| "no pre-registration mentioned" | No registration statement found in the full text | ✅ |
| Funding "Mizuno Sports Promotion Foundation" | "This work was supported by a research grant from Mizuno Sports Promotion Foundation (2019-5)" | ✅ |
| COI "no conflict of interest declared; no companies or manufacturers will benefit" | "The authors declare that there is no conflict of interest, that no companies or manufacturers will benefit from the results of the study" | ✅ — quoted faithfully |

### PopulationSpec

| Field | Encoded | Paper | Match? |
|---|---|---|---|
| `training_status` | `"untrained"` | "none had been involved in any type of systematic resistance training program in the past 12 months" | ✅ — "untrained" is the right call; the encoded notes paraphrase the paper's exact wording. |
| `sex` | `"mixed"` | **Not stated in inspectable text.** | ⚠️ See Concern 1 — flagged UNVERIFIED in the module. |
| `age_range` | `(20, 30)` | **Not stated in inspectable text.** | ⚠️ See Concern 1 — flagged "not a paper figure" in the module. |
| `outcome` | `"hypertrophy"` | MRI muscle volume change — hypertrophy | ✅ |
| `notes` | UNVERIFIED flags present | — | ✅ Honest. |

---

## Math checks

### 1. Emphasis ratios

All five prone/seated ratios recomputed independently — see the table above.
Every value matches the module's inline `# ~= …` comments to the stated
precision. No discrepancy.

### 2. Quality-score weighted average

Per `QUALITY_RUBRIC.md` v1.0, seven dimensions and their rubric weights:

```
Study design   0.90 × 0.20 = 0.1800
Sample size    0.80 × 0.15 = 0.1200
Measurement    1.00 × 0.20 = 0.2000
Methodological 0.85 × 0.15 = 0.1275
Reporting      0.85 × 0.10 = 0.0850
Risk of bias   0.85 × 0.10 = 0.0850
Population     0.80 × 0.10 = 0.0800
                       sum = 0.8775  →  round to 0.88
```

Weights sum to 1.00. Result **0.8775 → 0.88**. The module's inline arithmetic
is reproduced exactly. No flat modifiers apply (correct — this is the paper's
own primary, pre-planned comparison, not a post-hoc subgroup; full text was
inspectable so no Sci-Hub modifier; not predatory; not retracted).

### 3. Per-dimension defensibility (the harder check)

| Dimension | Score | Defensible? |
|---|---|---|
| Study design 0.90 | Documented deviation from the rubric's literal 0.5 "side-to-side" row | **Defensible.** The "When to deviate" clause is invoked, with the same reasoning as `maeo_2023.py` and `pedrosa_2023.py` (0.88). Leg-to-condition was randomized via a computer-generated list with dominant/nondominant counterbalanced — verified verbatim. The contralateral-limb model removes between-subject variance and is an accepted, high-power hypertrophy design. 0.90 is consistent with the sibling precedent. Minor inconsistency noted below (Concern 5). |
| Sample size 0.80 | n=20 → rubric's "15–24" band = 0.8 | **Correct.** Note the rubric scores "participants per arm". The within-participant design gives 20 legs per condition; the encoder used 0.80, the band's value. Fine. |
| Measurement 1.00 | 3-T MRI muscle volume | **Correct** — rubric's explicit 1.0 tier for hypertrophy ("MRI muscle volume (gold standard)"). Blinded analysis and 1.4–2.1% CV support the top tier. |
| Methodological 0.85 | ANCOVA + mixed model + bootstrap CIs, normality checks, no pre-reg | **Defensible.** Rubric 0.8 = "no pre-reg but otherwise rigorous; multiple specifications tested"; 0.9 = "pre-registration". 0.85 sits between, justified by the bootstrap/estimation-statistics layer and the nonparametric cross-check. Slightly generous but within rounding tolerance; not a discrepancy. |
| Reporting 0.85 | Full % changes + figure CIs + SDC tables, but per-muscle exact p-values collapsed | **Defensible.** Rubric 0.8 = "effect sizes with CIs but no raw data"; 0.9 = "full effect sizes with CIs; data available on request". The paper deposits descriptive + test statistics in Supplemental Digital Content and shows bootstrap 95% CIs in Figure 4, but collapses four p-values to "≤ 0.010". 0.85 between the two tiers is fair. The module explicitly explains why it is held below 0.90. |
| Risk of bias 0.85 | Mizuno Sports Promotion Foundation funding | **Defensible — see Concern 4.** The rubric's note is explicit: do not score below 0.6 just because a funder is industry-adjacent; only a *direct conflict on the specific finding* warrants a low score. Here the finding favours a training *position* (seated leg curl), not a Mizuno product, and the authors declare "no companies or manufacturers will benefit". A clean academic grant would be 0.9; Mizuno is a sporting-goods company's research foundation, so one notch down to 0.85 is reasonable and well-reasoned. 0.80 would also be defensible and 0.90 only slightly generous — 0.85 is the most defensible midpoint. No change needed. |
| Population 0.80 | 20 young untrained adults; age/sex partly unverified | **Correct.** Rubric 0.7 = "population described but ranges wide"; 0.9 = "clearly described with minor ambiguity". Training history is well described (no systematic RT in 12 months) but age range and sex split are not in the inspectable text. 0.80 honestly reflects that gap. |

All seven dimension scores are individually defensible against the paper.

---

## Concerns & discrepancies

### Concern 1 — Participant demographics (age, sex split) unverified — **MINOR**

The full text was obtained and read in full. The Methods "Study Design and
Participants" section describes the cohort only as **"Twenty healthy adults"**
who had not done systematic resistance training in the prior 12 months. The
Abstract likewise says only "Twenty healthy adults" / "20 young adults". **No
age (mean, SD, or range) and no sex split appear anywhere in the Methods,
Results, Abstract, or Discussion.** The paper states demographic detail is in
"Figure 2 — Flow diagram and demographic information of participants", which is
an **image** and could not be parsed.

The module handles this correctly:
- `age_range=(20, 30)` is explicitly commented as "the conventional young-adult
  envelope, NOT a paper figure."
- `sex="mixed"` rests on a secondary source (sci-sport.com), and the
  `POPULATION.notes` flag this **UNVERIFIED**, naming the source and the
  13M/7W split.

I independently re-checked the secondary source: sci-sport.com states "20
untrained individuals (7 women and 13 men)". This is consistent with the
module's note. It remains a secondary source and is correctly labelled
unverified — I did **not** find the split confirmed in the primary text.

This is a **MINOR** documentation gap, not a discrepancy: no encoded value is
asserted as a paper fact when it is not. The honest UNVERIFIED labelling is
exactly what the brief's process requires. The recommendation below offers a
way to close it.

### Concern 2 — `age_range=(20, 30)` is wider than `maeo_2023.py`'s `(21, 27)` — **MINOR**

`maeo_2023.py` (the near-identical sibling) was tightened from `(20, 30)` to
`(21, 27)` because that paper *reports* age means±SD. Maeo 2021 keeps `(20, 30)`
because no age data is inspectable. This is internally consistent — you cannot
tighten a range you cannot read — but it does mean `applicability_to()` will
over-credit users near age 30 for this prior relative to the sibling. The
module documents the reason. Acceptable as-is; if the demographics are later
recovered from Figure 2, the range should be tightened (see recommendations).
Both papers are from the same lab with the same recruitment model, so the true
range is very likely close to `maeo_2023`'s `(21, 27)` — but encoding that
without the figure would be guessing, which the module correctly avoids.

### Concern 3 — BFS encoded at whole-percent precision (+10/+9) — **not a discrepancy**

The entry-maker flagged this for scrutiny. Verified: the "+10% vs +9%" BFS pair
is **not in the Results body text** — only the Abstract reports it, and only at
whole-percent precision ("not monoarticular (+10% vs +9%)"). The encoder did
not coarsen anything; this is the finest precision the paper provides for BFS.
The 0.90 ratio, the `confidence="low"` label, and the rationale text ("read as
'effectively equal to seated', not a real prone disadvantage") are all correct
and appropriately cautious. No action needed. One small note: the module
docstring line 23 lists BFS under the "ANCOVA-adjusted mean muscle-volume
change" table alongside the four exact-percent muscles; strictly the BFS row is
an *abstract* figure, not from the same Results sentence. This is cosmetic — the
`rationale` field on the BFS entries already states the precision caveat — but
a one-word docstring note would be tidier (see recommendations).

### Concern 4 — Risk-of-bias 0.85 with Mizuno funding — **not a discrepancy**

Scrutinized as requested. The funder is the Mizuno Sports Promotion Foundation,
a research foundation affiliated with a sporting-goods manufacturer. The rubric
is explicit that industry adjacency alone does not warrant a low score — only a
direct conflict on the specific finding does. The finding here (seated > prone
leg curl) favours a training position, not a Mizuno product, and the paper
declares "no companies or manufacturers will benefit". Among 0.80 / 0.85 /
0.90: 0.90 is the clean-academic-grant tier and slightly too generous given the
manufacturer affiliation; 0.80 would be defensible but mildly harsh given the
rubric's explicit "don't penalise industry ties alone" guidance; **0.85 is the
most defensible** and is what the module uses. No change.

### Concern 5 — Study-design deviation: 0.90 vs sibling `pedrosa_2023.py`'s 0.88 — **MINOR**

`maeo_2021.py` scores Study design **0.90**, matching `maeo_2023.py` (0.90).
`pedrosa_2023.py` — also a within-participant contralateral-limb training study
with randomized, counterbalanced limb assignment — scores **0.88** for the same
deviation. The 0.02 gap is immaterial to pooling and the rubric itself says
"two papers scoring 0.85 are similar… it doesn't follow that 0.86 is better
than 0.84." But for consistency the layer should eventually settle on one
number for the "randomized, counterbalanced contralateral-limb training study"
design archetype. This is a layer-wide consistency nit, not a fault specific to
this module, and changing it would move the quality score by at most 0.004
(0.90→0.88 ⇒ 0.8775→0.8735, still rounds to 0.87–0.88). Flagged for the
orchestrator to harmonise across `maeo_2021`/`maeo_2023`/`pedrosa_2023`, not as
a required fix here.

### Judgement call A — `ExerciseEmphasis`-only shape — **CORRECT**

The paper reports per-condition percent muscle-volume change, from which
within-muscle [0,1] emphasis ratios derive directly — the same shape as
`maeo_2023.py` and `kassiano_2023.py`. It does **not** tabulate a
between-condition Cohen's d / SMD with a recoverable SE (Maeo 2021 shows
bootstrap CIs in figures only and collapses p-values), so an `EffectEstimate`
on the SMD scale is not cleanly recoverable from the inspectable material
anyway. `ExerciseEmphasis`-only is the right and honest shape. The within-
participant correlation caveat (legs' change scores are correlated) is noted in
the docstring and correctly judged to matter less for a relative ranking than
for an effect size.

### Judgement call B — no Topic, no `_POOLABLE_OVERRIDE` — **CORRECT**

This is the most important judgement call and it is sound. Confirmed
independently:

- Maeo 2021 **is** one of the 12 primary studies inside the Varovic 2025
  meta-analysis encoded in `varovic_2025.py` (the relevance doc confirms it
  against Varovic's published included-study list; the paper's own regional
  data — BFL Proximal +20.8 vs +8.7%, BFL Distal +10.7 vs +5.4%, ST Proximal
  +28.2 vs +21.1% — is exactly the proximal/distal contrast Varovic pools).
- If Maeo 2021's *regional* data were encoded as a Topic-keyed `EffectEstimate`
  under `MUSCLE_LENGTH_REGIONAL_HYPERTROPHY`, it would double-count against
  Varovic — the same hazard already handled for `pedrosa_2023.py` via the
  existing `_POOLABLE_OVERRIDE` (pool = Varovic only).
- The module sidesteps this entirely by exporting **no** `EffectEstimate`.
  Emphasis data enters only `_EMPHASIS_INDEX`, keyed by (exercise, muscle,
  region) and pooled by `combine_emphasis_estimates` (quality-weighted average)
  — a path that **never** touches the inverse-variance Topic pool. I verified
  in `registry.py`: `_EMPHASIS_SOURCES = (maeo_2023, kassiano_2023, maeo_2021)`
  and there is no `maeo_2021` reference in `_EFFECT_INDEX`. Since no Topic-keyed
  estimate exists, there is **nothing to override** — adding a
  `_POOLABLE_OVERRIDE` entry would be meaningless. The relevance doc, the module
  docstring (lines 32–49), and the `registry.py` comment (lines 156–160) all
  state this reasoning correctly and consistently.
- The Q1 (exercise selection: which exercise grows the muscle more) vs Q2
  (regional: does growth differ by site within a condition) distinction is the
  right framing: Maeo 2021 supplies Q1 emphasis data, which Varovic does not
  answer, so the emphasis encoding adds genuinely new, non-overlapping
  information.

The decision to add no Topic and no override is correct.

---

## Recommendations

1. **(Optional, closes Concern 1)** Attempt to recover the age and sex split
   from **Figure 2** of the paper (the flow/demographic diagram) by reading the
   figure image directly — e.g. via the PMC figure viewer or the figure file in
   the PMC article. If the demographics are recovered: (a) replace the
   secondary-source 13M/7W note with the primary figure and drop the UNVERIFIED
   flag; (b) tighten `age_range` from the conventional `(20, 30)` envelope to
   the paper's actual range, mirroring how `maeo_2023.py` was tightened to
   `(21, 27)`. If the figure cannot be read, leave the module exactly as is —
   the UNVERIFIED labelling is correct and must not be replaced with a guess.

2. **(MINOR, cosmetic)** In the docstring "KEY FINDING" table (lines 19–23),
   add a half-sentence noting that the BFS `+10% / +9%` row is from the
   **Abstract** (whole-percent precision), whereas the WH/BFL/ST/SM rows are the
   exact ANCOVA-adjusted percentages from the Results text. The BFS
   `rationale` fields already carry the precision caveat, so this is a polish
   item, not a correctness fix.

3. **(MINOR, layer-wide — for the orchestrator, not this module)** Harmonise the
   Study-design score for the "randomized, counterbalanced contralateral-limb
   training study" archetype across `maeo_2021.py` (0.90), `maeo_2023.py`
   (0.90) and `pedrosa_2023.py` (0.88). Pick one value and apply it
   consistently. The effect on any quality score is ≤ 0.004 and changes no
   rounded value materially, so this is housekeeping, not urgent.

4. **No change required** to the encoded growth percentages, emphasis
   coefficients, confidence labels, quality score, scale handling, Topic
   decision, or `_POOLABLE_OVERRIDE` decision. All are verified correct.

---

## Summary

Verdict: **ACCURATE**. The full text was obtained from an open-access PDF
mirror and every encoded value verified against the paper itself: the five
per-muscle growth percentages, all ten emphasis ratios, the p-value collapse,
the measurement/design facts, and the funding/COI statement all match exactly,
and the quality-score arithmetic (0.8775 → 0.88) is correct. The single most
important finding is positive: the central judgement call — encode Maeo 2021 as
`ExerciseEmphasis`-only with **no** Topic-keyed `EffectEstimate` and **no**
`_POOLABLE_OVERRIDE`, because emphasis data never enters the inverse-variance
Topic pool that holds the Varovic 2025 meta-analysis Maeo 2021 is a constituent
of — is correct and correctly prevents the double-counting hazard. The only
soft spots are documentation-grade and honestly labelled: participant age and
sex split are genuinely absent from the inspectable text (they live in a figure
image) and are correctly flagged UNVERIFIED rather than guessed.
