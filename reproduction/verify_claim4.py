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
    assert large["sign_disagreement_rate"] > 0.04
    assert large["paired_orthogonal_absolute_lower_95"] > 0.015
    assert dimension["linear_objective_negative_control"]["sign_disagreement_rate"] == 0
print("FALSIFIED AS WRITTEN: finite-nu estimator; ideal Lemma 3.2 estimator VERIFIED")
