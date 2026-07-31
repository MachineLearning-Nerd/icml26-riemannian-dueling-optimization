# EVAL — Claim 4

**Verdict: VERIFIED.**

| Sub-claim | Result |
| --- | --- |
| Lemma 3.2 identity and interval | VERIFIED — C_hat 0.8375 / 0.8087 / 0.8017 at d = 5 / 25 / 100, all inside [0.398942, 1]; perpendicular error below 0.0042 |
| Lemma 3.1 probability bound | VERIFIED — 13/13 non-vacuous cells satisfy the 99.9% lower bound against gamma_x |
| gamma_x functional form | VERIFIED — measured rate linear in nu and L, inverse in ||grad f||, proportional to d^(-1/2) |
| Improved constant vs Saha et al. 2021 | VERIFIED — factor 7.978846 against the paper's stated 8 |
| Tightened-bound control | Violated in 13/13 cells, as required |
| Sign-blind control | 0.501388 against an expected 0.5 |

The previous FALSIFIED verdict is withdrawn: its cells had gamma_x between
11.283792 and 1410.473959, where Lemma 3.1 makes no assertion. No
assumption-satisfying counterexample exists in the regime where the lemma has
content.
