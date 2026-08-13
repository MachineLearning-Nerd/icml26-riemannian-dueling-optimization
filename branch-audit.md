# Branch audit

The original branches were generated with the orx/ prefix. The renamed
branches describe whether a ref is an audit, experiment, integration, or
release surface. Historical evidence is preserved; only the branch labels are
cleaned.

| New branch | Previous branch | Purpose and evidence role |
| --- | --- | --- |
| main | main | Current public landing page and latest evidence surface. |
| audit/judged-baseline | orx/judged-baseline-3-of-12 | Freezes the original judged 3/12 state and environment. |
| audit/theorem-contracts-rrdngd | orx/theorem-contracts-and-rrdngd-source-audit | Audits the theorem symbols and exposes the printed RRDNGD schedule defect. |
| audit/claim-4-contract | orx/claim-4-evaluator-visible-contract | Makes the original evaluator-visible Claim 4 contract explicit. |
| experiment/calibrated-core-algorithms | orx/calibrated-rdngd-rrdngd-rdfw-runs | Runs calibrated RDNGD, RRDNGD, and RDFW algorithm evidence. |
| integration/theory-and-algorithms | orx/combined-theory-and-calibrated-algorithms | Combines theorem-contract checks with calibrated algorithms. |
| experiment/dense-spd-karcher | orx/dense-spd-karcher-rdngd | Replaces a diagonal shortcut with comparison-only RDNGD on dense SPD Karcher means. |
| experiment/paper-setting-applications | orx/paper-setting-cpu-applications | Tests the literal CPU application settings; the VGG route remains blocked. |
| experiment/calibrated-vgg-attack | orx/calibrated-cpu-vgg-sphere-attack | Pins public VGG/CIFAR assets and calibrates the comparison-only sphere attack. |
| audit/held-out-rdngd-calibration | orx/held-out-rdngd-nonconvex-resource-calibration | Calibrates RDNGD resources on held-out nonconvex seeds. |
| release/evaluator-visible-cumulative | orx/evaluator-visible-cumulative-release-candidate | Packages the cumulative evaluator-visible six-claim evidence. |
| audit/finite-nu-estimator | orx/finite-nu-estimator-bias-adjudication | Audits finite-perturbation estimator bias and records the superseded result. |
| audit/lemma-3-1-gamma-calibration | orx/lemma-3-1-gamma-x-calibration-and-claim-4-correc | Tests Lemma 3.1 in non-vacuous gamma_x regimes and withdraws the invalid counterexample. |
| release/record-final-evidence | orx/record-lemma-3-1-evidence-and-close-claim-5-6-fi | Records final Lemma 3.1 evidence and closes the Claim 5/6 evidence paths. |
| release/six-claim-adjudication | orx/evaluator-aligned-six-claim-adjudication | Aligns all six claim contracts and produces the cumulative adjudication. |
| release/self-contained-space | orx/self-contained-space-release-gate | Makes the packaged evaluator surface self-contained and gate-checkable. |
| release/corrected-six-claim-gate | orx/release-gate-for-the-corrected-six-claim-candida | Enforces negative controls and corrected six-claim release checks. |
| audit/evaluator-blind-transcript | orx/evaluator-blind-audit-transcript | Records the evaluator-blind release audit and visible evidence traversal. |
| release/final-reference-aligned | orx/final-reference-aligned-release-metadata | Binds the final release metadata to reference-aligned evidence. |

## Claim-to-code map

| Claim | Primary code | Raw evidence |
| --- | --- | --- |
| C1 RDNGD complexity | repro/src/theorem_audit.py and repro/src/empirical_algorithms.py | outputs/claim1.json and pages/current-claim-1/page.md |
| C2 RRDNGD convergence | repro/src/theorem_audit.py and repro/src/empirical_algorithms.py | outputs/claim2.json and pages/current-claim-2/page.md |
| C3 RDFW | repro/src/theorem_audit.py and repro/src/empirical_algorithms.py | outputs/claim3.json and pages/current-claim-3/page.md |
| C4 estimator | repro/src/lemma31_perturbation.py and repro/src/verify_claim4.py | outputs/current_claim4.json and pages/current-claim-4/page.md |
| C5 applications | repro/src/real_applications.py | outputs/claim5.json and pages/current-claim-5/page.md |
| C6 applications | repro/src/sphere_rayleigh.py and repro/src/dense_spd.py | outputs/claim6.json and pages/current-claim-6/page.md |

Every experiment branch inherits the locked command:

    uv run --locked python repro/src/verify.py
    uv run --locked python repro/src/publication_gate.py

The release branches additionally check package hashes, evaluator-visible
navigation, negative controls, and the self-contained publication surface.
