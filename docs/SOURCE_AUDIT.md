# Primary-source audit

Paper: **Riemannian Dueling Optimization**, OpenReview `nDfDnsyllY`, arXiv
[`2603.00023`](https://arxiv.org/abs/2603.00023).

Pinned public source archive SHA-256:
`1df1a267c036a4ef161c02719c4b88bb4cb321099d10b5ac3485a97a51e1a71d`.

| Claim | Source anchor | Full-scope CPU route |
|---|---|---|
| C1 | Table 1; RDNGD Theorems | Literal `dε⁻²` / `dε⁻¹` schedules and sphere implementation |
| C2 | Table 1; RRDNGD theorem | Restart schedule and `d log(1/ε)` complexity check |
| C3 | Table 1; RDFW theorem/Algorithm | Batch growth, `2/(k+3)` update, and oracle-sum identity |
| C4 | Lemmas 3.1–3.2 | Independent Monte Carlo comparison-direction estimator on spheres |
| C6 | Source synthetic section | Rayleigh (`d=100,150`), Karcher/SPD (`n=5,10,m=50`), and SO(2) leveling constructions |

## C5 boundary

C5 specifies a VGG/CIFAR-10 black-box attack. The source gives high-level
parameters and cites an external Zeroth-order Riemannian repository, but omits
the authors' RDNGD modifications, VGG checkpoint/version, selected images, and
the processed benchmark state. The bundled archive includes rendered figures,
not executable results. A clean-room classifier attack would be a proxy, so C5
will remain explicitly unsupported unless the original artifacts are found.

Finite executions validate construction mechanisms and controls; they do not
claim to independently prove the paper's universal theorems.
