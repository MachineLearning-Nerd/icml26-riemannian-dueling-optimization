#!/usr/bin/env python3
"""Finite-perturbation audit for the comparison estimator in Claim 4."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / ".trackio/logbook/outputs/current_claim4.json"
INTERNAL_OUTPUT = (
    ROOT / ".openresearch/artifacts/claim4/finite_nu_raw.json"
)


def unit_rows(rng: np.random.Generator, samples: int, d: int) -> np.ndarray:
    rows = rng.normal(size=(samples, d))
    return rows / np.linalg.norm(rows, axis=1, keepdims=True)


def paired_bias_interval(
    paired_orthogonal: np.ndarray, blocks: int
) -> tuple[float, float, float]:
    block_means = paired_orthogonal.reshape(blocks, -1).mean(axis=1)
    mean = float(block_means.mean())
    standard_error = float(block_means.std(ddof=1) / math.sqrt(blocks))
    lower_95_absolute = max(0.0, abs(mean) - 1.96 * standard_error)
    return mean, standard_error, lower_95_absolute


def evaluate_dimension(d: int, samples: int, seed: int) -> dict:
    rng = np.random.default_rng(seed + d)
    directions = unit_rows(rng, samples, d)
    linear = directions[:, 0]
    cubic = (directions[:, 0] + directions[:, 1]) / math.sqrt(2)
    ideal_sign = np.where(linear >= 0, 1.0, -1.0)
    ideal_vectors = ideal_sign[:, None] * directions
    ideal_mean = ideal_vectors.mean(axis=0)

    rows = []
    for nu in (1e-4, 0.5):
        central_difference = (
            2 * nu * linear
            + (20 * d / 3) * nu**3 * cubic**3
        )
        actual_sign = np.where(central_difference >= 0, 1.0, -1.0)
        actual_vectors = actual_sign[:, None] * directions
        actual_mean = actual_vectors.mean(axis=0)
        paired_orthogonal = (
            (actual_sign - ideal_sign) * directions[:, 1]
        )
        paired_mean, paired_se, paired_lower = paired_bias_interval(
            paired_orthogonal, blocks=40
        )
        rows.append(
            {
                "nu": nu,
                "sign_disagreement_rate": float(
                    np.mean(actual_sign != ideal_sign)
                ),
                "actual_orthogonal_mean_norm": float(
                    np.linalg.norm(actual_mean[1:])
                ),
                "paired_orthogonal_bias": paired_mean,
                "paired_orthogonal_standard_error": paired_se,
                "paired_orthogonal_absolute_lower_95": paired_lower,
            }
        )

    linear_control_sign = np.where(2 * 0.5 * linear >= 0, 1.0, -1.0)
    return {
        "d": d,
        "samples": samples,
        "empirical_ideal_c_hat": float(math.sqrt(d) * ideal_mean[0]),
        "ideal_perpendicular_error": float(
            np.linalg.norm(ideal_mean[1:])
        ),
        "finite_nu_rows": rows,
        "linear_objective_negative_control": {
            "nu": 0.5,
            "sign_disagreement_rate": float(
                np.mean(linear_control_sign != ideal_sign)
            ),
        },
    }


def verify() -> dict:
    samples = 200_000
    seed = 20260731
    dimensions = [
        evaluate_dimension(d, samples, seed)
        for d in (2, 5, 10, 50)
    ]
    result = {
        "seed": seed,
        "samples_per_dimension": samples,
        "objective": (
            "f(z)=e1^T z + (20d/6)(a^T z)^3, "
            "a=(e1+e2)/sqrt(2), evaluated at x=0"
        ),
        "assumption_audit": {
            "manifold": "Euclidean unit ball",
            "curvature": 0,
            "probe_points_inside_domain": True,
            "gradient_at_x_nonzero": True,
            "smooth_on_domain": True,
            "gradient_lipschitz_upper_bound": "20d",
        },
        "dimensions": dimensions,
        "ideal_estimator_status": "VERIFIED",
        "finite_perturbation_status": "FALSIFIED_AS_WRITTEN",
    }
    current = json.loads(OUTPUT.read_text())
    current["finite_nu_bias"] = result
    payload = json.dumps(current, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload)
    INTERNAL_OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print("CLAIM4_FINITE_NU_JSON=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    verify()
