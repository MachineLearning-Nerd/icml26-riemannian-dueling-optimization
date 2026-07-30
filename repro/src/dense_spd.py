#!/usr/bin/env python3
"""Comparison-only RDNGD for dense affine-invariant SPD Karcher means."""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SEED = 20260730


def spectral(matrix: np.ndarray, function) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2)
    return (vectors * function(np.maximum(values, 1e-14))) @ vectors.T


def sqrt_spd(matrix: np.ndarray) -> np.ndarray:
    return spectral(matrix, np.sqrt)


def invsqrt_spd(matrix: np.ndarray) -> np.ndarray:
    return spectral(matrix, lambda values: 1 / np.sqrt(values))


def log_spd(matrix: np.ndarray) -> np.ndarray:
    return spectral(matrix, np.log)


def exp_sym(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2)
    return (vectors * np.exp(values)) @ vectors.T


def exp_map(point: np.ndarray, white_tangent: np.ndarray) -> np.ndarray:
    point_sqrt = sqrt_spd(point)
    updated = point_sqrt @ exp_sym(white_tangent) @ point_sqrt
    return (updated + updated.T) / 2


def objective(point: np.ndarray, samples: list[np.ndarray]) -> float:
    point_invsqrt = invsqrt_spd(point)
    squared_distances = [
        np.linalg.norm(
            log_spd(point_invsqrt @ sample @ point_invsqrt), "fro"
        )
        ** 2
        for sample in samples
    ]
    return float(0.5 * np.mean(squared_distances))


def fixed_point_reference(
    samples: list[np.ndarray], dimension: int
) -> tuple[np.ndarray, float, float, int]:
    point = np.eye(dimension)
    initial = objective(point, samples)
    for iteration in range(1, 101):
        point_invsqrt = invsqrt_spd(point)
        mean_log = np.mean(
            [
                log_spd(point_invsqrt @ sample @ point_invsqrt)
                for sample in samples
            ],
            axis=0,
        )
        residual = float(np.linalg.norm(mean_log, "fro"))
        point = exp_map(point, mean_log)
        if residual < 1e-12:
            break
    return point, objective(point, samples), residual, iteration


def make_samples(
    rng: np.random.Generator, dimension: int, count: int
) -> list[np.ndarray]:
    samples = []
    for _ in range(count):
        orthogonal, _ = np.linalg.qr(rng.normal(size=(dimension, dimension)))
        eigenvalues = np.exp(rng.uniform(np.log(0.45), np.log(2.2), dimension))
        samples.append(orthogonal @ np.diag(eigenvalues) @ orthogonal.T)
    return samples


def comparison(
    point: np.ndarray,
    direction: np.ndarray,
    radius: float,
    samples: list[np.ndarray],
    reverse: bool = False,
) -> int:
    plus = objective(exp_map(point, radius * direction), samples)
    minus = objective(exp_map(point, -radius * direction), samples)
    sign = 1 if plus <= minus else -1
    return -sign if reverse else sign


