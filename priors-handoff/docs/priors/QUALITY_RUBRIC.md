# Quality Rubric for Literature Priors

This document defines how `quality_score` (0.0–1.0) is assigned to every
`EffectEstimate` in the priors layer. Apply consistently so that pooling and
applicability scoring produce comparable results across papers.

## How to use this rubric

1. Read the paper.
2. Score each of the seven dimensions below from 0 to 1.
3. Compute the weighted average. The weights reflect how much each dimension
   should influence pooling weight in practice.
4. Apply any flat penalties from the modifier list.
5. Record the result in the prior module with a one-line justification per
   dimension in the module's docstring or comments.

Re-score if a paper is later corrected, retracted, or has its methods
materially clarified.

## The seven dimensions

| Dimension | Weight | What it captures |
|---|---|---|
| Study design | 0.20 | RCT vs observational, randomization quality, blinding where possible |
| Sample size | 0.15 | Statistical power; participants per arm, not total participants |
| Measurement quality | 0.20 | Direct site-specific MRI/DEXA vs. circumference tape vs. estimated 1RM |
| Methodological rigor | 0.15 | Preregistration, statistical approach, handling of missing data |
| Reporting transparency | 0.10 | Full effect sizes with uncertainty, raw data availability, clear protocols |
| Risk of bias | 0.10 | Funding sources, author conflicts, publication bias mitigation |
| Population specificity | 0.10 | How well-defined and well-described the studied population is |

Weights sum to 1.0. The weighted average becomes the base score.

## Scoring guide per dimension

### Study design (0.20 weight)

| Score | Description |
|---|---|
| 1.0 | Pre-registered RCT, randomized allocation, intention-to-treat analysis |
| 0.9 | RCT with minor design issues (no pre-reg, but solid randomization) |
| 0.8 | Systematic review/meta-analysis of RCTs with pre-registered protocol |
| 0.7 | Meta-analysis of mixed designs (RCT + non-randomized intervention) |
| 0.6 | Non-randomized controlled intervention |
| 0.5 | Within-subject design with confounds (e.g., side-to-side studies) |
| 0.4 | Cross-sectional with control group |
| 0.2 | Cross-sectional without controls, retrospective analyses |
| 0.0 | Anecdote, case study, expert opinion |

Note for meta-analyses: score based on the *worst* design tier of included
studies, not the meta-analysis methodology itself (that goes under
"Methodological rigor").

### Sample size (0.15 weight)

Score by participants per arm in the primary analysis, not by total N. A
study with 500 participants split into 10 arms of 50 is treated as n=50.

For meta-analyses, use total unique participants across the most relevant
sub-analysis.

| Score | Per-arm n (intervention) | Per-arm n (meta-analysis) |
|---|---|---|
| 1.0 | ≥40 | ≥800 across pooled studies |
| 0.9 | 25–39 | 500–799 |
| 0.8 | 15–24 | 300–499 |
| 0.7 | 10–14 | 150–299 |
| 0.5 | 6–9 | 75–149 |
| 0.3 | 3–5 | 30–74 |
| 0.1 | <3 | <30 |

Resistance training studies routinely run with n=8–15 per arm. That's normal
for the field but should still be reflected in the score.

### Measurement quality (0.20 weight)

Heavily depends on the outcome being measured.

**For hypertrophy:**

| Score | Measurement type |
|---|---|
| 1.0 | MRI muscle volume (gold standard) |
| 0.9 | Site-specific muscle thickness via ultrasound (high-quality) |
| 0.85 | Cross-sectional area via ultrasound or DEXA regional |
| 0.7 | DEXA lean mass (regional, not whole-body) |
| 0.5 | Whole-body DEXA lean mass |
| 0.4 | Circumference tape with controlled protocol |
| 0.3 | Circumference tape without controlled protocol |
| 0.2 | Bioelectrical impedance |
| 0.1 | Visual estimation, body weight |

**For strength:**

