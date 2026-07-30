# Method

- Nonconvex RDNGD: negative Rayleigh quotient on spheres of manifold
  dimensions 4, 8, and 16; random-iterate gradient norm is the theorem's
  criterion.
- Convex RDNGD: a smooth quadratic over a radius-two Euclidean ball, with
  projection and held-out first-success calibration.
- RRDNGD: the Appendix-F-consistent recurrent schedule on strongly convex
  quadratics, measuring median log2 error per phase.
- RDFW: a smooth quadratic over the simplex, the exact increasing comparison
  batch, one LMO per iteration, and zero projections.

The nonconvex control discards every comparison and freezes the iterate,
because reversed descent can reach a maximizer that is still stationary. The
convex control reverses the comparison sign and must move away from the
minimum.
