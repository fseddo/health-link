# Audit — `pedrosa_2023.py`

**What was audited:** `app/priors/pedrosa_2023.py` — the prior module encoding
Pedrosa et al. 2023 ("Training in the Initial Range of Motion Promotes Greater
Muscle Adaptations Than at Final in the Arm Curl", *Sports* 11(2):39,
DOI 10.3390/sports11020039, PMID 36828324), checked value-by-value against the
paper read fresh from source.

**Auditor:** independent literature auditor (priors layer)
**Date:** 2026-05-17

---

## Sources accessed

| Source | URL | Reached | Used for |
|---|---|---|---|
| PMC full text (open access) | https://pmc.ncbi.nlm.nih.gov/articles/PMC9960616/ | Yes (2 fetches) | Methods, Results, abstract, demographics, funding, ICCs |
| MDPI article page | https://www.mdpi.com/2075-4663/11/2/39 | **No** — WebFetch permission denied for that host | n/a (cross-check fell back to PMC + web search) |
| PubMed / web search (PMID 36828324) | https://pubmed.ncbi.nlm.nih.gov/ + general search | Yes | Cross-check of CSA results, p-values, design |
| Varovic 2025 included-study search | web search around PMID 40570881 / SportRxiv preprint | Yes | Confirming Pedrosa 2023 is inside Varovic's pool |

Note: the MDPI page itself could not be fetched (host-level WebFetch denial).
The PMC open-access full text was read in full instead, which carries the same
peer-reviewed content, so no verification was lost — only a redundant
cross-check source. Varovic 2025's full included-study table is paywalled; the
inclusion of Pedrosa 2023 was confirmed from multiple secondary descriptions of
that meta-analysis rather than its primary table (see caveat below).

---

## Verdict

**MINOR DISCREPANCIES.**

The module is a faithful, careful, and unusually honest encoding of the paper.
All three effect sizes (d = 0.89 / 0.23 / 0.39), the design (within-participant
contralateral, 21 enrolled / 19 completed), the ROM definitions, the
measurement method and ICCs, the funding/COI facts, and the quality-score
arithmetic (0.83) all check out against the primary source. The
encoding-shape decision (EffectEstimate not ExerciseEmphasis) and the
not-poolable-with-Varovic decision are both well-reasoned and correct.

Two genuine discrepancies, both minor: (1) the **mid-site p-value is reported
inconsistently *by the paper itself*** — the Abstract says `p = 0.311`, the
Results sentence says `p = 0.331`. The module encodes `0.331`, which matches the
Results text but not the abstract; the module should note the paper's internal
inconsistency rather than presenting `0.331` as unambiguous. (2) The module's
docstring and comments repeatedly say the CSA sites are "**50% and 70% of
humerus length**"; the paper actually measures at **"50% and 70% of the distance
from the acromion to the lateral epicondyle"** and the Results phrase it as
"% of biceps brachii length". "Humerus length" is a loose paraphrase that is
close but not what the paper says. Neither discrepancy changes any encoded
number or the verdict's substance.

---

## Value-by-value verification

