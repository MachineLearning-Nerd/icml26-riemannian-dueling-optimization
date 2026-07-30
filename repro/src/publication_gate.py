#!/usr/bin/env python3
"""Validate the research node without authorizing publication."""
from __future__ import annotations
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
v = json.loads((root / "outputs" / "verdict.json").read_text())
empirical = json.loads(
    (root / "outputs" / "empirical_algorithms.json").read_text()
)
assert v["paper"] == "nDfDnsyllY"
assert v["claims"]["C4"]["passed"]
assert empirical["rdfw"]["rows"]
assert empirical["rrdngd"]["rows"]
theorems = json.loads((root / "outputs" / "theorem_audit.json").read_text())
assert theorems["claim2_counterexample"]["status"] == "FALSIFIED"
gate = {
    "paper": "nDfDnsyllY",
    "arxiv": "2603.00023",
    "publication_eligible": False,
    "publication_gate_passed": False,
    "research_node_valid": True,
    "reason": "C5 and C6 remain incomplete; C1 nonconvex calibration needs refinement.",
}
(root / "outputs" / "publication_gate.json").write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n")
(root / "GATE_READY.md").write_text("RELEASE_BLOCKED: research node only\n")
print(json.dumps(gate, indent=2, sort_keys=True))
