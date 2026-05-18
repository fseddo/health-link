# Audit — `exercise_involvement.py` (ADR-011 involvement map)

**Module audited:** `priors-handoff/app/priors/exercise_involvement.py`
**Date:** 2026-05-18
**Auditor:** priors-involvement-auditor (independent functional-anatomy re-derivation)

---

## Scope

The ADR-011 prototype: 74 `(exercise, muscle)` involvement rows across the 16
exercises in `mechanistic/lats.py` (7) and `mechanistic/deltoids.py` (9). Each
row carries a `role` (primary / secondary / stabilizer) that maps via
`ROLE_SET_CREDIT` to a fractional set credit (1.0 / 0.5 / 0.0). The map answers
the CROSS-muscle volume-accounting question only. It was audited as such — not
as an emphasis/sub-region layer. Grip/forearm involvement is explicitly out of
prototype scope and its absence was not treated as a defect.

Every `biomechanical` role was re-derived from scratch (origin/insertion, the
joint action(s) the resistance loads, prime mover vs synergist vs isometric
stabiliser). The three `pelland_2026_table1` rows were additionally cross-checked
against `pelland_2026.HYPERTROPHY_CLASSIFICATIONS`.

## Sources accessed

- StatPearls — *Anatomy, Shoulder and Upper Limb, Teres Major Muscle*:
  https://www.ncbi.nlm.nih.gov/books/NBK580487/
- StatPearls — *Anatomy, Shoulder and Upper Limb, Scapulohumeral Muscles*:
  https://www.ncbi.nlm.nih.gov/books/NBK546633/
- Physiopedia — *Teres Major*: https://www.physio-pedia.com/Teres_Major
- *Effects of the Pullover Exercise on the Pectoralis Major and Latissimus
  Dorsi Muscles as Evaluated by EMG* (ResearchGate):
  https://www.researchgate.net/publication/51695295
- *Electromyographic Activation of Pectoralis Major and Triceps Brachii during
  Dumbbell Pullover*: https://www.researchgate.net/publication/353646302
- *Comparison of EMG Activity during Barbell Pullover and Straight Arm
  Pulldown* (MDPI Applied Sciences): https://www.mdpi.com/2076-3417/12/21/11138
- NASM — *The Biomechanics of the Lat Pulldown*:
  https://blog.nasm.org/biomechanics-of-the-lat-pulldown
- ISSA — *Upright Row: Muscles Worked*:
  https://www.issaonline.com/blog/post/upright-row-muscles-worked-benefits-proper-form-more
- Cross-check: `pelland_2026.py` `HYPERTROPHY_CLASSIFICATIONS` (encoded,
  audited, quality-0.94 transcription of Pelland 2026 Table 1).

---

## Verdict — **MINOR ERRORS**

The map is anatomically sound. Every prime-mover call is correct; no prime
mover is missing; no spurious muscle is listed; the multi-primary treatment of
rows (lat + mid-trap + rhomboids) and of the upright row (lateral delt + trap)
is correct functional anatomy. The three `pelland_2026_table1` rows are all
exact, correctly-classified matches against the encoded Pelland Table 1. The
structural walling-off is clean (`set_credit` is a derived property, every row
is outcome-shared, the registry routes through `_INVOLVEMENT_INDEX` only) and
all 244 tests pass.

The errors found are confined to **rationale honesty and one borderline-role
call that should be flagged but is not** — i.e. wording, not arithmetic or
provenance. Two rationales materially overstate the certainty of a genuinely
debatable call (pec as a pullover prime contributor; teres major treated
uniformly as the lat's helper across both shoulder-extension and
scapular-retraction movements). One muscle that is plausibly involved
(serratus anterior in the pullover) is borderline-omittable and is noted as a
discussion point, not a defect. None of this rises to MATERIAL: no role is
*wrong* in a way that changes a set credit incorrectly, just under-hedged.

---

## Entry-by-entry verification

Legend: ✓ = independent call matches encoded role · ≈ = matches but rationale
over/under-states · ✗ = mismatch · (—) = muscle I judge MISSING.

### Lats-module exercises

