# ---------------------------------------------------------------
# EXPERIENCE 5 (v0) -- DONNEES REELLES : VOCABULAIRE BRUT vs EXPERT
# German Credit (UCI). Pipeline du go/no-go du projet (Linear X-14/X-15).
#
# HYPOTHESE (ecrite avant l'experience, 2026-07-05) :
#   Sur donnees de credit, le vocabulaire expert -- des concepts qui
#   MELANGENT les dimensions brutes (mensualite = montant/duree,
#   charge = mensualite x taux d'effort) -- domine la courbe
#   d'explicabilite du vocabulaire brut, surtout a petit budget.
#
# PREDICTION DE CONTROLE (issue de l'Exp 1b / Proposition 1) :
#   Un vocabulaire "pseudo-expert" fait uniquement de deformations
#   monotones coordonnee-par-coordonnee (log montant, sqrt duree...)
#   ne change RIEN a la courbe. Si ce controle bouge, la Proposition 1
#   est en danger ; s'il ne bouge pas, c'est sa premiere confirmation
#   hors monde synthetique.
#
# CRITERE DE FALSIFICATION (a priori) :
#   Si la courbe du vocabulaire expert-melange est indistinguable de la
#   courbe brute (ecart d'AUC < 1 ecart-type inter-seeds), le
#   desalignement naturel n'existe pas sur ces donnees -> pese NO-GO.
#
# MODES :
#   --dry-run : monde credit semi-synthetique dont le G* est ecrit DANS
#     le vocabulaire expert. Valide la chaine de mesure de bout en bout
#     (le pipeline doit detecter la dominance quand elle existe par
#     construction). Ne vaut PAS decision go/no-go.
#   (defaut) : donnees reelles. Requiert data/german_credit.data
#     (python data/download_uci.py, ou depot manuel du fichier).
# ---------------------------------------------------------------

import argparse
import os
import sys

import numpy as np
from sklearn.neural_network import MLPClassifier

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
from rex import explainability_auc, fidelity_curve  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BUDGETS = [2, 4, 8, 16, 32, 64, 128, 256]
N_SEEDS = 5


# ----------------------------------------------------------------
# Monde credit semi-synthetique (dry-run) : G* ecrit en vocabulaire expert
# ----------------------------------------------------------------
def make_synthetic_credit(n, rng):
    montant = rng.uniform(500, 20000, n)
    duree = rng.uniform(6, 60, n)
    age = rng.uniform(19, 75, n)
    taux_remb = rng.integers(1, 5, n).astype(float)   # % du revenu disponible (1-4)
    epargne = rng.uniform(0, 1, n)
    anciennete = rng.uniform(0, 1, n)
    X_raw = np.column_stack([montant, duree, age, taux_remb, epargne, anciennete])

    mensualite = montant / duree
    y = np.where(
        (mensualite > 300) & (taux_remb >= 3), 1,
        np.where((age < 25) & (montant > 8000), 1,
                 np.where((epargne < 0.2) & (mensualite > 200), 1, 0)),
    )
    return X_raw, y


def synthetic_vocabularies(X_raw):
    montant, duree, age, taux_remb, epargne, anciennete = X_raw.T
    mensualite = montant / duree
    charge = mensualite * taux_remb
    # Vocabulaire expert : brut + concepts qui MELANGENT les dimensions.
    V_expert = np.column_stack([X_raw, mensualite, charge])
    # Controle monotone : deformations coordonnee-par-coordonnee, zero melange.
    V_mono = np.column_stack([
        np.log(montant), np.sqrt(duree), age ** 2, taux_remb,
        np.tanh(3 * (epargne - 0.5)), anciennete,
    ])
    return {"brut": X_raw, "expert (melange)": V_expert, "controle monotone": V_mono}


# ----------------------------------------------------------------
# Donnees reelles : German Credit (UCI, format german.data)
# ----------------------------------------------------------------
NUMERIC_COLS = {1: "duree", 4: "montant", 7: "taux_remb", 10: "residence",
                12: "age", 15: "nb_credits", 17: "nb_dependants"}


def load_german_credit(path):
    rows = [l.split() for l in open(path) if l.strip()]
    raw = np.array(rows)
    y = (raw[:, -1].astype(int) == 2).astype(int)      # 2 = mauvais credit
    num = raw[:, list(NUMERIC_COLS)].astype(float)
    # Categorielles -> one-hot (vocabulaire partage par tous les recepteurs)
    cat_idx = [j for j in range(20) if j not in NUMERIC_COLS]
    onehots = []
    for j in cat_idx:
        vals = np.unique(raw[:, j])
        onehots.append((raw[:, j][:, None] == vals[None, :]).astype(float))
    X_raw = np.column_stack([num] + onehots)
    return X_raw, y, num


def german_vocabularies(X_raw, num):
    duree, montant, taux_remb, residence, age, nb_credits, nb_dep = num.T
    mensualite = montant / duree
    charge = mensualite * taux_remb
    exposition = montant * nb_credits
    V_expert = np.column_stack([X_raw, mensualite, charge, exposition])
    V_mono = X_raw.copy()
    V_mono[:, 0] = np.sqrt(duree)
    V_mono[:, 1] = np.log(montant)
    V_mono[:, 4] = age ** 2
    return {"brut": X_raw, "expert (melange)": V_expert, "controle monotone": V_mono}


