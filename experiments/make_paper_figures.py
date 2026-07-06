# ---------------------------------------------------------------
# FIGURES DU PAPIER (anglais, qualite publication)
#
# Trace les figures des Exp 1 et 2 a partir des resultats sauvegardes
# par exp1_solid.py et exp2.py (experiments/results/*.npy) — memes
# chiffres, zero re-calcul. Les figures des Exp 5/6/7 sont tracees
# directement par leurs scripts (labels anglais).
#
# Usage :
#   python exp1_solid.py && python exp2.py   # produit les .npy
#   python make_paper_figures.py             # produit les .png
# ---------------------------------------------------------------

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
FIGURES = os.path.join(HERE, "..", "figures")


def fig_exp1():
    data = np.load(os.path.join(RESULTS, "exp1_solid.npy"), allow_pickle=True).item()
    budgets, thetas = data["budgets"], data["thetas"]
    mean, std = data["mean"], data["std"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = plt.cm.viridis(np.linspace(0.0, 0.85, len(thetas)))
    for th, c in zip(thetas, colors):
        m, s = np.array(mean[th]), np.array(std[th])
        ax.plot(budgets, m, marker="o", ms=4, color=c,
                label=rf"$\theta = {th}$" + (" (aligned)" if th == 0 else ""))
        ax.fill_between(budgets, m - s, m + s, color=c, alpha=0.15)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("budget (leaves)")
    ax.set_ylabel("fidelity to M")
    ax.set_title("Exp 1 — explainability curves vs. receiver-basis misalignment (10 seeds)")
    ax.axhline(0.95, color="grey", ls="--", lw=0.8, alpha=0.6)
    ax.text(budgets[0], 0.952, "95% threshold", fontsize=8, color="grey")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    path = os.path.join(FIGURES, "exp1_courbes.png")
    fig.savefig(path, dpi=200)
    print(f"Figure : {path}")


def fig_exp2():
    data = np.load(os.path.join(RESULTS, "exp2.npy"), allow_pickle=True).item()
    ma, sa, mr, sr = (np.asarray(data[k]) for k in ("ma", "sa", "mr", "sr"))
    q = np.arange(len(ma))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(q, ma, marker="o", ms=4, color="#2f6fb7", label="R aligned")
    ax.fill_between(q, ma - sa, ma + sa, color="#2f6fb7", alpha=0.15)
    ax.plot(q, mr, marker="o", ms=4, color="#c23b3b",
            label=r"R rotated ($\theta = 1.5$)")
    ax.fill_between(q, mr - sr, mr + sr, color="#c23b3b", alpha=0.15)
    ax.axhline(0.90, color="grey", ls="--", lw=0.8, alpha=0.6)
    ax.text(0, 0.905, "90% threshold", fontsize=8, color="grey")
    ax.set_xlabel('number of why-questions (operator W)')
    ax.set_ylabel("fidelity of the reconstructed graph to M")
    ax.set_title("Exp 2 — reconstructing M's graph through dialogue (5 seeds)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    path = os.path.join(FIGURES, "exp2_dialogue.png")
    fig.savefig(path, dpi=200)
    print(f"Figure : {path}")


if __name__ == "__main__":
    fig_exp1()
    fig_exp2()