| Score | Measurement type |
|---|---|
| 1.0 | Direct 1RM in tested exercise, with familiarization protocol |
| 0.9 | Direct 1RM without explicit familiarization |
| 0.8 | Direct 3RM or 5RM with conversion to estimated 1RM |
| 0.7 | Isometric or isokinetic peak torque, well-controlled |
| 0.5 | Estimated 1RM from sub-maximal sets |
| 0.4 | Repetitions-to-failure at fixed load |
| 0.2 | Self-reported strength |

**For power:**

| Score | Measurement type |
|---|---|
| 1.0 | Force plate analysis (CMJ, SJ) |
| 0.9 | Validated jump mat or linear position transducer |
| 0.7 | Velocity-based methods at standard loads |
| 0.5 | Vertical jump tape measure |

### Methodological rigor (0.15 weight)

| Score | Description |
|---|---|
| 1.0 | Pre-registration with deviations documented, Bayesian or robust methods, sensitivity analyses, transparent handling of missing data |
| 0.9 | Pre-registration, standard methods, minimal missing data |
| 0.8 | No pre-reg but otherwise rigorous; multiple specifications tested |
| 0.7 | Standard methods applied competently |
| 0.5 | Some methodological concerns (e.g., post-hoc subgroup analyses presented as primary) |
| 0.3 | Clear statistical problems (selective reporting, no correction for multiple comparisons) |
| 0.1 | Methodologically broken |

### Reporting transparency (0.10 weight)

| Score | Description |
|---|---|
| 1.0 | Raw data + analysis code on OSF/GitHub; full forest plots; all CIs reported |
| 0.9 | Full effect sizes with CIs; protocols clear; data available on request |
| 0.8 | Effect sizes with CIs but no raw data |
| 0.7 | Effect sizes and p-values, CIs sometimes missing |
| 0.5 | Point estimates and p-values only — must reconstruct SE from p |
| 0.3 | Selective reporting; key results buried in supplementary |
| 0.1 | Numbers don't even reconcile internally |

If you have to reconstruct SE from a p-value, this dimension shouldn't score
above 0.6 regardless of other strengths.

### Risk of bias (0.10 weight)

| Score | Description |
|---|---|
| 1.0 | Independently funded, no author conflicts, publication-bias analysis included with clean results |
| 0.9 | Academic funding, modest conflicts disclosed |
| 0.8 | Standard academic context, minor conflicts (e.g., authors run paid workshops) |
| 0.6 | Authors have meaningful commercial interest (own products, supplement companies, paid programs) but methods appear sound |
| 0.4 | Industry-funded with conclusions favorable to sponsor |
| 0.2 | Clear conflicts and questionable interpretation |
| 0.0 | Sponsored, no disclosure, results too good to be true |

Note: fitness science has many honest researchers who also work commercially.
Don't score below 0.6 on this dimension just because authors are "in the
industry" — only when there's a direct conflict on the specific finding.

### Population specificity (0.10 weight)

| Score | Description |
|---|---|
| 1.0 | Tight, well-described population (age range, training status, sex split) with documented inclusion/exclusion criteria |
| 0.9 | Clearly described population with minor ambiguity |
| 0.7 | Population described but ranges are wide (e.g., "adults 18–65") |
| 0.5 | Heterogeneous population without subgroup analysis |
| 0.3 | "Healthy adults" with no further detail |
| 0.1 | Population unclear or inconsistently described |

Higher specificity = more confident application of `PopulationSpec.applicability_to()`.

## Flat modifiers

Apply these **after** computing the weighted average. They are penalties only,
not bonuses, and stack multiplicatively.

