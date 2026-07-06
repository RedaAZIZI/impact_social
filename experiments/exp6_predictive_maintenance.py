# ---------------------------------------------------------------
# EXPERIENCE 6 -- TERRAIN INGENIERIE : CAPTEURS BRUTS vs GRANDEURS COMPOSEES
# Maintenance predictive (AI4I 2020, UCI n°601). Deuxieme banc d'essai
# du go/no-go (Linear X-15), sur un terrain ou le processus generateur
# du monde EST ecrit en grandeurs composees (les lois physiques).
#
# HYPOTHESE (ecrite avant l'experience, 2026-07-06) :
#   Les modes de defaillance d'une machine sont regis par des grandeurs
#   composees (puissance = couple x vitesse angulaire ; dissipation =
#   T_process - T_air ; surcontrainte = usure x couple). Le vocabulaire
#   de l'ingenieur (capteurs bruts + ces grandeurs) domine la courbe
#   d'explicabilite du vocabulaire capteurs bruts, surtout a petit
#   budget. C'est le renversement issu de l'Exp 5 : la dominance du
#   vocabulaire expert exige que le monde soit ecrit en concepts
#   composes -- en physique, il l'est.
#
# CONTROLE (Exp 1b / Proposition 1) : un vocabulaire de deformations
#   monotones coordonnee-par-coordonnee reste inerte.
#
# CRITERE DE FALSIFICATION (a priori) :
#   Si sur AI4I 2020 (donnees reelles du benchmark) l'ecart d'AUC
#   ingenieur - brut est < 1 ecart-type inter-seeds, la these "le
#   desalignement naturel compte sur les terrains physiques" est
#   infirmee et le NO-GO devient serieux.
#
# LECONS DE L'EXP 5 INTEGREES AU PROTOCOLE (avant le run, pas apres) :
#   - Metrique = fidelite EQUILIBREE par classe (les defaillances sont
#     rares ; la fidelite brute serait dominee par la classe "aucune
#     panne" et rendrait le protocole muet, cf. German Credit).
#   - Verifier que M a de la structure : accuracy equilibree de M
#     rapportee a cote des courbes.
#
# MODES :
#   --simulate : simulation physique du meme moteur (memes lois que les
#     modes de defaillance AI4I : HDF, PWF, OSF), executable sans
#     donnees. Plus fort que le dry-run de l'Exp 5 (le G* n'est pas
#     arbitraire, il est dicte par la physique) mais ne vaut pas
#     decision : c'est le run AI4I reel qui compte.
#   (defaut) : donnees reelles. Requiert data/ai4i2020.csv.
# ---------------------------------------------------------------

import argparse
import os
import sys

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
from rex import explainability_auc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BUDGETS = [2, 4, 8, 16, 32, 64, 128, 256]
N_SEEDS = 5   # surchargeable par --seeds (repasse formelle : 10)

RAW_NAMES = ["T_air", "T_process", "vitesse_rpm", "couple", "usure"]


def balanced_fidelity(y_ref, y_pred):
    """Fidelite equilibree : accord moyen par classe de reference."""
    classes = np.unique(y_ref)
    return float(np.mean([(y_pred[y_ref == c] == c).mean() for c in classes]))


def balanced_fidelity_curve(Vtr, yM_tr, Vte, yM_te, budgets, seed=0):
    fids = []
    for b in budgets:
        t = DecisionTreeClassifier(max_leaf_nodes=int(b), class_weight="balanced",
                                   random_state=seed)
        t.fit(Vtr, yM_tr)
        fids.append(balanced_fidelity(yM_te, t.predict(Vte)))
    return np.array(fids)


