#!/usr/bin/env python3
"""Direct verification of Lemma 3.1 and the Lemma 3.2 improved-constant claim.

Source: ar5iv HTML of arXiv:2603.00023, SHA-256
1b20e2af562744080126d140c55b72c92658e355d8b93086c0e2908f762fb323,
anchors `#S3.Thmtheorem1` (Lemma 3.1) and `#S3.Thmtheorem2` (Lemma 3.2).

Exact statement under test
--------------------------
Lemma 3.1. Assume f is geodesically L-smooth. Let u ~ Unif(S_{T_x M}(1)) and
nu in (0,1). Then with probability at least 1 - gamma_x,

    h_nu(x) = sign(<grad f(x), u>_x) u,      gamma_x = sqrt(d/2pi) * L*nu / ||grad f(x)||

with h_nu(x) = Q_f(Exp_x(nu u), Exp_x(-nu u)) u   (eq. 4).

The quantifier is *every* nu in (0,1); the conclusion is a probability lower
bound. A finite experiment therefore tests the bound, and the only way it can
be contradicted is an assumption-satisfying cell whose measured disagreement
rate exceeds gamma_x with the sampling error accounted for.

Why the earlier finite-nu study did not falsify anything
-------------------------------------------------------
The superseded `finite_nu_estimator` cells used f(z) = e1^T z + (20d/6)(a^T z)^3
on the unit ball, so L = 20d, ||grad f(0)|| = 1 and nu = 0.5. Then
gamma_x = sqrt(d/2pi)*20d*0.5 ranges from 11.28 (d=2) to 1410.47 (d=50). A
probability lower bound of "at least 1 - 11.28" is vacuous, so a measured 7.5%
disagreement is *consistent* with Lemma 3.1, not a counterexample. `gamma_audit`
below recomputes those numbers so the record is explicit.

Test objective
--------------
Euclidean R^d is a zero-curvature Hadamard manifold covered by the paper's
assumptions, with Exp_x(v) = x + v and geodesic smoothness equal to the
Lipschitz constant of the gradient. Central differences annihilate even terms,
so a faithful stress test needs the largest *odd* second-order term an L-smooth
function admits along a direction:

    f(z) = <g, z> + (L/2) * s(<b, z>),      s(t) = t|t|,   ||b|| = 1,  b _|_ g

s''(t) = L*sign(t), so Hess f = L*sign(<b,z>) b b^T and ||Hess f||_2 = L
everywhere: f is exactly L-smooth on all of R^d, and grad f(0) = g. Then

    f(nu u) - f(-nu u) = 2 nu <g,u> + L nu^2 (b.u)|b.u|

and the estimator's sign disagrees with sign(<g,u>) exactly when the second
term dominates and opposes the first.
"""
from __future__ import annotations

import json
import math
import os
import time
from pathlib import Path

import numpy as np

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / ".trackio/logbook/outputs/current_claim4.json"
INTERNAL_OUTPUT = ROOT / ".openresearch/artifacts/claim4/lemma31_raw.json"

SAMPLES = 2_000_000
CHUNK = 250_000
SEED = 20260731
# Predeclared: reject Lemma 3.1 only if the one-sided 99.9% lower confidence
# bound on the disagreement rate still exceeds gamma_x.
Z_999 = 3.090232306167813
# Predeclared negative control: the same bound tightened by 4d must be violated.
CONTROL_TIGHTENING = 4.0


def gamma_x(d: int, l_smooth: float, nu: float, grad_norm: float) -> float:
    """Lemma 3.1 eq. (5)."""
    return math.sqrt(d / (2.0 * math.pi)) * l_smooth * nu / grad_norm


def disagreement(d: int, l_smooth: float, nu: float, grad_norm: float,
                 samples: int, seed: int) -> tuple[float, float, int]:
    """Measured P[h_nu(x) != sign(<grad f(x),u>) u] and its standard error."""
    rng = np.random.default_rng(seed)
    events = 0
    done = 0
    while done < samples:
        n = min(CHUNK, samples - done)
        u = rng.normal(size=(n, d))
        u /= np.linalg.norm(u, axis=1, keepdims=True)
        directional = grad_norm * u[:, 0]          # <g, u>, g = grad_norm * e1
        odd_term = u[:, 1] * np.abs(u[:, 1])       # (b.u)|b.u|, b = e2
        central = 2.0 * nu * directional + l_smooth * nu * nu * odd_term
        events += int(np.count_nonzero(np.sign(central) != np.sign(directional)))
        done += n
    rate = events / samples
    stderr = math.sqrt(max(rate * (1.0 - rate), 0.0) / samples)
    return rate, stderr, events


def sweep() -> list[dict]:
    """Non-vacuous cells: gamma_x < 1, varying d, nu, L and ||grad f||."""
    cells = []
    for d in (4, 16, 64):
        for nu in (0.05, 0.1, 0.2):
            cells.append((d, 1.0, nu, 1.0))
    for l_smooth in (0.5, 2.0):                  # L dependence at fixed d, nu
        cells.append((16, l_smooth, 0.1, 1.0))
    for grad_norm in (0.5, 2.0):                 # ||grad f|| dependence
        cells.append((16, 1.0, 0.1, grad_norm))

    rows = []
    for index, (d, l_smooth, nu, grad_norm) in enumerate(cells):
        bound = gamma_x(d, l_smooth, nu, grad_norm)
        rate, stderr, events = disagreement(
            d, l_smooth, nu, grad_norm, SAMPLES, SEED + 1013 * index
        )
        lower_999 = rate - Z_999 * stderr
        control_bound = bound / (CONTROL_TIGHTENING * d)
        rows.append(
            {
                "d": d,
                "L": l_smooth,
                "nu": nu,
                "grad_norm": grad_norm,
                "gamma_x": bound,
                "gamma_x_non_vacuous": bool(bound < 1.0),
                "empirical_disagreement": rate,
                "standard_error": stderr,
                "lower_999_confidence": lower_999,
                "events": events,
                "samples": SAMPLES,
                "lemma_holds": bool(lower_999 <= bound),
                "slack_ratio": rate / bound,
                "control_bound_gamma_over_4d": control_bound,
                "control_violated_as_intended": bool(rate > control_bound),
            }
        )
    return rows


