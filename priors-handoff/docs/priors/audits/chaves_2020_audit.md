# Audit — chaves_2020.py

**Module audited:** `priors-handoff/app/priors/chaves_2020.py`
**Source paper:** Chaves SFN, Rocha-Júnior VA, Encarnação IGA, et al. "Effects of
Horizontal and Incline Bench Press on Neuromuscular Adaptations in Untrained
Young Men." *International Journal of Exercise Science* 2020;13(6):859–872.
DOI: 10.70252/FDNB1158 · PMID: 32922646 · PMC7449336.
**Date:** 2026-05-17
**Auditor:** independent priors-layer auditor

---

## Sources accessed

| Source | URL | Full text obtained? |
|---|---|---|
| PMC open-access HTML | https://pmc.ncbi.nlm.nih.gov/articles/PMC7449336/ | YES — full text, queried in four passes (thickness values, sample sizes, end-matter, Results/Limitations verbatim) |
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/32922646/ | Abstract only (confirmed citation + design) |
| WKU DigitalCommons (publisher) | https://digitalcommons.wku.edu/ijes/vol13/iss6/12/ | Landing page reached; PDF download returned HTTP 403 — not retrieved (PMC full text was sufficient) |
| ResearchGate / Semantic Scholar | listed in search | Not separately fetched; PMC is authoritative |

The PMC open-access full text was fully readable and was the primary verification
source. All numeric claims below are checked against it directly.

---

## Verdict

**MATERIAL DISCREPANCIES.**

The six emphasis coefficients, the per-site % growth derivations, the
significance pattern, the confidence labels, the population spec, and the
emphasis-vs-Topic encoding decision are all **correct and well reasoned**. The
arithmetic is clean to the claimed tolerance. However, the module misstates the
sample size of the **only** outcome it actually encodes. Every one of the six
`ExerciseEmphasis` coefficients is derived from the pectoralis-major
muscle-thickness data, and the paper states verbatim that this came from **30
subjects, 10 per group** — not the 47 (15/15/17) the module repeats throughout
the docstring, the `POPULATION` notes, the sanity-check print, and most
consequentially the **Sample size = 0.80** quality dimension. n=10 per arm falls
in the rubric's 0.5 band (6–9 → 0.5; 10–14 → 0.7), not the 0.80 (15–24) band the
module cites. This propagates a wrong premise into the quality score and the
provenance text. It is a factual error about the encoded data, so it is
material; the corrected quality score change is small (~0.78), but the stated
basis for the score is wrong and the n the optimizer would read is wrong.

---

## Value-by-value verification

### Muscle thickness means (mm), pre → post

| Site / group | Encoded | Paper value | Match? | Source |
|---|---|---|---|---|
| 2nd IC Horizontal | 11.9 (2.0) → 15.7 (3.9) | 11.9±2.0 → 15.7±3.9 | YES | Results, thickness table |
| 2nd IC Incline | 15.1 (3.8) → 24.5 (4.1) | 15.1±3.8 → 24.5±4.1 | YES | Results, thickness table |
| 2nd IC Combination | 14.3 (5.3) → 18.8 (6.5) | 14.3±5.3 → 18.8±6.5 | YES | Results, thickness table |
| 3rd IC Horizontal | 13.2 (3.5) → 19.3 (5.0) | 13.2±3.5 → 19.3±5.0 | YES | Results, thickness table |
| 3rd IC Incline | 15.4 (4.3) → 23.8 (5.7) | 15.4±4.3 → 23.8±5.7 | YES | Results, thickness table |
| 3rd IC Combination | 17.1 (5.0) → 21.2 (4.9) | 17.1±5.0 → 21.2±4.9 | YES | Results, thickness table |
| 5th IC Horizontal | 12.6 (2.7) → 18.0 (5.1) | 12.6±2.7 → 18.0±5.1 | YES | Results, thickness table |
| 5th IC Incline | 14.4 (4.2) → 22.8 (5.4) | 14.4±4.2 → 22.8±5.4 | YES | Results, thickness table |
| 5th IC Combination | 16.0 (5.5) → 22.7 (5.9) | 16.0±5.5 → 22.7±5.9 | YES | Results, thickness table |

All nine pre/post mean(SD) pairs verified exactly.

### Between-group significance

| Encoded claim | Paper value | Match? | Source |
|---|---|---|---|
| 2nd IC ANOVA P = 0.005 | p = 0.005 | YES | Results |
| Incline > Horizontal, 0.62 cm, P = 0.003 | MD 0.62 cm [95% CI 0.23–1.0], p = 0.003 | YES | Results |
| Incline > Combination, 0.50 cm, P = 0.008 | MD 0.50 cm [95% CI 0.14–0.86], p = 0.008 | YES | Results |
| Horizontal vs Combination, P = 0.524 | MD 0.11 cm [95% CI −0.25–0.48], p = 0.524 | YES | Results |
| 3rd IC P = 0.095 (n.s.) | p = 0.095 | YES | Results |
| 5th IC P = 0.227 (n.s.) | p = 0.227 | YES | Results |

