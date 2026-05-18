"""
Demonstration: combining literature estimates across overlapping meta-analyses.

This script exercises the prior infrastructure built in shared.py against
the failure-effects literature, showing:

  1. Per-paper estimates retrieved for different user profiles
  2. Routing to the most-applicable single estimate
  3. Inverse-variance pooling across compatible estimates
  4. Overlap-adjusted pooling for non-independent meta-analyses
  5. How the optimizer's chosen estimate changes with user characteristics

Run from repo root: python -m app.priors.demo_combine
"""

from .shared import (
    UserProfile, best_applicable, combine_inverse_variance, combine_for_user,
)
from . import failure_effects


def banner(title: str):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def show_estimate(label: str, est):
    if est is None:
        print(f"  {label}: <no applicable estimate>")
        return
    lo, hi = est.ci_95
    print(f"  {label}:")
    print(f"     mean   = {est.mean:+.3f}  (95% CI: {lo:+.3f}, {hi:+.3f})")
    print(f"     SE     = {est.se:.3f}    precision = {est.precision:.1f}")
    print(f"     n      = {est.n}")
    print(f"     source = {est.source}")
    print(f"     notes  = {est.notes[:80]}{'...' if len(est.notes) > 80 else ''}")


# ---------------------------------------------------------------------------
# Define two example users
# ---------------------------------------------------------------------------

trained_male_28 = UserProfile(
    age=28,
    sex="male",
    training_status="trained",
    notes="Hypothetical intermediate lifter, 6 years training experience.",
)

untrained_female_45 = UserProfile(
    age=45,
    sex="female",
    training_status="untrained",
    notes="Hypothetical new lifter; outside primary studied population.",
)


# ---------------------------------------------------------------------------
# 1. Show all hypertrophy estimates
# ---------------------------------------------------------------------------

banner("Step 1: All hypertrophy estimates in the registry")
for i, est in enumerate(failure_effects.HYPERTROPHY_ESTIMATES, 1):
    show_estimate(f"#{i}", est)
    print()


# ---------------------------------------------------------------------------
# 2. Per-user applicability scoring
# ---------------------------------------------------------------------------

banner("Step 2: Applicability scoring for two users")
print()
print(f"User A: {trained_male_28}")
print(f"User B: {untrained_female_45}")
print()
print("Applicability scores (higher = better fit):")
print(f"{'Estimate':<55} {'User A':>8} {'User B':>8}")
print("-" * 72)
for est in failure_effects.HYPERTROPHY_ESTIMATES:
    src = str(est.source)
    label = f"{src} — {est.notes[:35]}"
    app_a = est.population.applicability_to(trained_male_28)
    app_b = est.population.applicability_to(untrained_female_45)
    print(f"{label:<55} {app_a:>8.2f} {app_b:>8.2f}")


# ---------------------------------------------------------------------------
# 3. Best single estimate routing
# ---------------------------------------------------------------------------

banner("Step 3: Best single estimate routing")
print()
print("If we had to pick ONE estimate per user (no pooling):")
print()
print("User A (trained 28yo male):")
best_a = best_applicable(failure_effects.HYPERTROPHY_ESTIMATES, trained_male_28)
show_estimate("Best", best_a)
print()
print("User B (untrained 45yo female):")
best_b = best_applicable(failure_effects.HYPERTROPHY_ESTIMATES, untrained_female_45)
show_estimate("Best", best_b)


# ---------------------------------------------------------------------------
# 4. Inverse-variance pooling — naive (no overlap adjustment)
# ---------------------------------------------------------------------------

banner("Step 4: Inverse-variance pooling (naive)")
print()
print("Pooling ALL volume-equated hypertrophy estimates for trained males,")
print("ignoring the fact that Grgic and Refalo share underlying studies:")
print()

