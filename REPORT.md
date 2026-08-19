# Audit report

This repository is an independent CPU reproduction and source audit for
**Riemannian Dueling Optimization**.

Claims 1, 3, 4, and 6 pass their scoped evidence contracts. Claim 2 supports
the intended RRDNGD theorem but exposes a separate defect in the printed
restart schedule. Claim 4's earlier finite-ν falsification is withdrawn after
the `gamma_x` vacuity audit; the current non-vacuous sweep, ideal estimator,
and controls support the scoped claim. Claim 5 verifies the calibrated
comparison-only application mechanism, while the exact paper-setting attack
and licensed HLW annotations remain blocked.

The package publication gate passed, but the prior live evaluator score remains
`3/12` and no current score increase is claimed. Detailed pages are under
[`pages/current-claim-1`](pages/current-claim-1/page.md) through
[`pages/current-claim-6`](pages/current-claim-6/page.md); branch roles are in
[`branch-audit.md`](branch-audit.md).
