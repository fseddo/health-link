# Mechanistic prior audit — deltoids

**Module audited:** `app/priors/mechanistic/deltoids.py`
**Date:** 2026-05-18
**Auditor:** priors-mechanistic-auditor

This is an independent biomechanics audit of an ADR-010 mechanistic
exercise-selection prior. There is no paper to check against — the loaded-length
classification of every entry was re-derived from scratch (joint angles,
muscle length-vs-angle relationships, resistance profiles) and compared to the
module. EMG-activation studies were excluded as evidence, by design.

---

## Sources accessed

Biomechanics corroboration (not used as EMG evidence — used for moment-arm /
resistance-profile / joint-angle facts):

- Chris Beardsley, "Deltoids" — anterior-delt internal moment arm rises with
  shoulder flexion; shoulder-flexion training is best done substantially above
  shoulder height. https://www.patreon.com/posts/deltoids-61681834
- Coelho et al., "Moment arms of the deltoid… for movements with high range of
  motion: a cadaveric study." https://pubmed.ncbi.nlm.nih.gov/35671631/
- "The moment arms of the muscles spanning the glenohumeral joint" (PMC6284439).
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6284439/
- Frontiers in Physiology 2025, "Dumbbell versus cable lateral raises for
  lateral deltoid hypertrophy" — explicitly states the dumbbell lateral raise
  has an ascending resistance profile with reduced torque in the lengthened
  position, the cable variant a descending profile loading the lengthened
  position; the lateral delt reaches its descending limb when the humerus is
  parallel to the torso. https://pmc.ncbi.nlm.nih.gov/articles/PMC12277279/
- "Understanding and Overcoming the Sticking Point in Resistance Exercise"
  (PMC4887540) — press sticking points sit out of phase with the load's peak
  moment. https://pmc.ncbi.nlm.nih.gov/articles/PMC4887540/
- BarBend, "How to Do the Reverse Pec Deck"; Inspire US, "Pec Deck Machine Rear
  Delt Fly" — reverse pec deck delivers a fixed-path, comparatively even tension
  vs the dumbbell reverse fly's tension loss at the bottom.
  https://barbend.com/reverse-pec-deck/
- "The best exercise for shoulders with dumbbells looks like a mistake" /
  upright-row biomechanics — resistance on a vertical-load upright row peaks
  around 90° of humeral elevation, strength curve peaks ~70°.
  https://www.gxmmat.us/blogs/daily-news/the-best-exercise-for-shoulders-with-dumbbells-looks-like-a-mistake

---

## Verdict

**MINOR REASONING GAPS.**

Every one of the nine entries' loaded-length classifications is biomechanically
defensible and I independently arrive at the same long/mid/short call for all
nine. The bucket mapping is uniform and correct (long→1.0, mid→0.70, short→0.50,
no off-bucket values). The structural walling-off is correct: the module exports
`MechanisticEmphasis` only, registry routes it through `_MECHANISTIC_INDEX` with
a one-entry-per-key guard, it can never be pooled with measured emphasis, the
module runs, and 228 tests pass. The confidence discipline is sound: `low` (not
`speculative`) is the right call — the three deltoid heads are uncontested
functional sub-targets, unlike the lats' contested upper/lower fibre split.

What holds this back from `SOUND` is **not** a wrong classification but two
honesty/wording gaps, both on the highest-emphasis (1.0) entries:

1. The `incline_bench_press` rationale states the humerus "travels behind the
   plane of the torso" and the anterior delt is "stretched" there. For a
   correctly-performed incline press the humerus reaches roughly the torso
   plane / slightly forward of it, not appreciably behind it — the elbows are
   cued ~45° from the torso for shoulder safety, and going behind the bench
   plane is the impingement fault. The anterior delt at the bottom of an
   incline press is *long, but not maximally stretched*. The classification
   `long` is still the best of the three buckets and survives, but the
   rationale overstates the depth of stretch and should be softened. This is
   the single most important finding.