# ----------------------------------------------------------------
# Simulation physique (memes lois que les modes de defaillance AI4I)
# ----------------------------------------------------------------
def make_machine_world(n, rng):
    T_air = rng.normal(300, 2, n)                      # K
    T_process = T_air + rng.normal(10, 1.5, n)         # K
    vitesse = np.clip(rng.normal(1540, 250, n), 1150, 2900)   # rpm
    couple = np.clip(rng.normal(40, 10, n), 10, 76)    # Nm
    usure = rng.uniform(0, 250, n)                     # min
    X = np.column_stack([T_air, T_process, vitesse, couple, usure])

    dT = T_process - T_air                             # K
    puissance = couple * vitesse * 2 * np.pi / 60      # W
    contrainte = usure * couple                        # min.Nm

    y = np.zeros(n, dtype=int)
    y[(dT < 8.6) & (vitesse < 1380)] = 1               # HDF : dissipation
    y[(y == 0) & ((puissance < 3500) | (puissance > 9000))] = 2   # PWF
    y[(y == 0) & (contrainte > 8000)] = 3              # OSF : surcontrainte
    return X, y


def vocabularies(X):
    T_air, T_process, vitesse, couple, usure = X.T
    dT = T_process - T_air
    puissance = couple * vitesse * 2 * np.pi / 60
    contrainte = usure * couple
    V_expert = np.column_stack([X, dT, puissance, contrainte])
    V_mono = np.column_stack([
        T_air - 273.15, np.log(T_process), np.sqrt(vitesse), couple ** 2, usure,
    ])
    return {"brut (capteurs)": X, "ingenieur (melange)": V_expert,
            "controle monotone": V_mono}


# ----------------------------------------------------------------
# Donnees reelles AI4I 2020 (data/ai4i2020.csv)
# ----------------------------------------------------------------
def load_ai4i(path):
    import csv
    with open(path) as f:
        rows = list(csv.DictReader(f))
    X = np.array([[float(r["Air temperature [K]"]),
                   float(r["Process temperature [K]"]),
                   float(r["Rotational speed [rpm]"]),
                   float(r["Torque [Nm]"]),
                   float(r["Tool wear [min]"])] for r in rows])
    y = np.zeros(len(rows), dtype=int)
    for i, r in enumerate(rows):
        if int(r["HDF"]):
            y[i] = 1
        elif int(r["PWF"]):
            y[i] = 2
        elif int(r["OSF"]):
            y[i] = 3
        elif int(r["TWF"]) or int(r["RNF"]):
            y[i] = 4          # modes residuels (usure seule / aleatoire)
    return X, y


