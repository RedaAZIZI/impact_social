"""The why-operator W.

``W(x)`` answers "why is x classified c?" with the minimal rule that decides
x in the reference decision structure of M: the decision path of x, i.e. a
conjunction of predicates ``(feature, threshold, is_leq)`` plus the class.

W is the read direction of the explanation channel; :mod:`rex.edit`
implements the write direction W⁻¹.
"""

import numpy as np
from sklearn.tree import _tree

from .models import rule_membership  # noqa: F401  (part of the W vocabulary)


def extract_rule(tree, x):
    """W(x): decision path of ``x`` in a fitted tree → ``(conds, cls)``.

    ``conds`` is the list of predicates along the root-to-leaf path of ``x``
    (minimal by construction: every node on the path was actually tested),
    ``cls`` the class of the reached leaf.
    """
    x = np.asarray(x)
    t = tree.tree_
    node, conds = 0, []
    while t.children_left[node] != _tree.TREE_LEAF:
        f, thr = t.feature[node], t.threshold[node]
        if x[f] <= thr:
            conds.append((f, thr, True))
            node = t.children_left[node]
        else:
            conds.append((f, thr, False))
            node = t.children_right[node]
    cls = int(np.argmax(t.value[node]))
    return conds, cls


def extract_rules(tree):
    """All rules of a fitted tree, in leaf order (see RuleListModel.from_tree)."""
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
    return rules