The relevance-checker's key claim — that the 2nd-intercostal (clavicular)
incline advantage is the **only** significant between-group result and both
sternocostal sites are non-significant — is **confirmed exactly**. The
confidence labels follow correctly: `high` on the three clavicular pairs,
`low` on the three sternocostal pairs.

### Emphasis coefficients

| Entry | Encoded emphasis | Recomputed | Match? |
|---|---|---|---|
| INCLINE clavicular | 1.0 (reference) | 1.0 | YES |
| HORIZONTAL clavicular | 31.9/62.3 = 0.5120 | raw-mm ratio 0.5130 | YES (Δ 0.0009) |
| COMBINATION clavicular | 31.5/62.3 = 0.5056 | raw-mm ratio 0.5055 | YES (Δ 0.0001) |
| INCLINE sternocostal | 1.0 (reference) | 1.0 | YES |
| HORIZONTAL sternocostal | 46.2/54.5 = 0.8477 | raw-mm ratio 0.8472 | YES (Δ 0.0005) |
| COMBINATION sternocostal | 24.0/54.5 = 0.4404 | raw-mm ratio 0.4396 | YES (Δ 0.0008) |

### Population spec

| Field | Encoded | Paper value | Match? |
|---|---|---|---|
| training_status | "untrained" | "no resistance training in the prior 6 months" | YES |
| sex | "male" | "young male college students" | YES |
| age_range | (18, 30) | inclusion criterion 18–30; sample mean 21.1±3.3 y | YES |
| outcome | "hypertrophy" | muscle thickness | YES |
| mean age/mass/height | 21.1 y, 71.9 kg, 176 cm | 21.1±3.3 y, 71.9±13.5 kg, 176±7 cm | YES |
| "47 untrained young men" | stated | 47 *completed the training protocol* | PARTIALLY — see below |
| 25 of 72 excluded | stated | 72 enrolled, 47 completed (16 attendance, 2 nutrition, 7 personal) | YES (25 = 16+2+7) |

### Citation block

| Field | Encoded | Correct? |
|---|---|---|
| authors | "Chaves et al." | YES |
| year | 2020 | YES |
| doi | "10.70252/FDNB1158" | YES |
| journal | "International Journal of Exercise Science" | YES |

---

## Math checks

### Per-site % growth — recomputed independently

```
2nd IC (clavicular):  Horizontal 31.933%   Incline 62.252%   Combination 31.469%
3rd IC (sternocostal): Horizontal 46.212%   Incline 54.545%   Combination 23.977%
5th IC (sternocostal): Horizontal 42.857%   Incline 58.333%   Combination 41.875%
```
All match the rounded values used in the module (31.9 / 62.3 / 31.5; 46.2 /
54.5 / 24.0; 42.9 / 58.3 / 41.9).

### Rounded-% vs raw-mm ratio discrepancy (entry-maker flag #3)

```
Clavicular:    horizontal  rounded 0.51204  raw 0.51296  Δ 0.00092
               combination rounded 0.50562  raw 0.50551  Δ 0.00011
Sternocostal:  horizontal  rounded 0.84771  raw 0.84722  Δ 0.00048
               combination rounded 0.44037  raw 0.43957  Δ 0.00080
```
All four discrepancies are ≤ 0.001, comfortably inside the ≤ 0.005 claim.
**Flag #3: confirmed accurate.**

### Quality-score weighted average — recomputed

