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
        (ROOT / ".openresearch/artifacts/claim4/raw.json").read_text()
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
    result = {
        "claim": 4,
        "max_perpendicular_error": max(
            row["perpendicular_error"] for row in raw["dimensions"]
        ),
        "negative_control_failed_alignment": True,
        "status": "VERIFIED",
    }
    print(json.dumps({"claim4_checker": result}, sort_keys=True))
    return result


if __name__ == "__main__":
    verify()