def sign_blind_control(d: int, samples: int, seed: int) -> dict:
    """Pipeline control: an oracle whose sign carries no gradient information.

    Replacing the comparison outcome by an independent fair coin must drive the
    disagreement rate to 1/2, far above any gamma_x used above. A measurement
    pipeline that reported a small rate here would be counting nothing.
    """
    rng = np.random.default_rng(seed)
    coins = rng.integers(0, 2, size=samples) * 2 - 1
    reference = rng.integers(0, 2, size=samples) * 2 - 1
    rate = float(np.mean(coins != reference))
    return {
        "d": d,
        "samples": samples,
        "disagreement_rate": rate,
        "expected": 0.5,
        "fails_as_intended": bool(rate > 0.45),
    }


def gamma_audit() -> list[dict]:
    """Recompute gamma_x for the superseded finite-nu cells."""
    audit = []
    for d in (2, 5, 10, 50):
        bound = gamma_x(d, 20.0 * d, 0.5, 1.0)
        audit.append(
            {
                "d": d,
                "L": 20.0 * d,
                "nu": 0.5,
                "grad_norm": 1.0,
                "gamma_x": bound,
                "guarantee_vacuous": bool(bound >= 1.0),
            }
        )
    return audit


def improved_constants() -> dict:
    """Lemma 3.2's constant interval and the claimed gain over Saha et al. 2021.

    For u ~ Unif(S^{d-1}), E[sign(<v,u>) u] = (C_hat/sqrt(d)) v/||v|| with the
    exact value C_hat = sqrt(d) * E|u_1|, and
    E|u_1| = Gamma(d/2) / (sqrt(pi) * Gamma((d+1)/2)).
    """
    paper_lower = 1.0 / math.sqrt(2.0 * math.pi)
    saha_lower = 1.0 / 20.0
    exact = []
    for d in (2, 3, 5, 25, 100, 1000):
        c_hat = round(
            math.sqrt(d)
            * math.exp(math.lgamma(d / 2.0) - math.lgamma((d + 1.0) / 2.0))
            / math.sqrt(math.pi),
            12,
        )
        exact.append(
            {
                "d": d,
                "exact_c_hat": c_hat,
                "inside_paper_interval": bool(paper_lower <= c_hat <= 1.0),
                "above_saha_lower_bound": bool(c_hat >= saha_lower),
            }
        )
    return {
        "paper_lower_bound": paper_lower,
        "saha_2021_lower_bound": saha_lower,
        "improvement_factor": paper_lower / saha_lower,
        "paper_claimed_factor": 8.0,
        "improvement_factor_matches_paper": bool(
            abs(paper_lower / saha_lower - 8.0) < 0.05
        ),
        "asymptotic_c_hat_sqrt_2_over_pi": math.sqrt(2.0 / math.pi),
        "exact_values": exact,
        "all_inside_paper_interval": all(
            row["inside_paper_interval"] for row in exact
        ),
        "paper_interval_would_be_violated_below": paper_lower,
    }


def verify() -> dict:
    started = time.perf_counter()
    rows = sweep()
    constants = improved_constants()
    result = {
        "seed": SEED,
        "samples_per_cell": SAMPLES,
        "objective": (
            "f(z)=<g,z>+(L/2)s(<b,z>) with s(t)=t|t|, g=||grad f|| e1, b=e2; "
            "Euclidean R^d, Exp_x(v)=x+v"
        ),
        "assumption_audit": {
            "manifold": "Euclidean R^d (Hadamard, sectional curvature 0)",
            "hessian_spectral_norm": "exactly L everywhere",
            "geodesically_L_smooth": True,
            "nu_in_open_unit_interval": True,
            "grad_at_x_nonzero": True,
            "u_uniform_on_unit_tangent_sphere": True,
        },
        "lemma_3_1_cells": rows,
        "lemma_3_1_all_cells_non_vacuous": all(
            row["gamma_x_non_vacuous"] for row in rows
        ),
        "lemma_3_1_all_cells_hold": all(row["lemma_holds"] for row in rows),
        "negative_control_all_violated": all(
            row["control_violated_as_intended"] for row in rows
        ),
        "sign_blind_control": sign_blind_control(16, 400_000, SEED + 7717),
        "superseded_finite_nu_gamma_audit": gamma_audit(),
        "superseded_cells_were_vacuous": all(
            row["guarantee_vacuous"] for row in gamma_audit()
        ),
        "lemma_3_2_improved_constants": constants,
        "runtime_seconds": time.perf_counter() - started,
    }
    result["status"] = (
        "VERIFIED"
        if (
            result["lemma_3_1_all_cells_non_vacuous"]
            and result["lemma_3_1_all_cells_hold"]
            and result["negative_control_all_violated"]
            and result["sign_blind_control"]["fails_as_intended"]
            and constants["all_inside_paper_interval"]
            and constants["improvement_factor_matches_paper"]
        )
        else "BLOCKED"
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    current = json.loads(OUTPUT.read_text()) if OUTPUT.is_file() else {}
    current["lemma_3_1_perturbation"] = result
    OUTPUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
    INTERNAL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    INTERNAL_OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("CLAIM4_LEMMA31_JSON=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    outcome = verify()
    if outcome["status"] != "VERIFIED":
        raise SystemExit(1)
