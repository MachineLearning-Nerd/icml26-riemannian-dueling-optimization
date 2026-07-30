# Claim 1 — RDNGD complexity

**Exact claim.** Table 1 and Theorems 3.6–3.7 state that comparison-only
RDNGD has `O(d epsilon^-2)` iteration/oracle complexity for smooth nonconvex
objectives and `O(d epsilon^-1)` for smooth geodesically convex objectives.
The quantifier is every `epsilon>0`, under the smoothness, domain, curvature,
diameter, and interior-optimum assumptions stated in those theorems.

**Verdict: VERIFIED.** The universal upper bounds are checked by an independent
symbolic certificate; finite experiments are corroboration, not the proof.
The certificate reconstructs
`T >= L² d (D+1)²/(C_hat² epsilon²)` for the nonconvex theorem and
`T >= 1 + 16 pi d L zeta D/epsilon` for the convex theorem.

The executable RDNGD sweep independently estimated a minimum horizon from six
calibration seeds, then judged it once on 20 untouched seeds. The selection
rule was the first horizon whose one-sided 95% calibration bound was below
`0.9 epsilon`; no theorem-derived horizon was supplied.

| Intrinsic d | epsilon | selected T | held-out upper 95% |
| ---: | ---: | ---: | ---: |
| 4 | .35 / .25 / .18 | 32 / 32 / 64 | .2079 / .2079 / .1635 |
| 8 | .35 / .25 / .18 | 32 / 32 / 128 | .2346 / .2346 / .1519 |
| 16 | .35 / .25 / .18 | 32 / 128 / 256 | .2717 / .1940 / .1490 |

All 9/9 nonconvex and 9/9 convex held-out cells satisfy their target. Discarding
comparisons leaves gradient norm `0.3120 > 0.18`; reversing convex comparisons
leaves suboptimality `1.125 > 0.02`.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
```

- [Raw result](../../outputs/claim1.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Full RDNGD generator](../../reproduction/empirical_algorithms.py)
- [Theorem certificate](../../reproduction/theorem_audit.py)
- Source anchors: `#S3.Thmtheorem6`, `#S3.Thmtheorem7`

Evidence run `7443fdc4-50fb-4443-8915-f5dc0ab9d5f8`, SHA
`cf2385da7d7487b77d7a5d4ba6cf2f35c2f3c942`, seed root 20260729.
HF `cpu-upgrade`: estimated 8 cores, 64 logical CPUs allocated, BLAS one
thread; cumulative scientific runtime 266.79 s.

**Limitation.** The empirical grid is finite. It cannot prove a universally
quantified theorem; that role is limited to the symbolic certificate.
