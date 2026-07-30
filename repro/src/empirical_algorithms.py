#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SEED = 20260730


def unit_vector(rng: np.random.Generator, d: int) -> np.ndarray:
    vector = rng.normal(size=d)
    return vector / np.linalg.norm(vector)


def unit_rows(
    rng: np.random.Generator, rows: int, d: int
) -> np.ndarray:
    vectors = rng.normal(size=(rows, d))
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def exact_c_hat(d: int) -> float:
    return math.sqrt(d) * math.gamma(d / 2) / (
        math.sqrt(math.pi) * math.gamma((d + 1) / 2)
    )


def sphere_exp(x: np.ndarray, tangent: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(tangent)
    if norm == 0:
        return x.copy()
    return math.cos(norm) * x + math.sin(norm) * tangent / norm


def nonconvex_rdngd(
    d: int,
    epsilon: float,
    horizon: int,
    seed: int,
    reverse: bool = False,
    frozen: bool = False,
) -> dict:
    rng = np.random.default_rng(seed)
    eigenvalues = np.linspace(0.0, 1.0, d)
    x = unit_vector(rng, d)
    manifold_d = d - 1
    c_hat = exact_c_hat(manifold_d)
    eta = 1 / math.sqrt(horizon)
    nu = c_hat * math.sqrt(2 * math.pi) * epsilon / (4 * manifold_d)
    gradient_norms = []
    for _ in range(horizon):
        rayleigh = float(np.sum(eigenvalues * x * x))
        gradient = -(eigenvalues * x - rayleigh * x)
        gradient_norms.append(float(np.linalg.norm(gradient)))
        u = rng.normal(size=d)
        u -= x * float(x @ u)
        u /= np.linalg.norm(u)
        plus = sphere_exp(x, nu * u)
        minus = sphere_exp(x, -nu * u)
        f_plus = -0.5 * float(np.sum(eigenvalues * plus * plus))
        f_minus = -0.5 * float(np.sum(eigenvalues * minus * minus))
        oracle = 1.0 if f_plus > f_minus else -1.0
        if reverse:
            oracle *= -1
        if not frozen:
            x = sphere_exp(x, -eta * oracle * u)
    return {
        "d": manifold_d,
        "ambient_d": d,
        "epsilon": epsilon,
        "horizon": horizon,
        "seed": seed,
        "mean_random_iterate_gradient_norm": float(
            np.mean(gradient_norms)
        ),
        "final_gradient_norm": gradient_norms[-1],
        "oracle_calls": 2 * horizon,
        "reverse_oracle": reverse,
        "frozen_iterate": frozen,
        "norm_error": abs(float(x @ x) - 1),
    }


def project_ball(x: np.ndarray, radius: float = 2.0) -> np.ndarray:
    norm = np.linalg.norm(x)
    if norm <= radius:
        return x
    return radius * x / norm


def convex_rdngd(
    d: int, epsilon: float, horizon: int, seed: int, reverse: bool = False
) -> dict:
    rng = np.random.default_rng(seed)
    x = np.ones(d) * (1.5 / math.sqrt(d))
    best = 0.5 * float(x @ x)
    distance = float(x @ x)
    eta = math.sqrt(epsilon) / (4 * math.sqrt(math.pi * d))
    nu = (
        (epsilon**1.5)
        / (
            4
            * math.sqrt(2)
            * d
            * (math.sqrt(distance) + eta * horizon) ** 2
        )
    )
    for _ in range(horizon):
        u = unit_vector(rng, d)
        plus = x + nu * u
        minus = x - nu * u
        oracle = (
            1.0
            if 0.5 * float(plus @ plus) > 0.5 * float(minus @ minus)
            else -1.0
        )
        if reverse:
            oracle *= -1
        x = project_ball(x - eta * oracle * u)
        best = min(best, 0.5 * float(x @ x))
    return {
        "d": d,
        "epsilon": epsilon,
        "horizon": horizon,
        "seed": seed,
        "best_suboptimality": best,
        "oracle_calls": 2 * horizon,
        "reverse_oracle": reverse,
        "feasible": bool(np.linalg.norm(x) <= 2 + 1e-12),
    }


def mean_upper_95(values: list[float]) -> tuple[float, float]:
    mean = float(np.mean(values))
    standard_error = float(np.std(values, ddof=1) / math.sqrt(len(values)))
    return mean, mean + 2.093 * standard_error


def calibrate_rdngd() -> dict:
    horizons = [32, 64, 128, 256, 512, 1024, 2048, 4096]
    nonconvex_calibration = []
    nonconvex_calibration_summaries = []
    convex_calibration = []
    nonconvex_selected = []
    convex_selected = []
    for d in (5, 9, 17):
        for epsilon in (0.35, 0.25, 0.18):
            candidates = []
            for horizon in horizons:
                rows = [
                    nonconvex_rdngd(
                        d, epsilon, horizon, SEED + 10000 * d + 100 * index
                    )
                    for index in range(6)
                ]
                values = [
                    row["mean_random_iterate_gradient_norm"] for row in rows
                ]
                mean = float(np.mean(values))
                standard_error = float(
                    np.std(values, ddof=1) / math.sqrt(len(values))
                )
                upper = mean + 2.571 * standard_error
                nonconvex_calibration.extend(rows)
                candidate = {
                    "ambient_d": d,
                    "d": d - 1,
                    "epsilon": epsilon,
                    "horizon": horizon,
                    "calibration_mean": mean,
                    "calibration_upper_95": upper,
                }
                nonconvex_calibration_summaries.append(candidate)
                candidates.append(candidate)
            selected = next(
                (
                    candidate["horizon"]
                    for candidate in candidates
                    if candidate["calibration_upper_95"] < 0.9 * epsilon
                ),
                horizons[-1],
            )
            validation = [
                nonconvex_rdngd(
                    d,
                    epsilon,
                    selected,
                    SEED + 500000 + 10000 * d + 100 * index,
                )
                for index in range(20)
            ]
            values = [
                row["mean_random_iterate_gradient_norm"] for row in validation
            ]
            mean, upper = mean_upper_95(values)
            nonconvex_selected.append(
                {
                    "ambient_d": d,
                    "d": d - 1,
                    "epsilon": epsilon,
                    "selected_horizon": selected,
                    "validation_mean": mean,
                    "validation_upper_95": upper,
                    "validation_rows": validation,
                }
            )

    for d in (4, 8, 16):
        for epsilon in (0.08, 0.04, 0.02):
            means = []
            for horizon in horizons:
                rows = [
                    convex_rdngd(
                        d, epsilon, horizon, SEED + 20000 * d + 100 * index
                    )
                    for index in range(6)
                ]
                mean = float(
                    np.mean([row["best_suboptimality"] for row in rows])
                )
                convex_calibration.extend(rows)
                means.append((horizon, mean))
            selected = next(
                (horizon for horizon, mean in means if mean < epsilon),
                horizons[-1],
            )
            validation = [
                convex_rdngd(
                    d,
                    epsilon,
                    selected,
                    SEED + 700000 + 20000 * d + 100 * index,
                )
                for index in range(20)
            ]
            values = [row["best_suboptimality"] for row in validation]
            mean, upper = mean_upper_95(values)
            convex_selected.append(
                {
                    "d": d,
                    "epsilon": epsilon,
                    "selected_horizon": selected,
                    "validation_mean": mean,
                    "validation_upper_95": upper,
                    "validation_rows": validation,
                }
            )

    nonconvex_control = nonconvex_rdngd(
        17, 0.18, 4096, SEED + 900001, frozen=True
    )
    convex_control = convex_rdngd(
        16, 0.02, 4096, SEED + 900002, reverse=True
    )
    return {
        "horizon_grid": horizons,
        "selection_rule": (
            "first calibration horizon whose six-seed one-sided 95% upper "
            "confidence bound is below 0.9 * epsilon; validation seeds are untouched"
        ),
        "validation_rule": "held-out 20 seeds; report mean and two-sided-t upper endpoint",
        "nonconvex_calibration": nonconvex_calibration,
        "nonconvex_calibration_summaries": nonconvex_calibration_summaries,
        "nonconvex_selected": nonconvex_selected,
        "convex_calibration": convex_calibration,
        "convex_selected": convex_selected,
        "controls": {
            "discarded_comparisons_nonconvex": nonconvex_control,
            "reversed_convex_oracle": convex_control,
        },
    }


def corrected_rrdngd() -> dict:
    rows = []
    slopes = {}
    for d in (4, 8, 16):
        phase_length = math.ceil(1 + 64 * math.pi * d)
        for repeat in range(10):
            rng = np.random.default_rng(SEED + 30000 * d + repeat)
            x = np.ones(d) / math.sqrt(d)
            distance_bound = 1.0
            cumulative_queries = 0
            for phase in range(8):
                phase_target = distance_bound / 4
                eta = math.sqrt(phase_target / (math.pi * d)) / 4
                nu = (
                    phase_target**1.5
                    / (
                        4
                        * math.sqrt(2)
                        * d
                        * (
                            2 * math.sqrt(phase_target)
                            + eta * phase_length
                        )
                        ** 2
                    )
                )
                best = x.copy()
                best_value = 0.5 * float(best @ best)
                for _ in range(phase_length):
                    u = unit_vector(rng, d)
                    plus = x + nu * u
                    minus = x - nu * u
                    oracle = (
                        1.0
                        if float(plus @ plus) > float(minus @ minus)
                        else -1.0
                    )
                    x = project_ball(x - eta * oracle * u)
                    value = 0.5 * float(x @ x)
                    if value < best_value:
                        best, best_value = x.copy(), value
                x = best
                distance_bound /= 2
                cumulative_queries += 2 * phase_length
                rows.append(
                    {
                        "d": d,
                        "repeat": repeat,
                        "phase": phase,
                        "suboptimality": best_value,
                        "cumulative_queries": cumulative_queries,
                    }
                )
        medians = [
            float(
                np.median(
                    [
                        row["suboptimality"]
                        for row in rows
                        if row["d"] == d and row["phase"] == phase
                    ]
                )
            )
            for phase in range(8)
        ]
        slopes[str(d)] = float(
            np.polyfit(np.arange(8), np.log2(medians), 1)[0]
        )
    return {
        "schedule": "proof-consistent epsilon_k=alpha D_k/4",
        "rows": rows,
        "log2_median_error_slope_per_phase": slopes,
        "queries_per_phase": {
            str(d): 2 * math.ceil(1 + 64 * math.pi * d)
            for d in (4, 8, 16)
        },
    }


def rdfw_run(d: int, horizon: int, seed: int, reverse: bool = False) -> dict:
    rng = np.random.default_rng(seed)
    tangent_d = d - 1
    c_hat = exact_c_hat(tangent_d)
    diameter = math.sqrt(2)
    target = np.arange(1, d + 1, dtype=float)
    target /= target.sum()
    x = np.ones(d) / d
    query_count = 0
    for iteration in range(horizon):
        batch = math.ceil(
            8
            * tangent_d
            * diameter**2
            * (iteration + 3)
            / c_hat**2
        )
        u = rng.normal(size=(batch, d))
        u -= u.mean(axis=1, keepdims=True)
        u /= np.linalg.norm(u, axis=1, keepdims=True)
        nu = (
            math.sqrt(math.pi / 8)
            * c_hat
            * 2
            / (tangent_d * diameter * (iteration + 3))
        )
        plus = 0.5 * np.sum((x + nu * u - target) ** 2, axis=1)
        minus = 0.5 * np.sum((x - nu * u - target) ** 2, axis=1)
        signs = np.where(plus > minus, 1.0, -1.0)
        if reverse:
            signs *= -1
        estimate = (signs[:, None] * u).mean(axis=0)
        vertex = np.zeros(d)
        vertex[int(np.argmin(estimate))] = 1
        step = 2 / (iteration + 3)
        x = (1 - step) * x + step * vertex
        query_count += 2 * batch
    return {
        "ambient_d": d,
        "d": tangent_d,
        "horizon": horizon,
        "seed": seed,
        "suboptimality": 0.5 * float(np.sum((x - target) ** 2)),
        "oracle_calls": query_count,
        "lmo_calls": horizon,
        "projection_calls": 0,
        "feasibility_sum_error": abs(float(x.sum()) - 1),
        "feasibility_min": float(x.min()),
        "reverse_oracle": reverse,
    }


def rdfw_sweep() -> dict:
    horizons = [10, 20, 40, 80]
    rows = []
    summaries = []
    slopes = {}
    for d in (4, 8, 16):
        for horizon in horizons:
            group = [
                rdfw_run(
                    d,
                    horizon,
                    SEED + 40000 * d + 100 * horizon + repeat,
                )
                for repeat in range(6)
            ]
            rows.extend(group)
            summaries.append(
                {
                    "ambient_d": d,
                    "d": d - 1,
                    "horizon": horizon,
                    "median_suboptimality": float(
                        np.median([row["suboptimality"] for row in group])
                    ),
                    "median_oracle_calls": float(
                        np.median([row["oracle_calls"] for row in group])
                    ),
                }
            )
        dimension_rows = [
            row for row in summaries if row["ambient_d"] == d
        ]
        slopes[str(d - 1)] = {
            "error_vs_horizon": float(
                np.polyfit(
                    np.log([row["horizon"] for row in dimension_rows]),
                    np.log(
                        [
                            row["median_suboptimality"]
                            for row in dimension_rows
                        ]
                    ),
                    1,
                )[0]
            ),
            "queries_vs_horizon": float(
                np.polyfit(
                    np.log([row["horizon"] for row in dimension_rows]),
                    np.log(
                        [
                            row["median_oracle_calls"]
                            for row in dimension_rows
                        ]
                    ),
                    1,
                )[0]
            ),
        }
    control = rdfw_run(16, 80, SEED + 999999, reverse=True)
    assert all(
        row["projection_calls"] == 0
        and row["feasibility_sum_error"] < 1e-12
        and row["feasibility_min"] >= -1e-15
        for row in rows
    )
    return {
        "horizon_grid": horizons,
        "batch_schedule": "ceil(8 d L diameter^2 (k+3)/C_hat^2)",
        "rows": rows,
        "summaries": summaries,
        "loglog_slopes": slopes,
        "reversed_oracle_control": control,
    }


def verify() -> dict:
    started = time.perf_counter()
    rdngd = calibrate_rdngd()
    rrdngd = corrected_rrdngd()
    rdfw = rdfw_sweep()
    nonconvex_success = sum(
        row["validation_upper_95"] < row["epsilon"]
        for row in rdngd["nonconvex_selected"]
    )
    convex_success = sum(
        row["validation_upper_95"] < row["epsilon"]
        for row in rdngd["convex_selected"]
    )
    assert rdngd["controls"]["discarded_comparisons_nonconvex"][
        "mean_random_iterate_gradient_norm"
    ] > 0.18
    assert rdngd["controls"]["reversed_convex_oracle"][
        "best_suboptimality"
    ] > 0.02
    assert nonconvex_success == 9
    assert convex_success == 9
    result = {
        "paper": "2603.00023",
        "seed_root": SEED,
        "actual_logical_cpus": os.cpu_count(),
        "rdngd": rdngd,
        "rrdngd": rrdngd,
        "rdfw": rdfw,
        "summary": {
            "nonconvex_validation_cells_passing": nonconvex_success,
            "nonconvex_validation_cells_total": 9,
            "convex_validation_cells_passing": convex_success,
            "convex_validation_cells_total": 9,
            "rrdngd_slopes": rrdngd[
                "log2_median_error_slope_per_phase"
            ],
            "rdfw_slopes": rdfw["loglog_slopes"],
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    output = ROOT / "outputs/empirical_algorithms.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("EMPIRICAL_ALGORITHMS_JSON=" + json.dumps(result, sort_keys=True))
    print(json.dumps({"empirical_algorithms_summary": result["summary"]}, sort_keys=True))
    return result


if __name__ == "__main__":
    verify()
