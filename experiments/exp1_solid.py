import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from scipy.linalg import expm

# ---------------------------------------------------------------
# EXPERIENCE 1 -- VERSION SOLIDE
# 10 seeds x rotations completes d'angle controle + G* plus profond
# ---------------------------------------------------------------

def G_star(x):
    taille, teinte, forme, px, py = x
    if taille > 0.6 and teinte > 0.5:
        return 0
    elif forme > 0.7:
        return 1
    elif px < 0.3 and py < 0.3:
        return 0
    elif teinte < 0.2 and taille < 0.4:
        return 1
    else:
        return 2

def rotation_full(theta, seed):
    """Rotation de 'force' theta appliquee a TOUTES les dimensions.
    On genere une matrice antisymetrique aleatoire A normalisee,
    R = expm(theta * A) : theta=0 -> identite, theta grand -> melange complet."""
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(5, 5))
    A = (A - A.T) / 2
    A = A / np.linalg.norm(A, 2)   # normalise la plus grande vitesse angulaire
    return expm(theta * A)

budgets = [2, 4, 8, 16, 32, 64, 128, 256]
thetas = [0.0, 0.2, 0.4, 0.8, 1.5]   # radians "efficaces"
n_seeds = 10

curves = {th: [] for th in thetas}    # theta -> list (per seed) of fidelity curves
mlp_accs = []

for seed in range(n_seeds):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 1, size=(6000, 5))
    y = np.array([G_star(x) for x in X])
    Xtr, Xte, ytr, yte = X[:5000], X[5000:], y[:5000], y[5000:]

    M = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
    M.fit(Xtr, ytr)
    mlp_accs.append(M.score(Xte, yte))
    yM_tr, yM_te = M.predict(Xtr), M.predict(Xte)

    for th in thetas:
        R = rotation_full(th, seed=seed + 100)
        fids = []
        for b in budgets:
            t = DecisionTreeClassifier(max_leaf_nodes=b, random_state=0)
            t.fit(Xtr @ R, yM_tr)
            fids.append(t.score(Xte @ R, yM_te))
        curves[th].append(fids)

print(f"MLP accuracy: {np.mean(mlp_accs):.4f} +/- {np.std(mlp_accs):.4f}\n")
print("Fidelite moyenne (+/- std) par budget et par angle theta:")
header = "budget | " + " | ".join([f"th={th:>4}" for th in thetas])
print(header)
results_mean, results_std = {}, {}
for th in thetas:
    arr = np.array(curves[th])
    results_mean[th] = arr.mean(axis=0)
    results_std[th] = arr.std(axis=0)
for i, b in enumerate(budgets):
    row = f"{b:6d} | " + " | ".join([f"{results_mean[th][i]:.3f}±{results_std[th][i]:.3f}" for th in thetas])
    print(row)

# Metrique scalaire : AUC de la courbe (moyenne des fidelites sur budgets log)
print("\nAUC d'explicabilite (moyenne fidelite sur tous budgets):")
for th in thetas:
    auc = results_mean[th].mean()
    print(f"theta={th}: AUC = {auc:.4f}")

# Budget minimal pour atteindre 95% de fidelite
print("\nBudget minimal pour fidelite >= 0.95 (moyenne):")
for th in thetas:
    idx = np.where(results_mean[th] >= 0.95)[0]
    print(f"theta={th}: {budgets[idx[0]] if len(idx) else '>256 (jamais atteint)'}")

import os
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(outdir, exist_ok=True)
np.save(os.path.join(outdir, 'exp1_solid.npy'),
        {'budgets': budgets, 'thetas': thetas,
         'mean': {th: results_mean[th].tolist() for th in thetas},
         'std': {th: results_std[th].tolist() for th in thetas}},
        allow_pickle=True)
