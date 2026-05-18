# Literature Audit — Maeo et al. 2023 (triceps overhead vs. neutral)

**Module audited:** `priors-handoff/app/priors/maeo_2023.py`
**Paper:** Maeo S, Wu Y, Huang M, Sakurai H, Kusagawa Y, Sugiyama T, Kanehisa H, Isaka T.
"Triceps brachii hypertrophy is substantially greater after elbow extension training
performed in the overhead versus neutral arm position." *European Journal of Sport
Science* 2023;23(7):1240-1250. DOI 10.1080/17461391.2022.2100279. PMID 35819335.
**Audit date:** 2026-05-17
**Auditor:** Independent priors-layer literature auditor

---

## Sources accessed

The paper is Open Access (Creative Commons Attribution 4.0), published by Taylor &
Francis. I read it fresh, independent of the module's encoding.

| Source | URL / record | Result |
|---|---|---|
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/35819335/ | **Accessed** — full abstract with all headline numbers |
| Publisher full text (HTML) | https://www.tandfonline.com/doi/full/10.1080/17461391.2022.2100279 | HTTP 403 (bot-blocked) — not used |
| Open-access PDF (uniguacu.com.br mirror) | https://uniguacu.com.br/.../Artigo-Hipertrofia-do-triceps-braquial-1.pdf | **Accessed** — full text (Introduction → References, ~47k chars) extracted locally with pdfminer.six. This is the published Taylor & Francis PDF, verified by DOI, journal, volume/issue/pages, and CC-BY notice. |
| ECU institutional repository | https://ro.ecu.edu.au/cgi/viewcontent.cgi?article=6999... | HTTP 403 — not used |
| ResearchGate | publication/361956092 | Not fetched (PDF mirror already gave full text) |

**Full text obtained.** Methods, Results, Discussion, Acknowledgments, Disclosure, and
Funding were all read directly. The one section I could **not** inspect is
**Supplementary data 1** ("see Table for details, Supplementary data 1"), which holds
per-condition pre/post volumes and the bootstrap CIs. The main-text Results paragraph
reports the absolute change means and SDs underlying every Cohen's d, so the headline
numbers are fully verifiable without the supplement; only the bootstrap CIs are not.

---

## Verdict

**MINOR DISCREPANCIES** (one of which is conceptually significant for downstream pooling).

Every headline number the module encodes — the six growth percentages, the three
Cohen's d values, the three p-values, n=21, the within-participant design, 70% 1RM /
5×10 / 2×wk / 12 wk, and the 34–39% lower overhead load — is **faithfully and
correctly transcribed from the paper.** The emphasis-ratio arithmetic is correct and
the quality score recomputes exactly to 0.89. However, the module **mischaracterises
what Cohen's d measures.** The paper is explicit that d is the *between-condition*
effect size "based on absolute change values" — i.e. a standardized difference between
the overhead and neutral arms. The module's `EffectEstimate` notes say the opposite:
that d "is the ABSOLUTE growth in the overhead condition, not a difference effect
size." That is backwards. The encoded `mean` values (0.61, 0.39, 0.54) *are* in fact
difference SMDs and *are* poolable as such — but the module's own warning tells a
future maintainer they are not, which would cause them to be mishandled. Separately,
the `_paired_se` formula does not match how the paper actually computed d (a pooled-SD
ANCOVA-context comparison, not a paired-d formula), and the population `age_range` is
encoded as a wider band than the data support. None of these corrupt the numbers; they
corrupt the *metadata describing the numbers*. Hence MINOR, not MATERIAL — but the
d-interpretation note should be fixed before any cross-study pooling is built on it.

---

## Value-by-value verification

Paper section references: **Abstract**; **Methods → Participants and study overview**
(p.1241–1242); **Methods → Training programme** (p.1242–1243); **Methods → Statistical
analysis** (p.1244); **Results → Muscle volume** (p.1244); **Acknowledgments / Funding /
Disclosure** (p.1248–1249).

