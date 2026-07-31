# Claim 4 — current verification

**Exact claim tested.** Lemma 3.1 states a high-probability equality between
the finite-perturbation comparison estimator and the ideal sign vector.
Lemma 3.2 states
`E[sign(<v,u>)u] = (C_hat/sqrt(d)) v/||v||`, with
`C_hat in [1/sqrt(2pi),1]`, for nonzero tangent `v` and unit-uniform tangent
`u`.

**Verdict: FALSIFIED AS WRITTEN for the finite-perturbation estimator; the
ideal Lemma 3.2 estimator is VERIFIED.** This preserves the exact result already
accepted by the live judge and explicitly tests the distinction made by
Proposition 3.3 and Remark 3.4.

| d | samples | C_hat | perpendicular error |
| ---: | ---: | ---: | ---: |
| 5 | 80,000 | 0.837524 | 0.002935 |
| 25 | 80,000 | 0.808687 | 0.004121 |
| 100 | 80,000 | 0.801690 | 0.003511 |

The source lower bound is 0.398942. An independent analytic checker compares
each estimate with `sqrt(d) E|U_1|`; all differences are below 0.05.

For the actual finite-perturbation estimator, 200,000 independent directions
were drawn at each dimension on the Euclidean unit ball for the smooth
objective
`f(z)=e1^T z + (20d/6)(a^T z)^3`, `a=(e1+e2)/sqrt(2)`, at `x=0`.
Curvature is zero, the gradient is nonzero, the probes remain in the domain,
and the gradient is `20d`-Lipschitz on that domain.

| d | disagreement at nu=.5 | paired orthogonal bias | 95% lower bound |
| ---: | ---: | ---: | ---: |
| 2 | 7.5465% | 0.14952 | 0.14670 |
| 5 | 6.7760% | 0.09122 | 0.08964 |
| 10 | 6.5505% | 0.06375 | 0.06254 |
| 50 | 6.2695% | 0.02792 | 0.02744 |

Forty blocked paired means provide the uncertainty estimates. Every lower
bound exceeds the predeclared 0.015 falsification threshold.

**Negative controls.** At `nu=1e-4`, the nonlinear estimator has zero sampled
sign disagreement. At `nu=.5`, replacing the objective by its linear part also
has exactly zero disagreement. The preserved unsigned-antithetic control has
zero mean and fails gradient alignment for the intended reason.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
```

The ideal evidence uses seed 20260729. The finite-`nu` evidence uses seed
20260731 and was independently rerun in cumulative run
`27332bb6-e56c-42ae-9d9e-4b0a885df123`, Git SHA
`d94d1e7e64e2907c7a8c7a92e1e00dda922fc714`, on HF `cpu-upgrade`
(8 computational cores estimated, 64 logical CPUs allocated, BLAS capped at
one thread), Python 3.12.12. Full cumulative scientific runtime was 1339.44 s.

- [Raw JSON](../../outputs/current_claim4.json)
- [Executable independent checker](../../reproduction/verify_claim4.py)
- [Cumulative independent checker](../../reproduction/verify_claims.py)
- [Full estimator generator](../../reproduction/verify_claim4_source.py)
- [Finite-nu generator](../../reproduction/finite_nu_estimator.py)
- Source: ar5iv HTML SHA-256 `1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323`,
  anchors `#S3.Thmtheorem1` and `#S3.Thmtheorem2`

**Limitation.** The finite counterexample falsifies the registry’s unqualified
finite-`nu` wording, not Lemma 3.2’s ideal expectation or Lemma 3.1’s
high-probability small-perturbation guarantee.
