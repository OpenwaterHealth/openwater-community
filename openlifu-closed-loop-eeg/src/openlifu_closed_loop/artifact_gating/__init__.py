"""Artifact gating.

A median-absolute-deviation (MAD) gate over a 500-sample rolling buffer. Samples whose
deviation from the rolling median exceeds the MAD threshold are flagged as contaminated.
The gate runs upstream of the trigger logic so that artefactual samples never influence
the theta Z-score or a sonication decision. See docs/architecture.md.

Scaffolding: the concrete gate is migrated in with the developer's code. The rolling
buffer length is documented here as the design constant.
"""

ROLLING_BUFFER_SAMPLES = 500
