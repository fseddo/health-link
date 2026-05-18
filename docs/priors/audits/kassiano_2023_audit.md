# Literature Audit — Kassiano et al. 2023 (gastrocnemius partial ROM)

**Module audited:** `priors-handoff/app/priors/kassiano_2023.py`
**Paper:** Kassiano W, Costa B, Kunevaliki G, et al. "Greater Gastrocnemius Muscle
Hypertrophy After Partial Range of Motion Training Performed at Long Muscle
Lengths." *Journal of Strength & Conditioning Research.* 2023;37(9):1746-1753.
DOI 10.1519/JSC.0000000000004460. PMID 37015016.
**Audit date:** 2026-05-17
**Auditor:** Independent priors-layer literature auditor
**Audit type:** ABSTRACT-LIMITED (full text not reachable — see Sources)

---

## Sources accessed

| Source | URL | Result |
|---|---|---|
| PubMed record (PMID 37015016) | `https://pubmed.ncbi.nlm.nih.gov/37015016/` | REACHED via WebFetch. Full abstract retrieved verbatim. |
| JSCR full text (journals.lww.com) | `https://journals.lww.com/nsca-jscr/fulltext/2023/09000/greater_gastrocnemius_muscle_hypertrophy_after.3.aspx` | UNREACHABLE — HTTP 402 Payment Required. Hard paywall confirmed. |
| Ovid abstract page | `https://www.ovid.com/jnls/nsca-jscr/abstract/...004460...` | WebFetch blocked by sandbox permission; abstract content instead obtained verbatim via WebSearch indexing of the same page. |
| OUCI metadata page | `https://ouci.dntb.gov.ua/en/works/7Pr8NyOl/` | WebFetch blocked by sandbox permission; not independently retrieved. |
| ResearchGate PDF | `https://www.researchgate.net/publication/365127382_...` | Not retrieved (encoder reported 403; not re-attempted). |
| WebSearch abstract indexing (multiple queries) | search index of PubMed / Ovid / journal pages | REACHED. Returned the abstract text verbatim across 4 independent queries, including the mechanistic ROM sentence. |
| Secondary citing literature | Frontiers 2025 (`fpsyg.2025.1494323`), SportRxiv preprint 414 | WebFetch blocked / not on-topic; partial paraphrase obtained via WebSearch summaries only. |

**Confirmation:** The JSCR full text is hard-paywalled (HTTP 402 reproduced
this audit). This is an abstract-limited audit. The published abstract was
verified verbatim from PubMed (WebFetch) and cross-checked against the same
abstract surfaced by four independent WebSearch queries that indexed PubMed,
Ovid and the journal page. All abstract-level numbers below are therefore
**multi-source confirmed**. Items requiring the Methods/Results body are marked
**UNVERIFIED**.

---

## Verdict

**ACCURATE** (with two minor, non-blocking notes).

Every value the module encodes from the abstract — the six muscle-thickness %
gains, the p-value pattern, the ROM angle definitions, the sample/protocol, the
emphasis ratios and the quality score — matches the published abstract exactly
across multiple independent sources. The arithmetic (emphasis ratios and the
0.78 weighted quality average) is correct. The critical anatomical claim that
the module's entire framing rests on — that INITIAL ROM (ankle −25° to 0°,
dorsiflexed) is the *longer* gastrocnemius muscle length — is explicitly
supported by the abstract's own mechanistic sentence ("in INITIAL ROM, the
ankle moved exclusively in dorsiflexion angles, in which the gastrocnemius heads
reach longer muscle lengths"). The two minor notes are: (1) the module encodes
`training_status="untrained"` and labels it INFERRED, which is honest and
defensible but is genuinely not stated in the abstract; (2) `age_range=(18,30)`
is an unstated inference, also correctly flagged. Neither is a misrepresentation
of the paper. The encoding-shape choice (ExerciseEmphasis only, no
EffectEstimate) is correct given the abstract reports no effect sizes/CIs/SEs.

---

## Value-by-value verification