| Encoded value | Paper value | Match? | Notes |
|---|---|---|---|
| TBLong overhead +28.5% | +28.5% | ✅ | Results → Muscle volume; ANCOVA-adjusted mean change. |
| TBLong neutral +19.6% | +19.6% | ✅ | Same sentence. |
| TBLat+Med overhead +14.6% | +14.6% | ✅ | Results → Muscle volume. |
| TBLat+Med neutral +10.5% | +10.5% | ✅ | Same sentence. |
| Whole-TB overhead +19.9% | +19.9% | ✅ | Results → Muscle volume. (Discussion text once writes "+13.5%" for the neutral arm — a typo in the paper itself; the Results section and Abstract both say +13.9%, which is what the module uses. Module is correct.) |
| Whole-TB neutral +13.9% | +13.9% | ✅ | Abstract + Results. |
| d = 0.61 (TBLong) | d = 0.61 [medium] | ✅ (value) / ⚠️ (interpretation) | Results: "Cohen's d = 0.61 [medium] based on absolute changes of 50.6 ± 30.6 vs 34.5 ± 21.2 cm³." It is a **between-condition** d, not a paired/within d, and not an "absolute growth" effect. See Methodology audit. |
| d = 0.39 (TBLat+Med) | d = 0.39 [small] | ✅ (value) / ⚠️ | Based on absolute changes 42.1 ± 33.4 vs 30.4 ± 26.9 cm³. |
| d = 0.54 (Whole-TB) | d = 0.54 [medium] | ✅ (value) / ⚠️ | Based on absolute changes 92.8 ± 58.1 vs 64.9 ± 45.2 cm³. |
| P < 0.001 (TBLong) | P < 0.001 | ✅ | Results. |
| P = 0.002 (TBLat+Med) | P = 0.002 | ✅ | Results. |
| P < 0.001 (Whole-TB) | P < 0.001 | ✅ | Results. |
| n = 21 per condition | 21 arms per condition (within-participant) | ✅ | Methods. Note `EffectEstimate.n` is documented in `shared.py` as "total participants" — here 21 is both the participant count and the per-condition arm count, so it is fine, but see Concerns. |
| 14 M, 7 F | 14 males + 7 females = 21 | ✅ | Methods → Participants. |
| Mean age ~23 | Males 23.0 ± 1.4 y; females 24.3 ± 1.6 y | ✅ | "~23" is a fair summary; pooled mean ≈ 23.4. |
| `age_range=(20, 30)` | SDs imply roughly 21–27 y observed | ⚠️ | Paper gives means ± SD, not an explicit min/max range. (20, 30) is wider than the data support. Minor; see Recommendations. |
| Untrained | "none had been involved in any type of systematic resistance training programme in the past 12 months" | ✅ | Methods → Participants. "Untrained" is the correct `TrainingStatus` mapping. |
| 12-week within-participant design | 12 weeks, within-participant comparison model | ✅ | Methods + Introduction. |
| 70% 1RM, 5×10, 2×/week | 70% 1RM (after ramp), 10 reps × 5 sets, 2 sessions/week | ✅ | Methods → Training programme. Minor nuance: load ramped 50→60→70% over sessions 1–3, then 70% with +5% progressions. The module's "70% 1RM" is the steady-state value and is a fair shorthand. |
| 34–39% lower overhead load | "−34−39%, P < 0.001" absolute load/1RM lower in overhead | ✅ | Abstract; corroborated by 1RM data (Pre 7.2 vs 11.5 kg; Post 12.0 vs 18.3 kg). |
| Journal = European Journal of Sport Science | Confirmed | ✅ | |
| DOI 10.1080/17461391.2022.2100279 | Confirmed | ✅ | |
| Year 2023 | Issue 23(7) is 2023 (published online 2022) | ✅ | Citing 2023 is correct. |
| MRI muscle volume | MRI-measured ACSA → volume, investigators blinded | ✅ | Methods → MRI. Gold-standard, supports measurement = 1.00. |
| "raw data in supplements" (quality comment) | Supplementary data 1 = a *table* of details; bootstrap CIs in Figure 4 | ⚠️ | The paper provides a supplementary **table**, not a raw-data/code deposit. "Raw data" overstates it slightly — see quality discussion. |
| No commercial conflict | "No potential conflict of interest was reported"; funded by Descente & Ishimoto Memorial Foundation for the Promotion of Sports Science (academic sports-science grant) | ✅ | Disclosure + Funding. |

---

## Math checks

### 1. SE recomputation — `_paired_se(d, n) = sqrt(1/n + d²/(2n))`, n = 21

