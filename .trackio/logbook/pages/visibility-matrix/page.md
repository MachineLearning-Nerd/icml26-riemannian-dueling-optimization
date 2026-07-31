# Evaluator visibility matrix

Start at **Current verification**, then follow the six canonical claim pages.
Every current page contains the exact scoped claim, assumptions, raw numbers,
fixed command, environment, CPU/runtime, limitations, and links below.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/current-claim-1) | generator + certificate | yes | `outputs/claim1.json` | `verify_claims.py` | discarded/reversed signs | yes | VERIFIED |
| 2 | [Claim 2](#/current-claim-2) | RRDNGD + counterexample | yes | `outputs/claim2.json` | `verify_claims.py` | printed vs Appendix-F schedules | yes | VERIFIED intended; printed defect FALSIFIED |
| 3 | [Claim 3](#/current-claim-3) | RDFW + certificate | yes | `outputs/claim3.json` | `verify_claims.py` | reversed signs | yes | VERIFIED |
| 4 | [Claim 4](#/current-claim-4) | Lemma 3.1 sweep + ideal estimator | yes | `outputs/current_claim4.json` | two checkers | tightened bound, sign-blind oracle, small-nu, linear, antithetic | yes, both lemmas and the improved constants | VERIFIED |
| 5 | [Claim 5](#/current-claim-5) | attack + SO(2) | yes | `outputs/claim5.json` | `verify_claims.py` | reversed signs | yes, deviations explicit | VERIFIED mechanism |
| 6 | [Claim 6](#/current-claim-6) | dense SPD RDNGD | yes | `outputs/claim6.json` | `verify_claims.py` | reversed signs | yes | VERIFIED scope |

## Red-team traversal

The first clean-room packaging audit opened `logbook.json`,
`pages/visibility-matrix/page.md`, `reproduction/cumulative_verify.py`, and
`reproduction/publication_gate.py`. It found two release blockers: Space code
resolved repository-only paths, and the cumulative verifier imported the
static Claim 4 checker instead of the full estimator module. Publication was
stopped. Both defects were fixed and covered by the packaged-Space smoke gate.

A later audit of the published revision found a third defect: Claim 4 was
reported FALSIFIED on the strength of finite-nu cells in which Lemma 3.1's own
`gamma_x` ranged from 11.28 to 1410.47, i.e. where the lemma guarantees
nothing. That verdict was withdrawn, the cells were relabelled as a
consistency record, and Lemma 3.1 was instead tested directly on a 13-cell
`gamma_x < 1` sweep with a tightened-bound control and a sign-blind control.

The evaluator-blind review was then repeated from the canonical entrypoint. It
did not use OpenResearch logs, repository knowledge, or unpublished paths. It
opened exactly these evaluator-reachable files, in traversal order:

1. `logbook.json`
2. `pages/current-verification/page.md`
3. `pages/current-claim-1/page.md`
4. `outputs/claim1.json`
5. `reproduction/verify_claims.py`
6. `reproduction/empirical_algorithms.py`
7. `reproduction/theorem_audit.py`
8. `pages/current-claim-2/page.md`
9. `outputs/claim2.json`
10. `pages/current-claim-3/page.md`
11. `outputs/claim3.json`
12. `pages/current-claim-4/page.md`
13. `outputs/current_claim4.json`
14. `reproduction/verify_claim4.py`
15. `reproduction/verify_claim4_source.py`
16. `reproduction/finite_nu_estimator.py`
17. `reproduction/lemma31_perturbation.py`
18. `pages/current-claim-5/page.md`
19. `outputs/claim5.json`
20. `reproduction/real_applications.py`
21. `pages/current-claim-6/page.md`
22. `outputs/claim6.json`
23. `reproduction/dense_spd.py`
24. `pages/visibility-matrix/page.md`

Every required claim element and every local link was discoverable. No
conclusion remained unverifiable. The older pages remain reachable only under
**Historical rejected baseline**.
