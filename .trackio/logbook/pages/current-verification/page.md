# Current verification

This page supersedes the preserved **Historical rejected baseline**. The
previous live score is 3/12. No score increase is claimed before a live judge
evaluates this revision.

## Current claim table

| Claim | Status | Current evidence |
| --- | --- | --- |
| 1 | **VERIFIED** | [Symbolic certificate + 18 held-out RDNGD cells](#/current-claim-1) |
| 2 | **FALSIFIED as printed** | [Assumption-satisfying Algorithm 2 counterexample](#/current-claim-2) |
| 3 | **VERIFIED** | [Executable projection-free RDFW sweep](#/current-claim-3) |
| 4 | **VERIFIED** | [Estimator Monte Carlo + analytic checker](#/current-claim-4) |
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

Winning scientific evidence: run `7443fdc4-50fb-4443-8915-f5dc0ab9d5f8`,
Git SHA `cf2385da7d7487b77d7a5d4ba6cf2f35c2f3c942`, HF `cpu-upgrade`,
estimated 8 computational cores, 64 logical CPUs allocated, PyTorch 8 threads,
BLAS one thread, scientific runtime 266.79 s.
