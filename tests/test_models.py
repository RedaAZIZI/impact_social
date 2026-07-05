import numpy as np
from sklearn.tree import DecisionTreeClassifier

from rex import RuleListModel, rule_membership


def make_world(seed=0, n=2000):
    """The reference synthetic world: 5 attributes, hand-written G*."""
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 1, size=(n, 5))

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

    y = np.array([G_star(x) for x in X])
    return X, y


def test_first_match_semantics_and_default():
    # Two overlapping rules: the first one must win on the overlap.
    rules = [
        ([(0, 0.5, True)], 1),   # x0 <= 0.5 -> 1
        ([(1, 0.5, True)], 2),   # x1 <= 0.5 -> 2 (only where rule 0 didn't fire)
    ]
    m = RuleListModel(rules, default=0)
    X = np.array([
        [0.2, 0.2],  # both match -> first rule -> 1
        [0.8, 0.2],  # only rule 2 -> 2
        [0.8, 0.8],  # none -> default 0
    ])
    assert m.predict(X).tolist() == [1, 2, 0]
    assert m.firing_rule(X).tolist() == [0, 1, -1]


def test_rule_membership():
    conds = [(0, 0.5, True), (1, 0.3, False)]  # x0 <= 0.5 and x1 > 0.3
    X = np.array([[0.4, 0.5], [0.6, 0.5], [0.4, 0.1]])
    assert rule_membership(conds, X).tolist() == [True, False, False]


def test_from_tree_is_exactly_faithful():
    X, y = make_world()
    tree = DecisionTreeClassifier(max_leaf_nodes=32, random_state=0).fit(X, y)
    model = RuleListModel.from_tree(tree, default=int(np.bincount(y).argmax()))
    # The rules partition the space: the rule list reproduces the tree exactly.
    assert (model.predict(X) == tree.predict(X)).all()
    # A tree partition leaves nothing to the default class.
    assert (model.firing_rule(X) >= 0).all()
