# Priors Layer — Priority Candidate Shortlist

**Date:** 2026-05-17
**Seeker pass:** No focus area — worked COVERAGE.md section 3 priority-gaps list
top-down.
**Scope:** Priority candidates (bucket 1) only. Deferred (bucket 2) papers were
appended to `DEFERRED_CANDIDATES.md`.

Ranked best-first by: coverage-area value (gap > thin), evidence strength,
accessibility. Each candidate goes next to the `priors-relevance-checker`.

---

## Pipeline disposition (updated 2026-05-17, Session 5)

| # | Paper | Outcome |
|---|---|---|
| 1 | Maeo 2021 | **ENCODED** — `maeo_2021.py`, quality 0.88, audit ACCURATE. |
| 2 | Krause Neto 2025 | **DEFERRED** — relevance-check found no per-exercise data; moved to `DEFERRED_CANDIDATES.md`. |
| 3 | Kassiano 2026 | **PENDING** — not yet run through the pipeline (paywalled). |
| 4 | Singer 2024 | **ENCODED** — `singer_2024.py`, quality 0.77, audit MINOR DISCREPANCIES (fixed). |
| 5 | Grgic 2018 | **PENDING** — not yet run through the pipeline (paywalled). |

---

## 1. Maeo et al. (2021) — Seated vs. prone leg curl, hamstrings hypertrophy

- **Citation:** Maeo S, Huang M, Wu Y, Sakurai H, Kusagawa Y, Sugiyama T,
  Kanehisa H, Isaka T. "Greater Hamstrings Muscle Hypertrophy but Similar
  Damage Protection after Training at Long versus Short Muscle Lengths."
  *Medicine & Science in Sports & Exercise*, 2021, 53(4):825-837.
- **DOI:** 10.1249/MSS.0000000000002523 · **PMID:** 33009197
- **Target:** Section 2 — Hamstrings exercise selection (`Gap`). The exact paper
  COVERAGE.md names as the nearest hamstrings candidate.
- **Type:** `gap-filler`
- **Why it matters:** 12-week controlled training intervention, within-subject
  design (one leg seated, one leg prone leg curl), MRI-measured muscle volume —
  the strongest measurement tier. Seated (hip-flexed, longer-length) leg curl
  produced greater total hamstrings hypertrophy (~14% vs ~9%) and a much larger
  biceps femoris long-head effect. Directly yields `ExerciseEmphasis` data for a
  large muscle group with zero current coverage, and gives an exercise-vs-
  exercise selection result the optimizer can act on.
- **Access:** Open access (Wolters Kluwer, CC-BY-NC-ND) on PMC
  (PMC7969179). Full text reachable.
- **Overlap flag:** Distinct from encoded Varovic 2025 (muscle-length →
  regional hypertrophy meta-analysis) — Maeo 2021 is an exercise-comparison
  primary study and may be one of Varovic's included studies, so the length
  *mechanism* could overlap. The seated-vs-lying *exercise selection* result is
  not encoded anywhere. Relevance-checker to confirm it is not already inside
  Varovic 2025's pool in a way that double-counts.

## 2. Krause Neto et al. (2025) — Gluteus maximus hypertrophy, exercise selection meta-analysis

- **Citation:** Krause Neto W, Vieira TLK, Gama EF. "The impact of resistance
  training on gluteus maximus hypertrophy: a systematic review and
  meta-analysis." *Frontiers in Physiology*, 2025, 16:1542334.
- **DOI:** 10.3389/fphys.2025.1542334 · **PMID:** 40276368
- **Target:** Section 2 — Gluteus maximus exercise selection (`Gap`).
- **Type:** `gap-filler`
- **Why it matters:** Systematic review + meta-analysis (12 studies / 11 in the
  MA, 318 participants) — top evidence tier. Addresses which exercises drive
  glute hypertrophy (single- vs multi-joint; hip thrust prioritisation).
  Fills a large-muscle-group exercise-selection gap with a meta-analysis rather
  than a single primary study, which is the preferred evidence form.
- **Access:** Open access (Frontiers, CC-BY) on PMC (PMC12018462). Full text
  reachable.
- **Overlap flag:** None expected — no glute paper currently encoded. As a
  recent MA it likely pools primary studies not individually encoded; the
  relevance-checker should note its constituent studies so future seeker passes
  do not re-propose them.

## 3. Kassiano et al. (2026) — Back squat vs. leg extension, quadriceps hypertrophy & strength

- **Citation:** Kassiano W, Costa B, Kunevaliki G, et al. "Comparison of Muscle
  Hypertrophy and Strength Adaptations Induced by Back Squat and Leg Extension
  Resistance Exercises." *Journal of Strength and Conditioning Research*, 2026,
  40(4):367-376.
- **DOI:** 10.1519/JSC.0000000000005338 · **PMID:** 41379528
- **Target:** Section 2 — Quadriceps exercise selection (`Gap`; the queued
  Pedrosa 2022 is blocked on inaccessible full text — this is an unblocked
  alternative).
