# Claim-to-evidence ledger

The six claims are evaluated by executable theorem audits, calibrated
experiments, independent checkers, and negative controls. The verdicts below
describe the current evidence scope; they are not formal proofs of universal
theorems.

| Claim | Verdict | How the claim is produced | Primary evidence |
| --- | --- | --- | --- |
| C1. RDNGD complexity | `VERIFIED_SCOPED` | Build symbolic `O(d ε⁻²)`/`O(d ε⁻¹)` certificates, calibrate resources on six seeds, then validate 9 nonconvex and 9 convex held-out cells with 20 untouched seeds. | [`repro/src/theorem_audit.py`](repro/src/theorem_audit.py), [`repro/src/empirical_algorithms.py`](repro/src/empirical_algorithms.py), [`outputs/claim1.json`](outputs/claim1.json) |
| C2. RRDNGD linear convergence | `VERIFIED_INTENDED_THEOREM_PRINTED_SCHEDULE_FALSIFIED` | Compare the printed restart schedule with the proof-consistent schedule on `f(x)=x²/2`, then check log₂ error slopes and dimension-linear phase costs. The printed schedule ends at `8.02e-5` for a `1e-6` target; the corrected control reaches `2.26e-16`. | [`outputs/claim2.json`](outputs/claim2.json), [`pages/current-claim-2/page.md`](pages/current-claim-2/page.md) |
| C3. Projection-free RDFW | `VERIFIED_SCOPED` | Run the named zero-projection RDFW update, verify the exact oracle-sum identity, and require reversed comparison signs to degrade. At intrinsic `d=15`, median suboptimality falls from `1.86e-2` to `3.74e-4`. | [`repro/src/empirical_algorithms.py`](repro/src/empirical_algorithms.py), [`outputs/claim3.json`](outputs/claim3.json) |
| C4. Comparison-based estimator | `VERIFIED_SCOPED` | Check the ideal Lemma 3.2 identity and constants independently, then run 13 non-vacuous Lemma 3.1 cells with 2,000,000 directions each and tightened-bound/sign-blind controls. The older finite-ν falsification is withdrawn because its `gamma_x` values were `≥1`. | [`repro/src/lemma31_perturbation.py`](repro/src/lemma31_perturbation.py), [`repro/src/verify_claim4.py`](repro/src/verify_claim4.py), [`outputs/current_claim4.json`](outputs/current_claim4.json), [`pages/current-claim-4/page.md`](pages/current-claim-4/page.md) |
| C5. Applications | `VERIFIED_MECHANISM_PAPER_SETTING_BLOCKED` | Run a calibrated comparison-only VGG/CIFAR route and the paper's SO(2) comparison objective with reversed-sign controls. The calibrated route changes 3/4 predictions and SO(2) succeeds on 19/19 deterministic tilts; the exact `nu=eta=1e-6` attack and licensed HLW annotations remain unavailable. | [`repro/src/real_applications.py`](repro/src/real_applications.py), [`outputs/claim5.json`](outputs/claim5.json) |
| C6. Synthetic applications | `VERIFIED_SCOPED` | Run held-out sphere Rayleigh RDNGD and comparison-only RDNGD on dense noncommuting SPD matrices against independent Karcher references. Relative gaps are `6.73e-6` and `2.45e-5`; reversed controls fail as intended. | [`repro/src/sphere_rayleigh.py`](repro/src/sphere_rayleigh.py), [`repro/src/dense_spd.py`](repro/src/dense_spd.py), [`outputs/claim6.json`](outputs/claim6.json) |

## Branch-to-evidence map

`main` is the landing page and current evidence surface. The 18 supporting
branches are clean `audit/`, `experiment/`, `integration/`, and `release/`
names; their historical `orx/*` names and exact roles are recorded in
[`branch-audit.md`](branch-audit.md). The most important paths are:

- [`audit/theorem-contracts-rrdngd`](https://github.com/MachineLearning-Nerd/icml26-riemannian-dueling-optimization/tree/audit/theorem-contracts-rrdngd) — C1/C2 source and theorem contracts.
- [`audit/lemma-3-1-gamma-calibration`](https://github.com/MachineLearning-Nerd/icml26-riemannian-dueling-optimization/tree/audit/lemma-3-1-gamma-calibration) — corrected non-vacuous C4 sweep.
- [`experiment/calibrated-vgg-attack`](https://github.com/MachineLearning-Nerd/icml26-riemannian-dueling-optimization/tree/experiment/calibrated-vgg-attack) — C5 calibrated application route.
- [`experiment/dense-spd-karcher`](https://github.com/MachineLearning-Nerd/icml26-riemannian-dueling-optimization/tree/experiment/dense-spd-karcher) — C6 noncommuting SPD route.
- [`release/final-reference-aligned`](https://github.com/MachineLearning-Nerd/icml26-riemannian-dueling-optimization/tree/release/final-reference-aligned) — final reference-aligned release metadata.

## Score and publication boundary

The previous live score was `3/12`. A forecast of `9/12–12/12` is historical
planning context only. No current score increase, official author endorsement,
or leaderboard result is claimed.
