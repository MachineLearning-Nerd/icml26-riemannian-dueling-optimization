#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]


def symbolic_certificates() -> dict:
    epsilon, c_hat, d, length, smooth, distance = sp.symbols(
        "epsilon c_hat d L D", positive=True
    )
    horizon_root = smooth * sp.sqrt(d) * (distance + 1) / (
        c_hat * epsilon
    )
    nonconvex_optimization = (
        smooth
        * sp.sqrt(d)
        * (distance + 1)
        / (2 * c_hat * horizon_root)
    )
    nu = c_hat * sp.sqrt(2 * sp.pi) * epsilon / (
        4 * d * smooth
    )
    nonconvex_smoothing = (
        2 * d * smooth * nu / (c_hat * sp.sqrt(2 * sp.pi))
    )
    assert sp.simplify(nonconvex_optimization - epsilon / 2) == 0
    assert sp.simplify(nonconvex_smoothing - epsilon / 2) == 0

    curvature = sp.symbols("zeta", positive=True)
    convex_horizon = 1 + (
        16
        * sp.pi
        * d
        * smooth
        * curvature
        * distance
        / epsilon
    )
    convex_total_decrement = (
        (convex_horizon - 1)
        * epsilon
        / (16 * sp.pi * d * smooth * curvature)
    )
    assert sp.simplify(convex_total_decrement - distance) == 0

    k, phases = sp.symbols("k T", integer=True, nonnegative=True)
    batch_coefficient = sp.symbols("a", positive=True)
    batch_sum = sp.summation(
        batch_coefficient * d * (k + 3), (k, 0, phases - 1)
    )
    expected_sum = (
        batch_coefficient * d * phases * (phases + 5) / 2
    )
    assert sp.simplify(batch_sum - expected_sum) == 0

    return {
        "claim1_nonconvex": {
            "optimization_term": str(
                sp.simplify(nonconvex_optimization)
            ),
            "smoothing_term": str(sp.simplify(nonconvex_smoothing)),
            "sum": str(
                sp.simplify(
                    nonconvex_optimization + nonconvex_smoothing
                )
            ),
            "certificate": "T >= L^2 d (D+1)^2/(C_hat^2 epsilon^2)",
        },
        "claim1_convex": {
            "contradiction_decrement_at_T_minus_1": str(
                sp.simplify(convex_total_decrement)
            ),
            "certificate": "T >= 1 + 16 pi d L zeta D/epsilon",
        },
        "claim3_rdfw": {
            "batch_sum": str(expected_sum),
            "two_query_oracle_sum": str(2 * expected_sum),
            "certificate": "T=O(1/epsilon) implies 2 sum M_k=O(d/epsilon^2)",
        },
    }


def comparison_direction(x: float, nu: float, u: float) -> float:
    plus = 0.5 * (x + nu * u) ** 2
    minus = 0.5 * (x - nu * u) ** 2
    oracle = 1.0 if plus > minus else -1.0
    return oracle * u


def rdngd_phase(
    x: float, eta: float, nu: float, iterations: int
) -> tuple[float, float]:
    best = x
    for inner in range(iterations):
        u = 1.0 if inner % 2 == 0 else -1.0
        x = max(-2.0, min(2.0, x - eta * comparison_direction(x, nu, u)))
        if x * x < best * best:
            best = x
    return best, 0.5 * best * best


def rrdngd_schedule(schedule: str, target: float) -> dict:
    d = smooth = strong = curvature = distance = 1.0
    lipschitz = 2.0
    phases = math.ceil(
        math.log2(lipschitz * lipschitz * distance / target**2)
    )
    phase_length = math.ceil(
        1 + 64 * math.pi * d * smooth * curvature / strong
    )
    x = 1.0
    rows = []
    for phase in range(phases):
        if schedule == "printed":
            phase_target = strong * distance / 2 ** (2 - phase)
        else:
            phase_target = strong * distance / 2 ** (phase + 2)
        eta = (
            math.sqrt(
                phase_target / (math.pi * d * smooth)
            )
            / (4 * curvature)
        )
        nu = (
            (phase_target / smooth) ** 1.5
            / (
                4
                * math.sqrt(2)
                * d
                * (
                    2 * math.sqrt(phase_target / strong)
                    + eta * phase_length
                )
                ** 2
            )
        )
        x, gap = rdngd_phase(x, eta, nu, phase_length)
        rows.append(
            {
                "phase": phase,
                "phase_target": phase_target,
                "eta": eta,
                "nu": nu,
                "best_gap": gap,
            }
        )
    return {
        "schedule": schedule,
        "target": target,
        "phases": phases,
        "phase_length": phase_length,
        "oracle_calls": 2 * phases * phase_length,
        "final_gap": rows[-1]["best_gap"],
        "meets_target": rows[-1]["best_gap"] <= target,
        "rows": rows,
    }


def verify() -> dict:
    certificates = symbolic_certificates()
    target = 1e-6
    printed = rrdngd_schedule("printed", target)
    corrected = rrdngd_schedule("proof_consistent", target)
    assert not printed["meets_target"]
    assert corrected["meets_target"]
    for phase in range(1, 8):
        printed_target = printed["rows"][phase]["phase_target"]
        proof_target = corrected["rows"][phase]["phase_target"]
        assert math.isclose(
            printed_target / proof_target, 2 ** (2 * phase)
        )
    result = {
        "paper": "2603.00023",
        "source_sha256": "1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323",
        "symbolic_certificates": certificates,
        "claim2_counterexample": {
            "assumptions": {
                "domain": "Euclidean R restricted to X=[-2,2]",
                "f": "f(x)=x^2/2",
                "dimension": 1,
                "L_smooth": 1,
                "alpha_strongly_convex": 1,
                "curvature_lower_bound": 0,
                "projection_nonexpansive": True,
                "optimum_interior": True,
                "initial_squared_distance": 1,
                "lipschitz_constant_on_X": 2,
            },
            "printed": printed,
            "proof_consistent_control": corrected,
            "source_mismatch": "printed epsilon_k / proof epsilon_k = 2^(2k)",
            "status": "FALSIFIED",
        },
    }
    output = ROOT / "outputs/theorem_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    summary = {
        "claim1_symbolic_certificate": "PASS",
        "claim2_printed_final_gap": printed["final_gap"],
        "claim2_proof_consistent_final_gap": corrected["final_gap"],
        "claim2_target": target,
        "claim2_status": "FALSIFIED",
        "claim3_symbolic_certificate": "PASS",
    }
    print("THEOREM_AUDIT_JSON=" + json.dumps(result, sort_keys=True))
    print(json.dumps({"theorem_audit_summary": summary}, sort_keys=True))
    return result


if __name__ == "__main__":
    verify()