| Item | Module value | Paper value | Source location | Verdict |
|---|---|---|---|---|
| Design | within-participant, contralateral arms | "Each participant's upper limb was allocated in a randomized fashion… order of training was counterbalanced" | Methods | OK |
| Enrolled / completed | 21 enrolled, 19 completed (2 withdrew) | "21 untrained women"; "Two participants withdrew… 19 women completed" | Participants | OK |
| Sex | female | "untrained women" | Participants | OK |
| Training status | untrained, no activity ≥6 months | "had not performed any physical activity for at least six months" | Participants | OK |
| INITIAL ROM | elbow 0–68° | "trained from 0° to 68° of elbow flexion" | Methods | OK |
| FINAL ROM | elbow 68–135° | "trained from 68° to 135° of elbow flexion" | Methods | OK |
| INITIAL = longer muscle length | yes (0° = extended elbow → flexors longer) | 0° = full extension; flexors are at greater length nearer extension | Methods + biomechanics | **OK — confirmed correct** (see note below) |
| Duration / frequency | 8 weeks, 3×/week | "eight-week study period… three times per week" | Methods | OK |
| Exercise | seated dumbbell preacher curl | "seated dumbbell preacher curl" | Methods | OK |
| Sets | 4 sets, rising to 5 from week 5 | "four sets per session"; "Five sets… from the fifth week on" | Methods | OK — module says "4–5 sets", correct |
| To failure | yes | "all sets were carried out until volitional failure" | Methods | OK |
| CSA method | B-mode ultrasound | "B-mode ultrasound (MindRay DC-7)" | Methods | OK |
| CSA sites | "50% and 70% of humerus length" | "50% and 70% of the distance from the acromion to the lateral epicondyle" / "% of biceps brachii length" | Methods / Results | **Minor discrepancy** — "humerus length" is a paraphrase; the reference landmark is acromion→lateral-epicondyle ("biceps length"), not the humerus bone |
| Blinding | blinded CSA analysis | "images were saved… coded for blinded CSA calculation" | Methods | OK |
| ICCs | "0.92–0.94" | ICC3,1 = 0.94 (50%) and 0.92 (70%) | Methods | OK |
| **Distal (70%) d** | 0.89 | ES = 0.89 | Results | OK |
| **Distal (70%) p** | 0.001 | p = 0.001 | Results / Abstract | OK |
| **Mid (50%) d** | 0.23 | ES = 0.23 | Results | OK |
| **Mid (50%) p** | 0.331 | Results: p = 0.331; **Abstract: p = 0.311** | Results vs Abstract | **Minor discrepancy** — paper is internally inconsistent; module matches Results, should flag |
| **Summed (50%+70%) d** | 0.39 | ES = 0.39 | Results | OK |
| **Summed p** | 0.111 | p = 0.111 | Results / Abstract | OK |
| Direction of positive d | favours INITIAL (longer length) | "Positive d values indicate larger gains in INITIALROM" | Results | OK |
| CI on d? | "paper reports 95% CIs only on the raw cm² difference, not on d" | CIs reported are in cm² (e.g. distal 0.18–0.59 cm²) | Results | **OK — confirmed**; no CI for d itself |
| Strength (context only) | INITIAL +42.8% vs FINAL +19.0%, d=1.05, p<0.001 | "42.8 ± 14.8%" vs "19.0 ± 10.3%", ES = 1.05, p < 0.001 | Results | OK — correctly recorded as context, not encoded |
| Funding | FAPEMIG / CAPES / UFMG, "no external funding" | "Supported by the FAPEMIG; CAPES (Brazil); PRPq of UFMG"; "received no external funding" | Funding | OK |
| COI | BJS on Tonal Corp. advisory board; others none | "B.J.S. serves on the scientific advisory board for Tonal Corporation… other authors declare no conflicts" | COI | OK |

### Note on "INITIAL = longer muscle length"

