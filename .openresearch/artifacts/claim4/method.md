# Method — Claim 4

Two lemmas, tested separately, plus the improved-constant statement.

## Lemma 3.2 (ideal estimator)

Monte Carlo of `E[sign(<v,u>) u]` for `u ~ Unif(S^{d-1})` at d = 5, 25, 100 and
80,000 samples, recovering `C_hat = sqrt(d) * <mean, v/||v||>` and the
perpendicular residual. The independent checker compares each estimate with the
closed form `C_hat = sqrt(d) * Gamma(d/2) / (sqrt(pi) Gamma((d+1)/2))`.

## Lemma 3.1 (finite perturbation)

Lemma 3.1 bounds the probability that the comparison estimator disagrees with
the ideal sign vector by `gamma_x = sqrt(d/2pi) L nu / ||grad f(x)||`. The bound
is only testable where `gamma_x < 1`; above that it asserts nothing.

Objective: `f(z) = <g,z> + (L/2) s(<b,z>)` with `s(t) = t|t|`, `b` a unit vector
orthogonal to `g`, on Euclidean `R^d`. Then `Hess f = L sign(<b,z>) b b^T`, so
`||Hess f||_2 = L` exactly and `f` is geodesically `L`-smooth everywhere, with
`grad f(0) = g`. Because `s` is odd it survives the central difference
`f(nu u) - f(-nu u) = 2 nu <g,u> + L nu^2 (b.u)|b.u|` that annihilates even
terms — this is the largest odd second-order deviation an `L`-smooth function
permits along a direction, i.e. the hardest case for the lemma.

Sweep: 13 cells at 2,000,000 directions each, independently varying `d` (4, 16,
64), `nu` (0.05, 0.1, 0.2), `L` (0.5, 1, 2) and `||grad f(x)||` (0.5, 1, 2).
Acceptance requires the one-sided 99.9% lower confidence bound on the measured
disagreement rate to stay at or below `gamma_x` in every cell.

## Improved constants

`(1/sqrt(2pi)) / (1/20)` is compared with the paper's stated eightfold factor,
and the exact `C_hat` is evaluated at d = 2, 3, 5, 25, 100, 1000 to confirm it
lies inside `[1/sqrt(2pi), 1]` and above Saha et al.'s `1/20` for every one.

## Controls

- Tightened bound `gamma_x/(4d)`: must be violated in every cell.
- Sign-blind fair-coin oracle: must give a disagreement rate near 0.5.
- Nonlinear objective at `nu = 1e-4` and linear-only objective at `nu = 0.5`:
  must give exactly zero disagreement.