#### `dumbbell_pullover`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| latissimus_dorsi | primary | primary | ✓ | Resisted shoulder extension/adduction from deep flexion — lat prime action. Correct. |
| teres_major | secondary | secondary | ✓ | Synergist of shoulder extension/adduction — "lat's little helper" (StatPearls). Correct. |
| pectoralis_major | secondary | secondary | ≈ | Correct that the pec is involved; EMG shows the *sternocostal pec is often the dominant agonist* in a dumbbell pullover (PM ~50% MVIC vs LD ~23%). Calling it merely "secondary" is defensible only because role here is anatomy-of-the-resisted-action, not EMG magnitude — but the rationale's claim that the pec is a clean "secondary contributor" understates how prominent it is. See Concerns. |
| triceps_brachii | secondary | secondary | ✓ | Long head crosses the shoulder; assists shoulder extension with a near-straight arm. EMG corroborates meaningful triceps demand. Correct. |
| posterior_deltoid | secondary | secondary | ✓ | Shoulder extensor; assists. Correct. |
| serratus_anterior | (absent) | borderline secondary | (—) | The serratus is commonly cited as engaged in the pullover (scapular control / rib protraction at the stretched position). Genuinely debatable whether it is dynamically trained or only stabilising. Acceptable to omit in a prototype; noted as MINOR. |

#### `cable_pullover`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| latissimus_dorsi | primary | primary | ✓ | Correct. |
| teres_major | secondary | secondary | ✓ | Correct. |
| pectoralis_major | secondary | secondary | ≈ | Same over-hedge as the dumbbell pullover, slightly less acute (cable line of pull can be set to bias the lat more). Acceptable. |
| triceps_brachii | secondary | secondary | ✓ | Correct. |
| posterior_deltoid | secondary | secondary | ✓ | Correct. |

#### `straight_arm_pulldown`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| latissimus_dorsi | primary | primary | ✓ | Straight-arm shoulder extension — lat prime action. Correct. |
| teres_major | secondary | secondary | ✓ | Correct. |
| triceps_brachii | secondary | secondary | ✓ | Long head assists shoulder extension across the straight-arm range. Correct. |
| posterior_deltoid | secondary | secondary | ✓ | Correct. |
| pectoralis_major | secondary | secondary | ✓ | Sternocostal fibres assist shoulder extension over the early (overhead) range; rationale honestly says "minor". Correct and well-hedged. |

#### `pull_up`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| latissimus_dorsi | primary | primary | ✓ | Lat-driven shoulder extension/adduction. Correct. |
| teres_major | secondary | secondary | ✓ | Correct. |
| biceps_brachii | secondary | secondary | ✓ | Elbow flexion under load. Correct. |
| brachialis | secondary | secondary | ✓ | Prime elbow flexor regardless of grip. Correct. |
| posterior_deltoid | secondary | secondary | ✓ | Assists shoulder extension/adduction. Correct. |
| trapezius | secondary | secondary | ✓ | Lower/mid traps drive scapular depression + downward rotation through the pull. Correct. Note: not in Pelland Table 1 for the bodyweight pull-up, so `biomechanical` is the right basis (Pelland lists `lat_pulldown` not `pull_up`). |
| rhomboids | secondary | secondary | ✓ | Assist scapular retraction/downward rotation. Correct. |

#### `lat_pulldown`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| latissimus_dorsi | primary | primary | ✓ | Correct. |
| teres_major | secondary | secondary | ✓ | Correct. |
| biceps_brachii | secondary (Pelland T1) | secondary | ✓ | **Provenance verified:** `HYPERTROPHY_CLASSIFICATIONS["biceps_brachii"]["indirect"]` contains `lat_pulldown`. `indirect ↔ secondary` agrees. Correct. |
| brachialis | secondary | secondary | ✓ | Correct; `biomechanical` basis is right — Pelland's table has no `brachialis` key. |
| posterior_deltoid | secondary | secondary | ✓ | Correct. |
| trapezius | secondary (Pelland T1) | secondary | ✓ | **Provenance verified:** `HYPERTROPHY_CLASSIFICATIONS["trapezius"]["indirect"]` contains `lat_pulldown`. `indirect ↔ secondary` agrees. Correct. |
| rhomboids | secondary | secondary | ✓ | Correct; `biomechanical` basis right — no `rhomboids` key in Pelland's table. |

