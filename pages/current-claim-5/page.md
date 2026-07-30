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

The exact `SO(2)` optimizer corrected all 19 deterministic tilts below `1e-5`
in 100 comparison-only steps. Reversed signs left maximum best loss `0.1991`.

**Reproduce.**

```bash
uv run --locked python repro/src/verify.py && uv run --locked python repro/src/publication_gate.py
```

- [Raw result and asset hashes](../../outputs/claim5.json)
- [Independent artifact checker](../../reproduction/verify_claims.py)
- [Full application generator](../../reproduction/real_applications.py)
- Source: Section 5.2.1–5.2.2

Checkpoint SHA-256 begins `eaeebf42`; CIFAR dataset revision
`0b2714987fa478483af9968de7c934580d0bb9a2`. Evidence run
`7443fdc4-50fb-4443-8915-f5dc0ab9d5f8`, seed 20260730. HF `cpu-upgrade`:
estimated 8 cores, 64 logical CPUs allocated, PyTorch limited to 8 threads;
route runtime 168.17 s.

**Limitations.** The paper does not identify its checkpoint or indices. HLW
pixels require a separate non-transferable license, so the `SO(2)` route uses
deterministic tilt annotations and is not labeled an HLW-image reproduction.
