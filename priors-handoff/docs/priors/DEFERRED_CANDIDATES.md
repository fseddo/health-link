# Priors Layer — Deferred Candidate Papers

Papers the `priors-seeker` has found that are **on-topic** for the project's
broader research scope (resistance training for hypertrophy/strength, exercise
selection, form) and genuinely useful **eventually**, but are **not** aligned
with a current priority gap (see `COVERAGE.md` section 3).

They are parked here so the discovery is not lost. When a deferred paper's
coverage area later becomes a priority, it can be promoted into the normal
pipeline without re-finding it.

## What belongs here

- On-topic but not a current priority: a niche muscle, a tier-3 topic (sleep,
  RIR/RPE calibration, protein/nutrition), or a deeper sub-question of an
  already-covered area.

## What does NOT belong here

- **Priority candidates** — those go in the seeker's dated shortlist and into
  the pipeline, not here.
- **Out-of-scope papers** — anything not about resistance training for
  hypertrophy/strength (cardio, rehab, pure mechanism). These are discarded,
  not parked.

## How to use this file

- The `priors-seeker` **appends** rows; it never prunes.
- To **promote** a paper: run it through the pipeline (relevance-checker →
  entry-maker → auditor) and delete its row here.
- A human should review periodically and promote or delete stale rows.

## Deferred papers

| Paper (authors, year, title) | DOI / PMID | Relevant to | Why deferred | Access | Found |
|---|---|---|---|---|---|
| Schoenfeld BJ et al. (2018), "Resistance Training Volume Enhances Muscle Hypertrophy but Not Strength in Trained Men" | DOI 10.1249/MSS.0000000000001764 / PMID 30153194 | Volume → strength (THIN dose topic, COVERAGE sec.1) | On-topic strengthener for a THIN topic, but it is a single 8-week RCT (34 trained men) not a meta-analysis; the seeker brief prefers a second meta-analysis to strengthen a THIN dose topic. Promote if no volume→strength MA is found. | Open access (PMC6303131) | 2026-05-17 |
| Coleman M / Larsen S et al. (2024), dumbbell vs. cable lateral raises for lateral deltoid hypertrophy: an experimental study | DOI 10.3389/fphys.2025.1611468 / PMID 40692697 | Deltoid (lateral head) exercise selection (Gap, COVERAGE sec.2) | On-topic 8-week within-subject hypertrophy RCT (24 trained, ultrasound), but it is an equipment-equivalence question (dumbbell vs cable, ~null result) rather than the higher-value question of which delt exercises are best. Useful when delt coverage is actively built out. | Open access (PMC12277279) | 2026-05-17 |
| Lanza MB / Padro? et al. (2024), "Muscle hypertrophy response across four muscles involved in the bench press exercise: Randomized 10 weeks training intervention" | DOI 10.1016/j.jbmt.2024.10.022 (J Bodywork Mov Ther S1360-8592(24)00389-9) | Pectoralis major / anterior deltoid (Gap, COVERAGE sec.2) | On-topic 10-week RCT (24 men, CT/CSA) showing bench press grows pec major > pec minor/triceps, but it is bench-press-vs-control, not an exercise-*selection* comparison between chest exercises, and uses a low load (50-55% 1RM). Does not resolve upper/mid/lower chest selection. Promote if a stronger chest comparison is unavailable. | Paywalled (Elsevier; abstract only) | 2026-05-17 |
| Krause Neto W, Vieira TLK, Gama EF (2025), "The impact of resistance training on gluteus maximus hypertrophy: a systematic review and meta-analysis" | DOI 10.3389/fphys.2025.1542334 / PMID 40276368 | Gluteus maximus exercise selection (Gap, COVERAGE sec.2) | Shortlisted then deferred after relevance-check: it is a meta-analysis but pools only a generic whole-muscle RT-vs-baseline effect (SMD 0.71, 95% CI 0.50–0.91); it reports no per-exercise pooled comparison and no per-exercise growth data, so it yields no ExerciseEmphasis and does not fill the glute exercise-*selection* gap. Hip-thrust prioritisation is narrative only. Low actionability; would need a new single-source non-poolable Topic. Promote only if no controlled exercise-vs-exercise glute hypertrophy trial (e.g. hip thrust vs squat) can be found. | Open access (PMC12018462) | 2026-05-17 |
| Kassiano W, Kunevaliki G, Costa B, Nunes JP, Castro-E-Souza P, Tricoli I, Ribeiro AS, Cyrino ES (2024), "Addition of the barbell hip thrust elicits greater increases in gluteus maximus muscle thickness in untrained young women" | DOI 10.47206/ijsc.v4i1.284 | Gluteus maximus exercise selection (Gap, COVERAGE sec.2) | On-topic 10-week controlled trial (33 untrained women, B-mode ultrasound) showing adding the barbell hip thrust to a leg-press + stiff-leg-deadlift base produced greater glute max thickness gains (+9.3% vs +6.0%, P=0.016). Useful as a glute strengthener, but it is an *addition* design (with-hip-thrust vs without), not a clean head-to-head exercise-A-vs-B contrast, and is non-randomised — so under the new selection rules it ranks below Plotkin 2023 (hip thrust vs back squat RCT, shortlisted this pass). Promote as a second glute source once Plotkin 2023 is encoded and a corroborating study is wanted. | Open access (journal.iusca.org) | 2026-05-17 |
