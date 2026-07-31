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

Publication is complete. A text-only commit was made to the existing
`DineshAI/nDfDnsyllY` Space; no second Space was created. The exact published
revision is `d5b25eaf0ca7e62f1d9ac666bd11fab7dd936b5b`. It was downloaded into a
fresh directory, all uploaded hashes were checked, and the evaluator-visible
traversal passed. The paper is awaiting the live judge.

## Evaluator visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `current-claim-1` | yes | yes | yes | yes | yes | yes | VERIFIED |
| 2 | `current-claim-2` | yes | yes | yes | yes | yes | yes | VERIFIED intended; printed defect FALSIFIED |
| 3 | `current-claim-3` | yes | yes | yes | yes | yes | yes | VERIFIED |
| 4 | `current-claim-4` | yes | yes | yes | yes | yes | yes | FALSIFIED AS WRITTEN; ideal VERIFIED |
| 5 | `current-claim-5` | yes | yes | yes | yes | yes | yes, deviations inline | VERIFIED mechanism |
| 6 | `current-claim-6` | yes | yes | yes | yes | yes | yes | VERIFIED scope |

## Release identity

- Baseline branch and initial SHA: `main` at
  `bf02817115e1c048edb33f8c4db8419ec0653cb8`
- Previous HF Head and Judge Head:
  `8b6af91db9ee5e195f24aec73e9d96bb304113fc`
- Winning experiment:
  `orx/evaluator-visible-cumulative-release-candidate`
- Winning scientific SHA:
  `73c4b84239cbcc71549f64c22ce0dcd7700c64e5`
- Winning run: `c7711be1-ba38-4dce-af0d-503b167f27d8`
- Published HF revision:
  `d5b25eaf0ca7e62f1d9ac666bd11fab7dd936b5b`
- GitHub `main` after the exact Space mirror:
  `f063e5fd8c462a7a368ea82199d49034161970c7`

The fixed command inherited by every experiment was:

```console
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
```

Every remote run used Hugging Face `cpu-upgrade` with
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. The winning run estimated
eight computational cores, received 64 logical CPUs, restricted PyTorch to
eight threads and BLAS to one thread, and recorded 232.086 seconds of
scientific runtime (259 seconds wall time).

## Experiment tree

The campaign grew downward from the frozen judged baseline:

1. judged baseline;
2. Claim 4 preservation and executable contract;
3. calibrated RDNGD, RRDNGD, and RDFW implementations;
4. theorem contracts and the RRDNGD source audit;
5. combined cumulative verifier;
6. dense noncommuting SPD Karcher experiment;
7. exact paper-setting CPU applications;
8. calibrated VGG sphere attack and `SO(2)` leveling;
9. held-out Claim 1 resource calibration;
10. evaluator-visible cumulative release candidate.

Every accepted child reran the previously accepted checks. The final
cumulative run passed all scientific checks and the publication gate.

## Claim results

- Claim 1 — **VERIFIED**: independently reconstructed symbolic certificates
  and 18/18 held-out RDNGD resource cells.
- Claim 2 — **FALSIFIED as printed**: an assumption-satisfying exact
  counterexample fails the printed recurrent schedule; the corrected
  Appendix-F schedule is the passing control. This does not claim that all
  possible corrected formulations are false.
- Claim 3 — **VERIFIED**: symbolic oracle accounting and an actual
  projection-free RDFW sweep.
- Claim 4 — **VERIFIED**: the prior full-credit Monte Carlo check is preserved,
  rerun, and checked independently.
- Claim 5 — **VERIFIED for the comparison-only mechanism**: the calibrated
  pinned VGG attack succeeds on 3/4 images and the `SO(2)` experiment succeeds
  on 19/19. Exact paper settings and licensed HLW pixels remain explicit
  limitations.
- Claim 6 — **VERIFIED for the stated synthetic applications**: real
  comparison-only runs cover the sphere and dense, noncommuting SPD Karcher
  instances at the paper dimensions.

## Runtime and cost

All 16 experiment attempts used HF `cpu-upgrade`. Their displayed wall times
sum to 3,454 seconds (57 minutes 34 seconds), including six diagnostic or
environmental failures. Per-job minute rounding gives 67 billable minutes.
At the published `cpu-upgrade` price of USD 0.03/hour, the estimated campaign
compute charge is **USD 0.0335**. The exact invoice is not exposed by `orx`.
Successful runs account for 21 minutes 20 seconds of displayed wall time;
the remainder is primarily the failed first CIFAR download attempt.

Local execution was limited to one-core, sub-five-minute inspection,
hashing, syntax checks, report generation, and `marimo check`. No local
training or multithreaded experiment was run.

## Commands and evidence

The scientific command above is copied verbatim from `orx exp status`. The
orchestration and release command sequence was:

```console
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs f417b2c7-9ee1-470d-94c9-312c62d71454
orx create-experiment f417b2c7-9ee1-470d-94c9-312c62d71454 ...
orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp wait <experiment-id> --timeout 480
orx logs <run-id>
orx exp desc <experiment-id> --set <evidence-summary>
uv run --locked marimo check --strict notebooks/riemannian_dueling_reproduction.py
git ls-remote origin refs/heads/main
```

The omitted arguments in `create-experiment`, and the concrete experiment and
run IDs, are preserved in the OpenResearch tree descriptions and run table;
they do not alter the fixed scientific command. Source retrieval used an
explicit browser User-Agent. The paper HTML was retrieved on 2026-07-30 with
SHA-256
`1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323`.

Durable internal evidence is under `.openresearch/artifacts/claim1` through
`.openresearch/artifacts/claim6`. Evaluator-visible evidence begins at
`logbook.json`, leads to `pages/current-verification/page.md`, and exposes the
canonical claim pages, raw JSON, current checkers, controls, environment lock,
CPU allocation, runtime, seeds, limitations, and source anchors.

## Preservation and upload audit

The exact judged Space tree contained 21 files. The published tree contains
46 files; all 21 judged files are an unchanged subset, including historical
page hashes. Current verification appears first in navigation and the former
default page is labeled `Historical rejected baseline`.

The exact text-only upload allowlist was:

```text
logbook.json
pages/current-verification/page.md
pages/current-claim-1/page.md
pages/current-claim-2/page.md
pages/current-claim-3/page.md
pages/current-claim-4/page.md
pages/current-claim-5/page.md
pages/current-claim-6/page.md
pages/visibility-matrix/page.md
outputs/claim1.json
outputs/claim2.json
outputs/claim3.json
outputs/current_claim4.json
outputs/claim5.json
outputs/claim6.json
reproduction/verify_claims.py
reproduction/verify_claim4.py
reproduction/dense_spd.py
reproduction/empirical_algorithms.py
reproduction/real_applications.py
reproduction/theorem_audit.py
reproduction/verify_claim4_source.py
reproduction/cumulative_verify.py
reproduction/publication_gate.py
reproduction/pyproject.toml
reproduction/uv.lock
```

The upload used the Hugging Face text API with the judged revision asserted as
the parent. Post-publication verification checked all 26 uploaded hashes,
reran both evaluator-visible checkers, traversed 22 reachable files from the
canonical entrypoint, matched displayed values to raw data, and repeated the
historical subset test. Result: `POST_PUBLISH_PASS`.
