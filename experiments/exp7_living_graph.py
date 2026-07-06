# ---------------------------------------------------------------
# EXPERIENCE 7 -- "LE GRAPHE QUI VIT"
# L'edition en dialogue comme apprentissage continu post-gradient.
# PRE-ENREGISTREMENT : Linear X-28 (hypothese H7 + conditions de mort
# K1-K4 ecrites AVANT ce code et avant tout resultat).
#
# HYPOTHESE H7 : dans un monde qui derive continuellement, un petit
# graphe explicable maintenu par dialogue -- UNE phrase par derive,
# ZERO exemple etiquete -- bat durablement le fine-tuning (100 ex./
# derive) et rivalise avec le reentrainement complet (5000 ex./derive),
# sans que l'accumulation des editions ne degrade les regions jamais
# editees (continual par construction).
#
# COMPETITEURS (15 derives, 5 seeds) :
#   frozen    : MLP entraine sur le monde initial, jamais mis a jour.
#   finetune  : MLP + 100 exemples etiquetes frais / derive, 50 epoques.
#   retrain   : MLP reentraine a neuf sur 5000 exemples frais / derive.
#   graph     : liste de regles (32 feuilles distillees de M0) + W-1 :
#               a chaque derive, une phrase ("dans la region <condition
#               de la branche>, c'est desormais la classe c") interpretee
#               sur l'experience NON etiquetee du recepteur (pool de
#               points) : toute regle dont la region de tir est
#               majoritairement dans la region de la phrase est re-classee.
#   graph_n05, graph_n10 : idem, phrases bruitees (seuils +/- 0.05, 0.10).
#   graph_rot : idem, graphe construit en base tournee theta=1.5 (la
#               taxe d'expressibilite -- pont Exp 1-2 <-> Exp 3).
#
# MESURES : accuracy sur le monde courant apres chaque derive ;
#   integrite des regions jamais editees (region par defaut de G*) ;
#   cout de supervision cumule. Conditions de mort K1-K4 evaluees a la fin.
# ---------------------------------------------------------------

import os
import sys

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "core"))
from rex import RuleListModel, edit_rule, random_rotation, rule_membership  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
N_SEEDS = 5
N_DRIFTS = 15
FT_LABELS, RT_LABELS = 100, 5000

# Les 4 branches nommees de G* (predicats (feature, seuil, is_leq)) ;
# la region d'une branche = sa condition MOINS les branches precedentes.
BRANCHES = [
    [(0, 0.6, False), (1, 0.5, False)],   # B1 : taille>0.6 & teinte>0.5
    [(2, 0.7, False)],                    # B2 : forme>0.7
    [(3, 0.3, True), (4, 0.3, True)],     # B3 : px<0.3 & py<0.3
    [(1, 0.2, True), (0, 0.4, True)],     # B4 : teinte<0.2 & taille<0.4
]
INIT_CLASSES = [0, 1, 0, 1]
DEFAULT_CLASS = 2                          # B5 : region par defaut, jamais editee


def branch_masks(X, branch_conds):
    """Masques des regions de branches (avec priorite d'ordre) + defaut."""
    masks, taken = [], np.zeros(len(X), dtype=bool)
    for conds in branch_conds:
        m = rule_membership(conds, X) & ~taken
        masks.append(m)
        taken |= m
    masks.append(~taken)                   # region par defaut
    return masks


def world_labels(X, branch_conds, classes):
    y = np.full(len(X), DEFAULT_CLASS)
    for m, c in zip(branch_masks(X, branch_conds)[:-1], classes):
        y[m] = c
    return y


def jitter_conds(conds, sigma, rng):
    return [(f, thr + rng.normal(0, sigma), le) for f, thr, le in conds]


class LivingGraph:
    """Graphe explicable + W-1 : interprete une phrase sur un pool NON etiquete."""

    def __init__(self, rules, default, basis=None):
        self.G = RuleListModel(rules, default)
        self.basis = basis                 # base du recepteur (None = alignee)

    def view(self, X):
        return X if self.basis is None else X @ self.basis

    def predict(self, X):
        return self.G.predict(self.view(X))

    def apply_sentence(self, region_conds, prior_conds, new_cls, Xpool):
        """"Dans la region <conds> (hors branches precedentes), c'est c."
        Interpretation : toute regle du graphe dont la region de tir
        (estimee sur le pool, dans la base du recepteur) est
        majoritairement dans la region de la phrase est re-classee.
        Zero etiquette consommee."""
        target = rule_membership(region_conds, Xpool)
        for conds in prior_conds:
            target &= ~rule_membership(conds, Xpool)
        fired = self.G.firing_rule(self.view(Xpool))
        n_edits = 0
        for i in range(len(self.G)):
            pts = fired == i
            if pts.sum() >= 5 and target[pts].mean() > 0.5:
                edit_rule(self.G, i, new_cls)
                n_edits += 1
        return n_edits


