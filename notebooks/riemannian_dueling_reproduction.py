import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Riemannian Dueling Optimization — evidence first

    The optimizer sees only pairwise preferences. The strongest new
    application result is **3/4 successful CIFAR-10/VGG sphere attacks**;
    exact paper hyperparameters produced **0/2**, so that route remains
    separately BLOCKED.

    | Claim | Evidence | Verdict |
    |---|---|---|
    | 1 | symbolic rates + 18/18 held-out RDNGD cells | VERIFIED |
    | 2 | corrected slopes ≈ -1 bit/phase; printed schedule misses 1e-6 | VERIFIED intended; printed defect FALSIFIED |
    | 3 | zero-projection RDFW + exact oracle sum | VERIFIED |
    | 4 | ideal error <.0042; finite-nu bias lower bound ≥.0274 | FALSIFIED AS WRITTEN; ideal VERIFIED |
    | 5 | attack 3/4; SO(2) 19/19 | VERIFIED mechanism |
    | 6 | dense-SPD relative gaps < 2.5e-5 | VERIFIED scope |
    """)
    return


@app.cell
def _(mo):
    claim_data = [
        {"claim": 1, "status": "VERIFIED", "headline": "18/18 held-out cells"},
        {"claim": 2, "status": "VERIFIED", "headline": "≈ -1 bit/phase; printed defect"},
        {"claim": 3, "status": "VERIFIED", "headline": "0 projections"},
        {"claim": 4, "status": "FALSIFIED AS WRITTEN", "headline": "finite-nu paired bias > 0"},
        {"claim": 5, "status": "VERIFIED", "headline": "3/4 attack; 19/19 SO(2)"},
        {"claim": 6, "status": "VERIFIED", "headline": "dense n=5,10; m=50"},
    ]
    mo.ui.table(claim_data, pagination=False)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Claim 2: intended theorem versus printed schedule

    Algorithm 2 prints `epsilon_k = alpha D / 2^(2-k)`, which grows.
    Appendix F requires `alpha D / 2^(k+2)`, which shrinks. On the fully
    assumption-satisfying objective `f(x)=x²/2` over `[-2,2]`, the printed
    schedule stops at `8.024201e-5`; the proof-consistent control reaches
    `2.257724e-16`. The corrected algorithm has approximately one bit of
    median-error reduction per phase, so the intended theorem is VERIFIED
    while the printed schedule is separately FALSIFIED.

    ## Claim 4: ideal versus finite-perturbation estimator

    Lemma 3.2's ideal sign estimator matches its analytic expectation. For the
    actual finite-perturbation estimator at `nu=.5`, however, 200,000
    directions per dimension give 6.27–7.55% sign disagreement and paired
    orthogonal-bias 95% lower bounds of 0.0274–0.1467. Small-`nu` and linear
    controls have zero disagreement.

    ## Reproduction boundary

    The notebook embeds accepted results and never launches the expensive
    suite. Formal evidence comes from the fixed locked command on Hugging
    Face CPU. No GPU was used. The exact paper-setting attack and licensed
    HLW pixels are not represented as successes.
    """)
    return


if __name__ == "__main__":
    app.run()
