# Priors Layer — Coverage Map

What the literature-priors layer currently covers, what it does not, and how
strong each covered area is. This is a **living document**: the
`priors-entry-maker` updates it when a paper is encoded, and the
`priors-seeker` reads it to decide which papers to hunt for next.

**Last updated:** 2026-05-17 (after schoenfeld_load_2017).

## How to read this

Two things the priors layer must serve: **programming/dose questions** (how to
train) and **exercise selection per muscle** (what to train each muscle with).
There is a table for each.

- **Quality** = the paper's `quality_score` (0–1, per `QUALITY_RUBRIC.md`).
  Higher is stronger evidence. Every citation carries its score in its row.
- **Status**: `Covered` (≥1 solid source) · `Thin` (only one source, or only
  weak ones — a strengthening target) · `Gap` (no encoded evidence).

---

## 1. Programming & dose-response coverage

These map to registry `Topic`s — the questions the optimizer asks about *how*
to train.

| Coverage area | Status | Encoded sources (quality) | Notes |
|---|---|---|---|
| Volume → hypertrophy | Covered | Pelland 2026 (0.94); Schoenfeld/Ogborn/Krieger 2017 (0.75) | Two sources; not numerically pooled (different scales). |
| Volume → strength | Thin | Pelland 2026 (0.94) | Single source. |
| Frequency → hypertrophy | Thin | Pelland 2026 (0.94) | Single source; effect itself is ~null at fixed volume. |
| Frequency → strength | Thin | Pelland 2026 (0.94) | Single source. |
| Load / rep-range → hypertrophy | Thin | Schoenfeld/Grgic 2017 (0.77) | Single source; effect ~null (load-independent to failure). |
| Load / rep-range → strength | Thin | Schoenfeld/Grgic 2017 (0.77) | Single source; high load favoured for 1RM. |
| Failure / proximity-to-failure → hypertrophy | Covered | Vieira 2021 (0.51); Grgic 2021 (0.69–0.81); Refalo 2023 (0.87) | Best-covered topic — 3 overlapping meta-analyses. |
| Failure → strength | Covered | Vieira 2021 (0.74); Grgic 2021 (0.81) | Two sources. |
| Range of motion → hypertrophy | Thin | Wolf 2023 (0.81) | One meta-analysis; muscle-specific primary studies (Kassiano, Pedrosa) corroborate. |
| Range of motion → strength | Thin | Wolf 2023 (0.81) | Single source. |
| Muscle length → regional hypertrophy | Covered | Varovic 2025 (0.83); Pedrosa 2023 (0.83) | MA + one primary study (in the MA — not pooled). |
| Arm/joint position → whole-muscle hypertrophy | Thin | Maeo 2023 (0.89) | Single high-quality study (triceps). |
| Rest-interval duration → hypertrophy/strength | **Gap** | — | Not encoded. |
| Tempo / repetition duration → adaptations | **Gap** | — | Not encoded. |
| Exercise order / sequencing | **Gap** | — | Not encoded. |
| Periodization / progression models / deloads | **Gap** | — | Not encoded; central to the progression model. |
| RIR/RPE calibration accuracy | **Gap** | — | Needed to interpret user-reported effort (BACKLOG tier 3). |
| Sleep / recovery / readiness → performance | **Gap** | — | App has recovery features (BACKLOG tier 3). |
| Protein / nutrition → hypertrophy | **Gap** | — | Out of current focus; deferred. |

---

## 2. Exercise-selection coverage by muscle group

Which muscles have evidence for *what exercise (or execution) trains them
best* — `ExerciseEmphasis` data, or whole-muscle exercise comparisons.

| Muscle group | Status | Encoded sources (quality) | Notes |
|---|---|---|---|
| Triceps brachii | Covered | Maeo 2023 (0.89) | Long head, lateral+medial, whole; overhead vs neutral extension. |
| Gastrocnemius | Covered | Kassiano 2023 (0.78) | Medial + lateral heads; lengthened/full/shortened-ROM calf raise. |
| Biceps brachii / elbow flexors | Thin | Pedrosa 2023 (0.83) | Regional (distal/mid) ROM effect only — NOT exercise-vs-exercise selection. |
| Pectoralis major (chest) | **Gap** | — | No exercise-selection evidence (upper/mid/lower chest unaddressed). |
| Latissimus dorsi / mid-back | **Gap** | — | No evidence. |
| Quadriceps | **Gap** | — | Pedrosa 2022 (knee-extension ROM) queued but BLOCKED — full text inaccessible. |
| Hamstrings | **Gap** | — | Maeo 2021 (seated vs lying leg curl) is a strong candidate. |
| Gluteus maximus / medius | **Gap** | — | No evidence. |
| Deltoids (ant/lateral/posterior) | **Gap** | — | No evidence. |
| Soleus | **Gap** | — | Kassiano covers gastrocnemius, not soleus. |
| Trapezius / rhomboids / erectors | **Gap** | — | No evidence. |
| Forearms / abdominals | **Gap** | — | No evidence; lower priority. |

---

## 3. Priority gaps for the seeker

Ranked by value to the recommendation engine:

1. **Exercise selection for the large muscle groups** — chest, back/lats,
   quads, hamstrings, glutes, delts. The optimizer cannot recommend
   whole-body workouts (a stated research goal) without these. Hamstrings
   (Maeo 2021) and quads (Pedrosa 2022, currently blocked) are the nearest
   candidates.
2. **Strengthen the THIN dose topics** — volume→strength, frequency, and load
   each rest on a single source. A second meta-analysis on any of them adds
   real robustness (and would exercise multi-paper pooling).
3. **Rest intervals & periodization** — whole programming dimensions with no
   evidence yet; periodization is central to the progression model.
4. **RIR/RPE calibration** — needed for the app to interpret user-reported
   effort correctly.

The seeker should target (1) and (2) first: fill muscle-group gaps, then
strengthen single-source dose topics.
