# Source audit

The detailed primary-source record is [`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md).

## Pinned source

| Source | Identifier/hash | Role |
| --- | --- | --- |
| Paper | [arXiv:2603.00023](https://arxiv.org/abs/2603.00023) | Claim wording and theorem source |
| OpenReview | [nDfDnsyllY](https://openreview.net/forum?id=nDfDnsyllY) | Submission record |
| Retained source archive | `1df1a267c036a4ef161c02719c4b88bb4cb321099d10b5ac3485a97a51e1a71d` | Primary source archive recorded by the repository |
| Navigable ar5iv source | `1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323` | Claim 4 source anchors |

The audited implementation is the paper's named RDNGD/RRDNGD/RDFW family as
represented by the repository's clean-room and package mirrors. The source
archive, generated outputs, run IDs, and publication hashes remain under
`docs/`, `outputs/`, `pages/`, `reports/`, and `reproduction/`.

## Version and scope notes

- Claim 2 must retain both the intended proof-consistent theorem and the
  printed Algorithm 2 schedule defect.
- Claim 4's superseded finite-ν cells used vacuous `gamma_x` values and are
  not a counterexample; the current non-vacuous sweep is the evidence target.
- Claim 5's calibrated VGG route uses pinned public assets and explicit
  substitutions; the exact paper-setting attack and HLW annotations remain
  blocked.
- Finite experiments corroborate the named mechanisms but do not replace the
  paper's universal proofs.
