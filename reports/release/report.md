# Reference-aligned six-claim release

- Previous live judged score: `3/12`
- Conservative projected score range after the change: `10/12–12/12`
- Best-supported possible new score: `12/12` **forecast only**

The live verdict dataset still points to judged Space revision
`8b6af91db9ee5e195f24aec73e9d96bb304113fc`, judged on
2026-07-30. The new revision has not been judged.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 0/2 | 2/2 | HIGH | VERIFIED | Symbolic upper-bound certificate and 18 held-out RDNGD cells; finite experiments alone do not prove universal scope. |
| 2 | 0/2 | 2/2 | HIGH | VERIFIED | Corrected RRDNGD slopes are -1.003, -0.995, and -1.039 with dimension-linear phase cost; the printed schedule is separately FALSIFIED. |
| 3 | 0/2 | 2/2 | HIGH | VERIFIED | Named projection-free RDFW sweep, reversed-sign control, and exact oracle-sum certificate. |
| 4 | 2/2 | 2/2 | HIGH | FALSIFIED | The ideal identity remains VERIFIED; an assumption-satisfying finite-ν counterexample falsifies unqualified finite-perturbation unbiasedness. |
| 5 | 0/2 | 2/2 | MEDIUM | VERIFIED | Comparison-only VGG attack changes 3/4 predictions and SO(2) succeeds 19/19; checkpoint/settings substitutions and unavailable licensed HLW pixels remain explicit. |
| 6 | 1/2 | 2/2 | HIGH | VERIFIED | Dense noncommuting SPD RDNGD at n=5,10 and m=50 reaches relative reference gaps below 2.5e-5. |

Current total score: 3/12. Claims 1–3 and 5–6 gained direct evidence; Claim 4
was strengthened with exact finite-ν adjudication. No whole claim remains
BLOCKED. The exact paper-setting attack and licensed HLW-image route remain
limited subroutes.

## Publication

- Existing Space only: `DineshAI/nDfDnsyllY`
- Previous Space head: `d5b25eaf0ca7e62f1d9ac666bd11fab7dd936b5b`
- Published Space revision:
  `889b4f1b32262f52aef3553ea5cc1daa5d0d57c1`
- Winning experiment branch: `orx/evaluator-blind-audit-transcript`
- Winning Git SHA: `772a4d264cc633d2ecd91008a87b78cb3d828c49`
- Winning HF run: `5e3afd6e-cb47-4358-b619-a75887ba7475`
- GitHub exact-path mirror commit:
  `08d1a20b15dcfa91ba57edee61223a0b05e6759a`
- State: awaiting live judge

The upload used the Hugging Face commit API with a parent-head assertion and
exactly 28 UTF-8 text additions. No Space was created.

## Experiment tree

The frozen baseline descended through theorem contracts, executable
RDNGD/RRDNGD/RDFW, dense SPD, paper-setting and calibrated applications,
held-out calibration, the evaluator-visible candidate, finite-ν estimator
adjudication, six-claim alignment, self-contained Space packaging, and the
final evaluator-blind transcript node. Completed experiment branches were
never rewritten.

Every node inherited exactly:

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
```

Final release-oriented launches were:

```bash
orx exp run d690eceb-d43d-409a-8fa0-8828a3c383d6 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run ac5dcf1e-ea84-45dc-bf8c-6e89185e7755 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run e7e5d0d5-ded1-4c21-a233-1e374e8a024e --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run 8d5d70fd-4185-4777-925f-1ff72c2e1037 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp run 75054272-f088-41c8-b52b-c8e7b780200c --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
```

The candidate was built and checked with:

```bash
uv run --locked python repro/src/package_space.py <exact-current-clone> <candidate>
python reproduction/verify_claims.py
python reproduction/verify_claim4.py
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

`orx exp status`, `orx exp wait`, `orx runs`, and `orx logs` supplied the
recorded branch, terminal-state, runtime, and claim evidence. Read-only Git,
`rg`, `jq`, SHA-256, JSON, import, subset, secret, and navigation checks were
used for the release audit.

## Compute and cost

The winning run estimated 8 computational cores, received 64 logical CPUs on
HF `cpu-upgrade`, used no GPU, and reported 473.5088 seconds of scientific
runtime. HF reported 507 running seconds. At the documented USD 0.03/hour,
minute-rounded cost is approximately USD 0.0045.

Across 22 HF `cpu-upgrade` attempts, displayed wall time totals 6,853 seconds
(114.22 minutes). Treating all displayed time as billable gives a conservative
cost upper estimate of USD 0.0571; the exact invoice is not exposed by `orx`.
Local work was limited to short single-core syntax, static-checker, packaging,
hash, and traversal tasks; no scientific experiment ran locally.

## Release audit

- Exact current Space clone: 46 files.
- Exact published clone: 48 files.
- Old/current file-set subset: 46/46 paths present.
- Immutable judged historical page hashes: preserved.
- Uploaded hashes: 28/28 match `candidate_manifest.sha256`.
- Static Claim 1–6 checker: passed.
- Finite-ν Claim 4 checker: passed.
- Packaged-Space root/import smoke: passed.
- Secret pattern scan: passed.
- Evaluator-blind traversal: passed, 23 files opened and enumerated on the
  canonical visibility page.
- Current verifier is the `logbook.json` root; historical rejected evidence is
  nested beneath it.

## Exact upload allowlist

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
reproduction/finite_nu_estimator.py
reproduction/cumulative_verify.py
reproduction/publication_gate.py
reproduction/protected_space_8b6af91_manifest.sha256
reproduction/pyproject.toml
reproduction/uv.lock
```
