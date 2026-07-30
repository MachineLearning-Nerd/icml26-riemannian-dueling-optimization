# Method

For each paper dimension, generate 50 independently rotated dense SPD
matrices. RDNGD samples unit symmetric tangent directions in whitened
coordinates, asks one two-probe comparison, and moves along the affine-invariant
exponential map using only the returned sign. An independent Karcher
fixed-point solver sees function geometry and supplies a reference objective
and residual, but never informs the RDNGD horizon or update.

The reversed-sign control uses the same valid SPD geometry and should increase
the objective. Every result, checkpoint, seed, comparison count, reference
residual, and control is emitted as JSON by the fixed reproduction command.
