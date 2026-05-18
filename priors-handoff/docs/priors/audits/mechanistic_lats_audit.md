# Mechanistic prior audit — latissimus dorsi

**Module audited:** `app/priors/mechanistic/lats.py` (ADR-010 prototype, 17 `MechanisticEmphasis` entries — 7 whole-muscle, 5 upper_fibres, 5 lower_fibres)
**Date:** 2026-05-18
**Auditor:** priors-mechanistic-auditor

---

## Sources accessed

Biomechanics re-derived independently; the following corroborated specific facts (no EMG-amplitude study used as evidence — the tier excludes them, and EMG under-reads long lengths):

- Latissimus dorsi anatomy (origin: T7–T12 spinous processes, thoracolumbar fascia, iliac crest, inferior 3–4 ribs; insertion: floor of intertubercular sulcus of the humerus; upper/scapular fibres run near-horizontal, iliac/costal fibres near-vertical) — Kenhub, https://www.kenhub.com/en/library/anatomy/latissimus-dorsi-muscle ; StatPearls, https://www.ncbi.nlm.nih.gov/books/NBK448120/
- Pullover force-vs-angle: peak isometric force at **45–90° shoulder flexion**, dropping significantly toward the **180° fully-overhead position** — Differences Between Pullover and Pulldown Exercises on Maximal Isometric Force, PMC9362894, https://pmc.ncbi.nlm.nih.gov/articles/PMC9362894/
- Barbell row resistance curve (hardest at the bottom for the bar's vertical load; arm near-parallel to gravity at the bottom; hardest *relative to leverage* near the contracted top) — outlift.com strength-curve and barbell-row guides, https://outlift.com/strength-curves-hypertrophy/ , https://outlift.com/barbell-row/
- Cable straight-arm pulldown / cable pullover constant-tension profile (cable holds load into the overhead stretched start) — Gravitus, https://gravitus.com/guides/exercises/straight-arm-pulldown/ ; SET FOR SET, https://www.setforset.com/blogs/news/lat-pullover/
- Lat training at different muscle lengths (straight-arm pulldown hardest near the lat's strong position; pullover hardest while stretched) — outlift.com, https://outlift.com/strength-curves-hypertrophy/

---

## Verdict

**MATERIAL REASONING ERRORS.**

The structural walling-off, the bucket mapping, the `grounded_in` provenance, the confidence discipline, and the *aggregate* whole-muscle ordering (pullover-family > vertical pulls > barbell row) are all sound, and the regional tier is honestly tagged. But the module contains one **material loaded-length error that recurs across three entries**: it classifies the free-weight `dumbbell_pullover` as `loaded_length="long"` / emphasis 1.0, and its own rationale even names the position where the load peaks — "upper arm horizontal behind the head" — yet then mislabels that position as "near-maximal length." With a *vertical dumbbell load*, peak shoulder torque is at roughly 90° shoulder flexion (upper arm horizontal); torque falls toward the deep-overhead stretch (the dumbbell's moment arm collapses as the arm approaches vertical-overhead). The lat at ~90° shoulder flexion is at **mid-to-moderately-long** length, not near-maximal. Corroborated directly: PMC9362894 measured pullover force highest at 45–90° and significantly *lower* at 180°. The honest call for the free-weight pullover is `mid` (0.70) — defensibly "mid, long-leaning," but not `long`/1.0. The same error propagates to `dumbbell_pullover` under `upper_fibres` (entry 8) and is the load-profile premise the `lower_fibres` pullover entries lean on. The *cable* pullover and *cable* straight-arm pulldown are correctly `long`, because a cable (unlike a vertical dumbbell) does hold tension into the overhead stretched start — so the module gets the free-weight-vs-cable distinction right everywhere except the dumbbell pullover itself, where it contradicts its own stated rule (docstring lines 28–31 explicitly warn that a dumbbell pullover is "hardest with the arm overhead" — that premise is the error). This is a wrong loaded-length call and a wrong bucket, so MATERIAL rather than MINOR; it is a fixable misclassification, not an unsupportable distinction, so not OVERREACH.

---

## Entry-by-entry verification

### Whole-muscle tier (region=None, confidence="low")

| Exercise | Encoded | Independent call | Match? | Notes |
|---|---|---|---|---|
| dumbbell_pullover | long / 1.0 | **mid (long-leaning) / 0.70** | **NO — MATERIAL** | Vertical dumbbell load: peak torque at ~90° shoulder flexion (upper arm horizontal), NOT at the deep-overhead stretch. PMC9362894: force highest 45–90°, drops to 180°. Rationale's own geometry ("upper arm is horizontal") is a mid-length position; "near-maximal length" is the error. |
| cable_pullover | long / 1.0 | long / 1.0 | YES | Cable holds tension into the fully-overhead stretched start; loaded while genuinely long. Rationale correct. |
| straight_arm_pulldown | long / 1.0 | long / 1.0 | YES | Long lever + high pulley keeps a large shoulder moment at the overhead start; cable maintains tension there. Loaded while long. Correct. |
| pull_up | mid / 0.70 | mid / 0.70 | YES | Vertical bodyweight pull; shoulder moment peaks ~upper-arm-horizontal at mid length. The rationale's note that the dead-hang start *cannot* be unloaded (genuine, unlike a pulldown) is a fair caveat and correctly does not change the bucket. |
| lat_pulldown | mid / 0.70 | mid / 0.70 | YES | Vertical cable pull; hardest mid-range; overhead start can be partly unloaded by relaxing into the top. Correct. |
| seated_cable_row | mid / 0.70 | mid / 0.70 | YES | Horizontal pull; constant cable tension does load a somewhat-lengthened start, but hardest leverage sits mid-to-short. `mid` is the honest call. Correct. |
| barbell_row | short / 0.50 | short / 0.50 | YES | Torso horizontal, vertical gravity load: peak torque *relative to leverage* is near the contracted top (shoulder extended, lat short); the lengthened bottom has the arm near-parallel to gravity and carries little shoulder moment. Correct. |

### Upper-fibres tier (region="upper_fibres", confidence="speculative")

| Exercise | Encoded | Independent call (as speculative) | Match? | Notes |
|---|---|---|---|---|
| dumbbell_pullover | long / 1.0 | **mid / 0.70** | **NO — MATERIAL** | Inherits the whole-muscle dumbbell-pullover error. The regional split itself is defensibly speculative, but the loaded-length value must match the corrected whole-muscle call. |
| cable_pullover | long / 1.0 | long / 1.0 (as speculative) | YES | Overhead humeral elevation under cable tension; upper (humerus-governed) fibres loaded long. Honest as speculative. |
| straight_arm_pulldown | long / 1.0 | long / 1.0 (as speculative) | YES | Straight-arm overhead loading of the humerus-governed upper fibres. Honest as speculative. |
| pull_up | mid / 0.70 | mid / 0.70 (as speculative) | YES | Hardest mid-range; upper fibres at mid length. Honest as speculative. |
| lat_pulldown | mid / 0.70 | mid / 0.70 (as speculative) | YES | As pull-up. Honest as speculative. |

### Lower-fibres tier (region="lower_fibres", confidence="speculative")

| Exercise | Encoded | Independent call (as speculative) | Match? | Notes |
|---|---|---|---|---|
| pull_up | long / 1.0 | long / 1.0 (as speculative) | YES | Hanging from a fixed bar, the pelvis is the far anchor on the iliac/thoracolumbar fibre line; that long vertical line is loaded under full bodyweight. The most internally-coherent of the regional entries — see Reasoning checks. |
| lat_pulldown | mid / 0.70 | mid / 0.70 (as speculative) | YES | Same vertical line, but seated with the pelvis fixed to a pad — the hanging long line is not reproduced. `mid` is the honest contrast with pull-up. |
| straight_arm_pulldown | mid / 0.70 | mid / 0.70 (as speculative) | YES | Loads via humeral elevation; the iliac-fibre length is governed partly by trunk/pelvis, which this does not load at length. Honest as speculative. |
| dumbbell_pullover | mid / 0.70 | mid / 0.70 (as speculative) | YES — coincidentally correct | The *value* lands right, but for a partly-wrong reason: the rationale frames it as "strong upper-fibre stretch loader, but lower fibres at mid" — yet the whole-muscle/upper dumbbell-pullover call is itself wrong (should be mid). The lower-fibre `mid` survives the correction, but the rationale's contrast against an overstated upper-fibre `long` should be reworded once the upper entry is fixed. |
| cable_pullover | mid / 0.70 | mid / 0.70 (as speculative) | YES | Cable pullover genuinely loads the upper fibres long but not the pelvis-anchored lower line; `mid` is honest. |

**Tally:** 13 of 17 entries match. 2 hard mismatches (`dumbbell_pullover` whole-muscle and upper_fibres). 2 entries (`dumbbell_pullover` lower_fibres, and indirectly the lower-fibre rationales) carry a correct value resting on the flawed pullover premise and need rationale rewording, not a value change.

---

## Reasoning checks (contested entries shown)

### Dumbbell pullover — the material error, derived from scratch

The lat crosses the shoulder; its length at the shoulder is set by humeral elevation — longest with the arm fully overhead (deep flexion), shortest with the arm extended behind the body. Loaded length is "is the muscle loaded *while* long," set by where the **external resistance moment is largest relative to the muscle's leverage**.

A dumbbell is a *vertical* load. Its shoulder moment arm = (horizontal distance from shoulder axis to the dumbbell). Lying supine, with the arm rotating in a vertical arc overhead:
- Arm pointing at the ceiling (~0° flexion from the torso line, dumbbell directly above the shoulder): horizontal moment arm ≈ 0 → near-zero shoulder torque.
- Arm horizontal, behind the head (~90° flexion): horizontal moment arm = full arm length → **peak shoulder torque**.
- Arm continuing toward the floor behind the head (approaching the deepest stretch, ~150–180°): the dumbbell swings back toward being under/level with the shoulder axis again and the moment arm *shrinks* → torque falls off.

So the free-weight pullover is loaded HARDEST at ~90° shoulder flexion. At 90° flexion the lat is *moderately* lengthened — clearly longer than mid-neutral, but well short of the deep-overhead maximal stretch. PMC9362894 measured exactly this: pullover force was highest at 45–90° and dropped significantly toward 180°. The honest classification is **`mid`** (a long-leaning mid, but the buckets are coarse and `mid` is the correct one), emphasis **0.70**.

The module's rationale is internally self-contradicting: it correctly states the load "peaks when the upper arm is horizontal behind the head" and then calls that "near-maximal length." Upper-arm-horizontal is ~90° flexion — not near-maximal. The docstring (lines 28–31) makes the same slip its headline rule ("a dumbbell pullover is hardest with the arm overhead — at the lat's longest length"). "Hardest with the arm overhead" is true only loosely; "at the lat's longest length" is false for a vertical dumbbell load. The deep-overhead position is the *longest* length but is *unloaded* — exactly the trap ADR-010 §2 and the module docstring warn against ("a range that passes through a stretch vs. a position that is LOADED while stretched"). The module applies that rule correctly to the lat pulldown and incorrectly to the dumbbell pullover.

Note this does **not** collapse the headline pattern: cable pullover and cable straight-arm pulldown remain genuine `long`/1.0 (a cable can hold tension into the overhead stretch where a vertical dumbbell cannot), so stretch-loaded work still tops the ranking. Only the *dumbbell* pullover is misranked — it should sit with the pull-ups/pulldowns at `mid`, not above them.

### Pull-up lower_fibres = long — defensible AS speculative

Re-derived: the iliac/thoracolumbar fibres run near-vertical from the pelvis/lower spine to the humeral insertion. Their length is governed by humeral elevation AND by the distance from the pelvis to the shoulder (trunk side-flexion / pelvic position). In a dead hang from a fixed bar the pelvis hangs as a free far-anchor under full bodyweight, putting that long vertical hand-to-pelvis line under load at length in a way a benched or pad-seated movement does not. As a *speculative* fibre-line-of-pull argument this is coherent and the most internally-consistent of the regional entries; `confidence="speculative"` is the honest tag and the rationale says "SPECULATIVE" plainly. It is not a `SOUND` claim and is not asserted as one — correct discipline. No change needed.

### Barbell row = short — confirmed

The bar is a vertical load; the lat's shoulder moment arm is largest when the upper arm is horizontal (bar pulled to the torso, top of the row) and smallest at the bottom (arm hanging near-parallel to gravity). The lat at the top is shoulder-extended → short. So the row is loaded hardest while short. The independent call matches `short`/0.50. The rationale is accurate.

---

## Confidence, bucket mapping, grounded_in, structural checks

- **Bucket mapping** — every entry obeys long→1.0 / mid→0.70 / short→0.50 uniformly; `_LONG/_MID/_SHORT` constants are used throughout, no off-bucket values. The `dumbbell_pullover` errors are *loaded_length* misclassifications; the *mapping* from the (wrong) class to the value is itself consistent. PASS.
- **`grounded_in`** — all four cited modules (`maeo_2023`, `maeo_2021`, `kassiano_2023`, `wolf_2023`) genuinely establish a lengthened-position → growth result (overhead triceps > pushdown; seated/hip-flexed hamstrings > prone; lengthened-ROM calf raise > shortened; ROM meta-analysis with a long-length-partial trend). They support the lengthened-position *principle* the prior leans on. PASS. Minor honesty credit: the module docstring correctly flags Wolf's wide lengthened-partial CI (−0.81 to +0.16) as the reason confidence is capped — it does not oversell the evidence.
- **Confidence discipline** — whole-muscle entries all `low`; regional entries all `speculative`. This matches the auditor rule exactly: a sound whole-muscle loaded-length call is `low`; the contested within-muscle upper/lower split is `speculative`. No over- or under-tagging. The `__main__` asserts pin this. PASS. (The `dumbbell_pullover` error is a wrong *class*, not a confidence breach — `low` would still be the right cap for a correct `mid` call.)
- **Rationale honesty** — every regional rationale opens "SPECULATIVE." and the docstring + `GUIDANCE_FOR_OPTIMIZER` repeatedly say the regional split is fibre-line-of-pull reasoning, not measured fact, and cite Varovic 2025's trivial within-muscle regional finding as a self-caution. Honest. The one dishonest-by-overstatement spot is the whole-muscle `dumbbell_pullover` rationale ("loaded HARDEST at near-maximal length" / "The canonical lengthened-loaded lat exercise") — it asserts more length than the vertical-load mechanics support. MATERIAL, captured above.
- **Structural walling-off** — verified by running the module and registry. `app/priors/mechanistic/lats.py` exports `MechanisticEmphasis` objects only (`MECHANISTIC_EMPHASIS`); no `ExerciseEmphasis`, no `EffectEstimate`, no `EMPHASIS_ESTIMATES` attribute. `registry.py` routes all 17 lat entries through `_MECHANISTIC_INDEX` (confirmed: 17 lat keys in `_MECHANISTIC_INDEX`, **0** in `_EMPHASIS_INDEX`); `selection_emphasis("latissimus_dorsi")` returns tier `"mechanistic"`. `combine_emphasis_estimates()` is typed to `ExerciseEmphasis` so a mechanistic prior is structurally unpoolable with measured data. `MechanisticEmphasis.__post_init__` enforces the `low`/`speculative` cap and a non-empty `grounded_in`. Full suite: **228 passed**. PASS.

---

## Concerns & discrepancies (ranked)

1. **MATERIAL — `dumbbell_pullover` whole-muscle is `long`/1.0; should be `mid`/0.70.** A vertical dumbbell load peaks at ~90° shoulder flexion (upper arm horizontal), not at the deep-overhead stretch; the lat there is mid-to-moderately-long, not near-maximal. The rationale contradicts itself (names the 90° position, then calls it "near-maximal length") and the docstring's headline rule (lines 28–31) embeds the same error. Corroborated by PMC9362894 (force highest 45–90°, falls to 180°). This misranks the dumbbell pullover above the cable pullover/straight-arm pulldown when it should sit with the vertical pulls.
2. **MATERIAL — `dumbbell_pullover` / `upper_fibres` is `long`/1.0; should be `mid`/0.70.** Same root cause; the regional value must track the corrected whole-muscle loaded-length call.
3. **MODERATE — lower-fibre `dumbbell_pullover` and `cable_pullover` rationales reference an overstated upper-fibre `long` premise.** The lower-fibre `mid` *values* survive the correction, but the rationale phrasing ("strong upper-fibre stretch loader, but…") leans on the wrong upper-fibre classification for `dumbbell_pullover` and should be reworded once entry 2 is fixed (cable_pullover's upper-fibre `long` is correct, so its lower-fibre rationale is fine as-is).
4. **MINOR — module docstring lines 28–31 state the general rule using the dumbbell pullover as the worked example of "loaded while stretched."** Because that example is itself the misclassification, the teaching example actively reinforces the error. Swap the example to the *cable* pullover / straight-arm pulldown (genuinely loaded long) and use the dumbbell pullover as the *counter*-example (passes through the stretch but is hardest at mid).
5. **MINOR — no `barbell_row` cable counterpart, and `seated_cable_row` is the only horizontal pull.** Not an error (the docstring explicitly declines to encode horizontal-pull regional behaviour as "the murkiest case"), but the whole-muscle horizontal-pull coverage is thin — worth a note for the deltoids-next generalisation: a chest-supported / cable row that holds the stretched start would plausibly be `mid` for a different reason than the barbell row's `short`, and the single `seated_cable_row` entry slightly under-represents that family.

---

## Recommendations

1. **Reclassify `dumbbell_pullover` whole-muscle** to `loaded_length="mid"`, `emphasis=_MID` (0.70). Rewrite the rationale to state the mechanics honestly: a vertical dumbbell load peaks at ~90° shoulder flexion (upper arm horizontal — moderately long), and the deep-overhead position, though the lat's longest, is nearly unloaded because the dumbbell's moment arm collapses there. Cite the free-weight-vs-cable distinction explicitly.
2. **Reclassify `dumbbell_pullover` / `upper_fibres`** to `mid`/0.70 to match.
3. **Reword the lower-fibre `dumbbell_pullover` rationale** so its contrast no longer rests on an overstated upper-fibre `long` (the value stays `mid`/0.70).
4. **Fix the module docstring (lines 28–31):** use the *cable* pullover / straight-arm pulldown as the worked "loaded while stretched" example, and demote the dumbbell pullover to the counter-example (range passes through the stretch but is hardest at mid). This makes the module's teaching rule consistent with its own entries.
5. **Keep everything else as-is.** The cable pullover, straight-arm pulldown, both vertical pulls, the cable row, the barbell row, all five `lower_fibres` *values*, four of five `upper_fibres` entries, the bucket mapping, the `grounded_in` set, the confidence caps, and the structural walling-off are all sound. The whole-muscle tier remains a defensible deliverable after fix #1; the regional tier remains honestly tagged as the speculative edge and should be retained as ADR-010 intends.
6. After the fixes, re-run `python3 -m app.priors.mechanistic.lats` and the suite — the `__main__` asserts and the 228-test suite should still pass (the changes are value/text only, no structural change).

---

## Orchestrator review (2026-05-18) — material finding REJECTED

The orchestrator independently re-examined the headline MATERIAL finding (that
`dumbbell_pullover` should be reclassified `long` → `mid`) and **rejects it**.
The module's `dumbbell_pullover = loaded_length="long"` is correct; no entry,
rationale or docstring line is changed. Recommendations 1–4 are NOT applied.

**Why the finding is wrong.** The audit conflated two distinct quantities:

- *External resistance load* — where the exercise is hardest, i.e. where the
  greatest muscle force is demanded. For a vertical free-weight load this peaks
  where the limb's moment arm is longest. In a supine dumbbell pullover the
  moment arm is longest when the upper arm is horizontal — arm in line with the
  torso, behind the head — which is the lat's **most lengthened** position.
  `loaded_length` is defined as exactly this quantity (ADR-010 step 2: muscle
  length "at the HARDEST point of the resistance curve"). So the pullover is
  loaded `long`.
- *Muscle force-output capacity* — which genuinely **does** fall toward long
  muscle length (the length-tension relationship). The audit's cited source
  describes force/capacity dropping toward the stretched end and read that as
  "not loaded long." But a muscle being weakest where the load is heaviest is
  not a reason to downgrade — it is the entire mechanism of stretch-mediated
  hypertrophy, and precisely what the lengthened-position prior is built to
  reward.

The audit's own physics was internally inconsistent: it placed the load peak
at "~90° shoulder flexion (upper arm horizontal)", but at 90° shoulder flexion
the upper arm is **vertical** (dumbbell stacked over the shoulder), where the
moment arm — and the load — is near **zero**. The module's rationale ("the
moment peaks when the upper arm is horizontal behind the head … the lat is
loaded hardest at near-maximal length") is the correct reading.

**Independent corroboration.** Standard biomechanical descriptions of the
dumbbell pullover state the exercise is hardest in the stretched position —
"the moment arm is longest exactly when the muscles are weakest [stretched]";
"resistance is greatest … precisely when the muscles are in their weakest
stretched position" (bodybuilding-wizard.com; powerliftingtechnique.com,
reviewed 2026-05-18).

**Net verdict (orchestrator):** the MATERIAL finding does not survive review.
With it set aside, every remaining check in this audit passed — the lats
module is **SOUND** and is left unchanged. This disagreement is itself a
useful outcome: the mechanistic-audit gate works in both directions, and an
audit's verdict is reviewed, not rubber-stamped. The `loaded_length` vs
muscle-force-capacity distinction has been noted for future
priors-mechanistic-auditor runs.
