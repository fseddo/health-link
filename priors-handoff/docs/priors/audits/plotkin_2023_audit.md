# Audit — `plotkin_2023.py`

**Module audited:** `priors-handoff/app/priors/plotkin_2023.py`
**Source paper:** Plotkin DL, Rodas MA, Vigotsky AD, et al. "Hip thrust and back
squat training elicit similar gluteus muscle hypertrophy and transfer similarly
to the deadlift." *Frontiers in Physiology* 2023;14:1279170.
DOI 10.3389/fphys.2023.1279170 · PMID 37877099 · PMC10593473.
**Date:** 2026-05-17
**Auditor:** independent priors-layer auditor

---

## Sources accessed

| Source | URL | Full text obtained? |
|---|---|---|
| PMC open-access HTML | https://pmc.ncbi.nlm.nih.gov/articles/PMC10593473/ | Yes — Results, Methods (statistics), demographics, funding/COI all reachable |
| Frontiers article page | https://www.frontiersin.org/articles/10.3389/fphys.2023.1279170/full | Yes — Results contrasts, regression coding, strength transfer |
| Frontiers "simple text" abstract | https://public-pages-files-2025.frontiersin.org/journals/physiology/articles/10.3389/fphys.2023.1279170/text | Abstract only — used to confirm the verbatim sign-convention notation |
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/37461495/ (search hit) | Metadata only |
| MASS Research Review summary | massresearchreview.com (search hit) | Not used for values; corroboration only |

Full text was obtained. Every encoded number was checked against the paper's
Results text and abstract. The one item that could not be inspected as a
rendered image is the between-group contrast **figure** itself; its caption and
all numeric values were recovered from the Results/abstract text instead, which
is sufficient.

---

## Verdict

**MATERIAL DISCREPANCIES.**

Every encoded *number* is correct — the seven `mean` values, all seven SEs, n,
n_studies, the population fields, the strength-transfer constants, and the
quality score (0.875, arithmetic exact) all match the paper. The encoding
*shapes*, the `scale`, the new Topic, the `_POOLABLE_OVERRIDE`, the
equivalence-emphasis design and the strength-as-constants decision are all
sound. **However, the module states the sign convention backwards.** The paper
defines its contrast as **"(−) favors HT; (+) favors SQ"** (negative = the hip
thrust grew the site more; positive = the back squat grew it more). The module
docstring asserts the opposite — "a negative sign favours the SQUAT ... a
positive sign favours the HIP THRUST" — and that inverted rule propagates into
the docstring narrative and into the four glute / glute-med `notes` strings,
which describe negative estimates as "lean toward the squat" when the paper
says they lean toward the hip thrust. The quadriceps and adductors `notes` are,
by contrast, *correct* ("the back squat grew ... significantly more"), so the
module is also **internally self-contradictory**: the same sign means "squat"
in one note and "hip thrust" in the docstring rule. This is a material
documentation defect — a reader (or a future maintainer wiring the optimizer)
who trusts the stated convention will invert the glute-region interpretation.
The encoded equivalence result is unaffected (a null is a null whichever way
the trivial lean points), but the labelling must be fixed before integration.

---

## Value-by-value verification

Contrast direction per the paper (abstract, verbatim): *"estimates [(−) favors
HT; (+) favors SQ]"*. Regression (Methods/Statistics, verbatim): *"group was
dummy-coded 0 for SQ and 1 for HT, and the pre-intervention score was included
as a covariate."* Results, verbatim: glute-max estimates *"modestly favored the
HT versus SQ"*; *"SQ produced greater mCSA growth for quadriceps ... and
adductors."*

