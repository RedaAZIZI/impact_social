"""Rule-list models: the explicit, editable decision structure ("graph of M").

A rule is a pair ``(conds, cls)`` where ``conds`` is a list of predicates
``(feature, threshold, is_leq)`` — feature index, threshold value, and the
direction of the test (``x[feature] <= threshold`` when ``is_leq`` is True,
``x[feature] > threshold`` otherwise) — and ``cls`` is the predicted class.

A :class:`RuleListModel` is an ordered list of such rules with first-match
semantics and a default class. It is the target structure of the why-operator
W (see :mod:`rex.why`) and the substrate of the edit operator W⁻¹
(see :mod:`rex.edit`).
"""

import numpy as np
from sklearn.tree import _tree


def rule_membership(conds, X):
    """Boolean mask of the rows of ``X`` satisfying every predicate in ``conds``."""
    X = np.asarray(X)
    m = np.ones(len(X), dtype=bool)
    for f, thr, le in conds:
        m &= (X[:, f] <= thr) if le else (X[:, f] > thr)
    return m


class RuleListModel:
    """Ordered rule list with first-match semantics.

    Parameters
    ----------
    rules : list of (conds, cls)
        Ordered rules; the first rule whose conditions match a point decides it.
    default : int
        Class predicted when no rule matches.
    """

    def __init__(self, rules, default):
        self.rules = list(rules)
        self.default = int(default)

    def __len__(self):
        return len(self.rules)

    @classmethod
    def from_tree(cls, tree, default):
        """Extract the full ordered rule list of a fitted decision tree.

        The rules partition the input space, so the resulting model
        reproduces the tree's predictions exactly.
        """
        t = tree.tree_
        rules = []

        def rec(node, conds):
            if t.children_left[node] == _tree.TREE_LEAF:
                rules.append((list(conds), int(np.argmax(t.value[node]))))
                return
            f, thr = t.feature[node], t.threshold[node]
            rec(t.children_left[node], conds + [(f, thr, True)])
            rec(t.children_right[node], conds + [(f, thr, False)])

        rec(0, [])
        return cls(rules, default)

    def firing_rule(self, X):
        """Index of the rule that decides each row of ``X`` (-1 = default).

        This is the locality map of the model: an edit of rule ``i`` can only
        change predictions where ``firing_rule(X) == i``.
        """
        X = np.asarray(X)
        fired = np.full(len(X), -1)
        assigned = np.zeros(len(X), dtype=bool)
        for i, (conds, _) in enumerate(self.rules):
            m = rule_membership(conds, X) & ~assigned
            fired[m] = i
            assigned |= m
        return fired

    def predict(self, X):
        X = np.asarray(X)
        pred = np.full(len(X), self.default)
        assigned = np.zeros(len(X), dtype=bool)
        for conds, c in self.rules:
            m = rule_membership(conds, X) & ~assigned
            pred[m] = c
            assigned |= m
        return pred