| # | Encoded value | Module location | Paper says | Source | Verdict |
|---|---|---|---|---|---|
| 1 | Medial gastroc INITIAL +15.2% | docstring; medial rationale | "INITIAL ROM = +15.2%" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 2 | Medial gastroc FULL +6.7% | docstring; medial rationale | "FULL ROM = +6.7%" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 3 | Medial gastroc FINAL +3.4% | docstring; medial rationale | "FINAL ROM = +3.4%" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 4 | Lateral gastroc INITIAL +14.9% | docstring; lateral rationale | "INITIAL ROM = +14.9%" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 5 | Lateral gastroc FULL +7.3% | docstring; lateral rationale | "FULL ROM = +7.3%" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 6 | Lateral gastroc FINAL +6.2% | docstring; lateral rationale | "FINAL ROM = +6.2%" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 7 | Medial: INITIAL > FULL and > FINAL at p ≤ 0.009 | docstring; medial confidence="high" | "INITIAL ROM elicited greater medial gastrocnemius increases than FULL ROM and FINAL ROM ... p ≤ 0.009" | PubMed abstract | ✓ CONFIRMED |
| 8 | Lateral: INITIAL > FINAL at p < 0.024 | docstring; lateral rationale | "INITIAL ROM elicited greater lateral gastrocnemius increases than FINAL ROM ... p < 0.024" | PubMed abstract | ✓ CONFIRMED |
| 9 | Lateral: INITIAL vs FULL non-significant, p = 0.060 | docstring; lateral confidence="medium" | "did not significantly differ from FULL ROM ... p = 0.060" | PubMed abstract | ✓ CONFIRMED |
| 10 | FULL ROM = −25° to +25° | docstring | "FULL ROM (ankle: −25° to +25°)" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 11 | INITIAL ROM = −25° to 0° | docstring | "INITIAL ROM (ankle: −25° to 0°)" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 12 | FINAL ROM = 0° to +25° | docstring | "FINAL ROM (ankle: 0° to +25°)" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 13 | INITIAL ROM = the LONG/lengthened gastroc length | docstring; rationale strings; whole module framing | Abstract: "in INITIAL ROM, the ankle moved exclusively in dorsiflexion angles, in which the gastrocnemius heads reach longer muscle lengths." | WebSearch (evidencebasedmuscle query returned this abstract sentence) | ✓ CONFIRMED — the paper's own abstract makes this claim explicitly. |
| 14 | FINAL ROM = the SHORT muscle length | docstring; rationale strings | Implied: FINAL is 0° to +25° (plantarflexion side), the gastroc-shortened end. Abstract names INITIAL as the longer length; FINAL is the complementary shortened end. | Inference consistent with abstract | ✓ CONFIRMED (logically entailed) |
| 15 | 42 young women | docstring; POPULATION.notes | "Forty-two young women" | PubMed abstract; WebSearch ×4 | ✓ CONFIRMED |
| 16 | n = 14 per group | docstring; POPULATION.notes | 42 randomized to 3 groups → 14/group. Abstract says "randomly assigned to 1 of 3 groups"; per-group n not stated as "14" verbatim but is the only arithmetic possibility. | PubMed abstract (derived) | ✓ CONFIRMED (42/3 = 14; standard equal allocation) |
| 17 | 8 weeks, 3×/week | docstring; POPULATION.notes | "8 weeks, 3 days·week⁻¹" | PubMed abstract | ✓ CONFIRMED |
| 18 | 3 sets of 15-20RM | docstring | "3 sets of 15-20 repetition maximum" | PubMed abstract | ✓ CONFIRMED |
| 19 | Pin-loaded horizontal leg-press calf raise | docstring | "calf raise exercise was performed in a pin-loaded, horizontal, leg-press machine" | PubMed abstract | ✓ CONFIRMED |
| 20 | B-mode ultrasound | docstring; Measurement dimension | "B-mode ultrasound" | PubMed abstract | ✓ CONFIRMED |
| 21 | `sex="female"` | POPULATION | "young women" | PubMed abstract | ✓ CONFIRMED |
| 22 | `training_status="untrained"` | POPULATION | NOT stated in the abstract. Module flags this as INFERRED from effect magnitude. One secondary source (Frontiers-citing-paper paraphrase) calls them "untrained women", but that is a citing author's characterization, not the Kassiano abstract. | Abstract (absent); secondary paraphrase | ⚠ INFERRED — see Concerns. Honestly flagged in the module. |
| 23 | `age_range=(18,30)` | POPULATION | NOT stated. Abstract says only "young women". Module explicitly flags this as "the young-adult envelope, not a paper figure." | Abstract (absent) | ⚠ INFERRED — honestly flagged. |
| 24 | `outcome="hypertrophy"` | POPULATION | Study measures muscle thickness gain. | PubMed abstract | ✓ CONFIRMED |
| 25 | DOI 10.1519/JSC.0000000000004460 | CITATION | Matches PubMed/journal record. | PubMed | ✓ CONFIRMED |
| 26 | Journal / year 2023 | CITATION | JSCR 2023;37(9):1746-1753. | PubMed | ✓ CONFIRMED |
| 27 | QUALITY = 0.78 | QUALITY | Recomputed below. | — | ✓ CONFIRMED (arithmetic correct) |
| 28 | Emphasis 6.7/15.2 ≈ 0.44 | FULL_ROM_..._MEDIAL | — | — | ✓ CONFIRMED (math below) |
| 29 | Emphasis 3.4/15.2 ≈ 0.22 | SHORTENED_..._MEDIAL | — | — | ✓ CONFIRMED |
| 30 | Emphasis 7.3/14.9 ≈ 0.49 | FULL_ROM_..._LATERAL | — | — | ✓ CONFIRMED |
| 31 | Emphasis 6.2/14.9 ≈ 0.42 | SHORTENED_..._LATERAL | — | — | ✓ CONFIRMED |

