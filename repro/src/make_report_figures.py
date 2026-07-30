#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / ".trackio/logbook/outputs"
IMAGES = ROOT / "reports/reproduction/images"
IMAGES.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10})


def save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(IMAGES / name, format="svg", bbox_inches="tight")
    plt.close()


c5 = json.loads((DATA / "claim5.json").read_text())
fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.barh(["paper settings", "calibrated comparison-only"], [0, 75], color=["#9ca3af", "#2563eb"])
ax.set(xlim=(0, 100), xlabel="attack success rate (%)", title="Headline: pairwise sphere attack succeeds after honest calibration")
ax.text(1, 0, "0/2 — BLOCKED", va="center")
ax.text(76, 1, "3/4", va="center")
save("headline_attack.svg")

c1 = json.loads((DATA / "claim1.json").read_text())
matrix = np.array([[row["horizon"] for row in c1["nonconvex"] if row["d"] == d] for d in (4, 8, 16)])
fig, ax = plt.subplots(figsize=(7.2, 3.6))
image = ax.imshow(np.log2(matrix), cmap="Blues", aspect="auto")
ax.set_xticks(range(3), [".35", ".25", ".18"])
ax.set_yticks(range(3), ["4", "8", "16"])
ax.set(xlabel="epsilon", ylabel="intrinsic dimension d", title="Held-out nonconvex RDNGD: independently selected horizon")
for i in range(3):
    for j in range(3):
        ax.text(j, i, str(matrix[i, j]), ha="center", va="center", color="black")
fig.colorbar(image, ax=ax, label="log2(T)")
save("claim1_horizons.svg")

c2 = json.loads((DATA / "claim2.json").read_text())["counterexample"]
fig, ax = plt.subplots(figsize=(7.2, 3.4))
values = [c2["printed_final_gap"], c2["proof_consistent_final_gap"]]
ax.bar(["Algorithm 2 as printed", "Appendix-F control"], values, color=["#dc2626", "#16a34a"])
ax.axhline(c2["target"], color="black", linestyle="--", label="target 1e-6")
ax.set_yscale("log")
ax.set(ylabel="final objective gap", title="Claim 2 counterexample separates printed and proof schedules")
ax.legend()
save("claim2_counterexample.svg")

c3 = json.loads((DATA / "claim3.json").read_text())
rows = c3["d15_rows"]
fig, ax = plt.subplots(figsize=(7.2, 3.4))
ax.loglog([row["horizon"] for row in rows], [row["median_suboptimality"] for row in rows], "o-", label="normal RDFW")
ax.scatter([80], [c3["negative_control"]["suboptimality"]], color="#dc2626", marker="x", s=80, label="reversed signs")
ax.set(xlabel="iterations T", ylabel="median suboptimality", title="Projection-free RDFW improves; reversed comparisons do not")
ax.legend()
save("claim3_rdfw.svg")

c6 = json.loads((DATA / "claim6.json").read_text())
fig, ax = plt.subplots(figsize=(7.2, 3.4))
labels = ["n=5", "n=10"]
x = np.arange(2)
width = 0.25
ax.bar(x - width, [r["initial_objective"] for r in c6["rows"]], width, label="initial")
ax.bar(x, [r["final_objective"] for r in c6["rows"]], width, label="RDNGD")
ax.bar(x + width, [r["reverse_final_objective"] for r in c6["rows"]], width, label="reversed signs")
ax.set_xticks(x, labels)
ax.set(ylabel="Karcher objective", title="Dense noncommuting SPD application at paper dimensions")
ax.legend()
save("claim6_spd.svg")