| Encoded item | Encoded value | Paper value | Match? | Notes |
|---|---|---|---|---|
| Glute max upper, mean | −0.5 cm² | −0.5 ± 2.6, CI (−5.8, 4.1) | YES (number) | Paper: −0.5 *favors HT*. Module note says "trivial lean toward the squat" — **WRONG direction**. |
| Glute max upper, SE | 2.6 | 2.6 | YES | Read directly from paper "± SE". |
| Glute max middle, mean | −0.5 cm² | −0.5 ± 1.7, CI (−4.0, 2.6) | YES (number) | Paper: −0.5 favors HT. Note says "no detectable difference" (true) but module rule labels − as squat — **inconsistent**. |
| Glute max middle, SE | 1.7 | 1.7 | YES | |
| Glute max lower, mean | −1.6 cm² | −1.6 ± 2.1, CI (−6.1, 2.0) | YES (number) | Paper: −1.6 *favors HT*. Note says "largest ... glute-max lean toward the squat" — **WRONG direction**. |
| Glute max lower, SE | 2.1 | 2.1 | YES | |
| Glute med+min, mean | −1.8 cm² | −1.8 ± 1.5, CI (−4.6, 1.4) | YES (number) | Paper: −1.8 favors HT. Note is direction-neutral, so not wrong, but the docstring rule still mislabels it. |
| Glute med+min, SE | 1.5 | 1.5 | YES | |
| Quadriceps, mean | +3.6 cm² | +3.6 ± 1.5, CI (0.7, 6.4) | YES | Paper: +3.6 favors SQ. Note "back squat grew the quadriceps significantly more" — **CORRECT**. |
| Quadriceps, SE | 1.5 | 1.5 | YES | CI excludes zero — confirmed. |
| Adductors, mean | +2.5 cm² | +2.5 ± 0.7, CI (1.2, 3.9) | YES | Paper: +2.5 favors SQ. Note "back squat grew the hip adductors significantly more" — **CORRECT**. |
| Adductors, SE | 0.7 | 0.7 | YES | CI excludes zero — confirmed. |
| Hamstrings, mean | +0.1 cm² | +0.1 ± 0.6, CI (−0.9, 1.4) | YES | Equivocal — confirmed. |
| Hamstrings, SE | 0.6 | 0.6 | YES | |
| n | 34 | 18 HT + 16 SQ completers = 34 | YES | Participants analysed. |
| n_studies | None | single primary RCT | YES | Correct — not a meta-analysis. |
| Back squat 3RM contrast | +14 ± 2 kg, CI (9,18) | "Squat 3RM favored SQ [14 ± 2 kg], CI (9,18)" | YES (number) | Constant, not an EffectEstimate — sound (see below). Label "HT minus SQ" is **wrong**: a HT−SQ contrast favouring SQ would be negative. |
| Hip thrust 3RM contrast | −26 ± 5 kg, CI (−34,−16) | "hip thrust 3RM favored HT [−26 ± 5 kg]" | YES (number) | −26 favors HT, consistent with "(−) favors HT". |
| Deadlift 3RM contrast | 0 ± 2 kg, CI (−4, 3) | "[0 ± 2 kg; CI95% (−4, 3)]" | YES | Equal transfer — confirmed. |
| Training status | "untrained" | "<1 day/week RT over prior 5 years" | YES | |
| Sex | "mixed" | HT 5M/13F, SQ 6M/10F | YES | |
| age_range | (18, 30) | HT 22±3, SQ 24±4 (mean±SD) | YES (defensible envelope) | See judgement-call section. |
| outcome | "hypertrophy" | MRI mCSA | YES | |
| scale | "between_exercise_csa_diff_cm2" | raw cm² between-group difference | YES — see judgement call 1 | |
| quality_score | 0.875 | rubric recompute = 0.875 | YES | |

---

## Math checks

### Quality-score weighted average

Dimension scores and rubric weights, recomputed independently:

```
design       0.90 × 0.20 = 0.1800
sample       0.80 × 0.15 = 0.1200
measurement  1.00 × 0.20 = 0.2000
method       0.80 × 0.15 = 0.1200
reporting    0.90 × 0.10 = 0.0900
risk_of_bias 0.80 × 0.10 = 0.0800
population   0.85 × 0.10 = 0.0850
                           ------
total                      0.8750
```

Weights sum to 1.00. Weighted average = **0.875**, exactly as encoded. No flat
modifiers apply (not a meta-analysis, not predatory, full text free, not a
subgroup-as-primary, not retracted). **Arithmetic confirmed.**