| Effect | d | Module SE (recomputed) | 95% CI on d (mean ± 1.96·SE) |
|---|---|---|---|
| TBLong | 0.61 | **0.2377** | (0.144, 1.076) |
| TBLat+Med | 0.39 | **0.2264** | (−0.054, 0.834) |
| Whole-TB | 0.54 | **0.2336** | (0.082, 0.998) |

The arithmetic in the formula is correct, and the module's inline comment ("≈ 0.236
for d=0.61") rounds 0.2377 acceptably.

**But the formula is the wrong formula for this study.** `sqrt(1/n + d²/(2n))` is the
large-sample SE for an **independent-groups (between-subjects) Cohen's d**, where n is
the per-group size. It is *not* the SE of a paired/within-participant d. For a paired
design the SE of d depends on the pre-post (or arm-to-arm) correlation r:
`Var(d_paired) ≈ (1/n + d²/(2n)) · 2(1−r)` (one common approximation). The module both
names the function `_paired_se` and comments "Approximate SE for paired Cohen's d" —
but the formula it contains is the *unpaired* one. So the label is wrong relative to
the formula.

There is a deeper issue. The paper did **not** report a paired d at all. Methods →
Statistical analysis: *"Effect sizes of between-condition differences were calculated
as Cohen's d values based on absolute change values."* Independent reconstruction from
the change-score means and SDs in the Results confirms this is a pooled-SD,
between-condition d:

- TBLong: (50.6 − 34.5) / sqrt((30.6² + 21.2²)/2) = **0.612** → reported 0.61 ✓
- TBLat+Med: (42.1 − 30.4) / sqrt((33.4² + 26.9²)/2) = **0.386** → reported 0.39 ✓
- Whole-TB: (92.8 − 64.9) / sqrt((58.1² + 45.2²)/2) = **0.536** → reported 0.54 ✓

All three reproduce to two decimals. The d values are a **standardized difference
between the two arms' change scores**, using the pooled SD of those change scores.
This is genuinely a difference effect size (good — it *is* poolable), but it is
neither "paired" nor "absolute growth." Because the two arms belong to the same
participants, those change scores are correlated, so even the pooled-SD-of-changes d
is not a textbook independent-groups d either; the paper layered it on top of a linear
mixed-effects model / ANCOVA. The honest SE here is not cleanly recoverable from
`(d, n)` alone without the arm-to-arm correlation, which lives in the unread
supplement. The current SE is therefore a defensible rough approximation but is
**mislabeled** and likely **somewhat too large** (ignoring the within-participant
correlation inflates it). See Recommendations.

### 2. Emphasis-ratio arithmetic

| Pair | Encoded expression | Computed | Module comment | Match? |
|---|---|---|---|---|
| Pushdown long head | 19.6 / 28.5 | **0.6877** | "≈ 0.69" | ✅ |
| Pushdown lat+med | 10.5 / 14.6 | **0.7192** | "≈ 0.72" | ✅ |
| Pushdown whole | 13.9 / 19.9 | **0.6985** | "≈ 0.70" | ✅ |

Arithmetic is exact. Overhead variants are hard-coded to 1.0 by construction.
(Methodology of the ratio itself is audited below — the arithmetic is fine; the
*derivation method* is the questionable part.)

### 3. Quality-score recomputation

Per-dimension scores and rubric v1.0 weights:

```
design  0.90 × 0.20 = 0.180
sample  0.80 × 0.15 = 0.120
meas    1.00 × 0.20 = 0.200
method  0.85 × 0.15 = 0.1275
report  0.95 × 0.10 = 0.095
bias    0.90 × 0.10 = 0.090
pop     0.85 × 0.10 = 0.085
                      ------
total              = 0.8975  → 0.89  ✅
```

The weighted average is arithmetically exact (0.8975 → 0.89). No flat modifiers apply
(open-access, no conflict, single primary RCT-style design, no I² heterogeneity since
it is not a meta-analysis). The rounding direction (0.8975 → 0.89) is conventional.

**Defensibility of the individual dimension scores** (the rubric requires reading the
paper, which I did):

