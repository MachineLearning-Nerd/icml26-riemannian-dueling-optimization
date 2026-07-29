# Results

Run the full CPU verification:

```bash
OPENBLAS_NUM_THREADS=1 .venv/bin/python repro/src/verify.py
.venv/bin/python repro/src/publication_gate.py
```

Five anchored claims pass. Machine-readable evidence: [`outputs/verdict.json`](outputs/verdict.json).

| Claim | Executable evidence | Negative control |
|---|---|---|
| C1 — RDNGD | Table-1 schedules have exact 4× / 2× halving ratios | Incorrect nonconvex `ε⁻¹` fails |
| C2 — RRDNGD | Explicit `d log(1/ε)` restart schedule | `1/ε` grows eightfold rather than logarithmically |
| C3 — RDFW | Literal `M_k∝d(k+3)` batch sum is `8.2dT²` | Constant batch has wrong oracle order |
| C4 — estimator | Sphere Monte Carlo gives `Ĉ=.802–.838`, perpendicular error `<.0042` | Removing signs produces mean zero |
| C6 — applications | Full 50k Rayleigh at `d=100,150`; SPD `n=5,10,m=50`; SO(2) residual `9.2e-6` | Wrong SO(2) direction leaves `1.78` residual |

## Scope

This is a source-faithful finite construction audit, not a replacement proof of universal Riemannian theorems. C5 is not claimed: the source lacks the author-modified CIFAR/VGG attack implementation, checkpoint/version, selected examples, and processed benchmark state, so a surrogate attack would be a proxy.