| Modifier | Multiplier | When to apply |
|---|---|---|
| Addresses a different question than the one we're using it for | × 0.7 | E.g., Vieira's non-volume-equated SMD when we want the volume-equated effect |
| Significant unresolved heterogeneity (I² > 75% in meta-analysis) | × 0.85 | When pooled studies are wildly inconsistent |
| Published in predatory or low-quality journal | × 0.7 | Check Beall's list, journal indexing in PubMed |
| Subgroup analysis presented as primary | × 0.85 | Post-hoc subgroups are exploratory, not confirmatory |
| Conflicts visibly with multiple other higher-quality sources | × 0.85 | Be conservative: don't downweight too aggressively here, since the outlier might be right |
| Authors have publicly retracted or corrected this paper's claims | × 0.5 | And add a note in the module |
| Sci-Hub-only access; can't verify methods | × 0.9 | Slight penalty for not being able to inspect supplementary materials |

## Worked examples

### Pelland et al. 2026

| Dimension | Score | Reasoning |
|---|---|---|
| Study design | 0.85 | Meta-analysis of RCTs, pre-registered on OSF |
| Sample size | 1.0 | 2058 total participants across 67 studies |
| Measurement quality | 0.95 | Restricted to direct site-specific MRI/MT/CSA |
| Methodological rigor | 1.0 | Bayesian meta-regression, multiple functional forms compared, sensitivity analyses |
| Reporting transparency | 1.0 | Full data + code on OSF |
| Risk of bias | 0.85 | Authors are coaches/writers in the industry but methods are exemplary |
| Population specificity | 0.9 | Clear inclusion criteria; well-described participant pool |

Weighted average:
```
0.85 × 0.20 + 1.0 × 0.15 + 0.95 × 0.20 + 1.0 × 0.15 + 1.0 × 0.10 + 0.85 × 0.10 + 0.9 × 0.10
= 0.17 + 0.15 + 0.19 + 0.15 + 0.10 + 0.085 + 0.09
= 0.935
```
Modifiers: none.
**Final score: 0.94** (rounded). The 0.95 currently in the code is within
acceptable variance for a rubric this granular.

### Vieira et al. 2021 — overall (non-volume-equated)

| Dimension | Score | Reasoning |
|---|---|---|
| Study design | 0.7 | Meta-analysis of mixed RCT + non-randomized |
| Sample size | 0.8 | 13 studies, ~240 participants |
| Measurement quality | 0.75 | Mixed MT/CSA/circumference across studies |
| Methodological rigor | 0.7 | Random-effects, but no pre-reg; volume-equated subgroup not the primary analysis |
| Reporting transparency | 0.5 | Abstract lacks CIs; had to recover SE from p-value |
| Risk of bias | 0.85 | Standard academic context |
| Population specificity | 0.85 | Trained adults, mostly young, reasonably described |

Weighted average:
```
0.7 × 0.20 + 0.8 × 0.15 + 0.75 × 0.20 + 0.7 × 0.15 + 0.5 × 0.10 + 0.85 × 0.10 + 0.85 × 0.10
= 0.14 + 0.12 + 0.15 + 0.105 + 0.05 + 0.085 + 0.085
= 0.735
```
Modifiers: addresses a different question (×0.7).
**Final score: 0.735 × 0.7 = 0.51**.

The earlier code has 0.525 (= 0.75 × 0.7), which is close but rests on a base
score that this rubric would not produce. Update the module to 0.51.

### Vieira et al. 2021 — strength outcome (also non-volume-equated)

Same dimensions except no different-question modifier:
**Final score: 0.74**, not the 0.75 currently in the code. Close enough that
either is defensible, but if applied consistently the rubric produces 0.74.

### Grgic et al. 2021

| Dimension | Score | Reasoning |
|---|---|---|
| Study design | 0.75 | Meta-analysis of RCTs, no pre-reg mentioned |
| Sample size | 0.8 | 15 studies, ~312 participants |
| Measurement quality | 0.8 | Site-specific measures predominantly |
| Methodological rigor | 0.85 | Volume-equated vs not separated cleanly; trained subgroup analysis |
| Reporting transparency | 0.85 | CIs reported in main results |
| Risk of bias | 0.85 | Standard academic context |
| Population specificity | 0.85 | Young adults, training status reported |

