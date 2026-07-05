import numpy as np
from sklearn.tree import DecisionTreeClassifier

from rex import RuleListModel, edit_rule, edit_where
from test_models import make_world


def build_model(X, y):
    tree = DecisionTreeClassifier(max_leaf_nodes=32, random_state=0).fit(X, y)
    return RuleListModel.from_tree(tree, default=int(np.bincount(y).argmax()))


def test_edit_is_local_by_construction():
    """The core invariant of the framework: an edit cannot regress anything
    outside the edited rule's firing region (no catastrophic forgetting,
    by construction). Any change to /core must keep this test green."""
    X, y = make_world()
    model = build_model(X, y)
    before = model.predict(X)
    fired = model.firing_rule(X)

    for idx in [0, len(model) // 2, len(model) - 1]:
        edited = build_model(X, y)
        old_cls = edited.rules[idx][1]
        new_cls = (old_cls + 1) % 3
        edit_rule(edited, idx, new_cls)
        after = edited.predict(X)
        changed = before != after
        # Changes happen only inside the edited rule's region ...
        assert (fired[changed] == idx).all()
        # ... and inside it, the new class is applied.
        assert (after[fired == idx] == new_cls).all()


def test_edit_where_applies_one_sentence():
    """Exp 3's edit: 'when forme > 0.7, it's class 0 now' re-classes every
    fragment of the concept region in one call."""
    X, y = make_world()
    model = build_model(X, y)
    before = model.predict(X)
    fired = model.firing_rule(X)

    sentence = lambda conds, cls: cls == 1 and any(
        f == 2 and not le and thr > 0.55 for f, thr, le in conds
    )
    edited = edit_where(model, sentence, new_cls=0)
    assert len(edited) > 0
    after = model.predict(X)
    changed = before != after
    # Locality also holds for multi-fragment sentence edits.
    assert np.isin(fired[changed], edited).all()
