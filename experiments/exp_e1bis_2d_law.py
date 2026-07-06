# ---------------------------------------------------------------
# E1-bis -- LA LOI THETA TESTEE DANS SON PROPRE REGIME
# (modele minimal 2D exactement soluble du noyau formel, T 4.1 :
#  frontiere lineaire oblique d'angle theta vs vocabulaire axis-aligned)
#
# Verdict du run initial (2026-07-06, 5 seeds, n=40k, budgets 4..256) :
#   - symetrie theta <-> 90-theta : CONFIRMEE (AUC 35deg=0.9680 vs 55deg=0.9684 ;
#     15deg=0.9875 vs 75deg=0.9870)
#   - maximum du cout a 45deg : CONFIRME (AUC minimale a 45deg)
#   - monotonie en sin(2*theta) : CONFIRMEE
#   - pente log-log : -0.53..-0.81 (au lieu de -1) ; collapse R^2 = 0.43 —
#     l'ecart quantitatif est attribuable a CART glouton vs l'escalier
#     optimal de la preuve (a verifier contre l'escalier analytique).
# Contraste : sur l'Exp 1 (5D, listes de regles, rotation multi-plans),
# la forme naive de la loi ne persiste PAS (voir exp_e1_collapse.py) :
# pente universelle ~ -0.21, pas de symetrie -> c'est le chantier
# dimension-d [C 4.3] du noyau formel.
# ---------------------------------------------------------------
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
budgets = np.array([4, 8, 16, 32, 64, 128, 256])
degs = [5, 15, 25, 35, 45, 55, 65, 75, 85]
n_seeds = 5

F = {}
for deg in degs:
    th = np.deg2rad(deg)
    curves = []
    for seed in range(n_seeds):
        rng = np.random.default_rng(seed)
        X = rng.uniform(0, 1, size=(40000, 2))
        y = (X[:, 1] - 0.5 >= np.tan(th) * (X[:, 0] - 0.5)).astype(int) if deg <= 45 else \
            (X[:, 0] - 0.5 <= (X[:, 1] - 0.5) / np.tan(th)).astype(int)
        Xtr, Xte, ytr, yte = X[:30000], X[30000:], y[:30000], y[30000:]
        fids = []
        for k in budgets:
            t = DecisionTreeClassifier(max_leaf_nodes=int(k), random_state=0).fit(Xtr, ytr)
            fids.append(t.score(Xte, yte))
        curves.append(fids)
    F[deg] = np.array(curves).mean(0)

print("deg | sin(2t) | pente log-log (loi : -1) | AUC")
for deg in degs:
    m = (1 - F[deg]) > 1e-4
    s, _ = np.polyfit(np.log(budgets[m]), np.log(1 - F[deg][m]), 1)
    print(f"{deg:3d} | {np.sin(2*np.deg2rad(deg)):.3f} | {s:23.2f} | {F[deg].mean():.4f}")

xs, ys = [], []
for deg in degs:
    for j, k in enumerate(budgets):
        if k < 16:
            continue
        xs.append(np.sin(2 * np.deg2rad(deg))); ys.append(k * (1 - F[deg][j]))
xs, ys = np.array(xs), np.array(ys)
A = np.vstack([xs, np.ones_like(xs)]).T
coef, res, *_ = np.linalg.lstsq(A, ys, rcond=None)
r2 = 1 - res[0] / (((ys - ys.mean()) ** 2).sum())
print(f"\nCollapse 2D : k*(1-F) = {coef[0]:.2f}*sin(2t) + {coef[1]:.2f}, R^2 = {r2:.3f}")
print(f"Symetrie : AUC(35)={F[35].mean():.4f} vs AUC(55)={F[55].mean():.4f} ; "
      f"AUC(15)={F[15].mean():.4f} vs AUC(75)={F[75].mean():.4f}")
print(f"Max du cout a 45 deg ? {min(F[d].mean() for d in degs) == F[45].mean()}")

outdir = os.path.join(HERE, "results")
os.makedirs(outdir, exist_ok=True)
np.save(os.path.join(outdir, "exp_e1bis_2d.npy"),
        {"budgets": budgets.tolist(), "degs": degs, "F": {d: F[d].tolist() for d in degs}},
        allow_pickle=True)
