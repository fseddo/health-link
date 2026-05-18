# Priors Layer — Coverage Map

What the literature-priors layer currently covers, what it does not, and how
strong each covered area is. This is a **living document**: the
`priors-entry-maker` updates it when a paper is encoded, and the
`priors-seeker` reads it to decide which papers to hunt for next.

**Last updated:** 2026-05-18 (ADR-011 involvement layer noted below; map
otherwise unchanged since 2026-05-17 — Chaves 2020 moved pectoralis major
Gap -> Thin).

## How to read this

Two things the priors layer must serve: **programming/dose questions** (how to
train) and **exercise selection per muscle** (what to train each muscle with).
Section 1 is one table; section 2 is grouped into tables by body region.

This map covers **literature evidence** only. The exercise→muscle
**involvement** map (ADR-011, `app/priors/exercise_involvement.py`) is a
separate, anatomy-derived layer — cross-muscle volume accounting, not
literature coverage — and is deliberately not tracked here. See `BACKLOG.md`
for its state and the catalogue build-out.

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
| Rest-interval duration → hypertrophy | Thin | Singer 2024 (0.77) | One Bayesian meta-analysis (9 RCTs). Effect trivial — limb hypertrophy mildly favours longer rest, whole-body slightly favours shorter; all CrIs cross zero. |
| Rest-interval duration → strength | **Gap** | — | Singer 2024 is hypertrophy-only; no rest-interval strength source encoded. |
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

Exercise selection operates at **sub-muscle granularity**. Most muscles have
heads or regions that different exercises emphasise differently — the
clavicular vs sternocostal pectoralis, the three deltoid heads, the triceps
long head, the four quadriceps heads. The optimizer needs evidence at that
level, so the "Heads / regions for selection" column names the sub-targets
that matter. A muscle is only fully `Covered` once its selection-relevant
sub-regions are; `Status` is for the muscle as a whole.

Rows are grouped by body region. **Out of scope** (not tracked): neck and
rotator cuff — rehab-oriented, not hypertrophy-selection targets.

**Coverage tally:** 4 muscles `Covered` (triceps, hamstrings, gastrocnemius,
gluteus maximus), 2 `Thin` (biceps, pectoralis major), 17 `Gap`. Exercise
selection is the layer's weakest area.

### Chest

| Muscle | Status | Heads / regions for selection | Sources (quality) | Notes |
|---|---|---|---|---|
| Pectoralis major | Thin | Clavicular head (upper chest); sternocostal head (mid/lower); sternal "inner" fibres — fullness near the sternum, adduction-biased | Chaves 2020 (0.79) | Incline vs flat vs combination bench press, 8-week 1x/week RCT, untrained men, ultrasound MT. Incline preferentially grows the **clavicular** head (+62% vs +32% flat, p=0.003) — encoded `confidence=high`. The **sternocostal** head grew comparably with all variants (no sig. between-group difference, p=0.095 / 0.227) — encoded `confidence=low`. Decline press and adduction-biased "inner" work (cable crossover, pec-deck end-range) remain unaddressed, so the row is Thin, not Covered. |
| Pectoralis minor | **Gap** | (whole; postural) | — | Low priority — not a primary hypertrophy-selection target. |

### Back

| Muscle | Status | Heads / regions for selection | Sources (quality) | Notes |
|---|---|---|---|---|
| Latissimus dorsi | **Gap** (measured) | Upper vs lower lat fibres; width- vs thickness-biased pulls | — measured; mechanistic fallback exists | **No measured trial — literature-blocked** (searched 2026-05-17; pulldown / pull-up / row literature is acute-EMG only). A **mechanistic fallback prior** now covers lat exercise selection — ADR-010, `app/priors/mechanistic/lats.py`: biomechanics-derived, `confidence` low (whole-muscle) / speculative (upper-lower), never pooled with measured emphasis, superseded if a real RCT is encoded. Re-check for a longitudinal pulldown-vs-row hypertrophy RCT. |
| Trapezius | **Gap** | Upper, middle, lower traps — three distinct selection targets | — | Shrug vs row vs Y-raise / lower-trap work unaddressed. |
| Rhomboids | **Gap** | (whole) | — | Mid-back retraction; overlaps row selection with mid-trap. |
| Erector spinae | **Gap** | Thoracic vs lumbar; whole | — | Deadlift / back-extension / good-morning selection unaddressed. |
| Serratus anterior | **Gap** | (whole) | — | Niche — scapular protraction work. |

### Shoulders

| Muscle | Status | Heads / regions for selection | Sources (quality) | Notes |
|---|---|---|---|---|
| Deltoids | **Gap** (measured) | Anterior, lateral, posterior heads — three functionally distinct targets needing different exercises | — measured; mechanistic fallback exists | **No measured trial — literature-blocked** (searched 2026-05-17; only Coleman/Larsen 2024 dumbbell-vs-cable lateral raise, an equipment-equivalence question, parked in `DEFERRED_CANDIDATES.md`; remaining delt literature is acute EMG). A **mechanistic fallback prior** now covers deltoid exercise selection per head — ADR-010, `app/priors/mechanistic/deltoids.py`: biomechanics-derived, `confidence` low, never pooled with measured emphasis, superseded if a real RCT is encoded. |

### Arms

