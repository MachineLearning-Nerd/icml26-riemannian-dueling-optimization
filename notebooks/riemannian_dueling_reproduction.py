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
    | 2 | printed gap 8.02e-5 > target 1e-6 | FALSIFIED as printed |
    | 3 | zero-projection RDFW + exact oracle sum | VERIFIED |
    | 4 | max perpendicular error 0.00412 | VERIFIED |
    | 5 | attack 3/4; SO(2) 19/19 | VERIFIED mechanism |
    | 6 | dense-SPD relative gaps < 2.5e-5 | VERIFIED scope |
    """)
    return


@app.cell
def _(mo):
    claim_data = [
        {"claim": 1, "status": "VERIFIED", "headline": "18/18 held-out cells"},
        {"claim": 2, "status": "FALSIFIED", "headline": "printed schedule misses 1e-6"},
        {"claim": 3, "status": "VERIFIED", "headline": "0 projections"},
        {"claim": 4, "status": "VERIFIED", "headline": "80k samples/dimension"},
        {"claim": 5, "status": "VERIFIED", "headline": "3/4 attack; 19/19 SO(2)"},
        {"claim": 6, "status": "VERIFIED", "headline": "dense n=5,10; m=50"},
    ]
    mo.ui.table(claim_data, pagination=False)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why Claim 2 is a falsification

    Algorithm 2 prints `epsilon_k = alpha D / 2^(2-k)`, which grows.
    Appendix F requires `alpha D / 2^(k+2)`, which shrinks. On the fully
    assumption-satisfying objective `f(x)=x²/2` over `[-2,2]`, the printed
    schedule stops at `8.024201e-5`; the proof-consistent control reaches
    `2.257724e-16`.

    ## Reproduction boundary

    The notebook embeds accepted results and never launches the expensive
    suite. Formal evidence comes from the fixed locked command on Hugging
    Face CPU. No GPU was used. The exact paper-setting attack and licensed
    HLW pixels are not represented as successes.
    """)
    return


if __name__ == "__main__":
    app.run()