volume_equated = failure_effects.hypertrophy_estimates_volume_equated()
print(f"  Pooling {len(volume_equated)} estimates...")
pooled_naive = combine_for_user(
    volume_equated, trained_male_28,
    min_applicability=0.7,
    overlap_se_inflation=1.0,  # no penalty
)
show_estimate("Naive pooled", pooled_naive)


# ---------------------------------------------------------------------------
# 5. Inverse-variance pooling — with overlap penalty
# ---------------------------------------------------------------------------

banner("Step 5: Overlap-adjusted pooling")
print()
print(f"Applying SE inflation factor {failure_effects.OVERLAP_SE_INFLATION} to")
print("account for shared underlying studies across the three meta-analyses:")
print()

pooled_adjusted = combine_for_user(
    volume_equated, trained_male_28,
    min_applicability=0.7,
    overlap_se_inflation=failure_effects.OVERLAP_SE_INFLATION,
)
show_estimate("Overlap-adjusted pooled", pooled_adjusted)

print()
print("Notice the difference:")
print(f"  Naive pooled SE:    {pooled_naive.se:.4f}")
print(f"  Adjusted pooled SE: {pooled_adjusted.se:.4f}")
print(f"  Adjusted CI is {(pooled_adjusted.ci_95[1] - pooled_adjusted.ci_95[0]) / (pooled_naive.ci_95[1] - pooled_naive.ci_95[0]):.2f}x wider —")
print("  more honest uncertainty for the truly available evidence.")


# ---------------------------------------------------------------------------
# 6. Demonstration: Vieira's overall estimate gets EXCLUDED appropriately
# ---------------------------------------------------------------------------

banner("Step 6: Why Vieira's 0.75 estimate is excluded from the pool")
print()
print("Vieira 2021's overall SMD=0.75 looks like a huge effect, but it didn't")
print("equate volume between failure/non-failure arms. The volume-equated")
print("estimates from the same paper (and from Grgic/Refalo) are all near")
print("zero. Vieira's 0.75 answers a different question.")
print()
print("Our filter `hypertrophy_estimates_volume_equated()` excludes it:")
print()
all_count = len(failure_effects.HYPERTROPHY_ESTIMATES)
veq_count = len(failure_effects.hypertrophy_estimates_volume_equated())
print(f"  All hypertrophy estimates:        {all_count}")
print(f"  Volume-equated only:              {veq_count}")
print(f"  Excluded:                         {all_count - veq_count} "
      f"(Vieira's non-equated overall)")
print()
print("This is exactly the kind of question-framing decision that has to live")
print("IN CODE, not in a database. Schema can't know that two SMDs answer")
print("different questions.")


# ---------------------------------------------------------------------------
# 7. What the optimizer would actually use
# ---------------------------------------------------------------------------

banner("Step 7: Practical takeaway for the optimizer")
print()
print(f"For user A (trained 28yo male) considering RIR=0 (failure) vs")
print(f"RIR=2 (non-failure) hypertrophy training at SAME weekly volume:")
print()
final = pooled_adjusted
if final is not None:
    lo, hi = final.ci_95
    print(f"  Expected SMD advantage of failure: {final.mean:+.3f}")
    print(f"  95% CI: [{lo:+.3f}, {hi:+.3f}]")
    print()
    if lo < 0 < hi:
        print(f"  CI CROSSES ZERO → effect is uncertain in direction.")
        print(f"  Optimizer interpretation: do NOT default to failure training.")
        print(f"  Default to moderate RIR (1-3) and let user preference decide.")
    else:
        print(f"  CI excludes zero → effect is reliably {('positive' if final.mean > 0 else 'negative')}.")
        if final.mean > 0:
            print(f"  Failure training expected to provide small hypertrophy benefit.")
        else:
            print(f"  Non-failure training expected to be slightly better.")
print()
print("This is the actual programming advice produced by combining 3 papers.")
print("Defensible, with traceable provenance, and updates automatically when")
print("a new meta-analysis is added to the registry.")
