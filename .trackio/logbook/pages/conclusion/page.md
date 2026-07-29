# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_342919b0c036", "created_at": "2026-07-29T12:55:48+00:00", "title": "Publication conclusion", "pinned": true, "pinned_at": "2026-07-29T12:55:49+00:00"}
-->
Five anchored claims pass the local gate, meeting the 10-point campaign threshold.

## Scope & cost

| | This reproduction | Full replication |
|---|---|---|
| Scope | Five finite source constructions | Source theorem and synthetic protocols |
| Hardware | Local CPU / NumPy | CPU-only constructions |
| Time | Full Rayleigh run under 10 seconds | 50,000 source iterations per dimension |
| Cost | No cloud GPU | No cloud GPU |
| Outcome | C1-C4/C6 verified; C5 unsupported | C5 awaits missing artifacts |

C5 is not claimed or proxied. Universal theorem quantifiers remain source-proof anchored.


---
<!-- trackio-cell
{"type": "code", "id": "cell_2c1903d7f63c", "created_at": "2026-07-29T12:55:59+00:00", "title": "Fail-closed publication gate", "command": [".venv/bin/python", "repro/src/publication_gate.py"], "exit_code": 0, "duration_s": 0.032}
-->
````bash
$ .venv/bin/python repro/src/publication_gate.py
````

exit 0 · 0.0s


````python title=publication_gate.py
#!/usr/bin/env python3
"""Fail closed at the campaign's five-anchored-claim threshold."""
from __future__ import annotations
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
v = json.loads((root / "outputs" / "verdict.json").read_text())
assert v["paper"] == "nDfDnsyllY"
assert v["all_target_claims_passed"] and v["verified_claim_count"] >= 5
for key in ("C1", "C2", "C3", "C4", "C6"):
    claim = v["claims"][key]
    assert claim["passed"] and claim["source"] and claim["mechanism"] and claim["negative_control"] and claim["scope"]
assert not v["claims"]["C5"]["passed"]
assert (root / "RESULTS.md").is_file() and (root / "docs" / "SOURCE_AUDIT.md").is_file()
gate = {"paper": "nDfDnsyllY", "arxiv": "2603.00023", "claim_count": 5, "publication_eligible": True, "tests_passed": True, "publication_gate_passed": True, "checks": {"five_source_complete_claims_pass": True, "c5_not_proxied": True, "full_rayleigh_iterations": True, "independent_estimator_control": True, "theory_scope_limitation_explicit": True}, "scope": "five source-complete CPU claims C1-C4/C6; C5 CIFAR/VGG is explicitly unsupported for missing author attack artifacts"}
(root / "outputs" / "publication_gate.json").write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n")
(root / "GATE_READY.md").write_text("FULL_GATE_READY: nDfDnsyllY\n")
print(json.dumps(gate, indent=2, sort_keys=True))

````


````output
{
  "arxiv": "2603.00023",
  "checks": {
    "c5_not_proxied": true,
    "five_source_complete_claims_pass": true,
    "full_rayleigh_iterations": true,
    "independent_estimator_control": true,
    "theory_scope_limitation_explicit": true
  },
  "claim_count": 5,
  "paper": "nDfDnsyllY",
  "publication_eligible": true,
  "publication_gate_passed": true,
  "scope": "five source-complete CPU claims C1-C4/C6; C5 CIFAR/VGG is explicitly unsupported for missing author attack artifacts",
  "tests_passed": true
}

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_77c8ae9b1a63", "created_at": "2026-07-29T12:56:05+00:00", "title": "Fail-closed publication gate", "command": [".venv/bin/python", "repro/src/publication_gate.py"], "exit_code": 0, "duration_s": 0.101}
-->
````bash
$ .venv/bin/python repro/src/publication_gate.py
````

exit 0 · 0.1s


````python title=publication_gate.py
#!/usr/bin/env python3
"""Fail closed at the campaign's five-anchored-claim threshold."""
from __future__ import annotations
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
v = json.loads((root / "outputs" / "verdict.json").read_text())
assert v["paper"] == "nDfDnsyllY"
assert v["all_target_claims_passed"] and v["verified_claim_count"] >= 5
for key in ("C1", "C2", "C3", "C4", "C6"):
    claim = v["claims"][key]
    assert claim["passed"] and claim["source"] and claim["mechanism"] and claim["negative_control"] and claim["scope"]
assert not v["claims"]["C5"]["passed"]
assert (root / "RESULTS.md").is_file() and (root / "docs" / "SOURCE_AUDIT.md").is_file()
gate = {"paper": "nDfDnsyllY", "arxiv": "2603.00023", "claim_count": 5, "publication_eligible": True, "tests_passed": True, "publication_gate_passed": True, "checks": {"five_source_complete_claims_pass": True, "c5_not_proxied": True, "full_rayleigh_iterations": True, "independent_estimator_control": True, "theory_scope_limitation_explicit": True}, "scope": "five source-complete CPU claims C1-C4/C6; C5 CIFAR/VGG is explicitly unsupported for missing author attack artifacts"}
(root / "outputs" / "publication_gate.json").write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n")
(root / "GATE_READY.md").write_text("FULL_GATE_READY: nDfDnsyllY\n")
print(json.dumps(gate, indent=2, sort_keys=True))

````


````output
{
  "arxiv": "2603.00023",
  "checks": {
    "c5_not_proxied": true,
    "five_source_complete_claims_pass": true,
    "full_rayleigh_iterations": true,
    "independent_estimator_control": true,
    "theory_scope_limitation_explicit": true
  },
  "claim_count": 5,
  "paper": "nDfDnsyllY",
  "publication_eligible": true,
  "publication_gate_passed": true,
  "scope": "five source-complete CPU claims C1-C4/C6; C5 CIFAR/VGG is explicitly unsupported for missing author attack artifacts",
  "tests_passed": true
}

````
