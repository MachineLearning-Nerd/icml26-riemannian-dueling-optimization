# Riemannian Dueling Optimization reproduction

Claim-by-claim, CPU-only reproduction of
[arXiv:2603.00023](https://arxiv.org/abs/2603.00023). The previous live judge
score is 3/12; no score increase is claimed until the published revision is
evaluated.

The campaign tests all six judged claims. Headline observed evidence:

- RDNGD: symbolic rate certificates and 18/18 held-out target cells pass.
- RRDNGD: Algorithm 2 as printed ends at `8.02e-5` for a `1e-6` target;
  the Appendix-F control reaches `2.26e-16`. Verdict: FALSIFIED as printed.
- RDFW: zero-projection executable sweeps and the exact oracle-sum certificate
  pass.
- Estimator: maximum perpendicular error is 0.00412 over 80,000 samples per
  dimension, preserving the existing full-credit result.
- Applications: the calibrated comparison-only VGG sphere attack changes 3/4
  predictions; the paper-setting route changes 0/2 and remains separately
  BLOCKED. `SO(2)` leveling succeeds on 19/19 deterministic tilts.
- Dense SPD: relative Karcher-reference gaps are `6.73e-6` and `2.45e-5` at
  the paper dimensions.

The only full-scale substitutions are explicit: a pinned public VGG11-BN
checkpoint/indices replace unspecified paper assets, the successful attack
uses calibrated `nu`, `eta`, radius, and margin objective, and licensed HLW
pixels are unavailable. No GPU was used.

[Detailed visual report](reports/reproduction/report.md) ·
[Evaluator entrypoint](.trackio/logbook/pages/current-verification/page.md) ·
[Tutorial notebook](notebooks/riemannian_dueling_reproduction.py)

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-nDfDnsyllY-riemannian-dueling/blob/main/notebooks/riemannian_dueling_reproduction.py)

## Experiment log

Every formal node inherited this exact command:
`uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public landing page and reports | Not run as an experiment (publication surface) | Presentation only | none |
| [judged baseline](https://github.com/MachineLearning-Nerd/icml26-repro-nDfDnsyllY-riemannian-dueling/tree/orx/judged-baseline-3-of-12) | Freeze and rerun judged 3/12 state | `uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py` | Legacy evidence reproduced | HF cpu-upgrade |
| [theorem audit](https://github.com/MachineLearning-Nerd/icml26-repro-nDfDnsyllY-riemannian-dueling/tree/orx/theorem-contracts-and-rrdngd-source-audit) | Exact contracts and Algorithm 2 counterexample | `uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py` | C2 FALSIFIED as printed | HF cpu-upgrade |
| [dense SPD](https://github.com/MachineLearning-Nerd/icml26-repro-nDfDnsyllY-riemannian-dueling/tree/orx/dense-spd-karcher-rdngd) | Replace diagonal shortcut with comparison-only RDNGD | `uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py` | C6 VERIFIED scope | HF cpu-upgrade |
| [calibrated applications](https://github.com/MachineLearning-Nerd/icml26-repro-nDfDnsyllY-riemannian-dueling/tree/orx/calibrated-cpu-vgg-sphere-attack) | Pinned VGG/CIFAR sphere attack and `SO(2)` | `uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py` | attack 3/4; `SO(2)` 19/19 | HF cpu-upgrade |
| [winning scientific node](https://github.com/MachineLearning-Nerd/icml26-repro-nDfDnsyllY-riemannian-dueling/tree/orx/held-out-rdngd-nonconvex-resource-calibration) | Held-out Claim 1 calibration plus cumulative regression | `uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py` | 9/9 nonconvex, 9/9 convex; all inherited checks pass | HF cpu-upgrade, 266.79 s |

## Environment

Python 3.12 with one repository `.venv`, managed by `uv`; dependencies are
pinned in `uv.lock`.

```bash
uv sync --locked
uv run --locked python repro/src/verify.py
uv run --locked python repro/src/publication_gate.py
uv run --locked marimo edit notebooks/riemannian_dueling_reproduction.py
```

The paper source audit is in [docs/SOURCE_AUDIT.md](docs/SOURCE_AUDIT.md).