Weighted average:
```
0.75 × 0.20 + 0.8 × 0.15 + 0.8 × 0.20 + 0.85 × 0.15 + 0.85 × 0.10 + 0.85 × 0.10 + 0.85 × 0.10
= 0.15 + 0.12 + 0.16 + 0.1275 + 0.085 + 0.085 + 0.085
= 0.81
```
Modifiers: none for the overall analysis. For the trained-subgroup estimate
specifically, apply ×0.85 for subgroup-as-primary.
**Final scores: 0.81 (overall), 0.69 (trained subgroup)**.

The code currently has 0.85 / 0.765. Update to rubric-derived values.

### Robinson et al. 2022

| Dimension | Score | Reasoning |
|---|---|---|
| Study design | 0.85 | Meta-analysis of RCTs in Sports Medicine, well-cited methods |
| Sample size | 0.8 | 15 studies, ~300 participants total |
| Measurement quality | 0.9 | Hypertrophy-specific, mostly site-specific |
| Methodological rigor | 0.9 | Separates momentary failure from set failure; velocity-loss analysis included |
| Reporting transparency | 0.9 | Full CIs, multiple sub-analyses with point estimates |
| Risk of bias | 0.85 | Standard academic context |
| Population specificity | 0.85 | Healthy adults with RT experience |

Weighted average:
```
0.85 × 0.20 + 0.8 × 0.15 + 0.9 × 0.20 + 0.9 × 0.15 + 0.9 × 0.10 + 0.85 × 0.10 + 0.85 × 0.10
= 0.17 + 0.12 + 0.18 + 0.135 + 0.09 + 0.085 + 0.085
= 0.865
```
Modifiers: none.
**Final score: 0.87** (code has 0.90; close, slight downgrade).

## Reconciliation with current code

After applying this rubric:

| Estimate | Code value | Rubric value | Action |
|---|---|---|---|
| Pelland 2026 | 0.95 | 0.94 | Keep — within rounding |
| Vieira 2021 hypertrophy (non-eq) | 0.525 | 0.51 | Update |
| Vieira 2021 strength | 0.75 | 0.74 | Keep — within rounding |
| Grgic 2021 overall | 0.85 | 0.81 | Update |
| Grgic 2021 trained subgroup | 0.765 | 0.69 | Update |
| Robinson 2022 (both) | 0.90 | 0.87 | Update |

The discrepancies are small but worth fixing now to set the precedent. Going
forward, every new paper gets scored against this rubric and the scores show
up in the module's docstring with reasoning.

## When to deviate from the rubric

The rubric is a starting point, not a constraint. Cases where you might
override:

- A landmark paper that's the only source for a particular question
  (give it benefit of the doubt within reason)
- A recent paper using novel methodology that this rubric doesn't capture
  well (note it and document the override)
- A paper that's technically excellent but addresses such a narrow population
  that its general applicability is limited (the applicability scoring should
  handle this, but if it doesn't, downweight quality_score)

Document every deviation in the module's notes with reasoning. The rubric
exists so deviations are visible and defensible, not to eliminate judgment.

## What this rubric is not

- Not a substitute for actually reading the paper. The dimensions only make
  sense if you've engaged with the methods.
- Not a perfect ranking. Two papers scoring 0.85 are similar in quality, but
  it doesn't follow that 0.86 is better than 0.84. Treat scores as approximate.
- Not the only filter on which papers go into the registry. Some papers should
  be rejected outright (retracted, fundamentally flawed methods, sponsored
  with bias) rather than included with a low quality score. Quality scores
  modulate weight; they don't gate inclusion.
- Not a substitute for `applicability_to()`. Quality is about how well the
  paper answers ITS OWN question. Applicability is about how well the paper's
  question matches the user's situation. Both matter and they're orthogonal.

## Versioning

Bump this rubric's version when the weights or scoring criteria change
materially. Re-score all existing priors against the new version.

**Current version: v1.0** (initial release).
