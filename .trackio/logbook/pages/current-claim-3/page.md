# Claim 3 — projection-free RDFW

**Exact claim.** Algorithm 3 and Theorem 4.1 state that comparison-only RDFW
uses a linear minimization oracle, no projections, `O(epsilon^-1)` iterations,
and `O(d epsilon^-2)` comparisons on smooth geodesically convex objectives.

**Verdict: VERIFIED.** The machine-checkable oracle sum is
`sum 2 M_k = T a d (T+5)`; substituting the independently derived
`T=O(1/epsilon)` theorem certificate gives `O(d/epsilon²)`. The named RDFW
algorithm was also run on simplex-constrained convex objectives using only its
LMO and comparison signs.

| d | T=10 error | T=80 error | error slope | query slope |
| ---: | ---: | ---: | ---: | ---: |
| 3 | `6.31e-5` | `4.53e-5` | -0.250 | 1.835 |
| 7 | `1.22e-2` | `1.79e-4` | -2.018 | 1.835 |
| 15 | `1.86e-2` | `3.74e-4` | -1.890 | 1.835 |

Every run used zero projections and stayed feasible. The `d=3` series is
explicitly floor-limited and is not used to estimate the asymptotic error
slope.

**Negative control.** Reversing the comparison signs at `d=15, T=80` leaves
error `0.532789` against `0.000374` normally — three orders of magnitude worse,
confirming the LMO steps are driven by the oracle and not by the geometry
alone.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
# Downloaded Space:
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

- [Raw result](../../outputs/claim3.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Full RDFW generator](../../reproduction/empirical_algorithms.py)
- [Symbolic certificate](../../reproduction/theorem_audit.py)
- Source anchors: `#alg3`, `#S4.Thmtheorem1`

Evidence run `27332bb6-e56c-42ae-9d9e-4b0a885df123`, SHA
`d94d1e7e64e2907c7a8c7a92e1e00dda922fc714`, seed root 20260729,
HF `cpu-upgrade`; 64 logical CPUs allocated, BLAS one thread.

Reproduced unchanged by the current evidence run `b05c7cfe-f022-403d-881a-773c407c28ac`, Git SHA
`1a094fdc3edb0dcf785d8e0755ec1029ea47e531`, on HF `cpu-upgrade` (Python 3.12.12, Linux x86_64).

**Limitation.** The finite sweep corroborates the named algorithm. Universal
complexity is supported by the symbolic certificate, not inferred from four
horizons.
