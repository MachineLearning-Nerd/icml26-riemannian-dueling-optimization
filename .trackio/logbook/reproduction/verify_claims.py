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
assert c2["printed_schedule_status"] == "FALSIFIED"
assert c2["status"] == "VERIFIED"
assert all(
    -1.2 < slope < -0.8
    for slope in c2["corrected_empirical_control"][
        "log2_error_slope_per_phase"
    ].values()
)

c3 = load(3)
assert c3["projection_calls"] == 0
assert c3["loglog_slopes"]["d15"]["queries_vs_horizon"] < 2
assert c3["d15_rows"][-1]["median_suboptimality"] < c3["d15_rows"][0]["median_suboptimality"]
assert c3["negative_control"]["suboptimality"] > 0.5

c4 = json.loads((ROOT / "outputs/current_claim4.json").read_text())
assert all(row["perpendicular_error"] < 0.01 for row in c4["dimensions"])
finite = c4["finite_nu_bias"]
assert finite["ideal_estimator_status"] == "VERIFIED"
assert finite["finite_perturbation_status"] == "CONSISTENT_WITH_LEMMA_3_1"
lemma31 = c4["lemma_3_1_perturbation"]
assert lemma31["status"] == "VERIFIED"
assert lemma31["lemma_3_1_all_cells_non_vacuous"]
assert lemma31["lemma_3_1_all_cells_hold"]
assert lemma31["negative_control_all_violated"]
assert lemma31["sign_blind_control"]["fails_as_intended"]
assert lemma31["lemma_3_2_improved_constants"]["all_inside_paper_interval"]
assert lemma31["lemma_3_2_improved_constants"]["improvement_factor_matches_paper"]
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
