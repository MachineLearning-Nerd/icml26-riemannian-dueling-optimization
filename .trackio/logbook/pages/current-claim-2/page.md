# Claim 2 — RRDNGD linear convergence and printed source defect

**Exact claim.** Algorithm 2 and Theorem 3.10 assert that RRDNGD reaches every
`epsilon>0` on an `L`-smooth, `alpha`-strongly geodesically convex objective
over bounded `X`, with an interior optimum and the paper's curvature
assumptions, using `O(d log(1/epsilon))` comparisons.

**Verdict: VERIFIED for the intended theorem.** The proof-consistent recurrent
algorithm shows approximately one bit of error reduction per phase while the
per-phase oracle count is linear in `d`:

| d | log2 median-error slope/phase | comparisons/phase |
| ---: | ---: | ---: |
| 4 | `-1.003` | 1,612 |
| 8 | `-0.995` | 3,220 |
| 16 | `-1.039` | 6,436 |

Eight phases and ten deterministic seeds were executed per dimension on
`f(x)=||x||²/2`. The optimizer receives only signs of paired objective
comparisons. The slopes lie inside the predeclared `[-1.2,-0.8]` interval and
the query counts double with dimension, directly supporting linear convergence
and `O(d log(1/epsilon))` oracle cost under geometric phase targets.

**Separate source finding: FALSIFIED as printed.** Algorithm 2 sets
`epsilon_k = alpha D / 2^(2-k)`, which grows with `k`. Appendix F instead
requires `epsilon_k = alpha D_k/4 = alpha D/2^(k+2)`. The schedules differ by
`2^(2k)`.

An exact counterexample satisfies every stated assumption:
`f(x)=x²/2` on Euclidean `X=[-2,2]`, with `d=L=alpha=1`, curvature zero,
interior optimum zero, and nonexpansive projection. At target `1e-6`, 42
phases of 203 iterations consume 17,052 comparisons.

**Negative control.** The two schedules are run head-to-head on identical
seeds, iterate counts and oracle budgets, so only the schedule differs:

| Schedule | final gap | meets `1e-6` |
| --- | ---: | --- |
| Algorithm 2 as printed | `8.024201e-5` | no |
| Appendix-F-consistent control | `2.257724e-16` | yes |

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
# Downloaded Space:
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

- [Raw counterexample](../../outputs/claim2.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Executable theorem audit](../../reproduction/theorem_audit.py)
- [Corrected RRDNGD control](../../reproduction/empirical_algorithms.py)
- Source anchors: `#alg2`, `#S3.Thmtheorem10`, Appendix F

Evidence run `27332bb6-e56c-42ae-9d9e-4b0a885df123`, SHA
`d94d1e7e64e2907c7a8c7a92e1e00dda922fc714`, deterministic seed root
20260729, HF `cpu-upgrade`, cumulative runtime 1339.44 s.

Reproduced unchanged by the current evidence run `b05c7cfe-f022-403d-881a-773c407c28ac`, Git SHA
`1a094fdc3edb0dcf785d8e0755ec1029ea47e531`, on HF `cpu-upgrade` (Python 3.12.12, Linux x86_64).

**Limitation.** The broad complexity verdict uses the proof-consistent schedule
required by Appendix F. The literal Algorithm 2 schedule is separately
falsified and must not be mistaken for the verified correction. Finite
experiments corroborate the geometric rate; Appendix F supplies the universal
upper-bound derivation.
