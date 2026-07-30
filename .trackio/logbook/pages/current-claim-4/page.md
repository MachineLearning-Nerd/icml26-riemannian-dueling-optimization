# Claim 4 — current verification

**Exact claim tested.** Lemma 3.1 states a high-probability equality between
the finite-perturbation comparison estimator and the ideal sign vector.
Lemma 3.2 states
`E[sign(<v,u>)u] = (C_hat/sqrt(d)) v/||v||`, with
`C_hat in [1/sqrt(2pi),1]`, for nonzero tangent `v` and unit-uniform tangent
`u`.

**Verdict: VERIFIED.** This preserves the live judge’s 2/2 result without
overstating finite-`nu` unbiasedness.

| d | samples | C_hat | perpendicular error |
| ---: | ---: | ---: | ---: |
| 5 | 80,000 | 0.837524 | 0.002935 |
| 25 | 80,000 | 0.808687 | 0.004121 |
| 100 | 80,000 | 0.801690 | 0.003511 |

The source lower bound is 0.398942. An independent analytic checker compares
each estimate with `sqrt(d) E|U_1|`; all differences are below 0.05.

**Negative control.** Removing the sign and pairing every sampled direction
with its antipode gives an exactly zero mean, so it fails gradient alignment
for the intended reason.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
```

The raw evidence was generated with seed 20260729 on HF `cpu-upgrade`
(64 logical CPUs allocated, BLAS capped at one thread), Python 3.12.12. The
cumulative baseline suite took 3.124 seconds.

- [Raw JSON](../../outputs/current_claim4.json)
- [Executable independent checker](../../reproduction/verify_claim4.py)
- Source: ar5iv HTML SHA-256 `1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323`,
  anchors `#S3.Thmtheorem1` and `#S3.Thmtheorem2`

**Limitation.** The Monte Carlo test is finite-dimensional. Proposition 3.3
and Remark 3.4 qualify the actual finite-perturbation estimator as biased; this
page does not claim otherwise.
