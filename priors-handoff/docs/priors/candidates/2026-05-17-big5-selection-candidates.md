# Priors Layer — Priority Candidate Shortlist (Big-5 exercise selection)

**Date:** 2026-05-17
**Seeker pass:** Focus area from orchestrator — exercise-selection `Gap`s for
the large muscle groups, at sub-muscle granularity: chest (clavicular vs
sternocostal pec), lats/mid-back, gluteus maximus, deltoids. Quadriceps SKIPPED
(Kassiano 2026 already shortlisted in `2026-05-17-candidates.md`).
**Scope:** Priority candidates (bucket 1) only. Bucket-2 papers appended to
`DEFERRED_CANDIDATES.md`.

Ranked best-first by: coverage-area value (gap > thin), evidence strength,
accessibility. Each candidate goes next to the `priors-relevance-checker`.

Selection-hunt rule applied: the target shape is a head-to-head
exercise-A-vs-exercise-B longitudinal RCT with direct hypertrophy measurement;
such a paper outranks a muscle-X hypertrophy meta-analysis (which usually pools
only RT-vs-baseline and carries no per-exercise contrast).

---

## Pipeline disposition (updated 2026-05-17, Session 5)

| # | Paper | Outcome |
|---|---|---|
| 1 | Plotkin 2023 | **ENCODED** — `plotkin_2023.py`, quality 0.875, audit MATERIAL DISCREPANCIES (sign-convention labels corrected). |
| 2 | Chaves 2020 | **ENCODED** — `chaves_2020.py`, quality 0.79, audit MATERIAL DISCREPANCIES (sample-size statements + quality re-score corrected). |

Lats/mid-back and deltoid selection were reported unfillable this pass and are
now annotated `literature-blocked` in `COVERAGE.md` §2.

---

## 1. Plotkin et al. (2023) — Hip thrust vs. back squat, gluteus maximus hypertrophy

- **Citation:** Plotkin DL, Rodas MA, Vigotsky AD, McIntosh MC, Breeze E,
  Ubrik R, Robitzsch C, Agyin-Birikorang A, Mattingly ML, Michel JM, Kontos NJ,
  Lennon S, Frugé AD, Wilburn CM, Weimar WH, Bashir A, Beyers RJ, Henselmans M,
  Contreras BM, Roberts MD. "Hip thrust and back squat training elicit similar
  gluteus muscle hypertrophy and transfer similarly to the deadlift."
  *Frontiers in Physiology*, 2023, 14:1279170.
- **DOI:** 10.3389/fphys.2023.1279170 · **PMID:** 37877099 · PMC10593473
- **Target:** §2 Legs (knee & hip) — Gluteus maximus exercise selection
  (`Gap`). Directly addresses the "hip thrust vs squat" selection question
  COVERAGE.md names, and at sub-region granularity (upper/middle/lower glute
  max sites).
- **Type:** `gap-filler`
- **Why it matters:** True head-to-head exercise-vs-exercise RCT — the target
  shape for a selection gap. 9-week supervised intervention, 34 untrained
  adults (mostly female) randomised to hip thrust vs back squat, volume-equated,
  with **MRI** cross-sectional area at three gluteus maximus sites (plus medius
  and minimus) — top measurement tier. Result: gluteal hypertrophy similar
  between exercises (hip thrust numerically slightly ahead, CIs span zero),
  thigh hypertrophy favours the squat, strength gains specific to the trained
  lift. Yields actionable `ExerciseEmphasis` data for a large-muscle-group gap
  with zero current coverage — and resolves the squat-vs-hip-thrust question
  that the deferred Krause Neto 2025 MA could only address narratively.
- **Access:** Open access (Frontiers, CC-BY) on PMC (PMC10593473). Full text
  reachable.
- **Overlap flag:** Likely one of the primary studies inside the deferred
  Krause Neto 2025 glute MA — but Krause Neto is parked, not encoded, and
  carries no per-exercise data, so there is no double-counting risk. No glute
  paper currently encoded. Relevance-checker to confirm.

## 2. Chaves et al. (2020) — Incline vs. horizontal bench press, regional chest hypertrophy

- **Citation:** Chaves SFN, Rocha-Júnior VA, Encarnação IGA, Martins-Costa HC,
  Freitas EDS, Coelho DB, Franco FSC, Loenneke JP, Bottaro M, Ferreira-Júnior JB.
  "Effects of Horizontal and Incline Bench Press on Neuromuscular Adaptations
  in Untrained Young Men." *International Journal of Exercise Science*, 2020,
  13(6):859–872.
