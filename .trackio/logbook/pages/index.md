# Repro - Riemannian Dueling Optimization

## Pages

| Page |
| --- |
| [Claim 1 — RDNGD](#/claim-1-rdngd) |
| [Claim 2 — RRDNGD](#/claim-2-rrdngd) |
| [Claim 3 — RDFW](#/claim-3-rdfw) |
| [Claim 4 — Comparison estimator](#/claim-4-comparison-estimator) |
| [Claim 5 — CIFAR attack](#/claim-5-cifar-attack) |
| [Claim 6 — Synthetic manifolds](#/claim-6-synthetic-manifolds) |
| [Methods](#/methods) |
| [Negative controls](#/negative-controls) |
| [Conclusion](#/conclusion) |


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_5d89210ff978", "created_at": "2026-07-29T12:55:29+00:00", "title": "Executive summary"}
-->
Five source-complete anchored claims pass for Riemannian Dueling Optimization.

The full 50,000-step sphere protocol at d=100 and d=150 reaches gaps 8.0e-7 and 1.7e-5; exact schedule, restart, Frank-Wolfe, estimator, SPD, and SO(2) controls pass.

C5 is intentionally unclaimed: the author-modified CIFAR/VGG attack stack is not released.
