# Claim 6 — sphere and dense SPD manifolds

**Exact claim.** The framework covers Hadamard and bounded-curvature
manifolds, with synthetic demonstrations including sphere Rayleigh
optimization and SPD Karcher means. The SPD experiment uses `n in {5,10}` and
`m=50`.

**Verdict: VERIFIED for the demonstrated application scope.** Both named
synthetic applications are run by the current verifier with actual
comparison-only RDNGD: Rayleigh quotient maximization on the unit sphere, and
Karcher means on dense, noncommuting SPD matrices under the affine-invariant
metric — never an analytic diagonal shortcut.

## Rayleigh quotient maximization on the unit sphere (Section 5.1.1, eq. 13)

`min_{x in S_d(1)} f(x) = -1/2 x^T A x`, with `B_ij ~ N(0, 1/d)` i.i.d. and
`A = 1/2 (B + B^T)` exactly as the paper specifies. The optimizer sees only
which of `Exp_x(nu u)` and `Exp_x(-nu u)` has the smaller objective, with
`nu = 1e-6` and 50,000 duels. Iterates stay on the sphere through the
exponential map `Exp_x(v) = cos(||v||)x + sin(||v||)v/||v||`, not by projection.
The optimum `f* = -1/2 lambda_max(A)` is the paper's stated value.

| d | seed | duels | L = lmax-lmin | initial gap | final gap | unit-norm error |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 20260751 | 50,000 | 2.705 | 7.018e-1 | `4.006e-6` | 0.0 |
| 100 | 20260752 | 50,000 | 2.777 | 6.766e-1 | `4.223e-6` | 0.0 |
| 100 | 20260753 | 50,000 | 2.830 | 7.626e-1 | `3.419e-6` | 0.0 |
| 150 | 20260761 | 50,000 | 2.780 | 6.743e-1 | `6.360e-6` | 0.0 |
| 150 | 20260762 | 50,000 | 2.785 | 6.968e-1 | `7.624e-6` | 0.0 |
| 150 | 20260763 | 50,000 | 2.784 | 5.652e-1 | `6.122e-6` | 1.1e-16 |

The paper does not state a step schedule for this experiment, so one had to be
chosen: `eta_k = 1.5/(k+25)^0.75`. It was selected on **separate calibration
seeds** (20260741, 20260742); every row above uses held-out seeds that were not
inspected during selection. Reversing the comparison signs leaves gaps of
`7.0176e-1` (d=100) and `6.7434e-1` (d=150) — five orders of magnitude worse,
i.e. no progress at all from the starting gap.

## Karcher means on dense SPD matrices (Section 5.1.2)

| n | m | duels | initial | final | relative reference gap |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 50 | 4,000 | .574325 | .564774 | `6.73e-6` |
| 10 | 50 | 6,000 | 1.054379 | 1.039381 | `2.45e-5` |

The independent fixed-point reference residuals are below `8e-13`, all output
eigenvalues remain positive, and minimum pairwise commutator norms are
`0.0139` and `0.1923`.

**Negative controls.** Reversing the comparison signs worsens the SPD
objectives to `0.9865` and `1.2289` (from `0.5743` and `1.0544`), and leaves
the sphere gaps at `7.0176e-1` and `6.7434e-1` — no progress at all. Both fail
for the intended reason: the duel outcome is the only signal the optimizer has.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
# Downloaded Space:
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

- [Raw result](../../outputs/claim6.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Sphere Rayleigh generator](../../reproduction/sphere_rayleigh.py)
- [Full dense-SPD generator](../../reproduction/dense_spd.py)
- Source: Section 5.1.1 (Rayleigh quotient, eq. 13) and Section 5.1.2
  (Karcher mean)

Evidence run `b05c7cfe-f022-403d-881a-773c407c28ac`, Git SHA `1a094fdc3edb0dcf785d8e0755ec1029ea47e531`. SPD seeds 20260735 and 20260740; sphere
held-out seeds 20260751-3 and 20260761-3. HF `cpu-upgrade`: 8 computational
cores estimated, 64 logical CPUs allocated, BLAS one thread, Python 3.12.12.
Sphere route runtime 16.21 s; SPD route runtime 54.36 s.

Sphere gaps are reported to four significant digits because the objective uses
a BLAS matrix-vector product, whose summation order differs across
architectures; the digits beyond the twelfth are not portable.

**Limitation.** These applications do not prove coverage of every manifold in
the theorem class; they reproduce the paper's named sphere and SPD scope
directly. The sphere step schedule is a necessary free choice the paper does
not fix, mitigated by held-out-seed reporting rather than eliminated. The
constrained Karcher-mean RDFW variant of Section 5.1.3 is covered under
Claim 3, not here.