2. The `cable_lateral_raise` and `cable_rear_delt_fly` rationales describe the
   stretched-loading cable setup as if it were the definitional form of the
   exercise. It is not — it is a *specific* setup. The lateral entry already
   carries a parenthetical caveat ("Assumes the cable variant set up to load
   the bottom, not a token cable swap"); the rear-delt entry makes the same
   assumption but states it as fact with no caveat. The two sibling 1.0 cable
   entries should be caveated consistently.

None of this requires dropping or re-bucketing an entry. The fixes are rationale
edits.

---

## Entry-by-entry verification

| Exercise / region | Encoded | Independent call | Match? | Notes |
|---|---|---|---|---|
| incline_bench_press / anterior | long, 1.00 | long, 1.00 | YES (classification) | Rationale overstates "behind the plane of the torso" — see Finding 1. Bucket correct. |
| overhead_press / anterior | mid, 0.70 | mid, 0.70 | YES | Hardest near the bottom, humerus ~shoulder height, anterior delt mid; does not go behind torso. Sound. |
| dumbbell_front_raise / anterior | mid, 0.70 | mid, 0.70 | YES | Vertical dumbbell load peaks at arm-horizontal; anterior delt mid there; lengthened (arm-behind) position never entered. Sound. |
| cable_lateral_raise / lateral | long, 1.00 | long, 1.00 | YES | Correct for the across/behind-body cable setup. Caveat present. See Finding 2. |
| upright_row / lateral | mid, 0.70 | mid, 0.70 | YES | Vertical-load resistance peaks ~90° humeral elevation; lateral delt mid across the hardest arc. Sound. |
| dumbbell_lateral_raise / lateral | short, 0.50 | short, 0.50 | YES | Vertical load peaks at arm-horizontal (top), lateral delt short/contracted; near-zero moment at the stretched bottom. Independently corroborated by the Frontiers 2025 resistance-profile description. |
| cable_rear_delt_fly / posterior | long, 1.00 | long, 1.00 | YES (classification) | Correct for the cross-body cable setup. Rationale states the setup as fact with no caveat — see Finding 2. |
| reverse_pec_deck / posterior | mid, 0.70 | mid, 0.70 | YES | Fixed-path machine, comparatively even tension; loaded around mid length; the across-body start is loaded but not maximally stretched. Sound. |
| dumbbell_reverse_fly / posterior | short, 0.50 | short, 0.50 | YES | Bent-over, vertical load peaks at arm-wide (top), posterior delt short; stretched across-body bottom carries almost no load. Sound. |

All nine classifications match. No bucket-mapping errors. No confidence-cap
breaches. `grounded_in` is identical across all entries and correct (see below).

---

## Reasoning checks (contested / highest-stakes entries)

### incline_bench_press — anterior delt (the 1.0 anchor for the anterior head)

What lengthens the anterior delt: shoulder extension — the upper arm drawn
*behind* the frontal plane of the torso. The module's involvement gate is
correct (incline press loads shoulder flexion, the anterior delt's prime
action).

Loaded length at the hardest point: an incline press loaded by vertical gravity
is hardest near the bottom, where the external moment on the shoulder is
largest. At that bottom position the humerus is at roughly torso-plane to
slightly-forward — cued ~45° from the torso. It is *not* drawn meaningfully
behind the torso; doing so is the impingement fault, not the target position. So
the anterior delt at the bottom of an incline press is at a *long-ish* length —
longer than at the top, longer than the front-raise's arm-horizontal position —
but it is not at the deep stretch the rationale describes. Of the three buckets
(long/mid/short), `long` is the correct relative call: among the three anterior
exercises encoded, the incline press loads the anterior delt at the longest
length under the heaviest load, so it earns the 1.0 bucket. The classification
is right; the rationale's specific claim ("travels behind the plane of the
torso") is not, and a knowledgeable reader will catch it. Soften the rationale,
keep the bucket.

A second-order point worth noting (not a defect): unlike the lat module's
`pull_up` rationale, which explicitly flags that the coarse bucket understates
one feature, the anterior-delt head has *no* exercise that genuinely loads the
deep behind-the-body stretch. There is no "true long" anterior-delt exercise in
the common-exercise set — the incline press is simply the best available. The
1.0 is therefore a *relative-within-head* maximum, exactly as ADR-010 and the
`MechanisticEmphasis` docstring intend ("RELATIVE within a muscle"). This is
fine, but it makes Finding 1 more important: the rationale should not imply an
absolute deep stretch the movement does not deliver.

### cable_lateral_raise / cable_rear_delt_fly — the cable 1.0 entries

Both are correct *for the across/behind-body cable setup* the module names. The
Frontiers 2025 lateral-raise study independently confirms the mechanism the
module relies on: a cable can be arranged to give a descending resistance
profile that loads the lateral delt in the lengthened position, whereas the
dumbbell's ascending profile loses torque there. The same logic transfers to the
posterior delt with a cross-body cable rear fly. So the classifications stand.

The honesty gap is that "cable lateral raise" and "cable rear delt fly" are not
single, fixed movements — a chest-height straight cross-body cable rear fly
loads the stretch; a poorly-set-up cable swap may not. The lateral entry says
this plainly ("Assumes the cable variant set up to load the bottom, not a token
cable swap"). The posterior entry does not — it asserts "the cable keeps tension
there" as established fact. The two sibling 1.0 cable entries should carry the
*same* explicit setup caveat, or a knowledgeable reader will reasonably ask why
one is hedged and the other is not.

Note for context (not a defect): a real cable-vs-dumbbell lateral-raise trial
*does* now exist (Frontiers/PMC12277279, 2025) and found the two
*equipment-equivalent* for lateral-delt hypertrophy. Like the
Coleman/Larsen dumbbell-vs-cable delt study the module's docstring already
discusses, this is an equipment-equivalence question, not a head-to-head
exercise-selection trial, so it correctly does not promote the deltoids out of
`literature-blocked` and does not supersede this mechanistic prior. If anything
it is mild *evidence against* the prior's central premise — that the
lengthened-loaded cable variant grows the muscle more — and a future revision
may want to acknowledge it in the docstring. It is not an audit defect today:
ADR-010 explicitly frames these as soft priors carrying real magnitude
uncertainty, and the `low` confidence cap already encodes that.

### Confidence discipline — is `low` right, or should anything be `speculative`?

`low` is correct for all nine. `speculative` is reserved (per the auditor brief
and the lats precedent) for genuinely *contested* within-muscle distinctions —
the lats' upper/lower fibre split, which rests on fibre-line-of-pull reasoning
and which Varovic 2025 actively cautions against. The three deltoid heads are
not that: they are anatomically distinct muscles-within-a-muscle with separate
prime actions, separate innervation patterns and an uncontested functional
split. Encoding the heads as regions is established anatomy, not a speculative
guess. The only soft inference is the loaded-length→emphasis weighting, which is
the *same* soft inference the lats whole-muscle entries make at `low`. So `low`
is right; nothing here is under- or over-tagged. The module's docstring argues
this explicitly and correctly.

### grounded_in

All nine entries cite the identical tuple `(maeo_2023, maeo_2021,
kassiano_2023, wolf_2023)`. Each of these is a longitudinal
lengthened-position→growth result (triceps long head, hamstrings, gastrocnemius,
and the ROM meta-analysis). They genuinely establish the lengthened-position
principle this prior leans on. They do *not* establish anything delt-specific —
but that is correct and expected: `grounded_in` per ADR-010 names the modules
supplying the general lengthened-position principle, not delt evidence (there is
none). No entry leans on a module that fails to support it.

---

## Structural walling-off

- Module exports `MechanisticEmphasis` only. No `ExerciseEmphasis`, no
  `EffectEstimate`. Confirmed.
- `MECHANISTIC_EMPHASIS` is consumed by `registry._MECHANISTIC_INDEX`, which is
  built from `_MECHANISTIC_SOURCES` and is structurally separate from
  `_EMPHASIS_INDEX`. Confirmed.
- The index build raises `ValueError` on a duplicate `(exercise, muscle,
  region)` key — one entry per key by construction. The nine delt entries are
  key-unique (3 exercises × 3 distinct regions). Confirmed.
- `combine_emphasis_estimates()` accepts only `ExerciseEmphasis`, so a
  mechanistic prior cannot be pooled with measured data. Confirmed.
- `selection_emphasis()` consults the mechanistic tier only as a fallback when
  no measured `ExerciseEmphasis` exists, and tags the tier `"mechanistic"`.
  Confirmed.
- `python3 -m app.priors.mechanistic.deltoids` runs; in-module asserts pass
  (all emphasis in [0,1], all confidence `low`, all regions in the head set).
- `python -m pytest tests/priors/ -q` → **228 passed** (in a throwaway venv at
  `/tmp/priors_venv`, removed afterward).

No walling-off defects.

---

## Concerns & discrepancies (ranked)

1. **MINOR — `incline_bench_press` rationale overstates the anterior-delt
   stretch.** It claims the humerus "travels behind the plane of the torso" and
   the anterior delt is "stretched". A correctly-performed incline press keeps
   the humerus at roughly torso-plane to slightly-forward; going behind the
   plane is the impingement fault. The `long` bucket is the right *relative*
   call (best of the three anterior exercises), but the rationale asserts an
   absolute deep stretch the movement does not deliver. Reword to "long-ish /
   lengthened relative to the other anterior options," not "behind the torso."

2. **MINOR — inconsistent caveating of the two cable 1.0 entries.**
   `cable_lateral_raise` explicitly notes its 1.0 assumes a stretch-loading
   setup ("not a token cable swap"); `cable_rear_delt_fly` makes the identical
   assumption but states "the cable keeps tension there" as fact. Add the same
   setup caveat to the rear-delt entry so the two siblings are honest in the
   same way.

3. **MINOR (optional) — the docstring could acknowledge the 2025
   cable-vs-dumbbell lateral-raise trial.** It found the two equipment-
   equivalent for lateral-delt hypertrophy — mild counter-evidence to the
   prior's stretch-bias premise. It correctly does *not* supersede this prior
   (equipment-equivalence, not exercise selection) and is not a defect, but a
   one-line mention would keep the module's "what would supersede this" framing
   current. Not required for the verdict.

No MATERIAL or MODERATE findings.

---

## Recommendations

1. Reword the `incline_bench_press` rationale: replace "the humerus travels
   behind the plane of the torso — the anterior deltoid is stretched" with a
   claim the movement actually supports — e.g. "at the bottom the humerus is at
   roughly torso-plane and the press is loaded heavily there, so the anterior
   delt is loaded at a long length *relative to the other anterior options*
   (no common anterior-delt exercise loads the deep behind-the-body stretch —
   1.0 here is the within-head maximum, not an absolute deep stretch)."

2. Add to `cable_rear_delt_fly`'s rationale the same explicit setup caveat the
   `cable_lateral_raise` entry already carries — e.g. "(Assumes the cross-body
   cable variant set up to load the stretched start, not a token cable swap.)"

3. Optional: add one line to the module docstring noting the 2025 Frontiers
   cable-vs-dumbbell lateral-raise trial as equipment-equivalence evidence that
   does not supersede this selection prior, mirroring the existing
   Coleman/Larsen sentence.

All three are rationale/wording edits. No entry should be dropped, re-bucketed,
or re-tagged. Once Recommendations 1 and 2 are applied this module is `SOUND`.