Per-dimension defensibility (all judged sound):
- **Study design 0.90** — parallel-group RCT, block randomisation, supervised,
  volume-equated; not pre-registered. Rubric's 0.90 "RCT, no pre-reg, solid
  randomisation" tier. Correct.
- **Sample size 0.80** — per-arm n = 16 and 18, both inside the rubric's 15–24
  band (0.80). Scored by per-arm n, as the rubric directs. Correct.
- **Measurement 1.00** — MRI cross-sectional area. The rubric's gold-standard
  row is "MRI muscle *volume*"; this paper used MRI *CSA*. CSA via MRI is still
  the rubric's top imaging modality and clearly above the 0.85 "CSA via
  ultrasound/DEXA" row, so 1.00 is defensible — a 0.95 would be the only
  arguable trim and the difference is immaterial.
- **Methodological rigor 0.80** — frequentist regression with baseline
  covariate; BCa stratified bootstrap, 10,000 replicates; no pre-registration.
  Rubric's 0.80 "no pre-reg but otherwise rigorous" tier. Correct.
- **Reporting 0.90** — every contrast given as effect ± SE *with* a 95% CI; no
  SE reconstructed. No raw-data/code deposit cited. 0.90 correct.
- **Risk of bias 0.80** — see judgement call 5; defensible.
- **Population 0.85** — n, per-group sex split, mean±SD age, training history
  all reported; only minor ambiguity is age as mean±SD not a range. 0.85
  correct.

### SE recovery cross-check

The module reads SE **directly** from the paper's "effect ± SE" reporting, so no
recovery was required. As an independent consistency check I recovered SE from
each bootstrap CI width, `SE ≈ (hi − lo) / (2 × 1.96)`:

| Contrast | Encoded SE | SE from paper CI width | Agreement |
|---|---|---|---|
| Glute max upper | 2.6 | 2.53 | close (BCa CI is asymmetric) |
| Glute max middle | 1.7 | 1.68 | close |
| Glute max lower | 2.1 | 2.07 | close |
| Glute med+min | 1.5 | 1.53 | close |
| Quadriceps | 1.5 | 1.45 | close |
| Adductors | 0.7 | 0.69 | close |
| Hamstrings | 0.6 | 0.59 | close |

All consistent. The small gaps are expected: the paper's CIs are bias-corrected
accelerated bootstrap intervals (asymmetric), so a symmetric `(hi−lo)/(2·1.96)`
back-out will not reproduce the reported SE exactly. The module documents this
honestly and notes that `EffectEstimate.ci_95` (symmetric Normal) will not
round-trip the printed bootstrap CI. The quadriceps and adductors Normal CIs
both still exclude zero, preserving the paper's significance verdict.

### Registry integration

`python -m app.priors.registry` runs clean: 14 topics, 40 effect estimates, 30
emphasis coefficients. `exercise_selection->hypertrophy` shows 7 estimates, 3
poolable — matching the `_POOLABLE_OVERRIDE` restricting the pool to the three
gluteus-maximus subregion contrasts. `python -m app.priors.plotkin_2023` runs
clean.

---

## Judgement-call assessment

**1. `scale = "between_exercise_csa_diff_cm2"` (raw cm², non-poolable).
SOUND.** A raw absolute CSA difference between two exercises is genuinely
incommensurable with the layer's `standardized_mean_diff`, `smd_per_set` and
`pct_per_set` scales — different units and a different question (exercise
selection, not dose-response). A dedicated scale string is the correct guard:
`combine_inverse_variance` raises on mixed scales, so this estimate can never be
silently pooled cross-paper. Correct.

