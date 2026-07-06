import numpy as np
from sklearn.tree import DecisionTreeClassifier

from rex import RuleListModel, extract_rule, extract_rules, rule_membership
from test_models import make_world


def test_extract_rule_answers_why():
    X, y = make_world()
    tree = DecisionTreeClassifier(max_leaf_nodes=32, random_state=0).fit(X, y)
    rng = np.random.default_rng(1)
    for x in X[rng.choice(len(X), 20, replace=False)]:
        conds, cls = extract_rule(tree, x)
        # The rule explains x itself: x satisfies its own explanation ...
        assert rule_membership(conds, x[None, :])[0]
        # ... and the explanation predicts what M predicts.
        assert cls == tree.predict(x[None, :])[0]


def test_extract_rules_matches_from_tree():
    X, y = make_world()
    tree = DecisionTreeClassifier(max_leaf_nodes=16, random_state=0).fit(X, y)
    rules = extract_rules(tree)
    model = RuleListModel(rules, default=0)
    assert (model.predict(X) == tree.predict(X)).all()