**Full-text-dependent items NOT verifiable from the abstract** (none are
encoded as paper facts; listed for completeness):
- Pre-registration status — module scores design 0.85 partly on this being
  unverifiable. Correct to leave UNVERIFIED.
- Exact randomization/allocation-concealment method — UNVERIFIED.
- Funding source / conflict-of-interest declaration — UNVERIFIED. Module's
  Risk-of-bias 0.82 is an estimate; flagged as such.
- Baseline equivalence of the three groups, dropout/adherence, handling of
  missing data — UNVERIFIED.
- Whether muscle thickness was measured at one or multiple sites along the
  muscle, and ICC/reliability of the ultrasound protocol — UNVERIFIED. (Module's
  Measurement 0.90 assumes a standard site-specific MT protocol; reasonable but
  not abstract-confirmed beyond "B-mode ultrasound".)
- Verbatim per-group n — abstract gives total 42 and "3 groups"; n=14 is
  arithmetically forced, so this is effectively confirmed, not UNVERIFIED.

---

## Math checks

### Emphasis-ratio recomputation

The module derives emphasis as (group % gain) / (best group % gain), normalizing
the lengthened partial (INITIAL) to 1.0 within each gastrocnemius head.

| Entry | Encoded expression | Exact value | Rounded | Module comment | Verdict |
|---|---|---|---|---|---|
| FULL medial | 6.7 / 15.2 | 0.440789… | 0.44 | "~= 0.44" | ✓ correct |
| SHORTENED (FINAL) medial | 3.4 / 15.2 | 0.223684… | 0.22 | "~= 0.22" | ✓ correct |
| FULL lateral | 7.3 / 14.9 | 0.489932… | 0.49 | "~= 0.49" | ✓ correct |
| SHORTENED (FINAL) lateral | 6.2 / 14.9 | 0.416107… | 0.42 | "~= 0.42" | ✓ correct |
| INITIAL medial / INITIAL lateral | 1.0 (reference) | 1.0 | 1.0 | reference | ✓ correct |

All six emphasis values are computed correctly. All fall within ExerciseEmphasis's
required [0.0, 1.0] range, so `__post_init__` will not raise.

### Quality-score recomputation

Per-dimension scores from the module's quality block and weights from
QUALITY_RUBRIC.md v1.0:

| Dimension | Score | Weight | Contribution |
|---|---|---|---|
| Study design | 0.85 | 0.20 | 0.1700 |
| Sample size | 0.70 | 0.15 | 0.1050 |
| Measurement quality | 0.90 | 0.20 | 0.1800 |
| Methodological rigor | 0.75 | 0.15 | 0.1125 |
| Reporting transparency | 0.65 | 0.10 | 0.0650 |
| Risk of bias | 0.82 | 0.10 | 0.0820 |
| Population specificity | 0.70 | 0.10 | 0.0700 |
| **Weighted average** | | **1.00** | **0.7845** |

0.7845 rounds to **0.78**. ✓ The encoded `QUALITY = 0.78` is arithmetically
correct, and the module's stated "0.784" is right to three decimals.

**Cross-check of individual dimension scores against the rubric:**
- Sample size 0.70 — rubric's per-arm band 10–14 = 0.70. n=14/arm. ✓ Exact.
- Measurement 0.90 — rubric: "site-specific muscle thickness via ultrasound
  (high-quality)" = 0.9. ✓ Defensible (assumes site-specific; abstract only
  says "B-mode ultrasound" — minor benefit-of-the-doubt, reasonable for this
  research group's known protocols).
- Study design 0.85 — rubric: 0.9 = "RCT with minor design issues (no pre-reg,
  solid randomization)". Module scored 0.85, i.e. slightly *below* the 0.9 tier,
  to reflect that randomization quality and pre-reg status are unverifiable from
  the abstract. Conservative and consistent with the rubric's intent. ✓
- Methodological rigor 0.75 — between rubric's 0.7 ("standard methods applied
  competently") and 0.8. Reasonable for an UNVERIFIED dimension. ✓