**2. Both exercises at emphasis = 1.0, confidence = "medium", for an
underpowered null. SOUND.** This is the cleanest part of the module. Encoding
the equivalence as an *equal* 1.0/1.0 pair, rather than inventing a fractional
ratio from untested descriptive figures, is exactly right — a fractional
coefficient would manufacture a measured ranking the authors explicitly
declined to test. `confidence="medium"` (not "high") correctly reflects that
the "no difference" direction rests on a single n=34 trial with CIs wide enough
not to exclude a real moderate difference. The docstring, the emphasis-section
comment and the optimizer guidance all repeatedly state "roughly
interchangeable / not proven identical / underpowered null." This does **not**
misrepresent an underpowered null as proven identity. Correct. (Minor caveat:
shared.py's `emphasis` is defined as a study-independent "fraction of maximum
stimulus"; a 1.0/1.0 equivalence pair is a different construct. The module
flags this explicitly under "PROVISIONAL-SCALE METHOD CAVEAT", consistent with
maeo_2021 / kassiano_2023 / chaves_2020 — acceptable.)

**3. Dual encoding (EffectEstimate contrasts + emphasis entries).
ACCEPTABLE, not harmfully redundant.** The two shapes feed different consumers:
the EffectEstimate contrasts are the faithful primary encoding routed to the
`EXERCISE_SELECTION_HYPERTROPHY` Topic; the two emphasis entries exist only so
the optimizer's exercise-selection path can read glute data through the
emphasis index. They are not double-counted — the emphasis index and the
inverse-variance Topic pool are separate paths that never combine, and the
emphasis pair carries no statistical weight (it is a 1.0/1.0 equivalence
marker). No redundancy harm. Correct.

**4. New `Topic.EXERCISE_SELECTION_HYPERTROPHY` + `_POOLABLE_OVERRIDE` to the 3
glute-max subregion contrasts. SOUND.** The contrasts map to no existing
dose/form Topic (all of which hold the exercise fixed and vary how you train);
a dedicated exercise-selection Topic is the right home. The override is the
*essential* guard the entry-maker correctly flagged: the seven contrasts share
one raw-cm² scale, so `combine_inverse_variance` would *not* raise on them — yet
they span seven different muscles, and pooling them would average unrelated
muscles into a meaningless number. Restricting the poolable set to the three
glute-max subregions (one muscle, three subregions — a genuinely homogeneous
set) is correct. The four thigh/abductor contrasts remain visible via
`effects()` for inspection. Verified at runtime: 7 estimates, 3 poolable.

**5. Quality 0.875; Risk of bias 0.80 despite Bret Contreras's commercial tie.
DEFENSIBLE.** Contreras is commercially associated with the barbell hip thrust
and is both an author and (via BC Strength) a funder — a *direct* conflict on
one of the two compared exercises. The rubric's 0.60 tier is for "authors have
meaningful commercial interest ... but methods appear sound"; the 0.80 tier is
"standard academic context, minor conflicts." The entry-maker scored 0.80 on
the reasoning that (a) the headline glute result is an *equivalence*, not a
finding favourable to the conflicted exercise, and (b) the squat actually
*wins* the quad/adductor contrasts — i.e. the result, if anything, runs against
the conflicted party's commercial interest. That reasoning is sound: the
rubric's risk-of-bias dimension is about whether bias plausibly *shaped the
finding*, and a null-plus-against-interest result is the canonical signal that
it did not. Funding is disclosed; COI is disclosed; the conflicted authors
state they were not involved in data collection/analysis. **0.80 is
defensible.** A reviewer who wanted to be maximally conservative could argue
for 0.70 (a direct product tie is more than the rubric's "run paid workshops"
example), but 0.80 is within reasonable judgement and is explicitly documented,
as the rubric requires. Not a discrepancy. Study design 0.90 (RCT, no
pre-registration) is correct.

**Strength-transfer data as plain constants, not EffectEstimates. SOUND.** The
3RM transfer numbers are a single trial's raw-kg between-group contrasts on a
scale shared with nothing else in the layer, and the optimizer's strength path
is not exercise-selection-keyed. Encoding them as `STRENGTH_TRANSFER_CONTRASTS_KG`
context constants — traceable but inert — is the right call; promoting them to
EffectEstimates would create a phantom poolable set of one. (But: the constants
dict carries the same inverted "HT minus SQ" label — see discrepancy 1.)

