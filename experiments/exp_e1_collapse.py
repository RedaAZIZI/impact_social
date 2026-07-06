# ---------------------------------------------------------------
# E1 (noyau formel v0.1, section 6) -- TEST DU COLLAPSE sin(2*theta)
# sur les courbes existantes de l'Exp 1 (experiments/results/exp1_solid.npy).
#
# Predictions de la loi theta [T 4.1, Cor 4.2] :
#   (i)  pente -1 en log-log de (1 - F(k)) contre k ;
#   (ii) collapse : k*(1 - F(k)) trace contre la variable de desalignement
#        doit etre affine, pour tous les budgets k a la fois ;
#   (iii) symetrie autour de 45 degres.
#
# SUBTILITE (Def 1.6 du noyau + construction de l'Exp 1) : notre theta est
# la NORME du generateur (R = expm(theta*A), ||A||_2 = 1), pas un angle
# principal unique. En 5D, A a deux plans invariants de vitesses lambda_1=1
# et lambda_2 <= 1 : la rotation reelle est (theta*lambda_1, theta*lambda_2).
# On teste donc DEUX variables de desalignement :
#   naive      : sin(2*theta)  (le theta-generateur pris pour un angle)
#   effective  : moyenne sur seeds et plans de |sin(2*theta*lambda_j)|
#                (angle de chaque plan, replie par la symetrie pi/2)
# ---------------------------------------------------------------

import os
import numpy as np
from scipy.linalg import expm

HERE = os.path.dirname(os.path.abspath(__file__))
d = np.load(os.path.join(HERE, "results", "exp1_solid.npy"), allow_pickle=True).item()
budgets = np.array(d["budgets"], dtype=float)
thetas = [t for t in d["thetas"] if t > 0]
F = {t: np.array(d["mean"][t]) for t in thetas}

def plane_speeds(seed):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(5, 5)); A = (A - A.T) / 2
    A = A / np.linalg.norm(A, 2)
    ev = np.linalg.eigvals(A)
    lam = np.sort(np.abs(ev.imag))[::-1]
    return lam[lam > 1e-9][::2]          # les 2 vitesses de plan (paires +/-i*lam)

speeds = [plane_speeds(seed + 100) for seed in range(10)]

def eff(theta):
    vals = []
    for lam in speeds:
        ang = theta * lam                              # angles reels des plans
        vals.append(np.mean(np.abs(np.sin(2 * ang))))  # repli symetrie pi/2
    return float(np.mean(vals))

naive = {t: np.sin(2 * t) for t in thetas}
effective = {t: eff(t) for t in thetas}

print("theta | sin(2*theta) naive | desalignement effectif (plans) | AUC")
for t in thetas:
    print(f"{t:5.1f} | {naive[t]:18.3f} | {effective[t]:30.3f} | {F[t].mean():.4f}")

# (i) pente log-log de (1-F) vs k, sur k >= 8 (avant plateau final)
print("\nPente log-log de (1 - F(k)) contre k (loi : -1) :")
for t in thetas:
    mask = (budgets >= 8) & (F[t] < 0.995)
    s, _ = np.polyfit(np.log(budgets[mask]), np.log(1 - F[t][mask]), 1)
    print(f"  theta={t}: pente = {s:.2f}")

# (ii) collapse : y = k*(1-F(k)) doit etre ~ c * variable, meme c pour tout k
print("\nCollapse k*(1-F(k)) = c * variable : R^2 de la regression lineaire")
print("(y agregee sur budgets 16..256, une observation par (theta, k))")
for name, var in [("naive sin(2*theta)", naive), ("effective (plans)", effective)]:
    xs, ys = [], []
    for t in thetas:
        for j, k in enumerate(budgets):
            if k < 16:
                continue
            xs.append(var[t]); ys.append(k * (1 - F[t][j]))
    xs, ys = np.array(xs), np.array(ys)
    A_ = np.vstack([xs, np.ones_like(xs)]).T
    coef, res, *_ = np.linalg.lstsq(A_, ys, rcond=None)
    ss_tot = ((ys - ys.mean()) ** 2).sum()
    r2 = 1 - (res[0] / ss_tot if len(res) else 0)
    print(f"  {name:22s}: pente {coef[0]:7.2f}, R^2 = {r2:.3f}")

# (iii) verdict de symetrie : la loi naive predit cost(1.5) << cost(0.8)
print("\nTest de symetrie (la loi naive predit theta=1.5 (86deg) moins couteux que 0.8 (46deg)) :")
print(f"  AUC(0.8) = {F[0.8].mean():.4f} ; AUC(1.5) = {F[1.5].mean():.4f} "
      f"-> {'SYMETRIE OBSERVEE' if F[1.5].mean() > F[0.8].mean() else 'PAS de symetrie naive (cout encore croissant a 86deg)'}")

# Figure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4))
for t in thetas:
    m = F[t] < 0.995
    axes[0].loglog(budgets[m], 1 - F[t][m], "o-", label=f"θ={t}")
axes[0].set_xlabel("budget k"); axes[0].set_ylabel("1 − F(k)")
axes[0].set_title("(i) pente log-log (loi : −1)"); axes[0].legend(fontsize=8)
for ax, (name, var) in zip(axes[1:], [("naïve sin(2θ)", naive), ("effective (plans)", effective)]):
    for j, k in enumerate(budgets):
        if k < 16: continue
        xs = [var[t] for t in thetas]
        ys = [k * (1 - F[t][j]) for t in thetas]
        ax.plot(xs, ys, "o-", alpha=.75, label=f"k={int(k)}")
    ax.set_xlabel(name); ax.set_ylabel("k·(1 − F(k))")
    ax.set_title("(ii) collapse vs " + name)
axes[2].legend(fontsize=7)
fig.tight_layout()
out = os.path.join(HERE, "..", "figures", "exp_e1_collapse.png")
fig.savefig(out, dpi=150)
print(f"\nFigure : {out}")
