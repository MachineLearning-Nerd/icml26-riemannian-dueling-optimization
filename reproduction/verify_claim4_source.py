#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def exact_c_hat(d: int) -> float:
    return math.sqrt(d) * math.gamma(d / 2) / (
        math.sqrt(math.pi) * math.gamma((d + 1) / 2)
    )


def verify() -> dict:
    raw = json.loads(
        (
            ROOT
            / ".trackio/logbook/outputs/current_claim4.json"
        ).read_text()
    )
    control = json.loads(
        (
            ROOT
            / ".openresearch/artifacts/claim4/negative_control_output.json"
        ).read_text()
    )
    lower = 1 / math.sqrt(2 * math.pi)
    for row in raw["dimensions"]:
        assert lower <= row["C_hat"] <= 1
        assert abs(row["C_hat"] - exact_c_hat(row["d"])) < 0.05
        assert row["perpendicular_error"] < 0.01
    assert control["paired_antithetic_unsigned_mean_norm"] == 0
    finite = raw["finite_nu_bias"]
    assumptions = finite["assumption_audit"]
    assert assumptions["probe_points_inside_domain"]
    assert assumptions["gradient_at_x_nonzero"]
    assert assumptions["smooth_on_domain"]
    for dimension in finite["dimensions"]:
        small, large = dimension["finite_nu_rows"]
        assert small["nu"] == 1e-4
        assert small["sign_disagreement_rate"] < 0.001
        assert large["nu"] == 0.5
        assert large["sign_disagreement_rate"] > 0.04
        assert large["paired_orthogonal_absolute_lower_95"] > 0.015
        assert (
            dimension["linear_objective_negative_control"][
                "sign_disagreement_rate"
            ]
            == 0
        )
    assert finite["ideal_estimator_status"] == "VERIFIED"
    assert finite["finite_perturbation_status"] == "FALSIFIED_AS_WRITTEN"
    result = {
        "claim": 4,
        "max_perpendicular_error": max(
            row["perpendicular_error"] for row in raw["dimensions"]
        ),
        "negative_control_failed_alignment": True,
        "ideal_estimator_status": "VERIFIED",
        "finite_perturbation_status": "FALSIFIED_AS_WRITTEN",
        "status": "FALSIFIED",
    }
    print(json.dumps({"claim4_checker": result}, sort_keys=True))
    return result


if __name__ == "__main__":
    verify()