# ----------------------------------------------------------------
def run(dry_run):
    curves = {}
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(seed)
        if dry_run:
            X_raw, y = make_synthetic_credit(6000, rng)
            vocabs = synthetic_vocabularies(X_raw)
            n_tr = 5000
        else:
            path = os.path.join(HERE, "..", "data", "german_credit.data")
            if not os.path.exists(path):
                sys.exit("data/german_credit.data manquant : lancer data/download_uci.py "
                         "ou deposer le fichier, ou utiliser --dry-run.")
            X_raw, y, num = load_german_credit(path)
            perm = rng.permutation(len(X_raw))
            X_raw, y, num = X_raw[perm], y[perm], num[perm]
            vocabs = german_vocabularies(X_raw, num)
            n_tr = int(0.8 * len(X_raw))

        # Normalisation par colonne pour le MLP (les arbres y sont insensibles)
        mu, sd = X_raw[:n_tr].mean(0), X_raw[:n_tr].std(0) + 1e-9
        M = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
        M.fit((X_raw[:n_tr] - mu) / sd, y[:n_tr])
        yM_tr = M.predict((X_raw[:n_tr] - mu) / sd)
        yM_te = M.predict((X_raw[n_tr:] - mu) / sd)
        acc = (M.predict((X_raw[n_tr:] - mu) / sd) == y[n_tr:]).mean()

        for name, V in vocabs.items():
            fids = fidelity_curve(V[:n_tr], yM_tr, V[n_tr:], yM_te, BUDGETS)
            curves.setdefault(name, []).append(fids)
        curves.setdefault("_acc", []).append(acc)

    accs = curves.pop("_acc")
    print(f"{'[DRY-RUN semi-synthetique]' if dry_run else '[German Credit reel]'} "
          f"MLP accuracy : {np.mean(accs):.4f} +/- {np.std(accs):.4f}\n")

    print("Fidelite moyenne (+/- std) par budget et par vocabulaire :")
    names = list(curves)
    print("budget | " + " | ".join(f"{n:>20}" for n in names))
    mean = {n: np.mean(curves[n], 0) for n in names}
    std = {n: np.std(curves[n], 0) for n in names}
    for i, b in enumerate(BUDGETS):
        print(f"{b:6d} | " + " | ".join(f"{mean[n][i]:.3f}±{std[n][i]:.3f}".rjust(20) for n in names))

    print("\nAUC d'explicabilite (moyenne fidelite sur budgets) :")
    aucs_per_seed = {n: [explainability_auc(c) for c in curves[n]] for n in names}
    for n in names:
        print(f"  {n}: {np.mean(aucs_per_seed[n]):.4f} +/- {np.std(aucs_per_seed[n]):.4f}")

    gap = np.array(aucs_per_seed["expert (melange)"]) - np.array(aucs_per_seed["brut"])
    ctrl = np.array(aucs_per_seed["controle monotone"]) - np.array(aucs_per_seed["brut"])
    print(f"\nEcart AUC expert - brut     : {gap.mean():+.4f} +/- {gap.std():.4f}"
          f"  -> {'DOMINANCE' if gap.mean() > gap.std() else 'indistinguable (falsifie)'}")
    print(f"Ecart AUC controle - brut   : {ctrl.mean():+.4f} +/- {ctrl.std():.4f}"
          f"  -> {'invariance OK (Prop 1)' if abs(ctrl.mean()) <= max(ctrl.std(), 0.01) else 'INVARIANCE VIOLEE ?'}")

    # Figure + resultats numeriques
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for n in names:
        ax.plot(BUDGETS, mean[n], marker="o", label=n)
        ax.fill_between(BUDGETS, mean[n] - std[n], mean[n] + std[n], alpha=0.15)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("budget (feuilles)")
    ax.set_ylabel("fidelite a M")
    ax.set_title("Exp 5 v0 — courbes d'explicabilite par vocabulaire"
                 + (" [dry-run]" if dry_run else " [German Credit]"))
    ax.legend()
    fig.tight_layout()
    tag = "dryrun" if dry_run else "german"
    figpath = os.path.join(HERE, "..", "figures", f"exp5_{tag}.png")
    fig.savefig(figpath, dpi=150)
    print(f"\nFigure : {figpath}")

    outdir = os.path.join(HERE, "results")
    os.makedirs(outdir, exist_ok=True)
    np.save(os.path.join(outdir, f"exp5_{tag}.npy"),
            {"budgets": BUDGETS,
             "mean": {n: mean[n].tolist() for n in names},
             "std": {n: std[n].tolist() for n in names},
             "auc": {n: [float(a) for a in aucs_per_seed[n]] for n in names}},
            allow_pickle=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="monde credit semi-synthetique (validation du pipeline)")
    run(p.parse_args().dry_run)
