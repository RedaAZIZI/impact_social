import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier, _tree
from scipy.linalg import expm

# ---------------------------------------------------------------
# EXPERIENCE 2 -- L'OPERATEUR W ET LA RECONSTRUCTION PAR POURQUOI
#
# Protocole :
#  - M = MLP opaque. Sa structure explicable de reference = arbre
#    haute-fidelite distille dans la base originale ("graphe de M").
#  - W(x) = "pourquoi x est classe c ?" -> renvoie la REGLE
#    (chemin de decision de x dans le graphe de M) : liste de
#    predicats (feature, seuil, direction) + classe.
#  - Le recepteur R reconstruit un modele par questions successives:
#    il choisit un point ou il est en desaccord avec M, pose W,
#    ajoute la regle a sa base de regles, recommence.
#  - R-aligne : stocke la regle telle quelle (meme vocabulaire).
#  - R-pivote : ne voit le monde que dans sa base tournee ; il doit
#    APPROXIMER la region de la regle avec ses propres predicats
#    (petit arbre axis-aligned dans SA base, budget fixe par regle).
#  - Mesure : fidelite a M en fonction du nombre de questions.
# ---------------------------------------------------------------

def G_star(x):
    taille, teinte, forme, px, py = x
    if taille > 0.6 and teinte > 0.5: return 0
    elif forme > 0.7: return 1
    elif px < 0.3 and py < 0.3: return 0
    elif teinte < 0.2 and taille < 0.4: return 1
    else: return 2

def rotation_full(theta, seed):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(5, 5)); A = (A - A.T) / 2
    A = A / np.linalg.norm(A, 2)
    return expm(theta * A)

def extract_rule(tree, x):
    """Operateur W : chemin de decision de x -> liste de (feat, seuil, <=?) + classe."""
    t = tree.tree_
    node, conds = 0, []
    while t.children_left[node] != _tree.TREE_LEAF:
        f, thr = t.feature[node], t.threshold[node]
        if x[f] <= thr:
            conds.append((f, thr, True)); node = t.children_left[node]
        else:
            conds.append((f, thr, False)); node = t.children_right[node]
    cls = int(np.argmax(t.value[node]))
    return conds, cls

def rule_membership(conds, X):
    m = np.ones(len(X), dtype=bool)
    for f, thr, le in conds:
        m &= (X[:, f] <= thr) if le else (X[:, f] > thr)
    return m

class ReceiverAligned:
    """Stocke les regles exactes ; predit par premiere regle qui matche."""
    def __init__(self, default):
        self.rules, self.default = [], default
    def add(self, conds, cls, *_):
        self.rules.append((conds, cls))
    def predict(self, X):
        pred = np.full(len(X), self.default)
        assigned = np.zeros(len(X), dtype=bool)
        for conds, cls in self.rules:
            m = rule_membership(conds, X) & ~assigned
            pred[m] = cls; assigned |= m
        return pred

class ReceiverRotated:
    """Ne voit que X @ R. Approxime chaque region de regle par un petit
    arbre axis-aligned dans SA base (budget par regle)."""
    def __init__(self, default, Rmat, Xpool, budget_per_rule=8):
        self.rules, self.default = [], default
        self.R, self.Xpool = Rmat, Xpool
        self.budget = budget_per_rule
    def add(self, conds, cls, *_):
        member = rule_membership(conds, self.Xpool)
        if member.sum() < 5 or (~member).sum() < 5:
            return
        clf = DecisionTreeClassifier(max_leaf_nodes=self.budget, random_state=0)
        clf.fit(self.Xpool @ self.R, member)
        self.rules.append((clf, cls))
    def predict(self, X):
        Xr = X @ self.R
        pred = np.full(len(X), self.default)
        assigned = np.zeros(len(X), dtype=bool)
        for clf, cls in self.rules:
            m = clf.predict(Xr).astype(bool) & ~assigned
            pred[m] = cls; assigned |= m
        return pred

def run_dialogue(receiver, ref_tree, Xpool, yM_pool, Xte, yM_te, n_questions, rng):
    fids = [(receiver.predict(Xte) == yM_te).mean()]
    for _ in range(n_questions):
        disagree = np.where(receiver.predict(Xpool) != yM_pool)[0]
        if len(disagree) == 0:
            fids.append(fids[-1]); continue
        x = Xpool[rng.choice(disagree)]
        conds, cls = extract_rule(ref_tree, x)      # <- l'operateur W
        receiver.add(conds, cls)
        fids.append((receiver.predict(Xte) == yM_te).mean())
    return fids

# ------------------- boucle multi-seeds -------------------
N_Q, n_seeds, THETA = 15, 5, 1.5
all_aligned, all_rotated = [], []

for seed in range(n_seeds):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 1, size=(6000, 5))
    y = np.array([G_star(x) for x in X])
    Xtr, Xte, ytr = X[:5000], X[5000:], y[:5000]

    M = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
    M.fit(Xtr, ytr)
    yM_tr, yM_te = M.predict(Xtr), M.predict(Xte)

    # Graphe de reference de M (haute fidelite, base originale)
    ref = DecisionTreeClassifier(max_leaf_nodes=32, random_state=0).fit(Xtr, yM_tr)

    default = int(np.bincount(yM_tr).argmax())
    Rmat = rotation_full(THETA, seed=seed + 100)

    ra = ReceiverAligned(default)
    rr = ReceiverRotated(default, Rmat, Xtr, budget_per_rule=8)
    all_aligned.append(run_dialogue(ra, ref, Xtr, yM_tr, Xte, yM_te, N_Q, np.random.default_rng(seed)))
    all_rotated.append(run_dialogue(rr, ref, Xtr, yM_tr, Xte, yM_te, N_Q, np.random.default_rng(seed)))

ma, sa = np.mean(all_aligned, 0), np.std(all_aligned, 0)
mr, sr = np.mean(all_rotated, 0), np.std(all_rotated, 0)

print("Questions | Fidelite R-aligne | Fidelite R-pivote (theta=1.5)")
for q in range(N_Q + 1):
    print(f"{q:9d} | {ma[q]:.3f} ± {sa[q]:.3f}    | {mr[q]:.3f} ± {sr[q]:.3f}")

# Questions necessaires pour fidelite >= 0.90
def q_needed(m, target=0.90):
    idx = np.where(m >= target)[0]
    return idx[0] if len(idx) else None
print(f"\nQuestions pour atteindre 90% : aligne={q_needed(ma)}, pivote={q_needed(mr)}")

import os
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(outdir, exist_ok=True)
np.save(os.path.join(outdir, 'exp2.npy'), {'ma': ma, 'sa': sa, 'mr': mr, 'sr': sr}, allow_pickle=True)
