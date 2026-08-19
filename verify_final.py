#!/usr/bin/env python3
"""Verify the public documentation, branch namespace, and commit identity."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = "MachineLearning-Nerd/icml26-riemannian-dueling-optimization"
CANONICAL = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
OVERALL_STATUS = (
    "PARTIAL_C1_C3_C4_C6_VERIFIED_C2_PRINTED_SCHEDULE_FALSIFIED_"
    "C5_MECHANISM_VERIFIED_PAPER_SETTING_BLOCKED"
)
EXPECTED_BRANCHES = {
    "main",
    "audit/claim-4-contract",
    "audit/evaluator-blind-transcript",
    "audit/finite-nu-estimator",
    "audit/held-out-rdngd-calibration",
    "audit/judged-baseline",
    "audit/lemma-3-1-gamma-calibration",
    "audit/theorem-contracts-rrdngd",
    "experiment/calibrated-core-algorithms",
    "experiment/calibrated-vgg-attack",
    "experiment/dense-spd-karcher",
    "experiment/paper-setting-applications",
    "integration/theory-and-algorithms",
    "release/corrected-six-claim-gate",
    "release/evaluator-visible-cumulative",
    "release/final-reference-aligned",
    "release/record-final-evidence",
    "release/self-contained-space",
    "release/six-claim-adjudication",
}
REQUIRED_FILES = {
    "README.md",
    "STATUS.md",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "docs/SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "branch-audit.md",
    "outputs/verdict.json",
    "outputs/publication_gate.json",
    "outputs/claim1.json",
    "outputs/claim2.json",
    "outputs/claim3.json",
    "outputs/current_claim4.json",
    "outputs/claim5.json",
    "outputs/claim6.json",
    "claims.json",
    "reproduction_verdicts.json",
    "AUTONOMOUS_STATE.json",
    "CITATION.cff",
    "AUTHOR_THANK_YOU.md",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def main() -> None:
    missing = sorted(path for path in REQUIRED_FILES if not (ROOT / path).exists())
    assert not missing, f"missing required files: {missing}"
    assert not git("status", "--porcelain"), "working tree is not clean"
    assert not git("for-each-ref", "--format=%(refname)", "refs/original"), "refs/original remains"

    remote = git("remote", "get-url", "origin").removesuffix(".git")
    assert remote.endswith(REPOSITORY), remote
    branch_lines = git("ls-remote", "--heads", "origin").splitlines()
    remote_branches = {
        line.split("\t", 1)[1].removeprefix("refs/heads/")
        for line in branch_lines
        if "\t" in line
    }
    assert remote_branches == EXPECTED_BRANCHES, remote_branches
    assert git("symbolic-ref", "--short", "refs/remotes/origin/HEAD") == "origin/main"

    identities = set(git("log", "--all", "--format=%an <%ae> | %cn <%ce>").splitlines())
    assert identities == {f"{CANONICAL} | {CANONICAL}"}, identities
    assert "Co-authored-by:" not in git("log", "--all", "--format=%B")

    claims = json.loads((ROOT / "claims.json").read_text())
    assert claims["overall_status"] == OVERALL_STATUS
    assert [claim["id"] for claim in claims["claims"]] == ["C1", "C2", "C3", "C4", "C5", "C6"]
    state = json.loads((ROOT / "AUTONOMOUS_STATE.json").read_text())
    assert state["overall_status"] == OVERALL_STATUS
    assert state["current_score_claim"] is False
    assert state["publication_allowed"] is False

    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(remote_branches)} commits={git('rev-list', '--all', '--count')} "
        "claims=C1,C3:C4,C6_verified,C2_printed_schedule_falsified,"
        "C5_mechanism_verified_paper_setting_blocked "
        "historical_score=3/12 current_score_claim=false publication_allowed=false"
    )


if __name__ == "__main__":
    main()