#### `seated_cable_row`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| latissimus_dorsi | primary | primary | ✓ | Lat-driven shoulder extension drawing the elbow back. Correct. |
| trapezius | primary | primary | ✓ | Mid traps drive scapular retraction — a genuine second prime action of a row. Correct multi-primary call. |
| rhomboids | primary | primary | ✓ | Scapular retraction/adduction, alongside the mid traps. Correct. |
| posterior_deltoid | secondary | secondary | ≈ | Defensible. The rear delt is a strong synergist of horizontal extension in a row and a case could be made for primary; the module flagged in ADR-011 that this exact call is "occasionally genuinely debatable" but the rationale itself reads as flatly settled. See Concerns (MINOR). |
| teres_major | secondary | secondary | ✓ | Correct. |
| biceps_brachii | secondary | secondary | ✓ | Elbow flexion under load. Correct. (Pelland lists `seated_row`, a different key — `biomechanical` basis is the honest call given the key mismatch.) |
| brachialis | secondary | secondary | ✓ | Correct. |
| erector_spinae | stabilizer | stabilizer | ✓ | Seated upright torso — erectors hold position isometrically. Correct, and the explicit zero-credit row is good documentation. |

#### `barbell_row`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| latissimus_dorsi | primary | primary | ✓ | Correct. |
| trapezius | primary | primary | ✓ | Correct. |
| rhomboids | primary | primary | ✓ | Correct. |
| posterior_deltoid | secondary | secondary | ≈ | Same MINOR hedge note as the seated cable row. |
| teres_major | secondary | secondary | ✓ | Correct. |
| biceps_brachii | secondary | secondary | ✓ | Correct. (Pelland's table lists `bent_over_barbell_row` for `biceps_brachii` indirect — a different key string from `barbell_row`; `biomechanical` basis is the honest, conservative call. See Concerns — MINOR, this is a missed *corroboration* opportunity, not an error.) |
| brachialis | secondary | secondary | ✓ | Correct. |
| erector_spinae | stabilizer | stabilizer | ≈ | **Borderline.** In a bent-over barbell row the erectors resist a large spinal-flexion moment isometrically — correctly `stabilizer`, no dynamic ROM. Defensible. But it is a *harder* isometric demand than the seated row's, and some practitioners train barbell rows partly for that erector demand; the 0.0 credit is the right call for a hypertrophy-volume map (no dynamic lengthening/shortening) and the rationale says so honestly. Accept. |

### Deltoid-module exercises

#### `incline_bench_press`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| pectoralis_major | primary | primary | ✓ | Press — pec-driven horizontal shoulder flexion/adduction. Correct. |
| anterior_deltoid | primary | primary | ✓ | Shoulder flexion is a genuine prime action of an incline press; co-primary is correct (the incline angle raises anterior-delt contribution well above a flat press). Correct multi-primary. |
| triceps_brachii | secondary (Pelland T1) | secondary | ✓ | **Provenance verified:** `HYPERTROPHY_CLASSIFICATIONS["triceps_brachii"]["indirect"]` contains `incline_bench_press`. `indirect ↔ secondary` agrees. Correct. |

#### `overhead_press`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| anterior_deltoid | primary | primary | ✓ | Correct. |
| lateral_deltoid | secondary | secondary | ✓ | Assists abduction/elevation through the press; strong synergist, not prime mover of the sagittal-plane press. Correct. |
| triceps_brachii | secondary | secondary | ✓ | Elbow extension through lockout. Correct. (Pelland lists `shoulder_press`/`dumbbell_shoulder_press` for triceps indirect, not `overhead_press` — key mismatch, so `biomechanical` is honest.) |
| trapezius | secondary | secondary | ✓ | Upper traps upwardly rotate the scapula to complete the overhead position — genuine synergist. Correct. |
| pectoralis_major | (absent) | not required | — | The clavicular pec assists the first ~30° of an overhead press; omission is defensible (contribution is small and range-limited). Not flagged. |

#### `dumbbell_front_raise`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| anterior_deltoid | primary | primary | ✓ | Isolated sagittal-plane shoulder flexion. Correct. |
| pectoralis_major | secondary | secondary | ✓ | Clavicular fibres assist shoulder flexion. Correct. |

#### `cable_lateral_raise`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| lateral_deltoid | primary | primary | ✓ | Shoulder abduction. Correct. |
| anterior_deltoid | secondary | secondary | ✓ | Assists humeral elevation depending on arm path. Correct. |
| trapezius | secondary | secondary | ✓ | Upper traps upwardly rotate the scapula through the raise. Correct. |
| supraspinatus | (absent) | borderline secondary | (—) | The supraspinatus initiates abduction (first ~15°) and is a genuine synergist of any lateral raise. Out of prototype's lat/delt taxonomy and the layer has no `supraspinatus` key encoded elsewhere — omission acceptable, noted MINOR for catalogue build-out. |

#### `upright_row`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| lateral_deltoid | primary | primary | ✓ | Abduction as the elbows rise. Correct. |
| trapezius | primary | primary | ✓ | Upper traps elevate the shoulder girdle / upwardly rotate the scapula — the upright row is a genuine prime trap movement. Correct multi-primary. |
| anterior_deltoid | secondary | secondary | ✓ | Assists humeral elevation. Correct. |
| biceps_brachii | secondary | secondary | ✓ | Elbow flexion as the bar rises. Correct. |
| brachialis | secondary | secondary | ✓ | Prime elbow flexor regardless of grip. Correct. |

#### `dumbbell_lateral_raise`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| lateral_deltoid | primary | primary | ✓ | Correct. |
| anterior_deltoid | secondary | secondary | ✓ | Correct. |
| trapezius | secondary | secondary | ✓ | Upper traps upwardly rotate the scapula. Correct. |
| supraspinatus | (absent) | borderline secondary | (—) | Same note as `cable_lateral_raise`. Consistently omitted across both lateral raises — at least internally consistent. MINOR. |

#### `cable_rear_delt_fly`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| posterior_deltoid | primary | primary | ✓ | Horizontal shoulder abduction/extension. Correct. |
| rhomboids | secondary | secondary | ✓ | Assist scapular retraction as the arms travel back. Correct. |
| trapezius | secondary | secondary | ✓ | Mid traps assist scapular retraction. Correct. |
| infraspinatus / teres_minor | (absent) | borderline secondary | (—) | The external rotators assist a rear-delt fly (horizontal abduction couples with external rotation in many setups). Out of prototype taxonomy; omission acceptable. MINOR, noted for catalogue. |

#### `reverse_pec_deck`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| posterior_deltoid | primary | primary | ✓ | Correct. |
| rhomboids | secondary | secondary | ✓ | Correct. |
| trapezius | secondary | secondary | ✓ | Correct. |

#### `dumbbell_reverse_fly`
| Muscle | Encoded | Independent call | Match | Notes |
|---|---|---|---|---|
| posterior_deltoid | primary | primary | ✓ | Correct. |
| rhomboids | secondary | secondary | ✓ | Correct. |
| trapezius | secondary | secondary | ✓ | Correct. |

**Tally:** 74 encoded rows. 74/74 roles match my independent call. 0 wrong
roles, 0 spurious muscles, 0 missing prime movers. 3 `pelland_2026_table1` rows
— all 3 verified as exact, correctly-classified matches. The discrepancies
below are all rationale-honesty (≈) or borderline-omission (—) items.

---

## Reasoning — contested derivations

**Pec in the pullover (rows marked ≈).** The resisted action of a pullover is
shoulder extension from a deeply flexed position. The lat is unambiguously the
prime mover *of that action*. The pec's sternocostal fibres extend a flexed
humerus only over the first part of the arc (from full flexion toward ~90°);
past that they have no extension moment. So anatomically "secondary" is the
correct role. The honesty issue is the rationale: dumbbell-pullover EMG
repeatedly shows the *pec* as the higher-activation muscle (~50% vs ~23% MVIC
for the lat in dynamic dumbbell pullovers). The role taxonomy here is "prime
mover of the resisted joint action", not "highest-EMG muscle", so the
*classification* survives — but a reader will reasonably read "secondary" as
"smaller contributor", which the EMG contradicts. The rationale should name
this tension instead of asserting a clean split. This is the single most
important honesty fix; it is still MINOR because the `set_credit` (0.5) is the
right number under the map's own stated methodology.

**Rear delt in rows (rows marked ≈).** In a horizontal row the rear delt
performs horizontal shoulder extension/abduction — the same action it is a
*prime mover* of in a reverse fly. In a row, however, the dominant resisted
actions are shoulder extension (lat) and scapular retraction (traps/rhomboids),
and the rear delt assists rather than leads. "Secondary" is the right call.
ADR-011 itself names "is the rear delt secondary or stabilising in a given
row?" as the canonical debatable case — yet the row rationales state
"secondary" with no hedge. Honest rationale would acknowledge the call is a
judgement, as the straight-arm-pulldown pec rationale ("a minor secondary
contributor") correctly does. MINOR.

**Teres major uniformly as "the lat's helper".** Correct for the
shoulder-extension exercises (pullovers, pulldowns, vertical pulls). For the
rows the teres major still assists shoulder extension, so "secondary" remains
correct — but the rationale "shares the lat's shoulder-extension line of pull"
is copied verbatim into the row rows, where the row's *other* prime action
(scapular retraction) is not a teres-major action at all. The role is right;
the rationale is just a touch lazy. MINOR.

**`barbell_row` / `biceps_brachii` basis.** Pelland Table 1 lists
`bent_over_barbell_row` and `supine_grip_bent_over_row` as indirect biceps
work. `barbell_row` is the same movement under a different key string. The
module conservatively used `basis="biomechanical"` because the key strings do
not match exactly — which is the *correct, honest* call given ADR-011's rule
that `pelland_2026_table1` requires an *exact* `(exercise, muscle)` match. Not
an error. Flagged only so the catalogue build-out reconciles exercise-key
strings with Pelland's so this corroboration can be claimed.

---

## Concerns & discrepancies (ranked)

1. **MINOR — pullover pec rationale overstates a clean split.** The dumbbell/
   cable pullover `pectoralis_major` rationales present "secondary" as
   uncontested, but dumbbell-pullover EMG shows the pec as the dominant
   agonist. Role is defensible; rationale should disclose the tension.
2. **MINOR — rear-delt-in-row rationale is unhedged on an ADR-flagged
   debatable call.** ADR-011 explicitly cites this as a genuinely debatable
   primary-vs-secondary call; the `seated_cable_row` / `barbell_row`
   `posterior_deltoid` rationales read as settled. Add a one-clause hedge.
3. **MINOR — teres-major rationale copy-pasted into row rows.** Says "shares
   the lat's shoulder-extension line of pull" in rows whose co-prime action is
   scapular retraction. Role correct; wording imprecise.
4. **MINOR — supraspinatus / external rotators omitted from raises and flies.**
   Genuinely involved synergists, but outside the prototype's lat/delt key set
   and the layer has no encoded keys for them. Acceptable omission; flag for
   the full catalogue build-out so they are not forgotten.
5. **MINOR — serratus anterior omitted from the pullover.** Plausibly involved
   (scapular control at the stretched position); debatable whether dynamically
   trained or only stabilising. Acceptable to omit; a `stabilizer` row would
   arguably be *more* honest documentation than silence, consistent with the
   module's own stated philosophy on the erector-spinae rows.
6. **MINOR — `barbell_row` biceps could carry Pelland corroboration after a
   key-string reconciliation.** Not an error today (exact-match rule correctly
   applied); a catalogue-time follow-up.

No MATERIAL or MODERATE findings. No wrong role, no missing prime mover, no
spurious muscle, no mis-cited Pelland basis. Structural checks all pass:
`set_credit` is a derived `@property` (no row hard-codes a number); every row
is `outcomes=("hypertrophy","strength")`; `basis` is `biomechanical` on all
non-Pelland rows; the registry routes involvement only through
`_INVOLVEMENT_INDEX` (never `_EMPHASIS_INDEX` / `_MECHANISTIC_INDEX`);
`set_credit()` returns `None` (not a silent `0.0`) for unknown pairs; 244/244
tests pass.

---

## Recommendations

1. **Reword the pullover `pectoralis_major` rationales** (dumbbell + cable) to
   disclose that EMG shows the pec as the dominant agonist, and to state
   explicitly that the "secondary" classification reflects "prime mover of the
   resisted joint action (shoulder extension)", not relative contribution. This
   is the one change worth making before cataloguing the wider library, because
   the same pattern (a high-EMG assistant that is not the prime mover of the
   *resisted action*) will recur.
2. **Add a one-clause hedge** to the `posterior_deltoid` rationale in
   `seated_cable_row` and `barbell_row` — e.g. "the primary-vs-secondary call
   here is a genuine judgement; encoded secondary because shoulder extension
   and scapular retraction are the dominant resisted actions." This aligns the
   rationale with ADR-011's own acknowledgement.
3. **De-duplicate the teres-major rationale** in the row rows so it does not
   imply teres major contributes to scapular retraction.
4. **Record supraspinatus / external rotators / serratus anterior as
   catalogue-build-out TODOs** (BACKLOG.md) so they are picked up when the
   exercise library expands beyond lat/delt and the muscle taxonomy grows the
   keys to express them. Consider a `stabilizer` serratus row for the pullover
   as honest documentation.
5. **At catalogue time, reconcile exercise-key strings with Pelland Table 1**
   (`barbell_row` vs `bent_over_barbell_row`, `overhead_press` vs
   `shoulder_press`) so legitimate Pelland corroboration can be claimed via
   `basis="pelland_2026_table1"` instead of conservatively defaulting to
   `biomechanical`.

The map is fit to proceed. The recommended changes are wording and
documentation only — no role reassignment, no row addition or removal is
required for correctness.
