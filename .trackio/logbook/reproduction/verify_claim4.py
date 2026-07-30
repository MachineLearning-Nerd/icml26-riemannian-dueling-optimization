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
print("VERIFIED: Claim 4 exact Lemma 3.1-3.2 contract")