- **Type:** `gap-filler`
- **Why it matters:** 8-week RCT, 63 untrained women, ultrasound muscle
  thickness at 3 sites of rectus femoris and vastus lateralis plus 3RM strength.
  Region-specific exercise-selection result: leg extension favours rectus
  femoris growth, back squat favours distal vastus lateralis and squat-specific
  strength. Gives the optimizer an actionable quad `ExerciseEmphasis`
  comparison where there is currently none.
- **Access:** Likely paywalled (Wolters Kluwer / JSCR; no PMC copy found).
  Flag for downstream — abstract is sufficient to confirm design but the
  entry-maker will need full-text access for effect sizes.
- **Overlap flag:** None — no quad paper encoded. Different author-team focus
  from encoded Kassiano 2023 (gastrocnemius calf-raise ROM); same lead author,
  different muscle and question.

## 4. Singer et al. (2024) — Inter-set rest interval duration, hypertrophy meta-analysis

- **Citation:** Singer A, Wolf M, Generoso L, Arias E, Delcastillo K,
  Echevarria E, Martinez A, Androulakis Korakakis P, Refalo MC, Swinton PA,
  Schoenfeld BJ. "Give it a rest: a systematic review with Bayesian
  meta-analysis on the effect of inter-set rest interval duration on muscle
  hypertrophy." *Frontiers in Sports and Active Living*, 2024, 6:1429789.
- **DOI:** 10.3389/fspor.2024.1429789 · **PMID:** 39205815
- **Target:** Section 1 — Rest-interval duration → hypertrophy/strength
  (`Gap`; "whole programming dimension with no evidence", priority 3).
- **Type:** `gap-filler`
- **Why it matters:** Systematic review with Bayesian meta-analysis, 9 RCTs / 19
  effect measurements. Concludes a small benefit to rest >60 s for arm and
  thigh hypertrophy, with hypertrophy achievable across a wide range — gives the
  programming model a defensible rest-interval prior where it currently has
  none. Bayesian pooling fits the layer's effect-estimate format well.
- **Access:** Open access (Frontiers, CC-BY) on PMC (PMC11349676). Full text
  reachable.
- **Overlap flag:** None — rest-interval topic has no encoded source. Shares
  several co-authors with encoded Wolf 2023 and Refalo 2023 (same Schoenfeld
  group); not a content overlap.

## 5. Grgic et al. (2018) — Resistance training frequency → strength meta-analysis

- **Citation:** Grgic J, Schoenfeld BJ, Davies TB, Lazinica B, Krieger JW,
  Pedisic Z. "Effect of Resistance Training Frequency on Gains in Muscular
  Strength: A Systematic Review and Meta-Analysis." *Sports Medicine*, 2018,
  48(5):1207-1220.
- **DOI:** 10.1007/s40279-018-0872-x · **PMID:** 29470825
- **Target:** Section 1 — Frequency → strength (`Thin`; currently single-source
  on Pelland 2026). Also informative for frequency → hypertrophy.
- **Type:** `strengthener`
- **Why it matters:** Dedicated meta-analysis of 22 studies on training
  frequency and strength. Adds a second independent meta-analysis to a THIN
  dose topic and would exercise multi-paper pooling. Its conclusion (frequency
  effect on strength is largely volume-driven; raw frequency effect sizes rise
  0.74 → 1.08 across 1 → 4+ sessions) corroborates and adds nuance to the
  Pelland 2026 frequency prior.
- **Access:** Likely paywalled (Springer / Sports Medicine; no PMC copy
  found). Flag for downstream — abstract gives the headline effect sizes but
  full text needed for the volume-equated subgroup numbers.
- **Overlap flag:** Possible — Pelland 2026 is a recent dose-response
  meta-regression that may include several of the same primary frequency
  studies. This is a separate, older, frequency-specific MA, not a duplicate of
  Pelland 2026, but the relevance-checker should confirm the primary-study
  overlap so the two are not naively pooled.

---

## Notes on gaps not filled this pass

- **Chest (pectoralis major) exercise selection** remains a `Gap`. No strong
  longitudinal exercise-comparison hypertrophy trial surfaced — the available
  literature is dominated by acute EMG-activation studies (excluded by the
  evidence rubric) and one incline-vs-flat training study with known
  measurement-validity concerns. Recommend a dedicated follow-up search.
- **Lats / mid-back exercise selection** remains a `Gap` — current evidence is
  EMG-activation and one in-progress (results-pending) pulldown-vs-row RCT.
  Recommend re-checking once that trial publishes.
- **Volume → strength** (`Thin`) — the best corroborating source found
  (Schoenfeld et al. 2018, "Resistance Training Volume Enhances Muscle
  Hypertrophy but Not Strength in Trained Men", DOI 10.1249/MSS.0000000000001764)
  is a single 8-week RCT, not a meta-analysis. Parked in DEFERRED_CANDIDATES.md
  rather than shortlisted, since the brief prefers a second *meta-analysis* for
  a strengthener.