# ----------------------------------------------------------------
def run(simulate, model="mlp"):
    curves = {}
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(seed)
        if simulate:
            X, y = make_machine_world(10000, rng)
        else:
            path = os.path.join(HERE, "..", "data", "ai4i2020.csv")
            if not os.path.exists(path):
                sys.exit("data/ai4i2020.csv manquant (UCI n°601), ou utiliser --simulate.")
            X, y = load_ai4i(path)
            perm = rng.permutation(len(X))
            X, y = X[perm], y[perm]
        n_tr = int(0.8 * len(X))
        vocabs = vocabularies(X)

        mu, sd = X[:n_tr].mean(0), X[:n_tr].std(0) + 1e-9
        if model == "gbt":
            M = HistGradientBoostingClassifier(class_weight="balanced", random_state=seed)
        else:
            M = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
        M.fit((X[:n_tr] - mu) / sd, y[:n_tr])
        yM_tr = M.predict((X[:n_tr] - mu) / sd)
        yM_te = M.predict((X[n_tr:] - mu) / sd)
        curves.setdefault("_acc", []).append(balanced_fidelity(y[n_tr:], yM_te))

        for name, V in vocabs.items():
            fids = balanced_fidelity_curve(V[:n_tr], yM_tr, V[n_tr:], yM_te, BUDGETS)
            curves.setdefault(name, []).append(fids)

    accs = curves.pop("_acc")
    mode = "[SIMULATION physique]" if simulate else "[AI4I 2020 reel]"
    print(f"{mode} accuracy EQUILIBREE de M ({model}) : "
          f"{np.mean(accs):.4f} +/- {np.std(accs):.4f}\n")

    names = list(curves)
    mean = {n: np.mean(curves[n], 0) for n in names}
    std = {n: np.std(curves[n], 0) for n in names}
    print("Fidelite equilibree (+/- std) par budget et par vocabulaire :")
    print("budget | " + " | ".join(f"{n:>22}" for n in names))
    for i, b in enumerate(BUDGETS):
        print(f"{b:6d} | " + " | ".join(f"{mean[n][i]:.3f}±{std[n][i]:.3f}".rjust(22) for n in names))

    print("\nAUC d'explicabilite (fidelite equilibree moyenne sur budgets) :")
    aucs = {n: [explainability_auc(c) for c in curves[n]] for n in names}
    for n in names:
        print(f"  {n}: {np.mean(aucs[n]):.4f} +/- {np.std(aucs[n]):.4f}")

    gap = np.array(aucs["ingenieur (melange)"]) - np.array(aucs["brut (capteurs)"])
    ctrl = np.array(aucs["controle monotone"]) - np.array(aucs["brut (capteurs)"])
    print(f"\nEcart AUC ingenieur - brut : {gap.mean():+.4f} +/- {gap.std():.4f}"
          f"  -> {'DOMINANCE' if gap.mean() > gap.std() else 'indistinguable (falsifie)'}")
    print(f"Ecart AUC controle - brut  : {ctrl.mean():+.4f} +/- {ctrl.std():.4f}"
          f"  -> {'invariance OK (Prop 1)' if abs(ctrl.mean()) <= max(ctrl.std(), 0.01) else 'INVARIANCE VIOLEE ?'}")

    # Statistiques formelles (appariees par seed) pour l'article
    from scipy import stats
    t, p_t = stats.ttest_rel(aucs["ingenieur (melange)"], aucs["brut (capteurs)"])
    try:
        w, p_w = stats.wilcoxon(gap)
    except ValueError:
        p_w = float("nan")
    print(f"Test t apparie (ingenieur vs brut, n={len(gap)} seeds) : t = {t:.3f}, p = {p_t:.4g}")
    print(f"Wilcoxon signe apparie : p = {p_w:.4g}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4.5))
    # Noms d'affichage anglais (figures publiques / papier) ; les cles internes restent
    display = {"brut (capteurs)": "raw (sensors)",
               "ingenieur (melange)": "engineer (compound)",
               "controle monotone": "monotone control"}
    for n in names:
        ax.plot(BUDGETS, mean[n], marker="o", label=display.get(n, n))
        ax.fill_between(BUDGETS, mean[n] - std[n], mean[n] + std[n], alpha=0.15)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("budget (leaves)")
    ax.set_ylabel("class-balanced fidelity to M")
    ax.set_title("Exp 6 — predictive maintenance: raw-sensor vs. engineer vocabularies"
                 + (" [simulation]" if simulate else " [AI4I 2020]"))
    ax.legend()
    fig.tight_layout()
    tag = ("sim" if simulate else "ai4i") + (f"_{model}" if model != "mlp" else "")
    figpath = os.path.join(HERE, "..", "figures", f"exp6_{tag}.png")
    fig.savefig(figpath, dpi=150)
    print(f"\nFigure : {figpath}")

    outdir = os.path.join(HERE, "results")
    os.makedirs(outdir, exist_ok=True)
    np.save(os.path.join(outdir, f"exp6_{tag}.npy"),
            {"budgets": BUDGETS,
             "mean": {n: mean[n].tolist() for n in names},
             "std": {n: std[n].tolist() for n in names},
             "auc": {n: [float(a) for a in aucs[n]] for n in names}},
            allow_pickle=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--simulate", action="store_true",
                   help="simulation physique (sans donnees ; ne vaut pas decision)")
    p.add_argument("--model", choices=["mlp", "gbt"], default="mlp")
    p.add_argument("--seeds", type=int, default=N_SEEDS)
    a = p.parse_args()
    N_SEEDS = a.seeds
    run(a.simulate, model=a.model)