| Muscle | Status | Heads / regions for selection | Sources (quality) | Notes |
|---|---|---|---|---|
| Triceps brachii | Covered | Long head; lateral + medial heads | Maeo 2023 (0.89) | Overhead vs neutral extension; long-head emphasis quantified. |
| Biceps brachii | Thin | Long head (outer) vs short head (inner); distal vs mid regions | Pedrosa 2023 (0.83) | Pedrosa covers the distal/mid ROM *regional* effect only — NOT exercise-vs-exercise (incline vs preacher vs spider curl) selection. |
| Brachialis | **Gap** | (whole) | — | Neutral/pronated-grip curl emphasis. Previously folded into "elbow flexors"; now its own row. |
| Forearms | **Gap** | Wrist flexors; wrist extensors; brachioradialis | — | Wrist-curl / reverse-curl selection unaddressed. |

### Core

| Muscle | Status | Heads / regions for selection | Sources (quality) | Notes |
|---|---|---|---|---|
| Rectus abdominis | **Gap** | Upper- vs lower-region emphasis | — | Crunch vs reverse-crunch / leg-raise vs anti-extension selection. |
| Obliques | **Gap** | Internal / external obliques | — | Rotation and anti-rotation work. |

### Legs — knee & hip

| Muscle | Status | Heads / regions for selection | Sources (quality) | Notes |
|---|---|---|---|---|
| Quadriceps | **Gap** | Rectus femoris (biarticular — needs hip-extended work); vastus lateralis, medialis, intermedius | — | Squat vs leg-extension vs hip-flexed work differ by head. Kassiano 2026 (back squat vs leg extension) shortlisted but paywalled; Pedrosa 2022 (knee-extension ROM) BLOCKED — full text inaccessible. Partial side-evidence: Plotkin 2023 found the back squat out-grows the barbell hip thrust for the quadriceps (+3.6 cm² mCSA, CI excludes zero) — a squat-vs-hip-thrust contrast, not a quad-isolation comparison; status stays Gap. |
| Hamstrings | Covered | Biceps femoris long & short heads; semitendinosus; semimembranosus | Maeo 2021 (0.88) | Seated (long-length) vs prone leg curl; sub-muscle emphasis quantified. BF short-head pair is `confidence=low` (n.s.). |
| Gluteus maximus | Covered | Upper / middle / lower subregions | Plotkin 2023 (0.875) | Hip thrust vs back squat: 9-week volume-equated RCT, MRI mCSA. EQUIVALENCE — no detectable glute-max difference at any subregion; both exercises encoded at equal 1.0 emphasis (`confidence=medium`). Squat additionally out-grows the hip thrust for quads + adductors. Krause Neto 2025 (glute MA) still deferred — no per-exercise data; record Plotkin as a constituent if it is ever encoded. Lunge selection still unaddressed. |
| Hip abductors | **Gap** | Gluteus medius & minimus; tensor fasciae latae | — | New row — glute medius was previously only named in passing. Abduction / lateral-band / single-leg work. Partial side-evidence: Plotkin 2023 reports a combined gluteus medius+minimus mCSA contrast (hip thrust vs back squat, −1.8 cm², CI crosses zero — no difference); the two abductors are not separated and neither exercise is abduction-specific, so status stays Gap. |
| Hip adductors | **Gap** | Adductor magnus (also a hip extensor), longus, brevis; gracilis | — | New row — was entirely absent from the map. Adduction-machine / Copenhagen / wide-stance work. Partial side-evidence: Plotkin 2023 found the back squat out-grows the barbell hip thrust for the adductors (+2.5 cm² mCSA, CI excludes zero) — a squat-vs-hip-thrust contrast, not an adduction-isolation comparison; status stays Gap. |
| Hip flexors | **Gap** | Iliopsoas; sartorius; (rectus femoris — see Quadriceps) | — | New row; niche, low priority. |

### Legs — lower

| Muscle | Status | Heads / regions for selection | Sources (quality) | Notes |
|---|---|---|---|---|
| Gastrocnemius | Covered | Medial & lateral heads | Kassiano 2023 (0.78) | Lengthened / full / shortened-ROM calf raise. |
| Soleus | **Gap** | (whole) | — | Seated (knee-flexed) calf raise — Kassiano covers gastrocnemius only. |
| Tibialis anterior | **Gap** | (whole) | — | New row — calf antagonist. Dorsiflexion / tib-raise work. |

---

## 3. Priority gaps for the seeker

Ranked by value to the recommendation engine:

1. **Exercise selection for the large muscle groups** — lats/mid-back, quads,
   delts. The optimizer cannot recommend whole-body workouts
   (a stated research goal) without these, and needs evidence at sub-region
   granularity (see §2): the three deltoid heads, the four quad heads.
   Hamstrings (Maeo 2021) and gluteus maximus (Plotkin 2023) are now covered;
   chest is now Thin (Chaves 2020 — incline vs flat, clavicular vs
   sternocostal) but still needs a decline/adduction source to reach Covered.
   Quads has two queued candidates — Kassiano
   2026 (shortlisted, paywalled) and Pedrosa 2022 (blocked, full text
   inaccessible). The smaller groups newly added to
   the §2 map — traps, erectors, forearms, abs, brachialis, hip
   adductors/abductors, soleus, tibialis anterior, serratus — are genuine gaps
   but rank below the five big movers.
2. **Strengthen the THIN dose topics** — volume→strength, frequency, and load
   each rest on a single source. A second meta-analysis on any of them adds
   real robustness (and would exercise multi-paper pooling).
3. **Periodization & rest-interval strength** — periodization is a whole
   programming dimension with no evidence yet and is central to the
   progression model. Rest-interval *hypertrophy* is now Thin (Singer 2024);
   its *strength* half remains a Gap.
4. **RIR/RPE calibration** — needed for the app to interpret user-reported
   effort correctly.

The seeker should target (1) and (2) first: fill muscle-group gaps, then
strengthen single-source dose topics.
