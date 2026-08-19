# Riemannian Dueling Optimization

Independent, claim-by-claim CPU reproduction and source audit of:

> Riemannian Dueling Optimization

This repository studies the paper's algorithms and evidence contracts. It is
not a replacement for the paper's proofs, and application results with
explicit substitutions are labelled as such.

## Paper

- [arXiv:2603.00023](https://arxiv.org/abs/2603.00023)
- [HTML paper](https://arxiv.org/html/2603.00023)
- [OpenReview record](https://openreview.net/forum?id=nDfDnsyllY)

The paper formulates optimization on Riemannian manifolds when the objective is
available only through pairwise comparisons. It introduces Riemannian Dueling
Normalized Gradient Descent (RDNGD), its restarted strongly-convex variant
(RRDNGD), and the projection-free Riemannian Dueling Frank-Wolfe method
(RDFW), followed by synthetic and application experiments.

## Current status

**Evidence status: resolved, awaiting a new live judge result.** The prior live
score was 3/12; this repository does not claim a score increase until a live
evaluator records one. The current evidence release is recorded in
`outputs/verdict.json` and uses CPU-only runs. The current machine-readable disposition is in
[`claims.json`](claims.json), the claim ledger is in
[`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md), and the final public-state check is
[`verify_final.py`](verify_final.py).

Overall status:
`PARTIAL_C1_C3_C4_C6_VERIFIED_C2_PRINTED_SCHEDULE_FALSIFIED_C5_MECHANISM_VERIFIED_PAPER_SETTING_BLOCKED`.
`current_score_claim=false`, `publication_allowed=false`, and
`official_author_endorsement=false`. The publication gate passed for the
packaged evidence surface; that is not a current judge result.

| Claim | How the claim is produced | Current assessment |
| --- | --- | --- |
| C1 — RDNGD complexity | theorem_audit.py creates symbolic upper-bound certificates; empirical_algorithms.py validates 9 nonconvex and 9 convex held-out cells using six-seed calibration and 20 untouched validation seeds. | VERIFIED for the stated contracts; all 18 held-out cells pass. |
| C2 — RRDNGD linear convergence | theorem_audit.py compares the printed restart schedule with the proof-consistent schedule on f(x)=x²/2, then measures log2 error slopes and dimension-linear phase costs. | Intended theorem VERIFIED; the printed Algorithm 2 schedule is FALSIFIED. It leaves an 8.02e-5 gap for a 1e-6 target, while the corrected control reaches 2.26e-16. |
| C3 — projection-free RDFW | empirical_algorithms.py runs the named RDFW update with zero projection calls; theorem_audit.py checks the exact oracle-sum identity and reversed-sign control. | VERIFIED. At intrinsic d=15, median suboptimality falls from 1.86e-2 to 3.74e-4 over horizons 10 to 80. |
| C4 — comparison-based estimator | lemma31_perturbation.py tests the non-vacuous Lemma 3.1 bound; verify_claim4_source.py checks the ideal Lemma 3.2 identity and constants; verify_claim4.py checks both. | VERIFIED for the ideal identity and non-vacuous finite-perturbation guarantee. An earlier finite-nu falsification is withdrawn because its gamma_x bound was vacuous (gamma_x ≥ 1). |
| C5 — applications | real_applications.py runs comparison-only VGG/CIFAR and SO(2) routes with reversed-sign controls and records asset hashes. | VERIFIED for the application mechanism and stated scope: calibrated attack changes 3/4 predictions and SO(2) corrects 19/19 deterministic tilts. The exact paper-setting attack is BLOCKED and HLW image annotations are unavailable. |
| C6 — synthetic applications | sphere_rayleigh.py runs held-out sphere Rayleigh RDNGD; dense_spd.py runs comparison-only RDNGD against independent dense SPD Karcher references. | VERIFIED for the demonstrated scope: 50,000-duel sphere runs at d=100,150 and dense SPD relative gaps 6.73e-6 and 2.45e-5 at n=5,10. |

The statuses above are evidence adjudications, not formal proofs of
universally quantified theorems. The canonical machine-readable aggregation is
outputs/verdict.json; detailed claim pages are under pages/current-claim-* and
the narrative audit is reports/reproduction/report.md.

## Evidence production

The repository has two related paths:

- repro/src/ is the current verifier and publication gate.
- reproduction/ is the independently checkable/downloaded package mirror.

The root verifier runs the claim-specific modules, writes outputs/claim*.json
and outputs/verdict.json, and checks negative controls. The publication gate
checks the packaged release, hashes, traversal, and visible evidence paths.

The principal claim-to-code paths are:

| Evidence | Code and artifacts |
| --- | --- |
| C1 and C2 theorem contracts | repro/src/theorem_audit.py, outputs/claim1.json, outputs/claim2.json |
| C1 empirical RDNGD cells and C3 RDFW | repro/src/empirical_algorithms.py, outputs/claim3.json |
| C4 Lemmas 3.1 and 3.2 | repro/src/lemma31_perturbation.py, repro/src/verify_claim4.py, repro/src/verify_claim4_source.py, outputs/current_claim4.json |
| C5 applications | repro/src/real_applications.py, outputs/claim5.json |
| C6 applications | repro/src/sphere_rayleigh.py, repro/src/dense_spd.py, outputs/claim6.json |
| Release consistency | repro/src/verify.py, repro/src/publication_gate.py, reports/release/candidate_manifest.sha256 |

## Reproduce

The full CPU verification is resource-intensive and was executed on a
cpu-upgrade environment. It is not a lightweight smoke test.

    uv sync --locked
    uv run --locked python repro/src/verify.py
    uv run --locked python repro/src/publication_gate.py

The independent package checks are:

    python reproduction/verify_claims.py
    python reproduction/verify_claim4.py
    cd reproduction
    uv run --locked python cumulative_verify.py
    uv run --locked python publication_gate.py

No GPU is required. The notebook is
notebooks/riemannian_dueling_reproduction.py, and the visual report is
reports/reproduction/report.md.

## Branches

The original exploration branches were generated with the orx/ prefix. They
are being replaced with descriptive audit, experiment, integration, and
release names. The complete old-to-new mapping, purpose, and evidence role of
all branches is in branch-audit.md.

At a high level:

- audit/* records theorem contracts, estimator corrections, controls, and
  evaluator audits.
- experiment/* records calibrated algorithm and application runs.
- integration/* combines theory and calibrated evidence.
- release/* records packaging, publication, and final evidence gates.
- main is the public landing page and current evidence surface.

## Citation

If this reproduction or audit is useful, please cite:

    @article{ren2026riemannian,
      title={Riemannian Dueling Optimization},
      author={Ren, Yuxuan and Roy, Abhishek and Ma, Shiqian},
      journal={arXiv preprint arXiv:2603.00023},
      year={2026},
      doi={10.48550/arXiv.2603.00023}
    }

## Thank you

Thank you to Yuxuan Ren, Abhishek Roy, and Shiqian Ma for sharing this work
and for making the mathematical and algorithmic ideas concrete enough to
audit. This repository is an independent reproduction and is not affiliated
with or endorsed by the authors.

## Limitations and attribution

- The paper's proofs are not re-proved by these experiments.
- The exact VGG checkpoint, evaluated image indices, and author-modified
  benchmark state are not specified; the calibrated route pins public assets
  and records their hashes.
- The paper-setting attack route remains BLOCKED rather than falsified.
- HLW image annotations are request-gated; the SO(2) result uses deterministic
  tilts with the paper's own comparison objective.
- The superseded finite-nu artifact is retained as a consistency record, not a
  counterexample.

No license is declared in this repository. Changes in this repository are
attributed to MachineLearning-Nerd.
