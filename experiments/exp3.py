import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier, _tree

# ---------------------------------------------------------------
# EXPERIENCE 3 -- L'OPERATEUR INVERSE : APPRENDRE PAR LE DIALOGUE
#
# Scenario "concept drift" : le monde change (une regle de G* bascule).
#  - Voie A (notre cadre) : le recepteur corrige le GRAPHE de M par
#    UNE phrase de dialogue -> edition de regle. Cout = 1 interaction.
#  - Voie B (paradigme standard) : le MLP est fine-tune sur n nouveaux
#    exemples etiquetes du nouveau monde. Cout = n exemples.
#  - Mesure : accuracy sur le NOUVEAU monde vs cout d'interaction.
# ---------------------------------------------------------------

def G_star_old(x):
    taille, teinte, forme, px, py = x
    if taille > 0.6 and teinte > 0.5: return 0
    elif forme > 0.7: return 1                       # <- regle qui va changer
    elif px < 0.3 and py < 0.3: return 0
    elif teinte < 0.2 and taille < 0.4: return 1
    else: return 2

def G_star_new(x):
    taille, teinte, forme, px, py = x
    if taille > 0.6 and teinte > 0.5: return 0
    elif forme > 0.7: return 0                       # <- LE MONDE A CHANGE : B -> A
    elif px < 0.3 and py < 0.3: return 0
    elif teinte < 0.2 and taille < 0.4: return 1
    else: return 2

class RuleListModel:
    """Le graphe explicable de M sous forme de liste ordonnee de regles."""
    def __init__(self, rules, default):
        self.rules, self.default = list(rules), default
    def predict(self, X):
        pred = np.full(len(X), self.default)
        assigned = np.zeros(len(X), dtype=bool)
        for conds, cls in self.rules:
            m = np.ones(len(X), dtype=bool)
            for f, thr, le in conds:
                m &= (X[:, f] <= thr) if le else (X[:, f] > thr)
            m &= ~assigned
            pred[m] = cls; assigned |= m
        return pred
    def edit(self, rule_idx, new_cls):
        """L'operateur inverse de W : 'non, dans ce cas c'est A parce que...'"""
        conds, _ = self.rules[rule_idx]
        self.rules[rule_idx] = (conds, new_cls)

def extract_rules(tree):
    """Extraire la liste de regles d'un arbre distille."""
    t = tree.tree_; rules = []
    def rec(node, conds):
        if t.children_left[node] == _tree.TREE_LEAF:
            rules.append((list(conds), int(np.argmax(t.value[node])))); return
        f, thr = t.feature[node], t.threshold[node]
        rec(t.children_left[node], conds + [(f, thr, True)])
        rec(t.children_right[node], conds + [(f, thr, False)])
    rec(0, [])
    return rules

n_seeds = 5
ft_budgets = [10, 30, 100, 300, 1000, 3000]
acc_graph_edit, acc_ft = [], {n: [] for n in ft_budgets}
acc_before = []

for seed in range(n_seeds):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 1, size=(9000, 5))
    y_old = np.array([G_star_old(x) for x in X])
    y_new = np.array([G_star_new(x) for x in X])
    Xtr, Xft, Xte = X[:5000], X[5000:8000], X[8000:]
    ytr_old = y_old[:5000]
    yft_new = y_new[5000:8000]
    yte_new = y_new[8000:]

    # M entraine sur l'ANCIEN monde
    M = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000,
                      random_state=seed, warm_start=True)
    M.fit(Xtr, ytr_old)
    acc_before.append((M.predict(Xte) == yte_new).mean())

    # ----- Voie A : edition du graphe (1 interaction) -----
    ref = DecisionTreeClassifier(max_leaf_nodes=32, random_state=0)
    ref.fit(Xtr, M.predict(Xtr))
    rules = extract_rules(ref)
    G = RuleListModel(rules, default=int(np.bincount(ytr_old).argmax()))

    # Le dialogue : l'utilisateur pointe UN exemple mal classe du nouveau
    # monde et dit "non, ici c'est la classe 0 parce que forme > 0.7".
    # On identifie LA regle responsable (celle qui matche l'exemple et
    # predit l'ancienne classe) et on la corrige. Une regle peut etre
    # fragmentee en plusieurs feuilles -> on corrige toutes les regles
    # dont la condition contient forme>~0.7 et la classe est 1 :
    # c'est UNE phrase ("quand forme>0.7, c'est 0 maintenant").
    n_edits = 0
    for i, (conds, cls) in enumerate(G.rules):
        if cls == 1 and any(f == 2 and not le and thr > 0.55 for f, thr, le in conds):
            G.edit(i, 0); n_edits += 1
    acc_graph_edit.append((G.predict(Xte) == yte_new).mean())

    # ----- Voie B : fine-tuning du MLP sur n exemples du nouveau monde -----
    for n in ft_budgets:
        Mft = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000,
                            random_state=seed)
        # warm start realiste : on repart des poids appris
        Mft.fit(Xtr, ytr_old)
        for _ in range(50):   # 50 epoques de fine-tuning sur les n exemples
            Mft.partial_fit(Xft[:n], yft_new[:n], classes=[0, 1, 2])
        acc_ft[n].append((Mft.predict(Xte) == yte_new).mean())

print(f"Accuracy de M (ancien) sur le NOUVEAU monde : {np.mean(acc_before):.3f} ± {np.std(acc_before):.3f}")
print(f"\nVoie A - edition de graphe (1 phrase de dialogue) : "
      f"{np.mean(acc_graph_edit):.3f} ± {np.std(acc_graph_edit):.3f}")
print("\nVoie B - fine-tuning du MLP :")
for n in ft_budgets:
    print(f"  {n:5d} exemples : {np.mean(acc_ft[n]):.3f} ± {np.std(acc_ft[n]):.3f}")

import os
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(outdir, exist_ok=True)
np.save(os.path.join(outdir, 'exp3.npy'),
        {'before': float(np.mean(acc_before)),
         'graph_edit': [float(np.mean(acc_graph_edit)), float(np.std(acc_graph_edit))],
         'ft_budgets': ft_budgets,
         'ft_mean': [float(np.mean(acc_ft[n])) for n in ft_budgets],
         'ft_std': [float(np.std(acc_ft[n])) for n in ft_budgets]},
        allow_pickle=True)