**`age_range = (18, 30)`. DEFENSIBLE.** The paper reports ages only as mean±SD
(HT 22±3, SQ 24±4); no explicit min–max is printed. A (18, 30) young-adult
envelope comfortably contains both mean±SD ranges (and even mean±2SD: 16–32 vs
encoded 18–30 is a touch tight at the low end, but mean±2SD is not a population
range and the cohort is described as "college-aged"). The module explicitly
labels this as an envelope, not a verbatim figure, in both the `PopulationSpec`
comment and `notes`. Consistent with how chaves_2020 / maeo_2021 handle the
same situation. Acceptable.

---

## Concerns & discrepancies (ranked)

### MATERIAL — Sign convention stated backwards in the docstring

The module docstring (lines 23–24, 35–36) states the contrast is **"effect = HT
minus SQ"** and the rule **"A negative sign favours the SQUAT (HT grew the site
less); a positive sign favours the HIP THRUST."**

The paper states the opposite. Abstract, verbatim: *"estimates [(−) favors HT;
(+) favors SQ]"*. Results, verbatim: the negative glute-max estimates *"modestly
favored the HT versus SQ"*; the positive quad/adductor estimates mean *"SQ
produced greater mCSA growth."* So in the paper: **negative = hip thrust grew it
more; positive = back squat grew it more.**

(The regression Methods sentence — "group dummy-coded 0 for SQ and 1 for HT" —
would on its own imply a coefficient of HT−SQ; the paper nonetheless presents
and labels the published contrast with the "(−) favors HT; (+) favors SQ"
notation. The published, abstract-level notation is what the encoding must
match, and it is the opposite of the module's stated rule. Whether the figure
plots SQ−HT or flips the axis, the *interpretation* the paper attaches to each
sign is unambiguous and the module contradicts it.)

This is material because the wrong rule has **propagated into the encoded
`notes`**:
- `GLUTE_MAX_UPPER_HT_VS_SQ.notes`: "trivial lean toward the squat" — should be
  *hip thrust*.
- `GLUTE_MAX_LOWER_HT_VS_SQ.notes`: "the largest (still trivial) glute-max lean
  toward the squat" — should be *hip thrust*.
- Docstring narrative lines 38–43: "The point estimates lean trivially toward
  the squat" — should be *hip thrust*.

And it makes the module **internally self-contradictory**: `QUADRICEPS_HT_VS_SQ`
and `ADDUCTORS_HT_VS_SQ` notes correctly say the *back squat* grew those sites
more (positive value) — which is the paper's "(+) favors SQ" — while the
docstring rule says positive favours the hip thrust. The same sign is labelled
two opposite ways within one file.

The encoded `mean` values themselves are all correct, and because the glute
result is a genuine null (every glute CI spans zero), the *equivalence*
conclusion and the 1.0/1.0 emphasis pair are unaffected. But the labelling is
wrong and self-inconsistent, and a maintainer wiring the optimizer's
selection/guidance logic against the stated convention would invert every
glute-region statement.

### MODERATE — Variable names and constant keys bake in the wrong convention

The estimate identifiers are `GLUTE_MAX_UPPER_HT_VS_SQ` etc. and the strength
dict is `STRENGTH_TRANSFER_CONTRASTS_KG` keyed with a docstring saying "HT minus
SQ". "HT_VS_SQ" / "HT minus SQ" naming asserts the HT−SQ direction, which is the
inverted label. The values are right; the names mislead. Because the paper's
own notation is "(−) favors HT; (+) favors SQ", the honest label is **SQ minus
HT** (a contrast where positive = squat advantage, matching every encoded sign).
Renaming the symbols is intrusive, but at minimum the docstring and the inline
"effect = HT minus SQ" comments (lines 23, 231, 268, and the
`__main__` print "HT minus SQ") must be corrected, and the chosen convention
stated once, unambiguously, in the paper's own words.

### MINOR — `combine_emphasis_estimates` lowest-confidence label

