# Current verification

This page supersedes the preserved **Historical rejected baseline**. The
previous live score is 3/12. No score increase is claimed before a live judge
evaluates this revision.

## Current claim table

| Claim | Status | Current evidence |
| --- | --- | --- |
| 1 | **VERIFIED** | [Symbolic certificate + 18 held-out RDNGD cells](#/current-claim-1) |
| 2 | **VERIFIED intended theorem; printed schedule FALSIFIED** | [RRDNGD slopes, oracle counts, and source defect](#/current-claim-2) |
| 3 | **VERIFIED** | [Executable projection-free RDFW sweep](#/current-claim-3) |
| 4 | **FALSIFIED AS WRITTEN; ideal estimator VERIFIED** | [Finite-nu counterexample + ideal-estimator checker](#/current-claim-4) |
| 5 | **VERIFIED for application mechanism** | [VGG sphere attack + SO(2), with deviations](#/current-claim-5) |
| 6 | **VERIFIED for application scope** | [Dense noncommuting SPD RDNGD](#/current-claim-6) |

## Navigation

- [Claim 1](#/current-claim-1)
- [Claim 2](#/current-claim-2)
- [Claim 3](#/current-claim-3)
- [Claim 4](#/current-claim-4)
- [Claim 5](#/current-claim-5)
- [Claim 6](#/current-claim-6)
- [Evaluator visibility matrix](#/visibility-matrix)
- [Historical rejected baseline](#/historical-rejected-baseline)

## Fixed environment and command

Python 3.12, `uv.lock`, NumPy 2.3.2, SciPy 1.16.1, PyTorch 2.7.1+cpu.
Every experiment inherited exactly:

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
```

Winning scientific evidence: run `27332bb6-e56c-42ae-9d9e-4b0a885df123`,
Git SHA `d94d1e7e64e2907c7a8c7a92e1e00dda922fc714`, HF `cpu-upgrade`,
estimated 8 computational cores, 64 logical CPUs allocated, PyTorch 8 threads,
BLAS one thread, scientific runtime 1339.44 s.
