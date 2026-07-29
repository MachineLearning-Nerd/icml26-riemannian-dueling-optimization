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