Not a Plotkin defect, but worth noting for whoever later adds a second glute
source: `combine_emphasis_estimates` selects the *lowest* confidence via
`max(..., key=conf_order.index)`. If a future high-confidence glute emphasis
source is combined with Plotkin's "medium" pair, the consensus drops to
"medium". That is the intended conservative behaviour and Plotkin's "medium" is
correctly chosen — flagged only so the equivalence label is understood as a
floor.

### MINOR — Measurement dimension wording

The rubric's 1.0 hypertrophy row is literally "MRI muscle *volume*"; this study
used MRI *CSA*. 1.00 is defensible (MRI CSA is clearly the top imaging tier and
above the 0.85 ultrasound/DEXA-CSA row), but a one-line note that the paper
measured CSA not volume, and that 1.00 is read as "MRI imaging, gold-standard
modality", would pre-empt the question. No score change needed.

---

## Recommendations

1. **(MATERIAL) Correct the sign convention throughout the module.** State it
   once, in the paper's own words: *"Contrast notation follows the paper:
   (−) favours the hip thrust (HT grew the site more); (+) favours the back
   squat."* Then:
   - Fix docstring lines 23–24 and 35–36 (the "effect = HT minus SQ" framing and
     the "negative favours the squat / positive favours the hip thrust" rule —
     both inverted).
   - Fix docstring narrative lines 38–43: the glute-max point estimates lean
     trivially toward the **hip thrust**, not the squat.
   - Fix `GLUTE_MAX_UPPER_HT_VS_SQ.notes` and `GLUTE_MAX_LOWER_HT_VS_SQ.notes`:
     "lean toward the squat" → "lean toward the hip thrust".
   - Leave `QUADRICEPS_HT_VS_SQ.notes` and `ADDUCTORS_HT_VS_SQ.notes` as-is —
     they are already correct (squat wins).
2. **(MODERATE) Re-label the contrast direction in names/keys.** Either rename
   the estimate symbols and the `__main__` print from `HT_VS_SQ` / "HT minus SQ"
   to a "SQ minus HT" framing (positive = squat advantage, which matches every
   encoded sign), or — if renaming is too intrusive pre-integration — keep the
   names but add an explicit comment at each definition that the symbol name's
   "HT_VS_SQ" ordering is *not* the algebraic sign direction, and that the
   paper's "(−) favours HT, (+) favours SQ" notation is authoritative. The
   docstring fix in (1) is mandatory either way.
3. **(MODERATE) Fix the strength-constant label.** `STRENGTH_TRANSFER_CONTRASTS_KG`
   docstring says "HT minus SQ"; with `back_squat_3rm: +14` favouring the squat,
   that label is inverted. Change to "SQ minus HT" (or restate as "(−) favours
   HT, (+) favours SQ"). Values stay; only the label changes.
4. **(MINOR) Add a one-line note** that the measurement dimension scores MRI
   *CSA* (the paper's modality), read at the rubric's gold-standard imaging
   tier — to make the 1.00 explicit rather than apparently mismatched against
   the rubric's "MRI volume" wording.
5. No change to any encoded `mean`, `se`, `n`, `quality_score`, `scale`,
   `PopulationSpec`, the Topic, the `_POOLABLE_OVERRIDE`, or the 1.0/1.0
   emphasis pair — all verified correct.

---

## Summary

All encoded numbers verify against the full text and the quality score (0.875)
is arithmetically exact. The non-trivial design decisions the entry-maker
flagged — the dedicated non-poolable raw-cm² scale, the equal-emphasis
equivalence encoding of an underpowered null, the dual EffectEstimate +
emphasis encoding, the new `EXERCISE_SELECTION_HYPERTROPHY` Topic with its
glute-max-only poolable override, and the 0.80 risk-of-bias score despite a
conflicted author — are all sound and defensible. The single material defect is
that the module **states the contrast sign convention backwards**: the paper's
notation is "(−) favours hip thrust, (+) favours squat", but the docstring
asserts the reverse, and that error has propagated into the glute-region
`notes` while the quad/adductor notes use the correct convention — leaving the
module internally self-contradictory. The fix is documentation-only (no encoded
value changes) but must be applied before integration.
