"""The edit operator W⁻¹: learning through the explanation channel.

An edit is the receiver pushing a fragment of decision structure back into
the model — "no, in this case it's A, because …". Edits are **local by
construction**: changing the class of rule ``i`` can only affect points whose
firing rule is ``i`` (see ``RuleListModel.firing_rule``), so no regression is
possible outside the edited region. ``tests/test_edit.py`` enforces this
invariant.
"""


def edit_rule(model, rule_idx, new_cls):
    """Set the class of rule ``rule_idx`` to ``new_cls`` (in place).

    Returns the model to allow chaining.
    """
    conds, _ = model.rules[rule_idx]
    model.rules[rule_idx] = (conds, int(new_cls))
    return model


def edit_where(model, matches, new_cls):
    """Apply one semantic sentence to the whole rule list.

    ``matches(conds, cls)`` selects the rules the sentence talks about
    (a concept region may be fragmented into several leaves); every selected
    rule is re-classed to ``new_cls``. Returns the list of edited indices.

    Example (Exp 3, "when forme > 0.7 it's class 0 now")::

        edit_where(G,
                   lambda conds, cls: cls == 1 and
                       any(f == 2 and not le and thr > 0.55 for f, thr, le in conds),
                   new_cls=0)
    """
    edited = []
    for i, (conds, cls) in enumerate(model.rules):
        if matches(conds, cls):
            edit_rule(model, i, new_cls)
            edited.append(i)
    return edited
