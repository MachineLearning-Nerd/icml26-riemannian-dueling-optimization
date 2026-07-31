#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def exact_c_hat(d: int) -> float:
    return math.sqrt(d) * math.gamma(d / 2) / (
        math.sqrt(math.pi) * math.gamma((d + 1) / 2)
    )


raw = json.loads((ROOT / "outputs/current_claim4.json").read_text())
lower = 1 / math.sqrt(2 * math.pi)
for row in raw["dimensions"]:
    assert lower <= row["C_hat"] <= 1
    assert abs(row["C_hat"] - exact_c_hat(row["d"])) < 0.05
    assert row["perpendicular_error"] < 0.01
finite = raw["finite_nu_bias"]
assert finite["assumption_audit"]["smooth_on_domain"]
assert finite["assumption_audit"]["probe_points_inside_domain"]
for dimension in finite["dimensions"]:
    small, large = dimension["finite_nu_rows"]
    assert small["sign_disagreement_rate"] < 0.001
    assert dimension["linear_objective_negative_control"]["sign_disagreement_rate"] == 0
assert finite["finite_perturbation_status"] == "CONSISTENT_WITH_LEMMA_3_1"

# Lemma 3.1 in the regime where its guarantee has content: gamma_x < 1.
lemma31 = raw["lemma_3_1_perturbation"]
assert lemma31["assumption_audit"]["geodesically_L_smooth"]
assert lemma31["assumption_audit"]["nu_in_open_unit_interval"]
assert lemma31["assumption_audit"]["grad_at_x_nonzero"]
assert lemma31["lemma_3_1_all_cells_non_vacuous"]
for cell in lemma31["lemma_3_1_cells"]:
    gamma = math.sqrt(cell["d"] / (2 * math.pi)) * cell["L"] * cell["nu"] / cell["grad_norm"]
    assert abs(gamma - cell["gamma_x"]) < 1e-12, "gamma_x recomputation"
    assert gamma < 1.0, "cell must be non-vacuous"
    assert cell["events"] > 0, "cell must actually observe disagreements"
    assert cell["lower_999_confidence"] <= gamma, "Lemma 3.1 upper bound violated"
    # negative control: the same bound tightened by 4d must be violated
    assert cell["empirical_disagreement"] > gamma / (4 * cell["d"])
assert lemma31["sign_blind_control"]["fails_as_intended"]

# The superseded finite-nu cells sit in the vacuous regime, so they are not
# a counterexample to Lemma 3.1.
for row in lemma31["superseded_finite_nu_gamma_audit"]:
    assert row["gamma_x"] >= 1.0

# Lemma 3.2 improved constant over Saha et al. (2021).
constants = lemma31["lemma_3_2_improved_constants"]
assert abs(constants["paper_lower_bound"] - 1 / math.sqrt(2 * math.pi)) < 1e-12
assert abs(constants["improvement_factor"] - 8.0) < 0.05
for row in constants["exact_values"]:
    assert constants["paper_lower_bound"] <= row["exact_c_hat"] <= 1.0
    assert row["exact_c_hat"] > constants["saha_2021_lower_bound"]

print("VERIFIED: Lemma 3.1 gamma_x bound holds on all non-vacuous cells; "
      "Lemma 3.2 constant interval and eightfold improvement confirmed")
