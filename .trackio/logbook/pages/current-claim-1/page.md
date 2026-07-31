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

All 9/9 nonconvex and 9/9 convex held-out cells satisfy their target.

**Negative controls.** Discarding the comparison outcomes leaves gradient norm
`0.3120 > 0.18`, and reversing the convex comparisons leaves suboptimality
`1.125 > 0.02`. Both fail for the intended reason: without a usable sign the
iterate has no descent information.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
# Downloaded Space:
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

- [Raw result](../../outputs/claim1.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Full RDNGD generator](../../reproduction/empirical_algorithms.py)
- [Theorem certificate](../../reproduction/theorem_audit.py)
- Source anchors: `#S3.Thmtheorem6`, `#S3.Thmtheorem7`

Evidence run `27332bb6-e56c-42ae-9d9e-4b0a885df123`, SHA
`d94d1e7e64e2907c7a8c7a92e1e00dda922fc714`, seed root 20260729.
HF `cpu-upgrade`: estimated 8 cores, 64 logical CPUs allocated, BLAS one
thread; cumulative scientific runtime 1339.44 s.

Reproduced unchanged by the current evidence run `b05c7cfe-f022-403d-881a-773c407c28ac`, Git SHA
`1a094fdc3edb0dcf785d8e0755ec1029ea47e531`, on HF `cpu-upgrade` (Python 3.12.12, Linux x86_64).

**Limitation.** The empirical grid is finite. It cannot prove a universally
quantified theorem; that role is limited to the symbolic certificate.