def run_case(dimension: int, iterations: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    samples = make_samples(rng, dimension, 50)
    commutators = [
        np.linalg.norm(left @ right - right @ left, "fro")
        for index, left in enumerate(samples)
        for right in samples[:index]
    ]
    reference, reference_objective, residual, reference_iterations = (
        fixed_point_reference(samples, dimension)
    )
    point = np.eye(dimension)
    initial_objective = objective(point, samples)
    best = point.copy()
    best_objective = initial_objective
    checkpoints = [{"iteration": 0, "best_objective": best_objective}]
    radius = 0.02
    for iteration in range(iterations):
        direction = rng.normal(size=(dimension, dimension))
        direction = (direction + direction.T) / 2
        direction /= np.linalg.norm(direction, "fro")
        oracle_sign = comparison(point, direction, radius, samples)
        step = 0.14 / np.sqrt(iteration + 20)
        point = exp_map(point, step * oracle_sign * direction)
        current_objective = objective(point, samples)
        if current_objective < best_objective:
            best = point.copy()
            best_objective = current_objective
        if (iteration + 1) % 500 == 0:
            checkpoints.append(
                {
                    "iteration": iteration + 1,
                    "best_objective": best_objective,
                }
            )

    reference_invsqrt = invsqrt_spd(reference)
    distance_to_reference = float(
        np.linalg.norm(
            log_spd(reference_invsqrt @ best @ reference_invsqrt), "fro"
        )
    )

    control_rng = np.random.default_rng(seed + 1)
    reversed_point = np.eye(dimension)
    reversed_initial = objective(reversed_point, samples)
    for iteration in range(256):
        direction = control_rng.normal(size=(dimension, dimension))
        direction = (direction + direction.T) / 2
        direction /= np.linalg.norm(direction, "fro")
        oracle_sign = comparison(
            reversed_point, direction, radius, samples, reverse=True
        )
        reversed_point = exp_map(
            reversed_point,
            0.14 / np.sqrt(iteration + 20) * oracle_sign * direction,
        )
    reversed_final = objective(reversed_point, samples)

    return {
        "dimension": dimension,
        "manifold_dimension": dimension * (dimension + 1) // 2,
        "matrices": 50,
        "seed": seed,
        "duels": iterations,
        "initial_objective": initial_objective,
        "final_best_objective": best_objective,
        "relative_objective_gap_to_reference": (
            best_objective - reference_objective
        )
        / reference_objective,
        "affine_invariant_distance_to_reference": distance_to_reference,
        "minimum_pairwise_commutator_norm": float(min(commutators)),
        "median_pairwise_commutator_norm": float(np.median(commutators)),
        "minimum_output_eigenvalue": float(np.linalg.eigvalsh(best).min()),
        "checkpoints": checkpoints,
        "independent_reference": {
            "objective": reference_objective,
            "fixed_point_residual": residual,
            "iterations": reference_iterations,
        },
        "negative_control": {
            "kind": "reversed comparison signs",
            "initial_objective": reversed_initial,
            "final_objective": reversed_final,
            "failed_progress_as_intended": reversed_final > reversed_initial,
        },
    }


def verify() -> dict:
    started = time.perf_counter()
    rows = [
        run_case(dimension=5, iterations=4_000, seed=SEED + 5),
        run_case(dimension=10, iterations=6_000, seed=SEED + 10),
    ]
    checks = {
        "paper_dimensions": all(
            row["dimension"] in (5, 10) and row["matrices"] == 50
            for row in rows
        ),
        "dense_noncommuting": all(
            row["minimum_pairwise_commutator_norm"] > 1e-3 for row in rows
        ),
        "comparison_rdngd_progress": all(
            row["final_best_objective"] < 0.99 * row["initial_objective"]
            for row in rows
        ),
        "near_independent_reference": all(
            row["relative_objective_gap_to_reference"] < 5e-3
            for row in rows
        ),
        "spd_feasibility": all(
            row["minimum_output_eigenvalue"] > 0 for row in rows
        ),
        "negative_controls_fail": all(
            row["negative_control"]["failed_progress_as_intended"]
            for row in rows
        ),
    }
    result = {
        "paper": "2603.00023",
        "claim": 6,
        "algorithm": "RDNGD with two-probe pairwise comparison oracle",
        "geometry": "affine-invariant dense SPD manifold",
        "function_values_exposed_to_update": False,
        "rows": rows,
        "checks": checks,
        "status": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "runtime_seconds": time.perf_counter() - started,
    }
    output = ROOT / "outputs" / "dense_spd.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("DENSE_SPD_JSON=" + json.dumps(result, sort_keys=True))
    print(
        json.dumps(
            {
                "dense_spd_summary": {
                    "status": result["status"],
                    "runtime_seconds": result["runtime_seconds"],
                    "rows": [
                        {
                            key: row[key]
                            for key in (
                                "dimension",
                                "duels",
                                "initial_objective",
                                "final_best_objective",
                                "relative_objective_gap_to_reference",
                                "affine_invariant_distance_to_reference",
                            )
                        }
                        for row in rows
                    ],
                }
            },
            sort_keys=True,
        )
    )
    if result["status"] != "VERIFIED":
        raise SystemExit("dense SPD claim contract failed")
    return result


if __name__ == "__main__":
    verify()
