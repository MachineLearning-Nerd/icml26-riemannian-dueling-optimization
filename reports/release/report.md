# Release forecast — Riemannian Dueling Optimization

- Previous live judged score: `3/12`
- Conservative projected score range after the proposed change: `9/12–12/12`
- Best-supported possible new score: `12/12` **forecast, not a judge result**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 0 | 2 | HIGH | VERIFIED | SymPy certificates reconstruct both rates; 18/18 held-out RDNGD cells pass. Risk: evaluator interpretation of proof scope. |
| 2 | 0 | 2 | HIGH | VERIFIED intended; printed defect FALSIFIED | Corrected RRDNGD slopes are near -1 bit/phase with dimension-linear cost; literal schedule fails a valid counterexample. |
| 3 | 0 | 2 | HIGH | VERIFIED | Symbolic oracle sum plus actual zero-projection RDFW sweep. Risk: `d=3` is floor-limited and excluded from the slope conclusion. |
| 4 | 2 | 2 | HIGH | FALSIFIED AS WRITTEN; ideal VERIFIED | Existing full-credit ideal Monte Carlo is preserved; finite-nu paired-bias lower bounds remain strictly positive with two zero-disagreement controls. |
| 5 | 0 | 2 | MEDIUM | VERIFIED for mechanism | Pinned VGG sphere attack succeeds 3/4 and `SO(2)` succeeds 19/19. Risk: calibrated settings differ and licensed HLW pixels are unavailable. |
| 6 | 1 | 2 | HIGH | VERIFIED for scope | Actual comparison-only RDNGD on dense noncommuting SPD inputs at paper dimensions. Risk: application evidence does not prove every manifold class. |

Current total score: `3/12`.

Conservative projected total score range: `9/12–12/12`.

Best-supported possible total score: `12/12` forecast only.

Claims 1, 2, 3, 5, and 6 have materially changed since the previous judge
result. Claim 4's prior ideal-estimator evidence is preserved and rerun, with
an added finite-perturbation falsification route.

No overall claim remains BLOCKED. The exact-setting Claim 5 attack subroute is
BLOCKED at 0/2 images, and the HLW image route is unavailable because the
dataset requires a separate non-transferable license. Those limitations remain
inline on the canonical page.

The publication action, after the final cumulative gate and evaluator-blind
review pass, is a text-only commit to the existing
`DineshAI/nDfDnsyllY` Space, followed by an exact-revision download and hash
verification. No second Space will be created.

## Evaluator visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `current-claim-1` | yes | yes | yes | yes | yes | yes | VERIFIED |
| 2 | `current-claim-2` | yes | yes | yes | yes | yes | yes | VERIFIED intended; printed defect FALSIFIED |
| 3 | `current-claim-3` | yes | yes | yes | yes | yes | yes | VERIFIED |
| 4 | `current-claim-4` | yes | yes | yes | yes | yes | yes | FALSIFIED AS WRITTEN; ideal VERIFIED |
| 5 | `current-claim-5` | yes | yes | yes | yes | yes | yes, deviations inline | VERIFIED mechanism |
| 6 | `current-claim-6` | yes | yes | yes | yes | yes | yes | VERIFIED scope |
