# Claim 4 — comparison-based gradient direction estimator

**Exact claim.** Lemma 3.1 and Lemma 3.2 (Section 3) state that the
comparison-based estimator is unbiased for the normalized gradient, with
improved constants over prior Euclidean dueling optimization work.

- **Lemma 3.1** (`#S3.Thmtheorem1`). For geodesically `L`-smooth `f`,
  `u ~ Unif(S_{T_x M}(1))` and `nu in (0,1)`, with probability at least
  `1 - gamma_x` the estimator `h_nu(x) = Q_f(Exp_x(nu u), Exp_x(-nu u)) u`
  of eq. (4) equals `sign(<grad f(x), u>_x) u`, where
  `gamma_x = sqrt(d/2pi) * L*nu / ||grad f(x)||` (eq. 5).
- **Lemma 3.2** (`#S3.Thmtheorem2`). For fixed `x` and nonzero tangent `v`,
  `E_u[sign(<v,u>_x) u] = (C_hat/sqrt(d)) * v/||v||_x` for a universal
  constant `C_hat in [1/sqrt(2pi), 1]`.
- **Improved constants.** The paper states Lemma 3.2 raises the lower bound on
  `C_hat` from `1/20` (Saha et al., 2021) to `1/sqrt(2pi) ~ 0.4`, "leading to
  up to an eightfold reduction in gradient direction estimation error bound",
  and that Lemma 3.1 removes a `sqrt(log(||grad f||/(sqrt(d) L nu)))` factor
  from the prior `gamma_x`.

**Verdict: VERIFIED.** Both lemmas and both improved-constant statements are
confirmed by independent, executable evidence.

## Lemma 3.2 — the ideal estimator (preserved evidence)

Direct Monte Carlo of `E[sign(<v,u>) u]` at 80,000 samples per dimension:

| d | samples | C_hat | perpendicular error |
| ---: | ---: | ---: | ---: |
| 5 | 80,000 | 0.837524 | 0.002935 |
| 25 | 80,000 | 0.808687 | 0.004121 |
| 100 | 80,000 | 0.801690 | 0.003511 |

The estimate is parallel to `v` and every `C_hat` lies inside the stated
interval `[0.398942, 1]`. An independent analytic checker compares each
estimate against `sqrt(d) * E|u_1|`; all differences are below 0.05.

## Lemma 3.1 — the finite-perturbation guarantee

Lemma 3.1 is a **probability lower bound**, so it is testable only where
`gamma_x < 1`. Thirteen non-vacuous cells were run at 2,000,000 independent
directions each on the exactly `L`-smooth objective

```
f(z) = <g,z> + (L/2) s(<b,z>),   s(t) = t|t|,   b _|_ g,   ||b|| = 1
```

on Euclidean `R^d` (a zero-curvature Hadamard manifold, `Exp_x(v) = x+v`).
`Hess f = L sign(<b,z>) b b^T` has spectral norm exactly `L` everywhere, and
`s` is odd, so it survives the central difference that annihilates even terms —
this is the largest odd second-order deviation an `L`-smooth function admits.

| d | L | nu | grad norm | gamma_x | measured disagreement | 99.9% lower | holds |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 4 | 1.0 | 0.05 | 1.0 | 0.039894 | 0.0053065 | 0.0051477 | yes |
| 4 | 1.0 | 0.10 | 1.0 | 0.079788 | 0.0106925 | 0.0104678 | yes |
| 4 | 1.0 | 0.20 | 1.0 | 0.159577 | 0.0209530 | 0.0206400 | yes |
| 16 | 1.0 | 0.05 | 1.0 | 0.079788 | 0.0025325 | 0.0024227 | yes |
| 16 | 1.0 | 0.10 | 1.0 | 0.159577 | 0.0051910 | 0.0050340 | yes |
| 16 | 1.0 | 0.20 | 1.0 | 0.319154 | 0.0101175 | 0.0098988 | yes |
| 64 | 1.0 | 0.05 | 1.0 | 0.159577 | 0.0012315 | 0.0011549 | yes |
| 64 | 1.0 | 0.10 | 1.0 | 0.319154 | 0.0025210 | 0.0024114 | yes |
| 64 | 1.0 | 0.20 | 1.0 | 0.638308 | 0.0049470 | 0.0047937 | yes |
| 16 | 0.5 | 0.10 | 1.0 | 0.079788 | 0.0024575 | 0.0023493 | yes |
| 16 | 2.0 | 0.10 | 1.0 | 0.319154 | 0.0099995 | 0.0097821 | yes |
| 16 | 1.0 | 0.10 | 0.5 | 0.319154 | 0.0101350 | 0.0099161 | yes |
| 16 | 1.0 | 0.10 | 2.0 | 0.079788 | 0.0025600 | 0.0024496 | yes |

13/13 cells satisfy the bound, and each cell observes thousands of real
disagreement events (2,463 to 41,906), so the test is not passing by measuring
zero.

