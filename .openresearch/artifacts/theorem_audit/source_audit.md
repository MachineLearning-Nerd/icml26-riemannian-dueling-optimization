# Theorem source audit

Primary source: `https://ar5iv.labs.arxiv.org/html/2603.00023`, retrieved
2026-07-30 UTC with an explicit browser user agent. SHA-256:
`1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323`.

| Claim | Source anchor | Assumptions and quantifier |
| --- | --- | --- |
| 1 nonconvex | `#S3.Thmtheorem6` | Any epsilon>0; geodesically L-smooth; X=M; existence of x-star via D |
| 1 convex | `#S3.Thmtheorem7` | Any epsilon>0; L-smooth, geodesically convex, bounded X; Assumptions 2.5–2.6 |
| 2 | `#S3.Thmtheorem10`, `#alg2`, Appendix F | Any epsilon>0; L-smooth, alpha-strongly convex, bounded X; Assumptions 2.5–2.6; interior optimum |
| 3 | `#S4.Thmtheorem1`, `#alg3` | Any epsilon>0; L-smooth and geodesically convex; LMO constraint handling |

Theorem 3.10 prints
`epsilon_k = alpha D / 2^(2-k)`. Appendix F instead requires
`epsilon_k = alpha D_k/4` with `D_k=D/2^k`, hence
`epsilon_k = alpha D/2^(k+2)`. Their ratio is `2^(2k)`.
