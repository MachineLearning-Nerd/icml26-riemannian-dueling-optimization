#!/usr/bin/env python3
"""Validate the empirical research node without authorizing publication."""
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
gate = {
    "paper": "nDfDnsyllY",
    "arxiv": "2603.00023",
    "publication_eligible": False,
    "publication_gate_passed": False,
    "research_node_valid": True,
    "reason": "The theorem audit sibling and application/manifold evidence are not yet combined.",
}
(root / "outputs" / "publication_gate.json").write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n")
(root / "GATE_READY.md").write_text("RELEASE_BLOCKED: research node only\n")
print(json.dumps(gate, indent=2, sort_keys=True))
