"""rex — Relational Explainability core library.

Explainability is a property of the relation (M, R, Q), not of the model M.
This package is the first extraction of the engine behind the experiments:

- :mod:`rex.models` — RuleListModel, the explicit decision structure of M
- :mod:`rex.why` — the why-operator W (read direction of the channel)
- :mod:`rex.edit` — the edit operator W⁻¹ (write direction; local by construction)
- :mod:`rex.metrics` — explainability curves and AUC, receiver bases
"""

from .models import RuleListModel, rule_membership
from .why import extract_rule, extract_rules
from .edit import edit_rule, edit_where
from .metrics import fidelity, fidelity_curve, explainability_auc, random_rotation

__version__ = "0.1.0"

__all__ = [
    "RuleListModel",
    "rule_membership",
    "extract_rule",
    "extract_rules",
    "edit_rule",
    "edit_where",
    "fidelity",
    "fidelity_curve",
    "explainability_auc",
    "random_rotation",
    "__version__",
]
