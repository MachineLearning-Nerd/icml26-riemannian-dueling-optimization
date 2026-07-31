# Claim 6 — sphere and dense SPD manifolds

**Exact claim.** The framework covers Hadamard and bounded-curvature
manifolds, with synthetic demonstrations including sphere Rayleigh
optimization and SPD Karcher means. The SPD experiment uses `n in {5,10}` and
`m=50`.

**Verdict: VERIFIED for the demonstrated application scope.** The preserved
sphere run remains reachable in the historical evidence. The new check runs
actual comparison-only RDNGD on dense, noncommuting SPD matrices under the
affine-invariant metric—never an analytic diagonal shortcut.

| n | m | duels | initial | final | relative reference gap |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 50 | 4,000 | .574325 | .564774 | `6.73e-6` |
| 10 | 50 | 6,000 | 1.054379 | 1.039381 | `2.45e-5` |

The independent fixed-point reference residuals are below `8e-13`, all output
eigenvalues remain positive, and minimum pairwise commutator norms are
`0.0139` and `0.1923`. Reversing comparison signs worsens the objectives to
`0.9865` and `1.2289`.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
# Downloaded Space:
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

- [Raw result](../../outputs/claim6.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Full dense-SPD generator](../../reproduction/dense_spd.py)
- Source: Section 5.1, Karcher mean computation

Evidence run `27332bb6-e56c-42ae-9d9e-4b0a885df123`, SHA
`d94d1e7e64e2907c7a8c7a92e1e00dda922fc714`, seeds 20260735 and 20260740.
HF `cpu-upgrade`: 64 logical CPUs allocated, BLAS one thread; SPD runtime
54.00 s.

**Limitation.** These applications do not prove coverage of every manifold in
the theorem class. They directly reproduce the paper's named sphere/SPD scope.