```
0.85·0.20 + 0.80·0.15 + 0.90·0.20 + 0.65·0.15 + 0.70·0.10 + 0.80·0.10 + 0.85·0.10
= 0.170 + 0.120 + 0.180 + 0.0975 + 0.070 + 0.080 + 0.085
= 0.8025  →  rounds to 0.80
```
The arithmetic in the module is **correct**. The issue is not the arithmetic —
it is the **Sample size = 0.80 input** (see Concern 1). With Sample size
corrected to 0.70 (rubric's 10–14 per-arm band):

```
0.85·0.20 + 0.70·0.15 + 0.90·0.20 + 0.65·0.15 + 0.70·0.10 + 0.80·0.10 + 0.85·0.10
= 0.170 + 0.105 + 0.180 + 0.0975 + 0.070 + 0.080 + 0.085
= 0.7875  →  rounds to 0.79  (or 0.78)
```

### Sternocostal representative-site cross-check (entry-maker flag #2)

5th-intercostal ratios: horizontal/incline = 0.7347, combination/incline =
0.7179. The entry-maker's stated "≈0.74 / ≈0.72" is **confirmed**. The chosen
3rd-IC representative gives 0.85 / 0.44 instead. See Concern 3.

---

## Concerns & discrepancies (ranked)

### 1. MATERIAL — Wrong sample size for the encoded outcome

The module states "n=47 (15/15/17)" in the docstring KEY FINDING, the
`POPULATION.notes`, the quality comment ("per-arm n = 15 / 15 / 17"), and the
`__main__` print. The paper states verbatim in Results:

> "Forty-seven subjects completed the training protocols, but **we had 30
> subjects for the muscle thickness data (10 subjects in each group)**, and 43
> subjects for EMG amplitude..."

Every `ExerciseEmphasis` in this module is derived **exclusively** from the
muscle-thickness data. The relevant n is therefore **10 per group / 30 total**,
not 15/15/17 / 47. The 47 (15/15/17) figure is the count of training-protocol
*completers* and the n for the *isometric-strength* outcome — neither of which
this module encodes.

Consequences:
- **Sample size quality dimension is wrong.** The module scores it 0.80 citing
  "per-arm n = 15 / 15 / 17 — rubric's 15-24 band, 0.80." Actual per-arm n = 10
  sits in the rubric's **10–14 band → 0.70** (the 6–9 band is 0.5). The base
  score should be ~0.79 rather than 0.80 (recomputation above).
- The provenance the optimizer/registry would surface (docstring, POPULATION
  notes) materially understates the uncertainty of the emphasis coefficients:
  a 10-per-arm pre/post comparison is a substantially thinner basis than
  15–17 per arm, and the wide SDs (e.g. combination 2nd-IC post 18.8±6.5 on
  n=10) make the point estimates fragile.
- The thickness subsample (30/47 = 64% of completers) is not a random subset
  by any stated mechanism; the paper gives no explanation for which 10 per
  group were measured. That is an additional, undocumented selection concern.

This is a factual error about the data actually being encoded, not a wording
gap — hence MATERIAL.

### 2. MODERATE — Risk-of-bias 0.80 deviation: disclosure genuinely absent, but the score is defensible

Entry-maker flag #1. I independently searched the full PMC text end-matter,
PubMed, and the publisher landing page. Confirmed:
- **No funding statement** anywhere in the article.
- **No conflict-of-interest / disclosure statement** anywhere in the article.
- **No trial-registration number.** The article reports only an IRB protocol
  number (44608115.6.0000.558) — that is ethics approval, not prospective
  trial registration.

So the UNVERIFIED flag is accurate; the disclosure is genuinely missing, not
merely unreached. International Journal of Exercise Science in 2020 did not
mandate a structured COI/funding section, so absence is consistent with journal
norms rather than evidence of concealment. The finding favours a training
position, not a commercial product. Scoring 0.80 (one notch below the 0.90
disclosed-academic tier) to reflect the missing disclosure, with the deviation
explicitly documented per the rubric, is **a defensible call** and the rubric's
"don't score below 0.6 just for industry context" guidance is correctly
respected. **No change required**, but the audit confirms the absence is real.

Note: author J.P. Loenneke is a well-published academic with no commercial
conflict on incline-vs-flat pressing; nothing surfaced to suggest a hidden COI.

### 3. MINOR — Two-sites-into-one-region collapse is defensible and honestly documented

Entry-maker flag #2. Both the 3rd and 5th intercostal sites measure the
sternocostal head. The module collapses them to one `sternocostal_head` key
using the 3rd IC (mid) as representative, and the rationale strings explicitly
report the 5th-IC numbers and note that the 5th-IC ratios differ (≈0.74/≈0.72
vs encoded 0.85/0.44). I confirmed the 5th-IC ratios (0.7347 / 0.7179). The
discrepancy IS honestly disclosed in both the comment block and the rationale
strings. Picking the *mid* sternocostal landmark as representative is
anatomically reasonable. Since both sites were **non-significant** and both
entries carry `confidence="low"` with rationale text telling the optimizer to
treat the mid/lower chest as "bench-angle-agnostic", the exact coefficient
value carries little weight — the choice is low-stakes and transparent.
Acceptable as-is. A marginally cleaner option would be to average the two
sites, but that is a judgement call, not a defect.

### 4. MINOR — Measurement 0.90 with no reliability/blinding reported

Entry-maker flag #4. Confirmed: the paper reports **no ICC/CV** for the
ultrasound thickness measurement and **does not state assessor blinding**. The
module scores Measurement 0.90 (rubric's "site-specific MT via ultrasound,
high-quality" row) and explicitly logs the missing reliability/blinding data in
the comment. The rubric's row is keyed to the *measurement modality*, and
site-specific B-mode ultrasound MT is the standard validated method, so 0.90 is
within rubric. However, the rubric's high-quality ultrasound row arguably
presumes a *competently executed* protocol; with neither reliability statistics
nor blinding reported, 0.85 ("CSA via ultrasound") would be at least equally
defensible and slightly more conservative. This is a borderline judgement, not
an error — the gap is logged, so it meets the rubric's documentation
requirement. **Optional** downgrade to 0.85; not required.

### 5. MINOR — Methodological rigor 0.65 is reasonable

Entry-maker flag #5. Confirmed against the paper: per-protocol analysis
excluding 25/72 enrolled; no prospective registration; the article reports
adjusted change scores with 95% CIs but states **no multiple-comparison
correction** and gives no explicit ANOVA-assumption checks or missing-data
handling. The rubric's 0.5–0.7 band ("some methodological concerns" /
"competent standard methods") fits; 0.65 is a sound midpoint. One nuance: the
muscle-thickness analysis is effectively a *subsample* analysis (30 of 47
completers, mechanism unstated), which is an additional rigor concern not
mentioned in the 0.65 justification. It does not change the score band but
should be noted in the comment. Acceptable; see Recommendation 3.

### 6. MINOR — Once-weekly frequency / untrained as applicability not quality: correct

Entry-maker flag #6. Treating the once-weekly training frequency and the
untrained-male population as **applicability** limitations (carried in
`PopulationSpec` and the docstring) rather than **quality** penalties is the
correct classification. The rubric scores how well a paper answers *its own*
question; `applicability_to()` handles how well that question matches a user.
Once-weekly training and untrained status do not make the study a worse test of
its own hypothesis — they limit transfer. The module's handling matches how
the layer treats population narrowness elsewhere. **No change required.**

### 7. MINOR — Encoding shape / registry decisions are sound

`ExerciseEmphasis`-only with no Topic-keyed `EffectEstimate`, no new `Topic`,
and no `_POOLABLE_OVERRIDE` entry is the correct decision. This is a genuine
between-exercise selection contrast; it does not belong in the
inverse-variance Topic pools, and `ARM_POSITION_HYPERTROPHY` is correctly
identified as a different question (joint position within one movement).
Chaves 2020 is a stand-alone primary RCT, not a constituent of any encoded
meta-analysis, so there is no double-counting risk and no override is needed.
The `registry.py` wiring (added to `_EMPHASIS_SOURCES`, fresh
`pectoralis_major` keys, passthrough combination) is correct. **No change
required.**

---

## Recommendations

1. **(MATERIAL — fix before integration)** Correct the sample size everywhere
   it describes the encoded outcome. The muscle-thickness data — the sole basis
   for all six emphasis coefficients — is **n=10 per group, 30 total**, per the
   paper's Results. Specifically:
   - Docstring KEY FINDING: distinguish "47 completed the 8-week protocol" from
     "muscle thickness measured in 30 (10 per group)".
   - `POPULATION.notes`: state that the thickness outcome encoded here rests on
     a 30-subject subsample (10/group), not all 47.
   - Quality comment: change "Sample size 0.80 (per-arm n = 15 / 15 / 17)" to
     reflect per-arm n=10 → rubric 0.70 band.
   - `__main__` print: "n=47 (15/15/17)" is misleading for this module — change
     to "muscle-thickness n=30 (10/group)".

2. **(MATERIAL — fix before integration)** Re-score and update `QUALITY`. With
   Sample size = 0.70, the weighted average is 0.7875 → **0.79** (or 0.78).
   Update the `QUALITY` constant and the weighted-average line in the comment.
   The emphasis coefficients themselves do not change.

3. **(MINOR)** In the Methodological-rigor comment, add that the
   muscle-thickness analysis is a 30/47 subsample with no stated selection
   mechanism — an additional rigor caveat. Score band (0.65) need not change.

4. **(OPTIONAL)** Consider downgrading Measurement from 0.90 to 0.85: no
   reliability ICC/CV and no assessor blinding are reported. Defensible either
   way; 0.85 is the more conservative reading. If kept at 0.90, the existing
   logged-gap comment already satisfies the rubric's documentation rule.

5. **(NO ACTION)** Concerns 2, 6, and 7 (risk-of-bias deviation, applicability
   vs quality classification, emphasis/registry encoding) are all sound as
   encoded and are confirmed by this audit.

Items 1 and 2 are coupled: both stem from the single underlying error and
should be fixed together. None of the six emphasis coefficient *values*, the
significance pattern, the confidence labels, or the registry wiring need to
change.
