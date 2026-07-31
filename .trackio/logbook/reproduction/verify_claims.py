#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(claim: int) -> dict:
    return json.loads((ROOT / f"outputs/claim{claim}.json").read_text())


c1 = load(1)
assert all(row["upper_95"] < row["epsilon"] for row in c1["nonconvex"])
assert all(row["upper_95"] < row["epsilon"] for row in c1["convex"])
assert c1["negative_controls"]["discard_comparisons_gradient_norm"] > 0.18
assert c1["negative_controls"]["reverse_convex_suboptimality"] > 0.02

c2 = load(2)
counterexample = c2["counterexample"]
assert counterexample["printed_final_gap"] > counterexample["target"]
assert counterexample["proof_consistent_final_gap"] < counterexample["target"]
assert c2["status"] == "FALSIFIED"

c3 = load(3)
assert c3["projection_calls"] == 0
assert c3["loglog_slopes"]["d15"]["queries_vs_horizon"] < 2
assert c3["d15_rows"][-1]["median_suboptimality"] < c3["d15_rows"][0]["median_suboptimality"]
assert c3["negative_control"]["suboptimality"] > 0.5

c4 = json.loads((ROOT / "outputs/current_claim4.json").read_text())
assert all(row["perpendicular_error"] < 0.01 for row in c4["dimensions"])
finite = c4["finite_nu_bias"]
assert finite["ideal_estimator_status"] == "VERIFIED"
assert finite["finite_perturbation_status"] == "FALSIFIED_AS_WRITTEN"
assert all(
    dimension["finite_nu_rows"][1]["paired_orthogonal_absolute_lower_95"] > 0.015
    for dimension in finite["dimensions"]
)
assert all(
    dimension["linear_objective_negative_control"]["sign_disagreement_rate"] == 0
    for dimension in finite["dimensions"]
)

c5 = load(5)
assert c5["calibrated_attack"]["successful_images"] >= 2
assert c5["calibrated_attack"]["maximum_radius_error"] < 0.00001
assert c5["calibrated_attack"]["reverse_control_margin"]["final"] > c5["calibrated_attack"]["reverse_control_margin"]["initial"]
assert c5["so2"]["successes_below_1e-5"] == c5["so2"]["tilts"]

c6 = load(6)
assert all(row["final_objective"] < row["initial_objective"] for row in c6["rows"])
assert all(row["relative_gap"] < 0.005 for row in c6["rows"])
assert all(row["reverse_final_objective"] > row["initial_objective"] for row in c6["rows"])
assert min(c6["minimum_output_eigenvalues"]) > 0

print("VERIFIED: cumulative Claim 1-6 artifact checks")
