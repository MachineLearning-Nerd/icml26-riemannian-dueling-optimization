# Claim 5 source audit

The paper applies RDNGD to a CIFAR-10 VGG black-box attack with a
sphere-constrained perturbation. It states `T=1000`, batch size 10,
`nu=1e-6`, and `eta=1e-6`, and says other settings follow Li et al.'s
open-source repository. That repository uses VGG11-BN and a sphere radius
`0.05 * ||image||_2`.

For horizon leveling, the paper minimizes
`||R R_tilt - I||_F^2` on `SO(2)` with `T=100`, `nu=1e-6`, and `eta=1e-2`.
It uses the objective only to generate reproducible pairwise preferences.

Source HTML retrieved 2026-07-30, SHA-256
`1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323`.
Anchors: Section 5.2.1 and Section 5.2.2.
