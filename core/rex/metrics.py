"""Explainability measurement: fidelity curves and their AUC.

The explainability of M relative to a receiver R is read off the
**explainability curve**: best fidelity to M achievable by an axis-aligned
decision structure *expressed in R's basis*, as a function of the structure
budget (number of leaves). Its AUC is the scalar signature used throughout
the paper (Exp 1: AUC 0.918 at θ=0 → 0.745 at θ=1.5).
"""

import numpy as np
from scipy.linalg import expm
from sklearn.tree import DecisionTreeClassifier


def fidelity(pred_a, pred_b):
    """Agreement rate between two prediction vectors."""
    return float(np.mean(np.asarray(pred_a) == np.asarray(pred_b)))


def random_rotation(dim, theta, seed):
    """Receiver basis of misalignment strength ``theta``.

    A random antisymmetric matrix A is normalised (largest angular velocity
    = 1) and the basis is R = expm(theta·A): theta=0 → identity,
    large theta → full mixing of the dimensions.
    """
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(dim, dim))
    A = (A - A.T) / 2
    A = A / np.linalg.norm(A, 2)
    return expm(theta * A)


def fidelity_curve(Xtr, yM_tr, Xte, yM_te, budgets, basis=None, seed=0):
    """Fidelity to M of distilled trees vs structure budget, in a receiver basis.

    Parameters
    ----------
    Xtr, Xte : arrays
        Train/test inputs (in M's original coordinates).
    yM_tr, yM_te : arrays
        M's predictions on Xtr/Xte (the labels being explained).
    budgets : sequence of int
        Tree sizes (max leaf nodes) to sweep.
    basis : array or None
        Receiver basis matrix; inputs are viewed as ``X @ basis``.
        None = identity (the degenerate, perfectly aligned case).

    Returns
    -------
    np.ndarray of fidelities, one per budget.
    """
    Vtr = np.asarray(Xtr) if basis is None else np.asarray(Xtr) @ basis
    Vte = np.asarray(Xte) if basis is None else np.asarray(Xte) @ basis
    fids = []
    for b in budgets:
        t = DecisionTreeClassifier(max_leaf_nodes=int(b), random_state=seed)
        t.fit(Vtr, yM_tr)
        fids.append(t.score(Vte, yM_te))
    return np.array(fids)


def explainability_auc(fidelities):
    """Scalar explainability signature: mean fidelity over the budget sweep."""
    return float(np.mean(np.asarray(fidelities)))
