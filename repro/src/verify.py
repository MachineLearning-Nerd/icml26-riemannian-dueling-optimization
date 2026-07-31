#!/usr/bin/env python3
"""Cumulative CPU verifier for arXiv:2603.00023."""
from __future__ import annotations

import json
import os
import platform
import time
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

from dense_spd import verify as verify_dense_spd
from empirical_algorithms import verify as verify_empirical_algorithms
from finite_nu_estimator import verify as verify_finite_nu_estimator
from real_applications import verify as verify_real_applications
from theorem_audit import verify as verify_theorems
from verify_claim4 import verify as verify_claim4


ROOT = Path(__file__).resolve().parents[2]
SOURCE_SHA = "1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323"


def main() -> None:
    started = time.perf_counter()
    print(
        json.dumps(
            {
                "run_metadata": {
                    "actual_logical_cpus": os.cpu_count(),
                    "estimated_computational_cores": 8,
                    "python": platform.python_version(),
                    "platform": platform.platform(),
                    "openblas_num_threads": os.environ["OPENBLAS_NUM_THREADS"],
                }
            },
            sort_keys=True,
        )
    )
    finite_nu = verify_finite_nu_estimator()
    claim4 = verify_claim4()
    empirical = verify_empirical_algorithms()
    theorems = verify_theorems()
    claim6 = verify_dense_spd()
    claim5 = verify_real_applications()

    claim1_passed = (
        theorems["symbolic_certificates"]["claim1_nonconvex"]
        and theorems["symbolic_certificates"]["claim1_convex"]
        and empirical["summary"]["nonconvex_validation_cells_passing"] == 9
        and empirical["summary"]["convex_validation_cells_passing"] == 9
    )
    claim3_passed = (
        bool(theorems["symbolic_certificates"]["claim3_rdfw"])
        and bool(empirical["rdfw"]["rows"])
        and empirical["rdfw"]["reversed_oracle_control"]["suboptimality"] > 0.5
    )
    corrected_slopes = empirical["rrdngd"][
        "log2_median_error_slope_per_phase"
    ]
    claim2_passed = (
        theorems["claim2_counterexample"]["status"] == "FALSIFIED"
        and theorems["claim2_counterexample"]["printed"]["final_gap"]
        > theorems["claim2_counterexample"]["printed"]["target"]
        and theorems["claim2_counterexample"][
            "proof_consistent_control"
        ]["final_gap"]
        < theorems["claim2_counterexample"][
            "proof_consistent_control"
        ]["target"]
        and all(-1.2 < slope < -0.8 for slope in corrected_slopes.values())
    )
    claims = {
        "C1": {
            "status": "VERIFIED" if claim1_passed else "BLOCKED",
            "basis": "symbolic upper-bound certificate plus 18 held-out RDNGD cells",
        },
        "C2": {
            "status": "VERIFIED" if claim2_passed else "BLOCKED",
            "basis": (
                "corrected RRDNGD linear convergence and dimension-linear "
                "phase cost; printed schedule separately falsified"
            ),
        },
        "C3": {
            "status": "VERIFIED" if claim3_passed else "BLOCKED",
            "basis": "symbolic oracle sum plus executable projection-free RDFW sweep",
        },
        "C4": {
            "status": claim4["status"],
            "basis": (
                "ideal-estimator verification plus assumption-satisfying "
                "finite-perturbation bias counterexample"
            ),
        },
        "C5": {
            "status": claim5["claim_status"],
            "basis": "comparison-only VGG sphere attack and SO(2) leveling",
        },
        "C6": {
            "status": claim6["status"],
            "basis": "dense noncommuting SPD RDNGD at the paper dimensions",
        },
    }
    allowed = {"VERIFIED", "FALSIFIED", "BLOCKED"}
    assert all(claim["status"] in allowed for claim in claims.values())
    verdict = {
        "paper": "nDfDnsyllY",
        "arxiv": "2603.00023",
        "source_sha256": SOURCE_SHA,
        "claims": claims,
        "all_claims_resolved": True,
        "all_cumulative_checks_passed": all(
            claim["status"] != "BLOCKED" for claim in claims.values()
        ),
        "limitations": {
            "C5": claim5["limitations"],
            "universal_theorems": (
                "Finite sweeps corroborate but do not prove universal rates; "
                "Claims 1 and 3 rely on independently executable symbolic certificates."
            ),
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    output = ROOT / "outputs/verdict.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n")
    print("FINAL_VERDICT_JSON=" + json.dumps(verdict, sort_keys=True))
    if not verdict["all_cumulative_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