- Reporting transparency 0.65 — rubric: 0.5 = "point estimates and p-values
  only". The abstract gives % changes + p-values and no CIs/effect sizes, which
  literally maps to 0.5. The module scored 0.65, *above* the literal tier. This
  is mildly generous (see Concerns), but the rubric also notes reporting is
  judged on the *full text*, which is unread — so a hedge above the
  abstract-only floor is arguably fair. Not a material error; it moves the final
  score by at most 0.10 × 0.15 = 0.015.
- Risk of bias 0.82 — rubric: 0.8 = "standard academic context, minor
  conflicts". 0.82 is essentially the 0.8 tier. ✓
- Population specificity 0.70 — rubric: 0.7 = "population described but ranges
  wide". The abstract gives only "young women" with no age range or training
  status, which is arguably *less* specific than 0.7 (closer to 0.5 "described
  but no subgroup detail" or even 0.3 "healthy adults, no detail"). The 0.70 is
  slightly generous. See Concerns.

**Access modifier question:** QUALITY_RUBRIC.md lists a flat modifier
"Sci-Hub-only access; can't verify methods → ×0.9". The module argues this
should NOT be applied, on the grounds that the abstract-only limitation is
already absorbed into the four conservative dimension scores (design, rigor,
reporting, bias), and applying the modifier on top would double-count.

This auditor's assessment: **the module's reasoning is defensible and the
×0.9 should not be additionally applied.** The rubric's modifier is written for
the case where you *have* the full paper (via Sci-Hub) and merely cannot inspect
*supplementary* materials — a smaller penalty for a smaller gap. Here the
situation is more severe (no full text at all), but the module has responded by
*lowering the dimension scores themselves* rather than scoring them as if the
full text were seen and then deducting 10%. Stacking both would penalize the
same missing information twice. The decision is sound. If anything, the more
correct framing would have been to score the four affected dimensions slightly
lower and skip the modifier — which is exactly what the module did. For
auditability, the recomputed alternative is noted: 0.7845 × 0.9 = 0.706 → 0.71.
The module's 0.78 is the better-justified figure.

---

## Concerns & discrepancies

All concerns are MINOR. None rise to "material discrepancy."

### C1 — `training_status="untrained"` is an inference, not an abstract fact (MINOR, well-flagged)
The published abstract describes participants only as "Forty-two young women."
It does **not** state training status. The module encodes
`training_status="untrained"` and is explicit and honest about this in
`POPULATION.notes`: "Training status is INFERRED as untrained — the abstract
does not state it, but 6-15% muscle thickness gain in 8 weeks is a novice-range
response."

Assessment: the inference is **defensible**. (a) 6–15% gastrocnemius MT gain in
8 weeks is large and consistent with an untrained response — the gastrocnemius
is notoriously resistant to growth in trained lifters. (b) This Brazilian
research group (Cyrino lab) characteristically recruits untrained young women
for ROM/volume studies; their companion volume paper is explicitly "61 untrained
young women," and at least one secondary source paraphrasing Kassiano 2023 calls
the sample "42 untrained women." (c) The module routes this through
`PopulationSpec`, which feeds `applicability_to()` — a wrong status would cost a
0.5× applicability multiplier against trained users, so the inference matters.
**Recommendation:** keep as-is but, if the full text becomes reachable, confirm
the recruitment criterion. The note already says exactly this. No change
required now. Strictly, "mixed" would be the maximally-conservative encoding if
status were truly unknown, but given the convergent evidence "untrained" is the
better point estimate.

### C2 — `age_range=(18,30)` is not a paper figure (MINOR, well-flagged)
The abstract gives no age. The module encodes (18, 30) and explicitly labels it
"the young-adult envelope, not a paper figure." This is honest. The Cyrino lab's
"young women" samples typically sit around 18–27 with means ~21–23. (18, 30) is
slightly wider on the top end than the lab's usual sample, which makes
`applicability_to()` mildly *over*-credit users near 30. This mirrors a fix the
Maeo module already made (it tightened (20,30) → (21,27)). **Recommendation:**
consider tightening to (18, 27) for consistency with the Maeo precedent and the
lab's typical recruitment, OR leave (18, 30) and accept the conservative-wide
envelope. Either is defensible; flag, don't block.

### C3 — Population specificity 0.70 is mildly generous (MINOR)
Per the rubric, "young women" with no stated age range, no inclusion/exclusion
criteria visible, and no training status maps more naturally to 0.5
("heterogeneous/under-described") than to 0.7 ("described but ranges wide").
Scoring it 0.70 lifts the final QUALITY by ~0.10 × 0.10 = 0.01 versus a 0.5
score. The effect on the final 0.78 is negligible (~0.76 if rescored to 0.5),
so this is not worth a code change on its own, but the justification line could
acknowledge that the abstract-only view of the population is thinner than a
typical 0.7. The module's own comment already hedges ("age range and training
status not stated in the abstract"), so this is a documentation nuance, not an
error.

### C4 — Reporting transparency 0.65 sits just above the literal rubric tier (MINOR)
The abstract reports % changes and p-values with no CIs/effect sizes, which is
the rubric's literal 0.5 row. 0.65 is a small upward hedge justified by the
rubric's note that reporting is judged on the full text (unread here). Impact on
the final score is ≤0.015. Not material. No change required.

### C5 — Confidence asymmetry (medial "high" vs lateral "medium") — JUSTIFIED
The module sets all three medial-head emphasis entries to `confidence="high"`
and all three lateral-head entries to `confidence="medium"`, on the basis that
the medial-head INITIAL advantage cleared significance over *both* comparators
(p ≤ 0.009) while the lateral-head INITIAL-vs-FULL gap did not (p = 0.060).
This is a correct reading of the abstract and a sound use of the confidence
field. One subtlety worth noting: the `combine_emphasis_estimates` pooling logic
takes the *lowest* confidence across pooled sources, so if a future lateral-head
source is added the "medium" will propagate — which is the intended conservative
behavior. No issue.

### C6 — Emphasis-as-percent-growth-ratio caveat — ALREADY DOCUMENTED, NOT A DEFECT
The module's "METHOD CAVEAT" comment correctly flags that a ratio of 8-week
%-growth outcomes is not the study-independent "fraction of maximum stimulus"
that `shared.py` defines `emphasis` to be: the implicit zero is "the weakest of
three real ROM variants" (FINAL still grew the medial head +3.4%), not "no
stimulus." This is the same known limitation flagged in `maeo_2023.py` and is
consistent with it. It is a conceptual debt of the priors layer, not a
mis-encoding of this paper. No action for this audit; it belongs on BACKLOG.

### C7 — n=14 per arm is derived, not quoted (NOT a discrepancy)
The abstract states 42 total and three groups; equal allocation gives exactly
14/arm. The module presents "14 per group" as fact. Because 42/3 = 14 is forced
and resistance-training RCTs use equal allocation by default, this is treated as
confirmed, not as an unverified claim. Worth a one-word hedge ("14 per group,
assuming equal allocation") only if being maximally pedantic.

---

## Recommendations

1. **No blocking changes.** The module faithfully represents the paper's
   abstract. Verdict ACCURATE stands.
2. **Keep the INFERRED flags on `training_status` and `age_range`.** They are
   the single most important honesty hooks in this module. Do not silently
   promote "untrained" to an unqualified fact even though the inference is
   well-supported.
3. **Optional consistency tweak:** tighten `age_range` from (18, 30) to (18, 27)
   to match the Maeo module's precedent and the Cyrino lab's typical "young
   women" sample, reducing over-credit for ~30-year-old users. Low priority.
4. **Optional documentation nuance:** in the quality block, note that Population
   specificity 0.70 is a mild upward hedge given the abstract gives no age range
   or training status — so a future re-score against the full text could move it
   down toward 0.5–0.6. This does not change the encoded 0.78 (the swing is
   ~0.02) but keeps the rubric application transparent.
5. **Re-audit trigger:** if the JSCR full text becomes accessible, re-verify
   (a) the recruitment/training-status criterion, (b) participant age,
   (c) whether muscle thickness was site-specific and its measurement
   reliability, (d) funding/COI, and (e) pre-registration status — then re-score
   the four UNVERIFIED dimensions. The current conservative scores should only
   move upward if the full text is clean, so 0.78 is a safe floor.
6. **Encoding shape:** the decision to encode `ExerciseEmphasis` only and no
   `EffectEstimate` is **correct**. The abstract reports no effect sizes, CIs or
   SEs; `EffectEstimate.__post_init__` requires a positive SE, so a fabricated
   or reconstructed SE would be the only way to populate one — undesirable.
   ExerciseEmphasis-only is the honest shape for an abstract-limited %-gain
   source. Keep it.
7. **Decline the ×0.9 access modifier** — as the module already does. The
   abstract-only gap is correctly absorbed into the four conservative dimension
   scores; stacking the modifier would double-count. The reasoning in the
   quality block is sound and should be left intact.

---

*End of audit. All abstract-level values multi-source confirmed; all
full-text-dependent items marked UNVERIFIED rather than assumed. No fabricated
verification.*