- **Study design 0.90** — The rubric has no row that exactly fits a within-participant
  *contralateral-limb* training study. The closest rows are "RCT with minor design
  issues" (0.9) and "Within-subject design with confounds (e.g., side-to-side
  studies)" (**0.5**). This *is* a side-to-side (contralateral-arm) study. Arm
  assignment was randomized/counterbalanced and order counterbalanced, which controls
  the obvious confounds, and the design is a recognized powerful model for hypertrophy
  comparisons (MacInnis 2017, cited). But a literal reading of the rubric's 0.5 row
  would pull this down hard. **0.90 is generous; a defensible range is 0.7–0.9.** This
  is the single most debatable input. If scored at 0.7, the weighted average drops to
  0.8575 → 0.86. The module should document this as a deliberate rubric deviation (the
  rubric's "When to deviate" section explicitly allows it) rather than leaving it
  implicit.
- **Sample size 0.80** — n=21 per condition falls in the rubric's 15–24 band = 0.80.
  Correct.
- **Measurement 1.00** — MRI muscle volume = gold standard, blinded analysis. Correct.
- **Methodological rigor 0.85** — ANCOVA with baseline covariate + linear mixed model,
  normality/homoscedasticity checked, estimation statistics with bootstrap CIs. No
  pre-registration mentioned. Rubric 0.8 row ("no pre-reg but otherwise rigorous") to
  0.9 ("pre-registration"). 0.85 is reasonable; arguably 0.80 since there is no
  pre-reg. Minor.
- **Reporting transparency 0.95** — Effect sizes with bootstrap CIs, clear protocol, a
  supplementary table. Rubric 0.9 = "full effect sizes with CIs, data available on
  request"; 1.0 = "raw data + code on OSF/GitHub." There is **no** OSF/GitHub raw-data
  or code deposit — only a supplementary table. **0.95 is slightly high; 0.90 is the
  rubric-correct value.** The module comment "raw data in supplements" overstates what
  the supplement contains.
- **Risk of bias 0.90** — Academic grant (Descente and Ishimoto Memorial Foundation,
  a sports-science foundation), explicit "no potential conflict of interest." Rubric
  0.9 = "academic funding, modest conflicts disclosed"; 1.0 requires a publication-bias
  analysis (N/A for a single trial). 0.90 is correct, arguably could be higher given a
  genuinely clean disclosure, but 0.9 is fine.
- **Population specificity 0.85** — Tight, well-described sample (sex-split means ± SD
  for age/height/mass, explicit training-status exclusion criterion, ethics approval
  number). This is closer to the rubric's 1.0/0.9 rows ("tight, well-described
  population … with documented inclusion/exclusion criteria"). **0.85 is mildly
  conservative; 0.90 would be defensible.** Not a problem.

Net: the 0.89 is arithmetically exact and broadly defensible, but it rests on a
**generous Study-design score** (0.90 vs. a literal-rubric 0.5–0.7 for side-to-side
designs) partly offset by a **generous Reporting score** (0.95 vs. 0.90). These roughly
cancel, so 0.89 is an acceptable final number — but the derivation should be made
honest: either drop Study design and note the deviation, or explicitly invoke the
"when to deviate" clause. As-is, the comment block presents debatable judgment calls as
if they were straight rubric lookups.

---

## Methodology audit — the `ExerciseEmphasis` derivation

This is where the module is weakest. The arithmetic is fine; the *construct* is shaky.

**The derivation:** `emphasis(exercise) = (% growth in that exercise) / (% growth in
overhead extension)`, with overhead extension pinned to 1.0.

### Problem 1 — "ratio of percent muscle growth" is not a sound [0,1] emphasis scale.

`ExerciseEmphasis.emphasis` is documented in `shared.py` as "fraction of maximum
stimulus this exercise provides … 1.0 = the exercise that maximally stimulates this
muscle." A ratio of 12-week hypertrophy percentages is not a stimulus fraction:

- **It is intervention-, duration-, and population-specific.** 19.6/28.5 = 0.69 is the
  ratio of *outcomes after this specific 12-week, 2×/week, 70%-1RM, untrained-subject
  protocol*. Hypertrophy is non-linear in time and saturating; the same two exercises
  over 24 weeks, or in trained lifters, would not yield 0.69. The coefficient is being
  treated as a stable exercise property when it is actually a study endpoint.
- **The floor is not 0.** A pushdown still grew the long head +19.6% — substantial
  hypertrophy, not "0.69 of the stimulus and 0.31 of nothing." An emphasis scale where
  1.0 = max should arguably have its zero anchored at "no stimulus," not at "the
  weaker of two real exercises." Both exercises here would sit near the top of any
  honest [0,1] triceps-emphasis scale; encoding pushdown at 0.69 understates it
  relative to, say, a bench press.
- **Ratios of percentages discard the baseline.** Percent change depends on starting
  volume. The two arms had near-identical baselines (within-participant design), so
  here the distortion is small — but the *method* as a general recipe ("as we add more
  papers… re-normalize") will break the moment it is applied across studies with
  different baseline volumes or different measurement modalities.

### Problem 2 — normalizing the single best-studied exercise to exactly 1.0.

The module's own comment admits this: *"we're assuming the best exercise we have data
for is also the best exercise that exists."* That assumption is false in general and
the module knows it. Overhead cable extension is a strong long-head exercise but is
very unlikely to be the literal global maximum (e.g., a fully-stretched overhead
*barbell/dumbbell* extension, or a long-head-biased preacher-style movement, could
plausibly exceed it). Pinning it to 1.0 means **every other exercise's coefficient is
silently capped** and the whole scale must be rebuilt the moment a better exercise is
studied. That re-normalization is not a minor maintenance note — it changes every
existing coefficient and any optimizer decision derived from them. A safer design
pins 1.0 to a *defined reference* (e.g., "best-studied as of v1") and treats it as
provisional, or expresses emphasis on an absolute scale (e.g., growth per set) so new
exercises slot in without disturbing old ones.

### Problem 3 — confidence labels.

- **Long head "high":** Defensible. This is the paper's primary, pre-stated hypothesis,
  the largest effect (d=0.61, P<0.001), and mechanistically expected. "High" for the
  *direction and existence* of a long-head advantage is fair.
- **Lat+Med "medium":** The module's reasoning ("unexpected finding, mechanism
  unclear") is sound and matches the paper — the authors explicitly *refuted their own
  second hypothesis* and offer only speculative mechanisms (metabolic stress, force
  redistribution). Also note d=0.39 is "small" and the paper says the 95% CI overlap
  was *larger* for TBLat+Med than for TBLong. "Medium" confidence is appropriate, even
  arguably should be "low" for the lat+med given a small effect the authors did not
  predict. Acceptable as-is.
- However, **confidence should also reflect that the emphasis number is a single-study,
  single-comparison value.** Only two exercises were ever compared. Calling the
  long-head coefficients "high" confidence risks the optimizer treating 0.69 as a
  well-established constant. The confidence field conflates "confident the effect is
  real" with "confident this exact coefficient is right." It is the former, not the
  latter.

### Problem 4 — only two exercises, both cable.

Both data points are *cable* elbow extensions. The exercise keys `cable_overhead_extension`
and `cable_pushdown` are appropriately specific (good — they do not over-claim to
"overhead extension" generally). But the emphasis registry will contain exactly two
triceps exercises from this paper, both variants of one movement. Any optimizer
choosing "exercises for long-head emphasis" from this prior alone is effectively
choosing between two cable setups. That is a coverage limitation, not an error, but it
should be flagged so the prior is not over-trusted.

**Bottom line on methodology:** the `ExerciseEmphasis` values are *internally
consistent and correctly computed*, and as a **provisional, relative, within-this-paper
ranking** they are usable. But the derivation method ("ratio of percent growth,
normalize best-studied to 1.0") does not produce a quantity that means what
`shared.py` says `emphasis` means, and it does not generalize across papers. This is a
design concern to resolve before the optimizer leans on these numbers, not a
transcription error.

---

## The Maeo-vs-Varovic conceptual claim

The module docstring asserts Maeo answers "whole-muscle differences between exercises"
while regional-hypertrophy meta-analyses (Varovic 2025) ask about proximal/mid/distal
differences *within* a muscle, and that these are different questions.

**This framing is accurate.** Maeo measured **whole-volume** changes of three
*anatomically distinct* structures — TBLong, TBLat+Med, Whole-TB — each summed over the
entire muscle length from most-proximal to most-distal slice (Methods → MRI). It did
**not** partition any single head into proximal/mid/distal regions. So Maeo is a
**between-head / between-exercise whole-muscle** comparison, exactly as the docstring
says. The long head and the lateral+medial heads are separate muscles with separate
architecture and (for the long head) a separate joint crossing — comparing their
growth is not the same as the "regional hypertrophy" question of whether one *site
within one muscle* grows more.

One precision note: the docstring frames Maeo as "does overhead extension grow the
long head more than pushdown does?" — correct — but readers should not over-read it.
Maeo's clean causal contrast is **overhead vs. neutral arm position for the same
movement pattern**, which the paper attributes substantially to long-head muscle
*length* during the exercise (plus blood-flow/force-redistribution for the monoarticular
heads). It is a length/position study that happens to map onto two named gym
exercises. The module's exercise-selection use is reasonable but the underlying
variable is "arm position," not "exercise brand." This does not contradict the
docstring; it just sharpens it.

---

## Concerns & discrepancies

1. **[Significant — interpretation] The `EffectEstimate` notes invert what Cohen's d
   is.** Lines 96–99 state d "is the ABSOLUTE growth in the overhead condition, not a
   difference effect size." The paper (Methods → Statistical analysis; Results) is
   explicit that d is the **between-condition difference** effect size based on
   absolute change values. Independent reconstruction confirms this. The encoded
   `mean` values are correct *as difference SMDs* — but the note tells a future
   maintainer they are not poolable as differences, which is exactly wrong and would
   cause them to be excluded from or mishandled in cross-study pooling. The
   `scale="standardized_mean_diff"` field, by contrast, *is* correct. So the structured
   field and the prose note contradict each other; the note is the wrong one.

2. **[Minor — label/formula] `_paired_se` contains the unpaired formula.** The function
   name and docstring say "paired," but `sqrt(1/n + d²/(2n))` is the independent-groups
   SE. The paper computed a pooled-SD between-condition d (with the data being
   within-participant, so correlated). The current SE ignores the arm-to-arm
   correlation and is therefore likely conservative (too wide). Acceptable as a rough
   approximation if relabeled honestly; not acceptable as "paired SE."

3. **[Minor] `n` semantics.** `EffectEstimate.n` is documented as "total participants."
   The module passes 21, which is simultaneously the participant count and the
   per-condition arm count, so the value is fine here — but for a within-participant
   design the *effective* sample for a between-condition contrast is not simply 21
   independent observations per arm. `combine_inverse_variance` and `best_applicable`
   both use `n` (via `sqrt(n)` and via SE); the design's non-independence is invisible
   to them. Worth a one-line note.

4. **[Minor] `age_range=(20, 30)`** is wider than the paper supports. The paper reports
   age as means ± SD (males 23.0 ± 1.4; females 24.3 ± 1.6), implying nearly all
   participants were ~21–27. (20, 30) will make `applicability_to()` score, e.g., a
   29-year-old user as a perfect in-range match when they are actually outside the
   studied sample. Tighten to roughly (21, 27) or (20, 28).

5. **[Minor] Quality comment "raw data in supplements"** overstates the supplement,
   which is a results *table*, not a raw-data/code deposit. This is the basis for the
   Reporting score of 0.95; rubric-correct is 0.90.

6. **[Minor — disclosure] Quality comment "Study design 0.90 (within-participant RCT)"**
   — the study is a within-participant *contralateral-limb training* study; the
   rubric's literal row for side-to-side designs is 0.5. 0.90 is a deliberate (and
   arguably reasonable) deviation, but it is presented as a plain rubric lookup. The
   rubric requires deviations to be documented with reasoning.

7. **[Methodology — not a transcription error] `ExerciseEmphasis` derivation.** Ratio
   of percent growth, best-studied exercise pinned to 1.0. See the Methodology section.
   Usable as provisional/relative values; does not match the `emphasis` construct as
   defined in `shared.py` and does not generalize across studies.

8. **[Cosmetic] CITATION lacks `osf_url`.** Correct — there is no OSF deposit. No
   action; noted only to confirm it is intentional, not an omission.

**Nothing rises to MATERIAL.** No encoded growth percentage, d value, p-value, or
design fact is wrong. The discrepancies are all in *metadata and interpretation*.

---

## Recommendations (concrete)

1. **Fix the inverted Cohen's d note** (highest priority). Replace the lines in the
   "Whole-muscle effect estimates" comment and in each `EffectEstimate.notes` that
   say d is "the ABSOLUTE growth in the overhead condition, not a difference effect
   size." The paper's d **is** a between-condition difference SMD (overhead − neutral,
   standardized by the pooled SD of the change scores). State that explicitly. The
   `scale="standardized_mean_diff"` field is already correct and should stay.

2. **Rename `_paired_se` and correct its docstring.** It implements the
   independent-groups SE. Either (a) rename to `_unpaired_se_approx` and add a comment
   that it ignores the within-participant correlation and is therefore likely
   conservative, or (b) if the arm-to-arm correlation can be recovered from
   Supplementary data 1, switch to a genuine paired-d SE. Until the supplement is
   inspected, (a) is the honest choice. Also lower the Reporting dimension to 0.90 to
   reflect that SE had to be approximated rather than read off the paper.

3. **Tighten `age_range`** from (20, 30) to approximately (21, 27) to match the
   reported age means ± SD, so `applicability_to()` does not over-credit users in
   their late twenties / at 30.

4. **Recompute and document the quality score honestly.** The 0.89 is arithmetically
   exact, but Study design 0.90 and Reporting 0.95 are both judgment calls dressed as
   rubric lookups. Recommended: keep Study design at 0.85–0.90 but add a one-line
   deviation note ("contralateral-limb design; rubric's 0.5 side-to-side row deviated
   from because allocation was randomized/counterbalanced and the model is established
   — see rubric 'When to deviate'"), and drop Reporting to 0.90 (no OSF/code deposit).
   With Reporting 0.90 the weighted average becomes 0.8925 → still rounds to 0.89, so
   the final number need not change — only the justification.

5. **Re-label the `ExerciseEmphasis` values as provisional and add a method caveat.**
   Add a comment that `emphasis` here is a *within-this-study relative ranking* derived
   from a ratio of 12-week percent-growth outcomes, not a study-independent stimulus
   fraction, and that the 1.0 anchor is "best-studied so far," not "global maximum."
   Consider downgrading the long-head confidence from "high" to "medium" for the
   *coefficient* (the *direction* is high-confidence; the exact 0.69 is one comparison
   from one study). At minimum, ensure the optimizer that consumes these treats them as
   soft priors with wide uncertainty, not constants.

6. **Add a non-independence note for `n=21`.** A one-line comment that 21 is a
   within-participant arm count and the between-condition contrast does not have 21
   independent observations per arm, so downstream `sqrt(n)` weighting in
   `best_applicable` slightly over-credits this study's statistical power.

7. **Fix the Whole-TB neutral typo reference (no module change needed).** The module
   correctly uses +13.9%. For completeness in the audit trail: the paper's Discussion
   once prints "+13.5%" for the neutral arm — this is a typo in the paper; Abstract and
   Results both say +13.9%. The module is right; no action.

---

## Summary

I re-read the full open-access paper fresh (PubMed abstract plus the complete Taylor &
Francis PDF; the publisher HTML and ECU repository were bot-blocked, and Supplementary
data 1 could not be inspected). **Every headline number in the module is faithfully and
correctly transcribed** — all six growth percentages, all three Cohen's d values, all
three p-values, the design, the protocol, the population, and the 34–39% lower overhead
load — and the emphasis ratios (0.69/0.72/0.70) and the 0.89 quality score recompute
exactly. The verdict is **MINOR DISCREPANCIES**, driven by metadata rather than data.
The most important finding: the module's `EffectEstimate` notes **invert what Cohen's d
means** — they claim d is "absolute growth, not a difference effect size," whereas the
paper explicitly defines d as the *between-condition difference* effect size, and
independent reconstruction from the change-score means/SDs confirms it; this should be
corrected before any cross-study pooling relies on it. Secondary issues: `_paired_se`
actually implements the *unpaired* SE formula, `age_range` is wider than the data
support, and the `ExerciseEmphasis` "ratio of percent growth, best-studied = 1.0"
derivation is internally consistent but does not match the `emphasis` construct defined
in `shared.py` and will not generalize across studies — it should be flagged as a
provisional within-study ranking.
