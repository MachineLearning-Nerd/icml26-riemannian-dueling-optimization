# Limitations and deviations

The paper does not release its random SPD matrices, so deterministic
noncommuting matrices are regenerated from documented seeds. The source
reports a figure rather than a numerical acceptance threshold. The experiment
therefore verifies a faithful application at the stated dimensions, not exact
pixel agreement with the unreleased figure. A fixed-point solver is used only
as an independent checker.

- The sphere Rayleigh step schedule `eta_k = 1.5/(k+25)^0.75` is a free choice
  the paper does not fix. It was calibrated on separate seeds and every
  reported row uses held-out seeds, which mitigates but does not eliminate the
  dependence on that choice.
- Two dimensions (100, 150) and three seeds each are a finite sample of the
  paper's synthetic scope, not proof of coverage for every manifold in the
  theorem class.
- The constrained Karcher-mean RDFW variant of Section 5.1.3 is evidenced
  under Claim 3, not here.
