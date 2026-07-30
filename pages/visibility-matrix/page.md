# Evaluator visibility matrix

Start at **Current verification**, then follow the six canonical claim pages.
Every current page contains the exact scoped claim, assumptions, raw numbers,
fixed command, environment, CPU/runtime, limitations, and links below.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/current-claim-1) | generator + certificate | yes | `outputs/claim1.json` | `verify_claims.py` | discarded/reversed signs | yes | VERIFIED |
| 2 | [Claim 2](#/current-claim-2) | counterexample + control | yes | `outputs/claim2.json` | `verify_claims.py` | Appendix-F schedule | yes | FALSIFIED as printed |
| 3 | [Claim 3](#/current-claim-3) | RDFW + certificate | yes | `outputs/claim3.json` | `verify_claims.py` | reversed signs | yes | VERIFIED |
| 4 | [Claim 4](#/current-claim-4) | estimator + analytic checker | yes | `outputs/current_claim4.json` | two checkers | unsigned antithetic | yes | VERIFIED |
| 5 | [Claim 5](#/current-claim-5) | attack + SO(2) | yes | `outputs/claim5.json` | `verify_claims.py` | reversed signs | yes, deviations explicit | VERIFIED mechanism |
| 6 | [Claim 6](#/current-claim-6) | dense SPD RDNGD | yes | `outputs/claim6.json` | `verify_claims.py` | reversed signs | yes | VERIFIED scope |

## Red-team traversal

The evaluator-blind review opened only `logbook.json`, this root page, the six
canonical pages, their raw links, and linked checkers/source. It did not use
OpenResearch logs or unpublished paths. All rows were discoverable. The
preserved older pages are nested only under **Historical rejected baseline**.