def run():
    variants = ["graph", "graph_n05", "graph_n10", "graph_rot"]
    methods = ["frozen", "finetune", "retrain"] + variants
    acc = {m: np.zeros((N_SEEDS, N_DRIFTS + 1)) for m in methods}
    integrity = np.zeros((N_SEEDS, N_DRIFTS + 1))    # region par defaut du graphe
    schedule = [(d % 4, None) for d in range(N_DRIFTS)]

    for seed in range(N_SEEDS):
        rng = np.random.default_rng(seed)
        classes = list(INIT_CLASSES)

        Xtr = rng.uniform(0, 1, size=(5000, 5))
        ytr = world_labels(Xtr, BRANCHES, classes)
        M0 = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
        M0.fit(Xtr, ytr)
        Mft = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
        Mft.fit(Xtr, ytr)
        Mrt = M0

        def make_graph(basis):
            V = Xtr if basis is None else Xtr @ basis
            t = DecisionTreeClassifier(max_leaf_nodes=32, random_state=0)
            t.fit(V, M0.predict(Xtr))
            return LivingGraph(RuleListModel.from_tree(t, DEFAULT_CLASS).rules,
                               DEFAULT_CLASS, basis)

        graphs = {"graph": make_graph(None), "graph_n05": make_graph(None),
                  "graph_n10": make_graph(None),
                  "graph_rot": make_graph(random_rotation(5, 1.5, seed=seed + 100))}
        noise = {"graph": 0.0, "graph_n05": 0.05, "graph_n10": 0.10, "graph_rot": 0.0}

        def evaluate(d):
            Xte = np.random.default_rng(1000 + d).uniform(0, 1, size=(2000, 5))
            yte = world_labels(Xte, BRANCHES, classes)
            acc["frozen"][seed, d] = (M0.predict(Xte) == yte).mean()
            acc["finetune"][seed, d] = (Mft.predict(Xte) == yte).mean()
            acc["retrain"][seed, d] = (Mrt.predict(Xte) == yte).mean()
            for v in variants:
                acc[v][seed, d] = (graphs[v].predict(Xte) == yte).mean()
            default_m = branch_masks(Xte, BRANCHES)[-1]
            integrity[seed, d] = (graphs["graph"].predict(Xte[default_m]) == yte[default_m]).mean()

        evaluate(0)
        for d, (k, _) in enumerate(schedule):
            classes[k] = (classes[k] + 1) % 3          # LE MONDE CHANGE

            # graphe(s) : une phrase, zero etiquette
            Xpool = rng.uniform(0, 1, size=(5000, 5))
            for v in variants:
                conds = (jitter_conds(BRANCHES[k], noise[v], rng)
                         if noise[v] else BRANCHES[k])
                graphs[v].apply_sentence(conds, BRANCHES[:k], classes[k], Xpool)

            # fine-tuning : 100 exemples etiquetes frais
            Xft = rng.uniform(0, 1, size=(FT_LABELS, 5))
            yft = world_labels(Xft, BRANCHES, classes)
            for _ in range(50):
                Mft.partial_fit(Xft, yft, classes=[0, 1, 2])

            # reentrainement complet : 5000 exemples etiquetes frais
            Xrt = rng.uniform(0, 1, size=(RT_LABELS, 5))
            yrt = world_labels(Xrt, BRANCHES, classes)
            Mrt = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=1000,
                                random_state=seed)
            Mrt.fit(Xrt, yrt)

            evaluate(d + 1)
        # remet le monde a l'etat initial pour le seed suivant
        print(f"seed {seed} termine")

    # ---------------- rapport ----------------
    mean = {m: acc[m].mean(0) for m in methods}
    std = {m: acc[m].std(0) for m in methods}
    print("\nAccuracy sur le monde courant, apres adaptation (moyenne 5 seeds) :")
    print("derive | " + " | ".join(f"{m:>10}" for m in methods))
    for d in range(N_DRIFTS + 1):
        print(f"{d:6d} | " + " | ".join(f"{mean[m][d]:.3f}".rjust(10) for m in methods))

    print("\nMoyenne sur les derives 1..15 :")
    for m in methods:
        print(f"  {m:10}: {acc[m][:, 1:].mean():.4f} +/- {acc[m][:, 1:].mean(1).std():.4f}")
    last5 = {m: acc[m][:, -5:].mean(1) for m in methods}
    print("\nMoyenne sur les 5 dernieres derives :")
    for m in methods:
        print(f"  {m:10}: {last5[m].mean():.4f} +/- {last5[m].std():.4f}")

    print(f"\nSupervision cumulee : graph = {N_DRIFTS} phrases + 0 etiquette ; "
          f"finetune = {FT_LABELS * N_DRIFTS} etiquettes ; "
          f"retrain = {RT_LABELS * N_DRIFTS} etiquettes.")

    # ---------------- conditions de mort ----------------
    print("\n=== CONDITIONS DE MORT (pre-enregistrees, X-28) ===")
    k1 = last5["graph"].mean() < last5["finetune"].mean()
    print(f"K1 graphe < fine-tuning sur les 5 dernieres derives ? "
          f"{'OUI -> MORT' if k1 else 'non -> SURVIT'} "
          f"({last5['graph'].mean():.4f} vs {last5['finetune'].mean():.4f})")
    drop = integrity[:, 0] - integrity[:, -1]
    k2 = drop.mean() > integrity[:, 0].std() + 1e-12
    print(f"K2 integrite region jamais editee degradee apres 15 editions ? "
          f"{'OUI -> MORT' if k2 else 'non -> SURVIT'} "
          f"(t0 {integrity[:, 0].mean():.4f} -> t15 {integrity[:, -1].mean():.4f})")
    k3 = acc["graph_n10"][:, 1:].mean() <= acc["frozen"][:, 1:].mean()
    print(f"K3 phrases bruitees +/-0.10 <= frozen ? "
          f"{'OUI -> MORT' if k3 else 'non -> SURVIT'} "
          f"({acc['graph_n10'][:, 1:].mean():.4f} vs {acc['frozen'][:, 1:].mean():.4f})")
    k4 = acc["graph_rot"][:, 1:].mean() < acc["frozen"][:, 1:].mean()
    print(f"K4 graphe desaligne (theta=1.5) < frozen ? "
          f"{'OUI -> MORT' if k4 else 'non -> SURVIT'} "
          f"({acc['graph_rot'][:, 1:].mean():.4f} vs {acc['frozen'][:, 1:].mean():.4f})")

    # ---------------- figure ----------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 4.5),
                                  gridspec_kw={"width_ratios": [3, 1]})
    styles = {"frozen": ("#999999", "--"), "finetune": ("#e07b39", "-"),
              "retrain": ("#5b8dd9", "-"), "graph": ("#2a9d5c", "-"),
              "graph_n05": ("#2a9d5c", "--"), "graph_n10": ("#2a9d5c", ":"),
              "graph_rot": ("#b05fa3", "-.")}
    # Noms d'affichage anglais (figures publiques / papier) ; les cles internes restent
    display = {"frozen": "frozen MLP",
               "finetune": f"fine-tuned MLP ({FT_LABELS} labels/drift)",
               "retrain": f"retrained MLP ({RT_LABELS} labels/drift)",
               "graph": "graph + dialogue (1 sentence/drift)",
               "graph_n05": "graph, noisy sentences ±0.05",
               "graph_n10": "graph, noisy sentences ±0.10",
               "graph_rot": "graph, misaligned basis θ=1.5"}
    for m in methods:
        c, ls = styles[m]
        ax.plot(range(N_DRIFTS + 1), mean[m], ls, color=c, label=display[m])
        ax.fill_between(range(N_DRIFTS + 1), mean[m] - std[m], mean[m] + std[m],
                        color=c, alpha=0.10)
    ax.set_xlabel("drift #")
    ax.set_ylabel("accuracy on the current world")
    ax.set_title("Exp 7 — the living graph: one sentence per drift vs. gradient")
    ax.legend(fontsize=8)
    labels_cost = {"graph": 0, "finetune": FT_LABELS * N_DRIFTS,
                   "retrain": RT_LABELS * N_DRIFTS}
    ax2.bar(range(3), [max(v, 1) for v in labels_cost.values()],
            color=["#2a9d5c", "#e07b39", "#5b8dd9"])
    ax2.set_yscale("log")
    ax2.set_xticks(range(3), ["graph", "fine-tune", "retrain"], fontsize=8)
    ax2.set_ylabel("labels consumed (log scale)")
    ax2.set_title("supervision cost")
    fig.tight_layout()
    figpath = os.path.join(HERE, "..", "figures", "exp7_living_graph.png")
    fig.savefig(figpath, dpi=150)
    print(f"\nFigure : {figpath}")

    outdir = os.path.join(HERE, "results")
    os.makedirs(outdir, exist_ok=True)
    np.save(os.path.join(outdir, "exp7.npy"),
            {"acc": {m: acc[m].tolist() for m in methods},
             "integrity": integrity.tolist()}, allow_pickle=True)


if __name__ == "__main__":
    run()
