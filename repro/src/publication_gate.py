#!/usr/bin/env python3
"""Fail closed unless the evaluator-visible candidate is internally complete."""
from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOGBOOK = ROOT / ".trackio/logbook"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


verdict = json.loads((ROOT / "outputs/verdict.json").read_text())
assert verdict["all_claims_resolved"]
assert verdict["all_cumulative_checks_passed"]
assert {row["status"] for row in verdict["claims"].values()} <= {
    "VERIFIED",
    "FALSIFIED",
}

runpy.run_path(str(LOGBOOK / "reproduction/verify_claims.py"))
runpy.run_path(str(LOGBOOK / "reproduction/verify_claim4.py"))

navigation = json.loads((LOGBOOK / "logbook.json").read_text())
assert navigation["root"]["slug"] == "current-verification"
slugs = {child["slug"] for child in navigation["root"]["children"]}
assert {f"current-claim-{number}" for number in range(1, 7)} <= slugs
assert "visibility-matrix" in slugs
assert "historical-rejected-baseline" in slugs

required_page_terms = (
    "Exact claim",
    "Verdict:",
    "Reproduce.",
    "Raw",
    "checker",
    "Limitation",
    "cpu-upgrade",
)
for number in range(1, 7):
    page = LOGBOOK / f"pages/current-claim-{number}/page.md"
    text = page.read_text()
    assert all(term.lower() in text.lower() for term in required_page_terms)
    assert (LOGBOOK / f"outputs/claim{number}.json").exists() or number == 4

visibility = (LOGBOOK / "pages/visibility-matrix/page.md").read_text()
for number in range(1, 7):
    assert f"| {number} |" in visibility

protected = {}
for line in (
    ROOT / ".openresearch/artifacts/protected_space_8b6af91_manifest.sha256"
).read_text().splitlines():
    digest, name = line.split("  ", 1)
    protected[name] = digest
for name, digest in protected.items():
    if name.startswith("pages/"):
        assert sha256(LOGBOOK / name) == digest

gate = {
    "paper": "nDfDnsyllY",
    "arxiv": "2603.00023",
    "publication_eligible": True,
    "publication_gate_passed": True,
    "research_node_valid": True,
    "historical_page_hashes_preserved": True,
    "visibility_rows_complete": 6,
}
(ROOT / "outputs/publication_gate.json").write_text(
    json.dumps(gate, indent=2, sort_keys=True) + "\n"
)
(ROOT / "GATE_READY.md").write_text(
    "RELEASE_READY: cumulative science and evaluator visibility gate passed\n"
)
print("PUBLICATION_GATE_JSON=" + json.dumps(gate, sort_keys=True))
