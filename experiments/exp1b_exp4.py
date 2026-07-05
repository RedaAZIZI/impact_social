import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier, _tree
from scipy.linalg import expm

def G_star(x):
    taille, teinte, forme, px, py = x
    if taille > 0.6 and teinte > 0.5: return 0
    elif forme > 0.7: return 1
    elif px < 0.3 and py < 0.3: return 0
    elif teinte < 0.2 and taille < 0.4: return 1
    else: return 2

# =====================================================================
# EXP 1b -- DESALIGNEMENT NON LINEAIRE
# Base du recepteur = transformation inversible non lineaire v = tanh(s * W x)
# (W orthogonale aleatoire, s = force de la non-linearite ; s->0 ~ lineaire)
# Comparaison avec la rotation lineaire pure.
# =====================================================================
def rotation_full(theta, seed):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(5, 5)); A = (A - A.T) / 2
    A = A / np.linalg.norm(A, 2)
    return expm(theta * A)

budgets = [2, 4, 8, 16, 32, 64, 128, 256]
n_seeds = 5
conditions = {
    'lineaire θ=1.5': lambda X, s: X @ rotation_full(1.5, seed=s + 100),
    'non-lin. douce (s=2)': lambda X, s: np.tanh(2.0 * (X - 0.5) @ rotation_full(1.5, seed=s + 100)),
    'non-lin. forte (s=6)': lambda X, s: np.tanh(6.0 * (X - 0.5) @ rotation_full(1.5, seed=s + 100)),
}
res = {k: [] for k in conditions}

for seed in range(n_seeds):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 1, size=(6000, 5))
    y = np.array([G_star(x) for x in X])
    Xtr, Xte, ytr = X[:5000], X[5000:], y[:5000]
    M = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
    M.fit(Xtr, ytr)
    yM_tr, yM_te = M.predict(Xtr), M.predict(Xte)
    for name, f in conditions.items():
        Vtr, Vte = f(Xtr, seed), f(Xte, seed)
        fids = []
        for b in budgets:
            t = DecisionTreeClassifier(max_leaf_nodes=b, random_state=0)
            t.fit(Vtr, yM_tr)
            fids.append(t.score(Vte, yM_te))
        res[name].append(fids)

print("=== EXP 1b : desalignement non lineaire (5 seeds) ===")
print("AUC d'explicabilite :")
aucs = {}
for name in conditions:
    arr = np.array(res[name])
    aucs[name] = arr.mean(axis=0)
    print(f"  {name}: {arr.mean():.4f}")

# =====================================================================
# EXP 4 -- L'EXPLICABILITE DEPEND DE LA QUESTION Q
# Pour le graphe de reference de M : taille moyenne de la reponse
# contrastive "pourquoi a plutot que b ?" = nombre de predicats
# divergents entre le chemin de x et le plus proche chemin menant a b.
# =====================================================================
def leaves_with_paths(tree):
    t = tree.tree_; out = []
    def rec(node, conds):
        if t.children_left[node] == _tree.TREE_LEAF:
            out.append((frozenset(conds), int(np.argmax(t.value[node])))); return
        f, thr = t.feature[node], t.threshold[node]
        rec(t.children_left[node], conds + [(f, round(thr, 3), True)])
        rec(t.children_right[node], conds + [(f, round(thr, 3), False)])
    rec(0, [])
    return out

seed = 0
rng = np.random.default_rng(seed)
X = rng.uniform(0, 1, size=(6000, 5))
y = np.array([G_star(x) for x in X])
Xtr, ytr = X[:5000], y[:5000]
M = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=2000, random_state=seed)
M.fit(Xtr, ytr)
ref = DecisionTreeClassifier(max_leaf_nodes=32, random_state=0).fit(Xtr, M.predict(Xtr))
leaves = leaves_with_paths(ref)

classes = [0, 1, 2]
print("\n=== EXP 4 : taille de la reponse contrastive par question Q ===")
print("(nb moyen de predicats divergents, pondere par la couverture des feuilles)")
t = ref.tree_
# couverture de chaque feuille
leaf_id = ref.apply(Xtr)
cover = {}
def leaf_ids(tree):
    t = tree.tree_; ids = []
    def rec(node):
        if t.children_left[node] == _tree.TREE_LEAF: ids.append(node); return
        rec(t.children_left[node]); rec(t.children_right[node])
    rec(0); return ids
ids = leaf_ids(ref)
for i, (conds, cls) in zip(ids, leaves):
    cover[(conds, cls)] = (leaf_id == i).mean()

matrix = {}
for a in classes:
    for b in classes:
        if a == b: continue
        sizes, weights = [], []
        for conds_a, ca in leaves:
            if ca != a: continue
            best = None
            for conds_b, cb in leaves:
                if cb != b: continue
                div = len(conds_a.symmetric_difference(conds_b))
                best = div if best is None else min(best, div)
            if best is not None:
                sizes.append(best); weights.append(cover[(conds_a, ca)])
        matrix[(a, b)] = np.average(sizes, weights=weights) if sizes else None

names = {0: 'A', 1: 'B', 2: 'C'}
for (a, b), v in matrix.items():
    print(f"  pourquoi {names[a]} plutot que {names[b]} ? -> taille moyenne = {v:.2f} predicats")

import os
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(outdir, exist_ok=True)
np.save(os.path.join(outdir, 'exp1b_exp4.npy'),
        {'budgets': budgets,
         'aucs': {k: v.tolist() for k, v in aucs.items()},
         'contrast_matrix': {f"{names[a]}-vs-{names[b]}": float(v) for (a, b), v in matrix.items()}},
        allow_pickle=True)