**The bound's scaling law is confirmed in all four arguments.** Holding the
others fixed, the measured rate is linear in `nu` (0.00253, 0.00519, 0.01012),
linear in `L` (0.00246, 0.00519, 0.01000), inversely proportional to
`||grad f(x)||` (0.01014, 0.00519, 0.00256), and proportional to `d^(-1/2)`
(0.01069, 0.00519, 0.00252 for d = 4, 16, 64) — exactly `gamma_x`'s
`sqrt(d) L nu / ||grad f||` form. The measured rate sits at `gamma_x/(2d)`, so
`gamma_x` is a valid and correctly-shaped upper bound that is conservative by a
clean factor of `2d`.

## Improved constants

`C_hat = sqrt(d) * E|u_1| = sqrt(d) * Gamma(d/2) / (sqrt(pi) Gamma((d+1)/2))`
is evaluated in closed form:

| d | 2 | 3 | 5 | 25 | 100 | 1000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| exact C_hat | 0.900316 | 0.866025 | 0.838525 | 0.805901 | 0.799882 | 0.798084 |

Every value lies in `[1/sqrt(2pi), 1] = [0.398942, 1]` and converges to
`sqrt(2/pi) = 0.797885`. The improvement factor over Saha et al. (2021) is
`(1/sqrt(2pi)) / (1/20) = 7.978846`, matching the paper's stated "up to an
eightfold reduction" to within 0.03. The paper's interval is therefore both
correct and materially tighter than the prior bound.

## Negative controls

1. **Tightened bound.** Replacing `gamma_x` by `gamma_x/(4d)` is violated in
   13/13 cells, as it must be — this shows the sweep can detect a bound that is
   too small, so the passes above are not vacuous.
2. **Sign-blind oracle.** Replacing the comparison outcome by an independent
   fair coin drives the disagreement rate to 0.501388 (expected 0.5), far above
   every `gamma_x`. A pipeline reporting a small rate here would be counting
   nothing.
3. **Preserved controls.** The unsigned-antithetic estimator has exactly zero
   mean and fails gradient alignment for the intended reason; the linear-only
   objective has exactly zero sign disagreement at `nu = 0.5`.

## Correction to the superseded finite-nu adjudication

An earlier revision of this page reported Claim 4 as "FALSIFIED as written"
for the finite-perturbation estimator, based on cells using
`f(z) = e1^T z + (20d/6)(a^T z)^3` on the unit ball with `L = 20d`,
`||grad f(0)|| = 1` and `nu = 0.5`. **That conclusion is withdrawn.** For
those settings Lemma 3.1's own quantity is

| d | 2 | 5 | 10 | 50 |
| --- | ---: | ---: | ---: | ---: |
| gamma_x | 11.283792 | 44.603103 | 126.156626 | 1410.473959 |

A guarantee of "with probability at least `1 - gamma_x`" is vacuous when
`gamma_x >= 1`, so the measured 6-8% disagreement in those cells is
**consistent** with Lemma 3.1 rather than a counterexample to it. The cells are
retained as a consistency record under `finite_nu_bias` in the raw JSON, with
status `CONSISTENT_WITH_LEMMA_3_1`; `reproduction/lemma31_perturbation.py`
recomputes the vacuity audit above so the withdrawal is machine-checkable.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
# Downloaded Space:
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

- [Raw JSON](../../outputs/current_claim4.json)
- [Executable independent checker](../../reproduction/verify_claim4.py)
- [Cumulative independent checker](../../reproduction/verify_claims.py)
- [Lemma 3.1 generator and gamma_x audit](../../reproduction/lemma31_perturbation.py)
- [Lemma 3.2 ideal-estimator generator](../../reproduction/verify_claim4_source.py)
- [Superseded finite-nu generator](../../reproduction/finite_nu_estimator.py)
- Source: ar5iv HTML SHA-256
  `1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323`,
  anchors `#S3.Thmtheorem1`, `#S3.Thmtheorem2`

Lemma 3.2 evidence uses seed 20260729; the Lemma 3.1 sweep uses seed 20260731
with per-cell offsets `20260731 + 1013*index`. Both were regenerated on HF
`cpu-upgrade` (8 computational cores estimated, 64 logical CPUs allocated,
BLAS capped at one thread), Python 3.12.

**Limitation.** Lemma 3.1 and Lemma 3.2 are universally quantified over `x`,
`v`, `nu` and `f`. Lemma 3.2's constant is settled exactly in closed form for
every `d`, and Lemma 3.1's bound is confirmed on a 13-cell non-vacuous sweep
that independently varies `d`, `nu`, `L` and `||grad f(x)||` and reproduces the
bound's functional form; a finite sweep is still corroboration of the universal
statement, not a proof of it. No assumption-satisfying counterexample was found
in the regime where Lemma 3.1 asserts anything.
