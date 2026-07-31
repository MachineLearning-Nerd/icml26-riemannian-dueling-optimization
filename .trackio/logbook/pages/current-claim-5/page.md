# Claim 5 — real-world applications

**Exact claim.** Section 5.2 applies comparison-only RDNGD to a VGG/CIFAR-10
black-box attack with sphere-constrained perturbations and to image horizon
leveling on `SO(2)`.

**Verdict: VERIFIED for the application mechanisms.** The optimizer received
only pairwise signs in both routes.

For the attack, a pinned public CIFAR-10 VGG11-BN checkpoint and the first four
correct test inputs were used. The calibrated sphere attack changed three of
four predictions in 1,000 steps (40,000 main duels):

| input | initial true-label margin | final margin | attacked |
| ---: | ---: | ---: | --- |
| 0 | 0.751 | -10.785 | yes |
| 1 | 10.218 | 1.640 | no |
| 2 | 9.561 | -9.718 | yes |
| 3 | 10.270 | -6.702 | yes |

Maximum sphere-radius error was `7.15e-7`. Reversed comparison signs increased
the control margin from `1.860` to `12.700`, failing the attack as intended.

The paper-setting route (`nu=eta=1e-6`, 1,000 steps, batch 10,
radius `0.05||image||`) changed 0/2 labels and remains **BLOCKED**, not
falsified. The successful route used `nu=.01`, `eta=.04`, radius `.5`, and
true-label logit margin.

For horizon leveling, the paper minimizes
`f(R) = ||R R_tilt - I||_F^2` over `SO(2)` and states plainly that, although
dueling feedback "could be obtained from human comparisons", it uses `f(R)`
itself as "a scalable and reproducible surrogate for human preference". This
route therefore uses **the paper's own oracle**, not a substitute for it: the
comparison returns whichever of two rotations has the smaller `f`, and function
values are never revealed. The paper's exact protocol `T = 100`, `nu = 1e-6`,
`eta = 1e-2` is used unchanged.

All 19 tilts were corrected to a best loss of exactly `0.0` (below the `1e-5`
threshold) in 100 comparison-only steps. Reversing the signs leaves a maximum
best loss of `0.3982`.

The one deviation is the source of `R_tilt`. HLW (Workman et al., 2016)
distributes its images *and* its horizon annotations only through a
per-requester access form at `https://mvrl.cse.wustl.edu/datasets/hlw/`, which
was verified to be the sole distribution route, so `R_tilt` could not be
computed from the human annotations. Since `f(R)` depends on `R_tilt` alone and
on no image pixels, 19 deterministic tilt angles spanning the paper's figure
range are substituted; every other element of the experiment is the paper's.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
# Downloaded Space:
cd reproduction && uv run --locked python cumulative_verify.py && uv run --locked python publication_gate.py
```

- [Raw result and asset hashes](../../outputs/claim5.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Full application generator](../../reproduction/real_applications.py)
- Source: Section 5.2.1–5.2.2

Checkpoint SHA-256 begins `eaeebf42`; CIFAR dataset revision
`0b2714987fa478483af9968de7c934580d0bb9a2`. Evidence run
`27332bb6-e56c-42ae-9d9e-4b0a885df123`, Git SHA
`d94d1e7e64e2907c7a8c7a92e1e00dda922fc714`, seed 20260730. HF `cpu-upgrade`:
estimated 8 cores, 64 logical CPUs allocated, PyTorch limited to 8 threads;
route runtime 1154.28 s.

**Limitations.** The paper does not identify its VGG checkpoint or evaluated
indices, so a pinned public CIFAR-10 VGG11-BN checkpoint and the first four
correctly-classified test inputs are used. The paper-setting attack route
(`nu = eta = 1e-6`) remains BLOCKED, not falsified. The `SO(2)` route
reproduces the paper's objective, oracle and protocol exactly but substitutes
deterministic tilt angles for HLW's request-gated human annotations, so it is
not labelled an HLW-image reproduction.