This is the single most important directional fact and it is **correct**. At
0° of elbow flexion the elbow is fully extended; the elbow flexors (biceps
brachii) are at their longest. The INITIAL ROM (0–68°) therefore trains the
flexors through the lengthened, stretched portion of the curl, and the FINAL
ROM (68–135°) trains the shortened portion. The module's docstring states this
explicitly and correctly ("0 = extended elbow → elbow flexors at the LONGER
muscle length"). This is the load-bearing claim that makes the paper a
"long-length training" study, and it is right.

---

## Math checks

### SE reconstruction (`_unpaired_d_se(d, n) = sqrt(1/n + d²/(2n))`, n = 19)

`1/19 = 0.0526316`. Recomputed:

| Estimate | d | d²/(2·19) | SE = sqrt(...) | Module SE (`__post_init__` would store) | 95% CI (Normal) |
|---|---|---|---|---|---|
| Distal | 0.89 | 0.0208447 | **0.27107** | matches `_unpaired_d_se(0.89,19)` | (0.359, 1.421) |
| Mid | 0.23 | 0.0013921 | **0.23243** | matches `_unpaired_d_se(0.23,19)` | (−0.226, 0.686) |
| Summed | 0.39 | 0.0040026 | **0.23798** | matches `_unpaired_d_se(0.39,19)` | (−0.076, 0.856) |

The formula is applied correctly and reproduces the helper's output. All SEs
are positive, so `EffectEstimate.__post_init__` will not raise.

**Is the unpaired formula sound for a within-participant design?** Yes, as a
*conservative* approximation, and the module says exactly that. For a paired
design the true SE of d is smaller (it depends on the arm-to-arm correlation r,
which the paper does not publish). The unpaired large-sample formula ignores r
and therefore over-states uncertainty — it produces a too-wide CI, never a
too-narrow one. That is the safe direction to err. This is consistent with the
`maeo_2023` exemplar, which uses the identical helper and the identical
justification. **One subtlety the module gets right and is worth highlighting:**
the comment correctly warns that `ci_95` will *not* reproduce the paper's cm²
interval because d and the cm² difference are different quantities — so a
re-auditor mechanically diffing intervals against the paper would otherwise be
misled.

**Does the paper report a CI for d?** No. Confirmed from the Results: the only
CIs given are on the raw cm² mean difference (distal 0.18–0.59 cm²; mid −0.10 to
0.34 cm²; summed −0.08 to 0.67 cm²). There is no published CI or SE for the
Cohen's d, so reconstruction from (d, n) is genuinely necessary. The module's
Reporting score of 0.80 already reflects this ("the CIs are on the raw cm²
difference… no per-arm pre/post descriptives").

One residual caveat the module *already* states honestly: `n = 19` is the
completer count, and the between-condition contrast does not carry 19
independent observations per arm, so `best_applicable()`'s `sqrt(n)` weighting
slightly over-credits this study. Acceptable and disclosed.

### Quality-score recomputation (rubric v1.0 weights)

Per-dimension scores from the module comments, with rubric weights:

| Dimension | Score | Weight | Contribution |
|---|---|---|---|
| Study design | 0.88 | 0.20 | 0.1760 |
| Sample size | 0.80 | 0.15 | 0.1200 |
| Measurement | 0.85 | 0.20 | 0.1700 |
| Methodological rigor | 0.80 | 0.15 | 0.1200 |
| Reporting | 0.80 | 0.10 | 0.0800 |
| Risk of bias | 0.84 | 0.10 | 0.0840 |
| Population | 0.80 | 0.10 | 0.0800 |
| **Weighted average** | | **1.00** | **0.8300** |

`0.830` → `QUALITY = 0.83`. **Arithmetic confirmed exactly.** No flat modifiers
apply (the distal result is a pre-planned regional comparison, not a post-hoc
subgroup — correct; the paper's design is explicitly built to compare the two
sites).

**Defensibility of the per-dimension scores:**

- *Study design 0.88* — deliberate deviation from the rubric's literal 0.5
  "side-to-side study" row, mirroring `maeo_2023` (0.90). The contralateral
  model with randomized + counterbalanced arm assignment is an established,
  powerful within-subject design; the rubric's "When to deviate" clause covers
  exactly this. Defensible. Slightly *below* maeo's 0.88-vs-0.90 — reasonable,
  since maeo has the same design and both are scored as deviations; the 0.02
  gap is within rubric noise.
- *Sample size 0.80* — 19 completers, rubric's 15–24 band = 0.80. Correct. (The
  contralateral design means each completer contributes both conditions, which
  is *better* than 19 per independent arm; 0.80 is if anything conservative.)
- *Measurement 0.85* — CSA via ultrasound, rubric's explicit 0.85 tier. Exact.
- *Rigor 0.80* — competent standard methods, no pre-registration. The rubric's
  "no pre-reg but otherwise rigorous" tier is 0.80. Confirmed no trial
  registration is mentioned in the paper. Defensible.
- *Reporting 0.80* — effect sizes, p-values, ICCs and cm² CIs all reported, but
  no CI on d and no per-arm pre/post descriptives. The rubric's 0.7 tier is
  "CIs sometimes missing"; 0.8 is "effect sizes with CIs but no raw data". 0.80
  is a touch generous given a CI on the headline effect size (d) is absent and
  SE had to be reconstructed — but the rubric's "reconstruct SE from a p-value"
  cap (≤0.6) does **not** strictly apply here, because SE was reconstructed from
  (d, n), not from a p-value. 0.80 is at the upper edge of defensible; 0.75
  would also be defensible. Minor, not a discrepancy.
- *Risk of bias 0.84* — academic Brazilian funding, one disclosed Tonal
  advisory-board tie (BJS), not specific to a ROM finding. Rubric's 0.8–0.9
  band ("standard academic context, minor conflicts"). 0.84 sits sensibly in
  that band. Defensible.
- *Population 0.80* — single sex, training status explicitly defined, but the
  reported age SD is implausible (see below). Rubric 1.0 wants a tight,
  well-described population; 0.80 reflects the single-sex narrowness plus the
  age-reporting problem. Defensible.

The 0.83 score is internally consistent and consistent with how `maeo_2023`
(0.89) and `varovic_2025` (0.83) were scored.

### Population / age typo call

The paper reports **"mean age = 22.8 ± 10.5 years"** (confirmed verbatim from
PMC). The module flags the SD of 10.5 as implausible for "young untrained
women" and substitutes an `age_range=(18, 30)` envelope.

**Assessment: the typo call is reasonable and the handling is sound.** A SD of
10.5 on a mean of 22.8 implies a population spanning roughly 12 to 33 years
under a Normal assumption — i.e. a meaningful fraction of early-teenage
participants, which contradicts "untrained women" recruited via a university
and is implausible for an 8-week supervised resistance-training study. The
body-mass SD (±8.05) and height SD (±4.7) are normal; only the age SD is
anomalous, which is the signature of a single-field transcription error
(e.g. an intended ±1.05, or ±0.5). The module does not silently "fix" the
number — it documents the anomaly in both the `QUALITY` comment and the
`POPULATION` comment and uses a defensible (18, 30) young-adult envelope. That
is the right way to handle a suspected source typo: visible, reasoned, and
conservative. The (18, 30) range matches the envelope used for `varovic_2025`,
keeping the registry consistent.

---

## Encoding-shape & Varovic-relationship

### Encoding shape — EffectEstimate, not ExerciseEmphasis

**Correct.** The BACKLOG queued this as an `ExerciseEmphasis` source ("biceps,
analogous to Kassiano"). The module overrides that and encodes three
`EffectEstimate` objects instead, arguing the paper reports between-condition
Cohen's d, not per-arm percentage growth.

This is right, and it is the substantive difference from `maeo_2023`. Maeo
reports **absolute per-arm percentage growth** for each condition (long head
+28.5% overhead vs +19.6% neutral), which gives a numerator and denominator
from which an emphasis ratio in [0,1] can be built. Pedrosa 2023 does **not**
publish per-arm pre/post CSA growth percentages for the two ROM conditions — it
publishes the *contrast* (Cohen's d and the cm² mean difference) and the
strength gains. With no per-condition growth numerator there is no honest way
to derive an emphasis coefficient; an `ExerciseEmphasis` encoding would require
inventing the per-arm values. `EffectEstimate` on the SMD scale is the only
faithful shape, and it is the same shape as `maeo_2023`'s whole-muscle effects
and `varovic_2025`'s regional SMDs — so the three modules are mutually
poolable in principle. Good decision, well-justified in the docstring.

(Worth noting the docstring's claim that maeo's emphasis coefficients come from
"growth ratios" is correct, but `maeo_2023` itself now carries an audit caveat
that those ratios are *provisional* and not stable exercise constants. That
does not affect Pedrosa — it only reinforces that Pedrosa was right *not* to go
down the emphasis-ratio path.)

### Varovic relationship — filed together, kept out of the pool

The module files the three Pedrosa estimates under the same topic as
Varovic 2025 (`muscle_length → regional_hypertrophy`) but keeps them **out** of
that topic's inverse-variance pool, with two stated reasons.

**Reason (a): double-counting risk — Pedrosa 2023 may be one of Varovic's 12
included studies.** This is **confirmed true**. Multiple independent
descriptions of the Varovic meta-analysis explicitly list Pedrosa et al. 2023
among its included studies — it is one of the four upper-body (elbow-flexor)
studies in the pool, and the meta-analysis cites it repeatedly as a key
ROM/regional study. So pooling Pedrosa's estimates with Varovic's pooled SMDs
would literally double-count Pedrosa's data inside the inverse-variance
combination. Keeping Pedrosa out of the pool is **correct and necessary**, not
merely cautious. (Caveat: I confirmed this from secondary descriptions of the
meta-analysis, not from Varovic's primary included-study table, which is
paywalled. The conclusion is firm but the citation chain is one step indirect.)

**Reason (b): region definitions don't match 1:1.** Also correct. Pedrosa
measures at 50% and 70% of acromion-to-epicondyle distance and reports a summed
CSA; Varovic's regional bins are proximal-25% / mid-50% / distal-75%. Pedrosa's
"70%" is not Varovic's "distal-75%" and there is no proximal-25% Pedrosa site
at all. Even setting aside double-counting, the sites are not co-registered, so
pooling would be combining non-equivalent quantities.

The `_POOLABLE_OVERRIDE → Varovic only` mechanism (referenced in the docstring;
the override list itself lives in the registry, outside this module and not
audited here) is the right structural choice.

**Is the d = 0.89 distal effect genuinely in tension with Varovic's trivial
pooled SMDs, and is the module honest about it?** Yes on both counts, and this
is the strongest part of the module. Varovic's pooled regional SMDs are
0.05 / 0.07 / 0.09 — trivial, intervals mostly crossing zero. Pedrosa's single
distal effect is d = 0.89 — *large*, p = 0.001. That is a genuine, roughly
ten-fold tension between one primary study and the meta-analytic consensus.
The module does not paper over it: the docstring explicitly calls it "the
honest tension… direct experimental evidence of a length-driven distal bias…
against a meta-analytic consensus that the regional effect is trivial", and the
`GUIDANCE_FOR_OPTIMIZER` string instructs the optimizer to bias toward the
stretched ROM but **not** to generalize a strong "distal biceps" regional claim
— "treat it as muscle-specific, single-study evidence pending replication."
This is exactly the right epistemic posture: encode both, let the meta-analysis
hold the pooled weight, keep the primary study visible as a companion. The
two reasons even partly *explain* the tension — Pedrosa's large within-muscle
distal effect is one data point that Varovic's pooling, across many muscles
and a more conservative regional binning, averages down toward zero.

One small observation: the tension is also partly a measurement-granularity
artifact. Pedrosa's *summed* (whole-ish) effect is only d = 0.39 (n.s.), much
closer to Varovic's whole-muscle-ish picture; the d = 0.89 is specifically the
distal *site*. The module's notes do capture this ("The effect is REGIONAL,
not whole-muscle"), so it is honest — just worth keeping in mind that the
"0.89 vs 0.05–0.09" framing compares a single-site estimate to pooled
multi-muscle regional estimates, which are not perfectly like-for-like.

---

## Concerns & discrepancies

1. **Mid-site p-value: the paper contradicts itself.** Abstract: `p = 0.311`.
   Results sentence: `p = 0.331`. The module encodes `0.331` (matches Results)
   but presents it as if unambiguous. *Severity: minor.* The p-value is not
   used in any computation (only `mean` and `se` feed `EffectEstimate`), so no
   downstream number is wrong — but a future re-auditor reading the abstract
   will see a mismatch. The module should note the paper's internal
   inconsistency.

2. **"Humerus length" is a paraphrase.** The module's docstring and three
   estimate `notes` say CSA was measured at "50% / 70% of humerus length". The
   paper measures at "50% and 70% of the distance from the acromion to the
   lateral epicondyle" and the Results call it "% of biceps brachii length".
   *Severity: minor.* The acromion is a scapular landmark, so the reference
   segment is an arm-length proxy, not the humerus bone. Cosmetic, but it is a
   factual paraphrase error and is easy to fix.

3. **Reporting score 0.80 is at the generous edge.** The headline effect size
   (d) has no published CI and its SE had to be reconstructed. The rubric's
   hard cap ("reconstruct SE from a p-value → ≤0.6") does not strictly bite
   because SE here was reconstructed from (d, n), not from p — but a stricter
   reading would land Reporting at ~0.75. *Severity: trivial.* At 0.75 the
   weighted average would be 0.825 → still rounds to 0.83 or 0.82; the QUALITY
   value is robust to this either way.

4. **`varol`/Varovic inclusion confirmed only indirectly.** Pedrosa 2023's
   membership in Varovic's 12-study pool is confirmed from secondary
   descriptions, not from Varovic's primary included-study table (paywalled).
   The double-counting concern is real regardless — but the audit trail is one
   step indirect. *Severity: trivial* — the not-poolable decision is correct
   even if Pedrosa were *not* in the pool, because of reason (b).

5. **No issues** with: the three d values, all p-values except the mid-site
   abstract/results split, the design, sample, ROM definitions, the
   long-length direction, ICCs, funding, COI, the SE formula, the quality
   arithmetic, the encoding shape, or the Varovic not-poolable decision.

---

## Recommendations

1. **(Should fix)** In `BICEPS_MID_INITIAL_VS_FINAL.notes` and the docstring,
   add a note that the paper reports the 50%-site p-value inconsistently —
   `p = 0.331` in the Results text, `p = 0.311` in the Abstract — and that the
   module follows the Results text. Both values are non-significant, so the
   substantive conclusion is unaffected, but the inconsistency should be
   visible to the next reader.

2. **(Should fix)** Replace "humerus length" with the paper's actual reference
   landmark — "% of the acromion-to-lateral-epicondyle distance" (or "% of
   biceps brachii length", matching the Results) — in the docstring and in the
   three `notes` strings. Cosmetic but factual.

3. **(Optional)** Consider dropping Reporting from 0.80 to 0.75 for strict
   rubric consistency (the headline d has no published CI). This changes the
   weighted average to 0.825, which still rounds to 0.83 — so it is a
   documentation tidy-up, not a value change. Leave QUALITY = 0.83.

4. **(Optional)** When the registry's `_POOLABLE_OVERRIDE` is next reviewed,
   record the *confirmed* fact that Pedrosa 2023 is an included study of
   Varovic 2025 (not just "plausibly") — the double-counting reason is now
   verified, not hypothetical, and the comment in this module ("plausibly one
   of the 12 studies") can be upgraded to a definite statement.

5. **(No action)** The encoding-shape decision, the SE methodology, the
   age-typo handling, the not-poolable decision, and the honest-tension framing
   are all sound and should be kept as-is. This module is a good template for
   how to encode a single primary study that sits in tension with a
   meta-analysis already in the registry.

---

## Encoder reconciliation (2026-05-17, post-audit)

The actionable items above were applied:

1. The `BICEPS_MID` estimate's `notes` now flags the paper's internal p-value
   inconsistency (Results 0.331 vs Abstract 0.311; non-significant either way).
   No encoded value changed — p is not used in computation.
2. "humerus length" was replaced with "the acromion-to-lateral-epicondyle
   distance" throughout the module docstring and the `notes` strings.
4. The module docstring and the registry `_POOLABLE_OVERRIDE` comment were
   upgraded from "plausibly one of Varovic's 12 studies" to **CONFIRMED** —
   this audit verified Pedrosa 2023 is an included study of Varovic 2025, so
   the double-counting rationale for keeping it out of the pool is now a
   verified fact, not a hypothesis.
3. Reporting left at 0.80; QUALITY stays 0.83 (0.75 for Reporting would still
   round to 0.83 — not worth a value change).

No encoded value changed. **Verdict after reconciliation: ACCURATE** — the
MINOR discrepancies were documentation gaps, now closed.
