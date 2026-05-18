"""
app/priors/mechanistic/ — derived, biomechanics-based exercise-selection priors.

A FALLBACK tier for muscles where no longitudinal head-to-head exercise
trial exists ("literature-blocked" in COVERAGE.md — currently lats and
deltoids). Modules here export `MechanisticEmphasis` objects (see
app/priors/shared.py and docs/priors/proposals/ADR-010-mechanistic-emphasis-priors.md).

These are NOT measured priors. They are derived from biomechanics weighted by
the layer's own encoded lengthened-position evidence, never from EMG. They are
kept structurally separate from the measured `ExerciseEmphasis` index: the
optimizer consults a mechanistic prior for a (muscle, region) only when no
measured source exists, and a measured source always supersedes it.
"""