- **DOI:** 10.70252/FDNB1158 · **PMID:** 32922646 · PMC7449336
- **Target:** §2 Chest — Pectoralis major exercise selection (`Gap`),
  specifically the clavicular (upper) vs sternocostal sub-region split that
  COVERAGE.md flags as the key chest selection question.
- **Type:** `gap-filler`
- **Why it matters:** A longitudinal exercise-vs-exercise RCT (8 weeks, 47
  untrained men, 3 groups: horizontal-only / incline-only / combination),
  with **B-mode ultrasound** muscle thickness at three pectoralis sites
  (2nd intercostal = clavicular, 3rd, 5th intercostal = sternocostal). Result:
  incline-only produced greater clavicular-region (upper chest) thickness gains
  (~0.5–0.6 cm advantage); sternocostal sites grew similarly across all groups;
  general strength similar. This is the strongest available longitudinal
  evidence for upper-vs-lower chest exercise selection — and the only one of
  acceptable design found, the rest of the chest literature being acute EMG.
- **Access:** Open access (free full text) on PMC (PMC7449336). Full text
  reachable.
- **Overlap flag:** None — no chest paper currently encoded. Distinct from the
  deferred Lanza 2024 (bench-press-vs-control, not an A-vs-B comparison).
  Caveats for the relevance-checker: once-weekly training frequency (low),
  untrained men, and a small per-group n (15–17) — design is acceptable but
  modest; the entry-maker should score quality accordingly.

---

## Gaps NOT filled this pass — reported as genuinely unfillable for now

Per the seeker brief's fallback rule for EMG-dominated muscles: where no
longitudinal exercise-vs-exercise hypertrophy trial of acceptable quality
exists, the gap is reported as blocked on the literature, not on seeker effort.
No weak paper was forced into the shortlist.

### Latissimus dorsi / mid-back — UNFILLABLE for now

Searched the known longitudinal comparison designs: pulldown vs row, pull-up
vs row, lat pulldown grip/orientation variants, straight-arm pulldown vs
pulldown. **Every** result was an acute surface-EMG activation study (e.g.
Lehman 2004; the 2025 MDPI grip-variation EMG analysis; pull-up vs row
activation papers) — excluded by the evidence rubric because activation
predicts long-term hypertrophy poorly. No longitudinal trial with direct
latissimus thickness/CSA measurement comparing two back exercises was found.
One pulldown-variation clinical trial (ClinicalTrials.gov NCT07296771-class)
appears to be activation-focused / unpublished. Recommend re-checking once a
longitudinal pulldown-vs-row hypertrophy RCT publishes; for now the lat
selection gap is genuinely blocked on the literature.

### Deltoids (anterior / lateral / posterior) — UNFILLABLE for now

Searched press-vs-lateral-raise, lateral-raise execution variants, and rear-delt
designs. The only longitudinal hypertrophy trial that surfaced is
Coleman/Larsen 2024 (dumbbell vs cable lateral raise) — already parked in
`DEFERRED_CANDIDATES.md`. Under the new selection rules it is **not** a true
exercise-vs-exercise selection paper: it is an equipment-equivalence question
(dumbbell vs cable, ~null result) within the *same* movement, so it does not
inform which delt exercises best target the anterior vs lateral vs posterior
heads. Status unchanged — it stays deferred, not promoted. The remaining delt
literature (e.g. Campos 2020 "Different Shoulder Exercises Affect the Activation
of Deltoid Portions") is acute EMG and excluded. No press-vs-raise or rear-delt
longitudinal hypertrophy RCT of acceptable design was found. Delt head-level
selection is genuinely blocked on the literature for now.

---

## Note on the deferred bench-press paper (Lanza 2024)

Lanza MB et al. 2024 (bench press, four-muscle hypertrophy response, 10-week
RCT) remains in `DEFERRED_CANDIDATES.md`. It is bench-press-vs-control, not an
exercise-A-vs-B comparison, and uses a low load (50–55% 1RM); it does not
resolve upper/mid/lower chest selection. Chaves 2020 (this shortlist) is the
correct chest selection candidate; Lanza stays deferred. Flagged here so the
orchestrator does not re-find it.
